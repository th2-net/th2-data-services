from typing import List, Iterable

from th2_data_services.data import Data
from th2_data_services.interfaces import IStreamAdapter
from tests.tests_unit.utils import (
    is_cache_file_exists,
    is_pending_cache_file_exists,
    double_generator,
    triple_generator,
    event_type_generator,
)


class SimpleAdapter(IStreamAdapter):
    def handle(self, stream: Iterable):
        for record in stream:
            if record["eventType"] == "Checkpoint":
                yield {"id": record["eventId"], "name": record["eventName"]}


def test_map_stream_with_adapter(general_data: List[dict]):
    data = Data(general_data).map_stream(SimpleAdapter())
    assert list(data) == [
        {
            "id": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
            "name": "Checkpoint",
        }
    ]


def test_map_stream_with_generator_function(general_data: List[dict]):
    def simple_gen(stream):
        for event in stream:
            if event["eventType"] == "Checkpoint":
                yield {"id": event["eventId"], "name": event["eventName"]}

    data = Data(general_data).map_stream(simple_gen)
    assert list(data) == [
        {
            "id": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e",
            "name": "Checkpoint",
        }
    ]


def test_map_stream_chaining(general_data: List[dict]):
    def simple_gen(stream):
        for event in stream:
            if "Checkpoint" in event["name"]:
                yield {"id": event["id"]}

    data = Data(general_data).map_stream(SimpleAdapter()).map_stream(simple_gen)
    assert list(data) == [
        {"id": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e"}
    ]


def test_map_stream_chaining_with_other_methods(general_data: List[dict]):
    def simple_gen(stream):
        for event in stream:
            if event["eventName"] == "Checkpoint":
                yield {"id": event["eventId"]}

    data = (
        Data(general_data)
        .filter(lambda event: "Checkpoint" in event["eventName"])
        .map_stream(simple_gen)
    )
    assert list(data) == [
        {"id": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e"}
    ]


def test_increase_records_after_similar_map_stream():
    source = [1, 2, 3]

    data = Data(source).map_stream(double_generator).map_stream(triple_generator)

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


def test_big_modification_chain(log_checker):
    d1 = Data([1, 2, 3, 4, 5]).use_cache(True)
    d2 = d1.filter(lambda x: x == 1 or x == 2)
    d3 = d2.map_stream(double_generator).use_cache(True)
    d4 = d3.limit(3)
    d5 = d4.map_stream(double_generator)

    # It should have all "Data[d3] Iterating working data" log records (for each data object)
    assert list(d5) == [1, 1, 1, 1, 2, 2]
    # Cache files should not be written because they not iterated to the end.
    assert not is_cache_file_exists(d3)
    assert not is_cache_file_exists(d1)
    assert not is_pending_cache_file_exists(d3)
    assert not is_pending_cache_file_exists(d1)

    assert list(d4) == [1, 1, 2]
    assert list(d3) == [1, 1, 2, 2]  # It also should iterate cache file.


def test_filter_for_list_record(general_data: List[dict]):
    data = (
        Data(general_data)
        .map_stream(double_generator)
        .map_stream(event_type_generator)
        .filter(lambda record: record in ["placeOrderFIX", "Checkpoint"])
    )

    event_types = [
        "placeOrderFIX",
        "placeOrderFIX",
        "Checkpoint",
        "Checkpoint",
    ]

    assert event_types == list(data)


def test_map_stream_for_list_record(general_data: List[dict]):
    data = (
        Data(general_data).map_stream(double_generator).map(lambda record: record.get("eventType"))
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


def test_map_stream_data_increase(general_data: List[dict]):
    data = (
        Data(general_data)
        .filter(lambda record: record.get("batchId") is None)
        .map_stream(double_generator)
        .map_stream(event_type_generator)
    )

    assert len(list(data)) == 18
