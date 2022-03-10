from typing import List, NamedTuple

from tests.conftest import get_super_type
from th2_data_services.events_tree.parent_events_tree import ParentEventsTree


def test_build_tree(general_data: List[dict], test_parent_events_tree: NamedTuple):
    tree = ParentEventsTree(general_data)

    assert list(tree.events.keys()) == test_parent_events_tree.events and sorted(tree.unknown_events.keys()) == sorted(
        test_parent_events_tree.unknown_events
    )


def test_is_in_ancestor_name_positive(general_data: List[dict]):
    tree = ParentEventsTree(general_data)
    event = {
        "eventId": "88a3ee80-d1b4-11eb-b0fb-199708acc7bc",
        "parentEventId": "84db48fc-d1b4-11eb-b0fb-199708acc7bc",
    }
    assert tree.is_in_ancestor_name(event, "Aggressive")


def test_is_in_ancestor_name_negative(general_data: List[dict]):
    tree = ParentEventsTree(general_data)
    event = {
        "eventId": "88a3ee80-d1b4-11eb-b0fb-199708acc7bc",
        "parentEventId": "84db48fc-d1b4-11eb-b0fb-199708acc7bc",
    }
    assert not tree.is_in_ancestor_name(event, "Data")


def test_is_in_ancestor_type_positive(general_data: List[dict]):
    tree = ParentEventsTree(general_data)
    event = {
        "eventId": "88a3ee80-d1b4-11eb-b0fb-199708acc7bc",
        "parentEventId": "84db48fc-d1b4-11eb-b0fb-199708acc7bc",
    }
    assert tree.is_in_ancestor_type(event, "")


def test_is_in_ancestor_type_negative(general_data: List[dict]):
    tree = ParentEventsTree(general_data)
    event = {
        "eventId": "88a3ee80-d1b4-11eb-b0fb-199708acc7bc",
        "parentEventId": "84db48fc-d1b4-11eb-b0fb-199708acc7bc",
    }
    assert not tree.is_in_ancestor_type(event, "NegativeType")


def test_get_ancestor_by_name_positive(general_data: List[dict]):
    tree = ParentEventsTree(general_data)
    event = {
        "eventId": "8c44806c-d1b4-11eb-8e55-d3a76285d588",
        "parentEventId": "8bc787fe-d1b4-11eb-bae5-57b0c4472880",
    }
    assert tree.get_ancestor_by_name(event, "Aggressive")


def test_get_ancestor_by_name_negative(general_data: List[dict]):
    tree = ParentEventsTree(general_data)
    event = {
        "eventId": "8c44806c-d1b4-11eb-8e55-d3a76285d588",
        "parentEventId": "8bc787fe-d1b4-11eb-bae5-57b0c4472880",
    }
    assert tree.get_ancestor_by_name(event, "Passive") is None


def test_get_ancestor_by_super_type_positive(general_data: List[dict]):
    tree = ParentEventsTree(general_data)
    event = {
        "parentEventId": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
        "eventType": "message",
    }

    assert tree.get_ancestor_by_super_type(event, "Test Case", get_super_type)


def test_get_ancestor_by_super_type_negative(general_data: List[dict]):
    tree = ParentEventsTree(general_data)
    event = {
        "parentEventId": "8c035903-d1b4-11eb-9278-591e568ad66e",
        "eventType": "message",
    }

    assert not tree.get_ancestor_by_super_type(event, "Test", get_super_type)
