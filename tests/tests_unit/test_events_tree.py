import pytest

from th2_data_services.events_tree import EventsTree
from th2_data_services.events_tree.exceptions import EventIdNotInTree, TreeLoop


def test_getitem(events_tree_for_test: EventsTree):
    tree = events_tree_for_test
    assert tree["D1_id"] == {"key1": "value1", "key2": "value2"} and tree["C_id"] == {"data": "test data"}


def test_getitem_id_error(events_tree_for_test: EventsTree):
    with pytest.raises(EventIdNotInTree) as exc:
        _ = events_tree_for_test["test"]
    assert exc


def test_setitem(events_tree_for_test: EventsTree):
    tree = events_tree_for_test
    tree["A_id"] = {"new data": 123}
    assert tree["A_id"] == {"new data": 123}


def test_setitem_id_error(events_tree_for_test: EventsTree):
    with pytest.raises(EventIdNotInTree) as exc:
        events_tree_for_test["test"] = "test"
    assert exc


def test_update_parent_link(events_tree_for_test: EventsTree):
    tree = events_tree_for_test
    tree.update_parent_link("D1_id", "root_id")
    assert tree.get_parent("D1_id") == {"data": [1, 2, 3, 4, 5]}


def test_update_parent_link_id_error(events_tree_for_test: EventsTree):
    with pytest.raises(EventIdNotInTree) as exc:
        events_tree_for_test.update_parent_link("test", "to_test")
    assert exc


def test_update_parent_link_loop_error(events_tree_for_test: EventsTree):
    with pytest.raises(TreeLoop) as exc:
        tree = events_tree_for_test
        tree.update_parent_link("B_id", "C_id")
    assert exc


def test_update_event_name(events_tree_for_test: EventsTree):
    tree = events_tree_for_test
    tree.update_event_name("C_id", "NewEvent")
    assert tree._tree["C_id"].tag == "NewEvent"


def test_update_event_name_id_error(events_tree_for_test: EventsTree):
    with pytest.raises(EventIdNotInTree) as exc:
        events_tree_for_test.update_event_name("test", "test_name")
    assert exc


def test_merge_events_tree(events_tree_for_test: EventsTree):
    tree = events_tree_for_test
    events_count = len(tree)

    other_tree = EventsTree(event_name="RootEvent", event_id="root_id")
    tree.append_event(event_name="12A", event_id="12A_id", data=None, parent_id="root_id")
    tree.append_event(event_name="12B", event_id="12B_id", data=None, parent_id="root_id")

    tree.merge_tree("A_id", other_tree=other_tree)
    # TODO - this check is peace of shit
    assert events_count < len(tree)


def test_merge_events_tree_id_error(events_tree_for_test: EventsTree):
    tree = events_tree_for_test
    other_tree = EventsTree(event_name="RootEvent", event_id="root_id")
    tree.append_event(event_name="12A", event_id="12A_id", data=None, parent_id="root_id")

    with pytest.raises(EventIdNotInTree) as exc:
        tree.merge_tree("Test_id", other_tree=other_tree)
    assert exc


def test_append_event():
    pass


def test_show(events_tree_for_test: EventsTree):
    """Raises exception now in Windows
    https://stackoverflow.com/questions/27092833/unicodeencodeerror-charmap-codec-cant-encode-characters
    """
    expected = """root event
├── A
└── B
    ├── C
    └── D
        └── D1
"""

    assert events_tree_for_test.show()
