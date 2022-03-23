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

from typing import Union, Type

from th2_data_services.provider.interfaces import IProviderDataSource
from th2_data_services.provider.v5.commands.grpc import GetEventsById as GetEventsByIdFromGRPC
from th2_data_services.provider.v5.commands.http import GetEventsById as GetEventsByIdFromHTTP

from th2_data_services.provider.v5.commands.grpc import GetEventById as GetEventByIdFromGRPC
from th2_data_services.provider.v5.commands.http import GetEventById as GetEventByIdFromHTTP

from th2_data_services.provider.v5.data_source.grpc import GRPCProvider5DataSource
from th2_data_services.provider.v5.data_source.http import HTTPProvider5DataSource


def resolver_get_event_by_id(
    data_source: IProviderDataSource,
) -> Union[Type[GetEventByIdFromHTTP], Type[GetEventByIdFromGRPC]]:
    """Resolves what 'GetEventById' command you need to use based Data Source.

    Args:
        data_source: DataSource instance.

    Returns:
        GetEventById command.
    """
    if isinstance(data_source, GRPCProvider5DataSource):
        return GetEventByIdFromGRPC
    elif isinstance(data_source, HTTPProvider5DataSource):
        return GetEventByIdFromHTTP
    else:
        raise ValueError("Unknown DataSource Object")


def resolver_get_events_by_id(
    data_source: IProviderDataSource,
) -> Union[Type[GetEventsByIdFromHTTP], Type[GetEventsByIdFromGRPC]]:
    """Resolves what 'GetEventsById' command you need to use based Data Source.

    Args:
        data_source: DataSource instance.

    Returns:
        GetEventsById command.
    """
    if isinstance(data_source, GRPCProvider5DataSource):
        return GetEventsByIdFromGRPC
    elif isinstance(data_source, HTTPProvider5DataSource):
        return GetEventsByIdFromHTTP
    else:
        raise ValueError("Unknown DataSource Object")
