from th2_data_services import Data

DEMO_CHILD_ID = "88a3ee80-d1b4-11eb-b0fb-199708acc7bc"
DEMO_PARENT_ID = "84db48fc-d1b4-11eb-b0fb-199708acc7bc"


def test_petc_for_detached_events_with_data(demo_petc_with_data):
    assert demo_petc_with_data.get_detached_events()  # Detached Events Exist Without Data Source


def test_petc_for_detached_events_without_data(demo_petc):
    assert not demo_petc.get_detached_events()  # No Detached Events Without Data


def test_petc_to_get_roots_ids(demo_petc_with_data, general_data):
    petc = demo_petc_with_data
    root_ids = petc.get_roots_ids()
    events_filtered = Data(general_data).filter(lambda event: not event.get("parentEventId"))
    assert root_ids == [event["eventId"] for event in events_filtered]


def test_petc_find_event(demo_petc_with_data, general_data):
    petc = demo_petc_with_data
    event_by_find = petc.find(lambda event: "Aggressive" in event["eventName"])
    event_filtered = Data(general_data).filter(lambda event: "Aggressive" in event["eventName"])
    assert list(event_filtered) == list(event_filtered)


def test_petc_find_events(demo_petc_with_data, general_data):
    petc = demo_petc_with_data
    event_by_find = petc.findall(lambda event: event["batchId"])
    event_filtered = Data(general_data).filter(lambda event: event["batchId"])
    assert list(event_filtered) == list(event_filtered)


def test_petc_find_ancestor(demo_petc_with_data):
    petc = demo_petc_with_data
    ancestor = petc.find_ancestor(DEMO_CHILD_ID, filter=lambda event: not event.get("parentEventId"))
    assert ancestor["eventId"] == DEMO_PARENT_ID


def test_petc_find_children(demo_petc_with_data, general_data):
    petc = demo_petc_with_data
    id_ = DEMO_CHILD_ID
    children = petc.get_children(id_)
    data = Data(general_data).filter(lambda event: event["parentEventId"] == id_)
    data = [event for event in data if petc.find(lambda ev: ev["parentEventId"] == event["eventId"])]
    assert list(children) == data


def test_petc_get_full_path(demo_petc_with_data):
    petc = demo_petc_with_data
    child, ancestor = DEMO_CHILD_ID, DEMO_PARENT_ID
    event_path = petc.get_full_path(child)  # [ancestor_root, ancestor_level1, ..., event]
    assert [event["eventId"] for event in event_path] == [ancestor, child]


#
def test_petc_get_parent(demo_petc_with_data):
    petc = demo_petc_with_data
    parent = petc.get_parent(DEMO_CHILD_ID)
    assert parent["eventId"] == "84db48fc-d1b4-11eb-b0fb-199708acc7bc"


def test_petc_append_stub_event(demo_petc_with_data):
    petc = demo_petc_with_data
    petc.append_event(
        event={
            "eventId": "a20f5ef4-c3fe-bb10-a29c-dd3d784909eb",
            "parentEventId": "8e2524fa-cf59-11eb-a3f7-094f904c3a62",
            "eventName": "StubEvent",
        }
    )
    detached_events = petc.get_detached_events()
    assert [event for event in detached_events if event["eventName"] == "StubEvent"]


def test_petc_append_non_stub_event(demo_petc_with_data):
    petc = demo_petc_with_data
    petc.append_event(
        event={
            "eventId": "a20f5ef4-c3fe-bb10-a29c-dd3d784909eb",
            "parentEventId": DEMO_PARENT_ID,  #
            "eventName": "DemoEvent",
        }
    )
    assert petc.find(lambda event: event["eventName"] == "DemoEvent")
