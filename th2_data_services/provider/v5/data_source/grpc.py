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

if TYPE_CHECKING:
    from th2_data_services.provider.v5.command import IGRPCProvider5Command

from th2_data_services.provider.data_source import IGRPCProviderDataSource

import logging

from th2_data_services.provider.stub_builder import IEventStub, IMessageStub
from th2_data_services.provider.v5.provider_api import GRPCProvider5API
from th2_data_services.provider.v5.struct import (
    provider5_event_struct,
    provider5_message_struct,
    Provider5EventStruct,
    Provider5MessageStruct,
)
from th2_data_services.provider.v5.stub_builder import (
    provider5_event_stub_builder,
    provider5_message_stub_builder,
)

logger = logging.getLogger("th2_data_services")
logger.setLevel(logging.DEBUG)


class GRPCProvider5DataSource(IGRPCProviderDataSource):
    """DataSource class which provide work with rpt-data-provider.

    Rpt-data-provider version: 5.x.y
    Protocol: GRPC
    """

    def __init__(
        self,
        url: str,
        event_struct: Provider5EventStruct = provider5_event_struct,
        message_struct: Provider5MessageStruct = provider5_message_struct,
        event_stub_builder: IEventStub = provider5_event_stub_builder,
        message_stub_builder: IMessageStub = provider5_message_stub_builder,
    ):
        """
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

        self.__provider_api = GRPCProvider5API(url)

        logger.info(url)

    def command(self, cmd: IGRPCProvider5Command) -> Any:
        """Execute the transmitted GRPC command.

        Args:
            cmd: GRPC Command.

        Returns:
            Any: Command response.

        Raises:
            ValueError: If command has broken.
        """
        try:
            return cmd.handle(data_source=self)
        except _InactiveRpcError as info:
            raise ValueError(f"A command has broken. Details of error:\n{info.details()}")

    @property
    def source_api(self) -> GRPCProvider5API:
        """Returns Provider API."""
        return self.__provider_api
