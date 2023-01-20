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
from th2_data_services.events_tree.event_tree import EventTree
from th2_data_services.events_tree.event_tree_collection import EventTreeCollection


class ParentEventTreeCollection(EventTreeCollection):
    """ParentEventTreeCollections is a class like an EventsTreeCollections.

    ParentEventsTree contains all parent events that are referenced.
    """

    def _build_trees(self, events_nodes: Dict[Optional[str], List[dict]]) -> None:
        """Builds trees and saves detached events.

        Args:
            events_nodes: Events nodes.
        """
        roots = []
        for event in events_nodes[None]:  # None - is parent_event_id for root events.
            event_id, event_name = self._driver.get_event_id(event), self._driver.get_event_name(event)
            if events_nodes[event_id]:
                tree = EventTree(event_name=event_name, event_id=event_id, data=event)
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
        for event in events_store[parent_id]:
            event_id, event_name = self._driver.get_event_id(event), self._driver.get_event_name(event)
            if events_store.get(event_id):
                current_tree.append_event(event_name=event_name, event_id=event_id, parent_id=parent_id, data=event)
                self._fill_tree(events_store, current_tree, event_id)  # recursive fill
        events_store.pop(parent_id)
