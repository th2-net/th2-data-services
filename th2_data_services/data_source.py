import requests
import json
import simplejson
import urllib3.exceptions
from itertools import chain
from requests.exceptions import ConnectionError
from urllib3 import PoolManager
from urllib.parse import quote
from functools import partial
from datetime import datetime, timezone
from csv import DictReader
from typing import Generator, Iterable, List, Union, Optional, Callable
from th2_data_services.sseclient import SSEClient

from th2_data_services.adapters import adapter_provider5, adapter_sse
from th2_data_services.data import Data
from http import HTTPStatus
from th2_data_services.filter import Filter
from th2_data_services.decode_error_handler import UNICODE_REPLACE_HANDLER

import logging

logger = logging.getLogger("th2_data_services")
logger.setLevel(logging.DEBUG)


class DataSource:
    """The class that provides methods for getting messages and events from rpt-data-provider."""

    def __init__(
        self,
        url: str,
        chunk_length: int = 65536,
        char_enc: str = "utf-8",
        decode_error_handler: str = UNICODE_REPLACE_HANDLER,
    ):
        """

        Args:
            url: HTTP data source url.
            chunk_length: How much of the content to read in one chunk.
            char_enc: Encoding for the byte stream.
            decode_error_handler: Registered decode error handler.
        """
        self.url = url
        self._char_enc = char_enc
        self._decode_error_handler = decode_error_handler
        self.__chunk_length = chunk_length
        self.__check_connect()
        logger.info(url)

    def __check_connect(self) -> None:
        """Checks whether url is working."""
        try:
            requests.get(self.__url, timeout=5.0)
        except ConnectionError as error:
            raise urllib3.exceptions.HTTPError(f"Unable to connect to host '{self.__url}'\nReason: {error}")

    @property
    def url(self) -> str:
        """str: URL of rpt-data-provider."""
        return self.__url

    @url.setter
    def url(self, url):
        if url[-1] == "/":
            url = url[:-1]
        self.__url = url

    def __get_data_obj(
        self,
        url: str,
        sse_adapter_flag: bool,
        provider_adapter: Optional[Callable],
        cache: bool,
    ) -> Data:
        data = partial(self.__execute_sse_request, url)

        if sse_adapter_flag:
            if provider_adapter is not None:
                data_obj = Data(data).map(adapter_sse).map(provider_adapter).use_cache(cache)
            else:
                data_obj = Data(data).map(adapter_sse).use_cache(cache)
        else:
            if provider_adapter is not None:
                raise Exception(f"Provider adapter expected to get dict but SSE adapter is turned off")
            else:
                data_obj = Data(data).use_cache(cache)

        return data_obj

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
            exception_msg = "Route is required field. Please fill it."
            logger.error(exception_msg)
            raise ValueError(exception_msg)

        if kwargs.get("startTimestamp") and isinstance(kwargs.get("startTimestamp"), datetime):
            timestamp = kwargs["startTimestamp"].replace(tzinfo=timezone.utc).timestamp()
            kwargs["startTimestamp"] = int(timestamp * 1000)  # unix timestamp in milliseconds
        if kwargs.get("endTimestamp") and isinstance(kwargs.get("endTimestamp"), datetime):
            timestamp = kwargs["endTimestamp"].replace(tzinfo=timezone.utc).timestamp()
            kwargs["endTimestamp"] = int(timestamp * 1000)

        url = self.__url + route
        url = f"{url}?{self._get_url(kwargs)}"
        logger.info(url)
        yield from self.__execute_sse_request(url)

    def get_events_from_data_provider(self, cache: bool = False, sse_adapter: bool = True, **kwargs) -> Data:
        """Sends SSE request for getting events.

        For help use this readme
        https://github.com/th2-net/th2-rpt-data-provider#sse-requests-api
        on route http://localhost:8080/search/sse/events.

        Args:
            cache (bool): If True, all requested data from rpt-data-provider will be saved to cache.
            sse_adapter (bool): If True, all data will go through SSE adapter and yield dicts.
                Otherwise adapter will yield SSE Events.
            kwargs: th2-rpt-data-provider API query options.

        Returns:
            Data: Data object with Events.

        """

        if kwargs.get("metadataOnly") and kwargs["metadataOnly"] is True:
            logger.warning(f"Meta data status is {kwargs['metadataOnly']}")
        kwargs["metadataOnly"] = False

        if not kwargs.get("startTimestamp") and not kwargs.get("resumeFromId"):
            exception_msg = (
                "'startTimestamp' or 'resumeFromId' must not be null for route /search/sse/events. Please "
                "note it. More information on request here: "
                "https://github.com/th2-net/th2-rpt-data-provider "
            )
            logger.error(exception_msg)
            raise ValueError(exception_msg)

        if isinstance(kwargs["startTimestamp"], datetime):
            timestamp = kwargs["startTimestamp"].replace(tzinfo=timezone.utc).timestamp()
            kwargs["startTimestamp"] = int(timestamp * 1000)  # unix timestamp in milliseconds

        if kwargs.get("endTimestamp") and isinstance(kwargs.get("endTimestamp"), datetime):
            timestamp = kwargs["endTimestamp"].replace(tzinfo=timezone.utc).timestamp()
            kwargs["endTimestamp"] = int(timestamp * 1000)

        url = self.__url + "/search/sse/events"
        url = f"{url}?{self._get_url(kwargs)}"

        logger.info(url)

        return self.__get_data_obj(url, sse_adapter, None, cache)

    @staticmethod
    def _get_url(kwargs):
        result = ""
        for k, v in kwargs.items():
            if k == "filters":
                if isinstance(v, Filter):
                    result += v.url()
                elif isinstance(v, (tuple, list)):

                    result += "".join([filter_.url() for filter_ in v])
            else:
                result += f"&{k}={v}"
        url = result[1:] if result[0] == "&" else result
        return quote(url.encode(), "/:&?=")

    def get_messages_from_data_provider(
        self,
        cache: bool = False,
        sse_adapter: bool = True,
        provider_adapter: Optional[Callable] = adapter_provider5,
        **kwargs,
    ) -> Data:
        """Sends SSE request for getting messages.

        For help use this readme
        https://github.com/th2-net/th2-rpt-data-provider#sse-requests-api
        on route http://localhost:8080/search/sse/messages.

        Args:
            cache (bool): If True, all requested data from rpt-data-provider will be saved to cache.
            sse_adapter (bool): If True, all data will go through SSE adapter and yield dicts.
                Otherwise adapter will yield SSE Events.
            provider_adapter (callable): Adapter function for rpt-data-provider.
                If None, Data object will yield object from previous map function.
            kwargs: th2-rpt-data-provider API query options.

        Returns:
            Data: Data object with Messages.

        """
        if not kwargs.get("startTimestamp") and not kwargs.get("resumeFromId"):
            exception_msg = (
                "'startTimestamp' or 'resumeFromId' must not be null for route /search/sse/messages. "
                "Please note it. More information on request here: "
                "https://github.com/th2-net/th2-rpt-data-provider "
            )
            logger.error(exception_msg)
            raise ValueError(exception_msg)

        if not kwargs.get("stream"):
            exception_msg = (
                "'stream' is required field. Please note it."
                "More information on request here: "
                "https://github.com/th2-net/th2-rpt-data-provider "
            )
            logger.error(exception_msg)
            raise ValueError(exception_msg)

        if isinstance(kwargs["startTimestamp"], datetime):
            timestamp = kwargs["startTimestamp"].replace(tzinfo=timezone.utc).timestamp()
            kwargs["startTimestamp"] = int(timestamp * 1000)  # unix timestamp in milliseconds

        if kwargs.get("endTimestamp") and isinstance(kwargs.get("endTimestamp"), datetime):
            timestamp = kwargs["endTimestamp"].replace(tzinfo=timezone.utc).timestamp()
            kwargs["endTimestamp"] = int(timestamp * 1000)

        streams = kwargs.pop("stream")
        if not isinstance(streams, (list, tuple)):
            streams = [streams]

        url = self.__url + "/search/sse/messages"
        url = f"{url}?{self._get_url(kwargs)}"
        fixed_part_len = len(url)

        current_url, resulting_urls = "", []
        for stream in streams:
            stream = f"&stream={stream}"
            if fixed_part_len + len(current_url) + len(stream) >= 2048:
                resulting_urls.append(url + current_url)
                current_url = ""
            current_url += stream
        if current_url:
            resulting_urls.append(url + current_url)

        if len(resulting_urls) > 1:
            source = partial(
                chain.from_iterable,
                [self.__get_data_obj(res_url, sse_adapter, provider_adapter, cache) for res_url in resulting_urls],
            )
            return Data(source).use_cache(cache)
        else:
            url = resulting_urls[0]
            return self.__get_data_obj(url, sse_adapter, provider_adapter, cache)

    def __execute_sse_request(self, url: str) -> Generator[dict, None, None]:
        """Creates SSE connection to server.

        Args:
            url: Url.

        Returns:
            dict: Response data.

        """
        response = self.__create_stream_connection(url)
        client = SSEClient(response, char_enc=self._char_enc, decode_errors_handler=self._decode_error_handler)
        for record in client.events():
            yield record

    def __create_stream_connection(self, url: str) -> Generator[bytes, None, None]:
        """Create stream connection.

        Args:
            url: Url.

        Yields:
            str: Response stream data.

        """
        headers = {"Accept": "text/event-stream"}
        http = PoolManager()
        response = http.request(method="GET", url=url, headers=headers, preload_content=False)

        # Check response
        if response.status != HTTPStatus.OK:
            for s in HTTPStatus:
                if s == response.status:
                    raise urllib3.exceptions.HTTPError(f"{s.value} {s.phrase} ({s.description})")
            raise urllib3.exceptions.HTTPError(f"Http returned bad status: {response.status}")

        for chunk in response.stream(self.__chunk_length):
            yield chunk

        response.release_conn()

    def find_messages_by_id_from_data_provider(
        self,
        messages_id: Union[Iterable, str],
        provider_adapter: Optional[Callable] = adapter_provider5,
    ) -> Optional[Union[List[dict], dict]]:
        """Gets message/messages by ids.

        Args:
            messages_id: One str with MessageID or list of MessagesIDs.
            provider_adapter: Adapter function for rpt-data-provider.
                If None, the function return message/messages without applying the adapter function.

        Returns:
            List[Message_dict] if you request a list or Message_dict or None if no massages found.

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
        msg_id_type_is_str = isinstance(messages_id, str)
        if isinstance(messages_id, str):
            messages_id = [messages_id]

        result = []
        for msg_id in messages_id:
            index = None
            if msg_id.find(".") != -1:
                msg_id, index = "".join(msg_id.split(".")[:-1]), int(msg_id[-1])

            url = f"{self.__url}/message/{msg_id}"
            logger.info(url)
            response = requests.get(url)
            try:
                answer = response.json()
            except (json.JSONDecodeError, simplejson.JSONDecodeError):
                exception_msg = (
                    f"Sorry, but the answer rpt-data-provider doesn't match the json format.\n"
                    f"Answer:{response.text}"
                )
                logger.exception(exception_msg)
                raise ValueError(exception_msg)

            if provider_adapter is not None:
                answer = provider_adapter(answer)

            if isinstance(answer, list):
                if index:
                    for message in answer:
                        if message["body"]["metadata"]["id"]["subsequence"][0] == index:
                            result.append(message)
                            break
                else:
                    result += answer
            else:
                result.append(answer)

            if len(result) > 1:
                msg_id_type_is_str = False

        return result[0] if msg_id_type_is_str else result if result else None

    def find_events_by_id_from_data_provider(
        self, events_id: Union[Iterable, str], broken_events: Optional[bool] = False
    ) -> Optional[Union[List[dict], dict]]:
        """Gets event/events by ids.

        Args:
            events_id: One str with EventID or list of EventsIDs.
            broken_events: If True broken events is replaced by a event stub.

        Returns:
            List[Event_dict] if you request a list or Event_dict or None if no events found.

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

        def __create_event_stub(broken_event_id):
            """Creates a event stub.

            Args:
                broken_event_id: Broken event id.

            Returns:
                Event Stub.
            """
            event_stub = {
                "attachedMessageIds": [],
                "batchId": "Broken_Event",
                "endTimestamp": {"nano": 0, "epochSecond": 0},
                "startTimestamp": {"nano": 0, "epochSecond": 0},
                "type": "event",
                "eventId": f"{broken_event_id}",
                "eventName": "Broken_Event",
                "eventType": "Broken_Event",
                "parentEventId": "Broken_Event",
                "successful": None,
                "isBatched": None,
            }
            return event_stub

        def __get_event(event_id: str, stub: bool):
            """Gets event from rpt-data-provider or replace on event stub.

            Args:
                event_id: Event id.
                stub: If True a broken event is replaced by a event stub.
            """
            url = f"{self.__url}/event/{event_id}"
            logger.info(url)
            response = requests.get(url)

            try:
                return response.json()
            except (json.JSONDecodeError, simplejson.JSONDecodeError):
                if stub:
                    return __create_event_stub(event_id)
                exception_msg = (
                    f"Sorry, but the answer rpt-data-provider doesn't match the json format.\n"
                    f"Answer:{response.text}"
                )
                logger.error(exception_msg)
                raise ValueError(exception_msg)

        event_id_type_is_str = isinstance(events_id, str)
        if isinstance(events_id, str):
            events_id = [events_id]
        result = []
        for id_ in events_id:
            result.append(__get_event(id_, broken_events))

        return result[0] if event_id_type_is_str else result if result else None

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
