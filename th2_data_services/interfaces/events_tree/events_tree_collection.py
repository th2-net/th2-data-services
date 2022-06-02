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

from abc import ABC, abstractmethod
from collections import defaultdict
from typing import List, Dict, Optional, Union, Generator, Tuple, Callable

from treelib import Node, Tree

from th2_data_services import Data
from th2_data_services.events_tree.events_tree import EventsTree
from th2_data_services.events_tree.events_tree import Th2Event
from th2_data_services.events_tree.exceptions import EventIdNotInTree
from th2_data_services.provider.interfaces.data_source import IProviderDataSource
from th2_data_services.provider.v5.command_resolver import resolver_get_events_by_id


class EventsTreeCollection(ABC):
    """EventsTreeCollection objective is building 'EventsTree's and storing them.

    - EventsTreeCollection stores all EventsTree. You can to refer to each of them.
    - Recovery of missing events occurs when you have passed DataSource class.
    Otherwise you should execute the method 'recover_unknown_events'.
    Note that there is no point in the method if the list of detached events is empty.
    """

    def __init__(
        self, data: Data, data_source: IProviderDataSource = None, preserve_body: bool = False, stub: bool = False
    ):
        """EventsTreeCollection constructor.

        Args:
            data: Data object.
            data_source: Data Source object.
            preserve_body: If True it will preserve 'body' field in the Events.
            stub: If True it will create stub when event is broken.
        """
        self._preserve_body = preserve_body
        self._roots: List[EventsTree] = []
        self._parentless: Optional[List[EventsTree]] = None
        self._detached_nodes: Dict[Optional[str], List[Node]] = defaultdict(list)  # {parent_event_id: [Node1, ..]}
        self._stub_status = stub
        self._data_source = data_source

        events_nodes = self._build_event_nodes(data)
        self._build_trees(events_nodes)

        if data_source is not None:
            self.recover_unknown_events(self._data_source)

    def get_parentless_trees(self) -> List[EventsTree]:
        """Builds and returns parentless trees by detached events.

        Detached events will be removed from the tree.

        Returns:
            List of parentless trees if they exist, otherwise empty list.
        """
        if self._parentless is not None:
            return self._parentless
        else:
            self._parentless = self._build_parentless_trees()
            return self._parentless

    def _build_parentless_trees(self) -> List[EventsTree]:
        """Builds parentless trees by detached events.

        Returns:
            Parentless trees.
        """
        self._parentless = []

        stub_roots = list(self._detached_nodes.keys())
        for nodes in self._detached_nodes.values():
            for node in nodes:
                if node.identifier in stub_roots:
                    stub_roots.remove(node.identifier)

        for id_ in stub_roots:
            tree = Tree()
            tree.create_node(tag="Stub", identifier=id_, data=self._build_stub_event(id_))
            self._fill_tree(self._detached_nodes, tree, id_)
            self._parentless.append(EventsTree(tree))

        return self._parentless

    @abstractmethod
    def _build_stub_event(self, id_: str) -> dict:
        """Builds stub event.

        Args:
            id_: Event Id.
        """

    def _build_event_nodes(self, data: Data) -> Dict[Optional[str], List[Node]]:
        """Builds event nodes and group them by parent_event_id.

        Args:
            data: Data.

        Returns:
            Nodes.
        """
        events_nodes: Dict[Optional[str], List[Node]] = defaultdict(list)  # {parent_event_id: [Node1, Node2, ..]}

        for event in self._parse_events(data):
            parent_event_id: str = self._get_parent_event_id(event)
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
        for node in nodes[parent_id].copy():
            event_id: str = node.identifier
            if event_id not in current_tree:
                current_tree.add_node(node, parent=parent_id)
            nodes[parent_id].remove(node)
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
        event_id: str = self._get_event_id(event)
        event_name: str = self._get_event_name(event)

        node = Node(tag=event_name, identifier=event_id, data=event)
        return node

    def append_event(self, event: dict) -> None:
        """Appends event into tree.

        Args:
            event: Event.
        """
        event: dict = self._parse_event(event)
        node: Node = self._build_node(event)
        parent_event_id: str = self._get_parent_event_id(event)

        if parent_event_id is not None:
            events_trees = list(filter(lambda tree: parent_event_id in tree, self._roots))
            if events_trees:
                event_tree = events_trees[0]
                if node.identifier in event_tree:
                    pass
                else:
                    event_tree._append_node(node, parent_event_id)
                    self._fill_tree(self._detached_nodes, event_tree._tree, parent_event_id)
            else:
                self._detached_nodes[parent_event_id].append(node)
        else:
            tree = Tree()
            tree.add_node(node)
            self._roots.append(EventsTree(tree))
            self._fill_tree(self._detached_nodes, tree, node.identifier)

    @property
    def detached_events(self) -> dict:
        """Returns detached events as a dict with a view {'parent_id': ['referenced event', ...]}."""
        return {id_: [node.data for node in nodes] for id_, nodes in self._detached_nodes.items()}

    def get_roots_ids(self) -> List[str]:
        """Returns roots ids."""
        return [tree.get_root_id() for tree in self._roots]

    def get_trees(self) -> List[EventsTree]:
        """Returns the list of trees inside the collection."""
        return self._roots

    def get_root_by_id(self, id) -> EventsTree:
        """Returns a root tree by id as EventsTree class.

        Args:
            id: Root id.

        Returns:
            Root tree.

        Raises:
            EventIdNotInTree: If event id is not in the trees.
        """
        for tree in self._roots:
            if tree.get_root_id() == id:
                return tree
        raise EventIdNotInTree(id)

    def show(self):
        """Prints all EventsTrees as tree view.

        For example:

        ```
        Root
            |___ C01
            |    |___ C11
            |         |___ C111
            |         |___ C112
            |___ C02
            |___ C03
            |    |___ C31
        ```
        """
        trees = self.get_trees()
        for tree in trees:
            tree.show()

    @abstractmethod
    def _get_parent_event_id(self, event):
        """Gets parent event id from the event."""

    @abstractmethod
    def _get_event_id(self, event):
        """Gets event id from the event."""

    @abstractmethod
    def _get_event_name(self, event):
        """Gets event name from the event."""

    def __len__(self) -> int:
        """Returns the number of all events, including detached events."""
        return self.len_trees + self.len_detached_events

    def __contains__(self, event_id: str):
        return any([event_id in tree for tree in self._roots])

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(trees={len(self.get_roots_ids())}, "
            f"events={len(self)}[trees={self.len_trees}, detached={self.len_detached_events}])"
        )

    def summary(self) -> str:
        """Returns the collection summary."""
        return self.__repr__()

    @property
    def len_trees(self) -> int:
        """Returns number of events in the trees inside the collection."""
        return sum([len(root) for root in self._roots])

    @property
    def len_detached_events(self) -> int:
        """Returns number of detached events in the collection."""
        return sum([len(de_lst) for de_lst in self.detached_events.values()])

    def get_all_events_iter(self) -> Generator[Th2Event, None, None]:
        """Returns all events from the trees as iterator."""
        for tree in self._roots:
            yield from tree.get_all_events()

    def get_all_events(self) -> List[Th2Event]:
        """Returns all events from the trees."""
        return [event for tree in self._roots for event in tree.get_all_events()]

    def get_event(self, id: str) -> Optional[Th2Event]:
        """Returns an event by id.

        Args:
            id: Event id.

        Raises:
            EventIdNotInTree: If event id is not in the trees.
        """
        for tree in self._roots:
            try:
                return tree.get_event(id)
            except EventIdNotInTree:
                continue
        raise EventIdNotInTree(id)

    def get_leaves(self) -> Tuple[Th2Event]:
        """Returns all trees leaves."""
        return tuple(self.get_leaves_iter())

    def get_leaves_iter(self) -> Generator[Th2Event, None, None]:
        """Returns all trees leaves as iterator."""
        for tree in self._roots:
            yield from tree.get_leaves_iter()

    def get_children(self, id: str) -> Tuple[Th2Event]:
        """Returns children for the event by its id.

        Args:
            id: Event id.

        Raises:
            EventIdNotInTree: If event id is not in the trees.
        """
        for tree in self._roots:
            try:
                return tree.get_children(id)
            except EventIdNotInTree:
                continue
        raise EventIdNotInTree(id)

    def get_children_iter(self, id: str) -> Generator[Th2Event, None, None]:
        """Returns children as iterator for the event by its id.

        Args:
            id: Event id.

        Raises:
            EventIdNotInTree: If event id is not in the trees.
        """
        is_iter = False
        for tree in self._roots:
            try:
                yield from tree.get_children_iter(id)
                is_iter = True
            except EventIdNotInTree:
                continue
        if not is_iter:
            raise EventIdNotInTree(id)

    def get_parent(self, id: str) -> Th2Event:
        """Returns a parent for the event by its id.

        Args:
            id: Event id.

        Raises:
            NodeIDAbsentError: If event id is not in the trees.
        """
        for tree in self._roots:
            try:
                return tree.get_parent(id)
            except EventIdNotInTree:
                continue
        raise EventIdNotInTree(id)

    def get_full_path(self, id: str, field: str = None) -> List[Union[str, Th2Event]]:  # noqa: D412
        """Returns the full path for the event by its id in the right order.

        Examples:

        Imagine we have the following tree.

        ```
        Harry
        ├── Bill
        └── Jane
            ├── Diane
            │   └── Mary
            └── Mark
        ```

        ```
        collection.get_full_path('Jane', id)
        ['Harry-event-id', 'Jane-event-id']

        collection.get_full_path('Jane', name)
        ['Harry-event-name', 'Jane-event-name']

        collection.get_full_path('Jane')
        ['Harry-event', 'Jane-event']
        ```

        Args:
            id: Event id.
            field: Field of event.

        Returns:
            Full path of event.

        Raises:
            EventIdNotInTree: If event id is not in the trees.
        """
        for tree in self._roots:
            try:
                return tree.get_full_path(id, field)
            except EventIdNotInTree:
                continue
        raise EventIdNotInTree(id)

    def get_ancestors(self, id: str) -> List[Th2Event]:
        """Returns all event's ancestors in right order.

        Args:
            id: Event id.

        Returns:
            All event's ancestors.

        Raises:
            EventIdNotInTree: If event id is not in the trees.
        """
        for tree in self._roots:
            try:
                return tree.get_ancestors(id)
            except EventIdNotInTree:
                continue
        raise EventIdNotInTree(id)

    def find_ancestor(self, id: str, filter: Callable) -> Optional[Th2Event]:
        """Finds the ancestor of an event.

        Args:
            id: Event id.
            filter: Filter function

        Returns:
            Ancestor of Event.
        """
        for tree in self._roots:
            ancestor = tree.find_ancestor(id, filter)
            if ancestor is not None:
                return ancestor
        return None

    def findall_iter(
        self,
        filter: Callable,
        stop: Callable = None,
        max_count: int = None,
    ) -> Generator[Th2Event, None, None]:
        """Searches events matches as iterator.

        - The search uses 'filter' which is a filtering function.
        - Optionally, the search uses 'stop' which is a stopping function.
        If 'stop' function returns 'True' then search is complete.
        - 'max_count' is a parameter that limits the search to a specified count.

        Args:
            filter: Filter function.
            stop: Stop function. If None searches for all nodes in the trees.
            max_count: Max count of matched events. Stops searching when `max_count` will be reached.

        Yields:
            Matching events.
        """
        for tree in self._roots:
            yield from tree.findall_iter(filter=filter, stop=stop, max_count=max_count)

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
            stop: Stop function. If None searches for all nodes in the trees.
            max_count: Max count of matched events. Stops searching when `max_count` will be reached.

        Returns:
            Matching events.
        """
        result = []
        for tree in self._roots:
            events = tree.findall(filter=filter, stop=stop, max_count=max_count)
            if result is not None:
                result += [*events]
        return result

    def find(self, filter: Callable, stop: Callable = None) -> Optional[Th2Event]:
        """Searches the first event match.

        - The search uses 'filter' which is a filtering function.
        - Optionally, the search uses 'stop' which is a stopping function.
        If 'stop' function returns 'True' then search is complete.

        Args:
            filter: Filter function.
            stop: Stop function. If None searches for all nodes in the trees.

        Returns:
            One matching event.
        """
        for tree in self._roots:
            event = tree.find(filter=filter, stop=stop)
            if event is not None:
                return event
        return None

    def get_subtree(self, id: str) -> "EventsTree":
        """Returns subtree of the event by its id.

        Args:
            id: Event id.

        Returns:
            Subtree.

        Raises:
            EventIdNotInTree: If event id is not in the trees.
        """
        for tree in self._roots:
            try:
                return tree.get_subtree(id)
            except EventIdNotInTree:
                continue
        raise EventIdNotInTree(id)

    def recover_unknown_events(self, data_source: IProviderDataSource) -> None:
        """Loads missed events and recover events.

        Args:
            data_source: Data Source.
        """
        instance_command = resolver_get_events_by_id(data_source)

        previous_detached_events = list(self.detached_events.keys())
        while previous_detached_events:
            called_command = instance_command(self.detached_events.keys(), use_stub=self._stub_status)
            events = data_source.command(called_command)

            for event in events:
                if not self._get_event_name(event) == "Broken_Event":
                    self.append_event(event)

            if previous_detached_events == list(self.detached_events.keys()):
                break
            previous_detached_events = list(self.detached_events.keys())
