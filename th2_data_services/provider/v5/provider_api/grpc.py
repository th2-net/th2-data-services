import logging
from datetime import timezone, datetime
from typing import Iterable, List

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
)
from grpc import Channel, insecure_channel
from th2_data_services.provider.source_api import IGRPCProviderSourceAPI

logger = logging.getLogger("th2_data_services")
logger.setLevel(logging.DEBUG)


class GRPCProvider5API(IGRPCProviderSourceAPI):
    def __init__(self, url: str):
        self._create_connection(url)

    def _create_connection(self, url: str) -> None:
        channel: Channel = insecure_channel(url)
        self.__stub: DataProviderStub = DataProviderStub(channel)

    def get_message_streams(self) -> StringList:
        return self.__stub.getMessageStreams(MessageStreamNamesRequest())

    # TODO Filters
    # TODO nano in timestamp
    def search_events(
        self,
        start_timestamp: datetime = None,
        end_timestamp: datetime = None,
        parent_event: str = None,
        search_direction: str = "NEXT",
        resume_from_id: str = None,
        result_count_limit: int = None,
        keep_open: bool = False,
        limit_for_parent: int = None,
        metadata_only: bool = True,
        attached_messages: bool = False,
    ) -> Iterable[StreamResponse]:
        if start_timestamp is None and resume_from_id is None:
            raise ValueError("One of the 'startTimestamp' or 'resumeFromId' must not be null.")

        if end_timestamp is None and result_count_limit is None:
            raise ValueError("One of the 'end_timestamp' or 'result_count_limit' must not be null.")

        if search_direction is not None:
            search_direction = search_direction.upper()
            if search_direction not in ("NEXT", "PREVIOUS"):
                raise ValueError("Argument 'search_direction' must be 'NEXT' or 'PREVIOUS'.")

        if start_timestamp:
            start_timestamp = start_timestamp.replace(tzinfo=timezone.utc).timestamp()
            start_timestamp = Timestamp(seconds=int(start_timestamp * 1000))

        if end_timestamp:
            end_timestamp = end_timestamp.replace(tzinfo=timezone.utc).timestamp()
            end_timestamp = Timestamp(seconds=int(end_timestamp * 1000))

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
        )
        return self.__stub.searchEvents(event_search_request)

    def search_messages(
        self,
        start_timestamp: datetime,
        stream: List[str],
        end_timestamp: datetime = None,
        resume_from_id: str = None,
        search_direction: str = None,
        result_count_limit: int = None,
        keep_open: bool = False,
        message_id: List[str] = None,
        attached_events: bool = False,
        look_limit_days: int = None,
    ) -> Iterable[StreamResponse]:
        if start_timestamp is None and resume_from_id is None:
            raise ValueError("One of the 'startTimestamp' or 'resumeFromId' must not be null.")

        if end_timestamp is None and result_count_limit is None:
            raise ValueError("One of the 'end_timestamp' or 'result_count_limit' must not be null.")

        if search_direction is not None:
            search_direction = search_direction.upper()
            if search_direction not in ("NEXT", "PREVIOUS"):
                raise ValueError("Argument 'search_direction' must be 'NEXT' or 'PREVIOUS'.")

        if stream is None:
            raise ValueError("Argument 'stream' is required.")

        # TODO

        # TODO END

        message_search_request = MessageSearchRequest()
        return self.__stub.searchMessages(message_search_request)

    def get_event(self, event_id: str) -> EventData:
        event_id = EventID(id=event_id)
        return self.__stub.getEvent(event_id)

    def get_message(self, message_id: str) -> MessageData:
        split_id = message_id.split(":")
        split_id.reverse()

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
        return self.__stub.getMessage(message_id)

    def get_messages_filters(self) -> ListFilterName:
        return self.__stub.getMessagesFilters(MessageFiltersRequest())

    def get_events_filters(self) -> ListFilterName:
        return self.__stub.getEventsFilters(EventFiltersRequest())

    def get_event_filter_info(self, filter_name: str) -> FilterInfo:
        filter_name = FilterName(filter_name=filter_name)
        return self.__stub.getEventFilterInfo(filter_name)

    def get_message_filter_info(self, filter_name: str) -> FilterInfo:
        filter_name = FilterName(filter_name=filter_name)
        return self.__stub.getMessageFilterInfo(filter_name)

    # TODO Filters
    def match_event(self, event_id: str, filters=None) -> IsMatched:
        match_request = MatchRequest(event_id=EventID(id=event_id), filters=filters)
        return self.__stub.matchEvent(match_request)

    # TODO Filters
    def match_message(self, message_id: str, filters=None) -> IsMatched:
        split_id = message_id.split(":")
        split_id.reverse()

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

        match_request = MatchRequest(message_id=message_id, filters=filters)
        return self.__stub.matchMessage(match_request)
