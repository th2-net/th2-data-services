#  Copyright 2022-2024 Exactpro (Exactpro Systems Limited)
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


class EventNotFound(Exception):
    def __init__(self, id_, error_description):
        """Exception for the case when the event was not found in data source.

        Args:
            id_: Event id.
            error_description: Description of error
        """
        self._id = id_
        self._error_description = error_description

    def __str__(self):
        return (
            f"An error occurred while trying to get event with id: {self._id}. "
            f"Description of error: {self._error_description}"
        )


class MessageNotFound(Exception):
    def __init__(self, id_, error_description):
        """Exception for the case when the message was not found in data source.

        Args:
            id_: Event id.
            error_description: Description of error
        """
        self._id = id_
        self._error_description = error_description

    def __str__(self):
        return (
            f"An error occurred while trying to get message with id: {self._id}. "
            f"Description of error: {self._error_description}"
        )


class CommandError(Exception):
    """Exception raised for errors in the command."""
