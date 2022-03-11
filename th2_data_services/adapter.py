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

from abc import ABC, abstractmethod
from typing import Any


class IAdapter(ABC):
    """High level interface for Adapter."""

    @abstractmethod
    def handle(self, record: Any) -> Any:
        pass


class IMessageAdapter(IAdapter):
    """Interface of Adapter for messages."""

    @abstractmethod
    def handle(self, message: dict) -> Any:
        pass


class IEventAdapter(IAdapter):
    """Interface of Adapter for events."""

    @abstractmethod
    def handle(self, event: dict) -> Any:
        pass
