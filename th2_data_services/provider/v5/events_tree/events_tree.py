from collections import defaultdict
from typing import Union, Iterator, Generator, Optional

from th2_data_services import Data
from th2_data_services.data_source import IDataSource
from th2_data_services.et_interface import IEventsTree
from th2_data_services.provider.v5.struct import provider5_event_struct


class EventsTree5(IEventsTree):
    def __init__(
        self,
        data: Union[Iterator, Generator[dict, None, None], Data] = None,
        data_source: IDataSource = None,
        preserve_body: Optional[bool] = False,
        event_struct=provider5_event_struct,
    ):
        """
        Args:
            data: Events.
            preserve_body (:obj:`bool`, optional): if true keep events bodies.
        """
        if data is None:
            data = []

        self.__preserve_body = preserve_body
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
        if not self.__preserve_body:
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
        super_type_get_func: Callable[[dict, Dict[int, dict]], str],
    ) -> Optional[dict]:
        """Gets event ancestor by super_type.

        :param event: Event.
        :param super_type: Super type.
        :param super_type_get_func: Super type get function.
        :return: Event.
        """
        parent_id = event.get("parentEventId")

        if parent_id is None:
            raise ValueError("event must have field 'parentEventId'")

        ancestor = self._events.get(parent_id)
        while ancestor:
            if super_type == super_type_get_func(ancestor, self._events):
                return ancestor
            parent_id = ancestor.get("parentEventId")
            ancestor = self._events.get(parent_id)
        return ancestor

    def recover_unknown_events(self, data_source: DataSource, broken_events: Optional[bool] = False) -> None:
        """Loads unknown events from data provider and recover EventsTree.

        :param data_source: DataSources.
        :param broken_events: If True broken events is replaced on event stub.
        """
        old_unknown_events = self._unknown_events.keys()
        while self._unknown_events:
            new_events = data_source.find_events_by_id_from_data_provider(self._unknown_events.keys(), broken_events)
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
