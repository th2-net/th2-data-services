from th2_data_services import Data

DEMO_CHILD_ID = "88a3ee80-d1b4-11eb-b0fb-199708acc7bc"
DEMO_PARENT_ID = "84db48fc-d1b4-11eb-b0fb-199708acc7bc"


def test_petc_for_detached_events_with_data(demo_petc_with_general_data):
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
    assert demo_petc_with_general_data.get_detached_events() == expected_detached


def test_petc_to_get_roots_ids(demo_petc_with_general_data, general_data):
    petc = demo_petc_with_general_data
    root_ids = petc.get_roots_ids()
    events_filtered = Data(general_data).filter(lambda event: not event.get("parentEventId"))
    assert root_ids == [event["eventId"] for event in events_filtered]


def test_petc_to_get_roots_ids_with_multiple_trees(demo_petc):
    """Check that ETC returns correct root ids."""
    petc = demo_petc
    root_ids = petc.get_roots_ids()
    assert all(["root_id" in root_id for root_id in root_ids])


def test_petc_find_event(demo_petc_with_general_data, general_data):
    petc = demo_petc_with_general_data
    event_by_find = petc.find(lambda event: "Aggressive" in event["eventName"])
    event_filtered = Data(general_data).filter(lambda event: "Aggressive" in event["eventName"])
    assert list(event_filtered) == list(event_filtered)


def test_petc_find_events(demo_petc_with_general_data, general_data):
    petc = demo_petc_with_general_data
    event_by_find = petc.findall(lambda event: event["batchId"])
    event_filtered = Data(general_data).filter(lambda event: event["batchId"])
    assert list(event_filtered) == list(event_filtered)


def test_petc_find_ancestor(demo_petc_with_general_data):
    petc = demo_petc_with_general_data
    ancestor = petc.find_ancestor(DEMO_CHILD_ID, filter=lambda event: not event.get("parentEventId"))
    assert ancestor["eventId"] == DEMO_PARENT_ID


def test_petc_get_children(demo_petc_with_general_data, general_data):
    petc = demo_petc_with_general_data
    id_ = DEMO_CHILD_ID
    children = petc.get_children(id_)
    data = Data(general_data).filter(lambda event: event["parentEventId"] == id_)
    data = [event for event in data if petc.find(lambda ev: ev["parentEventId"] == event["eventId"])]
    assert list(children) == data


def test_petc_get_full_path(demo_petc_with_general_data):
    petc = demo_petc_with_general_data
    child, ancestor = DEMO_CHILD_ID, DEMO_PARENT_ID
    event_path = petc.get_full_path(child)  # [ancestor_root, ancestor_level1, ..., event]
    assert [event["eventId"] for event in event_path] == [ancestor, child]


#
def test_petc_get_parent(demo_petc_with_general_data):
    petc = demo_petc_with_general_data
    parent = petc.get_parent(DEMO_CHILD_ID)
    assert parent["eventId"] == "84db48fc-d1b4-11eb-b0fb-199708acc7bc"


def test_petc_append_stub_event(demo_petc_with_general_data):
    petc = demo_petc_with_general_data
    petc.append_event(
        event=(
            stub_event := {
                "eventId": "a20f5ef4-c3fe-bb10-a29c-dd3d784909eb",
                "parentEventId": "8e2524fa-cf59-11eb-a3f7-094f904c3a62",
                "eventName": "CustomStubEvent",
            }
        )
    )
    filter_for_stub_event = [event for event in petc.get_all_events_iter() if event["eventName"] == "CustomStubEvent"]
    assert len(filter_for_stub_event) == 1
    assert filter_for_stub_event[0] == stub_event


def test_petc_append_non_stub_event(demo_petc_with_general_data):
    petc = demo_petc_with_general_data
    petc.append_event(
        event=(
            demo_event := {
                "eventId": "a20f5ef4-c3fe-bb10-a29c-dd3d784909eb",
                "parentEventId": DEMO_PARENT_ID,  #
                "eventName": "DemoEvent",
            }
        )
    )
    event = petc.find(lambda event_: event_["eventName"] == "DemoEvent")
    assert event == demo_event


def test_petc_get_trees(demo_petc):
    petc = demo_petc
    trees = petc.get_trees()
    assert all(["root_id" in tree.get_root_id() for tree in trees])


def test_petc_get_root_by_id(demo_petc):
    petc = demo_petc
    root = petc.get_root_by_id("root_id2")
    expected_root = {"eventName": "Root Event 2", "eventId": "root_id2", "data": {"data": [6, 7, 8, 9, 10]}}
    assert root == expected_root


def test_petc_get_tree_by_id(demo_petc):
    petc = demo_petc
    tree = petc.get_tree_by_id("b2_id")
    expected_tree = petc.get_trees()[1]
    assert tree == expected_tree
