from th2_data_services.provider.v5.commands import IHTTPProvider5Command
from th2_data_services.provider.v5.data_source.http import HTTPProvider5DataSource


class GetEventById(IHTTPProvider5Command):
    def handle(self, data_source: HTTPProvider5DataSource):
        pass
