from typing import Iterable, Optional

from treelib import Tree

from th2_data_services.interfaces.events_tree.events_tree import EventsTree
from th2_data_services.interfaces.events_tree.exceptions import FieldIsNotExist
from th2_data_services.provider.interfaces import IEventStruct
from th2_data_services.provider.v5.struct import provider5_event_struct


class EventsTreeProvider5(EventsTree):
    """EventsTree for data-provider v5."""

    def __init__(self, data: Iterable = None, tree: Tree = None, event_struct: IEventStruct = provider5_event_struct):
        """EventsTreeProvider5 constructor.

        Args:
            data: Iterable object.
            tree: Tree.
            event_struct: Event struct object.
        """
        self._event_struct = event_struct  # Should be placed before super!

        super().__init__(data, tree)

    def _get_event_name(self, event: dict) -> str:
        """Gets event name from the event.

        Returns:
            Event name.

        Raises:
            FieldIsNotExist: If the event doesn't have an 'event name' field.
        """
        try:
            return event[self._event_struct.NAME]
        except KeyError:
            raise FieldIsNotExist(self._event_struct.NAME)

    def _get_event_id(self, event: dict) -> str:
        """Gets event id from the event.

        Returns:
            Event id.

        Raises:
            FieldIsNotExist: If the event doesn't have an 'event id' field.
        """
        try:
            return event[self._event_struct.EVENT_ID]
        except KeyError:
            raise FieldIsNotExist(self._event_struct.EVENT_ID)

    def _get_parent_event_id(self, event: dict) -> Optional[str]:
        """Gets parent event id from event.

        Returns:
            Parent event id.
        """
        return event.get(self._event_struct.PARENT_EVENT_ID)
