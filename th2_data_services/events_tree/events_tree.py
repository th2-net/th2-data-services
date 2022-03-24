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

from typing import List, Tuple, Generator, Callable, Optional, Union

from treelib import Tree, Node
from treelib.exceptions import NodeIDAbsentError

from th2_data_services.events_tree.exceptions import EventIdNotInTree

Th2Event = dict


class EventsTree:
    """EventsTree is a tree-based data structure of events.

    - get_x methods raise Exceptions if no result is found.
    - find_x methods return None if no result is found.
    - EventsTree stores events as Nodes and interacts with them using an internal tree.
    - EventsTree removes the 'body' field by default to save memory, but you can keep it.
    - Note that EventsTree stores only one tree.
        If you want to store all trees, use EventsTreeCollections.
    - EventsTree contains all events in memory.

    Take a look at the following HTML tree to understand some important terms.

    ```
    <body> <!-- ancestor (grandparent), but not parent -->
        <div> <!-- parent & ancestor -->
            <p>Hello, world!</p> <!-- child -->
            <p>Goodbye!</p> <!-- sibling -->
        </div>
    </body>
    ```
    """

    def __init__(self, tree: Tree):
        """EventsTree constructor.

        Args:
            tree (treelib.Tree): Tree.
        """
        self._tree = tree

    def _append_node(self, node: Node, parent_id: str) -> None:
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

    def get_event(self, id: str) -> Th2Event:
        """Gets event by id.

        Args:
            id: Event id.

        Raises:
            EventIdNotInTree: If event id is not in the tree.
        """
        node: Node = self._tree.get_node(id)
        if node is None:
            raise EventIdNotInTree(id)
        return node.data

    # TODO: In future it will be added.
    # def __getitem__(self, item):
    #     pass

    def get_root_id(self) -> str:
        """Gets root id."""
        return self._tree.root

    def get_root(self) -> Th2Event:
        """Gets root event."""
        return self.get_event(self._tree.root)

    def get_leaves(self) -> Tuple[Th2Event]:
        """Gets all tree leaves."""
        return tuple(leaf.data for leaf in self._tree.leaves())

    def get_children(self, id: str) -> Tuple[Th2Event]:
        """Gets children for an event.

        Args:
            id: Event id.

        Raises:
            EventIdNotInTree: If event id is not in the tree.
        """
        try:
            return tuple(child.data for child in self._tree.children(id))
        except NodeIDAbsentError:
            raise EventIdNotInTree(id)

    def get_children_iter(self, id: str) -> Generator[Th2Event, None, None]:
        """Gets children as iterator for an event.

        Args:
            id: Event id.

        Raises:
            EventIdNotInTree: If event id is not in the tree.
        """
        try:
            for child in self._tree.children(id):
                yield child.data
        except NodeIDAbsentError:
            raise EventIdNotInTree(id)

    def get_parent(self, id: str) -> Th2Event:
        """Gets parent for an event.

        Args:
            id: Event id.

        Raises:
            EventIdNotInTree: If event id is not in the tree.
        """
        try:
            return self._tree.parent(id).data
        except NodeIDAbsentError:
            raise EventIdNotInTree(id)

    def get_full_path(self, id: str, field: str = None) -> List[Union[str, Th2Event]]:  # noqa: D412
        """Returns full path for an event in right order.

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
        tree.get_full_path('Jane', id)
        ['Harry-event-id', 'Jane-event-id']

        tree.get_full_path('Jane', name)
        ['Harry-event-name', 'Jane-event-name']

        tree.get_full_path('Jane')
        ['Harry-event', 'Jane-event']
        ```

        Args:
            id: Event id.
            field: Field of event.

        Returns:
            Full path of event.

        Raises:
            EventIdNotInTree: If event id is not in the tree.
        """
        result = []

        for event in self.get_ancestors(id) + [self.get_event(id)]:
            if field is None:
                result.append(event)
            else:
                result.append(event[field])

        return result

    def get_ancestors(self, id: str) -> List[Th2Event]:
        """Returns all event's ancestors in right order.

        Args:
            id: Event id.

        Returns:
            All event's ancestors.

        Raises:
            EventIdNotInTree: If event id is not in the tree.
        """
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

        Raises:
            EventIdNotInTree: If event id is not in the tree.
        """
        try:
            ancestor: Node = self._tree.parent(id)
        except NodeIDAbsentError:
            raise EventIdNotInTree(id)

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
        try:
            for ancestor in self._iter_ancestors(id):
                if filter(ancestor):
                    return ancestor
        except EventIdNotInTree:
            return None
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
            stop: Stop function. If None searches for all nodes in the tree.
            max_count: Max count of matched events. Stops searching when `max_count` will be reached.

        Yields:
            Matching events.
        """
        counter = 0
        for node in self._tree.all_nodes_itr():
            event = node.data
            if stop is not None and stop(event):
                break
            if filter(event):
                yield event
                counter += 1
                if max_count is not None and max_count <= counter:
                    break

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
        for event in self.findall_iter(filter=filter, stop=stop, max_count=max_count):
            result.append(event)
        return result

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

        Raises:
            EventIdNotInTree: If event id is not in the tree.
        """
        subtree = self._tree.subtree(id)
        if not subtree:
            raise EventIdNotInTree(id)
        return subtree

    def show(self) -> None:
        """Prints EventsTree as tree view.

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
        self._tree.show()

    def __len__(self) -> int:
        return len(self._tree)

    def __contains__(self, event_id: str):
        return event_id in self._tree
