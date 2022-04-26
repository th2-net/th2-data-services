from typing import List, NamedTuple

from th2_data_services.provider.v5.events_tree import ParentEventsTreeCollectionProvider5
from th2_data_services.provider.v5.struct import provider5_event_struct


def test_build_tree(general_data: List[dict], test_parent_events_tree: NamedTuple):
    collection = ParentEventsTreeCollectionProvider5(general_data)
    tree = collection.get_trees()[0]

    assert [
        event[provider5_event_struct.EVENT_ID] for event in tree.get_all_events()
    ] == test_parent_events_tree.events and list(
        collection.detached_events.keys()
    ) == test_parent_events_tree.unknown_events


def test_build_parentless_tree(general_data: List[dict]):
    collection = ParentEventsTreeCollectionProvider5(general_data)
    trees = collection.get_parentless_trees()

    template = {
        "attachedMessageIds": [],
        "batchId": "Broken_Event",
        "endTimestamp": {"nano": 0, "epochSecond": 0},
        "startTimestamp": {"nano": 0, "epochSecond": 0},
        "type": "event",
        "eventName": "Broken_Event",
        "eventType": "Broken_Event",
        "parentEventId": "Broken_Event",
        "successful": None,
        "isBatched": None,
    }

    assert trees[0].get_all_events() == [{"eventId": "a3779b94-d051-11eb-986f-1e8d42132387", **template}] and trees[
        1
    ].get_all_events() == [{"eventId": "845d70d2-9c68-11eb-8598-691ebd7f413d", **template}]
