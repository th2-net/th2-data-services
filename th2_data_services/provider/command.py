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
from __future__ import annotations

from typing import Callable

from th2_data_services.provider.interfaces.command import IProviderCommand


class ProviderAdaptableCommand(IProviderCommand):
    def __init__(self):
        """Class to make Command classes adaptable."""
        self._workflow = []

    def apply_adapter(self, adapter: Callable) -> "ProviderAdaptableCommand":
        """Adds adapter to the Command workflow.

        Note, sequence that you will add adapters make sense.

        Args:
            adapter: Callable function that will be used as adapter.

        Returns:
            self
        """
        self._workflow.append(adapter)
        return self

    def _handle_adapters(self, data):
        for step in self._workflow:
            # TODO - known issue. If the previous adapter returns None
            #   the lib will raise exception
            #   This class will be remove in dev 2.0.0
            data = step(data)
        return data
