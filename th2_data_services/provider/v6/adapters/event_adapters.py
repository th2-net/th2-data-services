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
from typing import Optional

from th2_data_services.interfaces.adapter import IEventAdapter
from th2_data_services.provider.v6.struct import HTTPProvider6EventStruct, http_provider6_event_struct


class DeleteEventWrappersAdapter(IEventAdapter):
    """Adapter that deletes unnecessary wrappers in events.

    It used for events to which an AdaptorGRPCObjectToDict has been applied.
    """

    def __init__(self, event_struct: HTTPProvider6EventStruct = http_provider6_event_struct):
        """AdapterDeleteEventWrappers constructor.

        Args:
            event_struct: Event struct.
        """
        self._event_struct = event_struct

    def handle(self, event: dict) -> dict:
        """Deletes unnecessary wrappers for fields eventId, parentEventId and BatchId.

        Args:
            event: Event.

        Returns:
            Event without wrappers.
        """
        event_id_field = self._event_struct.EVENT_ID
        parent_event_id_field = self._event_struct.PARENT_EVENT_ID
        batch_id_field = self._event_struct.BATCH_ID

        event_id = self.__get_id_from_wrapper(event, event_id_field)
        parent_event_id = self.__get_id_from_wrapper(event, parent_event_id_field)
        batch_id = self.__get_id_from_wrapper(event, batch_id_field)

        if event_id:
            event[event_id_field] = event_id
        if parent_event_id:
            event[parent_event_id_field] = parent_event_id
        if batch_id:
            event[batch_id_field] = batch_id

        return event

    @staticmethod
    def __get_id_from_wrapper(event: dict, field: str):
        """Opens the wrapper and getting the id."""
        wrapper: dict = event.get(field)
        if wrapper:
            return wrapper["id"]
        return None


class DeleteSystemEvents(IEventAdapter):
    """Adapter that deletes unnecessary system events."""

    def handle(self, event: dict) -> Optional[dict]:
        """Deletes unnecessary system events.

        System events have form '{'hasEnded': bool, 'hasStarted': bool, 'lastId': bool}'
        """
        if event.get("hasEnded") or event.get("hasStarted") or event.get("lastId"):
            return None
        return event
