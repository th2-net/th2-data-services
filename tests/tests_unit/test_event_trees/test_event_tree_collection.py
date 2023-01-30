from th2_data_services import Data

DEMO_CHILD_ID = "88a3ee80-d1b4-11eb-b0fb-199708acc7bc"
DEMO_PARENT_ID = "84db48fc-d1b4-11eb-b0fb-199708acc7bc"


def test_etc_for_detached_events_with_data(demo_etc_with_general_data):
    """Checks that ETC returns its detached events."""
    expected_detached = [
        {
            "batchId": "654c2724-5202-460b-8e6c-a7ee9fb02ddf",
            "eventId": "654c2724-5202-460b-8e6c-a7ee9fb02ddf:8ca20288-d1b4-11eb-986f-1e8d42132387",
            "eventName": "Remove 'NewOrderSingle' id='demo-conn1:SECOND:1624005455622135205' Hash='7009491514226292581' Group='NOS_CONN' Hash['SecondaryClOrdID': 11111, 'SecurityID': INSTR1]",
            "isBatched": True,
            "eventType": "",
            "parentEventId": "a3779b94-d051-11eb-986f-1e8d42132387",
        },
        {
            "batchId": None,
            "eventId": "8ceb47f6-d1b4-11eb-a9ed-ffb57363e013",
            "eventName": "Send 'ExecutionReport' message",
            "isBatched": False,
            "eventType": "Send message",
            "parentEventId": "845d70d2-9c68-11eb-8598-691ebd7f413d",
        },
        {
            "batchId": None,
            "eventId": "8ced1c93-d1b4-11eb-a9f4-b12655548efc",
            "eventName": "Send 'ExecutionReport' message",
            "isBatched": False,
            "eventType": "Send message",
            "parentEventId": "845d70d2-9c68-11eb-8598-691ebd7f413d",
        },
    ]

    assert demo_etc_with_general_data.get_detached_events() == expected_detached


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
    assert all(["root_id" in root_id for root_id in root_ids])


def test_etc_find_event(demo_etc_with_general_data, general_data):
    etc = demo_etc_with_general_data
    event_by_find = etc.find(lambda event: "Aggressive" in event["eventName"])
    event_filtered = list(filter(lambda event: "Aggressive" in event["eventName"], general_data))[0]
    assert event_filtered == event_by_find


def test_etc_find_events(demo_etc_with_general_data, general_data):
    etc = demo_etc_with_general_data
    event_by_find = etc.findall(lambda event: event["batchId"])
    event_filtered = list(filter(lambda event: event["batchId"] and event["eventType"], general_data))
    assert event_filtered == event_by_find


def test_etc_find_ancestor(demo_etc_with_general_data):
    etc = demo_etc_with_general_data
    ancestor = etc.find_ancestor(DEMO_CHILD_ID, filter=lambda event: not event.get("parentEventId"))
    assert ancestor["eventId"] == DEMO_PARENT_ID


def test_etc_get_ancestors(demo_etc_with_general_data):
    etc = demo_etc_with_general_data
    ancestor = etc.find_ancestor(DEMO_CHILD_ID, filter=lambda event: not event.get("parentEventId"))
    assert ancestor["eventId"] == DEMO_PARENT_ID


def test_etc_get_children(demo_etc_with_general_data, general_data):
    etc = demo_etc_with_general_data
    id_ = DEMO_CHILD_ID
    children = etc.get_children(id_)
    data = filter(lambda event: event["parentEventId"] == id_, general_data)
    assert children == tuple(data)


def test_etc_get_full_path(demo_etc_with_general_data):
    etc = demo_etc_with_general_data
    child, ancestor = DEMO_CHILD_ID, DEMO_PARENT_ID
    event_path = etc.get_full_path(child)  # [ancestor_root, ancestor_level1, ..., event]
    assert [event["eventId"] for event in event_path] == [ancestor, child]


def test_etc_get_parent(demo_etc_with_general_data):
    etc = demo_etc_with_general_data
    parent = etc.get_parent(DEMO_CHILD_ID)
    assert parent["eventId"] == "84db48fc-d1b4-11eb-b0fb-199708acc7bc"


def test_etc_append_stub_event(demo_etc_with_general_data):
    etc = demo_etc_with_general_data
    stub_event = {
        "eventId": "a20f5ef4-c3fe-bb10-a29c-dd3d784909eb",
        "parentEventId": "8e2524fa-cf59-11eb-a3f7-094f904c3a62",
        "eventName": "CustomStubEvent",
    }
    etc.append_event(event=stub_event)
    filter_for_stub_event = [event for event in etc.get_all_events_iter() if event["eventName"] == "CustomStubEvent"]
    assert len(filter_for_stub_event) == 1
    assert filter_for_stub_event[0] == stub_event


def test_etc_append_non_stub_event(demo_etc_with_general_data):
    etc = demo_etc_with_general_data
    demo_event = {
        "eventId": "a20f5ef4-c3fe-bb10-a29c-dd3d784909eb",
        "parentEventId": DEMO_PARENT_ID,  #
        "eventName": "DemoEvent",
    }
    etc.append_event(event=demo_event)
    event = etc.find(lambda event_: event_["eventName"] == "DemoEvent")
    assert event == demo_event


def test_etc_get_all_events(demo_etc_with_general_data, general_data):
    etc = demo_etc_with_general_data
    data = sorted(general_data, key=lambda event: event["eventId"])
    events = sorted(etc.get_all_events(), key=lambda event: event["eventId"])
    assert events == data


def test_get_parentless_trees(demo_etc):
    etc = demo_etc
    parentless_trees = etc.get_parentless_trees()
    expected_parentless_tree = [
        {
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
        },
        {"eventName": "Root Event 4", "eventId": "root_id4", "data": {"data": [13, 14]}, "parentEventId": "Unknown"},
    ]
    assert len(parentless_trees) == 1
    assert parentless_trees[0].get_all_events() == expected_parentless_tree


def test_etc_get_trees(demo_etc):
    etc = demo_etc
    trees = etc.get_trees()
    assert all(["root_id" in tree.get_root_id() for tree in trees])


def test_etc_get_root_by_id(demo_etc):
    etc = demo_etc
    root = etc.get_root_by_id("root_id")
    expected_root = {"eventName": "Root Event", "eventId": "root_id", "data": {"data": [1, 2, 3, 4, 5]}}
    assert root == expected_root


def test_etc_get_tree_by_id(demo_etc):
    etc = demo_etc
    tree = etc.get_tree_by_id("b1_child2_id")
    expected_tree = etc.get_trees()[0]
    assert tree == expected_tree


# TODO - add big set of tests after user used `get_parentless_trees`
#   I prefer to create separate file for big set of tests.
#   Like for test_data/test_cache -- there are only cache tests and all methods with cache.
