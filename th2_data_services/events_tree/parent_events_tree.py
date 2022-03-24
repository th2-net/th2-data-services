from collections import defaultdict
from typing import Union, Iterator, Generator, Optional

from th2_data_services.data import Data
from th2_data_services.events_tree import EventsTree


class ParentEventsTree(EventsTree):
    """
    ParentEventsTree is a class (like an EventsTree).

    ParentEventsTree contains all parent events inside.
    """

    def __init__(self, data: Union[Iterator, Generator[dict, None, None], Data] = None, preserve_body: Optional[bool] = False):

        """
        Args:
            data: Events.
            preserve_body (:obj:`bool`, optional): if true keep events bodies.
        """
        if data is None:
            data = []

        self.__preserve_body = preserve_body
        self._parents_ids = set()
        self._unknown_events = defaultdict(lambda: 0)
        self._events = {}
        self.build_tree(data)

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
            parent_id = event["parentEventId"]
            if parent_id is not None:
                self._parents_ids.add(parent_id)

        for event in data:
            self.append_element(event)
        self.search_unknown_parents()

    def append_element(self, event: dict) -> None:
        """Append new parent event to events tree.

        Args:
            event: Event
        """
        event_id = event["eventId"]
        if not self.__preserve_body:
            try:
                event.pop("body")
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
