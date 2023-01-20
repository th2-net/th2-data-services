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


class EventIdNotInTree(Exception):
    def __init__(self, id_: str):
        """Exception for the case when the tree hasn't the event.

        Args:
            id_: Event id.
        """
        self._id = id_

    def __str__(self):
        return f"Event with the id '{self._id}' doesn't exist in the tree"


class FieldIsNotExist(Exception):
    def __init__(self, field_name: str):
        """Exception for the case when event as dict hasn't field.

        Args:
            field_name: Field name.
        """
        self._field_name = field_name

    def __str__(self):
        return f"Event doesn't have '{self._field_name}' field"


class EventAlreadyExist(Exception):
    def __init__(self, event_id: str):
        """Exception for the case when event already exist in tree.

        Args:
            event_id: Event id.
        """
        self._event_id = event_id

    def __str__(self):
        return f"Event with the id '{self._event_id}' already exist in tree."


class EventRootExist(Exception):
    def __init__(self, event_id: str):
        """Exception for the case when root already added in tree.

        Args:
            event_id: Event id.
        """
        self._event_id = event_id

    def __str__(self):
        return f"Event with the id '{self._event_id}' can't be added in tree. Root event already exist."


class TreeLoop(Exception):
    def __init__(self, event_id: str, parent_id: str):
        """Exception for the case when an event has link to a parent which is its descendant.

        Args:
            event_id: Event id.
            parent_id: Parent id.
        """
        self._event_id = event_id
        self._parent_id = parent_id

    def __str__(self):
        return (
            f"Event with the id '{self._event_id}' can't link to parent with id '{self._parent_id}'. "
            f"The parent is descendant."
        )
