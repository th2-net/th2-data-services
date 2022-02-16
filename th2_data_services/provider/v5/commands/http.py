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
from typing import List
import json
import simplejson

from th2_data_services.provider.v5.adapters.basic_adapters import AdapterSSE
from th2_data_services.provider.v5.command import IHTTPProvider5Command
from th2_data_services.provider.v5.data_source.http import HTTPProvider5DataSource
from th2_data_services.provider.v5.provider_api import HTTPProvider5API
from th2_data_services.provider.command import IProviderAdaptableCommand

import logging

logger = logging.getLogger("th2_data_services")
logger.setLevel(logging.DEBUG)


class GetEventById(IHTTPProvider5Command, IProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It retrieves the event by id.

    Returns:
        dict: Th2 event.
    """

    def __init__(self, id: str):
        """
        Args:
            id: Event id.

        """
        super().__init__()
        self._id = id
        self._stub_status = False

    def handle(self, data_source: HTTPProvider5DataSource) -> dict:
        api: HTTPProvider5API = data_source.source_api
        url = api.get_url_find_event_by_id(self._id)

        logger.info(url)

        response = api.execute_request(url)
        try:
            event = response.json()
        except (json.JSONDecodeError, simplejson.JSONDecodeError):
            if self._stub_status:
                return data_source.event_stub.build({data_source.event_struct.EVENT_ID: self._id})
            else:
                exception_msg = f"Unable to find the message. Id: {self._id}"
                logger.error(exception_msg)
                raise ValueError(exception_msg)
        return self._handle_adapters(event)

    def use_stub(self):
        self._stub_status = True
        return self


class GetEventsById(IHTTPProvider5Command, IProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It retrieves the events by ids.

    Returns:
        List[dict]: Th2 events.
    """

    def __init__(self, ids: List[str]):
        """
        Args:
            ids: Event id list.

        """
        super().__init__()
        self._ids: ids = ids
        self._stub_status = False

    def handle(self, data_source: HTTPProvider5DataSource):
        result = []
        for event_id in self._ids:
            try:
                event = GetEventById(event_id).handle(data_source)
            except (json.JSONDecodeError, simplejson.JSONDecodeError):
                if self._stub_status:
                    return data_source.event_stub.build({data_source.event_struct.EVENT_ID: event_id})
                else:
                    exception_msg = f"Unable to find the message. Id: {event_id}"
                    logger.error(exception_msg)
                    raise ValueError(exception_msg)
            result.append(self._handle_adapters(event))
        return result

    def use_stub(self):
        self._stub_status = True
        return self


class GetEvents(IHTTPProvider5Command, IProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It searches events stream by options.

    Returns:
        Iterable[dict]: Stream of Th2 events.
    """

    def __init__(
        self,
        start_timestamp: int,
        end_timestamp: int = None,
        parent_event: str = None,
        search_direction: str = "next",
        resume_from_id: str = None,
        result_count_limit: int = None,
        keep_open: bool = False,
        limit_for_parent: int = None,
        metadata_only: bool = True,
        attached_messages: bool = False,
        filters: str = None,
    ):
        """
        Args:
            start_timestamp: Start timestamp of search.
            end_timestamp: End timestamp of search.
            parent_event: Match events to the specified parent.
            search_direction: Search direction.
            resume_from_id: Event id from which search starts.
            result_count_limit: Result count limit.
            keep_open: If the search has reached the current moment.
                It is need to wait further for the appearance of new data.
                the one closest to the specified timestamp.
            limit_for_parent: How many children events for each parent do we want to request.
            metadata_only: Receive only metadata (true) or entire event (false) (without attached_messages).
            attached_messages: Gets messages ids which linked to events.
            filters: Filters using in search for messages.

        """
        super().__init__()
        self._start_timestamp = start_timestamp
        self._end_timestamp = end_timestamp
        self._parent_event = parent_event
        self._search_direction = search_direction
        self._resume_from_id = resume_from_id
        self._result_count_limit = result_count_limit
        self._keep_open = keep_open
        self._limit_for_parent = limit_for_parent
        self._metadata_only = metadata_only
        self._attached_messages = attached_messages
        self._filters = filters

        self._adapters = AdapterSSE()

    def handle(self, data_source: HTTPProvider5DataSource):
        api: HTTPProvider5API = data_source.source_api
        url = api.get_url_search_sse_events(
            start_timestamp=self._start_timestamp,
            end_timestamp=self._end_timestamp,
            parent_event=self._parent_event,
            search_direction=self._search_direction,
            resume_from_id=self._resume_from_id,
            result_count_limit=self._result_count_limit,
            keep_open=self._keep_open,
            limit_for_parent=self._limit_for_parent,
            metadata_only=self._metadata_only,
            attached_messages=self._attached_messages,
            filters=self._filters,
        )

        logger.info(url)

        for response in api.execute_sse_request(url):
            response = self._handle_adapters(response)
            if response is not None:
                yield response


class GetMessageById(IHTTPProvider5Command, IProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It retrieves the message by id.

    Returns:
        dict: Th2 message.
    """

    def __init__(self, id: str):
        """
        Args:
            id: Message id.

        """
        super().__init__()
        self._id = id
        self._stub_status = False

    def handle(self, data_source: HTTPProvider5DataSource):
        api: HTTPProvider5API = data_source.source_api
        url = api.get_url_find_message_by_id(self._id)

        logger.info(url)

        response = api.execute_request(url)
        try:
            message = response.json()
        except (json.JSONDecodeError, simplejson.JSONDecodeError):
            if self._stub_status:
                return data_source.message_stub.build({data_source.message_struct.MESSAGE_ID: self._id})
            else:
                exception_msg = f"Unable to find the message. Id: {self._id}"
                logger.error(exception_msg)
                raise ValueError(exception_msg)
        return self._handle_adapters(message)

    def use_stub(self):
        self._stub_status = True
        return self


class GetMessagesById(IHTTPProvider5Command, IProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It retrieves the messages by ids.

    Returns:
        List[dict]: Th2 messages.
    """

    def __init__(self, ids: List[str]):
        """
        Args:
            ids: Message id list.

        """
        super().__init__()
        self._ids: ids = ids
        self._stub_status = False

    def handle(self, data_source: HTTPProvider5DataSource):
        result = []
        for message_id in self._ids:
            try:
                message = GetMessageById(message_id).handle(data_source)
            except (json.JSONDecodeError, simplejson.JSONDecodeError):
                if self._stub_status:
                    return data_source.event_stub.build({data_source.message_struct.MESSAGE_ID: message_id})
                else:
                    exception_msg = f"Unable to find the message. Id: {message_id}"
                    logger.error(exception_msg)
                    raise ValueError(exception_msg)
            result.append(self._handle_adapters(message))
        return result

    def use_stub(self):
        self._stub_status = True
        return self


class GetMessages(IHTTPProvider5Command, IProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It searches messages stream by options.

    Returns:
        Iterable[dict]: Stream of Th2 messages.
    """

    def __init__(
        self,
        start_timestamp: int,
        stream: List[str],
        end_timestamp: int = None,
        resume_from_id: str = None,
        search_direction: str = "next",
        result_count_limit: int = None,
        keep_open: bool = False,
        message_id: List[str] = None,
        attached_events: bool = False,
        lookup_limit_days: int = None,
        filters: str = None,
    ):
        """
        Args:
            start_timestamp: Start timestamp of search.
            end_timestamp: End timestamp of search.
            stream: Alias of messages.
            resume_from_id: Message id from which search starts.
            search_direction: Search direction.
            result_count_limit: Result count limit.
            keep_open: If the search has reached the current moment.
                It is need to wait further for the appearance of new data.
            message_id: List of message IDs to restore search. If given, it has
                the highest priority and ignores stream (uses streams from ids), startTimestamp and resumeFromId.
            attached_events: If true, additionally load attached_event_ids
            lookup_limit_days: The number of days that will be viewed on
                the first request to get the one closest to the specified timestamp.
            filters: Filters using in search for messages.
        """
        super().__init__()
        self._start_timestamp = start_timestamp
        self._end_timestamp = end_timestamp
        self._stream = stream
        self._resume_from_id = resume_from_id
        self._search_direction = search_direction
        self._result_count_limit = result_count_limit
        self._keep_open = keep_open
        self._message_id = message_id
        self._attached_events = attached_events
        self._lookup_limit_days = lookup_limit_days
        self._filters = filters

        self._adapter_sse = AdapterSSE()

    def handle(self, data_source: HTTPProvider5DataSource):
        api: HTTPProvider5API = data_source.source_api
        url = api.get_url_search_sse_messages(
            start_timestamp=self._start_timestamp,
            end_timestamp=self._end_timestamp,
            stream=self._stream,
            resume_from_id=self._resume_from_id,
            search_direction=self._search_direction,
            result_count_limit=self._result_count_limit,
            keep_open=self._keep_open,
            attached_events=self._attached_events,
            lookup_limit_days=self._lookup_limit_days,
            filters=self._filters,
        )

        logger.info(url)

        for response in api.execute_sse_request(url):
            response = self._handle_adapters(response)
            if response is not None:
                yield response
