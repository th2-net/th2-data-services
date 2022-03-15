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
from th2_data_services.provider.struct import IEventStruct
from th2_data_services.provider.v5.struct import provider5_event_struct

Th2Event = dict


# TODO - implement custom exceptions!


class EventsTree:
    """EventsTree - is a useful wrapper for your retrieved data.

    Note:
        get_x methods raise Exceptions if no result is found.
        find_x methods return None if no result is found.

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
        """EventsTree constructor.

        Args:
            tree (treelib.Tree): Tree.
        """
        self._tree = tree

    @property
    def tree(self) -> Tree:
        # TODO - del it?
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

    def get_all_events_iter(self) -> Generator[Th2Event, None, None]:
        """Gets all events from the tree as iterator."""
        for node in self._tree.all_nodes_itr():
            yield node.data

    def get_all_events(self) -> List[Th2Event]:
        """Gets all events from the tree."""
        return [node.data for node in self._tree.all_nodes()]

    # TODO - implement custom exceptions!
    def get_event(self, id: str) -> Optional[Th2Event]:
        """Gets event by id.

        Args:
            id: Event id.

        Raises:
            NodeIDAbsentError: If event id not in the tree.
        """
        node: Node = self._tree.get_node(id)
        if node is None:
            raise NodeIDAbsentError(f"Event '{id}' is not in the tree.")
        return node.data

    # TODO: In future it will be added.
    # def __getitem__(self, item):
    #     pass

    def get_root_id(self) -> str:
        """Gets root id."""
        return self._tree.root

    def get_root(self) -> Th2Event:
        """Gets root event"""
        return self.get_event(self._tree.root)

    def get_leaves(self) -> Tuple[Th2Event]:
        """Gets all tree leaves."""
        return tuple(leaf.data for leaf in self._tree.leaves())

    # TODO - implement custom exceptions!
    def get_children(self, id: str) -> Tuple[Th2Event]:
        """Gets children for an event.

        Args:
            id: Event id.

        Raises:
            NodeIDAbsentError: If event id not in the tree.
        """
        children: List[Node] = self._tree.children(id)
        return tuple(child.data for child in children)

    # TODO - implement custom exceptions!
    def get_children_iter(self, id: str) -> Generator[Th2Event, None, None]:
        """Gets children as iterator for an event.

        Args:
            id: Event id.

        Raises:
            NodeIDAbsentError: If event id not in the tree.
        """
        for child in self._tree.children(id):
            yield child.data

    # TODO - implement custom exceptions!
    def get_parent(self, id: str) -> Th2Event:
        """Gets parent for an event.

        Args:
            id: Event id.

        Raises:
            NodeIDAbsentError: If event id not in the tree.
        """
        return self._tree.parent(id).data

    # TODO - update docstring
    def get_full_path(self, id: str, field: str = None) -> List[Union[str, Th2Event]]:
        """Returns full path for an event in right order.

        Harry
        ├── Bill
        └── Jane
            ├── Diane
            │   └── Mary
            └── Mark

        Examples:
            tree.get_full_path('Jane', id)
            ['Harry-event-id', 'Jane-event-id']

            tree.get_full_path('Jane', name)
            ['Harry-event-name', 'Jane-event-name']

            tree.get_full_path('Jane', event)
            ['Harry-event', 'Jane-event']
        """
        result = []

        for event in self.get_ancestors(id) + [self.get_event(id)]:
            if field is None:
                result.append(event)
            else:
                result.append(event[field])

        return result

    def get_ancestors(self, id: str) -> List[Th2Event]:
        """Returns all event's ancestors in right order."""
        result = [e for e in self._iter_ancestors(id)]
        result.reverse()
        return result

    def _iter_ancestors(self, id: str) -> Generator[Th2Event, None, None]:
        """Search ancestors by event id.

        Note, it yields ancestors in reverse order.

        Args:
            id: Event id.

        Yields:
            Ancestor of event.
        """
        ancestor: Node = self._tree.parent(id)
        while ancestor:
            yield ancestor.data
            ancestor = self._tree.parent(ancestor.identifier)

    def find_ancestor(self, id: str, filter: Callable) -> Optional[Th2Event]:
        """Finds the ancestor of an event.

        Args:
            id: Event id.
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
    ) -> List[Th2Event]:
        """Searches events matches.

        - The search uses 'filter' which is a filtering function.
        - Optionally, the search uses 'stop' which is a stopping function.
        If 'stop' function returns 'True' then search is complete.
        - 'max_count' is a parameter that limits the search to a specified count.

        Args:
            filter: Filter function.
            stop: Stop function. If None searches for all nodes in the tree.
            max_count: Max count of matched events. Stops searching when `max_count` will be reached.

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

    # TODO - Add findall_iter

    def find(self, filter: Callable, stop: Callable = None) -> Optional[Th2Event]:
        """Searches the first event match.

        - The search uses 'filter' which is a filtering function.
        - Optionally, the search uses 'stop' which is a stopping function.
        If 'stop' function returns 'True' then search is complete.

        Args:
            filter: Filter function.
            stop: Stop function. If None searches for all nodes in the tree.

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

    # TODO - add output format class. (Slava can do it)
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

        self._tree.show()

    def __len__(self) -> int:
        return len(self._tree)

    def __contains__(self, event_id: str):
        return event_id in self._tree


# TODO - (proposal) - perhaps it's better to separate collection and tree to other modules.
# TODO - Collection should contains a lot of method from EventsTree. They do the same but for all trees
# TODO - (proposal) - do you think it's ok to make it via ABC and implement methods instead of self._event_struct?
# TODO - (question) - why do we recover_unknown_events not here?
class EventsTreesCollection:  # (ABC):
    """EventsTreeCollection objective is building EventsTrees and storing them.

    EventsTreeCollection stores all EventsTree. You can to refer to each of them.
    """

    # TODO - what about headless trees ?
    # TODO - update docstring (args names)
    def __init__(
        self,
        data: Data,
        preserve_body: bool = False,
        event_struct: IEventStruct = provider5_event_struct,
        # event_struct: IEventStruct = None,  # TODO - if use ABC it perhaps should be deleted.
    ):
        """EventsTreesCollection constructor.

        Args:
            data:
            preserve_body:
            event_struct:
        """
        self._preserve_body = preserve_body
        self._event_struct = event_struct

        self._roots: List[EventsTree] = []
        self._detached_nodes: Dict[Optional[str], List[Node]] = defaultdict(list)  # {parent_event_id: [Node1, ..]}

        events_nodes = self._build_event_nodes(data)
        self._build_trees(events_nodes)

    def _build_event_nodes(self, data: Data) -> Dict[Optional[str], List[Node]]:
        """Builds event nodes and group them by parent_event_id.

        Args:
            data: Data.
        """
        events_nodes: Dict[Optional[str], List[Node]] = defaultdict(list)  # {parent_event_id: [Node1, Node2, ..]}

        for event in self._parse_events(data):
            # TODO - perhaps it's better to realise it via ABC
            # TODO - Perhaps, it was meant to be 'event.get()'
            parent_event_id: str = event[self._event_struct.PARENT_EVENT_ID]  # self._get_parent_event_id(event)
            node = self._build_node(event)
            events_nodes[parent_event_id].append(node)

        return events_nodes

    def _build_trees(self, nodes: Dict[Optional[str], List[Node]]) -> None:
        """Builds trees and saves detached events.

        Args:
            nodes: Events nodes.
        """

        roots = []
        for root_node in nodes[None]:  # None - is parent_event_id for root events.
            tree = Tree()
            tree.add_node(root_node)
            roots.append(tree)
            root_event_id: str = root_node.identifier
            self._fill_tree(nodes, tree, root_event_id)
        nodes.pop(None)

        self._roots = [EventsTree(root) for root in roots]
        self._detached_nodes = nodes

    def _fill_tree(self, nodes: Dict[Optional[str], List[Node]], current_tree: Tree, parent_id: str) -> None:
        """Fills tree recursively.

        Args:
            nodes: Events nodes.
            current_tree: Tree for fill.
            parent_id: Parent even id.
        """
        # TODO - разобраться что тут и как. (It's for Slava)
        # TODO - Не будет ли сильно расти память, не будет ли слишком много рекурсивных вызовов при большом дереве?
        for node in nodes[parent_id]:
            event_id: str = node.identifier
            if event_id not in current_tree:
                current_tree.add_node(node, parent=parent_id)
            self._fill_tree(nodes, current_tree, event_id)  # Recursive fill.
        nodes.pop(parent_id)

    def _parse_event(self, event: Th2Event) -> Th2Event:
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

    def _build_node(self, event: dict) -> Node:
        """Builds event as dict into event as Node.

        Args:
            event: Event.

        Returns:
            Node.
        """
        # TODO - perhaps it's better to realise it via ABC
        event_id: str = event[self._event_struct.EVENT_ID]  # self._get_event_id(event)
        event_name: str = event[self._event_struct.NAME]  # self._get_event_name(event)

        node = Node(tag=event_name, identifier=event_id, data=event)
        return node

    def append_element(self, event: dict) -> None:
        """Appends event into tree.

        Args:
            event: Event.
        """
        event: dict = self._parse_event(event)
        node: Node = self._build_node(event)
        # TODO - perhaps it's better to realise it via ABC
        parent_event_id: str = event[self._event_struct.PARENT_EVENT_ID]  # self._get_parent_event_id(event)

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
            self._fill_tree(self._detached_nodes, tree, node.identifier)

    # TODO - add docstring
    @property
    def detached_events(self) -> dict:
        return {id_: [node.data for node in nodes] for id_, nodes in self._detached_nodes.items()}

    def get_roots_ids(self) -> List[str]:
        """Gets roots ids."""
        return [tree.get_root_id() for tree in self._roots]

    def get_trees(self) -> List[EventsTree]:
        """Gets trees as EventsTree class."""
        return self._roots

    # TODO - should raise an Exception if id not found
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

    def show(self):
        """Prints all EventsTree as tree view.

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
        trees = self.get_trees()
        for tree in trees:
            tree.show()

    # @abstractmethod
    # def _get_parent_event_id(self, event):
    #     pass
    #
    # @abstractmethod
    # def _get_event_id(self, event):
    #     pass
    #
    # @abstractmethod
    # def _get_event_name(self, event):
    #     pass

    def __len__(self) -> int:
        return sum([len(root) for root in self._roots])

    def __contains__(self, event_id: str):
        return any([event_id in tree for tree in self._roots])
