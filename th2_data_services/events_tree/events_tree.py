from typing import List, Tuple

from treelib import Tree

from th2_data_services import Data
from th2_data_services.provider.struct import IEventStruct


class EventsTreesCollection:
    """Builds events trees and keep them."""

    def __init__(self, data: Data, datasource, preserve_body: bool, event_struct: IEventStruct, event_stub_builder):
        self._roots: List[EventsTree] = []
        self._unknown_ids: List[str]

    def get_roots_ids(self):
        """"""

    def get_trees(self):
        pass

    def get_root_by_id(self, id):
        pass


class UnlinkedEventsTreeCollection:
    # TODO - think the name!!!!
    pass


class EventsTree:
    def __init__(self, treelib_tree: Tree):
        self._treelib_tree = treelib_tree

    def get_event(self, id) -> dict:
        pass

    # def __getitem__(self, item):
    #     pass

    def get_leaves(self):
        pass

    def get_children(self, id: str) -> Tuple[dict]:
        """Gets children for a event.

        Args:
            event: Event.
        """

    def get_children_iter(self, id: str) -> Tuple[dict]:
        pass

    def get_parent(self, id: str) -> dict:
        """Gets parent for an event."""

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

    def findall(node, filter_=None, stop=None, maxlevel=None, mincount=None, maxcount=None):
        pass

    def findall_by_field(node, value, name="name", maxlevel=None, mincount=None, maxcount=None):
        pass

    def find(node, filter_=None, stop=None, maxlevel=None):
        pass

    def find_by_field(node, value, name="name", maxlevel=None):
        pass

    def get_ancestor_by_filter(self, event: dict, filter: Callable) -> Optional[dict]:
        """Gets event ancestor by condition.

        Args:
            event: Event.
            filter: filter function that has one argument - ancestor event.
        """

    def get_ancestors(self):
        # list(tree.rsearch('diane'))
        pass

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
