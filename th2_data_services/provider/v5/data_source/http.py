import requests
import urllib3


from th2_data_services.decode_error_handler import UNICODE_REPLACE_HANDLER


import logging

from th2_data_services.provider.data_source import IHTTPProviderDataSource
from th2_data_services.provider.v5.commands.interface import IHTTPProvider5Command
from th2_data_services.provider.v5.provider_api.http import HTTPProvider5API
from th2_data_services.provider.v5.struct import provider5_event_struct, provider5_message_struct
from th2_data_services.source_api import IEventStruct, IMessageStub, IEventStub, IMessageStruct

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
    ):
        """

        Args:
            url: HTTP data source url.
            chunk_length: How much of the content to read in one chunk.
            char_enc: Encoding for the byte stream.
            decode_error_handler: Registered decode error handler.
        """
        self.url = url
        self._char_enc = char_enc
        self._decode_error_handler = decode_error_handler
        self.__chunk_length = chunk_length
        self.__check_connect()
        self._provider_api = HTTPProvider5API()
        self._event_struct = event_struct
        self._message_struct = message_struct
        logger.info(url)

    @property
    def url(self) -> str:
        """str: URL of rpt-data-provider."""
        return self.__url

    @url.setter
    def url(self, url):
        if url[-1] == "/":
            url = url[:-1]
        self.__url = url

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

    @property
    def event_struct(self) -> IEventStruct:
        return self._event_struct

    @property
    def message_struct(self) -> IMessageStruct:
        return self._message_struct

    @property
    def event_stub(self) -> IEventStub:
        pass

    @property
    def message_stub(self) -> IMessageStub:
        pass
