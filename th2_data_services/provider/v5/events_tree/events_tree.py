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
from typing import Union

from th2_data_services import Data
from th2_data_services.events_tree import EventsTreesCollection
from th2_data_services.provider.struct import IEventStruct
from th2_data_services.provider.v5.command_resolver import resolver_get_events_by_id
from th2_data_services.provider.v5.data_source import HTTPProvider5DataSource, GRPCProvider5DataSource
from th2_data_services.provider.v5.struct import provider5_event_struct


class EventsTreesCollectionProvider5(EventsTreesCollection):
    """EventsTreesCollections for data-provider v5."""

    def __init__(
        self,
        data: Data,
        data_source: Union[GRPCProvider5DataSource, HTTPProvider5DataSource] = None,
        preserve_body: bool = False,
        event_struct: IEventStruct = provider5_event_struct,
        stub: bool = False,
    ):
        super().__init__(data=data, preserve_body=preserve_body, event_struct=event_struct)
        self._stub_status = stub
        self._data_source = data_source
        self._broken_events = []

        self._recover_unknown_events()

    def _recover_unknown_events(self) -> None:
        """Loads missed events and recover events."""
        instance_command = resolver_get_events_by_id(self._data_source)

        previous_detached_events = list(self.detached_events.keys())
        while previous_detached_events:
            called_command = instance_command(self.detached_events.keys())
            if self._stub_status:
                called_command.use_stub()

            events = self._data_source.command(called_command)

            for event in events:
                if not event.get(self._event_struct.NAME) == "Broken_Event":
                    self.append_element(event)

            if previous_detached_events == list(self.detached_events.keys()):
                break
            previous_detached_events = list(self.detached_events.keys())
