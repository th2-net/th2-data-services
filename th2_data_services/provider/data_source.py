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
    @property
    @abstractmethod
    def event_struct(self) -> IEventStruct:
        """Returns event structure class."""

    @property
    @abstractmethod
    def message_struct(self) -> IMessageStruct:
        """Returns message structure class."""

    @property
    @abstractmethod
    def event_stub(self) -> IEventStub:
        """Returns event stub template."""

    @property
    @abstractmethod
    def message_stub(self) -> IMessageStub:
        """Returns message stub template."""

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

    @abstractmethod
    @property
    def source_api(self) -> IHTTPProviderSourceAPI:
        pass


class IGRPCProviderDataSource(IProviderDataSource):
    @abstractmethod
    def command(self, cmd: IGRPCProviderCommand):
        pass

    @abstractmethod
    @property
    def source_api(self) -> IGRPCProviderSourceAPI:
        pass
