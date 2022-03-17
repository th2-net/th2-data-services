from datetime import datetime

from th2_data_services import Data
from th2_data_services.provider.v5.commands.http import GetEvents
from th2_data_services.provider.v5.data_source import HTTPProvider5DataSource
from th2_data_services.provider.v5.events_tree.events_trees_collection import EventsTreesCollectionProvider5


def test_recover_unknown_events():
    data_source = HTTPProvider5DataSource("http://10.64.66.66:30999/")
    events: Data = data_source.command(
        GetEvents(
            start_timestamp=datetime(year=2021, month=6, day=15, hour=9, minute=44, second=41, microsecond=692724),
            end_timestamp=datetime(year=2021, month=6, day=15, hour=12, minute=45, second=49, microsecond=28579),
        )
    )

    before_tree = events.len
    collection = EventsTreesCollectionProvider5(events, data_source=data_source)
    after_tree = len(collection)

    assert not collection.detached_events and before_tree != after_tree


def test_recover_unknown_events_with_stub_events():
    data_source = HTTPProvider5DataSource("http://10.64.66.66:30999/")
    events: Data = data_source.command(
        GetEvents(
            start_timestamp=datetime(year=2021, month=6, day=15, hour=9, minute=44, second=41, microsecond=692724),
            end_timestamp=datetime(year=2021, month=6, day=15, hour=12, minute=45, second=49, microsecond=28579),
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
    collection = EventsTreesCollectionProvider5(events, data_source=data_source, stub=True)
    after_tree = len(collection)

    assert collection.detached_events == {"Broken_Event": [broken_event]} and before_tree != after_tree


def test_preserve_body():
    data_source = HTTPProvider5DataSource("http://10.64.66.66:30999/")
    events: Data = data_source.command(
        GetEvents(
            start_timestamp=datetime(year=2021, month=6, day=15, hour=9, minute=44, second=41, microsecond=692724),
            end_timestamp=datetime(year=2021, month=6, day=15, hour=12, minute=45, second=49, microsecond=28579),
        )
    )

    collection = EventsTreesCollectionProvider5(events, data_source=data_source, preserve_body=True)

    assert all(
        [True if event.get("body") is not None else False for event in collection.get_trees()[0].get_all_events()]
    )
