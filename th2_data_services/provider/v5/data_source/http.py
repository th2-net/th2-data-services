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

import logging

from th2_data_services.decode_error_handler import UNICODE_REPLACE_HANDLER
from typing import TYPE_CHECKING

from th2_data_services.provider.interfaces import IEventStub, IMessageStub

if TYPE_CHECKING:
    from th2_data_services.provider.v5.interfaces.command import IHTTPProvider5Command

from th2_data_services.provider.interfaces.data_source import IHTTPProviderDataSource
from th2_data_services.provider.v5.struct import (
    provider5_event_struct,
    provider5_message_struct,
    Provider5EventStruct,
    Provider5MessageStruct,
)
from th2_data_services.provider.v5.provider_api.http import HTTPProvider5API
from th2_data_services.provider.v5.stub_builder import Provider5EventStubBuilder, Provider5MessageStubBuilder

logger = logging.getLogger("th2_data_services")
logger.setLevel(logging.DEBUG)


class HTTPProvider5DataSource(IHTTPProviderDataSource):
    """DataSource class which provide work with rpt-data-provider.

    Rpt-data-provider version: 5.x.y
    Protocol: HTTP
    """

    def __init__(
        self,
        url: str,
        chunk_length: int = 65536,
        char_enc: str = "utf-8",
        decode_error_handler: str = UNICODE_REPLACE_HANDLER,
        event_struct: Provider5EventStruct = provider5_event_struct,
        message_struct: Provider5MessageStruct = provider5_message_struct,
        event_stub_builder: IEventStub = None,
        message_stub_builder: IMessageStub = None,
        check_connect_timeout: (int, float) = 5,
    ):
        """HTTPProvider5DataSource constructor.

        Args:
            url: HTTP data source url.
            check_connect_timeout: How many seconds to wait for the server to send data before giving up.
            chunk_length: How much of the content to read in one chunk.
            char_enc: Encoding for the byte stream.
            decode_error_handler: Registered decode error handler.
            event_struct: Event structure that is supplied by rpt-data-provider.
            message_struct: Message structure that is supplied by rpt-data-provider.
            event_stub_builder: Stub builder for broken events. Provider5EventStubBuilder by default.
            message_stub_builder: Stub builder for broken messages. Provider5MessageStubBuilder by default.
        """
        super().__init__(
            url=url,
            event_struct=event_struct,
            message_struct=message_struct,
            event_stub_builder=Provider5EventStubBuilder() if event_stub_builder is None else event_stub_builder,
            message_stub_builder=Provider5MessageStubBuilder()
            if message_stub_builder is None
            else message_stub_builder,
        )

        self._char_enc = char_enc
        self._decode_error_handler = decode_error_handler
        self.__chunk_length = chunk_length
        self.check_connect(check_connect_timeout)
        self._provider_api = HTTPProvider5API(url, chunk_length, decode_error_handler, char_enc)

        logger.info(url)

    def command(self, cmd: IHTTPProvider5Command):
        """HTTP Provider5 command processor.

        Args:
            cmd: The command of data source to execute.

        Returns:
            Data source command result.
        """
        try:
            return cmd.handle(data_source=self)
        except Exception as e:
            raise ValueError(f"A command has broken. Details of error:\n{e}")

    @property
    def source_api(self) -> HTTPProvider5API:
        """HTTP Provider5 API."""
        return self._provider_api
