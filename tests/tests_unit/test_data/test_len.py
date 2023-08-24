import pathlib
from typing import List

from tests.tests_unit.utils import (
    is_cache_file_exists,
    is_pending_cache_file_exists,
)

from th2_data_services.data import Data
import pytest


def test_len_with_stream_cache(general_data: List[dict], cache=True):
    # From empty list
    data = Data(general_data, cache=cache)
    elements_num = len(general_data)
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
        assert not is_pending_cache_file_exists(
            data
        ), f"The cache was dumped after using len: {cache}"

    # TODO - Check that we do not calc len, after already calculated len or after iter


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


@pytest.mark.xfail(
    reason="TH2-4930 - known issue. Should be fixed in 2.0.0. "
    "The new feature Data.from_csv was really needed, so we OK with the issue."
)
def test_len_after_reading_file():
    # Any file: cache, json, csv
    path = pathlib.Path("tests/test_files/file_to_read_by_data.csv")
    data = Data.from_csv(path)

    assert list(data.limit(1)) == ["A", "B", "Two Words"]
