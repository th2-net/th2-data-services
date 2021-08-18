from typing import List

from th2_data_services.data import Data


def test_iter_data(general_data: List[dict]):
    data = Data(general_data)

    output = [record for record in data]
    assert len(output) == 21


def test_len_data(general_data: List[dict]):
    data = Data(general_data)

    assert len(data) == 21


def test_filter_data(general_data: List[dict]):
    data = Data(general_data).filter(lambda record: record.get("batchId") is None)

    assert len(data) == 9


def test_map_data_transform(general_data: List[dict]):
    data = Data(general_data).map(lambda record: record.get("eventType"))
    event_types = set([record for record in data])

    assert event_types == {
        "",
        "placeOrderFIX",
        "Send message",
        "Checkpoint",
        "Checkpoint for session",
        "message",
        "Outgoing message",
    }


def test_map_data_increase(general_data: List[dict]):
    data = (
        Data(general_data)
        .filter(lambda record: record.get("batchId") is None)
        .map(lambda record: (record.get("eventType"), record.get("eventType")))
    )

    assert len(data) == 18


def test_shuffle_data(general_data: List[dict]):
    data = (
        Data(general_data)
        .filter(lambda record: record.get("batchId") is not None)
        .map(lambda record: record.get("eventId"))
        .filter(lambda record: "b" in record)
    )

    assert len(data) == 12


def test_sift_limit_data(general_data: List[dict]):
    data = Data(general_data)
    output = [record for record in data.sift(limit=2)]

    assert len(output) == 2


def test_sift_skip_data(general_data: List[dict]):
    data = Data(general_data)
    output1 = [record for record in data.sift(limit=2)]
    output2 = [record for record in data.sift(limit=2, skip=2)]

    assert output1 != output2
