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
from typing import List, Dict, Optional

from treelib import Node, Tree

from th2_data_services import Data
from th2_data_services.events_tree import EventsTree
from th2_data_services.events_tree.events_trees_collection import EventsTreesCollection
from th2_data_services.provider.data_source import IProviderDataSource
from th2_data_services.provider.struct import IEventStruct
from th2_data_services.provider.v5.struct import provider5_event_struct


class ParentEventsTreesCollection(EventsTreesCollection):
    """ParentEventsTreeCollections is a class like an EventsTreeCollections.

    - ParentEventsTree contains all parent events that are referenced.
    - Approximately for 1 million events will be ~23 thousand parent events.
    """

    def __init__(
        self,
        data: Data,
        data_source: IProviderDataSource = None,
        preserve_body: bool = False,
        event_struct: IEventStruct = provider5_event_struct,
        event_stub_builder=None,
    ):
        """Args:
        data: Data
        data_source: Data Source
        preserve_body: If True then save body of event.
        event_struct: Event struct.
        event_stub_builder: Event Stub Builder.
        """
        self._preserve_body = preserve_body
        self._event_struct = event_struct
        self._event_stub_builder = event_stub_builder
        self._data_source = data_source

        self._roots: List[EventsTree] = []
        self._detached_nodes: Dict[Optional[str], List[Node]] = defaultdict(list)  # {parent_event_id: Node}
        self._unknown_ids: List[str]

        self._build_event_nodes(data)

    def _build_trees(self, nodes: Dict[Optional[str], List[Node]]) -> None:
        """Builds trees and saves detached events.

        Args:
            nodes: Events nodes.
        """
        roots = []
        for node in nodes[None]:
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
            current_tree: Tree for fill.
            parent_id: Parent even id.
        """
        for node in nodes[parent_id]:
            event_id: str = node.identifier
            if nodes.get(event_id):
                current_tree.add_node(node, parent=parent_id)
                self._fill_tree(nodes, current_tree, event_id)  # recursive fill
        nodes.pop(parent_id)
