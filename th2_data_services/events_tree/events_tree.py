#  Copyright 2022 Exactpro (Exactpro Systems Limited)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from collections import defaultdict
from typing import List, Tuple, Generator, Dict, Callable, Optional, Union

from treelib import Tree, Node
from treelib.exceptions import NodeIDAbsentError

from th2_data_services import Data
from th2_data_services.provider.data_source import IProviderDataSource
from th2_data_services.provider.struct import IEventStruct
from th2_data_services.provider.v5.struct import provider5_event_struct


class EventsTree:
    """EventsTree - is a useful wrapper for your retrieved data.

    - EventsTree stores events as Nodes and interacts with them using an internal tree.
    - EventsTree removes the 'body' field by default to save memory, but you can keep it.
    - Note that EventsTree stores only one tree.
        If you want to store all trees, use EventsTreeCollections.
    - EventTree contains all events inside, so it takes
        ~2.5Gb for 1 million events.

    Take a look at the following HTML tree to understand some important terms.

        <body> <!-- ancestor (grandparent), but not parent -->
            <div> <!-- parent & ancestor -->
                <p>Hello, world!</p> <!-- child -->
                <p>Goodbye!</p> <!-- sibling -->
            </div>
        </body>
    """

    def __init__(self, tree: Tree):
        """
        Args:
            tree: Tree.
        """
        self._tree = tree

    @property
    def tree(self) -> Tree:
        return self._tree

    def append_node(self, node: Node, parent_id: str) -> None:
        """Appends a node to the tree.

        Args:
            node: Node.
            parent_id: Parent event id.
        """
        if parent_id not in self._tree:
            raise NodeIDAbsentError(f"Node {parent_id} is not in the tree.")

        self._tree.add_node(node, parent_id)

    def get_all_events_iter(self) -> Generator[dict, None, None]:
        """Gets all events from the tree as iterator."""
        for node in self._tree.all_nodes_itr():
            yield node.data

    def get_all_events(self) -> List[dict]:
        """Gets all events from the tree."""
        return [node.data for node in self._tree.all_nodes()]

    def get_event(self, id: str) -> Optional[dict]:
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

    # TODO: In future it will be added.
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
        return self._tree.parent(id).data

    def get_full_path(self, id: str, field: str = None) -> List[Union[str, dict]]:
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
        """
        result = []

        for event in self._iter_ancestors(id):
            if field is None:
                result.append(event)
            else:
                result.append(event.get(field))
        return result

    def _iter_ancestors(self, id: str) -> Generator[dict, None, None]:
        """Search ancestors of event.

        Args:
            id: Event id.

        Yields:
            Ancestor of event.
        """
        ancestor: Node = self._tree.parent(id)
        while ancestor:
            yield ancestor.data
            ancestor = self._tree.parent(ancestor.identifier)

    def find_ancestor(self, id: str, filter: Callable) -> Optional[dict]:
        """Finds ancestor of event.

        Args:
            id: Id
            filter: Filter function

        Returns:
            Ancestor of Event.
        """
        for ancestor in self._iter_ancestors(id):
            if filter(ancestor):
                return ancestor
        return None

    def findall(
        self,
        filter: Callable,
        stop: Callable = None,
        max_count: int = None,
    ) -> List[str]:
        """Search events matching.

        - The search uses 'filter_' which is a filtering function.
        - Optionally, the search uses 'stop' which is a stopping function.
        If 'stop' function returns 'True' then search is complete.
        - 'max_count' is a parameter that limits the search to a specified count.

        Args:
            filter: Filter function.
            stop: Stop function.
            max_count: Max count.

        Returns:
            Matching events.
        """
        result = []
        for node in self._tree.all_nodes_itr():
            event = node.data
            if stop is not None and stop(event):
                break
            if filter(event):
                result.append(event)
                if max_count is not None and max_count <= len(result):
                    break
        return result

    def find(self, filter: Callable, stop: Callable = None) -> Optional[dict]:
        """Search first event matching.

        - The search uses 'filter_' which is a filtering function.
        - Optionally, the search uses 'stop' which is a stopping function.
        If 'stop' function returns 'True' then search is complete.

        Args:
            filter: Filter function.
            stop: Stop function.

        Returns:
            One matching event.
        """
        for node in self._tree.all_nodes_itr():
            event = node.data
            if stop is not None and stop(event):
                break
            if filter(event):
                return event
        return None

    def get_subtree(self, id: str) -> "EventsTree":
        """Gets subtree of event by id.

        Args:
            id: Event id.

        Returns:
            Subtree.
        """
        return self._tree.subtree(id)

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
        # TODO - add output format class.
        self._tree.show()

    def __len__(self) -> int:
        return len(self._tree)

    def __contains__(self, event_id: str):
        return event_id in self._tree


class EventsTreesCollection:
    """EventsTreeCollection objective is building EventsTree
    and storing ones.

    - EventsTreeCollections stores all EventsTree. You can to refer to each of them.
    -
    """

    def __init__(
        self,
        data: Data,
        data_source: IProviderDataSource = None,
        preserve_body: bool = False,
        event_struct: IEventStruct = provider5_event_struct,
        event_stub_builder=None,
    ):
        self._preserve_body = preserve_body
        self._event_struct = event_struct
        self._event_stub_builder = event_stub_builder
        self._data_source = data_source

        self._roots: List[EventsTree] = []
        self._detached_nodes: Dict[Optional[str], List[Node]] = {}  # {parent_event_id: Node}

        self._build_collections(data)

    def _build_collections(self, data: Data) -> None:
        """Builds collections. # TODO Consider How i can change this. I don't like it.

        Args:
            data: Data.
        """
        events_nodes: Dict[Optional[str], List[Node]] = defaultdict(list)

        for event in self._parse_events(data):
            parent_event_id: str = event.get(self._event_struct.PARENT_EVENT_ID)
            node = self._transform_to_node(event)
            events_nodes[parent_event_id].append(node)

        self._build_trees(events_nodes)

    def _build_trees(self, nodes: Dict[Optional[str], List[Node]]) -> None:
        """Builds trees and saves detached events.

        Args:
            nodes: Events nodes.
        """

        roots = []
        for node in nodes[None]:
            tree = Tree()
            tree.add_node(node)
            roots.append(tree)
            event_id: str = node.identifier
            self._fill_tree(nodes, tree, event_id)
        nodes.pop(None)

        self._roots = [EventsTree(root) for root in roots]
        self._detached_nodes = nodes

    def _fill_tree(self, nodes: Dict[Optional[str], List[Node]], current_tree: Tree, parent_id: str) -> None:
        """Fills tree recursively.

        Args:
            current_tree: Tree for fill.
            parent_id: Parent even id.
        """
        for node in nodes[parent_id]:
            event_id: str = node.identifier
            current_tree.add_node(node, parent=parent_id)
            self._fill_tree(nodes, current_tree, event_id)  # recursive fill
        nodes.pop(parent_id)

    def _parse_event(self, event: dict) -> dict:
        """Parses event.

        Args:
            event: Event.

        Returns:
            Parsed event.
        """
        if not self._preserve_body:
            try:
                event.pop("body")
            except KeyError:
                pass
        return event

    def _parse_events(self, data: Union[Data, List[dict]]) -> Generator[dict, None, None]:
        """Parses events.

        Args:
            data: Data.

        Returns:
            Parsed events iterator.
        """
        for event in data:
            event = self._parse_event(event)
            yield event

    def _transform_to_node(self, event: dict) -> Node:
        event_id: str = event[self._event_struct.EVENT_ID]
        event_name: str = event[self._event_struct.NAME]

        node = Node(tag=event_name, identifier=event_id, data=event)
        return node

    def append_element(self, event: dict) -> None:
        event: dict = self._parse_event(event)
        node: Node = self._transform_to_node(event)
        parent_event_id: str = event.get(self._event_struct.PARENT_EVENT_ID)

        if parent_event_id is not None:
            events_trees = list(filter(lambda tree: parent_event_id in tree, self._roots))
            if events_trees:
                event_tree = events_trees[0]
                event_tree.append_node(node, parent_event_id)
                self._fill_tree(self._detached_nodes, event_tree.tree, parent_event_id)
            else:
                self._detached_nodes[parent_event_id].append(node)
        else:
            tree = Tree()
            tree.add_node(node)
            self._roots.append(EventsTree(tree))

    @property
    def detached_events(self) -> dict:
        return {id_: [node.data for node in nodes] for id_, nodes in self._detached_nodes.items()}

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

    def __len__(self) -> int:
        return sum([len(root) for root in self._roots])

    def __contains__(self, event_id: str):
        return any([event_id in tree for tree in self._roots])

    # def recover_missing_events(self):
    #     if self._data_source is None:
    #         raise ConnectionError("DataSource isn't exist.")
    #     events_id = self._detached_nodes.keys()
    #     instance_command = resolver_get_events_by_id(self._data_source)
    #     self._data_source.command()
