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

#LOG import logging

from th2_data_services.decode_error_handler import UNICODE_REPLACE_HANDLER
from typing import TYPE_CHECKING

from th2_data_services.provider.exceptions import CommandError
from th2_data_services.provider.interfaces import IEventStruct, IMessageStruct, IEventStub, IMessageStub

if TYPE_CHECKING:
    from th2_data_services.provider.v5.interfaces.command import IHTTPProvider5Command

from th2_data_services.provider.interfaces.data_source import IHTTPProviderDataSource
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
from th2_data_services.provider.v5.provider_api.http import HTTPProvider5API

#LOG logger = logging.getLogger(__name__)


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
        event_struct: IEventStruct = provider5_event_struct,
        message_struct: IMessageStruct = provider5_message_struct,
        event_stub_builder: IEventStub = provider5_event_stub_builder,
        message_stub_builder: IMessageStub = provider5_message_stub_builder,
        check_connect_timeout: (int, float) = 5,
        use_ssl: bool = True,
    ):
        """HTTPProvider5DataSource constructor.

        Args:
            url: HTTP data source url.
            check_connect_timeout: How many seconds to wait for the server to send data before giving up.
            chunk_length: How much of the content to read in one chunk.
            char_enc: Encoding for the byte stream.
            decode_error_handler: Registered decode error handler.
            event_struct: Struct of event from rpt-data-provider.
            message_struct: Struct of message from rpt-data-provider.
            event_stub_builder: Stub for event.
            message_stub_builder: Stub for message.
            use_ssl: Checking SSL/TSL certification.
        """
        super().__init__(url, event_struct, message_struct, event_stub_builder, message_stub_builder)

        self._char_enc = char_enc
        self._decode_error_handler = decode_error_handler
        self.__chunk_length = chunk_length
        self._use_ssl = use_ssl
        self.check_connect(check_connect_timeout, use_ssl)
        self._provider_api = HTTPProvider5API(
            url=url,
            chunk_length=chunk_length,
            decode_error_handler=decode_error_handler,
            char_enc=char_enc,
            use_ssl=use_ssl,
        )

#LOG         logger.info(url)

    def command(self, cmd: IHTTPProvider5Command):
        """HTTP Provider5 command processor.

        Args:
            cmd: The command of data source to execute.

        Returns:
            Data source command result.

        Raises:
            CommandError: If the command was broken.
        """
        try:
            return cmd.handle(data_source=self)
        except Exception as e:
            raise CommandError(f"The command '{cmd.__class__.__name__}' was broken. Details of error:\n{e}")

    @property
    def source_api(self) -> HTTPProvider5API:
        """HTTP Provider5 API."""
        return self._provider_api

    @property
    def event_struct(self) -> Provider5EventStruct:
        """Returns event structure class."""
        return self._event_struct

    @property
    def message_struct(self) -> Provider5MessageStruct:
        """Returns message structure class."""
        return self._message_struct
