from pathlib import Path
from typing import List
from th2_data_services.data import Data
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
