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
from typing import Any

from grpc._channel import _InactiveRpcError

from typing import TYPE_CHECKING

from th2_data_services.provider.exceptions import CommandError
from th2_data_services.provider.interfaces import IEventStruct, IMessageStruct

if TYPE_CHECKING:
    from th2_data_services.provider.v6.interfaces.command import IGRPCProvider6Command

from th2_data_services.provider.interfaces.data_source import IGRPCProviderDataSource

#LOG import logging

from th2_data_services.provider.interfaces.stub_builder import IEventStub, IMessageStub
from th2_data_services.provider.v6.provider_api import GRPCProvider6API
from th2_data_services.provider.v6.struct import (
    HTTPProvider6EventStruct,
    HTTPProvider6MessageStruct,
    grpc_provider6_message_struct,
    grpc_provider6_event_struct,
)
from th2_data_services.provider.v6.stub_builder import (
    provider6_event_stub_builder,
    provider6_message_stub_builder,
)

#LOG logger = logging.getLogger(__name__)


class GRPCProvider6DataSource(IGRPCProviderDataSource):
    """DataSource class which provide work with rpt-data-provider.

    Rpt-data-provider version: 6.x.y
    Protocol: GRPC
    """

    def __init__(
        self,
        url: str,
        event_struct: IEventStruct = grpc_provider6_event_struct,
        message_struct: IMessageStruct = grpc_provider6_message_struct,
        event_stub_builder: IEventStub = provider6_event_stub_builder,
        message_stub_builder: IMessageStub = provider6_message_stub_builder,
    ):
        """GRPCProvider6DataSource constructor.

        Args:
            url: Url of rpt-data-provider.
            event_struct: Event structure that is supplied by rpt-data-provider.
            message_struct: Message structure that is supplied by rpt-data-provider.
            event_stub_builder: Stub builder for broken events.
            message_stub_builder: Stub builder for broken messages.
        """
        super().__init__(
            url=url,
            event_struct=event_struct,
            message_struct=message_struct,
            event_stub_builder=event_stub_builder,
            message_stub_builder=message_stub_builder,
        )

        self.__provider_api = GRPCProvider6API(url)

#LOG         logger.info(url)

    def command(self, cmd: IGRPCProvider6Command) -> Any:
        """Execute the transmitted GRPC command.

        Args:
            cmd: GRPC Command.

        Returns:
            Any: Command response.

        Raises:
            CommandError: If the command was broken.
        """
        try:
            return cmd.handle(data_source=self)
        except _InactiveRpcError as info:
            raise CommandError(
                f"The command '{cmd.__class__.__name__}' was broken. Details of error:\n{info.details()}"
            )

    @property
    def source_api(self) -> GRPCProvider6API:
        """Returns Provider API."""
        return self.__provider_api

    @property
    def event_struct(self) -> HTTPProvider6EventStruct:
        """Returns event structure class."""
        return self._event_struct

    @property
    def message_struct(self) -> HTTPProvider6MessageStruct:
        """Returns message structure class."""
        return self._message_struct
