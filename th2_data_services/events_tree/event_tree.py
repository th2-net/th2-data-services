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
from treelib.exceptions import NodeIDAbsentError, LoopError

from th2_data_services.events_tree.exceptions import EventIdNotInTree, EventAlreadyExist, EventRootExist, TreeLoop

Th2Event = dict  # TODO - move to types. Also this class knows that th2-event is a dict, but it cannot to know.


class EventTree:
    """EventTree is a tree-based data structure of events.

    - get_x methods raise Exceptions if no result is found.
    - find_x methods return None if no result is found.
    - EventTree stores events as Nodes and interacts with them using an internal tree.
    - Note that EventTree stores only one tree.
        If you want to store all trees, use EventTreeCollections.
    - EventTree contains all events in memory.

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

    def __init__(self, event_name: str, event_id: str, data: dict = None):
        """EventTree constructor.

        Args:
            event_name: Event Name.
            event_id: Event Id.
            data: Data of event.
        """
        self._tree = Tree()
        self._create_root_event(event_name, event_id, data)

    def _create_root_event(self, event_name: str, event_id: str, data: dict = None) -> None:
        """Appends a root event to the tree.

        Args:
            event_name: Event Name.
            event_id: Event Id.
            data: Data of event.
        """
        if self._tree.root is not None:
            raise EventRootExist(event_id)
        if event_id in self._tree:
            raise EventAlreadyExist(event_id)

        self._tree.create_node(tag=event_name, identifier=event_id, parent=None, data=data)

    def append_event(self, event_name: str, event_id: str, parent_id: str, data: dict = None) -> None:
        """Appends the event to the tree.

        Args:
            event_name: Event Name.
            event_id: Event Id.
            parent_id: Parent Id.
            data: Data of event.
        """
        if event_id in self._tree:
            raise EventAlreadyExist(event_id)
        if parent_id is None:
            raise ValueError(
                "The param 'parent_id' must be not None. If you want create root event then use 'create_root_event'"
            )

        try:
            self._tree.create_node(tag=event_name, identifier=event_id, parent=parent_id, data=data)
        except NodeIDAbsentError:
            raise EventIdNotInTree(parent_id)

    def get_all_events_iter(self) -> Generator[Th2Event, None, None]:
        """Returns all events from the tree as iterator."""
        for node in self._tree.all_nodes_itr():
            yield node.data

    def get_all_events(self) -> List[Th2Event]:
        """Returns all events from the tree."""
        return [node.data for node in self._tree.all_nodes()]

    def get_event(self, id: str) -> Th2Event:
        """Returns an event by id.

        Args:
            id: Event id.

        Raises:
            EventIdNotInTree: If event id is not in the tree.
        """
        node: Node = self._tree.get_node(id)
        if node is None:
            raise EventIdNotInTree(id)
        return node.data

    def __getitem__(self, id_: str) -> Th2Event:
        """e.g. ET['id1'] returns event.data."""
        try:
            return self._tree[id_].data
        except NodeIDAbsentError:
            raise EventIdNotInTree(id_)

    def __setitem__(self, id_: str, data: dict) -> None:
        # TODO - It shouldn't raise an exception.
        #   It should create new Node or change existing
        try:
            self._tree[id_].data = data
        except NodeIDAbsentError:
            raise EventIdNotInTree(id_)

    def update_event_name(self, event_id: str, event_name: str) -> None:
        """Updates Event name in the tree. Note that it doesn't change internal data.

        Args:
            event_id: Event id.
            event_name: Event name.

        Raises:
            EventIdNotInTree: If event id is not in the tree.
        """
        try:
            self._tree.update_node(event_id, tag=event_name)
        except NodeIDAbsentError:
            raise EventIdNotInTree(event_id)

    def update_parent_link(self, event_id: str, parent_id: str) -> None:
        """Updates the link to parent.

        Args:
            event_id: Event id.
            parent_id: New parent id.

        Raises:
            EventIdNotInTree: If event id is not in the tree.
            TreeLoop: If parent id will point to the descendant event.
        """
        try:
            self._tree.move_node(event_id, parent_id)
        except NodeIDAbsentError:
            raise EventIdNotInTree(event_id)
        except LoopError:
            raise TreeLoop(event_id, parent_id)

    def get_root_id(self) -> str:
        """Returns the root id."""
        return self._tree.root

    def get_root_name(self) -> str:
        """Returns the root name."""
        return self._tree.get_node(self.get_root_id()).tag

    def get_root(self) -> Th2Event:
        """Returns the root event."""
        return self.get_event(self._tree.root)

    def get_leaves(self) -> Tuple[Th2Event]:
        """Returns all tree leaves."""
        # Do not use self.get_leaves_iter here because it takes more time.
        return tuple(self.get_leaves_iter())

    def get_leaves_iter(self) -> Generator[Th2Event, None, None]:
        """Returns all tree leaves as iterator."""
        for leaf in self._tree.leaves():
            yield leaf.data

    def get_children(self, id: str) -> Tuple[Th2Event]:
        """Returns children for the event by its id.

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
        """Returns children as iterator for the event by its id.

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
        """Returns a parent for the event by its id.

        Args:
            id: Event id.

        Raises:
            EventIdNotInTree: If event id is not in the tree.
        """
        try:
            parent = self._tree.parent(id)

            if parent is None:
                raise EventIdNotInTree(id)

            return parent.data
        except NodeIDAbsentError:
            raise EventIdNotInTree(id)

    def get_full_path(self, id: str, field: str = None) -> List[Union[str, Th2Event]]:  # noqa: D412
        """Returns the full path for the event by its id in right order.

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
            event = node.data.copy()
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

    def get_subtree(self, id: str) -> "EventTree":
        """Returns subtree of the event by its id.

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

        et = EventTree(event_name="0", event_id="0")
        et._tree = subtree

        return et

    def merge_tree(self, parent_id: str, other_tree: "EventTree", use_deepcopy: bool = False) -> None:
        """Merges a EventTree to specified identifier.

        Args:
            parent_id: Event id to which merge.
            other_tree: EventTree.
            use_deepcopy: True if you need deepcopy for your objects in event.

        Raises:
             EventIdNotInTree: If event id is not in the tree.
        """
        if parent_id not in self._tree:
            raise EventIdNotInTree(parent_id)
        self._tree.merge(parent_id, other_tree._tree, use_deepcopy)

    def show(self) -> None:
        """Prints the EventTree as tree view.

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
        # TODO
        # et.append_event('a', '2', et.get_root_id())
        # et.show()
        # Traceback (most recent call last):
        #   File "C:\Users\admin\AppData\Local\Programs\Python\Python39\lib\code.py", line 90, in runcode
        #     exec(code, self.locals)
        #   File "<input>", line 1, in <module>
        #   File "C:\Users\admin\exactpro\prj\th2\internal\DS\github\th2-data-services\th2_data_services\events_tree\event_tree.py", line 475, in show
        #     self._tree.show()
        #   File "C:\Users\admin\exactpro\prj\th2\internal\DS\github\th2-data-services\ds_lib_venv_py39\lib\site-packages\treelib\tree.py", line 854, in show
        #     print(self._reader)
        #   File "C:\Users\admin\AppData\Local\Programs\Python\Python39\lib\encodings\cp1251.py", line 19, in encode
        #     return codecs.charmap_encode(input,self.errors,encoding_table)[0]
        # UnicodeEncodeError: 'charmap' codec can't encode characters in position 6-8: character maps to <undefined>
        self._tree.show()

    def __len__(self) -> int:
        return len(self._tree)

    def __contains__(self, event_id: str):
        return event_id in self._tree

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.get_root_name()}', root_id='{self.get_root_id()}', events={len(self)})"

    def summary(self) -> str:
        """Returns the tree summary."""
        return self.__repr__()
