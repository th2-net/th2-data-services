from collections import namedtuple
import pytest

from th2_data_services import Data
from . import (
    HTTPProviderAPI,
    HTTPProviderDataSource,
    GRPCProviderDataSource,
    http,
    grpc,
    CodecPipelinesAdapter,
    Filter,
    HTTP_PORT,
    GRPC_PORT,
)  # noqa  # noqa
from . import START_TIME, END_TIME, MESSAGE_ID_1, STREAM_1, STREAM_2, all_message_bodies_http,all_message_bodies_grpc, all_event_bodies_http,all_event_bodies_grpc


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


DataCase = namedtuple("DataCase", ["data", "expected_data_values", "protocol"])


@pytest.fixture(
    params=[
        ("http_data_source", all_event_bodies_http, 'http'),
        ("grpc_data_source", all_event_bodies_grpc, 'grpc'),
    ]
)
def all_events(request) -> DataCase:
    protocol = request.param[2]
    if protocol == 'http':
        commands = http
    elif protocol == 'grpc':
        commands = grpc
    else:
        raise Exception('Unknown protocol')

    return DataCase(
        data=request.getfixturevalue(request.param[0]).command(
            commands.GetEvents(start_timestamp=START_TIME, end_timestamp=END_TIME)
        ),
        expected_data_values=request.param[1],
        protocol=protocol
    )


@pytest.fixture(
    params=[
        ("http_data_source", all_message_bodies_http, 'http'),
        ("grpc_data_source", all_message_bodies_grpc, 'grpc'),
    ]
)
def all_messages(request) -> DataCase:
    protocol = request.param[2]
    if protocol == 'http':
        commands = http
    elif protocol == 'grpc':
        commands = grpc
    else:
        raise Exception('Unknown protocol')

    return DataCase(
        data=request.getfixturevalue(request.param[0]).command(
            commands.GetMessages(start_timestamp=START_TIME,
                                 end_timestamp=END_TIME,
                                 stream=[STREAM_1, STREAM_2])
        ),
        expected_data_values=request.param[1],
        protocol=protocol
    )


# TODO - temp comment the following block. That works not like expected
# @pytest.fixture(params=["all_events", "all_messages"])
# def messages_and_events_common(request) -> DataCase:
#     return DataCase(
#         {
#             "events": request.getfixturevalue(request.param).command(
#                 http.GetEvents(start_timestamp=START_TIME, end_timestamp=END_TIME)
#             ),
#             "messages": request.getfixturevalue(request.param).command(
#                 http.GetMessages(start_timestamp=START_TIME, end_timestamp=END_TIME)
#             ),
#         },
#         {"events": all_event_bodies, "messages": all_message_bodies},
#     )


@pytest.fixture
def get_events_with_one_filter(http_data_source: HTTPProviderDataSource) -> Data:
    case = http_data_source.command(
        http.GetEvents(
            start_timestamp=START_TIME,
            end_timestamp=END_TIME,
            filters=[Filter("body", "FilterString-3")],
        )
    )

    return case


@pytest.fixture
def get_events_with_filters(http_data_source: HTTPProviderDataSource) -> Data:
    case = http_data_source.command(
        http.GetEvents(
            start_timestamp=START_TIME,
            end_timestamp=END_TIME,
            filters=[Filter("name", "FilterString"), Filter("type", "ds-lib-test-event"), Filter("body", ["3"])],
        )
    )
    return case


@pytest.fixture
def get_messages_with_one_filter(http_data_source: HTTPProviderDataSource) -> Data:
    case = http_data_source.command(
        http.GetMessages(
            start_timestamp=START_TIME,
            end_timestamp=END_TIME,
            stream=[STREAM_1, STREAM_2],
            filters=Filter("body", MESSAGE_ID_1.split(":")[2]),  # MESSAGE_ID_1.split(":")[2] to get the sequence number
        )
    )

    return case


@pytest.fixture
def get_messages_with_filters(http_data_source: HTTPProviderDataSource) -> Data:
    case = http_data_source.command(
        http.GetMessages(
            start_timestamp=START_TIME,
            end_timestamp=END_TIME,
            stream=[STREAM_1, STREAM_2],
            filters=[
                Filter("type", "Incoming"),
                Filter("body", MESSAGE_ID_1.split(":")[2]),
            ],  # MESSAGE_ID_1.split(":")[2] to get the sequence number
        )
    )

    return case


@pytest.fixture
def messages_from_data_source(http_data_source: HTTPProviderDataSource) -> Data:
    messages = http_data_source.command(
        http.GetMessages(
            start_timestamp=START_TIME,
            end_timestamp=END_TIME,
            stream=[STREAM_1, STREAM_2],
        )
    )
    # Returns 6 messages
    return messages


@pytest.fixture
def events_from_data_source_with_cache_status(
    http_data_source: HTTPProviderDataSource,
) -> Data:
    events = http_data_source.command(http.GetEvents(start_timestamp=START_TIME, end_timestamp=END_TIME, cache=True))

    return events


@pytest.fixture
def messages_from_data_source_with_streams(
    http_data_source: HTTPProviderDataSource,
) -> Data:
    messages = http_data_source.command(
        http.GetMessages(
            start_timestamp=START_TIME,
            end_timestamp=END_TIME,
            stream=[
                STREAM_1,
                STREAM_2,
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
