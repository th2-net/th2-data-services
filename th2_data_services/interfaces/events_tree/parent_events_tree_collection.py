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


from th2_data_services import Data
from th2_data_services.events_tree.events_tree import EventsTree
from th2_data_services.interfaces.events_tree.events_tree_collection import EventsTreeCollection
from th2_data_services.provider.interfaces.data_source import IProviderDataSource


class ParentEventsTreeCollection(EventsTreeCollection):
    """ParentEventsTreeCollections is a class like an EventsTreeCollections.

    ParentEventsTree contains all parent events that are referenced.
    """

    def __init__(
        self,
        data: Data,
        data_source: IProviderDataSource = None,
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

    def _build_trees(self, events_store: Dict[Optional[str], List[dict]]) -> None:
        """Builds trees and saves detached events.

        Args:
            events_store: Events nodes.
        """
        roots = []
        for event in events_store[None]:  # None - is parent_event_id for root events.
            event_id, event_name = self._get_event_id(event), self._get_event_name(event)
            if events_store[event_id]:
                tree = EventsTree()
                tree.create_root_event(event_name=event_name, event_id=event_id, data=event)
                roots.append(tree)
                self._fill_tree(events_store, tree, event_id)
        events_store.pop(None)

        self._roots = roots
        self._detached_nodes = events_store

    def _fill_tree(
        self, events_store: Dict[Optional[str], List[dict]], current_tree: EventsTree, parent_id: str
    ) -> None:
        """Fills tree recursively.

        Args:
            events_store: Events nodes.
            current_tree: Tree for fill.
            parent_id: Parent even id.
        """
        for event in events_store[parent_id]:
            event_id, event_name = self._get_event_id(event), self._get_event_name(event)
            if events_store.get(event_id):
                current_tree.append_event(event_name=event_name, event_id=event_id, parent_id=parent_id, data=event)
                self._fill_tree(events_store, current_tree, event_id)  # recursive fill
        events_store.pop(parent_id)
