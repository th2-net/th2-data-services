import os
from pathlib import Path
from typing import List

import pytest

from th2_data_services.data import Data


def test_iter_data(general_data: List[dict]):
    data = Data(general_data)

    output = [record for record in data]
    assert len(output) == 21


def test_filter_data(general_data: List[dict]):
    data = Data(general_data).filter(lambda record: record.get("batchId") is None)

    assert len(list(data)) == 9


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

    assert len(list(data)) == 18


def test_map_for_list_record(general_data: List[dict]):
    data = Data(general_data).map(lambda record: [record, record]).map(lambda record: record.get("eventType"))

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


def test_filter_for_list_record(general_data: List[dict]):
    data = (
        Data(general_data)
        .map(lambda record: [record, record])
        .map(lambda record: record.get("eventType"))
        .filter(lambda record: record in ["placeOrderFIX", "Checkpoint"])
    )

    event_types = [
        "placeOrderFIX",
        "placeOrderFIX",
        "Checkpoint",
        "Checkpoint",
    ]

    assert event_types == list(data)


def test_increase_records_after_similar_map(general_data: List[dict]):
    data = Data(general_data).map(lambda record: [record, record]).map(lambda record: [record, record, record])

    assert len(list(data)) == 126


def test_shuffle_data(general_data: List[dict]):
    data = (
        Data(general_data)
        .filter(lambda record: record.get("batchId") is not None)
        .map(lambda record: record.get("eventId"))
        .filter(lambda record: "b" in record)
    )

    assert len(list(data)) == 12


"""def test_main():
    assert main() == [3, 9]
"""


def test_limit(general_data: List[dict]):
    data = Data(general_data)
    data10 = data.limit(10)
    data5 = data10.limit(5)

    assert len(list(data10)) == 10
    assert len(list(data5)) == 5


def test_limit_for_list_record(general_data: List[dict]):
    data = Data(general_data).map(lambda record: [record, record])

    data10 = data.limit(10)
    data5 = data10.limit(5)

    assert len(list(data10)) == 10
    assert len(list(data5)) == 5


def test_limit_in_cycles(general_data: List[dict]):
    data = Data(general_data)
    res5 = [0 for _ in range(4)]
    for _ in data.limit(4):
        res5[0] += 1
        for __ in data.limit(3):
            res5[1] += 1
            for ___ in data.limit(2):
                res5[2] += 1
                for ____ in data.limit(1):
                    res5[3] += 1

    assert res5 == [4, 4 * 3, 4 * 3 * 2, 4 * 3 * 2 * 1]


def test_limit_before_cycles(general_data: List[dict]):
    data3 = Data(general_data)
    data5 = data3.limit(5)

    res5 = [0 for _ in range(4)]

    for _ in data5:
        res5[0] += 1
        for __ in data5:
            res5[1] += 1
            for ___ in data5:
                res5[2] += 1
                for ____ in data5:
                    res5[3] += 1

    assert res5 == [data5._limit_num, data5._limit_num ** 2, data5._limit_num ** 3, data5._limit_num ** 4]

def test_new_limit_is_bigger(general_data: List[dict]):
    data = Data(general_data).limit(3)
    data5 = data.limit(5)
    res = [0 for _ in range(4)]

    for _ in data5:
        res[0] += 1
        for __ in data5:
            res[1] += 1
            for ___ in data5:
                res[2] += 1
                for ____ in data5:
                    res[3] += 1

    assert res == [3, 9, 27, 81]

def test_limit_for_limit_in_iterations(general_data: List[dict]):
    data = Data(general_data)
    data5 = data.limit(5)

    res5 = [0 for _ in range(4)]
    for _ in data5.limit(4):
        res5[0] += 1
        for __ in data5.limit(3):
            res5[1] += 1
            for ___ in data5.limit(7):
                res5[2] += 1
                for ____ in data5.limit(2):
                    res5[3] += 1

    assert res5 == [4, 3 * 4, 3 * 4 * 5, 3 * 4 * 5 * 2]


def test_sift_limit_data(general_data: List[dict]):
    data = Data(general_data)
    output = [record for record in data.sift(limit=2)]

    assert len(output) == 2


def test_sift_skip_data(general_data: List[dict]):
    data = Data(general_data)
    output1 = data.sift(limit=2)
    output2 = [record for record in data.sift(limit=2, skip=2)]

    assert len(list(output1)) == 2
    assert output1 != output2


def test_cache_common(general_data: List[dict]):
    data = Data(general_data, cache=True)

    output1 = list(data)

    data.use_cache(False)
    data._data = []
    output2 = list(data)

    data.use_cache(True)
    output3 = list(data)

    assert output1 == output3 and output2 == []


def test_cache_magic_function(general_data: List[dict]):
    data = Data(general_data, cache=True)
    output1 = len(list(data))

    data = Data(general_data, cache=True)
    bool(data)
    output2 = len(list(data))

    data = Data(general_data, cache=True)
    str(data)
    output3 = len(list(data))

    data = Data(general_data, cache=True)
    work_data = data.filter(lambda record: record.get("batchId") is None)
    output4 = len(list(work_data))
    output5 = len(list(work_data))

    assert output1 == output2 == output3 and output4 == output5 and output1 != output4


def test_cache_inheritance(general_data: List[dict]):
    data = Data(general_data, cache=True)
    data1 = data.filter(lambda record: record.get("isBatched"))
    data2 = data1.map(lambda record: {**record, "batch_status": record.get("isBatched")})
    data2.use_cache(True)
    data3 = data2.filter(lambda record: record.get("eventType"))
    data4 = data1.map(lambda record: (record, record))
    data4.use_cache(True)

    output1 = len(list(data))
    data._data = []
    output2 = len(list(data2))
    output3 = len(list(data3))
    output4 = len(list(data4))
    output5 = len(list(data4))

    assert output1 == 21 and output2 == 11 and output3 == 10 and output4 == output5 == 22


def test_cache_for_source(general_data: List[dict]):
    data = Data(general_data, cache=True)
    data1 = data.filter(lambda record: record.get("isBatched"))
    data2 = data1.map(lambda record: {**record, "batch_status": record.get("isBatched")})
    data3 = data1.map(lambda record: (record, record))

    list(data)
    list(data2)
    list(data3)

    assert data1.get_last_cache() == data2.get_last_cache() == data3.get_last_cache()


def test_cache_for_instance(general_data: List[dict]):
    data = Data(general_data, cache=True)
    data1 = data.filter(lambda record: record.get("isBatched"))
    data1.use_cache(True)
    data2 = data1.map(lambda record: {**record, "batch_status": record.get("isBatched")})
    data2.use_cache(True)
    data3 = data1.map(lambda record: (record, record))
    data3.use_cache(True)
    data4 = data1.map(lambda record: (record, record))
    data4.use_cache(True)

    list(data)
    list(data1)
    list(data4)

    assert data1.get_last_cache() != data4.get_last_cache() and data2.get_last_cache() == data3.get_last_cache()


def test_write_to_file(general_data):
    events = Data(general_data)
    file_to_test = "demo_file.txt"
    expected = """{'batchId': None,
 'eventId': '84db48fc-d1b4-11eb-b0fb-199708acc7bc',
 'eventName': "[TS_1]Aggressive IOC vs two orders: second order's price is "
              'lower than first',
 'eventType': '',
 'isBatched': False,
 'parentEventId': None}
--------------------------------------------------
"""
    events.limit(1).write_to_file(file_to_test)
    with open(file_to_test) as f:
        assert f.read() == expected

    os.remove(file_to_test)


@pytest.mark.parametrize("cache ", [True, False])
def test_len_with_stream_cache(general_data: List[dict], cache):
    # From empty list
    data = Data(general_data, cache=cache)
    assert data.len == len(list(data))
    assert data.limit(10).len == 10
    elements_num = len(list(data))

    # After print
    data = Data(general_data, cache=cache)
    str(data)  # The same as print.
    assert data.len == elements_num, f"After print, cache: {cache}"

    # After is_empty
    data = Data(general_data, cache=cache)
    r = data.is_empty
    assert data.len == elements_num, f"After is_empty, cache: {cache}"

    # After sift
    data = Data(general_data, cache=cache)
    r = list(data.sift(limit=5))
    assert data.len == elements_num, f"After sift, cache: {cache}"

    # The cache was dumped after using len
    data = Data(general_data, cache=cache)
    r = data.len
    if cache:
        assert (
            Path(f"./temp/{data._cache_filename}").is_file() is True
        ), f"The cache was dumped after using len: {cache}"
    else:
        assert (
            Path(f"./temp/{data._cache_filename}").is_file() is False
        ), f"The cache was dumped after using len: {cache}"

    # Check that we do not calc len, after already calculated len or after iter
    # TODO - append when we add logging


def test_is_empty(general_data: List[dict]):
    empty_data = Data([])
    data = Data(general_data)

    assert empty_data.is_empty is True
    assert data.is_empty is False
