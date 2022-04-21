import os
from typing import List

from tests.utils import is_cache_file_exists, iterate_data_and_do_checks, iterate_data, is_pending_cache_file_exists
from th2_data_services.th2_gui_report import Th2GUIReport
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


def test_limit_before_loops(cache):
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

    assert res5 == [limit, limit ** 2, limit ** 3, limit ** 4]
    assert not is_cache_file_exists(data)
    assert not is_pending_cache_file_exists(data)
    assert data.len == len(data_stream)  # It'll creates cache.


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


def map_read_failure(e):
    if e != 1:
        return e["a"]


def map_keyboard_interrupt(e):
    if e != 1:
        raise KeyboardInterrupt


@pytest.fixture(params=[True, False])
def interactive_mod(request):
    """INTERACTIVE_MODE or script mod"""
    INTERACTIVE_MODE = request.param
    return INTERACTIVE_MODE


def new_data_with_limit2(data: Data) -> Data:
    return data.limit(2)


def new_data_with_map_keyboard_interrupt(data: Data) -> Data:
    return data.map(map_keyboard_interrupt)


class TestDataCache:
    def test_data_iterates_own_cache_file(self, log_checker, general_data: List[dict]):
        data = Data(general_data, cache=True)
        output1 = iterate_data_and_do_checks(data, log_checker)  # It'll create a cache file.

        # Deactivate cache and set empty data source.
        data.use_cache(False)
        data._data_stream = []
        output2 = list(data)
        assert output2 == []

        # Activate cache to check that data iterate cache file.
        data.use_cache(True)
        output3 = list(data)
        assert output1 == output3
        log_checker.used_own_cache_file(data)

    @pytest.mark.parametrize("magic_func", [bool, str])
    def test_cache_file_isnt_created_after_using_magic_function(self, general_data: List[dict], magic_func):
        """Checks that Data object successfully iterates after using of magic functions.

        Data object shouldn't create cache file after using these functions.
        Otherwise it will consume data from incomplete cache.
        """
        data = Data(general_data, cache=True)
        magic_func(data)  # It shouldn't create cache file.
        output = list(data)
        assert output == general_data

    def test_data_doesnt_left_their_cache_file_if_you_change_dir(self, log_checker):
        """Issue related test: https://exactpro.atlassian.net/browse/TH2-3545"""
        data = Data([1, 2, 3], cache=True)
        dl = iterate_data_and_do_checks(data, log_checker)

        cwd = os.getcwd()
        os.chdir("/")
        data._data_stream = []
        assert list(data) == dl
        log_checker.used_own_cache_file(data)
        os.chdir(cwd)

    @pytest.mark.parametrize(
        ["expected_exception", "map_func"],
        [
            (TypeError, map_read_failure),
            (KeyboardInterrupt, map_keyboard_interrupt),
        ],
    )
    def test_cache_file_will_be_removed_only_if_data_write_it(self, interactive_mod, expected_exception, map_func):
        """Issue related test: https://exactpro.atlassian.net/browse/TH2-3546"""
        import th2_data_services

        th2_data_services.INTERACTIVE_MODE = interactive_mod

        # Write test
        data = Data([1, 2, 3, 4, 5], cache=True).map(map_func)
        with pytest.raises(expected_exception):
            list(data)
        assert not is_cache_file_exists(data), "Cache file exists despite data object wrote it."
        assert not is_pending_cache_file_exists(data), "Cache file exists despite data object wrote it."

        # Read test
        data = Data([1, 2, 3, 4, 5], cache=True)
        list(data)  # It'll create a cache file.
        with pytest.raises(expected_exception):
            list(data.map(map_func))
        if expected_exception is TypeError:
            if interactive_mod:
                assert is_cache_file_exists(
                    data
                ), "Cache file should be exist if Data object just read it in interactive_mod."
            # else:
            # It's expected that cache should be deleted if it's SCRIPT MODE but `del data` doesn't work for testing
            #     cache_filepath = data.get_cache_filepath()
            #     del data
            #     time.sleep(2)
            #     assert not cache_filepath.is_file()
        elif expected_exception is KeyboardInterrupt:
            if interactive_mod:
                assert is_cache_file_exists(
                    data
                ), "Cache file should be exist if Data object just read it in interactive_mod."
            # else:
            # It's expected that cache should be deleted if it's SCRIPT MODE but `del data` doesn't work for testing
            #     cache_filepath = data.get_cache_filepath()
            #     del data
            #     assert not cache_filepath.is_file()

    @pytest.mark.parametrize(
        ["change_type"],
        [
            (new_data_with_limit2,),
        ],
    )
    def test_tmp_cache_will_be_deleted_if_not_fully_recorded(self, change_type):
        # Cache has parent
        data = Data([1, 2, 3], cache=True)
        data2 = change_type(data)
        iterate_data(data2, to_return=False)
        assert not is_pending_cache_file_exists(data)

        # Cache has data itself
        data = Data([1, 2, 3])
        data2 = change_type(data).use_cache()
        iterate_data(data2, to_return=False)
        assert not is_pending_cache_file_exists(data2)

    class TestCacheInheritance:
        def test_parent_cache_was_created(self, log_checker, general_data: List[dict]):
            """
            Issue related test: https://exactpro.atlassian.net/browse/TH2-3557

            Cases:
                [1] D(cache) -> D1(filter) -> D2(map) - creates D cache when you iterate D2.
                [2] D(cache) -> D1(filter) -> D2(map + cache) - creates D and D2 cache files
            """
            # [1]
            data = Data(general_data, cache=True)
            data1 = data.filter(lambda record: record.get("isBatched"))
            data2 = data1.map(lambda record: {**record, "batch_status": record.get("isBatched")})
            list(data2)  # Just to iterate and create D cache file.
            assert is_cache_file_exists(data)
            log_checker.cache_file_created(data)

            # [2]
            data = Data(general_data, cache=True)
            data1 = data.filter(lambda record: record.get("isBatched"))
            data2 = data1.map(lambda record: {**record, "batch_status": record.get("isBatched")})
            data2.use_cache(True)
            list(data2)  # Just to iterate and create cache files.
            assert is_cache_file_exists(data)
            assert is_cache_file_exists(data2)
            log_checker.cache_file_created(data)
            log_checker.cache_file_created(data2)

        def test_data_iterates_parent_cache_file(self, log_checker, general_data: List[dict]):
            """D(cache) -> D1(filter) -> D2(map + cache) -> D3(filter) -> D4(map) - creates D and D2 cache files.
            There are 2 cache files, it should iterate D2 cache file.
            """
            data = Data(general_data, cache=True)
            data1 = data.filter(lambda record: record.get("isBatched"))
            data2 = data1.map(lambda record: {**record, "batch_status": record.get("isBatched")})
            data2.use_cache(True)
            iterate_data_and_do_checks(data2, log_checker)  # Just to iterate and create cache files.
            log_checker.cache_file_created(data)

            data3 = data2.filter(lambda record: record.get("eventType"))
            data4 = data3.map(lambda record: (record, record))

            # Change D and D2 sources to [] to be aware data iterates cache file.
            data._data_stream = ["D"]
            data2._data_stream = ["D2"]
            assert len(list(data4)) == len(list(data3)) * 2
            log_checker.used_own_cache_file(data2)

        def test_cache_linear_inheritance(self, general_data: List[dict]):
            """Cache file should be created for the first data object.

            Issue related test: https://exactpro.atlassian.net/browse/TH2-3487
            """
            data = (
                Data(general_data, cache=True)
                .filter(lambda record: record.get("isBatched"))
                .map(lambda record: {**record, "batch_status": record.get("isBatched")})
            )
            list(data)  # Just to iterate and create cache files.
            assert is_cache_file_exists(data._data_stream._data_stream)


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


###################
# TEST LEN
###################


def test_len_with_stream_cache(general_data: List[dict], cache):
    # From empty list
    data = Data(general_data, cache=cache)
    elements_num = len(list(data))
    assert data.len == elements_num
    assert data.limit(10).len == 10

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
        assert is_cache_file_exists(data), f"The cache was dumped after using len: {cache}"
    else:
        assert not is_cache_file_exists(data), f"The cache was dumped after using len: {cache}"
        assert not is_pending_cache_file_exists(data), f"The cache was dumped after using len: {cache}"

    # Check that we do not calc len, after already calculated len or after iter
    # TODO - append when we add logging


def test_len_has_correct_value_after_multiple_loop_iteration(cache):
    stream = [1, 2, 3]
    data = Data(stream, cache=cache)

    for a in data:
        for b in data:
            for c in data:
                pass

    assert data.len == len(stream)


@pytest.mark.parametrize(
    ["limit2", "limit3", "exp_data2", "exp_data3", "exp_data"],
    # Data.limit(A).limit(B)
    [
        # A == B
        pytest.param(1, 1, 1, 1, None, marks=pytest.mark.xfail(reason="Low priority issue")),
        (1, 1, None, 1, None),  # Issue, but it checks that data3 has correct value
        (2, 2, None, 2, None),  # Issue
        pytest.param(5, 5, 5, 5, 5, marks=pytest.mark.xfail(reason="Low priority issue")),
        (5, 5, None, 5, None),  # Issue, but it checks that data3 has correct value
        (10, 8, 5, 5, 5),  # Higher than data_stream len == 5
        # A > B
        (3, 2, None, 2, None),  # data2 should be None because it's not fully iterated.
        (5, 2, None, 2, None),
        (10, 2, None, 2, None),
        (10, 6, 5, 5, 5),  # data3 == 5 because data_stream len == 5
        # A < B
        (1, 2, 1, 1, None),
        (1, 10, 1, 1, None),
    ],
)
def test_len_will_be_saved_if_limit_used(cache, limit2, limit3, exp_data3, exp_data2, exp_data):
    data_stream = [1, 2, 3, 4, 5]
    data = Data(data_stream, cache)
    data2 = data.limit(limit2)
    data3 = data2.limit(limit3)
    list(data3)  # Just to iterate.
    assert data3._len == exp_data3
    assert data2._len == exp_data2
    assert data._len == exp_data


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
    data = Data(general_data)  # 21 objects
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
