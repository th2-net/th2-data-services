from typing import List, NamedTuple

from th2_data_services.provider.v5.events_tree import ParentsEventsTreesCollectionProvider5
from th2_data_services.provider.v5.struct import provider5_event_struct


def test_build_tree(general_data: List[dict], test_parent_events_tree: NamedTuple):
    collection = ParentsEventsTreesCollectionProvider5(general_data)
    tree = collection.get_trees()[0]

    assert [
        event[provider5_event_struct.EVENT_ID] for event in tree.get_all_events()
    ] == test_parent_events_tree.events and list(
        collection.detached_events.keys()
    ) == test_parent_events_tree.unknown_events
