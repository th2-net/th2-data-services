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

from typing import Generator, List, Sequence, Union, Optional
from datetime import datetime, timezone
from functools import partial

from th2_data_services import Filter, Data
from th2_data_services.interfaces import IAdapter
from th2_data_services.provider.exceptions import EventNotFound, MessageNotFound
from th2_data_services.provider.v5.interfaces.command import IHTTPProvider5Command
from th2_data_services.provider.v5.data_source.http import HTTPProvider5DataSource
from th2_data_services.provider.v5.filters.filter import (
    Provider5EventFilter,
    Provider5MessageFilter,
)
from th2_data_services.provider.v5.provider_api import HTTPProvider5API
from th2_data_services.provider.command import ProviderAdaptableCommand
from th2_data_services.sse_client import SSEClient
from th2_data_services.provider.adapters.adapter_sse import get_default_sse_adapter
from th2_data_services.decode_error_handler import UNICODE_REPLACE_HANDLER

# LOG import logging

# LOG logger = logging.getLogger(__name__)

EventFilters = Union[Filter, Provider5EventFilter, Sequence[Union[Filter, Provider5EventFilter]]]
MessageFilters = Union[Filter, Provider5MessageFilter, Sequence[Union[Filter, Provider5MessageFilter]]]


def _convert_filters_to_string(filters):
    if not filters:
        return None
    filters_res = filters
    if not isinstance(filters_res, (tuple, list)):
        filters_res = [filters_res]

    return "".join([filter_.url() for filter_ in filters_res])


class GetEventById(IHTTPProvider5Command, ProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It retrieves the event by id with `attachedMessageIds` list.

    Returns:
        dict: Th2 event.

    Raises:
        EventNotFound: If event by Id wasn't found.
    """

    def __init__(self, id: str, use_stub: bool = False):
        """GetEventById constructor.

        Args:
            id: Event id.
            use_stub: If True the command returns stub instead of exception.
        """
        super().__init__()
        self._id = id
        self._stub_status = use_stub

    def handle(self, data_source: HTTPProvider5DataSource) -> dict:  # noqa: D102
        api: HTTPProvider5API = data_source.source_api
        url = api.get_url_find_event_by_id(self._id)

        # LOG         logger.info(url)

        response = api.execute_request(url)

        if response.status_code == 404 and self._stub_status:
            stub = data_source.event_stub_builder.build({data_source.event_struct.EVENT_ID: self._id})
            return self._handle_adapters(stub)
        elif response.status_code == 404:
            # LOG             logger.error(f"Unable to find the message. Id: {self._id}")
            raise EventNotFound(self._id)
        else:
            return self._handle_adapters(response.json())


class GetEventsById(IHTTPProvider5Command, ProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It retrieves the events by ids with `attachedMessageIds` list.

    Returns:
        List[dict]: Th2 events.

    Raises:
        EventNotFound: If any event by Id wasn't found.
    """

    def __init__(self, ids: List[str], use_stub: bool = False):
        """GetEventsById constructor.

        Args:
            ids: Event id list.
            use_stub: If True the command returns stub instead of exception.
        """
        super().__init__()
        self._ids: ids = ids
        self._stub_status = use_stub

    def handle(self, data_source: HTTPProvider5DataSource):  # noqa: D102
        result = []
        for event_id in self._ids:
            event = GetEventById(event_id, use_stub=self._stub_status).handle(data_source)
            if event is None:
                continue
            event = self._handle_adapters(event)
            if event is None:
                continue
            result.append(event)

        return result


class GetEventsSSEBytes(IHTTPProvider5Command, ProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It searches events stream by options.

    Returns:
        Iterable[dict]: Stream of Th2 events.
    """

    def __init__(
        self,
        start_timestamp: datetime,
        end_timestamp: datetime = None,
        parent_event: str = None,
        search_direction: str = "next",
        resume_from_id: str = None,
        result_count_limit: int = None,
        keep_open: bool = False,
        limit_for_parent: int = None,
        attached_messages: bool = False,
        filters: EventFilters = None,
    ):
        """GetEventsSSEBytes constructor.

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
            attached_messages: Gets messages ids which linked to events.
            filters: Filters using in search for messages.

        """
        super().__init__()
        self._start_timestamp = int(1000 * start_timestamp.replace(tzinfo=timezone.utc).timestamp())
        self._end_timestamp = int(1000 * end_timestamp.replace(tzinfo=timezone.utc).timestamp())
        self._parent_event = parent_event
        self._search_direction = search_direction
        self._resume_from_id = resume_from_id
        self._result_count_limit = result_count_limit
        self._keep_open = keep_open
        self._limit_for_parent = limit_for_parent
        self._metadata_only = False
        self._attached_messages = attached_messages
        self._filters = filters

    def handle(self, data_source: HTTPProvider5DataSource):  # noqa: D102
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
            filters=_convert_filters_to_string(self._filters),
        )

        # LOG         logger.info(url)

        for response in api.execute_sse_request(url):
            response = self._handle_adapters(response)
            if response is not None:
                yield response


class GetEventsSSEEvents(IHTTPProvider5Command, ProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It searches events stream by options.

    Returns:
        Iterable[dict]: Stream of Th2 events.
    """

    def __init__(
        self,
        start_timestamp: datetime,
        end_timestamp: datetime = None,
        parent_event: str = None,
        search_direction: str = "next",
        resume_from_id: str = None,
        result_count_limit: int = None,
        keep_open: bool = False,
        limit_for_parent: int = None,
        attached_messages: bool = False,
        filters: EventFilters = None,
        char_enc: str = "utf-8",
        decode_error_handler: str = UNICODE_REPLACE_HANDLER,
    ):
        """GetEventsSSEEvents constructor.

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
            attached_messages: Gets messages ids which linked to events.
            filters: Filters using in search for messages.
            char_enc: Encoding for the byte stream.
            decode_error_handler: Registered decode error handler.
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
        self._attached_messages = attached_messages
        self._filters = filters
        self._char_enc = char_enc
        self._decode_error_handler = decode_error_handler

    def handle(self, data_source: HTTPProvider5DataSource):  # noqa: D102
        response = GetEventsSSEBytes(
            start_timestamp=self._start_timestamp,
            end_timestamp=self._end_timestamp,
            parent_event=self._parent_event,
            search_direction=self._search_direction,
            resume_from_id=self._resume_from_id,
            result_count_limit=self._result_count_limit,
            keep_open=self._keep_open,
            limit_for_parent=self._limit_for_parent,
            attached_messages=self._attached_messages,
            filters=self._filters,
        ).handle(data_source)
        client = SSEClient(
            response,
            char_enc=self._char_enc,
            decode_errors_handler=self._decode_error_handler,
        )
        for record in client.events():
            record = self._handle_adapters(record)
            if record is not None:
                yield record


class GetEvents(IHTTPProvider5Command, ProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It searches events stream by options.

    Returns:
        Iterable[dict]: Stream of Th2 events.
    """

    def __init__(
        self,
        start_timestamp: datetime,
        end_timestamp: datetime = None,
        parent_event: str = None,
        search_direction: str = "next",
        resume_from_id: str = None,
        result_count_limit: int = None,
        keep_open: bool = False,
        limit_for_parent: int = None,
        attached_messages: bool = False,
        filters: EventFilters = None,
        cache: bool = False,
        sse_handler: Optional[IAdapter] = None,
    ):
        """GetEvents constructor.

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
            attached_messages: Gets messages ids which linked to events.
            filters: Filters using in search for messages.
            cache: If True, all requested data from rpt-data-provider will be saved to cache.
            sse_handler: SSEEvents handler
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
        self._attached_messages = attached_messages
        self._filters = filters
        self._cache = cache
        self.sse_handler = sse_handler or get_default_sse_adapter()

    def handle(self, data_source: HTTPProvider5DataSource) -> Data:  # noqa: D102
        source = partial(self.sse_handler.handle, partial(self.__handle_stream, data_source))
        source = (self._handle_adapters(record) for record in source() if record is not None)
        return Data(source).use_cache(self._cache)

    def __handle_stream(self, data_source: HTTPProvider5DataSource) -> Generator[dict, None, None]:
        stream = GetEventsSSEEvents(
            start_timestamp=self._start_timestamp,
            end_timestamp=self._end_timestamp,
            parent_event=self._parent_event,
            search_direction=self._search_direction,
            resume_from_id=self._resume_from_id,
            result_count_limit=self._result_count_limit,
            keep_open=self._keep_open,
            limit_for_parent=self._limit_for_parent,
            attached_messages=self._attached_messages,
            filters=self._filters,
        ).handle(data_source)

        for event in stream:
            yield event


class GetMessageById(IHTTPProvider5Command, ProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It retrieves the message by id.

    Please note, Provider5 doesn't return `attachedEventIds`. It will be == [].
    It's expected that Provider7 will be support it.

    Returns:
        dict: Th2 message.

    Raises:
        MessageNotFound: If message by id wasn't found.
    """

    def __init__(self, id: str, use_stub: bool = False):
        """GetMessageById constructor.

        Args:
            id: Message id.
            use_stub: If True the command returns stub instead of exception.
        """
        super().__init__()
        self._id = id
        self._stub_status = use_stub

    def handle(self, data_source: HTTPProvider5DataSource) -> dict:  # noqa: D102
        api: HTTPProvider5API = data_source.source_api
        url = api.get_url_find_message_by_id(self._id)

        # LOG         logger.info(url)

        response = api.execute_request(url)

        if response.status_code == 404 and self._stub_status:
            stub = data_source.message_stub_builder.build({data_source.message_struct.MESSAGE_ID: self._id})
            return self._handle_adapters(stub)
        elif response.status_code == 404:
            # LOG             logger.error(f"Unable to find the message. Id: {self._id}")
            raise MessageNotFound(self._id)
        else:
            return self._handle_adapters(response.json())


class GetMessagesById(IHTTPProvider5Command, ProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It retrieves the messages by ids.

    Please note, Provider5 doesn't return `attachedEventIds`. It will be == [].
    It's expected that Provider7 will be support it.

    Returns:
        List[dict]: Th2 messages.

    Raises:
        MessageNotFound: If any message by id wasn't found.
    """

    def __init__(self, ids: List[str], use_stub: bool = False):
        """GetMessagesById constructor.

        Args:
            ids: Message id list.
            use_stub: If True the command returns stub instead of exception.
        """
        super().__init__()
        self._ids: ids = ids
        self._stub_status = use_stub

    def handle(self, data_source: HTTPProvider5DataSource) -> List[dict]:  # noqa: D102
        result = []
        for message_id in self._ids:
            message = GetMessageById(
                message_id,
                use_stub=self._stub_status,
            ).handle(data_source)
            if message is None:
                continue
            message = self._handle_adapters(message)
            if message is None:
                continue
            result.append(message)

        return result


class GetMessagesSSEBytes(IHTTPProvider5Command, ProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It searches messages stream by options.

    Returns:
        Iterable[dict]: Stream of Th2 messages.
    """

    def __init__(
        self,
        start_timestamp: datetime,
        stream: List[str],
        end_timestamp: datetime = None,
        resume_from_id: str = None,
        search_direction: str = "next",
        result_count_limit: int = None,
        keep_open: bool = False,
        message_id: List[str] = None,
        attached_events: bool = False,
        lookup_limit_days: int = None,
        filters: MessageFilters = None,
    ):
        """GetMessagesSSEBytes constructor.

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
        self._start_timestamp = int(1000 * start_timestamp.replace(tzinfo=timezone.utc).timestamp())
        self._end_timestamp = (
            end_timestamp
            if end_timestamp is None
            else int(1000 * end_timestamp.replace(tzinfo=timezone.utc).timestamp())
        )
        self._stream = stream
        self._resume_from_id = resume_from_id
        self._search_direction = search_direction
        self._result_count_limit = result_count_limit
        self._keep_open = keep_open
        self._message_id = message_id
        self._attached_events = attached_events
        self._lookup_limit_days = lookup_limit_days
        self._filters = filters

    def handle(self, data_source: HTTPProvider5DataSource) -> Generator[dict, None, None]:  # noqa: D102
        api: HTTPProvider5API = data_source.source_api
        url = api.get_url_search_sse_messages(
            start_timestamp=self._start_timestamp,
            end_timestamp=self._end_timestamp,
            stream=[""],
            resume_from_id=self._resume_from_id,
            search_direction=self._search_direction,
            result_count_limit=self._result_count_limit,
            keep_open=self._keep_open,
            attached_events=self._attached_events,
            lookup_limit_days=self._lookup_limit_days,
            filters=_convert_filters_to_string(self._filters),
        ).replace("&stream=", "")

        fixed_part_len = len(url)
        current_url, resulting_urls = "", []
        for stream in self._stream:
            stream = f"&stream={stream}"
            if fixed_part_len + len(current_url) + len(stream) >= 2048:
                resulting_urls.append(url + current_url)
                current_url = ""
            current_url += stream
        if current_url:
            resulting_urls.append(url + current_url)

        for url in resulting_urls:
            # LOG             logger.info(url)
            for response in api.execute_sse_request(url):
                response = self._handle_adapters(response)
                if response is not None:
                    yield response


class GetMessagesSSEEvents(IHTTPProvider5Command, ProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It searches messages stream by options.

    Returns:
        Iterable[dict]: Stream of Th2 messages.
    """

    def __init__(
        self,
        start_timestamp: datetime,
        stream: List[str],
        end_timestamp: datetime = None,
        resume_from_id: str = None,
        search_direction: str = "next",
        result_count_limit: int = None,
        keep_open: bool = False,
        message_id: List[str] = None,
        attached_events: bool = False,
        lookup_limit_days: int = None,
        filters: MessageFilters = None,
        char_enc: str = "utf-8",
        decode_error_handler: str = UNICODE_REPLACE_HANDLER,
    ):
        """GetMessagesSSEEvents constructor.

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
            char_enc: Character encode that will use SSEClient.
            decode_error_handler: Decode error handler.
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
        self._char_enc = char_enc
        self._decode_error_handler = decode_error_handler

    def handle(self, data_source: HTTPProvider5DataSource) -> Generator[dict, None, None]:  # noqa: D102
        response = GetMessagesSSEBytes(
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
        ).handle(data_source)

        client = SSEClient(
            response,
            char_enc=self._char_enc,
            decode_errors_handler=self._decode_error_handler,
        )

        for record in client.events():
            record = self._handle_adapters(record)
            if record is not None:
                yield record


class GetMessages(IHTTPProvider5Command, ProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It searches messages stream by options.

    Returns:
        Iterable[dict]: Stream of Th2 messages.
    """

    def __init__(
        self,
        start_timestamp: datetime,
        stream: List[str],
        end_timestamp: datetime = None,
        resume_from_id: str = None,
        search_direction: str = "next",
        result_count_limit: int = None,
        keep_open: bool = False,
        message_id: List[str] = None,
        attached_events: bool = False,
        lookup_limit_days: int = None,
        filters: MessageFilters = None,
        char_enc: str = "utf-8",
        decode_error_handler: str = UNICODE_REPLACE_HANDLER,
        cache: bool = False,
        sse_handler: Optional[IAdapter] = None,
    ):
        """GetMessages constructor.

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
            char_enc: Encoding for the byte stream.
            decode_error_handler: Registered decode error handler.
            cache: If True, all requested data from rpt-data-provider will be saved to cache.
            sse_handler: SSEEvents handler
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
        self._char_enc = char_enc
        self._decode_error_handler = decode_error_handler
        self._cache = cache
        self.sse_handler = sse_handler or get_default_sse_adapter()

    def handle(self, data_source: HTTPProvider5DataSource) -> Data:  # noqa: D102
        source = partial(self.sse_handler.handle, partial(self.__handle_stream, data_source))
        source = (self._handle_adapters(record) for record in source() if record is not None)
        return Data(source).use_cache(self._cache)

    def __handle_stream(self, data_source: HTTPProvider5DataSource) -> Generator[dict, None, None]:
        stream = GetMessagesSSEEvents(
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
        ).handle(data_source)

        for message in stream:
            yield message
