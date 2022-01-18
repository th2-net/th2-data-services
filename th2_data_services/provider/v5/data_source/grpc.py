from th2_data_services.command import IGRPCProviderCommand
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
    def __init__(
        self,
        url: str,
        event_struct: Provider5EventStruct = provider5_event_struct,
        message_struct: Provider5MessageStruct = provider5_message_struct,
        event_stub_builder: IEventStub = provider5_event_stub_builder,
        message_stub_builder: IMessageStub = provider5_message_stub_builder,
    ):
        super().__init__(
            url=url,
            event_struct=event_struct,
            message_struct=message_struct,
            event_stub_builder=event_stub_builder,
            message_stub_builder=message_stub_builder,
        )

        self.__provider_api = GRPCProvider5API(url)

        logger.info(url)

    def command(self, cmd: IGRPCProviderCommand):
        return cmd.handle(data_source=self)

    @property
    def source_api(self) -> GRPCProvider5API:
        return self.__provider_api
