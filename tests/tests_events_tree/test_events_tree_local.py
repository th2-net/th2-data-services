from datetime import datetime
from th2_data_services import Data
from th2_data_services.provider.v5.commands.http import GetEvents
from th2_data_services.provider.v5.data_source import HTTPProvider5DataSource
from th2_data_services.provider.v5.events_tree.events_tree_collection import EventsTreeCollectionProvider5


def test_recover_unknown_events():
    data_source = HTTPProvider5DataSource("http://10.64.66.66:30999/")
    events: Data = data_source.command(
        GetEvents(
            start_timestamp=datetime(year=2021, month=6, day=15, hour=9, minute=44, second=41, microsecond=692724),
            end_timestamp=datetime(year=2021, month=6, day=15, hour=12, minute=45, second=49, microsecond=28579),
        )
    )

    before_tree = events.len
    collection = EventsTreeCollectionProvider5(events, data_source=data_source)
    after_tree = len(collection)

    assert not collection.detached_events and before_tree != after_tree


def test_recover_unknown_events_ds_passed_into_method():
    data_source = HTTPProvider5DataSource("http://10.64.66.66:30999/")
    events: Data = data_source.command(
        GetEvents(
            start_timestamp=datetime(year=2021, month=6, day=15, hour=9, minute=44, second=41, microsecond=692724),
            end_timestamp=datetime(year=2021, month=6, day=15, hour=12, minute=45, second=49, microsecond=28579),
        )
    )

    before_tree = events.len
    collection = EventsTreeCollectionProvider5(events)
    collection.recover_unknown_events(data_source=data_source)
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
    collection = EventsTreeCollectionProvider5(events, data_source=data_source, stub=True)
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

    collection = EventsTreeCollectionProvider5(events, data_source=data_source, preserve_body=True)

    assert all(
        [True if event.get("body") is not None else False for event in collection.get_trees()[0].get_all_events()]
    )


def test_create_subtree_incoming_data_stream():
    data_source = HTTPProvider5DataSource("http://10.64.66.66:30999/")
    events: Data = data_source.command(
        GetEvents(
            start_timestamp=datetime(year=2021, month=6, day=15, hour=9, minute=44, second=41, microsecond=692724),
            end_timestamp=datetime(year=2021, month=6, day=15, hour=12, minute=45, second=49, microsecond=28579),
        )
    )
    tree = EventsTreeCollectionProvider5(events, preserve_body=True).get_trees()[0]
    etc_1 = EventsTreeCollectionProvider5(tree.findall(lambda e: e["eventName"]), preserve_body=True)
    sub_tree_0 = etc_1.get_trees()[0]
    root_sub_tree_0 = sub_tree_0.get_root().copy()
    etc_2 = EventsTreeCollectionProvider5(tree.findall(lambda e: e["eventName"]))
    assert root_sub_tree_0 != etc_2.get_trees()[0]
    assert root_sub_tree_0 == sub_tree_0.get_root()
    assert root_sub_tree_0.get("body") == {} and etc_2.get_trees()[0].get_root().get("body") is None
