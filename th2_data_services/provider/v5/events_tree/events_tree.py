from collections import defaultdict
from typing import Callable, Generator, Iterator, Optional, Union

from th2_data_services import Data
from th2_data_services.data_source import IDataSource
from th2_data_services.et_interface import IEventsTree
from th2_data_services.provider.v5.commands.grpc import GetEventsById
from th2_data_services.provider.v5.struct import provider5_event_struct


class EventsTree5(IEventsTree):
    def __init__(
        self,
        data: Union[Iterator, Generator[dict, None, None], Data] = None,
        data_source: IDataSource = None,
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
        event_id = event["eventId"]
        if not self._preserve_body:
            try:
                event.pop("body")
            except KeyError:
                pass

        self._events[event_id] = event

        event_id = event["eventId"]
        if event_id in self._unknown_events:
            self._unknown_events.pop(event_id)

    def search_unknown_parents(self) -> dict:
        """Searches unknown events.

        Returns:
             dict: Unknown events.
        """
        self.clear_unknown_events()
        event: dict
        for event in self.events.values():
            parent_id = event["parentEventId"]
            if parent_id is not None:
                if parent_id == "Broken_Event":
                    continue
                if parent_id not in self._events:
                    parent_id = event["parentEventId"]
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
        parent_id = event.get("parentEventId")
        if parent_id is None:
            return False

        ancestor = self._events.get(parent_id)
        while ancestor:
            if check_function:
                return True
            ancestor = self._events.get(ancestor.get("parentEventId"))
        return False

    def get_ancestor_by_condition(self, event: dict, condition_function: Callable) -> Optional[dict]:
        """Gets event ancestor by condition.

        Args:
            event: Event.
            condition_function: Condition function.

        Returns:
            Ancestor event If condition is True.
        """
        parent_id = event.get("parentEventId")
        if parent_id is None:
            return None

        ancestor = self._events.get(parent_id)
        while ancestor:
            if condition_function:
                return ancestor
            ancestor = self._events.get(ancestor.get("parentEventId"))
        return ancestor

    def recover_unknown_events(self, data_source: IDataSource, broken_events: Optional[bool] = False) -> None:
        """Loads unknown events from data provider and recover EventsTree.

        :param data_source: DataSources.
        :param broken_events: If True broken events is replaced on event stub.
        """
        old_unknown_events = self._unknown_events.keys()
        while self._unknown_events:
            command = GetEventsById(list(self._unknown_events.keys()))
            if broken_events:
                command.use_stub()
            new_events = data_source.command(command)

            if isinstance(new_events, dict):
                new_events = [new_events]
            if new_events is None:
                new_events = []
            self.build_tree(new_events)
            if self._unknown_events == old_unknown_events:
                break
            old_unknown_events = self._unknown_events.copy()

    def get_children(self, parent_event_id) -> list:
        return [e for e in self._events.values() if e["parentEventId"] == parent_event_id]
