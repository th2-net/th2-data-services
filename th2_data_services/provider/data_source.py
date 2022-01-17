from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from th2_data_services.command import IGRPCProviderCommand, IHTTPProviderCommand, IProviderCommand
    from th2_data_services.source_api import (
        IProviderSourceAPI,
        IHTTPProviderSourceAPI,
        IGRPCProviderSourceAPI,
        IEventStruct,
        IMessageStruct,
        IEventStub,
        IMessageStub,
    )
    from th2_data_services.data_source import IDataSource


class IProviderDataSource(IDataSource):
    def __init__(
        self,
        url: str,
        event_struct: IEventStruct,
        message_struct: IMessageStruct,
        event_stub_builder: IEventStub,
        message_stub_builder: IMessageStub,
    ):
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
    def event_stub(self) -> IEventStub:
        """Returns event stub template."""
        return self._event_stub_builder

    @property
    def message_stub(self) -> IMessageStub:
        """Returns message stub template."""
        return self._message_stub_builder

    @abstractmethod
    def command(self, cmd: IProviderCommand):
        pass

    @property
    @abstractmethod
    def source_api(self) -> IProviderSourceAPI:
        pass


class IHTTPProviderDataSource(IProviderDataSource):
    @abstractmethod
    def command(self, cmd: IHTTPProviderCommand):
        pass

    @property
    @abstractmethod
    def source_api(self) -> IHTTPProviderSourceAPI:
        pass


class IGRPCProviderDataSource(IProviderDataSource):
    @abstractmethod
    def command(self, cmd: IGRPCProviderCommand):
        pass

    @property
    @abstractmethod
    def source_api(self) -> IGRPCProviderSourceAPI:
        pass
