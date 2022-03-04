from typing import Union, Iterable, Generator, List, Callable, Optional, Tuple

import treelib

Data = Union[Iterable, Generator]
EventStruct = dict

"""
Examples

In [36]: tree.show()
Harry
├── Bill
└── Jane
    ├── Diane
    │   └── Mary
    └── Mark
    
    
tree.subtree('jane').show()
Jane
├── Diane
│   └── Mary
└── Mark


Event Id in the tree
In [14]: tree.contains('e22dd3fe-98ac-11ec-970e-712ca9ad16c9')
Out[14]: True
In [15]: 'e22dd3fe-98ac-11ec-970e-712ca9ad16c9' in tree
Out[15]: True

In [42]: tree.children('harry')
Out[42]: 
[Node(tag=Jane, identifier=jane, data=None),
 Node(tag=Bill, identifier=bill, data=None)]


# Returns the children (IDs) list of nid. - only one level
In [77]: tree.is_branch('jane')
Out[77]: ['diane', 'e22dd3fe-98ac-11ec-970e-712ca9ad16c9']


# Returns all nodes ids from putted to root
In [83]: list(tree.rsearch('diane'))
Out[83]: ['diane', 'jane', 'harry']

# All nodes for the tree or subtree
tree.all_nodes()
Out[85]: 
[Node(tag=Harry, identifier=harry, data=None),
 Node(tag=Jane, identifier=jane, data=None),
 Node(tag=Bill, identifier=bill, data=None),
 Node(tag=Diane, identifier=diane, data=None),
 Node(tag=Mary, identifier=e22dd3fd-98ac-11ec-970e-712ca9ad16c9, data=None),
 Node(tag=Mark, identifier=e22dd3fe-98ac-11ec-970e-712ca9ad16c9, data=None)]

---------- 01.03.2022

event = tree['id']
tree.is_root('id')
tree.is_leaf('id')

tree_collection.is_root('id')  # Ok
tree_collection.is_leaf('id')  # Ok 

# subtree 
Just create new EventsTree
tree.get_subtree('id')
tree_collection.get_subtree('id')

# children
tree.children('harry') -> [onlt children]
tree_collection.children('harry') -> [onlt children]

# All nodes for the tree or subtree (perhaps as generators)
tree.all_events() -> [Event]
tree_collection.all_events() -> [Event]

# Ancestor




"""


class EventsTreesCollection:
    """Builds events trees and keep them."""

    def __init__(self, data: Data, datasource, preserve_body: bool, event_struct: EventStruct, event_stub_builder):
        _roots: List[EventsTree] = []
        _unknown_ids: List[str]

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
    def __init__(self, treelib_tree: treelib.Tree):
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
