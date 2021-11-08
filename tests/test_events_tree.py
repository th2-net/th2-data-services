from typing import List, NamedTuple

from tests.conftest import get_super_type
from th2_data_services.events_tree import EventsTree, ParentEventsTree


def test_build_tree(general_data: List[dict], test_events_tree: NamedTuple):
    tree = EventsTree(general_data)

    assert all(
        [
            list(tree.events.keys()) == test_events_tree.events,
            list(tree.unknown_events.keys()) == test_events_tree.unknown_events,
        ]
    )

def test_build_parent_tree(general_data: List[dict], test_parent_events_tree: list):
    tree = ParentEventsTree(general_data)

    assert list(tree.parent_events.keys()) == test_parent_events_tree



def test_append_element(general_data: List[dict], test_events_tree: NamedTuple):
    tree = EventsTree(general_data)
    new_event = {
        "eventId": "111111-2222-3333-444444",
    }

    tree.append_element(new_event)

    assert list(tree.events.keys()) == [
        *test_events_tree.events,
        "111111-2222-3333-444444",
    ]


def test_search_unknown_parents(general_data: List[dict], test_events_tree: NamedTuple):
    tree = EventsTree(general_data)
    new_event = {"eventId": "111111-2222-3333-444444", "parentEventId": "111111"}

    tree.append_element(new_event)
    assert list(tree.search_unknown_parents()) == [
        *test_events_tree.unknown_events,
        "111111",
    ]


def test_is_in_ancestor_name_positive(general_data: List[dict]):
    tree = EventsTree(general_data)
    event = {
        "eventId": "8c035903-d1b4-11eb-9278-591e568ad66e",
        "parentEventId": "8bc787fe-d1b4-11eb-bae5-57b0c4472880",
    }
    assert tree.is_in_ancestor_name(event, "Case")


def test_is_in_ancestor_name_negative(general_data: List[dict]):
    tree = EventsTree(general_data)
    event = {
        "eventId": "8c035903-d1b4-11eb-9278-591e568ad66e",
        "parentEventId": "8bc787fe-d1b4-11eb-bae5-57b0c4472880",
    }
    assert not tree.is_in_ancestor_name(event, "TestTest")


def test_is_in_ancestor_type_positive(general_data: List[dict]):
    tree = EventsTree(general_data)
    event = {
        "eventId": "8c3fec4f-d1b4-11eb-bae5-57b0c4472880",
        "parentEventId": "8bc787fe-d1b4-11eb-bae5-57b0c4472880",
    }
    assert tree.is_in_ancestor_type(event, "placeOrderFIX")


def test_is_in_ancestor_type_negative(general_data: List[dict]):
    tree = EventsTree(general_data)
    event = {
        "eventId": "8c3fec4f-d1b4-11eb-bae5-57b0c4472880",
        "parentEventId": "8bc787fe-d1b4-11eb-bae5-57b0c4472880",
    }
    assert not tree.is_in_ancestor_type(event, "message")


def test_get_ancestor_by_name_positive(general_data: List[dict]):
    tree = EventsTree(general_data)
    event = {
        "eventId": "8c44806c-d1b4-11eb-8e55-d3a76285d588",
        "parentEventId": "8bc787fe-d1b4-11eb-bae5-57b0c4472880",
    }
    assert tree.get_ancestor_by_name(event, "Aggressive")


def test_get_ancestor_by_name_negative(general_data: List[dict]):
    tree = EventsTree(general_data)
    event = {
        "eventId": "8c44806c-d1b4-11eb-8e55-d3a76285d588",
        "parentEventId": "8bc787fe-d1b4-11eb-bae5-57b0c4472880",
    }
    assert tree.get_ancestor_by_name(event, "Passive") is None


def test_get_ancestor_by_super_type_positive(general_data: List[dict]):
    tree = EventsTree(general_data)
    event = {
        "parentEventId": "8c035903-d1b4-11eb-9278-591e568ad66e",
        "eventType": "message",
    }

    assert tree.get_ancestor_by_super_type(event, "Test Case", get_super_type)


def test_get_ancestor_by_super_type_negative(general_data: List[dict]):
    tree = EventsTree(general_data)
    event = {
        "parentEventId": "8c035903-d1b4-11eb-9278-591e568ad66e",
        "eventType": "message",
    }

    assert not tree.get_ancestor_by_super_type(event, "Test", get_super_type)
