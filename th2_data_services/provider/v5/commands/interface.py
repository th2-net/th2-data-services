from abc import abstractmethod

from th2_data_services.command import IHTTPProviderCommand
from th2_data_services.provider.v5.data_source.http import HTTPProvider5DataSource


class IHTTPProvider5Command(IHTTPProviderCommand):
    @abstractmethod
    def handle(self, data_source: HTTPProvider5DataSource):
        pass
