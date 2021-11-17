from th2_data_services.data_source import DataSource
from th2_data_services.events_tree.parent_events_tree import ParentEventsTree


def test_recover_events_tree(demo_data_source: DataSource, demo_events_from_data_source):
    parent_events_tree = ParentEventsTree(demo_events_from_data_source)

    before_recover_unknown_events = len(parent_events_tree.unknown_events)
    # 2 Missed events
    parent_events_tree.recover_unknown_events(demo_data_source)
    after_recover_unknown_events = len(parent_events_tree.unknown_events)

    assert before_recover_unknown_events != after_recover_unknown_events and after_recover_unknown_events == 0


def test_all_parent_events_from_stream_were_saved(demo_data_source: DataSource, demo_events_from_data_source):
    pet = ParentEventsTree(demo_events_from_data_source)
    pet.recover_unknown_events(demo_data_source)

    for e in demo_events_from_data_source:
        if e["parentEventId"] is not None:
            assert pet.events[e["parentEventId"]]
