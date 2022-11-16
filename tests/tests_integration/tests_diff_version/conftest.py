from collections import namedtuple
from datetime import datetime
import pytest

from th2_data_services import Data
from . import HTTPProviderAPI, HTTPProviderDataSource, GRPCProviderDataSource, http, grpc, CodecPipelinesAdapter, Filter, HTTP_PORT, GRPC_PORT  # noqa  # noqa
from . import START_TIME, END_TIME, MESSAGE_ID_1, all_test_message_bodies, all_test_event_bodies

@pytest.fixture
def http_data_source():
    HOST = "10.100.66.114"  # de-th2-qa
    data_source = HTTPProviderDataSource(f"http://{HOST}:{HTTP_PORT}")
    return data_source

@pytest.fixture
def grpc_data_source():
    HOST = "10.100.66.114"
    data_source = GRPCProviderDataSource(f"{HOST}:{GRPC_PORT}")
    return data_source


DataCase = namedtuple("DataCase", ["data", "expected_data_values"])


@pytest.fixture(
    params=[
        DataCase(http_data_source.command(http.GetEvents(start_timestamp=START_TIME,end_timestamp=END_TIME)), all_test_event_bodies),
        DataCase(grpc_data_source.command(grpc.GetEvents(start_timestamp=START_TIME,end_timestamp=END_TIME)), all_test_event_bodies)
    ]
)
def all_events(request) -> DataCase:
    return request.param

@pytest.fixture(
    params=[
        DataCase(http_data_source.command(http.GetMessages(start_timestamp=START_TIME,end_timestamp=END_TIME)), all_test_message_bodies),
        DataCase(grpc_data_source.command(grpc.GetMessages(start_timestamp=START_TIME,end_timestamp=END_TIME)), all_test_message_bodies)
    ]
)
def all_messages(request) -> Data:
    return request.param


@pytest.fixture(
    params=[
        DataCase({
            "events":http_data_source.command(http.GetEvents(start_timestamp=START_TIME,end_timestamp=END_TIME)),
            "messages":http_data_source.command(http.GetMessages(start_timestamp=START_TIME,end_timestamp=END_TIME)),
        },
        {
            "events":all_test_event_bodies,
            "messages":all_test_message_bodies
        }
        ),
        DataCase({
            "events":grpc_data_source.command(grpc.GetEvents(start_timestamp=START_TIME,end_timestamp=END_TIME)),
            "messages":grpc_data_source.command(grpc.GetMessages(start_timestamp=START_TIME,end_timestamp=END_TIME)),
        },
        {
            "events":all_test_event_bodies,
            "messages":all_test_message_bodies
        }
        )
    ]
)
def messages_and_events_common(request):
    return request.param


@pytest.fixture
def get_events_with_one_filter(data_source: HTTPProviderDataSource) -> Data:
    case = data_source.command(
        http.GetEvents(
            start_timestamp=START_TIME,
            end_timestamp=END_TIME,
            filters=[Filter("body", "FilterString-3")],
        )
    )

    return case


@pytest.fixture
def get_events_with_filters(data_source: HTTPProviderDataSource) -> Data:
    case = data_source.command(
        http.GetEvents(
            start_timestamp=START_TIME,
            end_timestamp=END_TIME,
            filters=[Filter("name", "FilterString"), Filter("type", "ds-lib-test-event"), Filter("body", ["3"])],
        )
    )
    return case


@pytest.fixture
def get_messages_with_one_filter(data_source: HTTPProviderDataSource) -> Data:
    case = data_source.command(
        http.GetMessages(
            start_timestamp=START_TIME,
            end_timestamp=END_TIME,
            stream=["ds-lib-session1","ds-lib-session2"],
            filters=Filter("body", MESSAGE_ID_1),
        )
    )

    return case


@pytest.fixture
def get_messages_with_filters(data_source: HTTPProviderDataSource) -> Data:
    case = data_source.command(
        http.GetMessages(
            start_timestamp=START_TIME,
            end_timestamp=END_TIME,
            stream=["ds-lib-session1","ds-lib-session2"],
            filters=[Filter("type", "Incoming"), Filter("body", MESSAGE_ID_1)]
        )
    )

    return case


@pytest.fixture
def events_from_data_source_with_cache_status(
    data_source: HTTPProviderDataSource,
) -> Data:
    events = data_source.command(http.GetEvents(start_timestamp=START_TIME, end_timestamp=END_TIME, cache=True))
    
    return events