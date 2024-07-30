#  Copyright 2023-2024 Exactpro (Exactpro Systems Limited)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from typing import Union

from th2_data_services.config import options
from pathlib import Path
import os


def transform_filename_to_valid(filename: str) -> str:
    """Transforms filename to valid OS name.

    Args:
        filename: string filename

    Returns:
        Valid filename.

    """
    chars = set(options.FORBIDDEN_CHARACTERS_IN_FILENAME)
    res_name = ""
    for sym in filename:
        if sym in chars:
            res_sym = options.FORBIDDEN_CHARACTERS_IN_FILENAME_CHANGE_TO
        else:
            res_sym = sym

        res_name += res_sym

    return res_name[: options.MAX_PATH]


def transform_filepath_to_valid(filepath: Path) -> Path:
    """Transforms filepath to valid OS name.

    Args:
        filepath: Path object.

    Returns:
        Valid path.
    """
    path_len = len(str(filepath))
    parent_path_len = len(str(filepath.parent))

    # -2 because we also have to add '/' symbol and at least 1 symbol for filename
    if parent_path_len >= options.MAX_PATH - 2:
        raise ValueError(
            f"It's impossible to create valid path for provided one: {filepath}. "
            f"Because its parent part is longer than Max possible OS path. {parent_path_len} >= {options.MAX_PATH-2}."
        )

    max_filename_len = options.MAX_PATH - parent_path_len
    valid_filename = transform_filename_to_valid(filepath.name)[:max_filename_len]

    return filepath.parent / valid_filename


def check_if_filename_valid(filename: str):
    """Returns status and reason string.

    Args:
        filename: string.

    Returns:
        Status and reason.
    """
    # Length check.
    if len(filename) > options.MAX_PATH:
        return (
            False,
            f"Filename length is more than MAX possible one. "
            f"{len(filename)} > {options.MAX_PATH}, filename: '{filename}'",
        )

    # Forbidden chars check.
    chars = set(options.FORBIDDEN_CHARACTERS_IN_FILENAME)
    for sym in filename:
        if sym in chars:
            return False, f"Forbidden char: '{sym}', filename: '{filename}'"

    return True, ""


def check_if_file_exists(filename: Union[str, Path]):
    """Raises error if file doesn't exist.

    Args:
        filename: string.

    Raises:
        FileNotFoundError: if file doesn't exist.
        ValueError: if filename contains illegal characters.
    """
    fp = Path(filename).resolve().absolute()
    try:
        if not fp.exists():
            raise FileNotFoundError(f"{fp} doesn't exist")

        if not fp.is_file():
            raise FileExistsError(f"{fp} isn't file")
    except OSError as e:
        if os.name == "nt" and e.winerror == 123:
            illegal_characters = set([char for char in filename if char in r'\/:*?"<>|'])
            illegal_characters_str = ", ".join(illegal_characters)
            raise ValueError(
                f"Invalid file path: {fp}. "
                f"It contains illegal characters: {illegal_characters_str}"
            )
        else:
            raise e
