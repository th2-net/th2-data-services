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

import requests
import urllib3
import logging

from th2_data_services.decode_error_handler import UNICODE_REPLACE_HANDLER
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from th2_data_services.provider.v5.command import IHTTPProvider5Command
    from th2_data_services.provider.v5.provider_api.http import HTTPProvider5API

from th2_data_services.provider.data_source import IHTTPProviderDataSource
from th2_data_services.provider.v5.struct import (
    provider5_event_struct,
    provider5_message_struct,
)
from th2_data_services.provider.v5.stub_builder import (
    provider5_event_stub_builder,
    provider5_message_stub_builder,
)

logger = logging.getLogger("th2_data_services")
logger.setLevel(logging.DEBUG)


class HTTPProvider5DataSource(IHTTPProviderDataSource):
    def __init__(
        self,
        url: str,
        chunk_length: int = 65536,
        char_enc: str = "utf-8",
        decode_error_handler: str = UNICODE_REPLACE_HANDLER,
        event_struct=provider5_event_struct,
        message_struct=provider5_message_struct,
        event_stub_builder=provider5_event_stub_builder,
        message_stub_builder=provider5_message_stub_builder,
    ):
        """

        Args:
            url: HTTP data source url.
            chunk_length: How much of the content to read in one chunk.
            char_enc: Encoding for the byte stream.
            decode_error_handler: Registered decode error handler.
        """
        super().__init__(url, event_struct, message_struct, event_stub_builder, message_stub_builder)

        self._char_enc = char_enc
        self._decode_error_handler = decode_error_handler
        self.__chunk_length = chunk_length
        self.__check_connect()
        self._provider_api = HTTPProvider5API()

        logger.info(url)

    def __check_connect(self) -> None:
        """Checks whether url is working."""
        try:
            requests.get(self.url, timeout=5.0)
        except ConnectionError as error:
            raise urllib3.exceptions.HTTPError(f"Unable to connect to host '{self.url}'\nReason: {error}")

    def command(self, cmd: IHTTPProvider5Command):
        return cmd.handle(data_source=self)

    @property
    def source_api(self) -> HTTPProvider5API:
        return self._provider_api
