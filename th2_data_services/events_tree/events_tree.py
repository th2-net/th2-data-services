from collections import defaultdict
from typing import Generator, Union, Iterator, Optional, Callable, Dict, List

from th2_data_services.data import Data
from th2_data_services.data_source import DataSource
from anytree import Node, RenderTree, findall
from abc import ABC


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

    def __init__(self, data: Union[Iterator, Generator[dict, None, None], Data] = None):
        if data is None:
            data = []

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


class TreeNode(Node):
    separator = " | "

    def __str__(self):
        s = ""
        for pre, fill, node in RenderTree(self):
            status = "P" if node.data["successful"] else "F"
            s += "[%s] %s%s\n" % (status, pre, node.name)
        return s

    # TODO - this name?
    @property
    def path_str(self):
        return self.separator.join([str(node.name) for node in self.path])

    def show(self, fmt: Callable = None, failed_only=False, show_status=True):
        if fmt is None:

            def fmt(pre, fill, node):
                if show_status:
                    status = "P" if node.data["successful"] else "F"
                    return "[%s] %s%s\n" % (status, pre, node.name)
                else:
                    return "%s%s\n" % (pre, node.name)

        s = ""
        if not failed_only:
            for pre, fill, node in RenderTree(self):
                s += fmt(pre, fill, node)
        else:
            for pre, fill, node in RenderTree(self):
                if not node.data["successful"]:
                    s += fmt(pre, fill, node)
        return s


class TreeNodeProviderEvent(TreeNode, ABC):
    def __init__(self, name, data, **kwargs):
        super().__init__(name, **kwargs)
        self._data = data

    @property
    def data(self):
        return self._data

    @property
    def event_id(self):
        return self.data[self.EVENT_ID_FIELD]

    @property
    def parent_event_id(self):
        return self.data[self.PARENT_EVENT_ID_FIELD]

    def get_by_status(self, status: bool):
        return findall(self, lambda node: node.data[self.STATUS_FIELD] is status)

    def get_by_leaves_status(self, status: bool):
        return [n for n in self.leaves if n.data[self.STATUS_FIELD] is status]


class TreeNodeProvider5Event(TreeNodeProviderEvent):
    EVENT_ID_FIELD = "eventId"
    PARENT_EVENT_ID_FIELD = "parentEventId"
    STATUS_FIELD = "successful"


class EventsTree2:
    """EventsTree2 - experimental tree."""

    def __init__(self, data: Union[Iterator, Generator[dict, None, None], Data] = None, ds=None):
        """
        Я бы, как пользователь, хотел иметь следующий доступ
            ET['id']  or et.get_by_id('id')


        Args:
            data:
            ds:
        """
        if data is None:
            data = []

        self._data = data
        self._data_source = ds
        self._all_nodes = []
        self.roots: List[TreeNodeProvider5Event] = []
        self.events = dict()  # {id: Node}
        self.events_ids = []  # Used to find unknown_parents_ids
        self.parent_events_ids = set()
        self.__unknown_parent_ids = set()
        self.parentless_nodes = []  # TODO - нужнен параметр, который будет отвечать хотим ли мы такое

        self._build_trees()

    def _create_node(self, event) -> TreeNodeProvider5Event:
        return TreeNodeProvider5Event(name=event["eventName"], data=event)

    def _append_node(self, node):
        self._all_nodes.append(node)

    def _append_events_ids(self, event_id):
        self.events_ids.append(event_id)

    def _get_events(self, with_body):
        for event in self._data:
            event = event.copy()

            if not with_body:
                try:
                    event.pop("body")
                except KeyError:
                    pass
            yield event

    def _append_events(self, node: TreeNodeProvider5Event):
        self.events[node] = node.data[""]

    def _build_trees(self, with_body=False) -> None:
        """Build or append new events to family tree.

        :param data: Events.
        """
        for event in self._get_events(with_body):
            node = self._create_node(event)
            x = node.data
            self._append_node(node)
            # self.events
            self._append_events_ids(event["eventId"])
            self.parent_events_ids.add(event["parentEventId"])

        unknown_parents_ids: list = self._get_unknown_parents_ids()

        # restore them
        restored_events = self._get_unknown_events(unknown_parents_ids, broken_events=True)

        for event in restored_events:
            event = event.copy()

            try:
                event.pop("body")
            except KeyError:
                pass

            try:
                self._all_nodes.append(TreeNode(name=event["eventName"], data=event))
            except KeyError as er:
                print(er)
                print(event)

        # search roots
        node: Node
        for node in self._all_nodes.copy():
            if node.data["parentEventId"] is None:
                self.roots.append(node)
                self._all_nodes.remove(node)

        self._last_nodes_len = -1

        try:
            self.__build_trees(self.roots)
        except RecursionError:
            pass

    def __build_trees(self, roots):
        nodes_len = len(self._all_nodes)
        if nodes_len != 0:
            if nodes_len != self._last_nodes_len:
                self._last_nodes_len = nodes_len
                new_roots = []
                for node in self._all_nodes.copy():
                    for root_node in roots:
                        if node.data["parentEventId"] == root_node.data["eventId"]:
                            node.parent = root_node
                            try:
                                self._all_nodes.remove(node)
                            except ValueError as er:
                                print(er)
                                print("The Exception because Duplicate Nodes in the self._all_nodes!")
                                print(node)
                                print(self._all_nodes)
                                raise
                            new_roots.append(node)
                            break
                self.__build_trees(new_roots)
            else:
                print(f"Cannot build EventsTree2, some nodes will be available as .parentless_nodes")
                self.parentless_nodes = self._all_nodes
                print(self.parentless_nodes)
                # raise Exception(F"Cannot build EventsTree2, due to some Nodes doesn't have parents")
        else:
            return None

    """
    Думаю куда лучше будет иметь функцию, которая позволит получить пэренты, по списку ивентов.
    """

    def _get_unknown_events(self, unknown_parents, broken_events: Optional[bool] = False):
        if unknown_parents:
            for up in unknown_parents:
                self.__unknown_parent_ids.add(up)

            # Кейс 1 - когда брокен ивентс = фолс, то нужно бросить эксепшен и сказать кто ссылается на заправшиваемый ивент
            if broken_events:
                new_events = []
                for up_id in unknown_parents:
                    try:
                        new_events.append(self._data_source.find_events_by_id_from_data_provider(up_id, broken_events))
                    except ValueError as err:
                        print(err)
                        print(f'Owners: {[n for n in self._all_nodes if n.data["parentEventId"] == up_id]}')
                        raise
            else:
                new_events: list = self._data_source.find_events_by_id_from_data_provider(unknown_parents, broken_events)

            unknown_parents2 = set()
            new_events = [new_events] if not isinstance(new_events, list) else new_events
            for e in new_events:

                try:
                    parent_event_id = e["parentEventId"]
                except KeyError as er:
                    print("_get_unknown_events")
                    print(er)
                    print(e)
                    print("Events which have ")
                    # raise
                    continue

                if parent_event_id == "Broken_Event":
                    print(e)

                if parent_event_id is not None and parent_event_id != "Broken_Event" and parent_event_id not in self.__unknown_parent_ids:
                    unknown_parents2.add(parent_event_id)

            new_events += self._get_unknown_events(unknown_parents2, broken_events)

            return new_events
        else:
            return []

    def _get_unknown_parents_ids(self) -> list:
        """Searches unknown events.

        :return: Unknown events.
        """
        unknown_parents_ids = []

        for parent_id in self.parent_events_ids:
            if parent_id is not None:
                if parent_id not in self.events_ids:
                    unknown_parents_ids.append(parent_id)

        return unknown_parents_ids
