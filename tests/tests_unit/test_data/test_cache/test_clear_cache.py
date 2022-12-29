from typing import List

from tests.tests_unit.utils import iterate_data_and_do_cache_checks, is_cache_file_exists, iterate_data
from th2_data_services.data import Data


def test_cache_file_removed(general_data: List[dict]):
    """
    Check that Tmp cache file is removed.
    """
    data = Data(general_data, cache=True)
    iterate_data_and_do_cache_checks(data)
    data.clear_cache()

    assert not is_cache_file_exists(data)


def test_cache_file_removed_but_data_object_iterates(general_data: List[dict]):
    """
    Check that second iteration the same data object works after cache clearing.
    """
    data = Data(general_data, cache=True)
    r = iterate_data(data)
    data.clear_cache()
    data += Data([1, 2, 3])
    res = r + [1, 2, 3]

    assert list(data) == res
    assert is_cache_file_exists(data)
