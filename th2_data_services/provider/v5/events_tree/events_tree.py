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
from collections import defaultdict
from typing import Callable, Generator, Iterator, Optional, Union

from th2_data_services import Data
from th2_data_services.et_interface import IEventsTree
from th2_data_services.provider.v5.command_resolver import resolver_get_events_by_id
from th2_data_services.provider.v5.data_source.grpc import GRPCProvider5DataSource
from th2_data_services.provider.v5.data_source.http import HTTPProvider5DataSource
from th2_data_services.provider.v5.struct import provider5_event_struct, Provider5EventStruct


class EventsTree(IEventsTree):
    """EventsTree - is a useful wrapper for your retrieved data.

    EventsTree - is not a tree in the literal sense.
    It is an object with a dict 'events' inside which contains
    events without their body.

    EventTree contains all events inside, so it takes
    ~2.5Gb for 1 million events.

    Take a look at the following HTML tree to understand some important terms.

        <body> <!-- ancestor (grandparent), but not parent -->
            <div> <!-- parent & ancestor -->
                <p>Hello, world!</p> <!-- child -->
                <p>Goodbye!</p> <!-- sibling -->
            </div>
        </body>
    """

    def __init__(
        self,
        data: Union[Iterator, Generator[dict, None, None], Data] = None,
        data_source: Union[GRPCProvider5DataSource, HTTPProvider5DataSource] = None,
        event_struct: Provider5EventStruct = provider5_event_struct,
        preserve_body: Optional[bool] = False,
    ):
        """
        Args:
            data: Events.
            data_source: Data Source.
            event_struct: Event Struct.
            preserve_body ('bool', optional): If true keep events bodies.
        """
        if data is None:
            data = []

        self._preserve_body = preserve_body
        self._data_source = data_source
        self._event_struct = event_struct

        self._events = {}  # {EventID_str: Event_dict}
        self._unknown_events = defaultdict(lambda: 0)  # {parent_id: int(cnt)}
        self.build_tree(data)

    @property
    def events(self) -> dict:
        return self._events

    @property
    def unknown_events(self):
        return self._unknown_events

    def clear_events(self) -> None:
        """Clear exist events."""
        self._events = {}

    def clear_unknown_events(self) -> None:
        """Clear unknown events."""
        self._unknown_events.clear()

    def build_tree(self, data: Union[Iterator, Generator[dict, None, None]]) -> None:
        """Build or append new events to family tree.

        Args:
            data: Events.
        """
        for event in data:
            event = event.copy()
            self.append_element(event)
        self.search_unknown_parents()

    def append_element(self, event: dict) -> None:
        """Append new event to events tree.

        Will update the event if event_id matches.
        Will remove the event from unknown_events if it in unknown_events dict.

        Args:
            event: Event
        """
        event_id_field = self._event_struct.EVENT_ID
        event_id = event[event_id_field]
        if not self._preserve_body:
            try:
                event.pop(self._event_struct.BODY)
            except KeyError:
                pass

        self._events[event_id] = event

        event_id = event[event_id_field]
        if event_id in self._unknown_events:
            self._unknown_events.pop(event_id)

    def search_unknown_parents(self) -> dict:
        """Searches unknown events.

        Returns:
             dict: Unknown events.
        """
        parent_event_id_field = self._event_struct.PARENT_EVENT_ID

        self.clear_unknown_events()
        event: dict
        for event in self.events.values():
            parent_id = event.get(parent_event_id_field)
            if parent_id is not None:
                if parent_id == "Broken_Event":
                    continue
                if parent_id not in self._events:
                    parent_id = event[parent_event_id_field]
                    self._unknown_events[parent_id] += 1

        return self._unknown_events

    def is_ancestor_by_condition(self, event: dict, check_function: Callable) -> bool:
        """Checks that events ancestor passed condition.

        Args:
            event: Event.
            check_function: Condition function.

        Returns:
            True if condition is passed.
        """
        parents_event_id_field = self._event_struct.PARENT_EVENT_ID

        parent_id = event.get(parents_event_id_field)
        if parent_id is None:
            return False

        ancestor = self._events.get(parent_id)
        while ancestor:
            if check_function(ancestor):
                return True
            ancestor = self._events.get(ancestor.get(parents_event_id_field))
        return False

    def get_ancestor_by_condition(self, event: dict, condition_function: Callable) -> Optional[dict]:
        """Gets event ancestor by condition.

        Args:
            event: Event.
            condition_function: Condition function.

        Returns:
            Ancestor event If condition is True.
        """
        parents_event_id_field = self._event_struct.PARENT_EVENT_ID

        parent_id = event.get(parents_event_id_field)
        if parent_id is None:
            return None

        ancestor = self._events.get(parent_id)
        while ancestor:
            if condition_function(ancestor):
                return ancestor
            ancestor = self._events.get(ancestor.get(parents_event_id_field))
        return ancestor

    def recover_unknown_events(self, stub: Optional[bool] = False) -> None:
        """Loads unknown events from data provider and recover EventsTree.

        Args:
            stub: True If you need handle broken events.
        """
        command_get_events_by_id = resolver_get_events_by_id(self._data_source)

        old_unknown_events = self._unknown_events.keys()
        while self._unknown_events:
            instance_command = command_get_events_by_id(self._unknown_events.keys())
            if stub:
                instance_command = command_get_events_by_id.use_stub()

            new_events = self._data_source.command(instance_command)
            if isinstance(new_events, dict):
                new_events = [new_events]
            if new_events is None:
                new_events = []
            self.build_tree(new_events)
            if self._unknown_events == old_unknown_events:
                break
            old_unknown_events = self._unknown_events.copy()

    def get_children(self, parent_event_id) -> list:
        parent_event_id_field = self._event_struct.PARENT_EVENT_ID
        return [e for e in self._events.values() if e[parent_event_id_field] == parent_event_id]
