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

from abc import abstractmethod

from th2_data_services.provider.interfaces.command import IHTTPProviderCommand, IGRPCProviderCommand
from th2_data_services.provider.v6.data_source.grpc import GRPCProvider6DataSource
from th2_data_services.provider.v6.data_source.http import HTTPProvider6DataSource


class IHTTPProvider6Command(IHTTPProviderCommand):
    """Interface of command for rpt-data-provider.

    Rpt-data-provider version: 5.x.y
    Protocol: HTTP
    """

    @abstractmethod
    def handle(self, data_source: HTTPProvider6DataSource):
        pass


class IGRPCProvider6Command(IGRPCProviderCommand):
    """Interface of command for rpt-data-provider.

    Rpt-data-provider version: 5.x.y
    Protocol: GRPC
    """

    @abstractmethod
    def handle(self, data_source: GRPCProvider6DataSource):
        pass
