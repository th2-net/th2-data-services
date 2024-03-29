from datetime import datetime

import pytest

from th2_data_services import Data
from th2_data_services.provider.v5.commands.http import GetEvents
from th2_data_services.provider.v5.data_source import HTTPProvider5DataSource
from th2_data_services.provider.v5.events_tree.parent_events_tree_collection import (
    ParentEventsTreeCollectionProvider5,
)


@pytest.mark.skip
def test_recover_unknown_events():
    data_source = HTTPProvider5DataSource("http://10.100.66.114:31787/")
    events: Data = data_source.command(
        GetEvents(
            start_timestamp=datetime(year=2022, month=6, day=30, hour=14, minute=0, second=0, microsecond=0),
            end_timestamp=datetime(year=2022, month=6, day=30, hour=15, minute=0, second=0, microsecond=0),
        )
    )

    before_tree = events.len
    collection = ParentEventsTreeCollectionProvider5(events, data_source=data_source)
    after_tree = len(collection)

    assert not collection.detached_events and before_tree != after_tree


@pytest.mark.skip
def test_recover_unknown_events_with_stub_events():
    data_source = HTTPProvider5DataSource("http://10.100.66.114:31787/")
    events: Data = data_source.command(
        GetEvents(
            start_timestamp=datetime(year=2022, month=6, day=30, hour=14, minute=0, second=0, microsecond=0),
            end_timestamp=datetime(year=2022, month=6, day=30, hour=15, minute=0, second=0, microsecond=0),
        )
    )

    broken_event = {
        "attachedMessageIds": [],
        "batchId": "Broken_Event",
        "endTimestamp": {"nano": 0, "epochSecond": 0},
        "startTimestamp": {"nano": 0, "epochSecond": 0},
        "type": "event",
        "eventId": f"33499-333-111-test-03221",
        "eventName": "Broken_Event",
        "eventType": "Broken_Event",
        "parentEventId": "Broken_Event",
        "successful": None,
        "isBatched": None,
    }
    events: list = [event for event in events] + [broken_event]

    before_tree = len(events)
    collection = ParentEventsTreeCollectionProvider5(events, data_source=data_source, stub=True)
    after_tree = len(collection)

    assert collection.detached_events == {"Broken_Event": [broken_event]} and before_tree != after_tree


@pytest.mark.skip
def test_preserve_body():
    data_source = HTTPProvider5DataSource("http://10.100.66.114:31787/")
    events: Data = data_source.command(
        GetEvents(
            start_timestamp=datetime(year=2022, month=6, day=30, hour=14, minute=0, second=0, microsecond=0),
            end_timestamp=datetime(year=2022, month=6, day=30, hour=15, minute=0, second=0, microsecond=0),
        )
    )

    collection = ParentEventsTreeCollectionProvider5(events, data_source=data_source, preserve_body=True)

    assert all(
        [True if event.get("body") is not None else False for event in collection.get_trees()[0].get_all_events()]
    )
