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


class IsSortedResult:
    """IsSortedResult is used by util methods that check whether a sequence of elements is sorted.

    The class provides some attributes that tells its user additional information about the sequence provided.
    """

    def __init__(self, status: bool = True):
        """IsSortedResult constructor.

        Args:
            status: Whether the sequence is sorted.
        """
        self._status = status
        self._first_unsorted = None

    def __bool__(self):
        return self._status

    def get_status(self) -> bool:
        return self._status

    def set_status(self, status: bool):
        self._status = status

    def get_first_unsorted(self) -> int:
        return self._first_unsorted

    def set_first_unsorted(self, first_unsorted: int):
        self._first_unsorted = first_unsorted
