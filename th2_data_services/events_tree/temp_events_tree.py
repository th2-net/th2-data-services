from typing import Union, Iterable, Generator, List, Callable, Optional


Data = Union[Iterable, Generator]
EventStruct = dict


class EventsTree:
    def __init__(self, data: Data, preserve_body: bool, event_struct: EventStruct):
        """
        Args:
            data: Data
            preserve_body: True If you need to keep events bodies.
            event_struct: Event Struct.
        """

    @property
    def events(self) -> List[dict]:
        pass

    @property
    def unknown_events(self) -> List[dict]:
        pass

    @property
    def roots(self) -> List[dict]:
        pass

    def get_children_for_event(self, event: dict) -> None:
        """Gets children for a event.

        Args:
            event: Event.
        """

    def get_parent_for_event(self, event: dict) -> None:
        """Gets parent for a event.

        Args:
            event: Event.
        """

    def build_tree(self, data: Data) -> None:
        """Builds or appends new events to events tree.

        :param data: Events.
        """

    def append_element(self, event: dict) -> None:
        """Appends new event to events tree.

        Will update the event if event_id matches.
        Will remove the event from unknown_events if it in unknown_events dict.

        Args:
            event: Event
        """

    def line_up_family_tree_by_event_id(self, event_id) -> List[dict]:
        """Lines up events as a family tree by event id.

        Args:
            event_id: Event Id
        """

    def find_by_condition(self, condition: Callable) -> dict:
        """Finds events in the tree by condition.

        Args:
            condition: Condition function.
        """

    def check_by_condition(self, condition: Callable) -> dict:
        """Checks If the tree has an event that satisfies the condition.

        Args:
            condition: Condition function.
        """

    def get_ancestor_by_condition(self, event: dict, condition: Callable) -> Optional[dict]:
        """Gets event ancestor by condition.

        Args:
            event: Event.
            condition: Condition function.
        """

    def is_ancestor_by_condition(self, event: dict, condition: Callable) -> Optional[dict]:
        """Verifies event has ancestor by condition.

        Args:
            event: Event.
            condition: Condition function.
        """

    def recover_unknown_events(self) -> None:
        """Loads unknown events and recover EventsTree parts."""

    def get_event_by_id(self, event_id: str) -> dict:
        """Gets event from Events Tree by id.

        Args:
            event_id: Event id.
        """

    def show(self) -> None:
        """Prints EventsTree as tree view.

        For example:
            Root
                |___ C01
                |    |___ C11
                |         |___ C111
                |         |___ C112
                |___ C02
                |___ C03
                |    |___ C31
        """
