#  Copyright 2022 Exactpro (Exactpro Systems Limited)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

#LOG import logging
from http import HTTPStatus
from typing import List, Generator, Optional, Union

import requests
from requests import Response
from urllib3 import PoolManager, exceptions
from urllib.parse import quote

from th2_data_services.provider.interfaces.source_api import IHTTPProviderSourceAPI
from th2_data_services.decode_error_handler import UNICODE_REPLACE_HANDLER

#LOG logger = logging.getLogger("th2_data_services")
#LOG logger.setLevel(logging.DEBUG)


class HTTPProvider6API(IHTTPProviderSourceAPI):
    def __init__(
        self,
        url: str,
        chunk_length: int = 65536,
        decode_error_handler: str = UNICODE_REPLACE_HANDLER,
        char_enc: str = "utf-8",
    ):
        """HTTP Provider6 API.

        Args:
            url: HTTP data source url.
            chunk_length: How much of the content to read in one chunk.
            char_enc: Encoding for the byte stream.
            decode_error_handler: Registered decode error handler.
        """
        self._url = self.__normalize_url(url)
        self._char_enc = char_enc
        self._chunk_length = chunk_length
        self._decode_error_handler = decode_error_handler

    def __normalize_url(self, url):
        if url is None:
                return url

        pos = len(url) - 1
        while url[pos] == '/' and pos >= 0:
            pos -= 1

        return url[:pos + 1]

    def __encode_url(self, url: str) -> str:
        return quote(url.encode(), "/:&?=")

    def get_url_message_streams(self) -> str:
        """REST-API `messageStreams` call returns a list of message stream names."""
        return self.__encode_url(f"{self._url}/messageStreams")

    def get_url_find_event_by_id(self, event_id: str) -> str:
        """REST-API `event` call returns a single event with the specified id."""
        return self.__encode_url(f"{self._url}/event/{event_id}")

    def get_url_find_events_by_id(self, *ids) -> str:
        """REST-API `events` call returns a list of events with the specified ids.

        Note, at a time you can request no more eventSearchChunkSize.

        Deprecated, use `get_url_find_event_by_id` instead.
        """
        query = ""
        for id in ids:
            query += f"ids={id}&"
        return self.__encode_url(f"{self._url}/events?{query[:-1]}")

    def get_url_find_message_by_id(self, message_id: str) -> str:
        """REST-API `message` call returns a single message with the specified id."""
        return self.__encode_url(f"{self._url}/message/{message_id}")

    def get_url_messages_filters(self) -> str:
        """SSE-API `filters/sse-messages` call returns all names of sse message filters.

        https://github.com/th2-net/th2-rpt-data-provider#filters-api
        """
        return self.__encode_url(f"{self._url}/filters/sse-messages")

    def get_url_events_filters(self) -> str:
        """SSE-API `/filters/sse-events` call returns all names of sse event filters.

        https://github.com/th2-net/th2-rpt-data-provider#filters-api
        """
        return self.__encode_url(f"{self._url}/filters/sse-events")

    def get_url_message_filter_info(self, filter_name: str) -> str:
        """SSE-API `filters/sse-messages/{filter name}` call returns filter info.

        https://github.com/th2-net/th2-rpt-data-provider#filters-api
        """
        return self.__encode_url(f"{self._url}/filters/sse-messages/{filter_name}")

    def get_url_event_filter_info(self, filter_name: str) -> str:
        """SSE-API `filters/sse-events/{filter_name}` call returns filter info.

        https://github.com/th2-net/th2-rpt-data-provider#filters-api
        """
        return self.__encode_url(f"{self._url}/filters/sse-events/{filter_name}")

    def get_url_match_event_by_id(self, event_id: str, filters: str = "") -> str:
        """REST-API `match/event/{id}` call returns boolean value.

        Checks that event with the specified id is matched by filter.

        https://github.com/th2-net/th2-rpt-data-provider#filters-api
        """
        return self.__encode_url(f"{self._url}/match/event/{event_id}{filters}")

    def get_url_match_message_by_id(self, message_id: str, filters: str = "") -> str:
        """REST-API `match/message/{id}` call returns boolean value.

        Checks that message with the specified id is matched by filter.

        https://github.com/th2-net/th2-rpt-data-provider#filters-api
        """
        return self.__encode_url(f"{self._url}/match/message/{message_id}{filters}")

    def get_url_search_sse_events(
        self,
        start_timestamp: int,
        end_timestamp: Optional[int] = None,
        parent_event: Optional[str] = None,
        resume_from_id: Optional[str] = None,
        search_direction: Optional[str] = "next",
        result_count_limit: Union[int, float] = None,
        keep_open: Optional[bool] = False,
        limit_for_parent: Union[int, float] = None,
        metadata_only: Optional[bool] = True,
        attached_messages: Optional[bool] = False,
        filters: Optional[str] = None,
    ) -> str:
        """REST-API `search/sse/events` call create a sse channel of event metadata that matches the filter.

        https://github.com/th2-net/th2-rpt-data-provider#sse-requests-api
        """
        kwargs = {
            "startTimestamp": start_timestamp,
            "endTimestamp": end_timestamp,
            "resumeFromId": resume_from_id,
            "parentEvent": parent_event,
            "searchDirection": search_direction,
            "resultCountLimit": result_count_limit,
            "limitForParent": limit_for_parent,
            "keepOpen": keep_open,
            "metadataOnly": metadata_only,
            "attachedMessages": attached_messages,
        }

        query = ""
        url = f"{self._url}/search/sse/events?"
        for k, v in kwargs.items():
            if v is None:
                continue
            else:
                query += f"&{k}={v}"
        url = f"{url}{query[1:]}"
        if filters is not None:
            url += filters
        return self.__encode_url(url)

    def get_url_search_sse_messages(
        self,
        start_timestamp: int,
        stream: List[str],
        end_timestamp: Optional[int] = None,
        resume_from_id: Optional[str] = None,
        search_direction: Optional[str] = "next",
        result_count_limit: Union[int, float] = None,
        keep_open: bool = False,
        message_id: Optional[List[str]] = None,
        attached_events: bool = False,
        lookup_limit_days: Union[int, float] = None,
        filters: Optional[str] = None,
    ) -> str:
        """REST-API `search/sse/messages` call create a sse channel of messages that matches the filter.

        https://github.com/th2-net/th2-rpt-data-provider#sse-requests-api
        """
        kwargs = {
            "startTimestamp": start_timestamp,
            "endTimestamp": end_timestamp,
            "resumeFromId": resume_from_id,
            "stream": stream,
            "searchDirection": search_direction,
            "resultCountLimit": result_count_limit,
            "keepOpen": keep_open,
            "messageId": message_id,
            "attachedEvents": attached_events,
            "lookupLimitDays": lookup_limit_days,
        }

        query = ""
        url = f"{self._url}/search/sse/messages?"
        for k, v in kwargs.items():
            if v is None:
                continue
            if k == "stream":
                for s in stream:
                    query += f"&{k}={s}"
            else:
                query += f"&{k}={v}"
        url = f"{url}{query[1:]}"
        if filters is not None:
            url += filters
        return self.__encode_url(url)

    def execute_sse_request(self, url: str) -> Generator[bytes, None, None]:
        """Create stream connection.

        Args:
            url: Url.

        Yields:
             str: Response stream data.
        """
        headers = {"Accept": "text/event-stream"}
        http = PoolManager()
        response = http.request(method="GET", url=url, headers=headers, preload_content=False)

        if response.status != HTTPStatus.OK:
            for s in HTTPStatus:
                if s == response.status:
                    raise exceptions.HTTPError(f"{s.value} {s.phrase} ({s.description})")
            raise exceptions.HTTPError(f"Http returned bad status: {response.status}")

        for chunk in response.stream(self._chunk_length):
            yield chunk

        response.release_conn()

    def execute_request(self, url: str) -> Response:
        """Sends a GET request to provider.

        Args:
            url: Url for a get request to rpt-data-provider.

        Returns:
            requests.Response: Response data.
        """
        return requests.get(url)
