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

from th2_grpc_data_provider.data_provider_pb2 import (
    EventData,
    StreamResponse,
    MessageData,
)

from th2_data_services import Filter
from th2_data_services.provider.v5.command import IGRPCProvider5Command
from th2_data_services.provider.v5.data_source.grpc import GRPCProvider5DataSource
from th2_data_services.provider.v5.provider_api import GRPCProvider5API


class GetEventById(IGRPCProvider5Command):
    def __init__(self, id: str):
        self._id = id

    def handle(self, data_source: GRPCProvider5DataSource) -> EventData:
        api: GRPCProvider5API = data_source.source_api
        response = api.get_event(self._id)
        return response


class GetEventsById(IGRPCProvider5Command):
    def __init__(self, ids: List[str]):
        self.ids = ids

    def handle(self, data_source: GRPCProvider5DataSource) -> List[EventData]:
        api: GRPCProvider5API = data_source.source_api
        response = [api.get_event(event_id) for event_id in self.ids]
        return response


class GetEvents(IGRPCProvider5Command):
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

    def handle(self, data_source: GRPCProvider5DataSource) -> Iterable[StreamResponse]:
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
            yield response


class GetMessageById(IGRPCProvider5Command):
    def __init__(self, id: str):
        self._id = id

    def handle(self, data_source: GRPCProvider5DataSource) -> MessageData:
        api: GRPCProvider5API = data_source.source_api
        response = api.get_message(self._id)
        return response


class GetMessagesById(IGRPCProvider5Command):
    def __init__(self, ids: List[str]):
        self._ids = ids

    def handle(self, data_source: GRPCProvider5DataSource) -> List[MessageData]:
        response = []
        for id_ in self._ids:
            message = GetMessageById(id_).handle(data_source)
            response.append(message)
        return response


class GetMessages(IGRPCProvider5Command):
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
        lookup_limit_days: int = None,
        filters: List[Filter] = None,
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
        self._lookup_limit_days = lookup_limit_days
        self._filters = filters

    def handle(self, data_source: GRPCProvider5DataSource) -> List[MessageData]:
        api = data_source.source_api

        start_timestamp = self._start_timestamp.timestamp() * 10 ** 9
        end_timestamp = self._end_timestamp.timestamp() * 10 ** 9

        response = api.search_messages(
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            stream=self._stream,
            resume_from_ids=self._resume_from_id,
            search_direction=self._search_direction,
            result_count_limit=self._result_count_limit,
            keep_open=self._keep_open,
            attached_events=self._attached_events,
            lookup_limit_days=self._lookup_limit_days,
        )

        for message in response:
            yield message
