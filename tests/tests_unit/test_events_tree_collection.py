from th2_data_services import Data

DEMO_CHILD_ID = "88a3ee80-d1b4-11eb-b0fb-199708acc7bc"
DEMO_PARENT_ID = "84db48fc-d1b4-11eb-b0fb-199708acc7bc"


def test_etc_for_detached_events_with_data(demo_etc_with_data, general_data):
    etc = demo_etc_with_data
    assert etc.get_detached_events()  # Detached Events Exist Without Data Source


def test_etc_for_detached_events_without_data(demo_etc):
    assert not demo_etc.get_detached_events()  # Detached Events Don't Exist If No Data


# TODO: How To Assert?
def test_etc_to_get_leaves(demo_etc_with_data):
    etc = demo_etc_with_data
    assert etc.get_leaves()  # == 14 ?


def test_etc_to_get_roots_ids(demo_etc_with_data, general_data):
    etc = demo_etc_with_data
    root_ids = etc.get_roots_ids()
    events_filtered = Data(general_data).filter(lambda event: not event.get("parentEventId"))
    assert root_ids == [event["eventId"] for event in events_filtered]


def test_etc_find_event(demo_etc_with_data, general_data):
    etc = demo_etc_with_data
    event_by_find = etc.find(lambda event: "Aggressive" in event["eventName"])
    event_filtered = Data(general_data).filter(lambda event: "Aggressive" in event["eventName"])
    assert list(event_filtered) == list(event_filtered)


def test_etc_find_events(demo_etc_with_data, general_data):
    etc = demo_etc_with_data
    event_by_find = etc.findall(lambda event: event["batchId"])
    event_filtered = Data(general_data).filter(lambda event: event["batchId"])
    assert list(event_filtered) == list(event_filtered)


def test_etc_find_ancestor(demo_etc_with_data):
    etc = demo_etc_with_data
    ancestor = etc.find_ancestor(DEMO_CHILD_ID, filter=lambda event: not event.get("parentEventId"))
    assert ancestor["eventId"] == DEMO_PARENT_ID


def test_etc_find_children(demo_etc_with_data, general_data):
    etc = demo_etc_with_data
    id_ = DEMO_CHILD_ID
    children = etc.get_children(id_)
    data = Data(general_data).filter(lambda event: event["parentEventId"] == id_)
    assert len(children) == data.len


def test_etc_get_subtree(demo_etc_with_data, general_data):
    etc = demo_etc_with_data
    subtree = etc.get_subtree(DEMO_CHILD_ID)
    assert subtree.get_root_id() == DEMO_CHILD_ID


def test_etc_get_full_path(demo_etc_with_data):
    etc = demo_etc_with_data
    child, ancestor = DEMO_CHILD_ID, DEMO_PARENT_ID
    event_path = etc.get_full_path(child)  # [ancestor_root, ancestor_level1, ..., event]
    assert [event["eventId"] for event in event_path] == [ancestor, child]


def test_etc_get_parent(demo_etc_with_data):
    etc = demo_etc_with_data
    child = DEMO_CHILD_ID
    parent = etc.get_parent(child)
    assert parent["eventId"] == "84db48fc-d1b4-11eb-b0fb-199708acc7bc"


def test_etc_append_stub_event(demo_etc_with_data):
    etc = demo_etc_with_data
    etc.append_event(
        event={
            "eventId": "a20f5ef4-c3fe-bb10-a29c-dd3d784909eb",
            "parentEventId": "8e2524fa-cf59-11eb-a3f7-094f904c3a62",
            "eventName": "StubEvent",
        }
    )
    detached_events = etc.get_detached_events()
    assert [event for event in detached_events if event["eventName"] == "StubEvent"]


def test_etc_append_non_stub_event(demo_etc_with_data):
    etc = demo_etc_with_data
    etc.append_event(
        event={
            "eventId": "a20f5ef4-c3fe-bb10-a29c-dd3d784909eb",
            "parentEventId": DEMO_PARENT_ID,  #
            "eventName": "DemoEvent",
        }
    )
    assert etc.find(lambda event: event["eventName"] == "DemoEvent")
