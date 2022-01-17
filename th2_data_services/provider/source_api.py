from th2_data_services.source_api import ISourceAPI


class IProviderSourceAPI(ISourceAPI):
    pass


class IHTTPProviderSourceAPI(IProviderSourceAPI):
    pass


class IGRPCProviderSourceAPI(IProviderSourceAPI):
    pass
