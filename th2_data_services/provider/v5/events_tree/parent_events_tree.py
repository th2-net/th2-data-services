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

from typing import Union, Iterator, Generator, Optional

from th2_data_services.data import Data
from th2_data_services.provider.v5.data_source.grpc import GRPCProvider5DataSource
from th2_data_services.provider.v5.data_source.http import HTTPProvider5DataSource
from th2_data_services.provider.v5.events_tree.events_tree import EventsTree
from th2_data_services.provider.v5.struct import provider5_event_struct


class ParentEventsTree(EventsTree):
    """
    ParentEventsTree is a class (like an EventsTree).

    ParentEventsTree contains all parent events inside.
    """

    def __init__(
        self,
        data: Union[Iterator, Generator[dict, None, None], Data] = None,
        data_source: Union[GRPCProvider5DataSource, HTTPProvider5DataSource] = None,
        event_struct=provider5_event_struct,
        preserve_body: Optional[bool] = False,
    ):
        """
        Args:
            data: Events.
            data_source: Data Source.
            event_struct: Event Struct.
            preserve_body ('bool', optional): If true keep events bodies.
        """
        self._parents_ids = set()
        super().__init__(
            data=data,
            preserve_body=preserve_body,
            data_source=data_source,
            event_struct=event_struct,
        )

    @property
    def events(self) -> dict:
        return self._events

    def clear_events(self) -> None:
        """Clear exist events."""
        self._events.clear()

    @property
    def unknown_events(self):
        return self._unknown_events

    def clear_unknown_events(self) -> None:
        """Clear unknown events."""
        self._unknown_events.clear()

    def build_tree(self, data: Union[Iterator, Generator[dict, None, None]]) -> None:
        """Build parent events tree.

        :param data: Events.
        """
        for event in data:
            parent_id = event.get(self._event_struct.PARENT_EVENT_ID)
            if parent_id is not None:
                self._parents_ids.add(parent_id)
            else:
                event_id = event.get(self._event_struct.EVENT_ID)
                self._parents_ids.add(event_id)
            self.append_element(event)

        self.search_unknown_parents()

    def append_element(self, event: dict) -> None:
        """Append new parent event to events tree.

        Args:
            event: Event
        """
        event_id = event[self._event_struct.EVENT_ID]
        if not self._preserve_body:
            try:
                event.pop(self._event_struct.BODY)
            except KeyError:
                pass

        if event_id in self._parents_ids:
            self._events[event_id] = event

        if event_id in self._unknown_events:
            self._unknown_events.pop(event_id)

    def search_unknown_parents(self) -> dict:
        """Searches unknown events.

        Returns:
             dict: Unknown events.
        """
        self.clear_unknown_events()
        for parent_id in self._parents_ids:
            if parent_id not in self.events.keys():
                self._unknown_events[parent_id] += 1
        return self._unknown_events
