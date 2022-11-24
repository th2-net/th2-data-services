from typing import List, Generator
import warnings
import pytest
from th2_data_services.events_tree.exceptions import EventIdNotInTree
from th2_data_services.provider.v5.events_tree.events_tree_collection import EventsTreeCollectionProvider5


def test_get_parentless_trees():
    """It checks that parentless trees were created, added to roots and detached events removed."""
    # TODO


def test_len_trees(general_data: List[dict]):
    etc = EventsTreeCollectionProvider5(general_data)
    assert etc.len_trees == 18


def test_len_detached_events(general_data: List[dict]):
    etc = EventsTreeCollectionProvider5(general_data)
    assert etc.len_detached_events == 3


def test_len(general_data: List[dict]):
    """Total events in whole collection."""
    etc = EventsTreeCollectionProvider5(general_data)
    assert len(etc) == len(general_data)


def test_filter_all(general_data: List[dict]):
    collection = EventsTreeCollectionProvider5(general_data)

    assert len(collection.findall(lambda event: "Checkpoint" in event["eventName"])) == 11


def test_filter_all_max_count(general_data: List[dict]):
    collection = EventsTreeCollectionProvider5(general_data)

    assert len(collection.findall(lambda event: "Checkpoint" in event["eventName"], max_count=5)) == 5


def test_filter_stop_function(general_data: List[dict]):
    collection = EventsTreeCollectionProvider5(general_data)

    assert (
        len(
            collection.findall(
                lambda event: "Checkpoint" in event["eventName"],
                stop=lambda event: "th2-hand-demo" in event["eventName"],
            )
        )
        == 1
    )


def test_filter_one(general_data: List[dict]):
    collection = EventsTreeCollectionProvider5(general_data)

    assert collection.find(lambda event: "Checkpoint" in event["eventName"]) == {
        "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
        "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        "eventName": "Checkpoint",
        "eventType": "Checkpoint",
        "isBatched": True,
        "parentEventId": "8bc787fe-d1b4-11eb-bae5-57b0c4472880",
    }


def test_filter_stop(general_data: List[dict]):
    collection = EventsTreeCollectionProvider5(general_data)

    assert not collection.find(
        lambda event: "Checkpoint" in event["eventName"],
        stop=lambda event: "Checkpoint" in event["eventType"],
    )


def test_subtree(general_data: List[dict]):
    collection = EventsTreeCollectionProvider5(general_data)

    assert (
        len(collection.get_subtree("6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e")) == 11
    )


def test_get_roots_ids_with_parentless(parentless_data: List[dict]):
    etc = EventsTreeCollectionProvider5(parentless_data)
    assert etc.get_roots_ids() == ["a", "x"]
    etc.get_parentless_trees()
    assert etc.get_roots_ids() == ["a", "x", "e"]


def test_get_trees_with_parentless(parentless_data: List[dict]):
    etc = EventsTreeCollectionProvider5(parentless_data)
    full_fledged_trees = etc.get_trees()
    parentless_trees = etc.get_parentless_trees()
    assert etc.get_trees() == full_fledged_trees + parentless_trees


def test_get_root_by_id_with_parentless(parentless_data: List[dict]):
    etc = EventsTreeCollectionProvider5(parentless_data)
    assert etc.get_root_by_id("b") == {"type": "event", "eventId": "a", "eventName": "a", "parentEventId": None}
    etc.get_parentless_trees()
    assert etc.get_root_by_id("d") == etc._build_stub_event("e")

    with pytest.raises(EventIdNotInTree):
        etc.get_root_by_id("EventIdNotInTree")


def test_get_tree_by_id_with_parentless(parentless_data: List[dict]):
    etc = EventsTreeCollectionProvider5(parentless_data)
    parentless_trees = etc.get_parentless_trees()[0]
    assert etc.get_tree_by_id("d") == parentless_trees

    with pytest.raises(EventIdNotInTree):
        etc.get_tree_by_id("EventIdNotInTree")


def test_len_with_parentless(parentless_data: List[dict]):
    etc = EventsTreeCollectionProvider5(parentless_data)
    assert etc.len_trees == 6 and etc.len_detached_events == 2 and etc.len_parentless == 0
    etc.get_parentless_trees()
    assert etc.len_trees == 9 and etc.len_detached_events == 0 and etc.len_parentless == 3


def test_get_all_events_iter_with_parentless(parentless_data: List[dict]):
    etc = EventsTreeCollectionProvider5(parentless_data)
    iter_events = etc.get_all_events_iter()
    assert isinstance(iter_events, Generator)
    assert list(iter_events) == parentless_data
    etc.get_parentless_trees()
    iter_events = etc.get_all_events_iter()
    parentless_data.insert(6, etc._build_stub_event("e"))
    assert list(iter_events) == parentless_data


def test_get_all_events_with_parentless(parentless_data: List[dict]):
    etc = EventsTreeCollectionProvider5(parentless_data)
    events = etc.get_all_events()
    assert isinstance(events, list)
    assert events == parentless_data
    etc.get_parentless_trees()
    events = etc.get_all_events()
    parentless_data.insert(6, etc._build_stub_event("e"))
    assert events == parentless_data


def test_get_event_with_parentless(parentless_data: List[dict]):
    etc = EventsTreeCollectionProvider5(parentless_data)
    assert etc.get_event("a") and etc.get_event("x")
    assert etc.get_event("d") and etc.get_event("t")
    etc.get_parentless_trees()
    assert etc.get_event("d") and etc.get_event("t") and etc.get_event("e")

    with pytest.raises(EventIdNotInTree):
        etc.get_event("EventIdNotInTree")


def test_get_leaves_iter_with_parentless(parentless_data: List[dict]):
    etc = EventsTreeCollectionProvider5(parentless_data)
    iter_leaves = etc.get_leaves_iter()
    assert isinstance(iter_leaves, Generator)
    assert list(iter_leaves) == [parentless_data[2], parentless_data[5]]
    etc.get_parentless_trees()
    iter_leaves = etc.get_leaves_iter()
    assert list(iter_leaves) == [parentless_data[2], parentless_data[5], parentless_data[7]]


def test_get_leaves_with_parentless(parentless_data: List[dict]):
    etc = EventsTreeCollectionProvider5(parentless_data)
    leaves = etc.get_leaves()
    assert isinstance(leaves, tuple)
    assert leaves == (parentless_data[2], parentless_data[5])
    etc.get_parentless_trees()
    leaves = etc.get_leaves()
    assert leaves == (parentless_data[2], parentless_data[5], parentless_data[7])


def test_get_children_iter_with_parentless(parentless_data: List[dict]):
    etc = EventsTreeCollectionProvider5(parentless_data)
    etc.get_parentless_trees()
    iter_children_0 = etc.get_children_iter("e")
    iter_children_1 = etc.get_children_iter("d")
    assert isinstance(iter_children_0, Generator)
    assert list(iter_children_0) == [parentless_data[6]]
    assert list(iter_children_1) == [parentless_data[7]]

    with pytest.raises(EventIdNotInTree):
        list(etc.get_children_iter("EventIdNotInTree"))


def test_get_children_with_parentless(parentless_data: List[dict]):
    etc = EventsTreeCollectionProvider5(parentless_data)
    etc.get_parentless_trees()
    children_0 = etc.get_children("e")
    children_1 = etc.get_children("d")
    assert isinstance(children_0, tuple)
    assert children_0 == (parentless_data[6],)
    assert children_1 == (parentless_data[7],)

    with pytest.raises(EventIdNotInTree):
        list(etc.get_children("EventIdNotInTree"))


def test_get_parent_with_parentless(parentless_data: List[dict]):
    etc = EventsTreeCollectionProvider5(parentless_data)
    with pytest.raises(EventIdNotInTree):
        etc.get_parent("d")
    assert etc.get_parent("t") == etc.get_event("d")
    etc.get_parentless_trees()
    assert etc.get_parent("d") == etc._build_stub_event("e")


def test_get_full_path_with_parentless(parentless_data: List[dict]):
    etc = EventsTreeCollectionProvider5(parentless_data)
    with pytest.raises(EventIdNotInTree):
        etc.get_full_path("t")

    etc.get_parentless_trees()
    assert etc.get_full_path("t") == [etc._build_stub_event("e"), parentless_data[6], parentless_data[7]]


def test_get_ancestors_with_parentless(parentless_data: List[dict]):
    etc = EventsTreeCollectionProvider5(parentless_data)
    with pytest.raises(EventIdNotInTree):
        etc.get_ancestors("t")
    etc.get_parentless_trees()
    assert etc.get_ancestors("t") == [etc._build_stub_event("e"), parentless_data[6]]


def test_find_ancestor_with_parentless(parentless_data: List[dict]):
    etc = EventsTreeCollectionProvider5(parentless_data)
    assert etc.find_ancestor("t", lambda event: "t" in event["eventName"]) is None
    etc.get_parentless_trees()
    assert etc.find_ancestor("t", lambda event: "d" in event["eventName"]) == parentless_data[6]


def test_findall_iter_with_parentless(parentless_data: List[dict]):
    etc = EventsTreeCollectionProvider5(parentless_data)
    assert list(etc.findall_iter(lambda event: "Broken_Event" == event["eventName"])) == []
    etc.get_parentless_trees()
    assert list(etc.findall_iter(lambda event: "Broken_Event" == event["eventName"]))[0] == etc._build_stub_event("e")


def test_findall_with_parentless(parentless_data: List[dict]):
    etc = EventsTreeCollectionProvider5(parentless_data)
    assert etc.findall(lambda event: "Broken_Event" == event["eventName"]) == []
    etc.get_parentless_trees()
    assert etc.findall(lambda event: "Broken_Event" == event["eventName"])[0] == etc._build_stub_event("e")


def test_find_with_parentless(parentless_data: List[dict]):
    etc = EventsTreeCollectionProvider5(parentless_data)
    assert etc.find(lambda event: "Broken_Event" == event["eventName"]) is None
    etc.get_parentless_trees()
    assert etc.find(lambda event: "Broken_Event" == event["eventName"]) == etc._build_stub_event("e")


def test_subtree_with_parentless(parentless_data: List[dict]):
    etc = EventsTreeCollectionProvider5(parentless_data)
    parentless = etc.get_parentless_trees()
    assert etc.len_detached_events == 0 and len(parentless[0]) == 3
    assert len(etc.get_subtree("d")) == 2 and len(etc.get_subtree("t")) == 1

    with pytest.raises(EventIdNotInTree):
        etc.get_subtree("EventIdNotInTree")


def test_contains_with_parentless(parentless_data: List[dict]):
    etc = EventsTreeCollectionProvider5(parentless_data)
    detached = ["a", "b", "c", "x", "y", "z"]
    assert all([id in etc for id in detached])
    detached.extend(["e", "d", "t"])
    with pytest.raises(AssertionError):
        assert all([id in etc for id in detached])
    etc.get_parentless_trees()
    assert all([id in etc for id in detached])


def test_get_all_events(general_data: List[dict]):
    collection = EventsTreeCollectionProvider5(general_data)

    assert len(collection.get_all_events()) == len(general_data)


def test_get_all_events_iter(general_data: List[dict]):
    collection = EventsTreeCollectionProvider5(general_data)

    assert len(list(collection.get_all_events_iter())) == len(general_data)


def test_get_event(general_data: List[dict]):
    collection = EventsTreeCollectionProvider5(general_data)

    assert collection.get_event("6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e")


def test_get_full_path(general_data: List[dict]):
    collection = EventsTreeCollectionProvider5(general_data)

    assert collection.get_full_path("8c3fec4f-d1b4-11eb-bae5-57b0c4472880") == [
        {
            "batchId": None,
            "eventId": "84db48fc-d1b4-11eb-b0fb-199708acc7bc",
            "eventName": "[TS_1]Aggressive IOC vs two orders: second order's price is lower than first",
            "eventType": "",
            "isBatched": False,
            "parentEventId": None,
        },
        {
            "batchId": None,
            "eventId": "88a3ee80-d1b4-11eb-b0fb-199708acc7bc",
            "eventName": "Case[TC_1.1]: Trader DEMO-CONN1 vs trader DEMO-CONN2 for instrument INSTR1",
            "eventType": "",
            "isBatched": False,
            "parentEventId": "84db48fc-d1b4-11eb-b0fb-199708acc7bc",
        },
        {
            "batchId": None,
            "eventId": "8bc787fe-d1b4-11eb-bae5-57b0c4472880",
            "eventName": 'placeOrderFIX demo-conn1 - STEP1: Trader "DEMO-CONN1" sends request to create passive Order.',
            "eventType": "placeOrderFIX",
            "isBatched": False,
            "parentEventId": "88a3ee80-d1b4-11eb-b0fb-199708acc7bc",
        },
        {
            "batchId": None,
            "eventId": "8c3fec4f-d1b4-11eb-bae5-57b0c4472880",
            "eventName": "Send 'NewOrderSingle' message to connectivity",
            "eventType": "Outgoing message",
            "isBatched": False,
            "parentEventId": "8bc787fe-d1b4-11eb-bae5-57b0c4472880",
        },
    ]


def test_get_full_path_with_field(general_data: List[dict]):
    collection = EventsTreeCollectionProvider5(general_data)

    assert collection.get_full_path("8c3fec4f-d1b4-11eb-bae5-57b0c4472880", field="eventName") == [
        "[TS_1]Aggressive IOC vs two orders: second order's price is lower than first",
        "Case[TC_1.1]: Trader DEMO-CONN1 vs trader DEMO-CONN2 for instrument INSTR1",
        'placeOrderFIX demo-conn1 - STEP1: Trader "DEMO-CONN1" sends request to create passive Order.',
        "Send 'NewOrderSingle' message to connectivity",
    ]


def test_get_leaves(general_data: List[dict]):
    collection = EventsTreeCollectionProvider5(general_data)

    assert len(collection.get_leaves()) == 14


def test_get_children(general_data: List[dict]):
    collection = EventsTreeCollectionProvider5(general_data)

    assert (
        len(collection.get_children("6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e")) == 10
    )


def test_get_children_iter(general_data: List[dict]):
    collection = EventsTreeCollectionProvider5(general_data)

    assert (
        len(
            list(
                collection.get_children_iter(
                    "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e"
                )
            )
        )
        == 10
    )


def test_get_parent(general_data: List[dict]):
    collection = EventsTreeCollectionProvider5(general_data)

    assert collection.get_parent("6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e") == {
        "batchId": None,
        "eventId": "8bc787fe-d1b4-11eb-bae5-57b0c4472880",
        "eventName": 'placeOrderFIX demo-conn1 - STEP1: Trader "DEMO-CONN1" sends ' "request to create passive Order.",
        "eventType": "placeOrderFIX",
        "isBatched": False,
        "parentEventId": "88a3ee80-d1b4-11eb-b0fb-199708acc7bc",
    }


def test_find_ancestor(general_data: List[dict]):
    collection = EventsTreeCollectionProvider5(general_data)

    assert collection.find_ancestor(
        "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114a4-d1b4-11eb-9278-591e568ad66e",
        lambda event: "placeOrderFIX" in event["eventName"],
    )


def test_build_parentless_tree(general_data: List[dict]):
    collections = EventsTreeCollectionProvider5(general_data)
    trees = collections.get_parentless_trees()

    template = {
        "attachedMessageIds": [],
        "batchId": "Broken_Event",
        "endTimestamp": {"nano": 0, "epochSecond": 0},
        "startTimestamp": {"nano": 0, "epochSecond": 0},
        "type": "event",
        "eventName": "Broken_Event",
        "eventType": "Broken_Event",
        "parentEventId": "Broken_Event",
        "successful": None,
        "isBatched": None,
    }

    assert trees[0].get_all_events() == [
        {"eventId": "a3779b94-d051-11eb-986f-1e8d42132387", **template},
        {
            "batchId": "654c2724-5202-460b-8e6c-a7ee9fb02ddf",
            "eventId": "654c2724-5202-460b-8e6c-a7ee9fb02ddf:8ca20288-d1b4-11eb-986f-1e8d42132387",
            "eventName": "Remove 'NewOrderSingle' id='demo-conn1:SECOND:1624005455622135205' Hash='7009491514226292581' Group='NOS_CONN' Hash['SecondaryClOrdID': 11111, 'SecurityID': INSTR1]",
            "isBatched": True,
            "eventType": "",
            "parentEventId": "a3779b94-d051-11eb-986f-1e8d42132387",
        },
    ] and trees[1].get_all_events() == [
        {"eventId": "845d70d2-9c68-11eb-8598-691ebd7f413d", **template},
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


def test_checker_tree_with_detached_events(log_checker, detached_data: List[dict]):
    etc = EventsTreeCollectionProvider5(detached_data)
    # log_checker.detached_etc_created(etc)


def test_show_warning_about_detached_events(detached_data: List[dict]):
    def create_etc():
        etc = EventsTreeCollectionProvider5(detached_data)

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        create_etc()
        assert "The collection were built with detached events because there are no some events in the source" in str(
            w[-1].message
        )


def test_get_tree_by_id(general_data: List[dict]):
    collection = EventsTreeCollectionProvider5(general_data)
    tree = collection.get_trees()[0]

    assert collection.get_tree_by_id("8d6e0c9e-d1b4-11eb-9278-591e568ad66e") == tree
    assert collection.get_tree_by_id("84db48fc-d1b4-11eb-b0fb-199708acc7bc") == tree
    assert collection.get_tree_by_id("8c3fec4f-d1b4-11eb-bae5-57b0c4472880") == tree


def test_get_root_by_id(general_data: List[dict]):
    collection = EventsTreeCollectionProvider5(general_data)
    tree = collection.get_trees()[0]
    dict_root = tree.get_event("84db48fc-d1b4-11eb-b0fb-199708acc7bc")
    assert collection.get_root_by_id("84db48fc-d1b4-11eb-b0fb-199708acc7bc") == dict_root
    assert collection.get_root_by_id("88a3ee80-d1b4-11eb-b0fb-199708acc7bc") == dict_root


def test_get_detached_events_iter(parentless_data: List[dict]):
    etc = EventsTreeCollectionProvider5(parentless_data)
    iter_detached = etc.get_detached_events_iter()
    assert isinstance(iter_detached, Generator)
    assert list(iter_detached) == [parentless_data[6], parentless_data[7]]


def test_get_detached_events(parentless_data: List[dict]):
    etc = EventsTreeCollectionProvider5(parentless_data)
    detached = etc.get_detached_events()
    assert isinstance(detached, list)
    assert detached == [parentless_data[6], parentless_data[7]]


def test_get_parentless_tree_collection(parentless_data: List[dict]):
    etc = EventsTreeCollectionProvider5(parentless_data)
    expected_events = [
        parentless_data[6],
        parentless_data[7],
        {"type": "event", "eventId": "k", "eventName": "k", "parentEventId": "m"},
        {"type": "event", "eventId": "s", "eventName": "s", "parentEventId": "k"},
    ]
    etc.append_event(expected_events[2])
    etc.append_event(expected_events[3])
    assert etc.len_trees == 6 and etc.len_detached_events == 4
    plt_c = etc.get_parentless_tree_collection()
    expected_events.insert(0, etc._build_stub_event("e"))
    expected_events.insert(3, etc._build_stub_event("m"))
    assert plt_c.len_trees == 6 and plt_c.get_all_events() == expected_events
    assert etc.get_detached_events() == []
