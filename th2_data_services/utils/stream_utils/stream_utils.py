#  Copyright 2024 Exactpro (Exactpro Systems Limited)
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

from typing import Iterable, Callable, Any


def is_sorted(obj: Iterable, get_timestamp_func: Callable[[Any], dict]) -> bool:
    """Checks whether stream is sorted.

    Args:
        obj: Stream
        get_timestamp_func: This function is responsible for getting the timestamp.

    Returns:
        bool
    """
    flag = True
    previous_timestamp = None
    for record in obj:
        if flag:
            previous_timestamp = get_timestamp_func(record)
            flag = False
        current_timestamp = get_timestamp_func(record)
        if previous_timestamp["epochSecond"] > current_timestamp["epochSecond"] or (
            previous_timestamp["epochSecond"] == current_timestamp["epochSecond"]
            and previous_timestamp["nano"] > current_timestamp["nano"]
        ):
            return False
        previous_timestamp = current_timestamp

    return True
