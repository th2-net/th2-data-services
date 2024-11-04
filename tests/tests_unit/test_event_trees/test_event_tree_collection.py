from tests.tests_unit.test_event_trees.demo_etc_data import demo_etc_data_small
from th2_data_services.data import Data

EXPECTED_STUB = {
    "attachedMessageIds": [],
    "batchId": "Broken_Event",
    "endTimestamp": {"nano": 0, "epochSecond": 0},
    "startTimestamp": {"nano": 0, "epochSecond": 0},
    "eventId": "Unknown",
    "eventName": "Broken_Event",
    "eventType": "Broken_Event",
    "parentEventId": "Broken_Event",
    "successful": None,
    "isBatched": None,
}


def test_etc_for_detached_events_with_data(demo_etc, all_test=False):
    """Checks that ETC returns its detached events."""
    detached_events = demo_etc.get_detached_events()
    if all_test:
        assert (
            detached_events == []
        )  # After get_parentless_trees Detached Events Become Root Events
    else:
        assert detached_events == [
            {
                "eventName": "Root Event 4",
                "eventId": "root_id4",
                "data": {"data": [13, 14]},
                "parentEventId": "Unknown",
            }
        ]


def test_etc_to_get_roots_ids(demo_etc_with_general_data, general_data):
    """Check that ETC returns correct root ids."""
    etc = demo_etc_with_general_data
    root_ids = etc.get_roots_ids()
    root_events_in_data = Data(general_data).filter(lambda event: event["parentEventId"] is None)
    assert root_ids == [event["eventId"] for event in root_events_in_data]


def test_etc_to_get_roots_ids_with_multiple_trees(demo_etc):
    """Check that ETC returns correct root ids."""
    etc = demo_etc
    root_ids = etc.get_roots_ids()
    assert all(["root_id" in root_id or "Unknown" in root_id for root_id in root_ids])


def test_etc_find_event(demo_etc, all_test=False):
    etc = demo_etc
    if all_test:
        event_by_find = etc.find(lambda event: event["eventName"] == "Root Event 4")
        expected_event = {
            "eventName": "Root Event 4",
            "eventId": "root_id4",
            "data": {"data": [13, 14]},
            "parentEventId": "Unknown",
        }
        assert event_by_find == expected_event
    else:
        event_by_find = etc.find(lambda event: event["eventName"] == "Event E2_child3")
        expected_event = {
            "eventName": "Event E2_child3",
            "eventId": "e2_child3_id",
            "data": {"data": "E2_child3"},
            "parentEventId": "e2_id",
        }
        assert event_by_find == expected_event


def test_etc_find_events(demo_etc, all_test=False):
    etc = demo_etc
    if all_test:
        event_by_find = etc.findall(lambda event: "Root Event" in event["eventName"])
        expected_events = [
            {"eventName": "Root Event", "eventId": "root_id", "data": {"data": [1, 2, 3, 4, 5]}},
            {
                "eventName": "Root Event 2",
                "eventId": "root_id2",
                "data": {"data": [6, 7, 8, 9, 10]},
            },
            {"eventName": "Root Event 3", "eventId": "root_id3", "data": {"data": [11, 12]}},
            {
                "eventName": "Root Event 4",
                "eventId": "root_id4",
                "data": {"data": [13, 14]},
                "parentEventId": "Unknown",
            },
        ]
        assert event_by_find == expected_events
    else:
        event_by_find = etc.findall(lambda event: "E2_child" in event["eventName"])
        expected_events = [
            {
                "eventName": "Event E2_child1",
                "eventId": "e2_child1_id",
                "data": {"data": "E2_child1"},
                "parentEventId": "e2_id",
            },
            {
                "eventName": "Event E2_child2",
                "eventId": "e2_child2_id",
                "data": {"data": "E2_child2"},
                "parentEventId": "e2_id",
            },
            {
                "eventName": "Event E2_child3",
                "eventId": "e2_child3_id",
                "data": {"data": "E2_child3"},
                "parentEventId": "e2_id",
            },
        ]
        assert event_by_find == expected_events


def test_etc_find_ancestor(demo_etc, all_test=False):
    etc = demo_etc
    if all_test:
        ancestor = etc.find_ancestor(
            "root_id4", filter=lambda event: event.get("parentEventId") == "Broken_Event"
        )
        expected_event = EXPECTED_STUB
        assert ancestor == expected_event
    else:
        ancestor = etc.find_ancestor(
            "e2_child1_id", filter=lambda event: not event.get("parentEventId")
        )
        expected_event = {
            "eventName": "Root Event 2",
            "eventId": "root_id2",
            "data": {"data": [6, 7, 8, 9, 10]},
        }
        assert ancestor == expected_event


def test_etc_get_ancestors(demo_etc, all_test=False):
    etc = demo_etc
    if all_test:
        ancestors = etc.get_ancestors("root_id4")
        assert [ancestor["eventId"] for ancestor in ancestors] == ["Unknown"]
    else:
        ancestors = etc.get_ancestors("b2_child1_id")
        assert [ancestor["eventId"] for ancestor in ancestors] == ["root_id2", "b2_id"]


def test_etc_get_children(demo_etc, all_test=False):
    etc = demo_etc
    if all_test:
        id_ = "Unknown"
        children = etc.get_children(id_)
        expected_children = (
            {
                "eventName": "Root Event 4",
                "eventId": "root_id4",
                "data": {"data": [13, 14]},
                "parentEventId": "Unknown",
            },
        )
        assert children == expected_children
    else:
        id_ = "a1_id"
        children = etc.get_children(id_)
        expected_children = (
            {
                "eventName": "Event A1_child1",
                "eventId": "a1_child1_id",
                "data": {"data": "A1_child1"},
                "parentEventId": "a1_id",
            },
            {
                "eventName": "Event A1_child2",
                "eventId": "a1_child2_id",
                "data": {"data": "A1_child2"},
                "parentEventId": "a1_id",
            },
        )
        assert children == expected_children


def test_etc_get_full_path(demo_etc, all_test=False):
    etc = demo_etc
    if all_test:
        child, ancestor = "root_id4", "Unknown"
        event_path = etc.get_full_path(child)
        assert [event["eventId"] for event in event_path] == [ancestor, child]
    else:
        expected_path = ["root_id", "c1_id", "d1_id", "e1_child1_id"]
        event_path = etc.get_full_path("e1_child1_id")
        assert [event["eventId"] for event in event_path] == expected_path


def test_etc_get_parent(demo_etc, all_test=False):
    etc = demo_etc
    if all_test:
        parent = etc.get_parent("root_id4")
        assert parent == EXPECTED_STUB
    else:
        parent = etc.get_parent("a1_child1_id")
        assert parent["eventId"] == "a1_id"


def test_etc_append_stub_event(demo_etc_with_general_data):
    etc = demo_etc_with_general_data
    stub_event = {
        "eventId": "a20f5ef4-c3fe-bb10-a29c-dd3d784909eb",
        "parentEventId": "8e2524fa-cf59-11eb-a3f7-094f904c3a62",
        "eventName": "CustomStubEvent",
    }
    etc.append_event(event=stub_event)
    filter_for_stub_event = [
        event for event in etc.get_all_events_iter() if event["eventName"] == "CustomStubEvent"
    ]
    assert len(filter_for_stub_event) == 1
    assert filter_for_stub_event[0] == stub_event


def test_etc_append_non_stub_event(demo_etc_with_general_data):
    etc = demo_etc_with_general_data
    demo_event = {
        "eventId": "a20f5ef4-c3fe-bb10-a29c-dd3d784909eb",
        "parentEventId": "84db48fc-d1b4-11eb-b0fb-199708acc7bc",  # NonStub Parent Event
        "eventName": "DemoEvent",
    }

    etc.append_event(event=demo_event)
    event = etc.find(lambda event_: event_["eventName"] == "DemoEvent")
    assert event == demo_event


def test_etc_get_all_events(demo_etc, all_test=False):
    etc = demo_etc
    data = sorted(demo_etc_data_small, key=lambda event: event["eventId"])
    events = sorted(etc.get_all_events(), key=lambda event: event["eventId"])
    if not all_test:
        events.extend(etc.get_detached_events())
        data.extend(
            [
                {
                    "eventName": "Root Event 4",
                    "eventId": "root_id4",
                    "data": {"data": [13, 14]},
                    "parentEventId": "Unknown",
                }
            ]
        )
        assert events == data
    else:
        data.insert(0, EXPECTED_STUB)
        assert events == data


def test_get_parentless_trees(demo_etc):
    etc = demo_etc
    parentless_trees = etc.get_parentless_trees()
    expected_parentless_tree = [
        EXPECTED_STUB,
        {
            "eventName": "Root Event 4",
            "eventId": "root_id4",
            "data": {"data": [13, 14]},
            "parentEventId": "Unknown",
        },
    ]
    assert len(parentless_trees) == 1
    assert parentless_trees[0].get_all_events() == expected_parentless_tree


def test_etc_get_trees(demo_etc):
    etc = demo_etc
    trees = etc.get_trees()
    root_ids = [tree.get_root_id() for tree in trees]
    assert all(["root_id" in root_id or "Unknown" in root_id for root_id in root_ids])


def test_etc_get_root_by_id(demo_etc, all_test=False):
    etc = demo_etc
    if all_test:
        root = etc.get_root_by_id("Unknown")
        expected_root = EXPECTED_STUB
        assert root == expected_root
    else:
        root = etc.get_root_by_id("root_id")
        expected_root = {
            "eventName": "Root Event",
            "eventId": "root_id",
            "data": {"data": [1, 2, 3, 4, 5]},
        }
        assert root == expected_root


def test_etc_get_tree_by_id(demo_etc, all_test=False):
    etc = demo_etc
    if all_test:
        tree = etc.get_tree_by_id("Unknown")
        expected_tree = etc.get_trees()[-1]
        assert tree == expected_tree
    else:
        tree = etc.get_tree_by_id("b1_child2_id")
        expected_tree = etc.get_trees()[0]
        assert tree == expected_tree


def test_all_after_get_parentless_trees(demo_etc):
    test_get_parentless_trees(demo_etc)

    test_etc_get_all_events(demo_etc, True)
    test_etc_get_trees(demo_etc)
    test_etc_get_ancestors(demo_etc, True)
    test_etc_get_children(demo_etc, True)
    test_etc_get_full_path(demo_etc, True)
    test_etc_get_parent(demo_etc, True)
    test_etc_get_root_by_id(demo_etc, True)
    test_etc_get_tree_by_id(demo_etc, True)
    test_etc_to_get_roots_ids_with_multiple_trees(demo_etc)
    test_etc_for_detached_events_with_data(demo_etc, True)
    test_etc_find_event(demo_etc, True)
    test_etc_find_events(demo_etc, True)
    test_etc_find_ancestor(demo_etc, True)


def test_findall_max_count(demo_etc_big):
    """https://exactpro.atlassian.net/browse/TH2-4711 - issue related test.
    these tests will fail when ETC will have More than 1 tree
    and max_count > than number of events that were found in the first tree.
    """
    etc = demo_etc_big
    max_nodes_to_get = 10
    expected_nodes = [
        {
            "eventName": "Event A0",
            "eventId": "A0_id",
            "data": {"data": [89, 98, 58]},
            "parentEventId": "root_id0",
        },
        {
            "eventName": "Event A1",
            "eventId": "A1_id",
            "data": {"data": [40, 40, 61]},
            "parentEventId": "root_id0",
        },
        {
            "eventName": "Event A1_child0",
            "eventId": "A1_child0_id",
            "data": {"data": [9, 90, 81]},
            "parentEventId": "A1_id",
        },
        {
            "eventName": "Event A1_child1",
            "eventId": "A1_child1_id",
            "data": {"data": [100, 67, 21]},
            "parentEventId": "A1_id",
        },
        {
            "eventName": "Event A1_child2",
            "eventId": "A1_child2_id",
            "data": {"data": [77, 83, 55]},
            "parentEventId": "A1_id",
        },
        {
            "eventName": "Event A2",
            "eventId": "A2_id",
            "data": {"data": [33, 60, 15]},
            "parentEventId": "root_id0",
        },
        {
            "eventName": "Event A2_child0",
            "eventId": "A2_child0_id",
            "data": {"data": [14, 13, 66]},
            "parentEventId": "A2_id",
        },
        {
            "eventName": "Event A3",
            "eventId": "A3_id",
            "data": {"data": [19, 1, 17]},
            "parentEventId": "root_id0",
        },
        {
            "eventName": "Event A3_child0",
            "eventId": "A3_child0_id",
            "data": {"data": [59, 37, 57]},
            "parentEventId": "A3_id",
        },
        {
            "eventName": "Event A3_child1",
            "eventId": "A3_child1_id",
            "data": {"data": [96, 94, 99]},
            "parentEventId": "A3_id",
        },
    ]
    findall_nodes = etc.findall(filter=lambda e: e.get("parentEventId"), max_count=max_nodes_to_get)
    assert len(findall_nodes) == max_nodes_to_get
    assert expected_nodes == findall_nodes


def test_findall_iter_max_count(demo_etc_big):
    etc = demo_etc_big
    one_value_from_findall = list(
        etc.findall_iter(filter=lambda e: e.get("parentEventId") is not None, max_count=1)
    )
    assert [
        {
            "eventName": "Event A0",
            "eventId": "A0_id",
            "data": {"data": [89, 98, 58]},
            "parentEventId": "root_id0",
        }
    ] == one_value_from_findall
