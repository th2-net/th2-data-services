import os
from typing import List

from tests.tests_unit.utils import (
    is_cache_file_exists,
    iterate_data_and_do_checks,
    iterate_data,
    is_pending_cache_file_exists,
)

from th2_data_services.data import Data
import pytest


def map_read_failure(e):
    if e != 1:
        return e["a"]


def map_keyboard_interrupt(e):
    if e != 1:
        raise KeyboardInterrupt


def new_data_with_limit2(data: Data) -> Data:
    return data.limit(2)


def new_data_with_map_keyboard_interrupt(data: Data) -> Data:
    return data.map(map_keyboard_interrupt)


##########
# TESTS
##########


EXTERNAL_CACHE_FILE = "external_cache_file"


def test_data_iterates_own_cache_file(log_checker, general_data: List[dict]):
    data = Data(general_data, cache=True)
    output1: List = iterate_data_and_do_checks(data, log_checker)  # It'll create a cache file.

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


def test_data_iterates_own_external_cache_file(log_checker, general_data: List[dict]):
    data = Data.from_cache_file(EXTERNAL_CACHE_FILE)
    output1: List = list(data)

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
def test_cache_file_isnt_created_after_using_magic_function(general_data: List[dict], magic_func):
    """Checks that Data object successfully iterates after using of magic functions.

    Data object shouldn't create cache file after using these functions.
    Otherwise, it will consume data from incomplete cache.
    """
    data = Data(general_data, cache=True)
    magic_func(data)  # It shouldn't create cache file.
    output = list(data)
    assert output == general_data


def test_data_doesnt_left_their_cache_file_if_you_change_dir(log_checker):
    """Issue related test: https://exactpro.atlassian.net/browse/TH2-3545"""
    data = Data([1, 2, 3], cache=True)
    dl = iterate_data_and_do_checks(data, log_checker)

    cwd = os.getcwd()
    os.chdir("/")
    data._data_stream = []
    assert list(data) == dl
    log_checker.used_own_cache_file(data)
    os.chdir(cwd)


def test_data_doesnt_left_their_cache_file_if_you_change_dir_external_cache(log_checker):
    """Issue related test: https://exactpro.atlassian.net/browse/TH2-3545"""
    data = Data.from_cache_file(EXTERNAL_CACHE_FILE)
    dl: List = list(data)

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
def test_cache_file_will_be_removed_only_if_data_write_it(interactive_mod, expected_exception, map_func):
    """If Data obj reads the cache file and something went wrong
        1. We have to delete it in the script mode
        2. We DO NOT have to delete it in the interactive mode
        3. We DO NOT have to delete file if we read the file using special method.

    Issue related test: https://exactpro.atlassian.net/browse/TH2-3546"""
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
    ["expected_exception", "map_func"],
    [
        (KeyError, map_read_failure),
        (KeyboardInterrupt, map_keyboard_interrupt),
    ],
)
def test_cache_file_wont_remove_external_cache(interactive_mod, expected_exception, map_func):
    # Read test for external cache
    data = Data.from_cache_file(EXTERNAL_CACHE_FILE)
    list(data)  # It'll create a cache file.
    with pytest.raises(expected_exception):
        list(data.map(map_func))

    assert is_cache_file_exists(
        data
    ), "Cache file should be exist if Data object just read it from external cache file."


@pytest.mark.parametrize(
    ["change_type"],
    [
        (new_data_with_limit2,),
    ],
)
def test_tmp_cache_will_be_deleted_if_not_fully_recorded(change_type):
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
