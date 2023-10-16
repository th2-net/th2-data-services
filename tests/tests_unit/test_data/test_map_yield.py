from typing import List

from th2_data_services.data import Data
from tests.tests_unit.utils import (
    is_cache_file_exists,
    is_pending_cache_file_exists,
    return_two_items_if_value_greater_than_10,
)


def test_map_yield_with_simple_function():
    data = Data([1, 2, 3, 4]).map_yield(lambda a: a * 2)
    assert list(data) == [2, 4, 6, 8]


def test_map_yield_list_return_value_increases_size():
    data = Data([1, 5, 10, 15, 20]).map_yield(return_two_items_if_value_greater_than_10)
    assert list(data) == [1, 5, 10, 15, 15, 20, 20]


def test_map_yield_chaining():
    data = (
        Data([2, 4, 6, 8])
        .map_yield(lambda a: a * 2)
        .map_yield(return_two_items_if_value_greater_than_10)
    )
    assert list(data) == [4, 8, 12, 12, 16, 16]


def test_map_yield_chaining_with_other_methods(general_data: List[dict]):
    data = (
        Data([5, 10, 15, 20])
        .filter(lambda item: item**2 > 100)
        .map_yield(lambda item: [item, item])
    )
    assert list(data) == [15, 15, 20, 20]


def test_increase_records_after_similar_map_yield():
    source = [1, 2, 3]

    data = (
        Data(source).map_yield(lambda item: [item, item]).map_yield(lambda item: [item, item, item])
    )

    assert list(data) == [
        1,
        1,
        1,
        1,
        1,
        1,
        2,
        2,
        2,
        2,
        2,
        2,
        3,
        3,
        3,
        3,
        3,
        3,
    ]


def test_map_yield_big_modification_chain():
    d1 = Data([1, 2, 3, 4, 5]).use_cache(True)
    d2 = d1.filter(lambda x: x == 1 or x == 2)
    d3 = d2.map_yield(lambda item: [item, item]).use_cache(True)
    d4 = d3.limit(3)
    d5 = d4.map_yield(lambda item: [item, item])

    # It should have all "Data[d3] Iterating working data" log records (for each data object)
    assert list(d5) == [1, 1, 1, 1, 2, 2]
    # Cache files should not be written because they not iterated to the end.
    assert not is_cache_file_exists(d3)
    assert not is_cache_file_exists(d1)
    assert not is_pending_cache_file_exists(d3)
    assert not is_pending_cache_file_exists(d1)

    assert list(d4) == [1, 1, 2]
    assert list(d3) == [1, 1, 2, 2]  # It also should iterate cache file.


def test_map_yield_for_list_record(general_data: List[dict]):
    data = (
        Data(general_data)
        .map_yield(lambda record: [record, record])
        .map_yield(lambda record: record.get("eventType"))
    )

    event_types = [
        "",
        "",
        "",
        "",
        "placeOrderFIX",
        "placeOrderFIX",
        "Checkpoint",
        "Checkpoint",
        "Checkpoint for session",
        "Checkpoint for session",
        "Checkpoint for session",
        "Checkpoint for session",
        "Checkpoint for session",
        "Checkpoint for session",
        "Checkpoint for session",
        "Checkpoint for session",
        "Checkpoint for session",
        "Checkpoint for session",
        "Checkpoint for session",
        "Checkpoint for session",
        "Checkpoint for session",
        "Checkpoint for session",
        "Checkpoint for session",
        "Checkpoint for session",
        "Checkpoint for session",
        "Checkpoint for session",
        "Checkpoint for session",
        "Checkpoint for session",
        "Outgoing message",
        "Outgoing message",
        "Outgoing message",
        "Outgoing message",
        "",
        "",
        "Send message",
        "Send message",
        "Send message",
        "Send message",
        "message",
        "message",
        "Checkpoint for session",
        "Checkpoint for session",
    ]
    assert event_types == list(data)
