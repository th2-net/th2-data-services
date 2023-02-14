from copy import deepcopy

import pytest

from th2.data_services.event_tree import CommonEventTree
from th2.data_services.event_tree.exceptions import EventIdNotInTree, TreeLoop


def test_getitem(events_tree_for_test: CommonEventTree):
    tree = events_tree_for_test
    assert tree["D1_id"] == {"key1": "value1", "key2": "value2"} and tree["C_id"] == {"data": "test data"}


def test_getitem_id_error(events_tree_for_test: CommonEventTree):
    with pytest.raises(EventIdNotInTree) as exc:
        _ = events_tree_for_test["test"]
    assert exc


def test_setitem(events_tree_for_test: CommonEventTree):
    tree = events_tree_for_test
    tree["A_id"] = {"new data": 123}
    assert tree["A_id"] == {"new data": 123}


def test_setitem_id_error(events_tree_for_test: CommonEventTree):
    with pytest.raises(EventIdNotInTree) as exc:
        events_tree_for_test["test"] = "test"
    assert exc


def test_update_parent_link(events_tree_for_test: CommonEventTree):
    tree = events_tree_for_test
    tree.update_parent_link("D1_id", "root_id")
    assert tree.get_parent("D1_id") == {"data": [1, 2, 3, 4, 5]}


def test_update_parent_link_id_error(events_tree_for_test: CommonEventTree):
    with pytest.raises(EventIdNotInTree) as exc:
        events_tree_for_test.update_parent_link("test", "to_test")
    assert exc


def test_update_parent_link_loop_error(events_tree_for_test: CommonEventTree):
    with pytest.raises(TreeLoop) as exc:
        tree = events_tree_for_test
        tree.update_parent_link("B_id", "C_id")
    assert exc


def test_update_event_name(events_tree_for_test: CommonEventTree):
    tree = events_tree_for_test
    tree.update_event_name("C_id", "NewEvent")
    assert tree._tree["C_id"].tag == "NewEvent"


def test_update_event_name_id_error(events_tree_for_test: CommonEventTree):
    with pytest.raises(EventIdNotInTree) as exc:
        events_tree_for_test.update_event_name("test", "test_name")
    assert exc


def test_merge_events_tree(events_tree_for_test: CommonEventTree):
    tree = deepcopy(events_tree_for_test)

    other_tree_root = dict(event_name="RootEvent", event_id="root_id")
    other_tree_nodes = [
        dict(event_name="12A", event_id="12A_id", data={"A": 65}, parent_id="root_id"),
        dict(event_name="12B", event_id="12B_id", data={"B": 66}, parent_id="root_id"),
    ]
    other_tree = CommonEventTree(**other_tree_root)
    other_tree.append_event(**other_tree_nodes[0])
    other_tree.append_event(**other_tree_nodes[1])

    tree.merge_tree("A_id", other_tree=other_tree)

    merged_tree_events = tree.get_all_events()
    expected_events = events_tree_for_test.get_all_events() + [event["data"] for event in other_tree_nodes]
    assert merged_tree_events == expected_events


def test_merge_events_tree_id_error(events_tree_for_test: CommonEventTree):
    tree = events_tree_for_test
    other_tree = CommonEventTree(event_name="RootEvent", event_id="root_id")
    tree.append_event(event_name="12A", event_id="12A_id", data=None, parent_id="root_id")

    with pytest.raises(EventIdNotInTree) as exc:
        tree.merge_tree("Test_id", other_tree=other_tree)
    assert exc


def test_append_event(events_tree_for_test):
    tree = events_tree_for_test
    node = {
        "event_name": "0xA",
        "event_id": "0xA_id",
        "data": {"msg": "Event Has Been Created"},
        "parent_id": "root_id",
    }
    tree.append_event(**node)
    assert tree.get_event("0xA_id") == node["data"]


@pytest.mark.xfail(reason="Raises exception now in Windows")
def test_show(events_tree_for_test: CommonEventTree):
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
