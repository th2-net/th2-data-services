from typing import List

from th2_data_services.provider.v5.events_tree.events_tree_collection import EventsTreeCollectionProvider5


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
