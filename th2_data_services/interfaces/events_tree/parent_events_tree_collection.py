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

from typing import Dict, List, Optional

from treelib import Node, Tree

from th2_data_services import Data
from th2_data_services.events_tree import EventsTree
from th2_data_services.interfaces.events_tree.events_tree_collection import EventsTreeCollection
from th2_data_services.interfaces import IDataSource


class ParentEventsTreeCollection(EventsTreeCollection):
    """ParentEventsTreeCollections is a class like an EventsTreeCollections.

    ParentEventsTree contains all parent events that are referenced.
    """

    def __init__(
        self,
        data: Data,
        data_source: IDataSource = None,
        preserve_body: bool = False,
        stub: bool = False,
    ):
        """ParentEventsTreeCollection constructor.

        Args:
            data: Data object.
            data_source: Data Source object.
            preserve_body: If True then save body of event.
            stub: If True it will create stub when event is broken.
        """
        super().__init__(data, data_source, preserve_body, stub)

    def _build_trees(self, nodes: Dict[Optional[str], List[Node]]) -> None:
        """Builds trees and saves detached events.

        Args:
            nodes: Events nodes.
        """
        roots = []
        for node in nodes[None]:  # None - is parent_event_id for root events.
            if nodes[node.identifier]:
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
            nodes: Events nodes.
            current_tree: Tree for fill.
            parent_id: Parent even id.
        """
        for node in nodes[parent_id]:
            event_id: str = node.identifier
            if nodes.get(event_id):
                current_tree.add_node(node, parent=parent_id)
                self._fill_tree(nodes, current_tree, event_id)  # recursive fill
        nodes.pop(parent_id)
