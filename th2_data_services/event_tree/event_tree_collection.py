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
from typing import Callable, Dict, Generator, Iterable, List, Optional, Tuple, Union

from treelib.exceptions import NodeIDAbsentError
from th2_data_services.event_tree.event_tree import EventTree
from th2_data_services.event_tree.event_tree import Th2Event
from th2_data_services.event_tree.exceptions import EventIdNotInTree

import warnings

from th2_data_services.event_tree.etc_driver import IETCDriver


class EventTreeCollection:
    """EventTreeCollection objective is building 'EventsTree's and storing them.

    - EventTreeCollection stores all EventsTree. You can to refer to each of them.
    - Recovery of missing events occurs when you have passed DataSource class to constructor.
    Otherwise you should execute the method 'recover_unknown_events' manually.
    Note that there is no point in the method if the list of detached events is empty.
    """

    def __init__(self, driver: IETCDriver):
        """EventTreeCollection constructor.

        Args:
            driver: initialized driver object.
        """
        self._driver = driver
        self._roots: List[EventTree] = []
        self._parentless: Optional[List[EventTree]] = None
        # {parent_event_id: [event1, ..]}
        self._detached_nodes: Dict[Optional[str], List[dict]] = defaultdict(list)

    def _detached_parent_ids(self):
        return self._detached_nodes.keys()

    def _build_parentless_trees(self) -> List[EventTree]:
        """Builds parentless trees by detached events.

        Returns:
            Parentless trees.
        """
        self._parentless = []

        stub_roots = set(self._detached_parent_ids())
        for event in self.get_detached_events_iter():
            event_id = self._driver.get_event_id(event)
            if event_id in stub_roots:
                stub_roots.remove(event_id)

        for id_ in stub_roots:
            stub_event = self._driver.build_stub_event(id_)
            event_id, event_name = self._driver.get_event_id(stub_event), self._driver.get_event_name(stub_event)
            tree = EventTree(event_id=event_id, event_name=event_name, data=stub_event)
            self._fill_tree(self._detached_nodes, tree, id_)
            self._parentless.append(tree)

        return self._parentless

    def _build_events_store(self, data: Iterable) -> Dict[Optional[str], List[dict]]:
        """Builds events store, grouping them by parent_event_id.

        Args:
            data: Data.

        Returns:
            Nodes.
        """
        events_store: Dict[Optional[str], List[dict]] = defaultdict(list)  # {parent_event_id: [event1, event2, ..]}

        for event in data:
            parent_event_id: str = self._driver.get_parent_event_id(event)
            events_store[parent_event_id].append(event)

        return events_store

    def _build_trees(self, events_nodes: Dict[Optional[str], List[dict]]) -> None:
        """Builds trees and saves detached events.

        Args:
            events_nodes: Events nodes.
        """
        roots = []
        for root_event in events_nodes[None]:  # None - is parent_event_id for root events.
            event_name, event_id = self._driver.get_event_name(root_event), self._driver.get_event_id(root_event)
            tree = EventTree(event_name=event_name, event_id=event_id, data=root_event)
            roots.append(tree)
            self._fill_tree(events_nodes, tree, event_id)
        events_nodes.pop(None)

        self._roots = roots
        self._detached_nodes = events_nodes

    def _fill_tree(
        self, events_store: Dict[Optional[str], List[dict]], current_tree: EventTree, parent_id: str
    ) -> None:
        """Fills tree recursively.

        Args:
            events_store: Events nodes.
            current_tree: Tree for fill.
            parent_id: Parent even id.
        """
        for event in events_store[parent_id].copy():
            event_name, event_id, = self._driver.get_event_name(
                event
            ), self._driver.get_event_id(event)
            if event_id not in current_tree:
                current_tree.append_event(event_name=event_name, event_id=event_id, parent_id=parent_id, data=event)
            events_store[parent_id].remove(event)
            self._fill_tree(events_store, current_tree, event_id)  # Recursive fill.
        events_store.pop(parent_id)

    def build(self, data: Iterable):
        events_nodes = self._build_events_store(data)  # {parent_event_id: [event1, event2, ..]}
        self._build_trees(events_nodes)  # Produces _detached_nodes.

    def get_parentless_trees(self) -> List[EventTree]:
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

    def append_event(self, event: dict) -> None:
        """Appends event into a tree.

        Args:
            event: Event.
        """
        parent_event_id: str = self._driver.get_parent_event_id(event)

        if parent_event_id is not None:  # Is root?
            events_trees = list(filter(lambda tree: parent_event_id in tree, self._roots))
            if events_trees:
                event_tree = events_trees[0]
                event_id, event_name = self._driver.get_event_id(event), self._driver.get_event_name(event)
                if event_id in event_tree:
                    pass
                else:
                    event_tree.append_event(
                        event_name=event_name, event_id=event_id, parent_id=parent_event_id, data=event
                    )
                    self._fill_tree(self._detached_nodes, event_tree, parent_event_id)
            else:
                self._detached_nodes[parent_event_id].append(event)
        else:
            event_id, event_name = self._driver.get_event_id(event), self._driver.get_event_name(event)
            tree = EventTree(event_id=event_id, event_name=event_name, data=event)
            self._roots.append(tree)

            event_id = self._driver.get_event_id(event)
            self._fill_tree(self._detached_nodes, tree, event_id)

    def _detached_events_dict(self) -> dict:
        """Returns detached events as a dict that looks like {'parent_id': ['referenced event', ...]}."""
        return {id_: events.copy() for id_, events in self._detached_nodes.items()}

    def get_detached_events_iter(self) -> Generator[Th2Event, None, None]:
        """Yields detached events."""
        for events in self._detached_nodes.values():
            for event in events:
                yield event

    def get_detached_events(self) -> List[Th2Event]:
        """Returns detached events list."""
        return list(self.get_detached_events_iter())

    def get_roots_ids(self) -> List[str]:
        """Returns ids of all trees roots located in the collection.

        If there are parentless trees, they also will be return.
        """
        if self._parentless is not None:
            return [tree.get_root_id() for tree in self._roots] + [tree.get_root_id() for tree in self._parentless]
        return [tree.get_root_id() for tree in self._roots]

    def get_trees(self) -> List[EventTree]:
        """Returns the list of trees inside the collection.

        If there are parentless trees, they also will be return.
        """
        if self._parentless is not None:
            return self._roots + self._parentless
        return self._roots

    def get_root_by_id(self, id) -> Th2Event:
        """Returns the root event of a tree by id of any event in this tree.

        If event id of parentless tree is passed, stub of this parentless tree will be returnd.

        Args:
            id: Event id.

        Returns:
            Th2Event.

        Raises:
            EventIdNotInTree: If event id is not in the trees.
        """
        try:
            return self.get_tree_by_id(id).get_root()
        except EventIdNotInTree:
            raise EventIdNotInTree(id)

    def get_tree_by_id(self, id) -> EventTree:
        """Returns a tree by id of any event in this tree.

        If event id of parentless tree is passed, stub of this parentless tree will be returnd.

        Args:
            id: Event id.

        Returns:
            Tree.

        Raises:
            EventIdNotInTree: If event id is not in the trees.
        """
        for tree in self._roots:
            if id in tree:
                return tree
        if self._parentless is not None:
            for tree in self._parentless:
                if id in tree:
                    return tree
        raise EventIdNotInTree(id)

    def show(self):
        # TODO - works in linux only now.
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

    def __len__(self) -> int:
        """Returns the number of all events, including detached events."""
        return self.len_trees + self.len_detached_events

    def __contains__(self, event_id: str):
        for tree in self._roots:
            if event_id in tree:
                return True
        if self._parentless is not None:
            for tree in self._parentless:
                if event_id in tree:
                    return True
        return False

    def __repr__(self) -> str:
        len_trees_events = self.len_trees
        len_detached_events = self.len_detached_events
        len_regular_trees = len(self.get_roots_ids())

        if self._parentless:
            len_parentless_trees = len(self.get_parentless_trees())
            trees_parentless_info = (
                f"[regular={len_regular_trees - len_parentless_trees}, parentless={len_parentless_trees}]"
            )
        else:
            trees_parentless_info = ""

        return (
            f"{self.__class__.__name__}(trees={len_regular_trees}{trees_parentless_info}, "
            f"events={len_trees_events + len_detached_events}[trees={len_trees_events}, detached={len_detached_events}])"
        )

    def summary(self) -> str:
        """Returns the collection summary.

        The same as repr(EventTreeCollection).
        """
        return self.__repr__()

    @property
    def len_trees(self) -> int:
        """Returns number of events in the trees inside the collection, including parentless trees."""
        if self._parentless is not None:
            return sum([len(root) for root in self._roots]) + self.len_parentless
        return sum([len(root) for root in self._roots])

    @property
    def len_parentless(self) -> int:
        """Returns number of events in the parentless trees inside the collection."""
        if self._parentless is not None:
            return sum([len(root) for root in self._parentless])
        return 0

    @property
    def len_detached_events(self) -> int:
        """Returns number of detached events in the collection."""
        return sum([len(events_lst) for events_lst in self._detached_nodes.values()])

    def get_all_events_iter(self) -> Generator[Th2Event, None, None]:
        """Yields all events from the collection."""
        for tree in self._roots:
            yield from tree.get_all_events_iter()
        if self._detached_nodes:
            yield from self.get_detached_events_iter()
        if self._parentless is not None:
            for tree in self._parentless:
                yield from tree.get_all_events_iter()

    def get_all_events(self) -> List[Th2Event]:
        """Returns all events from the collection."""
        return list(self.get_all_events_iter())

    def get_event(self, id: str) -> Optional[Th2Event]:
        """Returns an event by its id.

        Args:
            id: Event id.

        Raises:
            EventIdNotInTree: If event id is not in the collection.
        """
        for tree in self._roots:
            try:
                return tree.get_event(id)
            except EventIdNotInTree:
                continue
        if self._detached_nodes:
            for event in self.get_detached_events_iter():
                if self._driver.get_event_id(event) == id:
                    return event
        if self._parentless is not None:
            for tree in self._parentless:
                try:
                    return tree.get_event(id)
                except EventIdNotInTree:
                    continue
        raise EventIdNotInTree(id)

    def get_leaves(self) -> Tuple[Th2Event]:
        """Returns all trees leaves, including parentless trees."""
        return tuple(self.get_leaves_iter())

    def get_leaves_iter(self) -> Generator[Th2Event, None, None]:
        """Yields all trees leaves, including parentless trees."""
        for tree in self._roots:
            yield from tree.get_leaves_iter()
        if self._parentless is not None:
            for tree in self._parentless:
                yield from tree.get_leaves_iter()

    def get_children(self, id: str) -> Tuple[Th2Event]:
        """Returns children of the event by its id.

        This method applicable only for trees (regular or parentless), not for detached events.

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
        if self._parentless is not None:
            for tree in self._parentless:
                try:
                    return tree.get_children(id)
                except EventIdNotInTree:
                    continue
        raise EventIdNotInTree(id)

    def get_children_iter(self, id: str) -> Generator[Th2Event, None, None]:
        """Yields children of the event by its id.

        This method applicable only for trees (regular or parentless), not for detached events.

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
        if self._parentless is not None:
            for tree in self._parentless:
                try:
                    yield from tree.get_children_iter(id)
                    is_iter = True
                except EventIdNotInTree:
                    continue
        if not is_iter:
            raise EventIdNotInTree(id)

    def get_parent(self, id: str) -> Th2Event:
        """Returns a parent of the event by its id.

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
        if self._detached_nodes:
            parent_id = None
            for event in self.get_detached_events_iter():
                if self._driver.get_event_id(event) == id:
                    parent_id = self._driver.get_parent_event_id(event)
                    break
            for event in self.get_detached_events_iter():
                if self._driver.get_event_id(event) == parent_id:
                    return event
        if self._parentless is not None:
            for tree in self._parentless:
                try:
                    return tree.get_parent(id)
                except EventIdNotInTree:
                    continue
        raise EventIdNotInTree(id)

    def get_full_path(self, id: str, field: str = None) -> List[Union[str, Th2Event]]:  # noqa: D412
        """Returns the full path for the event by its id in the right order.

        This method applicable only for trees (regular or parentless), not for detached events.

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
        if self._parentless is not None:
            for tree in self._parentless:
                try:
                    return tree.get_full_path(id, field)
                except EventIdNotInTree:
                    continue
        raise EventIdNotInTree(id)

    def get_ancestors(self, id: str) -> List[Th2Event]:
        """Returns all event's ancestors in right order.

        This method applicable only for trees (regular or parentless), not for detached events.

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
        if self._parentless is not None:
            for tree in self._parentless:
                try:
                    return tree.get_ancestors(id)
                except EventIdNotInTree:
                    continue
        raise EventIdNotInTree(id)

    def find_ancestor(self, id: str, filter: Callable) -> Optional[Th2Event]:
        """Finds the ancestor of an event.

        This method applicable only for trees (regular or parentless), not for detached events.

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
        if self._parentless is not None:
            for tree in self._parentless:
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

        This method applicable only for trees (regular or parentless), not for detached events.

        Args:
            filter: Filter function.
            stop: Stop function. If None searches for all nodes in the trees.
            max_count: Max count of matched events. Stops searching when `max_count` will be reached.

        Yields:
            Matching events.
        """

        def finder_wrapper(iterator):
            nonlocal max_count
            if max_count:
                for tree in iterator:
                    if max_count <= 0:
                        break
                    for node in tree.findall_iter(filter=filter, stop=stop, max_count=max_count):
                        if max_count <= 0:
                            break
                        yield node
                        max_count -= 1
            else:
                for tree in iterator:
                    yield from tree.findall_iter(filter=filter, stop=stop, max_count=max_count)

        yield from finder_wrapper(self._roots)
        if self._parentless is not None:
            yield from finder_wrapper(self._parentless)

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

        This method applicable only for trees (regular or parentless), not for detached events.

        Args:
            filter: Filter function.
            stop: Stop function. If None searches for all nodes in the trees.
            max_count: Max count of matched events. Stops searching when `max_count` will be reached.

        Returns:
            Matching events.
        """
        return list(self.findall_iter(filter=filter, stop=stop, max_count=max_count))

    def find(self, filter: Callable, stop: Callable = None) -> Optional[Th2Event]:
        """Searches the first event match.

        - The search uses 'filter' which is a filtering function.
        - Optionally, the search uses 'stop' which is a stopping function.
        If 'stop' function returns 'True' then search is complete.

        This method applicable only for trees (regular or parentless), not for detached events.

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
        if self._parentless is not None:
            for tree in self._parentless:
                event = tree.find(filter=filter, stop=stop)
                if event is not None:
                    return event
        return None

    def get_subtree(self, id: str) -> "EventTree":
        """Returns subtree of the event by its id.

        This method applicable only for trees (regular or parentless), not for detached events.

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
            except (EventIdNotInTree, NodeIDAbsentError):
                continue
        if self._parentless is not None:
            for tree in self._parentless:
                try:
                    return tree.get_subtree(id)
                except (EventIdNotInTree, NodeIDAbsentError):
                    continue
        raise EventIdNotInTree(id)

    def recover_unknown_events(self, preprocessor=None) -> None:
        """Loads missed events and finish tree building.

        Args:
            preprocessor: the function that will be executed for each recovered event before store.

        """
        previous_detached_events = list(self._detached_parent_ids())
        while previous_detached_events:
            events = self._driver.get_events_by_id_from_source(ids=self._detached_parent_ids())
            if preprocessor is not None:
                events = preprocessor(preprocessor)

            for event in events:
                if not self._driver.get_event_name(event) == self._driver.stub_event_name():
                    self.append_event(event)

            dp_ids = list(self._detached_parent_ids())
            if previous_detached_events == dp_ids:
                # If previous_detached_events == current, it means that we cannot recover some data.
                # So break iteration to escape recursive exception.
                break
            else:
                previous_detached_events = dp_ids

        if self._detached_nodes:
            w = "The collection were built with detached events because there are no some events in the source"
            warnings.warn(w)

    def get_parentless_tree_collection(self) -> "EventTreeCollection":
        """Builds and returns parentless trees by detached events as EventTreeCollection.

        Detached events will be removed from the collection.

        Returns:
            EventTreeCollection.
        """
        new_etc = self.__class__(self._driver)
        new_etc._roots = self.get_parentless_trees()
        return new_etc
