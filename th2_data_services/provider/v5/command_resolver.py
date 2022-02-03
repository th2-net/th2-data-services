from typing import Union

from th2_data_services.provider.command import IProviderCommand
from th2_data_services.provider.v5.commands.grpc import GetEventById as GetEventByIdFromGRPC
from th2_data_services.provider.v5.commands.http import GetEventById as GetEventByIdFromHTTP
from th2_data_services.provider.v5.data_source.grpc import GRPCProvider5DataSource
from th2_data_services.provider.v5.data_source.http import HTTPProvider5DataSource


class GetEventById(IProviderCommand):
    def __init__(self, id: str):
        self._id = id

    def handle(self, data_source: Union[GRPCProvider5DataSource, HTTPProvider5DataSource]):
        if isinstance(data_source, GRPCProvider5DataSource):
            return GetEventByIdFromGRPC(self._id).handle(data_source)
        else:
            return GetEventByIdFromHTTP(self._id).handle(data_source)
