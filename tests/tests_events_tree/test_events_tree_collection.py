from typing import List

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


def test_get_all_events(general_data: List[dict]):
    collection = EventsTreeCollectionProvider5(general_data)

    assert len(collection.get_all_events()) == 18


def test_get_all_events_iter(general_data: List[dict]):
    collection = EventsTreeCollectionProvider5(general_data)

    assert len(list(collection.get_all_events_iter())) == 18


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
