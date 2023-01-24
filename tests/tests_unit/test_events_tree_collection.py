from th2_data_services import Data
import pytest

DEMO_CHILD_ID = "88a3ee80-d1b4-11eb-b0fb-199708acc7bc"
DEMO_PARENT_ID = "84db48fc-d1b4-11eb-b0fb-199708acc7bc"


def test_etc_for_detached_events_with_data(demo_etc_with_data):
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

    assert demo_etc_with_data.get_detached_events() == expected_detached


def test_etc_for_detached_events_without_data(demo_etc):
    assert not demo_etc.get_detached_events()  # Detached Events Don't Exist If No Data


def test_etc_to_get_roots_ids(demo_etc_with_data, general_data):
    """Check that ETC returns correct root ids."""
    etc = demo_etc_with_data
    root_ids = etc.get_roots_ids()
    root_events_in_data = Data(general_data).filter(lambda event: event["parentEventId"] is None)
    assert root_ids == [event["eventId"] for event in root_events_in_data]


@pytest.mark.skip("TODO - FIX IT")
def test_etc_find_event(demo_etc_with_data, general_data):
    # TODO - issue here.
    etc = demo_etc_with_data
    event_by_find = etc.find(lambda event: "Aggressive" in event["eventName"])
    event_filtered = Data(general_data).filter(lambda event: "Aggressive" in event["eventName"])
    assert list(event_filtered) == list(event_by_find)


@pytest.mark.skip("TODO - FIX IT")
def test_etc_find_events(demo_etc_with_data, general_data):
    # TODO - issue here.
    etc = demo_etc_with_data
    event_by_find = etc.findall(lambda event: event["batchId"])
    event_filtered = Data(general_data).filter(lambda event: event["batchId"])
    assert list(event_filtered) == list(event_by_find)


def test_etc_find_ancestor(demo_etc_with_data):
    etc = demo_etc_with_data
    ancestor = etc.find_ancestor(DEMO_CHILD_ID, filter=lambda event: not event.get("parentEventId"))
    assert ancestor["eventId"] == DEMO_PARENT_ID


# TODO - add
def test_etc_get_ancestors():
    pass


def test_etc_get_children(demo_etc_with_data, general_data):
    etc = demo_etc_with_data
    id_ = DEMO_CHILD_ID
    children = etc.get_children(id_)
    data = Data(general_data).filter(lambda event: event["parentEventId"] == id_)
    assert list(children) == list(data)


def test_etc_get_full_path(demo_etc_with_data):
    etc = demo_etc_with_data
    child, ancestor = DEMO_CHILD_ID, DEMO_PARENT_ID
    event_path = etc.get_full_path(child)  # [ancestor_root, ancestor_level1, ..., event]
    assert [event["eventId"] for event in event_path] == [ancestor, child]


def test_etc_get_parent(demo_etc_with_data):
    etc = demo_etc_with_data
    parent = etc.get_parent(DEMO_CHILD_ID)
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


@pytest.mark.skip("TODO - FIX IT")
def test_etc_get_all_events(demo_etc_with_data, general_data):
    # TODO - I changed it a little bit, it's failing now, check please. Was I wrong?
    etc = demo_etc_with_data
    data = Data(general_data)
    events = etc.get_all_events()
    assert events == list(data)


@pytest.mark.skip("TODO - FIX IT")
def test_get_parentless_trees(demo_etc_with_data, general_data):
    """Check that ETC returns parentless_tress."""
    etc = demo_etc_with_data
    parentless_tress = etc.get_parentless_trees()
    # TODO - check that ETC returns them
    assert False


# TODO - add big set of tests after user used `get_parentless_trees`
#   I prefer to create separate file for big set of tests.
#   Like for test_data/test_cache -- there are only cache tests and all methods with cache.

# TODO - check that ETC returns correct values for
#  - get_roots_ids
#  - get_trees
#  - get_root_by_id
#  - get_tree_by_id
#   ....
