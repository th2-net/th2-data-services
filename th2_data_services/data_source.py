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
from typing import Generator, Iterable, List, Union, Optional
from urllib.parse import urlencode, urlparse
from sseclient import SSEClient
from th2_data_services.data import Data


class DataSource:
    """The class that provides methods for getting messages and events from rpt-data-provider."""

    def __init__(self, url: str, chunk_length: int = 65536):
        self.url = url
        self._finalizer = finalize(self, self.__remove)
        self.__chunk_length = chunk_length
        self.__check_connect()

    def __check_connect(self) -> None:
        """Checks whether url is working."""
        try:
            requests.get(self.__url, timeout=3.0)
        except ConnectionError as error:
            raise HTTPError(f"Unable to connect to host '{self.__url}'.")

    def __remove(self):
        """Deconstructor of class."""
        filename = urlparse(self.__url).netloc
        path = Path("./").joinpath("temp")
        if path.exists():
            for file in path.iterdir():
                current_file = str(file)
                if filename in current_file:
                    file.unlink()

    @property
    def url(self) -> str:
        """str: URL of rpt-data-provider."""
        return self.__url

    @url.setter
    def url(self, url):
        if url[-1] == "/":
            url = url[:-1]
        self.__url = url

    def sse_request_to_data_provider(self, **kwargs) -> Generator[dict, None, None]:
        """Sends SSE request to rpt-data-provider.

        It used for create custom sse-request to data-provider
        use this readme https://github.com/th2-net/th2-rpt-data-provider#readme.

        Args:
            kwargs: Query options.

        Yields:
            dict: SSE response data.

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

    def get_events_from_data_provider(self, cache: bool = False, **kwargs) -> Data:
        """Sends SSE request for getting events.

        For help use this readme
        https://github.com/th2-net/th2-rpt-data-provider#sse-requests-api
        on route http://localhost:8080/search/sse/events.

        Args:
            cache (bool): If True all requested data from rpt-data-provider will be saved to cache.
                (See `use_cache` method in `Data` class).
            kwargs: th2-rpt-data-provider API query options.

        Returns:
            Data: Data object with Events.

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

        data = partial(self.__load_data, url, cache)
        return Data(data)

    def get_messages_from_data_provider(self, cache: bool = False, **kwargs) -> Data:
        """Sends SSE request for getting messages.

        For help use this readme
        https://github.com/th2-net/th2-rpt-data-provider#sse-requests-api
        on route http://localhost:8080/search/sse/messages.

        Args:
            cache (bool): If True all requested data from rpt-data-provider will be saved to cache.
                (See `use_cache` method in `Data` class).
            kwargs: th2-rpt-data-provider API query options.

        Returns:
            Data: Data object with Messages.

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

        data = partial(self.__load_data, url, cache)
        return Data(data)

    def __load_data(self, url: str, cache: bool = False):
        """Loads data from cache or provider.

        Args:
            url: Url.
            cache: Flag if you what save to cache.

        Returns:
             obj: Generator
        """
        filename = None
        if cache:
            filename = "__".join(url.split("/")[2:])
            filename = f"{filename}.pickle"

        if filename and self.__check_cache(filename):
            data = self.__load_file(filename)
        else:
            data = self.__load_from_provider(url, filename)
        return data

    def __check_cache(self, filename: str) -> bool:
        """Checks whether file exist.

        Args:
            filename: Name of the cache file.

        Returns:
            bool: File exists or not.

        """
        path = Path("./temp")
        path.mkdir(exist_ok=True)
        path = path.joinpath(filename)
        return path.is_file()

    def __load_file(self, filename: str) -> Generator[dict, None, None]:
        """Loads records from pickle file.

        Args:
            filename: Name of the cache file.

        Yields:
            dict: Generator records.

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

        Args:
            url: Url.
            filename: Filename if you what to create local storage.

        Yields:
            dict: Generator records.

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

        Args:
            url: Url.

        Returns:
            dict: Response data.

        """
        response = self.__create_stream_connection(url)
        client = SSEClient(response)
        for record in client.events():
            if record.event == "error":
                raise HTTPError(record.data)
            if record.event not in ["close", "keep_alive", "messageIds"]:
                record_data = json.loads(record.data)
                yield record_data

    def __create_stream_connection(self, url: str):
        """Create stream connection.

        Args:
            url: Url.

        Yields:
            str: Response stream data.

        """
        headers = {"Accept": "text/event-stream"}
        http = PoolManager()
        response = http.request(method="GET", url=url, headers=headers, preload_content=False)

        for chunk in response.stream(self.__chunk_length):
            yield chunk

        response.release_conn()

    def find_messages_by_id_from_data_provider(self, messages_id: Union[Iterable, str]) -> Optional[Union[List[dict], dict]]:
        """Gets message/messages by ids.

        Args:
            messages_id: One str with MessageID or list of MessagesIDs.

        Returns:
            List[Message_dict] if you request a list or Message_dict.

        Example:
            >>> How to use.

            >>> data_source.find_messages_by_id_from_data_provider('demo-conn1:first:1619506157132265837')
            Returns 1 message (dict).

            >>> data_source.find_messages_by_id_from_data_provider(['demo-conn1:first:1619506157132265836'])
            Returns list(dict) with 1 message.

            >>> data_source.find_messages_by_id_from_data_provider([
                'demo-conn1:first:1619506157132265836',
                'demo-conn1:first:1619506157132265833',
            ])
            Returns list(dict) with 2 messages.

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
        """Gets event/events by ids.

        Args:
            events_id: One str with EventID or list of EventsIDs.

        Returns:
            List[Event_dict] if you request a list or Event_dict.

        Example:
            >>> How to use.

            >>> data_source.find_events_by_id_from_data_provider('8bc787fe-d1b4-11eb-bae5-57b0c4472880')
            Returns 1 message (dict).

            >>> data_source.find_events_by_id_from_data_provider(['8bc787fe-d1b4-11eb-bae5-57b0c4472880'])
            Returns list(dict) with 1 event.

            >>> data_source.find_events_by_id_from_data_provider([
                '8bc787fe-d1b4-11eb-bae5-57b0c4472880',
                '6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e',
            ])
            Returns list(dict) with 2 events.

        """
        if isinstance(events_id, str):
            events_id = [events_id]
        result = []
        for event_id in events_id:
            response = requests.get(f"{self.__url}/event/{event_id}")
            try:
                result.append(response.json())
            except json.JSONDecodeError:
                raise ValueError(f"Sorry, but the answer rpt-data-provider doesn't match the json format.\n" f"Answer:{response.text}")
        return result if len(result) > 1 else result[0] if result else None

    @staticmethod
    def read_csv_file(*sources: str) -> Generator[str, None, None]:
        """Gets data in a stream way from csv files.

        Args:
            sources: Path to files.

        Yields:
            dict: Csv files payload.

        """
        for source in sources:
            with open(source) as data:
                for message in DictReader(data):
                    yield dict(message)
