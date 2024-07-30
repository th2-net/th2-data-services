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

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Sequence

from th2_data_services.interfaces import IEventStruct, IDataSource

Th2EventType = TypeVar("Th2EventType")


class IETCDriver(ABC, Generic[Th2EventType]):
    def __init__(
        self,
        event_struct: IEventStruct,
        data_source: IDataSource,
        use_stub: bool = False,
    ):
        """The driver for EventsTreeCollection and its inheritors.

        Args:
            event_struct: Structure of the event.
            data_source: DataSource object.
            use_stub: Build stubs or not.
        """
        self.event_struct = event_struct
        self.use_stub = use_stub
        self._data_source = data_source

    @abstractmethod
    def build_stub_event(self, id_: str) -> Th2EventType:
        """Builds stub event to generate parentless trees.

        Args:
            id_: Event Id.
        """

    @abstractmethod
    def get_parent_event_id(self, event: Th2EventType):
        """Returns parent event id from the event."""

    @abstractmethod
    def get_event_id(self, event: Th2EventType):
        """Returns event id from the event."""

    @abstractmethod
    def get_event_name(self, event: Th2EventType):
        """Returns event name from the event."""

    @abstractmethod
    def get_events_by_id_from_source(self, ids: Sequence) -> list:
        """Downloads the list of events from the provided data_source."""

    @abstractmethod
    def stub_event_name(self):
        """Returns stub event name."""
