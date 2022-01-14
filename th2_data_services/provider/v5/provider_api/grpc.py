import logging

from th2_data_services.source_api import IGRPCProviderSourceAPI

logger = logging.getLogger("th2_data_services")
logger.setLevel(logging.DEBUG)


class GRPCProvider5API(IGRPCProviderSourceAPI):
    """It will be made by Sviatoslav"""
