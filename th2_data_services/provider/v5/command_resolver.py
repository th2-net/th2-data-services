from typing import Union

from th2_data_services.provider.v5.commands.grpc import GetEventsById as GetEventsByIdFromGRPC
from th2_data_services.provider.v5.commands.http import GetEventsById as GetEventsByIdFromHTTP

from th2_data_services.provider.v5.commands.grpc import GetEventById as GetEventByIdFromGRPC
from th2_data_services.provider.v5.commands.http import GetEventById as GetEventByIdFromHTTP

from th2_data_services.provider.v5.data_source.grpc import GRPCProvider5DataSource
from th2_data_services.provider.v5.data_source.http import HTTPProvider5DataSource


def resolver_get_event_by_id(
    data_source: Union[GRPCProvider5DataSource, HTTPProvider5DataSource]
) -> Union[GetEventByIdFromGRPC, GetEventByIdFromHTTP]:
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
        raise ValueError("Unknown DataSource Object.")


def resolver_get_events_by_id(
    data_source: Union[GRPCProvider5DataSource, HTTPProvider5DataSource]
) -> Union[GetEventsByIdFromHTTP, GetEventsByIdFromGRPC]:
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
        raise ValueError("Unknown DataSource Object.")
