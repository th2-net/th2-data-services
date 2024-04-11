from pathlib import Path

import pytest

from th2_data_services.utils.path_utils import check_if_file_exists


def test_check_if_file_exists_takes_str_filepath():
    with pytest.raises(FileNotFoundError):
        check_if_file_exists(filename="no_such_file.xxx")


def test_check_if_file_exists_takes_path_filepath():
    with pytest.raises(FileNotFoundError):
        check_if_file_exists(filename=Path("no_such_file.xxx"))
