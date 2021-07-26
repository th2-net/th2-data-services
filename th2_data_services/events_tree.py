from typing import Generator, Union, Iterator, Optional, Callable, Dict

from data_sources import DataSources


class EventsTree:
    def __init__(self, data: Union[Iterator, Generator[dict, None, None]] = None):
        if data is None:
            data = []

        self._events = {}
        self._unknown_events = {}
        self.build_tree(data)

    @property
    def events(self):
        return self._events

    @property
    def unknown_events(self):
        return self._unknown_events

    def clear_events(self) -> None:
        """Clear exist events."""
        self._events = {}

    def clear_unknown_events(self) -> None:
        """Clear unknown events."""
        self._unknown_events = {}

    def build_tree(self, data: Union[Iterator, Generator[dict, None, None]]) -> None:
        """Build or append new events to family tree.

        :param data: Events.
        """
        for event in data:
            self.append_element(event)
        self.search_unknown_parents()

    def append_element(self, event: dict) -> None:
        """Append new event to family tree.

        :param event: Event
        """
        event_id = event.get("eventId")

        if event.get("body"):
            event.pop("body")

        if event_id:
            if ":" in event_id:
                event_id = event_id.split(":")[1]

            self._events[event_id] = event
            if event_id in self._unknown_events:
                self._unknown_events.pop(event_id)

    def search_unknown_parents(self) -> dict:
        """Searches unknown events.

        :return: Unknown events.
        """
        self._unknown_events = {}
        for event in self.events.values():
            parent_id = event.get("parentEventId")
            if parent_id:
                if ":" in parent_id:
                    parent_id = parent_id.split(":")[1]

                if parent_id not in self._events:
                    if parent_id not in self._unknown_events:
                        self._unknown_events[parent_id] = 0
                    self._unknown_events[parent_id] += 1

        return self._unknown_events

    def is_in_ancestor_name(self, event: dict, event_name: str):
        """Verify event has ancestor with specified event name.

        :param event: Event parent id.
        :param event_name: Event name.
        :return: True/False.
        """
        parent_id = event.get("parentEventId")

        if parent_id is None:
            raise ValueError("event must have field 'parentEventId'")

        ancestor = self._events.get(parent_id)
        while ancestor:
            if event_name in ancestor.get("eventName"):
                return True
            ancestor = self._events.get(ancestor.get("parentEventId"))
        return False

    def is_in_ancestor_type(self, event: dict, event_type: str) -> bool:
        """Verify event has ancestor with specified event type.

        :param event: Event.
        :param event_type: Event type.
        :return: True/False.
        """
        parent_id = event.get("parentEventId")

        if parent_id is None:
            raise ValueError("event must have field 'parentEventId'")

        ancestor = self._events.get(parent_id)
        while ancestor:
            if event_type == ancestor.get("eventType"):
                return True
            ancestor = self._events.get(ancestor.get("parentEventId"))
        return False

    def get_ancestor_by_name(self, event: dict, event_name: str) -> Optional[dict]:
        """Gets event ancestor by event_name.

        :param event: Record.
        :param event_name: Event name.
        :return: Event.
        """
        parent_id = event.get("parentEventId")

        if parent_id is None:
            raise ValueError("event must have field 'parentEventId'")

        ancestor = self._events.get(parent_id)
        while ancestor:
            if event_name in ancestor.get("eventName"):
                return ancestor
            ancestor = self._events.get(ancestor.get("parentEventId"))
        return ancestor

    def get_ancestor_by_super_type(
        self,
        event: dict,
        super_type: str,
        get_super_type: Callable[[dict, Dict[int, dict]], str],
    ) -> Optional[dict]:
        """Gets event ancestor by super_type.

        :param event: Event.
        :param super_type: Super type.
        :param get_super_type: Super type get function.
        :return: Event.
        """
        parent_id = event.get("parentEventId")

        if parent_id is None:
            raise ValueError("event must have field 'parentEventId'")

        if parent_id and ":" in parent_id:
            parent_id = parent_id.split(":")[1]

        ancestor = self._events.get(parent_id)
        while ancestor:
            if super_type == get_super_type(ancestor, self._events):
                return ancestor
            parent_id = ancestor.get("parentEventId")
            if parent_id and ":" in parent_id:
                parent_id = parent_id.split(":")[1]
            ancestor = self._events.get(parent_id)
        return ancestor

    def recover_unknown_events(self, data_source: DataSources) -> None:
        """Loads unknown events from data provider.

        :param data_source: DataSources.
        """
        old_unknown_events = self._unknown_events.keys()
        while self._unknown_events:
            new_events = data_source.find_events_by_id_from_data_provider(
                self._unknown_events.keys()
            )
            self.build_tree(new_events)
            if self._unknown_events == old_unknown_events:
                break
            old_unknown_events = self._unknown_events
