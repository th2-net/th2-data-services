from typing import List, Iterable

from th2_data_services import Data
from th2_data_services.interfaces import IStreamAdapter


class SimpleAdapter(IStreamAdapter):
    def handle(self, stream: Iterable):
        for record in stream:
            if record["eventType"] == "Checkpoint":
                yield {"id": record["eventId"], "name": record["eventName"]}


def test_map_stream_with_adapter(general_data: List[dict]):
    data = Data(general_data).map_stream(SimpleAdapter())
    assert list(data) == [
        {"id": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e", "name": "Checkpoint"}
    ]


def test_map_stream_with_generator_function(general_data: List[dict]):
    def simple_gen(stream):
        for event in stream:
            if event["eventType"] == "Checkpoint":
                yield {"id": event["eventId"], "name": event["eventName"]}

    data = Data(general_data).map_stream(simple_gen)
    assert list(data) == [
        {"id": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e", "name": "Checkpoint"}
    ]


def test_map_stream_chaining(general_data: List[dict]):
    def simple_gen(stream):
        for event in stream:
            if "Checkpoint" in event["name"]:
                yield {"id": event["id"]}

    data = Data(general_data).map_stream(SimpleAdapter()).map_stream(simple_gen)
    assert list(data) == [{"id": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e"}]


def test_map_stream_chaining_with_other_methods(general_data: List[dict]):
    def simple_gen(stream):
        for event in stream:
            if event["eventName"] == "Checkpoint":
                yield {"id": event["eventId"]}

    data = Data(general_data).filter(lambda event: "Checkpoint" in event["eventName"]).map_stream(simple_gen)
    assert list(data) == [{"id": "6e3be13f-cab7-4653-8cb9-6e74fd95ade4:8c035903-d1b4-11eb-9278-591e568ad66e"}]
