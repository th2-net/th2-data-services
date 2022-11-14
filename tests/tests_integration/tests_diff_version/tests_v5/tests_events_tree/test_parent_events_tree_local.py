from datetime import datetime

from th2_data_services import Data
from th2_data_services.provider.v5.commands import http
from th2_data_services.provider.v5.data_source import HTTPProvider5DataSource
from th2_data_services.provider.v5.events_tree.parent_events_tree_collection import (
    ParentEventsTreeCollectionProvider5,
)

EVENT_ID_CHILD1 = '24aae778-6017-11ed-b87c-b48c9dc9ebfa'
EVENT_ID_CHILD2 = '24aae779-6017-11ed-9cb4-b48c9dc9ebfa'

def test_recover_unknown_events(demo_data_source: HTTPProvider5DataSource):
    events = demo_data_source.command(
        http.GetEventsById([EVENT_ID_CHILD1,EVENT_ID_CHILD2])
    )

    before_tree = len(events)
    collection = ParentEventsTreeCollectionProvider5(events, data_source=demo_data_source)
    after_tree = len(collection)

    assert not collection.detached_events and before_tree != after_tree


def test_recover_unknown_events_with_stub_events(demo_data_source: HTTPProvider5DataSource):
    events = demo_data_source.command(
        http.GetEventsById([EVENT_ID_CHILD1,EVENT_ID_CHILD2])
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
    collection = ParentEventsTreeCollectionProvider5(events, data_source=demo_data_source, stub=True)
    after_tree = len(collection)

    assert collection.detached_events == {"Broken_Event": [broken_event]} and before_tree != after_tree


def test_preserve_body(demo_data_source: HTTPProvider5DataSource):
    events = demo_data_source.command(
        http.GetEventsById([EVENT_ID_CHILD1,EVENT_ID_CHILD2])
    )

    collection = ParentEventsTreeCollectionProvider5(events, data_source=demo_data_source, preserve_body=True)

    assert all(
        [True if event.get("body") is not None else False for event in collection.get_trees()[0].get_all_events()]
    )
