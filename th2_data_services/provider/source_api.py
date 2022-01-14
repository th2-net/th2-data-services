from abc import abstractmethod

from th2_data_services.source_api import ISourceAPI


class IProviderSourceAPI(ISourceAPI):
    # TODO - Do???
    @abstractmethod
    def build_event_stub(self, *args):
        pass

    # TODO - Do???
    @abstractmethod
    def build_message_stub(self, *args):
        pass


class IHTTPProviderSourceAPI(IProviderSourceAPI):
    pass


class IGRPCProviderSourceAPI(IProviderSourceAPI):
    pass
