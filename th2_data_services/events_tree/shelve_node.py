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

from treelib import Node


class ShelveNode(Node):
    def __init__(self, tag=None, identifier=None, expanded=True, data=None, shelve_file=None):
        self._shelve_file = shelve_file
        super().__init__(tag, identifier, expanded, data)

    @property
    def data(self) -> dict:
        return self._shelve_file[self.identifier]

    @data.setter
    def data(self, d: dict):
        self._shelve_file[self.identifier] = d