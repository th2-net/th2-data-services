from abc import ABC, abstractmethod

from th2_data_services.provider.data_source import (
    IDataSource,
    IProviderDataSource,
    IHTTPProviderDataSource,
    IGRPCProviderDataSource,
)


class ICommand(ABC):
    @abstractmethod
    def handle(self, data_source: IDataSource):
        pass


class IProviderCommand(ICommand):
    @abstractmethod
    def handle(self, data_source: IProviderDataSource):
        pass


class IHTTPProviderCommand(IProviderCommand):
    @abstractmethod
    def handle(self, data_source: IHTTPProviderDataSource):
        pass


class IGRPCProviderCommand(IProviderCommand):
    @abstractmethod
    def handle(self, data_source: IGRPCProviderDataSource):
        pass
