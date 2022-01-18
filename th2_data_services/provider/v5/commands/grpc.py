from datetime import datetime
from typing import List

from th2_grpc_common.common_pb2 import EventID

from th2_data_services.command import IGRPCProviderCommand
from th2_data_services.provider.v5.data_source.grpc import GRPCProvider5DataSource
from th2_data_services.provider.v5.provider_api import GRPCProvider5API


class GetEventById(IGRPCProviderCommand):
    def __init__(self, id_: str):
        self._id = id_

    def handle(self, data_source: GRPCProvider5DataSource):
        api: GRPCProvider5API = data_source.source_api

        event_id = EventID(id=self._id)
        response = api.get_event(event_id)

        return response


class GetEventsById(IGRPCProviderCommand):
    def __init__(self, ids: List[str]):
        self.ids = ids

    def handle(self, data_source: GRPCProvider5DataSource):
        api: GRPCProvider5API = data_source.source_api

        response = [api.get_event(EventID(id=event_id)) for event_id in self.ids]
        return response


class GetEvents(IGRPCProviderCommand):
    def __init__(
        self,
        start_timestamp: datetime,
        end_timestamp: datetime,
        parent_event: str = None,
        search_direction: str = "NEXT",
        resume_from_id: str = None,
        result_count_limit: int = None,
        keep_open: bool = False,
        limit_for_parent: int = None,
        metadata_only: bool = True,
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

    # TODO Filters
    def handle(self, data_source: GRPCProvider5DataSource):
        api: GRPCProvider5API = data_source.source_api

        # event_search_request = EventSearchRequest(
        #     start_timestamp=Timestamp(),
        #     end_timestamp=Timestamp(),
        #     parent_event=EventID(),
        #     search_direction=TimeRelation(),
        # )
        api.search_events()
