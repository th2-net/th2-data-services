from collections import defaultdict
from typing import List, Tuple, Generator, Dict, Callable, Optional

from treelib import Tree, Node
from treelib.exceptions import NodeIDAbsentError

from th2_data_services import Data
from th2_data_services.provider.data_source import IProviderDataSource
from th2_data_services.provider.struct import IEventStruct


class DetachedEventsCollection:
    # TODO
    pass


class EventsTree:
    def __init__(self, tree: Tree):
        self._tree = tree

    def get_event(self, id) -> Optional[dict]:
        """Gets event by id.

        Args:
            id: Event id.

        Raises:
            NodeIDAbsentError: If event id not in the tree.
        """
        node: Node = self._tree.get_node(id)
        if node is None:
            raise NodeIDAbsentError(f"Node {node} is not in the tree.")
        return node.data

    # TODO: I think, maybe will add it ?
    # def __getitem__(self, item):
    #     pass

    def get_root_id(self) -> str:
        """Gets root id."""
        return self._tree.root

    def get_leaves(self) -> Tuple[dict]:
        """Gets all tree leaves."""
        return tuple(leaf.data for leaf in self._tree.leaves())

    def get_children(self, id: str) -> Tuple[dict]:
        """Gets children for a event.

        Args:
            id: Event id.

        Raises:
            NodeIDAbsentError: If event id not in the tree.
        """
        children: List[Node] = self._tree.children(id)
        return tuple(child.data for child in children)

    def get_children_iter(self, id: str) -> Generator[dict, None, None]:
        """Gets children as iterator for a event.

        Args:
            id: Event id.

        Raises:
            NodeIDAbsentError: If event id not in the tree.
        """
        for child in self._tree.children(id):
            yield child.data

    def get_parent(self, id: str) -> dict:
        """Gets parent for an event.

        Args:
            id: Event id.

        Raises:
            NodeIDAbsentError: If event id not in the tree.
        """
        return self._tree.parent(id)

    def get_full_path(self, id: str):
        """Returns full path in some view

        Harry
        ├── Bill
        └── Jane
            ├── Diane
            │   └── Mary
            └── Mark

        examples:

        tree.get_full_path('Jane', id)
        ['Harry-event-id', 'Jane-event-id']

        tree.get_full_path('Jane', name)
        ['Harry-event-name', 'Jane-event-name']

        tree.get_full_path('Jane', event)
        ['Harry-event', 'Jane-event']


        l = ['Harry-event', 'Jane-event']
        [x[name] for x in l]
        """

    # def get_full_path_value(self, id: str, value: str):
    #     return [x[value] for x in self.get_full_path(id)]

    # TODO: It's from anytree instead treelib.
    def findall(self, node, filter_=None, stop=None, maxlevel=None, mincount=None, maxcount=None):
        pass

    def findall_by_field(self, node, value, name="name", maxlevel=None, mincount=None, maxcount=None):
        pass

    def find(self, node, filter_=None, stop=None, maxlevel=None):
        pass

    def find_by_field(self, node, value, name="name", maxlevel=None):
        pass

    def get_ancestor_by_filter(self, event: dict, filter: Callable) -> Optional[dict]:
        """Gets event ancestor by filter function.

        Args:
            event: Event.
            filter: Filter function that has one argument - ancestor event.
        """

    def get_ancestors(self, id: str) -> List[dict]:
        """Gets ancestors for event by id."""
        self._tree.ancestor()

    def show(self) -> None:
        # TODO - add output format class.
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


class EventsTreesCollection:
    """Builds events trees and keep them."""

    def __init__(
        self,
        data: Data,
        data_source: IProviderDataSource = None,
        preserve_body: bool = False,
        event_struct: IEventStruct = None,
        event_stub_builder=None,
    ):
        self._preserve_body = preserve_body
        self._event_struct = event_struct
        self._event_stub_builder = event_stub_builder
        self._data_source = data_source

        self._roots: List[EventsTree] = []
        self._detached_nodes: Dict[str, Node] = {}  # {parent_event_id: Node}
        self._unknown_ids: List[str]

        self.__build_collections(data)

    def __build_collections(self, data: Data) -> None:
        """Builds collections. # TODO Consider How i can change this. I don't like it.

        Args:
            data: Data.
        """
        events_nodes: Dict[Optional[str], List[Node]] = defaultdict(list)

        for event in self.__parse_events(data):
            event_id: str = event[self._event_struct.EVENT_ID]
            parent_event_id: str = event[self._event_struct.PARENT_EVENT_ID]
            event_name: str = event[self._event_struct.NAME]

            node = Node(tag=event_name, identifier=event_id, data=event)
            events_nodes[parent_event_id].append(node)

        self.__build_trees(events_nodes)

    def __build_trees(self, nodes: Dict[Optional[str], List[Node]]) -> None:
        """Builds trees and saves detached events.

        Args:
            nodes: Events nodes.
        """

        def __fill_tree(current_tree: Tree, parent_id: str) -> None:
            """Fills tree recursively.

            Args:
                current_tree: Tree for fill.
                parent_id: Parent even id.
            """
            for node in nodes[parent_id]:
                event_id: str = node.identifier
                current_tree.add_node(node, parent=parent_id)
                __fill_tree(tree, event_id)  # recursive fill
            nodes.pop(parent_id)

        roots = []
        for node in nodes[None]:
            tree = Tree()
            tree.add_node(node)
            roots.append(tree)
            event_id: str = node.identifier
            __fill_tree(tree, event_id)
        nodes.pop(None)

        self._roots = [EventsTree(root) for root in roots]
        self._detached_nodes = nodes

    def __parse_events(self, data: Data) -> Generator[dict, None, None]:
        """Parses events.

        Args:
            data: Data.
        """
        for event in data:
            if not self._preserve_body:
                try:
                    event.pop("body")
                except KeyError:
                    pass
            yield event

    def get_roots_ids(self) -> List[str]:
        """Gets roots ids."""
        return [tree.get_root_id() for tree in self._roots]

    def get_trees(self) -> List[EventsTree]:
        """Gets trees as EventsTree class."""
        return self._roots

    def get_root_by_id(self, id) -> EventsTree:
        """Gets root tree by id as EventsTree class.

        Args:
            id: Root id.

        Returns:
            Root tree.
        """
        for tree in self._roots:
            if tree.get_root_id() == id:
                return tree
