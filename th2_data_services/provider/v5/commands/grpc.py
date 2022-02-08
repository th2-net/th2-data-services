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
from datetime import datetime
from typing import List, Iterable

from grpc._channel import _InactiveRpcError
from th2_grpc_data_provider.data_provider_template_pb2 import (
    EventData,
    MessageData,
)

from th2_data_services import Filter
from th2_data_services.provider.command import IGRPCProviderAdaptableCommand
from th2_data_services.provider.v5.adapters.basic_adapters import AdapterGRPCObjectToDict
from th2_data_services.provider.v5.command import IGRPCProvider5Command

from th2_data_services.provider.v5.data_source.grpc import GRPCProvider5DataSource
from th2_data_services.provider.v5.provider_api import GRPCProvider5API


class GetEventByIdGRPCObject(IGRPCProvider5Command, IGRPCProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It retrieves the event by id as GRPC object.

    Returns:
        EventData: Th2 event.
    """

    def __init__(self, id: str):
        """
        Args:
            id: Event id.

        """
        super().__init__()
        self._id = id

    def handle(self, data_source: GRPCProvider5DataSource) -> EventData:
        api: GRPCProvider5API = data_source.source_api
        event = api.get_event(self._id)

        event = self._handle_adapters(event)
        return event


class GetEventById(IGRPCProvider5Command, IGRPCProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It retrieves the event by id.

    Returns:
        dict: Th2 event.

    Raises:
        ValueError: If event by Id wasn't found.
    """

    def __init__(self, id: str):
        """
        Args:
            id: Event id.

        """
        super().__init__()
        self._id = id
        self._decoder = AdapterGRPCObjectToDict()
        self._stub_status = False

    def handle(self, data_source: GRPCProvider5DataSource) -> dict:
        event = {data_source.event_struct.EVENT_ID: self._id}
        try:
            event = GetEventByIdGRPCObject(self._id).handle(data_source)
            event = self._decoder.handle(event)
        except _InactiveRpcError:
            if self._stub_status:
                event = data_source.event_stub.build(event)
            else:
                raise ValueError(f"Unable to find the event. Id: {self._id}")

        event = self._handle_adapters(event)
        return event

    def use_stub(self):
        self._stub_status = True
        return self


class GetEventsById(IGRPCProvider5Command, IGRPCProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It retrieves the events by id.

    Returns:
        List[dict]: Th2 events.

    Raises:
        ValueError: If any event by Id wasn't found.
    """

    def __init__(self, ids: List[str]):
        """
        Args:
            ids: Events ids.

        """
        super().__init__()
        self.ids = ids
        self._decoder = AdapterGRPCObjectToDict()
        self._stub_status = False

    def handle(self, data_source: GRPCProvider5DataSource) -> List[EventData]:
        api: GRPCProvider5API = data_source.source_api

        response = []
        for event_id in self.ids:
            event = {data_source.event_struct.EVENT_ID: event_id}
            try:
                event = api.get_event(event_id)
                event = self._decoder.handle(event)
            except _InactiveRpcError:
                if self._stub_status:
                    event = data_source.event_stub.build(event)
                else:
                    raise ValueError(f"Unable to find the event. Id: {event_id}")

            event = self._handle_adapters(event)
            response.append(event)
        return response

    def use_stub(self):
        self._stub_status = True
        return self


class GetEventsGRPCObjects(IGRPCProvider5Command, IGRPCProviderAdaptableCommand):
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
        metadata_only: bool = True,
        attached_messages: bool = False,
        filters: List[Filter] = None,
    ):
        """
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

    def handle(self, data_source: GRPCProvider5DataSource) -> Iterable[EventData]:
        api: GRPCProvider5API = data_source.source_api

        start_timestamp = int(self._start_timestamp.timestamp() * 10 ** 9)
        end_timestamp = int(self._end_timestamp.timestamp() * 10 ** 9)

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
            response = self._handle_adapters(response)
            yield response.event


class GetEvents(IGRPCProvider5Command, IGRPCProviderAdaptableCommand):
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
        metadata_only: bool = True,
        attached_messages: bool = False,
        filters: List[Filter] = None,
    ):
        """
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

        self._decoder = AdapterGRPCObjectToDict()

    def handle(self, data_source: GRPCProvider5DataSource) -> Iterable[dict]:
        stream = GetEventsGRPCObjects(
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
        ).handle(data_source)
        for event in stream:
            event = self._decoder.handle(event)
            event = self._handle_adapters(event)
            yield event


class GetMessageByIdGRPCObject(IGRPCProvider5Command, IGRPCProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It retrieves the message by id as GRPC Object.

    Returns:
        MessageData: Th2 message.
    """

    def __init__(self, id: str):
        """
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


class GetMessageById(IGRPCProvider5Command, IGRPCProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It retrieves the message by id.

    Returns:
        dict: Th2 message.

    Raises:
        ValueError: If message by id wasn't found.
    """

    def __init__(self, id: str):
        """
        Args:
            id: Message id.

        """
        super().__init__()
        self._id = id
        self._decoder = AdapterGRPCObjectToDict()
        self._stub_status = False

    def handle(self, data_source: GRPCProvider5DataSource) -> dict:
        message = {data_source.message_struct.MESSAGE_ID: self._id}
        try:
            message = GetMessageByIdGRPCObject(self._id).handle(data_source)
            message = self._decoder.handle(message)
        except _InactiveRpcError:
            if self._stub_status:
                message = data_source.message_stub.build(message)
            else:
                raise ValueError(f"Unable to find the message. Id: {self._id}")
        message = self._handle_adapters(message)
        return message

    def use_stub(self):
        self._stub_status = True
        return self


class GetMessagesById(IGRPCProvider5Command, IGRPCProviderAdaptableCommand):
    """A Class-Command for request to rpt-data-provider.

    It retrieves the messages by id.

    Returns:
        List[dict]: Th2 messages.

    Raises:
        ValueError: If any message by id wasn't found.
    """

    def __init__(self, ids: List[str]):
        """
        Args:
            ids: Messages id.

        """
        super().__init__()
        self._ids = ids
        self._decoder = AdapterGRPCObjectToDict()
        self._stub_status = False

    def handle(self, data_source: GRPCProvider5DataSource) -> List[dict]:
        response = []
        for id_ in self._ids:
            message = {data_source.message_struct.MESSAGE_ID: id_}
            try:
                message = GetMessageByIdGRPCObject(id_).handle(data_source)
                message = self._decoder.handle(message)
            except _InactiveRpcError:
                if self._stub_status:
                    message = data_source.message_stub.build(message)
                else:
                    raise ValueError(f"Unable to find the message. Id: {id_}")
            message = self._handle_adapters(message)
            response.append(message)
        return response

    def use_stub(self):
        self._stub_status = True
        return self


class GetMessagesGRPCObject(IGRPCProvider5Command, IGRPCProviderAdaptableCommand):
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
        filters: List[Filter] = None,
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

    def handle(self, data_source: GRPCProvider5DataSource) -> List[MessageData]:
        api = data_source.source_api

        start_timestamp = int(self._start_timestamp.timestamp() * 10 ** 9)
        end_timestamp = int(self._end_timestamp.timestamp() * 10 ** 9)

        stream_response = api.search_messages(
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            stream=self._stream,
            resume_from_id=self._resume_from_id,
            search_direction=self._search_direction,
            result_count_limit=self._result_count_limit,
            keep_open=self._keep_open,
            filters=self._filters,
        )

        for response in stream_response:
            response = self._handle_adapters(response)
            yield response.message


class GetMessages(IGRPCProvider5Command, IGRPCProviderAdaptableCommand):
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

        self._decoder = AdapterGRPCObjectToDict()

    def handle(self, data_source: GRPCProvider5DataSource) -> List[dict]:
        stream = GetMessagesGRPCObject(
            start_timestamp=self._start_timestamp,
            end_timestamp=self._end_timestamp,
            stream=self._stream,
            resume_from_id=self._resume_from_id,
            search_direction=self._search_direction,
            result_count_limit=self._result_count_limit,
            keep_open=self._keep_open,
            filters=self._filters,
        ).handle(data_source)
        for message in stream:
            message = self._decoder.handle(message)
            message = self._handle_adapters(message)
            yield message
