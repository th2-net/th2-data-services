from pathlib import Path
from typing import List
from th2_data_services.data import Data
import pytest


@pytest.mark.parametrize(
    ["cache_file"],
    [
        ("my_cache_file",),
        ("dir_for_test/file_path",),
    ],
)
def test_build_cache_file_created(general_data: List[dict], cache_file):
    """Check that file have been created.

    Check for
        - filename
        - filepath
    """
    data = Data(general_data, cache=True)

    path_obj_filename = Path(cache_file).resolve()
    data.build_cache(cache_file)

    # Requested cache file have been created.
    assert path_obj_filename.is_file(), "Cache file haven't been created"
    path_obj_filename.unlink()
