from datetime import datetime

import requests
import json
from csv import DictReader
from pprint import pformat
from typing import Generator, List
from urllib.parse import urlencode
from sseclient import SSEClient


class DataSources:
    def __init__(self, host):
        self.host = host

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, host):
        if host[-1] == "/":
            host = host[:-1]
        self.__host = host

    def sse_request_to_data_provider(self, **kwargs) -> Generator[dict, None, None]:
        """Sends SSE request.

        :param kwargs: Query options.
        :return: SSE response data.
        """
        route = kwargs.get("route")
        if not route:
            raise ValueError("Route is required field. Please fill it.")

        if kwargs.get("startTimestamp") and isinstance(
            kwargs.get("startTimestamp"), datetime
        ):
            kwargs["startTimestamp"] = int(
                kwargs["startTimestamp"].timestamp() * 1000
            )  # unix timestamp in milliseconds
        if kwargs.get("endTimestamp") and isinstance(
            kwargs.get("endTimestamp"), datetime
        ):
            kwargs["endTimestamp"] = int(kwargs["endTimestamp"].timestamp() * 1000)

        url = self.__host + route
        url = f"{url}?{urlencode(kwargs)}"

        yield from self.__sse_request(url)

    def get_events_from_data_provider(self, **kwargs):
        """Sends SSE request for events.

        :param kwargs: Query options.
        :return: Events.
        """
        if not kwargs.get("startTimestamp") and not kwargs.get("resumeFromId"):
            raise ValueError(
                "'startTimestamp' or 'resumeFromId' must not be null for route /search/sse/events. Please note it. "
                "More information on request here: https://github.com/th2-net/th2-rpt-data-provider"
            )
        if isinstance(kwargs["startTimestamp"], datetime):
            kwargs["startTimestamp"] = int(
                kwargs["startTimestamp"].timestamp() * 1000
            )  # unix timestamp in milliseconds

        if kwargs.get("endTimestamp") and isinstance(
            kwargs.get("endTimestamp"), datetime
        ):
            kwargs["endTimestamp"] = int(kwargs["endTimestamp"].timestamp() * 1000)

        url = self.__host + "/search/sse/events"
        url = f"{url}?{urlencode(kwargs)}"

        yield from self.__sse_request(url)

    def get_messages_from_data_provider(self, **kwargs):
        """Sends SSE request for messages.

        :param kwargs: Query options.
        :return: Messages.
        """
        if not kwargs.get("startTimestamp") and not kwargs.get("resumeFromId"):
            raise ValueError(
                "'startTimestamp' or 'resumeFromId' must not be null for route /search/sse/messages. Please note it. "
                "More information on request here: https://github.com/th2-net/th2-rpt-data-provider"
            )
        if not kwargs.get("stream"):
            raise ValueError(
                "'stream' is required field. Please note it."
                "More information on request here: https://github.com/th2-net/th2-rpt-data-provider"
            )

        if isinstance(kwargs["startTimestamp"], datetime):
            kwargs["startTimestamp"] = int(
                kwargs["startTimestamp"].timestamp() * 1000
            )  # unix timestamp in milliseconds

        if kwargs.get("endTimestamp") and isinstance(
            kwargs.get("endTimestamp"), datetime
        ):
            kwargs["endTimestamp"] = int(kwargs["endTimestamp"].timestamp() * 1000)

        streams = kwargs.pop("stream")
        if isinstance(streams, (list, tuple)):
            streams = f"&stream=".join(streams)
        streams = f"&stream={streams}"

        url = self.__host + "/search/sse/messages"
        url = f"{url}?{urlencode(kwargs) + streams}"

        yield from self.__sse_request(url)

    @staticmethod
    def __sse_request(url):
        """Creates sse connection to server.

        :param url: Url.
        :return: Response data.
        """
        headers = {"Accept": "text/event-stream"}

        response = requests.get(url, stream=True, headers=headers)
        client = SSEClient(response)
        for record in client.events():
            if record.id:
                record_data = json.loads(record.data)
                yield record_data

    def find_messages_by_id_from_data_provider(
        self, messages_id: List[str]
    ) -> Generator[dict, None, None]:
        """Gets messages by ids.

        :param messages_id: Messages id.
        :return: Messages.
        """
        for message_id in messages_id:
            response = requests.get(f"{self.__host}/message/{message_id}")
            yield response.json()

    def find_events_by_id_from_data_provider(self, events_id: List[str]) -> dict:
        """Gets events by ids.

        :param events_id: Events id.
        :return: Events.
        """
        events = "&".join([f"ids={id_}" for id_ in events_id])

        response = requests.get(f"{self.__host}/events/?{events}")
        answer = response.json()
        return answer

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
