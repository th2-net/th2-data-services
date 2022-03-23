#  Copyright 2022 Exactpro (Exactpro Systems Limited)
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
    def __init__(self, id_):
        """Exception for the case when the the event was not found in data source.

        Args:
            id_: Event id.
        """
        self._id = id_

    def __str__(self):
        return f"Unable to find the event with id '{self._id}'"


class MessageNotFound(Exception):
    def __init__(self, id_):
        """Exception for the case when the the message was not found in data source.

        Args:
            id_: Event id.
        """
        self._id = id_

    def __str__(self):
        return f"Unable to find the message with id '{self._id}'"


class CommandError(Exception):
    """Exception raised for errors in the command."""
