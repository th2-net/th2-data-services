import pickle
import requests
import json
from requests.exceptions import ConnectionError
from urllib3 import PoolManager
from urllib3.exceptions import HTTPError
from functools import partial
from weakref import finalize
from pathlib import Path
from datetime import datetime
from csv import DictReader
from pprint import pformat
from typing import Generator, Iterable, List, Union, Optional
from urllib.parse import urlencode, urlparse
from sseclient import SSEClient
from th2_data_services.data import Data


class DataSource:
    def __init__(self, url, chunk_length: int = 65536):
        self.url = url
        self._finalizer = finalize(self, self.remove)
        self.__chunk_length = chunk_length

        self.__check_connect()

    def __check_connect(self) -> None:
        """Checks whether url is working."""
        try:
            requests.get(self.__url)
        except ConnectionError as error:
            raise HTTPError("We can't create a connection at this URL. Please check the URL.")

    def remove(self):
        """Deconstructor of class."""
        filename = urlparse(self.__url).netloc
        path = Path("./").joinpath("temp")
        if path.exists():
            for file in path.iterdir():
                current_file = str(file)
                if filename in current_file:
                    file.unlink()

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        if url[-1] == "/":
            url = url[:-1]
        self.__url = url

    def sse_request_to_data_provider(self, **kwargs) -> Generator[dict, None, None]:
        """Sends SSE request. For create custom sse-request to data-provider
        use this readme https://github.com/th2-net/th2-rpt-data-provider .

        :param kwargs: Query options.
        :return: SSE response data.
        """
        route = kwargs.get("route")
        if not route:
            raise ValueError("Route is required field. Please fill it.")

        if kwargs.get("startTimestamp") and isinstance(kwargs.get("startTimestamp"), datetime):
            kwargs["startTimestamp"] = int(kwargs["startTimestamp"].timestamp() * 1000)  # unix timestamp in milliseconds
        if kwargs.get("endTimestamp") and isinstance(kwargs.get("endTimestamp"), datetime):
            kwargs["endTimestamp"] = int(kwargs["endTimestamp"].timestamp() * 1000)

        url = self.__url + route
        url = f"{url}?{urlencode(kwargs)}"

        yield from self.__execute_sse_request(url)

    def get_events_from_data_provider(self, cache=False, **kwargs) -> Data:
        """Sends SSE request for events. For help use this readme
        https://github.com/th2-net/th2-rpt-data-provider#sse-requests-api
        on route http://localhost:8080/search/sse/events.

        :param cache: Flag if you what save to cache.
        :param kwargs: Query options.
        :return: Events.
        """
        if not kwargs.get("startTimestamp") and not kwargs.get("resumeFromId"):
            raise ValueError(
                "'startTimestamp' or 'resumeFromId' must not be null for route /search/sse/events. Please note it. "
                "More information on request here: https://github.com/th2-net/th2-rpt-data-provider"
            )
        if isinstance(kwargs["startTimestamp"], datetime):
            kwargs["startTimestamp"] = int(kwargs["startTimestamp"].timestamp() * 1000)  # unix timestamp in milliseconds

        if kwargs.get("endTimestamp") and isinstance(kwargs.get("endTimestamp"), datetime):
            kwargs["endTimestamp"] = int(kwargs["endTimestamp"].timestamp() * 1000)

        url = self.__url + "/search/sse/events"
        url = f"{url}?{urlencode(kwargs)}"

        filename = None
        if cache:
            filename = urlparse(self.__url).netloc + f"_events_{urlencode(kwargs)}"
            filename = f"{filename}.pickle"

        if filename and self.__check_cache(filename):
            data = self.__load_file(filename)
        else:
            data = partial(self.__load_from_provider, url, filename if cache else None)
        return Data(data)

    def get_messages_from_data_provider(self, cache: bool = False, **kwargs) -> Data:
        """Sends SSE request for messages. For help use this readme
        https://github.com/th2-net/th2-rpt-data-provider#sse-requests-api
        on route http://localhost:8080/search/sse/messages.

        :param cache: Flag if you what save to cache.
        :param kwargs: Query options.
        :return: Messages.
        """
        if not kwargs.get("startTimestamp") and not kwargs.get("resumeFromId"):
            raise ValueError(
                "'startTimestamp' or 'resumeFromId' must not be null for route /search/sse/messages. Please note it. "
                "More information on request here: https://github.com/th2-net/th2-rpt-data-provider"
            )
        if not kwargs.get("stream"):
            raise ValueError("'stream' is required field. Please note it." "More information on request here: https://github.com/th2-net/th2-rpt-data-provider")

        if isinstance(kwargs["startTimestamp"], datetime):
            kwargs["startTimestamp"] = int(kwargs["startTimestamp"].timestamp() * 1000)  # unix timestamp in milliseconds

        if kwargs.get("endTimestamp") and isinstance(kwargs.get("endTimestamp"), datetime):
            kwargs["endTimestamp"] = int(kwargs["endTimestamp"].timestamp() * 1000)

        streams = kwargs.pop("stream")
        if isinstance(streams, (list, tuple)):
            streams = f"&stream=".join(streams)
        streams = f"&stream={streams}"

        url = self.__url + "/search/sse/messages"
        url = f"{url}?{urlencode(kwargs) + streams}"

        filename = None
        if cache:
            filename = urlparse(self.__url).netloc + f"_messages_{urlencode(kwargs)}"
            filename = f"{filename}.pickle"

        if filename and self.__check_cache(filename):
            data = self.__load_file(filename)
        else:
            data = partial(self.__load_from_provider, url, filename)
        return Data(data)

    def __check_cache(self, filename: str) -> bool:
        """Checks whether file exist.

        :param filename: Filename.
        :return: File exists or not.
        """
        path = Path("./temp")
        path.mkdir(exist_ok=True)
        path = path.joinpath(filename)
        return path.is_file()

    def __load_file(self, filename: str) -> Generator[dict, None, None]:
        """Loads records from pickle file.

        :param filename: Filename.
        :return: Generator records.
        """
        path = Path("./").joinpath("temp").joinpath(filename)
        if not path.is_file():
            raise ValueError(f"{filename} isn't file.")

        if path.suffix != ".pickle":
            raise ValueError(f"File hasn't pickle extension.")

        with open(path, "rb") as file:
            while True:
                try:
                    decoded_data = pickle.load(file)
                    yield decoded_data
                except EOFError:
                    break

    def __load_from_provider(self, url: str, filename: str = None) -> Generator[dict, None, None]:
        """Loads records from data provider.

        :param url: Url.
        :param filename: Filename if you what to create local storage.
        :return: Generator records.
        """
        file = None
        if filename is not None:
            path = Path("./").joinpath("temp").joinpath(filename)
            file = open(path, "wb")

        for record in self.__execute_sse_request(url):
            if file is not None:
                pickle.dump(record, file)
            yield record

        if file:
            file.close()

    def __execute_sse_request(self, url: str):
        """Creates SSE connection to server.

        :param url: Url.
        :return: Response data.
        """
        response = self.__create_stream_connection(url)
        client = SSEClient(response)
        for record in client.events():
            if record.event == "error":
                raise HTTPError(record.data)
            if record.event not in ["close", "keep_alive"]:
                record_data = json.loads(record.data)
                yield record_data

    def __create_stream_connection(self, url: str):
        """Create stream connection.

        :param url: Url.
        :return: Response stream data.
        """
        headers = {"Accept": "text/event-stream"}
        http = PoolManager()
        response = http.request(method="GET", url=url, headers=headers, preload_content=False)

        for chunk in response.stream(self.__chunk_length):
            yield chunk

        response.release_conn()

    def find_messages_by_id_from_data_provider(self, messages_id: Union[Iterable, str]) -> Optional[Union[List[dict], dict]]:
        """Gets messages by ids using URL request.

        :param messages_id: Messages id.
        :return: List[Message_dict] if you request a list or Message_dict.
        """
        if isinstance(messages_id, str):
            messages_id = [messages_id]
        result = []
        for msg_id in messages_id:
            response = requests.get(f"{self.__url}/message/{msg_id}")
            try:
                result.append(response.json())
            except json.JSONDecodeError:
                raise ValueError(f"Sorry, but the answer rpt-data-provider doesn't match the json format.\n" f"Answer:{response.text}")
        return result if len(result) > 1 else result[0] if result else None

    def find_events_by_id_from_data_provider(self, events_id: Union[Iterable, str]) -> Optional[Union[List[dict], dict]]:
        """Gets events by ids using URL request.

        :param events_id: Events id.
        :return: List[Event_dict] if you request a list or Event_dict.
        """
        if isinstance(events_id, str):
            events_id = [events_id]
        events = "&".join([f"ids={id_}" for id_ in events_id])
        response = requests.get(f"{self.__url}/events/?{events}")
        try:
            answer = response.json()
        except json.JSONDecodeError:
            raise ValueError(f"Sorry, but the answer rpt-data-provider doesn't match the json format.\n" f"Answer:{response.text}")
        return answer if len(answer) > 1 else answer[0] if answer else None

    @staticmethod
    def read_csv_file(*sources: str) -> Generator[str, None, None]:
        """Gets data from csv files.

        :param sources: Path to files.
        :return: Csv files payload.
        """
        for source in sources:
            with open(source) as data:
                for message in DictReader(data):
                    yield dict(message)

    @staticmethod
    def write_to_txt(data: Generator[str, None, None], source: str) -> None:
        """Writes to txt files.

        :param data: Data.
        :param source: Path to file.
        """
        with open(source, "w") as txt_file:
            for record in data:
                txt_file.write(f"{pformat(record)}\n" + ("-" * 50) + "\n")
