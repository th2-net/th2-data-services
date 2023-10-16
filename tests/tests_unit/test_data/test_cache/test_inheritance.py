from typing import List

import pytest

from tests.tests_unit.utils import (
    is_cache_file_exists,
    iterate_data_and_do_cache_checks,
    double_generator,
)

from th2_data_services.data import Data


def test_parent_cache_was_created(log_checker, general_data: List[dict]):
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
    # log_checker.cache_file_created(data)

    # [2]
    data = Data(general_data, cache=True)
    data1 = data.filter(lambda record: record.get("isBatched"))
    data2 = data1.map(lambda record: {**record, "batch_status": record.get("isBatched")})
    data2.use_cache(True)
    list(data2)  # Just to iterate and create cache files.
    assert is_cache_file_exists(data)
    assert is_cache_file_exists(data2)
    # log_checker.cache_file_created(data)
    # log_checker.cache_file_created(data2)


def test_data_iterates_parent_cache_file(log_checker, general_data: List[dict]):
    """D(cache) -> D1(filter) -> D2(map + cache) -> D3(filter) -> D4(map) - creates D and D2 cache files.
    There are 2 cache files, it should iterate D2 cache file.
    """

    def add_batch_status_to_dict_generator(stream):
        for record in stream:
            yield {**record, "batch-status": record.get("isBatched")}

    data = Data(general_data, cache=True)
    data1 = data.filter(lambda record: record.get("isBatched"))
    data2 = data1.map(lambda record: {**record, "batch_status": record.get("isBatched")})
    data2.use_cache(True)
    iterate_data_and_do_cache_checks(data2, log_checker)  # Just to iterate and create cache files.
    # log_checker.cache_file_created(data)

    data3 = data2.filter(lambda record: record.get("eventType"))
    data4 = data3.map_stream(double_generator)

    # Change D and D2 sources to [] to be aware data iterates cache file.
    data._data_stream = ["D"]
    data2._data_stream = ["D2"]
    assert len(list(data4)) == len(list(data3)) * 2
    # log_checker.used_own_cache_file(data2)


@pytest.mark.xfail(reason="New methods return partial object which blocks knowing parent.")
def test_cache_linear_inheritance(general_data: List[dict]):
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
