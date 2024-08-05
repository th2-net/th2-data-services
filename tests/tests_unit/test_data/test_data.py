import os
from typing import List

from tests.tests_unit.utils import (
    is_cache_file_exists,
    iterate_data,
    is_pending_cache_file_exists,
)
from th2_data_services.data import Data
import pytest


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


def test_shuffle_data(general_data: List[dict]):
    data = (
        Data(general_data)
        .filter(lambda record: record.get("batchId") is not None)
        .map(lambda record: record.get("eventId"))
        .filter(lambda record: "b" in record)
    )

    assert len(list(data)) == 12


def test_limit(general_data: List[dict], cache):
    data = Data(general_data, cache=cache)
    data10 = data.limit(10)
    data5 = data10.limit(5)

    assert list(data10) == general_data[:10]
    if cache:
        assert not is_cache_file_exists(
            data
        ), "data shouldn't have cache because was iterated via child data object."
        assert not is_pending_cache_file_exists(
            data
        ), "data shouldn't have cache because was iterated via child data object."
    assert list(data5) == general_data[:5]
    assert data.len == len(general_data)
    assert data10.len == 10
    assert data5.len == 5


def test_limit_for_list_record(cache):
    data_stream = [1, 2, 3, 4, 5]
    data = Data(data_stream, cache=cache).map(lambda record: [record, record])

    data10 = data.limit(4)
    data5 = data10.limit(2)

    assert list(data10) == [[1, 1], [2, 2], [3, 3], [4, 4]]
    if cache:
        assert not is_cache_file_exists(
            data
        ), "data shouldn't have cache because was iterated via child data object."
        assert not is_pending_cache_file_exists(
            data
        ), "data shouldn't have cache because was iterated via child data object."
    assert list(data5) == [[1, 1], [2, 2]]


def test_limit_in_loops(cache):
    data_stream = [1, 2, 3, 4, 5]
    data = Data(data_stream, cache=cache)
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
    assert not is_cache_file_exists(data)
    assert not is_pending_cache_file_exists(data)
    assert data.len == len(data_stream)  # It'll create cache.


def test_limit_before_loops(cache=True):
    """Related Windows bug: https://exactpro.atlassian.net/browse/TH2-3767"""
    data_stream = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    data = Data(data_stream, cache)
    limit = 5
    data5 = data.limit(limit)

    res5 = [0 for _ in range(4)]

    for _ in data5:
        res5[0] += 1
        for __ in data5:
            res5[1] += 1
            for ___ in data5:
                res5[2] += 1
                for ____ in data5:
                    res5[3] += 1

    assert res5 == [limit, limit**2, limit**3, limit**4]
    assert not is_cache_file_exists(data)
    assert not is_pending_cache_file_exists(data)
    assert data.len == len(data_stream)  # It'll create cache.
    assert is_cache_file_exists(data)


def test_new_limit_is_less(general_data: List[dict], cache):
    data5 = Data(general_data, cache).limit(5)
    data3 = data5.limit(3)
    res = [0 for _ in range(4)]

    for _ in data3:
        res[0] += 1
        for __ in data3:
            res[1] += 1
            for ___ in data3:
                res[2] += 1
                for ____ in data3:
                    res[3] += 1

    assert res == [3, 9, 27, 81]
    assert data5.len == 5
    assert not is_cache_file_exists(data5)
    assert not is_pending_cache_file_exists(data5)


def test_new_limit_is_bigger(general_data: List[dict], cache):
    data5 = Data(general_data, cache=cache).limit(3).limit(5)
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
    assert data5.len == 3


def test_limit_for_limit_in_iterations(general_data: List[dict], cache):
    data = Data(general_data, cache=cache)
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


def test_data_loss_with_fixed_generator(general_data: List[dict]):
    def general_data_gen():
        return (item for item in general_data)

    with pytest.warns(RuntimeWarning):
        data = Data(general_data_gen())

    for _ in range(3):
        for _ in data:
            pass

    assert len(list(data)) == 0


def test_data_loss_with_new_generator(general_data: List[dict]):
    def general_data_gen():
        return (item for item in general_data)

    data = Data(general_data_gen)
    for _ in range(3):
        for _ in data:
            pass

    assert len(list(data)) == len(general_data)


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


def test_is_empty(general_data: List[dict]):
    empty_data = Data([])
    data = Data(general_data)

    assert empty_data.is_empty is True
    assert data.is_empty is False


def test_inner_cycle_with_cache(general_data: List[dict]):
    data = Data(general_data).use_cache(True)  # 21 objects
    external_counter = 0
    internal_counter = 0

    for _ in data:
        external_counter += 1
        for _ in data:
            internal_counter += 1

    assert external_counter == 21 and internal_counter == 441


def test_inner_cycle_with_cache_and_workflow(general_data: List[dict]):
    data = Data(general_data).use_cache(True)  # 21 objects
    data_filter = data.filter(lambda record: "Checkpoint" in record.get("eventType"))  # 12 objects
    external_counter = 0
    internal_counter = 0

    for _ in data:
        external_counter += 1
        for _ in data_filter:
            internal_counter += 1

    assert (
        external_counter == len(general_data)
        and internal_counter == len(general_data) * data_filter.len
    )


def test_break_cycle(general_data: List[dict]):
    data = Data(general_data).use_cache(True)  # 21 objects
    first_cycle = 0
    second_cycle = 0

    for _ in data:
        first_cycle += 1
        if first_cycle == 10:
            break
    for _ in data:
        second_cycle += 1

    assert second_cycle == 21


def test_to_json():
    data = Data([1, 2, {"3": 5, "tt": 4}, 6])
    path_result = "tests/test_files/file_to_test_to_json.txt"
    path_expected = "tests/test_files/file_to_test_to_json_expected.txt"

    data.to_json(path_result, indent=4, overwrite=True)

    with open(path_result, encoding="utf-8") as f1, open(path_expected, encoding="utf-8") as f2:
        for l1, l2 in zip(f1, f2):
            assert l1 == l2


def test_to_csv():
    data = Data([{"a": 1, "b": 2}, {"c": 3, "d": 4}])
    path_result = "tests/test_files/file_to_test_to_csv.csv"
    path_expected = "tests/test_files/file_to_test_to_csv_expected.csv"

    data.to_csv(path_result, overwrite=True)

    with open(path_result, encoding="utf-8") as f1, open(path_expected, encoding="utf-8") as f2:
        for l1, l2 in zip(f1, f2):
            assert l1 == l2


class TestDataObjectJoining:
    @classmethod
    def setup_class(cls):
        cls.d1 = Data([1, 2, 3])
        cls.d2 = Data(["a", {"id": 123}, "c"])
        cls.d3 = Data([7, 8, 9])
        cls.data_via_init = Data([cls.d1, cls.d2, cls.d3])
        cls.data_via_add = cls.d1 + cls.d2 + cls.d3
        cls.data_with_non_data_obj_via_add = cls.d1 + Data(["a", {"id": 123}, "c"]) + cls.d3
        cls.expected_dx_lst = [1, 2, 3, "a", {"id": 123}, "c", 7, 8, 9]

        # It contains Data objects with exactly the same values inside == cls.expected_dx_lst.
        cls.complex_datas_lst = [
            cls.data_via_init,
            cls.data_via_add,
            cls.data_with_non_data_obj_via_add,
        ]

    def test_iters_all_data_objects_inside(self):
        """Checks data consistency."""
        for dx in self.complex_datas_lst:
            assert list(dx) == self.expected_dx_lst

    def test_iterates_many_times(self):
        """Iterates the same data object 3 times."""
        for dx in self.complex_datas_lst:
            l1 = list(dx)
            l2 = list(dx)
            l3 = list(dx)
            assert l1 == l2 == l3

    def test_len_joined_data(self):
        for dx in self.complex_datas_lst:
            assert dx.len == len(self.expected_dx_lst)

    def test_cache(self):
        """
        dx = d1 + d2(with_cache) + d3  <- d2 cache should work
        dx.use_cache(True)  <- dx will get own cache
        """
        # dx = self.d1 + Data(['a', {'id': 123}, 'c'], cache=True) + self.d3
        d2 = Data(["a", {"id": 123}, "c"], cache=True)
        dx = self.d1 + d2 + self.d3
        iterate_data(dx, to_return=False)  # It should create d2 cache file.
        assert is_cache_file_exists(d2), "The cache was not dumped after using len"

        dx.use_cache(True)
        iterate_data(dx, to_return=False)  # It should create dx cache file.
        assert is_cache_file_exists(dx), "The cache was not dumped after using len"
