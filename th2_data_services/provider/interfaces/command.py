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


"""Interfaces for Provider Commands."""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from th2_data_services.interfaces import ICommand

if TYPE_CHECKING:
    from th2_data_services.provider.interfaces.data_source import (
        IProviderDataSource,
        IHTTPProviderDataSource,
        IGRPCProviderDataSource,
    )


class IProviderCommand(ICommand):
    """Interface of command for rpt-data-provider."""

    @abstractmethod
    def handle(self, data_source: IProviderDataSource):
        pass


class IHTTPProviderCommand(IProviderCommand):
    """Interface of command for rpt-data-provider which works via HTTP."""

    @abstractmethod
    def handle(self, data_source: IHTTPProviderDataSource):
        pass


class IGRPCProviderCommand(IProviderCommand):
    """Interface of command for rpt-data-provider which works via GRPC."""

    @abstractmethod
    def handle(self, data_source: IGRPCProviderDataSource):
        pass
