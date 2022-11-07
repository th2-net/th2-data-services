import os
from typing import List

from tests.tests_unit.utils import (
    is_cache_file_exists,
    iterate_data,
    is_pending_cache_file_exists,
)
from th2_data_services.th2_gui_report import Th2GUIReport
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


def test_increase_records_after_similar_map(cache):
    source = [1, 2, 3]
    data = Data(source, cache=cache).map(lambda record: [record, record]).map(lambda record: [record, record, record])

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
        assert not is_cache_file_exists(data), "data shouldn't have cache because was iterated via child data object."
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

    data10 = data.limit(10)
    data5 = data10.limit(5)

    assert list(data10) == [1, 1, 2, 2, 3, 3, 4, 4, 5, 5]
    if cache:
        assert not is_cache_file_exists(data), "data shouldn't have cache because was iterated via child data object."
        assert not is_pending_cache_file_exists(
            data
        ), "data shouldn't have cache because was iterated via child data object."
    assert list(data5) == [1, 1, 2, 2, 3]


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
    """There is known Windows bug: https://exactpro.atlassian.net/browse/TH2-3767"""
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


def test_big_modification_chain(log_checker):
    d1 = Data([1, 2, 3, 4, 5]).use_cache(True)
    d2 = d1.filter(lambda x: x == 1 or x == 2)
    d3 = d2.map(lambda x: [x, x]).use_cache(True)
    d4 = d3.limit(3)
    d5 = d4.map(lambda x: [x, x])

    # It should have all "Data[d3] Iterating working data" log records (for each data object)
    assert list(d5) == [1, 1, 1, 1, 2, 2]
    # Cache files should not be written because they not iterated to the end.
    assert not is_cache_file_exists(d3)
    assert not is_cache_file_exists(d1)
    assert not is_pending_cache_file_exists(d3)
    assert not is_pending_cache_file_exists(d1)

    assert list(d4) == [1, 1, 2]
    assert list(d3) == [1, 1, 2, 2]  # It also should iterate cache file.


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

    assert external_counter == len(general_data) and internal_counter == len(general_data) * data_filter.len


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


def test_link_provider():
    link_gui1 = Th2GUIReport("host:port/th2-common/")
    link_gui2 = Th2GUIReport("host:port/th2-common")
    link_gui3 = Th2GUIReport("http://host:port/th2-common/")
    link_gui4 = Th2GUIReport("http://host:port/th2-common")
    link_gui5 = Th2GUIReport("host:port/th2-commonhttp")

    result = "http://host:port/th2-common/"

    assert (
        link_gui1._provider_link == result
        and link_gui2._provider_link == result
        and link_gui3._provider_link == result
        and link_gui4._provider_link == result
        and link_gui5._provider_link == "http://host:port/th2-commonhttp/"
    )


def test_link_gui_with_event_id():
    gui = Th2GUIReport("host:port/th2-common/")
    link_event_id1 = gui.get_event_link("fcace9a4-8fd8-11ec-98fc-038f439375a0")

    result = "http://host:port/th2-common/?eventId=fcace9a4-8fd8-11ec-98fc-038f439375a0"

    assert link_event_id1 == result


def test_link_gui_with_message_id():
    gui = Th2GUIReport("host:port/th2-common/")
    link_message_id1 = gui.get_message_link("fix01:first:1600854429908302153")

    result = "http://host:port/th2-common/?messageId=fix01:first:1600854429908302153"

    assert link_message_id1 == result


def test_cache_filename():
    data = Data([1, 2, 3, 4, 5], cache=True)
    for d in data:
        d
    assert data._cache_filename.find(":") == -1


class TestDataObjectJoining:
    @classmethod
    def setup_class(cls):
        cls.d1 = Data([1, 2, 3])
        cls.d2 = Data(["a", {"id": 123}, "c"])
        cls.d3 = Data([7, 8, 9])
        cls.data_via_init = Data([cls.d1, cls.d2, cls.d3])
        cls.data_via_add = cls.d1 + cls.d2 + cls.d3
        cls.data_with_non_data_obj_via_init = Data([cls.d1, ["a", {"id": 123}, "c"], cls.d3])
        cls.data_with_non_data_obj_via_add = cls.d1 + ["a", {"id": 123}, "c"] + cls.d3
        cls.expected_dx_lst = [1, 2, 3, "a", {"id": 123}, "c", 7, 8, 9]

        # It contains Data objects with exactly the same values inside == cls.expected_dx_lst.
        cls.complex_datas_lst = [
            cls.data_via_init,
            cls.data_via_add,
            cls.data_with_non_data_obj_via_init,
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
        assert is_cache_file_exists(d2), f"The cache was not dumped after using len"

        dx.use_cache(True)
        iterate_data(dx, to_return=False)  # It should create dx cache file.
        assert is_cache_file_exists(dx), f"The cache was not dumped after using len"
