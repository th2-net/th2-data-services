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

from datetime import datetime, timezone
from functools import partial
from typing import List, Iterable, Generator

from grpc._channel import _InactiveRpcError
from th2_grpc_data_provider.data_provider_template_pb2 import (
    EventData,
    MessageData,
)

from th2_data_services import Filter, Data
from th2_data_services.provider.command import ProviderAdaptableCommand
from th2_data_services.provider.exceptions import EventNotFound, MessageNotFound
from th2_data_services.provider.v5.adapters.basic_adapters import GRPCObjectToDictAdapter
from th2_data_services.provider.v5.adapters.event_adapters import DeleteEventWrappersAdapter
from th2_data_services.provider.v5.adapters.message_adapters import DeleteMessageWrappersAdapter
from th2_data_services.provider.v5.interfaces.command import IGRPCProvider5Command

from th2_data_services.provider.v5.data_source.grpc import GRPCProvider5DataSource
from th2_data_services.provider.v5.provider_api import GRPCProvider5API

#LOG import logging

#LOG logger = logging.getLogger(__name__)


class GetEventByIdGRPCObject(IGRPCProvider5Command, ProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It retrieves the event by id as GRPC object.

    Returns:
        EventData: Th2 event.
    """

    def __init__(self, id: str):
        """GetEventByIdGRPCObject constructor.

        Args:
            id: Event id.

        """
        super().__init__()
        self._id = id

    def handle(self, data_source: GRPCProvider5DataSource) -> EventData:  # noqa: D102
        api: GRPCProvider5API = data_source.source_api
        event = api.get_event(self._id)

        event = self._handle_adapters(event)
        return event


class GetEventById(IGRPCProvider5Command, ProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It retrieves the event by id with `attachedMessageIds` list.

    Returns:
        dict: Th2 event.

    Raises:
        EventNotFound: If event by Id wasn't found.
    """

    def __init__(self, id: str, use_stub=False):
        """GetEventById constructor.

        Args:
            id: Event id.
            use_stub: If True the command returns stub instead of exception.

        """
        super().__init__()
        self._id = id
        self._grpc_decoder = GRPCObjectToDictAdapter()
        self._wrapper_deleter = DeleteEventWrappersAdapter()
        self._stub_status = use_stub

    def handle(self, data_source: GRPCProvider5DataSource) -> dict:  # noqa: D102
        try:
            event = GetEventByIdGRPCObject(self._id).handle(data_source)
            event = self._grpc_decoder.handle(event)
            event = self._wrapper_deleter.handle(event)
        except _InactiveRpcError:
            if self._stub_status:
                event = data_source.event_stub_builder.build({data_source.event_struct.EVENT_ID: self._id})
            else:
#LOG                 logger.error(f"Unable to find the event. Id: {self._id}")
                raise EventNotFound(self._id)

        event = self._handle_adapters(event)
        return event


class GetEventsById(IGRPCProvider5Command, ProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It retrieves the events by ids with `attachedMessageIds` list.

    Returns:
        List[dict]: Th2 events.

    Raises:
        EventNotFound: If any event by Id wasn't found.
    """

    def __init__(self, ids: List[str], use_stub=False):
        """GetEventsById constructor.

        Args:
            ids: Events ids.
            use_stub: If True the command returns stub instead of exception.

        """
        super().__init__()
        self.ids = ids
        self._stub_status = use_stub

    def handle(self, data_source: GRPCProvider5DataSource) -> List[dict]:  # noqa: D102
        response = []
        for event_id in self.ids:
            event = GetEventById(event_id, use_stub=self._stub_status).handle(data_source=data_source)
            event = self._handle_adapters(event)
            response.append(event)

        return response


class GetEventsGRPCObjects(IGRPCProvider5Command, ProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It searches events stream as GRPC object by options.

    Returns:
        Iterable[EventData]: Stream of Th2 events.
    """

    def __init__(
        self,
        start_timestamp: datetime,
        end_timestamp: datetime = None,
        parent_event: str = None,
        search_direction: str = "NEXT",
        resume_from_id: str = None,
        result_count_limit: int = None,
        keep_open: bool = False,
        limit_for_parent: int = None,
        attached_messages: bool = False,
        filters: List[Filter] = None,
    ):
        """GetEventsGRPCObjects constructor.

        Args:
            start_timestamp: Start timestamp of search.
            end_timestamp: End timestamp of search.
            resume_from_id: Event id from which search starts.
            parent_event: Match events to the specified parent.
            search_direction: Search direction.
            result_count_limit: Result count limit.
            keep_open: If the search has reached the current moment.
                It is need to wait further for the appearance of new data.
                the one closest to the specified timestamp.
            limit_for_parent: How many children events for each parent do we want to request.
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
        self._metadata_only = False
        self._attached_messages = attached_messages
        self._filters = filters

    def handle(self, data_source: GRPCProvider5DataSource) -> Iterable[EventData]:  # noqa: D102
        api: GRPCProvider5API = data_source.source_api

        start_timestamp = int(self._start_timestamp.replace(tzinfo=timezone.utc).timestamp() * 10 ** 9)
        end_timestamp = int(self._end_timestamp.replace(tzinfo=timezone.utc).timestamp() * 10 ** 9)

        stream_response = api.search_events(
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
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
        for response in stream_response:
            if response.WhichOneof("data") == "event":
                response = self._handle_adapters(response)
                yield response.event


class GetEvents(IGRPCProvider5Command, ProviderAdaptableCommand):
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
        search_direction: str = "NEXT",
        resume_from_id: str = None,
        result_count_limit: int = None,
        keep_open: bool = False,
        limit_for_parent: int = None,
        attached_messages: bool = False,
        filters: List[Filter] = None,
        cache: bool = False,
    ):
        """GetEvents constructor.

        Args:
            start_timestamp: Start timestamp of search.
            end_timestamp: End timestamp of search.
            resume_from_id: Event id from which search starts.
            parent_event: Match events to the specified parent.
            search_direction: Search direction.
            result_count_limit: Result count limit.
            keep_open: If the search has reached the current moment.
                It is need to wait further for the appearance of new data.
                the one closest to the specified timestamp.
            limit_for_parent: How many children events for each parent do we want to request.
            attached_messages: Gets messages ids which linked to events.
            filters: Filters using in search for messages.
            cache: If True, all requested data from rpt-data-provider will be saved to cache.

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
        self._metadata_only = False
        self._attached_messages = attached_messages
        self._filters = filters
        self._cache = cache

        self._grpc_decoder = GRPCObjectToDictAdapter()
        self._wrapper_deleter = DeleteEventWrappersAdapter()

    def handle(self, data_source: GRPCProvider5DataSource) -> Data:  # noqa: D102
        source = partial(self.__handle_stream, data_source)
        return Data(source, cache=self._cache)

    def __handle_stream(self, data_source: GRPCProvider5DataSource) -> Generator[dict, None, None]:
        stream = GetEventsGRPCObjects(
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
            event = self._grpc_decoder.handle(event)
            event = self._wrapper_deleter.handle(event)
            event = self._handle_adapters(event)
            yield event


class GetMessageByIdGRPCObject(IGRPCProvider5Command, ProviderAdaptableCommand):  # noqa: D102
    """A Class-Command for request to rpt-data-provider.

    It retrieves the message by id as GRPC Object.

    Returns:
        MessageData: Th2 message.
    """

    def __init__(self, id: str):
        """GetMessageByIdGRPCObject constructor.

        Args:
            id: Message id.

        """
        super().__init__()
        self._id = id

    def handle(self, data_source: GRPCProvider5DataSource) -> MessageData:
        api: GRPCProvider5API = data_source.source_api
        response = api.get_message(self._id)
        response = self._handle_adapters(response)
        return response


class GetMessageById(IGRPCProvider5Command, ProviderAdaptableCommand):  # noqa: D102
    """A Class-Command for request to rpt-data-provider.

    It retrieves the message by id.

    Please note, Provider5 doesn't return `attachedEventIds`. It will be == [].
    It's expected that Provider7 will be support it.

    Returns:
        dict: Th2 message.

    Raises:
        MessageNotFound: If message by id wasn't found.
    """

    def __init__(self, id: str, use_stub=False):
        """GetMessageById constructor.

        Args:
            id: Message id.
            use_stub: If True the command returns stub instead of exception.

        """
        super().__init__()
        self._id = id
        self._decoder = GRPCObjectToDictAdapter()
        self._wrapper_deleter = DeleteMessageWrappersAdapter()
        self._stub_status = use_stub

    def handle(self, data_source: GRPCProvider5DataSource) -> dict:  # noqa: D102
        try:
            message = GetMessageByIdGRPCObject(self._id).handle(data_source)
            message = self._decoder.handle(message)
            message = self._wrapper_deleter.handle(message)
        except _InactiveRpcError:
            if self._stub_status:
                message = data_source.message_stub_builder.build({data_source.message_struct.MESSAGE_ID: self._id})
            else:
#LOG                 logger.error(f"Unable to find the message. Id: {self._id}")
                raise MessageNotFound(self._id)
        message = self._handle_adapters(message)
        return message


class GetMessagesById(IGRPCProvider5Command, ProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It retrieves the messages by id.

    Please note, Provider5 doesn't return `attachedEventIds`. It will be == [].
    It's expected that Provider7 will be support it.

    Returns:
        List[dict]: Th2 messages.

    Raises:
        MessageNotFound: If any message by id wasn't found.
    """

    def __init__(self, ids: List[str], use_stub=False):
        """GetMessagesById constructor.

        Args:
            ids: Messages id.
            use_stub: If True the command returns stub instead of exception.

        """
        super().__init__()
        self._ids = ids
        self._stub_status = use_stub

    def handle(self, data_source: GRPCProvider5DataSource) -> List[dict]:  # noqa: D102
        response = []
        for id_ in self._ids:
            message = GetMessageById(id_, use_stub=self._stub_status).handle(data_source)
            message = self._handle_adapters(message)
            response.append(message)

        return response


class GetMessagesGRPCObject(IGRPCProvider5Command, ProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It searches messages stream as GRPC object by options.

    Returns:
        Iterable[MessageData]: Stream of Th2 messages.
    """

    def __init__(
        self,
        start_timestamp: datetime,
        stream: List[str],
        end_timestamp: datetime = None,
        resume_from_id: str = None,
        search_direction: str = "NEXT",
        result_count_limit: int = None,
        keep_open: bool = False,
        message_id: List[str] = None,
        attached_events: bool = False,
        filters: List[Filter] = None,
    ):
        """GetMessagesGRPCObject constructor.

        Args:
            start_timestamp: Start timestamp of search.
            end_timestamp: End timestamp of search.
            stream: Alias of messages.
            resume_from_id: Message id from which search starts.
            search_direction: Search direction.
            result_count_limit: Result count limit.
            keep_open: If the search has reached the current moment.
                It is need to wait further for the appearance of new data.
            message_id: List of message ids to restore the search
            attached_events: If true, it will additionally load attachedEventsIds.
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
        self._filters = filters
        self._message_id = message_id
        self._attached_events = attached_events

    def handle(self, data_source: GRPCProvider5DataSource) -> List[MessageData]:
        api = data_source.source_api

        start_timestamp = int(self._start_timestamp.replace(tzinfo=timezone.utc).timestamp() * 10 ** 9)
        end_timestamp = int(self._end_timestamp.replace(tzinfo=timezone.utc).timestamp() * 10 ** 9)

        stream_response = api.search_messages(
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            stream=self._stream,
            resume_from_id=self._resume_from_id,
            search_direction=self._search_direction,
            result_count_limit=self._result_count_limit,
            keep_open=self._keep_open,
            filters=self._filters,
            message_id=self._message_id,
            attached_events=self._attached_events,
        )
        for response in stream_response:
            if response.WhichOneof("data") == "message":
                response = self._handle_adapters(response)
                yield response.message


class GetMessages(IGRPCProvider5Command, ProviderAdaptableCommand):
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
        search_direction: str = "NEXT",
        result_count_limit: int = None,
        keep_open: bool = False,
        filters: List[Filter] = None,
        message_id: List[str] = None,
        attached_events: bool = False,
        cache: bool = False,
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
            filters: Filters using in search for messages.
            message_id: List of message ids to restore the search
            attached_events: If true, it will additionally load attachedEventsIds.
            cache: If True, all requested data from rpt-data-provider will be saved to cache.
        """
        super().__init__()
        self._start_timestamp = start_timestamp
        self._end_timestamp = end_timestamp
        self._stream = stream
        self._resume_from_id = resume_from_id
        self._search_direction = search_direction
        self._result_count_limit = result_count_limit
        self._keep_open = keep_open
        self._filters = filters
        self._message_id = message_id
        self._attached_events = attached_events
        self._cache = cache

        self._decoder = GRPCObjectToDictAdapter()
        self._wrapper_deleter = DeleteMessageWrappersAdapter()

    def handle(self, data_source: GRPCProvider5DataSource) -> Data:
        source = partial(self.__handle_stream, data_source)
        return Data(source, cache=self._cache)

    def __handle_stream(self, data_source: GRPCProvider5DataSource) -> Iterable[dict]:
        stream = GetMessagesGRPCObject(
            start_timestamp=self._start_timestamp,
            end_timestamp=self._end_timestamp,
            stream=self._stream,
            resume_from_id=self._resume_from_id,
            search_direction=self._search_direction,
            result_count_limit=self._result_count_limit,
            keep_open=self._keep_open,
            message_id=self._message_id,
            attached_events=self._attached_events,
            filters=self._filters,
        ).handle(data_source)
        for message in stream:
            message = self._decoder.handle(message)
            message = self._wrapper_deleter.handle(message)
            message = self._handle_adapters(message)
            yield message
