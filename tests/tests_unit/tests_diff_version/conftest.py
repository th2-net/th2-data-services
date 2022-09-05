from datetime import datetime

import pytest

from th2_data_services import Data
from th2_data_services.events_tree import EventsTree
from . import HTTPProviderAPI, HTTPProviderDataSource, http, CodecPipelinesAdapter, Filter, DEMO_PORT  # noqa  # noqa


@pytest.fixture
def demo_data_source():
    DEMO_HOST = "10.100.66.114"  # de-th2-qa
    data_source = HTTPProviderDataSource(f"http://{DEMO_HOST}:{DEMO_PORT}")
    return data_source


START_TIME = datetime(year=2022, month=6, day=30, hour=14, minute=0, second=0, microsecond=0)
END_TIME = datetime(year=2022, month=6, day=30, hour=15, minute=0, second=0, microsecond=0)


@pytest.fixture
def demo_get_events_with_one_filter(demo_data_source: HTTPProviderDataSource) -> Data:
    case = demo_data_source.command(
        http.GetEvents(
            start_timestamp=START_TIME,
            end_timestamp=END_TIME,
            filters=[Filter("name", "TS_1")],
        )
    )

    return case


@pytest.fixture
def demo_get_events_with_filters(demo_data_source: HTTPProviderDataSource) -> Data:
    case = demo_data_source.command(
        http.GetEvents(
            start_timestamp=START_TIME,
            end_timestamp=END_TIME,
            filters=[Filter("name", "ExecutionReport"), Filter("type", "message"), Filter("body", "589")],
        )
    )

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
    # Returns 49 events #TODO change comments
    # Failed = 6
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
    # Returns 49 events #TODO change comments
    # Failed = 6
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


@pytest.fixture
def events_tree_for_test():
    tree = EventsTree()
    tree.create_root_event(event_name="root event", event_id="root_id", data={"data": [1, 2, 3, 4, 5]})
    tree.append_event(event_name="A", event_id="A_id", data=None, parent_id="root_id")
    tree.append_event(event_name="B", event_id="B_id", data=None, parent_id="root_id")
    tree.append_event(event_name="C", event_id="C_id", data={"data": "test data"}, parent_id="B_id")
    tree.append_event(event_name="D", event_id="D_id", data=None, parent_id="B_id")
    tree.append_event(event_name="D1", event_id="D1_id", data={"key1": "value1", "key2": "value2"}, parent_id="D_id")
    return tree
