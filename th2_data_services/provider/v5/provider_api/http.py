import logging

from th2_data_services.source_api import IHTTPProviderSourceAPI

logger = logging.getLogger("th2_data_services")
logger.setLevel(logging.DEBUG)


class HTTPProvider5API(IHTTPProviderSourceAPI):
    """It will be made by Grigory"""
