from datetime import datetime

import pytest

from th2_data_services import Data
from . import HTTPProviderAPI, HTTPProviderDataSource, http, CodecPipelinesAdapter, Filter, PORT  # noqa  # noqa


@pytest.fixture
def data_source():
    HOST = "10.100.66.114"  # de-th2-qa
    data_source = HTTPProviderDataSource(f"http://{HOST}:{PORT}")
    return data_source


START_TIME_EVENT = datetime(year=2022, month=11, day=9, hour=10, minute=13, second=17, microsecond=0)
END_TIME_EVENT   = datetime(year=2022, month=11, day=9, hour=10, minute=13, second=24, microsecond=0)

START_TIME_MESSAGE = datetime(year=2022, month=11, day=10, hour=8, minute=15, second=11, microsecond=0)
END_TIME_MESSAGE   = datetime(year=2022, month=11, day=10, hour=8, minute=15, second=20, microsecond=0)


@pytest.fixture
def get_events_with_one_filter(data_source: HTTPProviderDataSource) -> Data:
    case = data_source.command(
        http.GetEvents(
            start_timestamp=START_TIME_EVENT,
            end_timestamp=END_TIME_EVENT,
            filters=[Filter("name", "Event for Filter test. FilterString-3")],
        )
    )

    return case


@pytest.fixture
def get_events_with_filters(data_source: HTTPProviderDataSource) -> Data:
    case = data_source.command(
        http.GetEvents(
            start_timestamp=START_TIME_EVENT,
            end_timestamp=END_TIME_EVENT,
            filters=[Filter("name", "FilterString"), Filter("type", "ds-lib-test-event"), Filter("body", ["3"])],
        )
    )
    return case


@pytest.fixture
def get_messages_with_one_filter(data_source: HTTPProviderDataSource) -> Data:
    case = data_source.command(
        http.GetMessages(
            start_timestamp=START_TIME_MESSAGE,
            end_timestamp=END_TIME_MESSAGE,
            stream=["ds-lib-session1"],
            filters=Filter("type", "Incoming"),
        )
    )

    return case


@pytest.fixture
def get_messages_with_filters(data_source: HTTPProviderDataSource) -> Data:
    case = data_source.command(
        http.GetMessages(
            start_timestamp=START_TIME_MESSAGE,
            end_timestamp=END_TIME_MESSAGE,
            stream=["ds-lib-session1","ds-lib-session2"],
            filters=[Filter("type", "Incoming"), Filter("body", "1668068118435545201")],
        )
    )

    return case


@pytest.fixture
def events_from_data_source(data_source: HTTPProviderDataSource) -> Data:
    events = data_source.command(
        http.GetEvents(
            start_timestamp=START_TIME_EVENT,
            end_timestamp=END_TIME_EVENT,
        )
    )
    # Returns 21 events
    return events


@pytest.fixture
def messages_from_data_source(data_source: HTTPProviderDataSource) -> Data:
    messages = data_source.command(
        http.GetMessages(
            start_timestamp=START_TIME_MESSAGE,
            end_timestamp=END_TIME_MESSAGE,
            stream=["ds-lib-session1"],
        )
    )
    # Returns 2 messages
    return messages


@pytest.fixture
def events_from_data_source_with_cache_status(
    data_source: HTTPProviderDataSource,
) -> Data:
    events = data_source.command(http.GetEvents(start_timestamp=START_TIME_EVENT, end_timestamp=END_TIME_EVENT, cache=True))
    # Returns 21 events
    return events


@pytest.fixture
def messages_from_data_source_with_test_streams(
    data_source: HTTPProviderDataSource,
) -> Data:
    messages = data_source.command(
        http.GetMessages(
            start_timestamp=START_TIME_MESSAGE,
            end_timestamp=END_TIME_MESSAGE,
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
