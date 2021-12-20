from abc import ABC, abstractmethod
from typing import Callable, Generator, Iterator, List, Union

from th2_data_services.data import Data
from th2_data_services.data_source import DataSource
from anytree import Node, RenderTree, findall

from th2_data_services.provider_api.event import ICurrentProviderEvent
from th2_data_services.provider_api.provider5.event import provider5_http_event


class ITreeNodeShowFmt(ABC):
    @abstractmethod
    def __call__(self, pre, fill, node, **kwargs):
        pass


class TreeNode(Node):
    separator = " | "

    def __init__(self, name, event_interface: ICurrentProviderEvent, **kwargs):
        super().__init__(name, **kwargs)
        self._event_interface = event_interface

    class DefaultShowFmt(ITreeNodeShowFmt):
        def __call__(self, pre, fill, node, **kwargs):
            if kwargs["show_status"]:
                status = "P" if kwargs["node_status"] else "F"
                return "[%s] %s%s\n" % (status, pre, node.name)
            else:
                return "%s%s\n" % (pre, node.name)

    def __str__(self):
        s = ""
        for pre, fill, node in RenderTree(self):
            status = "P" if node.data[self._event_interface.STATUS] else "F"
            s += "[%s] %s%s\n" % (status, pre, node.name)
        return s

    @property
    def full_path_name(self):
        return self.separator.join([str(node.name) for node in self.path])

    def show(self, fmt: Callable = DefaultShowFmt, failed_only=False, show_status=True, **kwargs):
        s = ""
        for pre, fill, node in RenderTree(self):
            status: bool = node.data[self._event_interface.STATUS]

            if failed_only:
                if status is False:
                    s += fmt(pre, fill, node, show_status=show_status, node_status=status, **kwargs)
            else:
                s += fmt(pre, fill, node, show_status=show_status, node_status=status, **kwargs)

        return s


class TreeNodeProviderEvent(TreeNode):
    def __init__(self, name, data, event_interface: ICurrentProviderEvent, **kwargs):
        super().__init__(name, event_interface, **kwargs)
        self._data = data

    @property
    def data(self):
        return self._data

    @property
    def event_id(self):
        return self.data[self._event_interface.EVENT_ID]

    @property
    def parent_event_id(self):
        return self.data[self._event_interface.PARENT_EVENT_ID]

    def get_by_status(self, status: bool):
        return findall(self, lambda node: node.data[self._event_interface.STATUS] is status)

    def get_by_leaves_status(self, status: bool):
        return [n for n in self.leaves if n.data[self._event_interface.STATUS] is status]


class EventsTree2:
    """EventsTree2 - experimental tree."""

    def __init__(
        self,
        data: Union[Iterator, Generator[dict, None, None], Data],
        ds: DataSource,
        event_interface: ICurrentProviderEvent = provider5_http_event,
        preserve_body: bool = False,
        broken_events: bool = False,
        parentless: bool = False,
    ):
        """
        Args:
            data: Iterable object with provider events.
            ds: Data source object.
            event_interface: Interface for provider Event.
            preserve_body (:obj:`bool`, optional): If True keep Events bodies.
            broken_events: If True broken events is replaced on event stub.
            parentless: If True Events without body will be added to the tree.parentless.
        """
        self._data = data if data is not None else []
        self._event_interface = event_interface
        self.__preserve_body = preserve_body
        self._broken_events_flag = broken_events
        self._parentless = parentless
        self._data_source = ds
        self._all_nodes = []
        self.roots: List[TreeNodeProviderEvent] = []
        self.events = dict()  # {id: Node}
        self.events_ids = []  # Used to find unknown_parents_ids
        self.parent_events_ids = set()
        self.__unknown_parent_ids = set()  # Set in order to remove duplicate Event IDs.
        self.parentless_nodes = []
        self._last_nodes_len = -1

        # Append nodes from the data source.
        for event in self._get_events(self._data):
            self._append_node_and_ids(event)

        # Append unknown nodes.
        restored_events = self._get_unknown_events(self._get_unknown_parents_ids(), self._broken_events_flag)
        for event in self._get_events(restored_events):
            self._append_node_and_ids(event)

        # Search roots.
        node: TreeNodeProviderEvent
        for node in self._all_nodes.copy():
            if node.data[self._event_interface.PARENT_EVENT_ID] is None:
                self.roots.append(node)
                self._all_nodes.remove(node)

        self._build_trees(self.roots)

    def _create_node(self, event) -> TreeNodeProviderEvent:
        return TreeNodeProviderEvent(
            name=event[self._event_interface.NAME], data=event, event_interface=self._event_interface
        )

    def _append_node(self, node):
        self._all_nodes.append(node)

    def _append_events_ids(self, event_id):
        self.events_ids.append(event_id)

    def _get_events(self, data):
        for event in data:
            event = event.copy()

            if not self.__preserve_body:
                try:
                    event.pop("body")
                except KeyError:
                    pass
            yield event

    def _append_events(self, node: TreeNodeProviderEvent):
        self.events[node] = node.data[""]

    def _append_node_and_ids(self, event):
        node = self._create_node(event)
        self._append_node(node)
        self._append_events_ids(event[self._event_interface.EVENT_ID])
        self.parent_events_ids.add(event[self._event_interface.PARENT_EVENT_ID])

    def _build_trees(self, roots):
        """Recursion method."""
        parentless_nodes_len = len(self._all_nodes)  # The number of nodes that are not included in any tree.
        if parentless_nodes_len != 0:
            if parentless_nodes_len != self._last_nodes_len:
                self._last_nodes_len = parentless_nodes_len
                new_roots = []
                for node in self._all_nodes.copy():
                    for root_node in roots:
                        if (
                            node.data[self._event_interface.PARENT_EVENT_ID]
                            == root_node.data[self._event_interface.EVENT_ID]
                        ):
                            node.parent = root_node
                            try:
                                self._all_nodes.remove(node)
                            except ValueError as er:
                                print(er)
                                print("The Exception because Duplicate Nodes in the self._nodes!")
                                print(node)
                                print(self._all_nodes)
                                raise
                            new_roots.append(node)
                            break
                self._build_trees(new_roots)
            else:  # It happens if some events doesn't exist in DB and self._parentless == True
                print(f"Cannot build complete EventsTree2, some nodes will be available as .parentless_nodes")
                self.parentless_nodes = self._all_nodes
                print(self.parentless_nodes)
        else:
            return None

    """
    Думаю куда лучше будет иметь функцию, которая позволит получить пэренты, по списку ивентов.
    """

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
                        owners = {
                            [n for n in self._all_nodes if n.data[self._event_interface.PARENT_EVENT_ID] == up_id]
                        }
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
                parent_event_id = e[self._event_interface.PARENT_EVENT_ID]

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

    def get_by_id(self, ids: Union[List[str], str]) -> Union[dict, List[dict]]:
        is_str = False

        if isinstance(ids, str):
            is_str = True
            ids = [ids]

        r = []
        for event_id in ids:
            r.append(self.events[event_id])

        if is_str and len(r) == 1:
            return r[0]
        else:
            return r
