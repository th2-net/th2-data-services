from datetime import datetime
from typing import List, Iterable

from th2_grpc_data_provider.data_provider_pb2 import (
    EventData,
    StreamResponse,
    MessageData,
)

from th2_data_services.command import IGRPCProviderCommand
from th2_data_services.provider.v5.data_source.grpc import GRPCProvider5DataSource
from th2_data_services.provider.v5.provider_api import GRPCProvider5API


class GetEventById(IGRPCProviderCommand):
    def __init__(self, id_: str):
        self._id = id_

    def handle(self, data_source: GRPCProvider5DataSource) -> EventData:
        api: GRPCProvider5API = data_source.source_api
        response = api.get_event(self._id)
        return response


class GetEventsById(IGRPCProviderCommand):
    def __init__(self, ids: List[str]):
        self.ids = ids

    def handle(self, data_source: GRPCProvider5DataSource) -> List[EventData]:
        api: GRPCProvider5API = data_source.source_api
        response = [api.get_event(event_id) for event_id in self.ids]
        return response


# TODO Events
class GetEvents(IGRPCProviderCommand):
    def __init__(
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
    ):
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

    def handle(self, data_source: GRPCProvider5DataSource) -> Iterable[StreamResponse]:
        api: GRPCProvider5API = data_source.source_api
        stream_response = api.search_events(
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
        )
        for response in stream_response:
            yield response


class GetMessageById(IGRPCProviderCommand):
    def __init__(self, id_: str):
        self._id = id_

    def handle(self, data_source: GRPCProvider5DataSource) -> MessageData:
        api: GRPCProvider5API = data_source.source_api
        response = api.get_message(self._id)
        return response


class GetMessagesById(IGRPCProviderCommand):
    def __init__(self, ids: List[str]):
        self._ids = ids

    def handle(self, data_source: GRPCProvider5DataSource) -> List[MessageData]:
        response = []
        for id_ in self._ids:
            message = GetMessageById(id_).handle(data_source)
            response.append(message)
        return response


# TODO Filters
class GetMessages(IGRPCProviderCommand):
    def __init__(
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
    ):
        self._start_timestamp = start_timestamp
        self._end_timestamp = end_timestamp
        self._stream = stream
        self._resume_from_id = resume_from_id
        self._search_direction = search_direction
        self._result_count_limit = result_count_limit
        self._keep_open = keep_open
        self._message_id = message_id
        self._attached_events = attached_events
        self._look_limit_days = look_limit_days

    def handle(self, data_source: GRPCProvider5DataSource) -> List[MessageData]:
        api = data_source.source_api

        response = api.search_messages(
            start_timestamp=self._start_timestamp,
            end_timestamp=self._end_timestamp,
            stream=self._stream,
            resume_from_id=self._resume_from_id,
            search_direction=self._search_direction,
            result_count_limit=self._result_count_limit,
            keep_open=self._keep_open,
            message_id=self._message_id,
            attached_events=self._attached_events,
            look_limit_days=self._look_limit_days,
        )

        for message in response:
            yield message
