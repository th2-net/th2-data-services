from abc import ABC


class ISourceAPI(ABC):
    """High level interface for Source API."""


class IProviderSourceAPI(ISourceAPI):
    pass


class IHTTPProviderSourceAPI(IProviderSourceAPI):
    pass


class IGRPCProviderSourceAPI(IProviderSourceAPI):
    pass
