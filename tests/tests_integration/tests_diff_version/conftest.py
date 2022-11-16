from collections import namedtuple
from datetime import datetime
import pytest

from th2_data_services import Data
from . import HTTPProviderAPI, HTTPProviderDataSource, GRPCProviderDataSource, http, grpc, CodecPipelinesAdapter, Filter, HTTP_PORT, GRPC_PORT  # noqa  # noqa
from . import START_TIME, END_TIME, MESSAGE_ID_1, STREAM_1, STREAM_2, all_test_message_bodies, all_test_event_bodies

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
            stream=[STREAM_1,STREAM_2],
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
            stream=[STREAM_1,STREAM_2],
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


@pytest.fixture
def messages_from_data_source_with_test_streams(
    data_source: HTTPProviderDataSource,
) -> Data:
    messages = data_source.command(
        http.GetMessages(
            start_timestamp=datetime(year=2022, month=6, day=30, hour=14, minute=58, second=0, microsecond=0),
            end_timestamp=END_TIME,
            stream=[
                "Test-123",
                "Test-1234",
                "Test-12345",
                "Test-123456",
                "Test-1234567",
                "Test-12345678",
                "Test-123456789",
                "Test-1234567810",
                "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest",
                "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest1",
                "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest2",
                "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest3",
                "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest4",
                "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest5",
                "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest6",
                "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest7",
                "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest8",
                "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest9",
                "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest10",
                "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest11",
                "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest12",
                "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest13",
                "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest14",
                "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest15",
                "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest16",
                "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest17",
                "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest18",
                "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest19",
                "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest20",
                "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest21",
                "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest22",
                "TestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTestTest23",
                "arfq01fix07",
                "arfq01dc03",
                "arfq02dc10",
            ],
        )
    )
    return messages