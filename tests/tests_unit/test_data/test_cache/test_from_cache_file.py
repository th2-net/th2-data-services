from pathlib import Path
from pickle import UnpicklingError
from typing import List
from th2.data_services.data import Data
import pytest


@pytest.mark.parametrize(
    ["cache_file"],
    [
        (Path().cwd() / "tests/tests_unit/test_data/test_cache/dir_for_test/external_cache_file",),
    ],
)
def test_from_cache_file(general_data: List[dict], cache_file):
    """Check that file have been created."""
    data = Data.from_cache_file(cache_file)
    print()
    assert list(data) == general_data


def test_from_cache_file_non_exist_file(general_data: List[dict]):
    """Check that the lib will raise exception."""
    cache_file = Path().cwd() / "tests/non_exist_file"
    with pytest.raises(FileNotFoundError) as ex:
        Data.from_cache_file(cache_file)


def test_from_cache_file_non_pickle_file(general_data: List[dict]):
    """Check that the lib will raise exception if unpickle file.

    Actually it will raise the Exception only during iteration.
    """
    cache_file = Path().cwd() / "tests/tests_unit/test_data/test_cache/dir_for_test/external_non_pickle_file"
    with pytest.raises(UnpicklingError) as ex:
        d = Data.from_cache_file(cache_file)
        print(d)
