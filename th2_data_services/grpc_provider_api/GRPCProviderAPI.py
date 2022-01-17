from typing import Iterable
from th2_grpc_common.common_pb2 import MessageID, EventID
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
)
from grpc import Channel, insecure_channel
from th2_data_services.grpc_provider_api.IGRPCProviderAPI import IGRPCProviderAPI


class GRPCProviderAPI(IGRPCProviderAPI):
    def __init__(self, url: str):
        self._create_connection(url)

    def _create_connection(self, url: str) -> None:
        channel: Channel = insecure_channel(url)
        self.__stub: DataProviderStub = DataProviderStub(channel)

    def get_message_streams(self) -> StringList:
        return self.__stub.getMessageStreams(MessageStreamNamesRequest())

    def search_events(self, event_search_request: EventSearchRequest) -> Iterable[StreamResponse]:
        return self.__stub.searchEvents(event_search_request)

    def search_messages(self, message_search_request: MessageSearchRequest) -> Iterable[StreamResponse]:
        return self.__stub.searchMessages(message_search_request)

    def get_event(self, event_id: EventID) -> EventData:
        return self.__stub.getEvent(event_id)

    def get_message(self, message_id: MessageID) -> MessageData:
        return self.__stub.getMessage(message_id)

    def get_messages_filters(self) -> ListFilterName:
        return self.__stub.getMessagesFilters(MessageFiltersRequest())

    def get_events_filters(self) -> ListFilterName:
        return self.__stub.getEventsFilters(EventFiltersRequest())

    def get_event_filter_info(self, filter_name: FilterName) -> FilterInfo:
        return self.__stub.getEventFilterInfo(filter_name)

    def get_message_filter_info(self, filter_name: FilterName) -> FilterInfo:
        return self.__stub.getMessageFilterInfo(filter_name)

    def match_event(self, match_request: MatchRequest) -> IsMatched:
        return self.__stub.matchEvent(match_request)

    def match_message(self, match_message: MatchRequest) -> IsMatched:
        return self.__stub.matchMessage(match_message)
