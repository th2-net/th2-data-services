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

import logging
from typing import Iterable, List, Optional

from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.wrappers_pb2 import BoolValue, Int32Value, Int64Value
from th2_grpc_common.common_pb2 import MessageID, EventID, ConnectionID, Direction
from th2_grpc_data_provider.data_provider_pb2_grpc import DataProviderStub
from th2_grpc_data_provider.data_provider_pb2 import (
    MessageStreamNamesRequest,
    EventSearchRequest,
    MessageSearchRequest,
    MessageFiltersRequest,
    EventFiltersRequest,
    FilterName,
    MatchRequest,
    FilterInfo,
    ListFilterName,
    StreamResponse,
    EventData,
    StringList,
    IsMatched,
    MessageData,
    TimeRelation,
    Filter,
)
from grpc import Channel, insecure_channel
from th2_data_services.provider.source_api import IGRPCProviderSourceAPI

logger = logging.getLogger("th2_data_services")
logger.setLevel(logging.DEBUG)


class GRPCProvider5API(IGRPCProviderSourceAPI):
    def __init__(self, url: str):
        """GRPC Provider5 API.

        Args:
            url: GRPC data source url.
        """
        self._create_connection(url)

    def _create_connection(self, url: str) -> None:
        channel: Channel = insecure_channel(url)
        self.__stub: DataProviderStub = DataProviderStub(channel)

    def get_message_streams(self) -> StringList:
        """GRPC-API `getMessageStreams` call returns a list of message stream names."""
        return self.__stub.getMessageStreams(MessageStreamNamesRequest())

    # TODO Filters
    # TODO nano in timestamp
    # TODO - May be we change datetime to int (nano-seconds) or Timestamp? (Sviatoslav)
    def search_events(
        self,
        start_timestamp: int = None,
        end_timestamp: int = None,
        parent_event: str = None,
        search_direction: str = "NEXT",
        resume_from_id: str = None,
        result_count_limit: int = None,
        keep_open: bool = False,
        limit_for_parent: int = None,
        metadata_only: bool = True,
        attached_messages: bool = False,
        filters: Optional[List[Filter]] = None,
    ) -> Iterable[StreamResponse]:
        """GRPC-API `searchEvents` call creates an event or an event metadata stream that matches the filter.

        Args:
            TODO - by Sviatoslav

        Returns:
            TODO - by Sviatoslav
        """
        if filters is None:
            filters = []

        if start_timestamp is None and resume_from_id is None:
            raise ValueError("One of the 'startTimestamp' or 'resumeFromId' must not be null.")

        if end_timestamp is None and result_count_limit is None:
            raise ValueError("One of the 'end_timestamp' or 'result_count_limit' must not be null.")

        if search_direction is not None:
            search_direction = search_direction.upper()
            if search_direction not in ("NEXT", "PREVIOUS"):
                raise ValueError("Argument 'search_direction' must be 'NEXT' or 'PREVIOUS'.")

        if start_timestamp:
            nanos = start_timestamp % 10 ** 9
            seconds = start_timestamp // 10 ** 9
            start_timestamp = Timestamp(seconds=seconds, nanos=nanos)

        if end_timestamp:
            nanos = end_timestamp % 10 ** 9
            seconds = end_timestamp // 10 ** 9
            end_timestamp = Timestamp(seconds=seconds, nanos=nanos)

        parent_event = EventID(id=parent_event) if parent_event else None
        search_direction = TimeRelation.Value(search_direction)  # getting a value from enum
        resume_from_id = EventID(id=resume_from_id) if resume_from_id else EventID()
        result_count_limit = Int32Value(value=result_count_limit) if result_count_limit else None
        keep_open = BoolValue(value=keep_open)
        limit_for_parent = Int64Value(value=limit_for_parent) if limit_for_parent else None
        metadata_only = BoolValue(value=metadata_only)
        attached_messages = BoolValue(value=attached_messages)

        event_search_request = EventSearchRequest(
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            parent_event=parent_event,
            search_direction=search_direction,
            resume_from_id=resume_from_id,
            result_count_limit=result_count_limit,
            keep_open=keep_open,
            limit_for_parent=limit_for_parent,
            metadata_only=metadata_only,
            attached_messages=attached_messages,
            filters=filters,
        )
        return self.__stub.searchEvents(event_search_request)

    # TODO - message_search_request is empty
    def search_messages(
        self,
        start_timestamp: int,
        stream: List[str],
        end_timestamp: int = None,
        resume_from_ids: List[str] = None,
        search_direction: str = "NEXT",
        result_count_limit: int = None,
        keep_open: bool = False,
        attached_events: bool = False,
        lookup_limit_days: int = None,
        filters: Optional[List[Filter]] = None,
    ) -> Iterable[StreamResponse]:
        """GRPC-API `searchMessages` call creates a message stream that matches the filter.

        Args:
            TODO - by Sviatoslav

        Returns:
            TODO - by Sviatoslav
        """
        if filters is None:
            filters = []

        if start_timestamp is None and resume_from_ids is None:
            raise ValueError("One of the 'startTimestamp' or 'resumeFromId' must not be null.")

        if end_timestamp is None and result_count_limit is None:
            raise ValueError("One of the 'end_timestamp' or 'result_count_limit' must not be null.")

        if search_direction is not None:
            search_direction = search_direction.upper()
            if search_direction not in ("NEXT", "PREVIOUS"):
                raise ValueError("Argument 'search_direction' must be 'NEXT' or 'PREVIOUS'.")

        if stream is None:
            raise ValueError("Argument 'stream' is required.")

        if start_timestamp:
            nanos = start_timestamp % 10 ** 9
            seconds = start_timestamp // 10 ** 9
            start_timestamp = Timestamp(seconds=seconds, nanos=nanos)

        if end_timestamp:
            nanos = end_timestamp % 10 ** 9
            seconds = end_timestamp // 10 ** 9
            end_timestamp = Timestamp(seconds=seconds, nanos=nanos)

        search_direction = TimeRelation.Value(search_direction)  # getting a value from enum
        resume_from_ids = (
            [self.__build_message_id_object(id_) for id_ in resume_from_ids] if resume_from_ids else MessageID()
        )
        result_count_limit = Int32Value(value=result_count_limit) if result_count_limit else None
        keep_open = BoolValue(value=keep_open)
        attached_events = BoolValue(value=attached_events)
        lookup_limit_days = Int32Value(value=lookup_limit_days) if lookup_limit_days else None

        message_search_request = MessageSearchRequest(
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            search_direction=search_direction,
            resume_from_ids=resume_from_ids,
            result_count_limit=result_count_limit,
            keep_open=keep_open,
            attached_events=attached_events,
            lookup_limit_days=lookup_limit_days,
            filters=filters,
        )
        return self.__stub.searchMessages(message_search_request)

    @staticmethod
    def __build_message_id_object(message_id: str) -> MessageID:
        split_id = message_id.split(":")
        split_id.reverse()  # Parse the message id from the end.

        sequence, direction, alias = split_id[0], split_id[1].upper(), split_id[2:]
        split_sequence = sequence.split(".")
        sequence, subsequence = int(split_sequence[0]), split_sequence[1:]
        subsequence = map(int, subsequence) if subsequence else subsequence
        alias.reverse()
        alias = ":".join(alias)

        connection_id = ConnectionID(session_alias=alias)
        direction = Direction.Value(direction)  # Get a value from enum.

        message_id = MessageID(
            connection_id=connection_id,
            direction=direction,
            sequence=sequence,
            subsequence=subsequence,
        )
        return message_id

    def get_event(self, event_id: str) -> EventData:
        """GRPC-API `getEvent` call returns a single event with the specified id."""
        event_id = EventID(id=event_id)
        return self.__stub.getEvent(event_id)

    def get_message(self, message_id: str) -> MessageData:
        """GRPC-API `getMessage` call returns a single message with the specified id."""
        message_id = self.__build_message_id_object(message_id)
        return self.__stub.getMessage(message_id)

    def get_messages_filters(self) -> ListFilterName:
        """GRPC-API `getMessagesFilters` call returns all the names of sse message filters."""
        return self.__stub.getMessagesFilters(MessageFiltersRequest())

    def get_events_filters(self) -> ListFilterName:
        """GRPC-API `getEventsFilters` call returns all the names of sse event filters."""
        return self.__stub.getEventsFilters(EventFiltersRequest())

    def get_event_filter_info(self, filter_name: str) -> FilterInfo:
        """GRPC-API `getEventFilterInfo` call returns event filter info."""
        filter_name = FilterName(filter_name=filter_name)
        return self.__stub.getEventFilterInfo(filter_name)

    def get_message_filter_info(self, filter_name: str) -> FilterInfo:
        """GRPC-API `getMessageFilterInfo` call returns message filter info."""
        filter_name = FilterName(filter_name=filter_name)
        return self.__stub.getMessageFilterInfo(filter_name)

    def match_event(self, event_id: str, filters: List[Filter]) -> IsMatched:
        """GRPC-API `matchEvent` call checks that the event with the specified id is matched by the filter."""
        match_request = MatchRequest(event_id=EventID(id=event_id), filters=filters)
        return self.__stub.matchEvent(match_request)

    def match_message(self, message_id: str, filters: List[Filter]) -> IsMatched:
        """GRPC-API `matchMessage` call checks that the message with the specified id is matched by the filter."""
        message_id = self.__build_message_id_object(message_id)
        match_request = MatchRequest(message_id=message_id, filters=filters)
        return self.__stub.matchMessage(match_request)
