from typing import List, NamedTuple

from th2_data_services.provider.v5.events_tree.events_tree_collection import EventsTreeCollectionProvider5
from th2_data_services.events_tree.events_tree import EventsTree
from th2_data_services.provider.v5.struct import provider5_event_struct


def test_build_tree(general_data: List[dict], test_events_tree: NamedTuple):
    collection = EventsTreeCollectionProvider5(general_data)
    tree = collection.get_trees()[0]

    assert [
        event[provider5_event_struct.EVENT_ID] for event in tree.get_all_events()
    ] == test_events_tree.events and list(collection.detached_events.keys()) == test_events_tree.unknown_events


def test_append_unknown_element(general_data: List[dict]):
    collection = EventsTreeCollectionProvider5(general_data)
    parent_event_id = "122111-2112-3333-445544"
    event_id = "111111-2222-3333-444444"
    new_event = {
        "eventId": event_id,
        "parentEventId": parent_event_id,
        "eventName": "testName",
    }
    collection.append_event(new_event)

    assert parent_event_id in collection.detached_events and event_id in [
        event["eventId"] for event in collection.detached_events[parent_event_id]
    ]


def test_append_new_element(general_data: List[dict]):
    collection = EventsTreeCollectionProvider5(general_data)
    parent_event_id = "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e"
    event_id = "1111-3333-4444-5555"
    new_event = {
        "eventId": event_id,
        "parentEventId": parent_event_id,
        "eventName": "testName",
    }
    collection.append_event(new_event)

    assert event_id in collection


def test_build_parentless_trees(general_data: List[dict]):
    general_data += [
        {
            "eventId": "a3779b94-d051-11eb-986f-1e8d42132387",
            "parentEventId": "a3777794-d051-11eb-986f-1eddddd387",
            "eventName": "test",
        }
    ]

    collection = EventsTreeCollectionProvider5(general_data)
    trees = collection.get_parentless_trees()

    assert trees[1]._tree.get_node("a3779b94-d051-11eb-986f-1e8d42132387") and not collection.detached_events


def test_contain_element(general_data: List[dict]):
    collection = EventsTreeCollectionProvider5(general_data)
    tree = collection.get_trees()[0]
    event_id = "84db48fc-d1b4-11eb-b0fb-199708acc7bc"

    assert event_id in collection and event_id in tree


def test_append_new_tree(general_data: List[dict]):
    collection = EventsTreeCollectionProvider5(general_data)
    event_id = "1111-3333-4444-5555"
    new_event = {"eventId": event_id, "eventName": "testName"}
    collection.append_event(new_event)

    assert event_id in collection and event_id in collection.get_roots_ids()


def test_filter_all(general_data: List[dict]):
    tree = EventsTreeCollectionProvider5(general_data).get_trees()[0]

    assert len(tree.findall(lambda event: "Checkpoint" in event["eventName"])) == 11


def test_filter_all_max_count(general_data: List[dict]):
    tree = EventsTreeCollectionProvider5(general_data).get_trees()[0]

    assert len(tree.findall(lambda event: "Checkpoint" in event["eventName"], max_count=5)) == 5


def test_filter_stop_function(general_data: List[dict]):
    tree = EventsTreeCollectionProvider5(general_data).get_trees()[0]

    assert (
        len(
            tree.findall(
                lambda event: "Checkpoint" in event["eventName"],
                stop=lambda event: "th2-hand-demo" in event["eventName"],
            )
        )
        == 1
    )


def test_filter_one(general_data: List[dict]):
    tree = EventsTreeCollectionProvider5(general_data).get_trees()[0]

    assert tree.find(lambda event: "Checkpoint" in event["eventName"]) == {
        "batchId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4",
        "eventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        "eventName": "Checkpoint",
        "eventType": "Checkpoint",
        "isBatched": True,
        "parentEventId": "8bc787fe-d1b4-11eb-bae5-57b0c4472880",
    }


def test_filter_stop(general_data: List[dict]):
    tree = EventsTreeCollectionProvider5(general_data).get_trees()[0]

    assert not tree.find(
        lambda event: "Checkpoint" in event["eventName"],
        stop=lambda event: "Checkpoint" in event["eventType"],
    )


def test_subtree(general_data: List[dict]):
    tree = EventsTreeCollectionProvider5(general_data).get_trees()[0]
    assert isinstance(
        tree.get_subtree("6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e"), EventsTree
    )
    assert len(tree.get_subtree("6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e")) == 11


def test_get_all_events(general_data: List[dict]):
    tree = EventsTreeCollectionProvider5(general_data).get_trees()[0]

    assert len(tree.get_all_events()) == 18


def test_get_all_events_iter(general_data: List[dict]):
    tree = EventsTreeCollectionProvider5(general_data).get_trees()[0]

    assert len(list(tree.get_all_events_iter())) == 18


def test_get_event(general_data: List[dict]):
    tree = EventsTreeCollectionProvider5(general_data).get_trees()[0]

    assert tree.get_event("6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e")


def test_get_full_path(general_data: List[dict]):
    tree = EventsTreeCollectionProvider5(general_data).get_trees()[0]

    assert tree.get_full_path("8c3fec4f-d1b4-11eb-bae5-57b0c4472880") == [
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
    tree = EventsTreeCollectionProvider5(general_data).get_trees()[0]

    assert tree.get_full_path("8c3fec4f-d1b4-11eb-bae5-57b0c4472880", field="eventName") == [
        "[TS_1]Aggressive IOC vs two orders: second order's price is lower than first",
        "Case[TC_1.1]: Trader DEMO-CONN1 vs trader DEMO-CONN2 for instrument INSTR1",
        'placeOrderFIX demo-conn1 - STEP1: Trader "DEMO-CONN1" sends request to create passive Order.',
        "Send 'NewOrderSingle' message to connectivity",
    ]


def test_get_leaves(general_data: List[dict]):
    tree = EventsTreeCollectionProvider5(general_data).get_trees()[0]

    assert len(tree.get_leaves()) == 14


def test_get_root_id(general_data: List[dict]):
    tree = EventsTreeCollectionProvider5(general_data).get_trees()[0]

    assert tree.get_root_id() == "84db48fc-d1b4-11eb-b0fb-199708acc7bc"


def test_get_children(general_data: List[dict]):
    tree = EventsTreeCollectionProvider5(general_data).get_trees()[0]

    assert len(tree.get_children("6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e")) == 10


def test_get_children_iter(general_data: List[dict]):
    tree = EventsTreeCollectionProvider5(general_data).get_trees()[0]

    assert (
        len(list(tree.get_children_iter("6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e")))
        == 10
    )


def test_get_parent(general_data: List[dict]):
    tree = EventsTreeCollectionProvider5(general_data).get_trees()[0]

    assert tree.get_parent("6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e") == {
        "batchId": None,
        "eventId": "8bc787fe-d1b4-11eb-bae5-57b0c4472880",
        "eventName": 'placeOrderFIX demo-conn1 - STEP1: Trader "DEMO-CONN1" sends ' "request to create passive Order.",
        "eventType": "placeOrderFIX",
        "isBatched": False,
        "parentEventId": "88a3ee80-d1b4-11eb-b0fb-199708acc7bc",
    }


def test_find_ancestor(general_data: List[dict]):
    tree = EventsTreeCollectionProvider5(general_data).get_trees()[0]

    assert tree.find_ancestor(
        "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c1114a4-d1b4-11eb-9278-591e568ad66e",
        lambda event: "placeOrderFIX" in event["eventName"],
    )


def test_get_root_by_id(general_data: List[dict]):
    collection = EventsTreeCollectionProvider5(general_data)
    tree = collection.get_trees()[0]
    dict_root = tree.get_event("84db48fc-d1b4-11eb-b0fb-199708acc7bc")
    assert collection.get_root_by_id("84db48fc-d1b4-11eb-b0fb-199708acc7bc") == dict_root
    assert collection.get_root_by_id("88a3ee80-d1b4-11eb-b0fb-199708acc7bc") == dict_root


def test_get_root(general_data: List[dict]):
    collection = EventsTreeCollectionProvider5(general_data)
    tree = collection.get_trees()[0]

    assert tree.get_root() == {
        "batchId": None,
        "eventId": "84db48fc-d1b4-11eb-b0fb-199708acc7bc",
        "eventName": "[TS_1]Aggressive IOC vs two orders: second order's price is lower than first",
        "eventType": "",
        "isBatched": False,
        "parentEventId": None,
    }
