from datetime import datetime

import pytest

from th2_data_services import Data
from . import HTTPProviderAPI, HTTPProviderDataSource, http, CodecPipelinesAdapter, Filter, DEMO_PORT  # noqa  # noqa


@pytest.fixture
def demo_data_source():
    DEMO_HOST = "10.100.66.114"  # de-th2-qa
    data_source = HTTPProviderDataSource(f"http://{DEMO_HOST}:{DEMO_PORT}")
    return data_source


START_TIME = datetime(year=2022, month=11, day=9, hour=10, minute=13, second=17, microsecond=0)
END_TIME   = datetime(year=2022, month=11, day=9, hour=10, minute=13, second=24, microsecond=0)


@pytest.fixture
def demo_get_events_with_one_filter(demo_data_source: HTTPProviderDataSource) -> Data:
    case = demo_data_source.command(
        http.GetEvents(
            start_timestamp=START_TIME,
            end_timestamp=END_TIME,
            filters=[Filter("name", "Event for Filter test.")],
        )
    )
    # Returns 10 events
    return case


@pytest.fixture
def demo_get_events_with_filters(demo_data_source: HTTPProviderDataSource) -> Data:
    case = demo_data_source.command(
        http.GetEvents(
            start_timestamp=START_TIME,
            end_timestamp=END_TIME,
            filters=[Filter("name", "FilterString"), Filter("type", "ds-lib-test-event"), Filter("body", ["2","3"])],
        )
    )
    # Returns 2 events
    return case


@pytest.fixture
def demo_get_messages_with_one_filter(demo_data_source: HTTPProviderDataSource) -> Data:
    case = demo_data_source.command(
        http.GetMessages(
            start_timestamp=datetime(year=2022, month=6, day=30, hour=14, minute=48, second=20, microsecond=0),
            end_timestamp=datetime(year=2022, month=6, day=30, hour=14, minute=48, second=25, microsecond=0),
            stream=["arfq01fix07"],
            filters=Filter("type", "NewOrderSingle"),
        )
    )

    return case


@pytest.fixture
def demo_get_messages_with_filters(demo_data_source: HTTPProviderDataSource) -> Data:
    case = demo_data_source.command(
        http.GetMessages(
            start_timestamp=datetime(year=2022, month=6, day=30, hour=14, minute=48, second=20, microsecond=0),
            end_timestamp=datetime(year=2022, month=6, day=30, hour=14, minute=48, second=25, microsecond=0),
            stream=["arfq01fix07"],
            filters=[Filter("type", "NewOrderSingle"), Filter("body", "200")],
        )
    )

    return case


@pytest.fixture
def demo_events_from_data_source(demo_data_source: HTTPProviderDataSource) -> Data:
    events = demo_data_source.command(
        http.GetEvents(
            start_timestamp=START_TIME,
            end_timestamp=END_TIME,
        )
    )
    # Returns 21 events
    return events


@pytest.fixture
def demo_messages_from_data_source(demo_data_source: HTTPProviderDataSource) -> Data:
    messages = demo_data_source.command(
        http.GetMessages(
            start_timestamp=datetime(year=2022, month=6, day=30, hour=14, minute=58, second=0, microsecond=0),
            end_timestamp=END_TIME,
            stream=["arfq01fix07"],
        )
    )
    # Returns 239 messages
    return messages


@pytest.fixture
def demo_events_from_data_source_with_cache_status(
    demo_data_source: HTTPProviderDataSource,
) -> Data:
    events = demo_data_source.command(http.GetEvents(start_timestamp=START_TIME, end_timestamp=END_TIME, cache=True))
    # Returns 21 events
    return events


@pytest.fixture
def demo_messages_from_data_source_with_test_streams(
    demo_data_source: HTTPProviderDataSource,
) -> Data:
    messages = demo_data_source.command(
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
