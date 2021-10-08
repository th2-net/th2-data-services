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
    data = Data(general_data).filter(lambda record: record.get("batchId") is None).map(lambda record: (record.get("eventType"), record.get("eventType")))

    assert len(list(data)) == 18


def test_shuffle_data(general_data: List[dict]):
    data = Data(general_data).filter(lambda record: record.get("batchId") is not None).map(lambda record: record.get("eventId")).filter(lambda record: "b" in record)

    assert len(list(data)) == 12


def test_limit(general_data: List[dict]):
    data = Data(general_data)
    data10 = data.limit(10)
    data5 = data10.limit(5)

    assert len(list(data10)) == 10
    assert len(list(data5)) == 5


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


def test_data_cache(general_data: List[dict]):
    data = Data(general_data, cache=True)

    output1 = list(data)

    data.use_cache(False)
    data._data = []
    output2 = list(data)

    data.use_cache(True)
    output3 = list(data)

    assert output1 == output3 and output2 == []


def test_data_cache_magic_function(general_data: List[dict]):
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


def test_write_to_file(
    general_data,
):
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


@pytest.mark.parametrize("cache", [True, False])
def test_len(general_data: List[dict], cache):

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
        assert Path(f"./temp/{data._cache_filename}").is_file() is True, f"The cache was dumped after using len: {cache}"
    else:
        assert Path(f"./temp/{data._cache_filename}").is_file() is False, f"The cache was dumped after using len: {cache}"

    # Check that we do not calc len, after already calculated len or after iter
    # TODO - append when we add logging


def test_is_empty(general_data: List[dict]):
    empty_data = Data([])
    data = Data(general_data)

    assert empty_data.is_empty is True
    assert data.is_empty is False
