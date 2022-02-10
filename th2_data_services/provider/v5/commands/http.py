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
from typing import List

from th2_data_services.provider.v5.command import IHTTPProvider5Command
from th2_data_services.provider.v5.data_source.http import HTTPProvider5DataSource


class GetEventById(IHTTPProvider5Command):
    def __init__(self, id: str):
        self._id = id

    def handle(self, data_source: HTTPProvider5DataSource):
        pass


class GetEventsById(IHTTPProvider5Command):
    def __init__(self, ids: List[str]):
        self._ids: ids

    def handle(self, data_source: HTTPProvider5DataSource):
        pass
