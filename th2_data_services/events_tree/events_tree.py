from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Generator, Union, Iterator, Optional, Callable, Dict, List

from th2_data_services.data import Data
from th2_data_services.data_source import DataSource
from anytree import Node, RenderTree, findall


class EventsTree:
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
        self, data: Union[Iterator, Generator[dict, None, None], Data] = None, preserve_body: Optional[bool] = False
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

        :param data: Events.
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
            self.build_tree(new_events)
            if self._unknown_events == old_unknown_events:
                break
            old_unknown_events = self._unknown_events.copy()

    def get_children(self, parent_event_id) -> list:
        return [e for e in self._events.values() if e["parentEventId"] == parent_event_id]


class ITreeNodeShowFmt(ABC):
    @abstractmethod
    def __call__(self, pre, fill, node, **kwargs):
        pass


class TreeNode(Node):
    separator = " | "

    class DefaultShowFmt(ITreeNodeShowFmt):
        def __call__(self, pre, fill, node, **kwargs):
            if kwargs["show_status"]:
                status = "P" if node.data["successful"] else "F"
                return "[%s] %s%s\n" % (status, pre, node.name)
            else:
                return "%s%s\n" % (pre, node.name)

    def __str__(self):
        s = ""
        for pre, fill, node in RenderTree(self):
            status = "P" if node.data["successful"] else "F"
            s += "[%s] %s%s\n" % (status, pre, node.name)
        return s

    @property
    def full_path_name(self):
        return self.separator.join([str(node.name) for node in self.path])

    def show(self, fmt: Callable = DefaultShowFmt, failed_only=False, show_status=True, **kwargs):
        s = ""
        if not failed_only:
            for pre, fill, node in RenderTree(self):
                s += fmt(pre, fill, node, show_status, **kwargs)
        else:
            for pre, fill, node in RenderTree(self):
                if not node.data["successful"]:
                    s += fmt(pre, fill, node, show_status, **kwargs)
        return s

    def get_by_status(self, status: bool):
        return findall(self, lambda node: node.data["successful"] is status)

    def get_by_leaves_status(self, status: bool):
        return [n for n in self.leaves if n.data["successful"] is status]


class EventsTree2:
    """EventsTree2 - experimental tree."""

    def __init__(
        self,
        data: Union[Iterator, Generator[dict, None, None], Data],
        ds: DataSource,
        preserve_body: bool = False,
        broken_events: bool = False,
        parentless: bool = False,
    ):
        if data is None:
            data = []
        self.__preserve_body = preserve_body
        self._broken_events = broken_events
        self._parentless = parentless
        self._data_source = ds
        self._nodes = []
        self.roots: List[TreeNode] = []
        self.events_ids = []
        self.parent_events_ids = set()
        self.__unknown_parent_ids = set()  # Set in order to remove duplicate Event IDs.
        self.parentless_nodes = []  # TODO - нужнен параметр, который будет отвечать хотим ли мы такое
        self._last_nodes_len = -1  # Just init value.
        # Shows how many nodes were without a parent during the last iteration.

        self._build_tree(data)

    def _build_tree(self, data: Union[Iterator, Generator[dict, None, None]]) -> None:
        """Build or append new events to family tree.

        :param data: Events.
        """
        for event in data:
            event = event.copy()

            event_id = event["eventId"]
            if not self.__preserve_body:
                try:
                    event.pop("body")
                except KeyError:
                    pass

            self._nodes.append(TreeNode(name=event["eventName"], data=event))
            self.events_ids.append(event_id)
            self.parent_events_ids.add(event["parentEventId"])

        unknown_parents_ids: list = self._get_unknown_parents_ids()

        # Restore them.
        restored_events = self._get_unknown_events(unknown_parents_ids, broken_events=self._broken_events)

        for event in restored_events:
            event = event.copy()
            if not self.__preserve_body:
                try:
                    event.pop("body")
                except KeyError:
                    pass

            try:
                self._nodes.append(TreeNode(name=event["eventName"], data=event))
            except KeyError as er:
                print(er)
                print(event)

        # search roots
        node: TreeNode
        for node in self._nodes.copy():
            if node.data["parentEventId"] is None:  # TODO - parentEventId
                self.roots.append(node)
                self._nodes.remove(node)

        try:
            self._build_trees(self.roots)
        except RecursionError:
            pass  # TODO

    def _build_trees(self, roots):
        parentless_nodes_len = len(self._nodes)  # The number of nodes that are not included in any tree.
        if parentless_nodes_len != 0:
            if parentless_nodes_len != self._last_nodes_len:
                self._last_nodes_len = parentless_nodes_len
                new_roots = []
                for node in self._nodes.copy():
                    for root_node in roots:
                        if node.data["parentEventId"] == root_node.data["eventId"]:
                            node.parent = root_node
                            try:
                                self._nodes.remove(node)
                            except ValueError as er:
                                print(er)
                                print("The Exception because Duplicate Nodes in the self._nodes!")
                                print(node)
                                print(self._nodes)
                                raise
                            new_roots.append(node)
                            break
                self._build_trees(new_roots)
            else:  # It happens if some events doesn't exist in DB and self._parentless == True
                print(f"Cannot build complete EventsTree2, some nodes will be available as .parentless_nodes")
                self.parentless_nodes = self._nodes
                print(self.parentless_nodes)
        else:
            return None

    def _get_unknown_events(self, unknown_parents, broken_events) -> List[dict]:
        """Recursion function to get all unknown events."""
        if unknown_parents:
            # Populate set in order to remove duplicate Event IDs.
            self.__unknown_parent_ids.update(set(unknown_parents))

            if not broken_events:
                new_events = []
                for up_id in unknown_parents:
                    try:
                        new_events.append(self._data_source.find_events_by_id_from_data_provider(up_id, broken_events))
                    except ValueError as err:
                        owners = {[n for n in self._nodes if n.data["parentEventId"] == up_id]}
                        if self._parentless:
                            print(
                                f"Cannot find in DB event with id: {up_id}\n"
                                f"Owners: {owners}\n"
                                f"EventsTree2 will be built with parentless_nodes"
                            )
                        else:
                            print(err)
                            print(f"Cannot build EventsTree2, due to some Nodes doesn't have parents")
                            # Show Events that references to not founded Event.
                            print(f"Owners: {owners}")
                            raise
            else:
                new_events: list = self._data_source.find_events_by_id_from_data_provider(
                    unknown_parents, broken_events
                )

            unknown_parents_for_next_recursion_step = set()
            new_events = [new_events] if not isinstance(new_events, list) else new_events
            for e in new_events:
                parent_event_id = e["parentEventId"]  # TODO - parentEventId может иметь другое имя.

                if (
                    parent_event_id is not None
                    and parent_event_id != "Broken_Event"
                    and parent_event_id not in self.__unknown_parent_ids
                ):
                    unknown_parents_for_next_recursion_step.add(parent_event_id)

            new_events += self._get_unknown_events(unknown_parents_for_next_recursion_step, broken_events)

            return new_events
        else:
            return []

    def _get_unknown_parents_ids(self) -> List[str]:
        """Searches unknown events ids.

        :return: Unknown events ids.
        """
        unknown_parents_ids = []

        for parent_id in self.parent_events_ids:
            if parent_id is not None:
                if parent_id not in self.events_ids:
                    unknown_parents_ids.append(parent_id)

        return unknown_parents_ids
