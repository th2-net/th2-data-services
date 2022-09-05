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


"""Interfaces for Provider Data Source."""

from abc import abstractmethod

import requests
import urllib3

from th2_data_services.provider.interfaces.command import IGRPCProviderCommand, IHTTPProviderCommand, IProviderCommand
from th2_data_services.interfaces.data_source import IDataSource
from th2_data_services.provider.interfaces.source_api import (
    IHTTPProviderSourceAPI,
    IGRPCProviderSourceAPI,
    IProviderSourceAPI,
)
from th2_data_services.provider.interfaces.struct import IEventStruct, IMessageStruct
from th2_data_services.provider.interfaces.stub_builder import IEventStub, IMessageStub


class IProviderDataSource(IDataSource):
    def __init__(
        self,
        url: str,
        event_struct: IEventStruct,
        message_struct: IMessageStruct,
        event_stub_builder: IEventStub,
        message_stub_builder: IMessageStub,
    ):
        """Interface of DataSource that provides work with rpt-data-provider.

        Args:
            url: Url address to data provider.
            event_struct: Event struct class.
            message_struct: Message struct class.
            event_stub_builder: Event stub builder class.
            message_stub_builder: Message stub builder class.
        """
        if url[-1] == "/":
            url = url[:-1]
        self._url = url
        self._event_struct = event_struct
        self._message_struct = message_struct
        self._event_stub_builder = event_stub_builder
        self._message_stub_builder = message_stub_builder

    @property
    def url(self) -> str:
        """str: URL of rpt-data-provider."""
        return self._url

    @property
    def event_struct(self) -> IEventStruct:
        """Returns event structure class."""
        return self._event_struct

    @property
    def message_struct(self) -> IMessageStruct:
        """Returns message structure class."""
        return self._message_struct

    @property
    def event_stub_builder(self) -> IEventStub:
        """Returns event stub template."""
        return self._event_stub_builder

    @property
    def message_stub_builder(self) -> IMessageStub:
        """Returns message stub template."""
        return self._message_stub_builder

    @abstractmethod
    def command(self, cmd: IProviderCommand):
        """Execute the transmitted command."""

    @property
    @abstractmethod
    def source_api(self) -> IProviderSourceAPI:
        """Returns Provider API."""


class IHTTPProviderDataSource(IProviderDataSource):
    """Interface of DataSource that provides work with rpt-data-provider via HTTP."""

    @abstractmethod
    def command(self, cmd: IHTTPProviderCommand):
        """Execute the transmitted HTTP command."""

    def check_connect(self, timeout: (int, float), certification: bool = True) -> None:
        """Checks whether url is working.

        Args:
            timeout: How many seconds to wait for the server to send data before giving up.
            certification: Checking SSL certification.

        Raises:
            urllib3.exceptions.HTTPError: If unable to connect to host.
        """
        try:
            requests.get(self.url, timeout=timeout, verify=certification)
        except ConnectionError as error:
            raise urllib3.exceptions.HTTPError(f"Unable to connect to host '{self.url}'\nReason: {error}")

    @property
    @abstractmethod
    def source_api(self) -> IHTTPProviderSourceAPI:
        """Returns HTTP Provider API."""


class IGRPCProviderDataSource(IProviderDataSource):
    """Interface of DataSource that provides work with rpt-data-provider via GRPC."""

    @abstractmethod
    def command(self, cmd: IGRPCProviderCommand):
        """Execute the transmitted GRPC command."""

    @property
    @abstractmethod
    def source_api(self) -> IGRPCProviderSourceAPI:
        """Returns GRPC Provider API."""
