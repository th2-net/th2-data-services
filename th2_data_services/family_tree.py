from typing import Generator, Union, Iterator, Optional


class FamilyTree:
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

    def is_in_ancestor_name(self, parent_id: str, event_name: str):
        """Verify event has ancestor with specified event name.

        :param parent_id: Event parent id.
        :param event_name: Event name.
        :return: True/False.
        """
        ancestor = self._events.get(parent_id)
        while ancestor:
            if event_name in ancestor.get("eventName"):
                return True
            ancestor = self._events.get(ancestor.get("parentEventId"))
        return False

    def is_in_ancestor_type(self, parent_id: str, event_type: str) -> bool:
        """Verify event has ancestor with specified event type.

        :param parent_id: Event parent id.
        :param event_type: Event type.
        :return: True/False.
        """
        ancestor = self._events.get(parent_id)
        while ancestor:
            if event_type == ancestor.get("eventType"):
                return True
            ancestor = self._events.get(ancestor.get("parentEventId"))
        return False

    def get_ancestor_by_name(self, parent_id: str, event_name: str) -> Optional[dict]:
        """Gets event ancestor by event_name.

        :param parent_id: Event parent id.
        :param event_name: Event name.
        :return: Event.
        """
        ancestor = self._events.get(parent_id)
        while ancestor:
            if event_name in ancestor.get("eventName"):
                return ancestor
            ancestor = self._events.get(ancestor.get("parentEventId"))
        return ancestor

    def get_ancestor_by_super_type(
        self, parent_id: str, super_type: str, get_super_type: object
    ) -> Optional[dict]:
        """Gets event ancestor by super_type.

        :param parent_id: Event parent id.
        :param super_type: Super type.
        :param get_super_type: Super type get function.
        :return: Event.
        """
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
