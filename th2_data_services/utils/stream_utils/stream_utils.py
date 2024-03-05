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
from th2_data_services.utils._is_sorted_result import IsSortedResult


def is_sorted(obj: Iterable, get_timestamp_func: Callable[[Any], Any]) -> IsSortedResult:
    """Checks whether stream is sorted.

    Args:
        obj: Stream
        get_timestamp_func: This function is responsible for getting the timestamp.

    Returns:
        IsSortedResult: Whether stream is sorted and additional info (e.g. index of the first unsorted element).
    """
    is_sorted_result = IsSortedResult()
    flag = True
    previous_timestamp = None
    i = 0
    for record in obj:
        if flag:
            previous_timestamp = get_timestamp_func(record)
            flag = False
        current_timestamp = get_timestamp_func(record)
        if previous_timestamp > current_timestamp:
            is_sorted_result.status = False
            is_sorted_result.first_unsorted = i
            break
        previous_timestamp = current_timestamp
        i += 1

    return is_sorted_result
