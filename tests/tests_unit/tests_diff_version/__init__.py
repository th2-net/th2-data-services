from importlib_metadata import version

v = version("th2_grpc_data_provider")
DEMO_PORT = "31789"  # GRPC provider v6

if v == "1.1.0":  # v6
    from bin_package.th2_data_services.provider.v6.data_source.http import (
        HTTPProvider6DataSource as HTTPProviderDataSource,
    )  # noqa
    from bin_package.th2_data_services.provider.v6.filters.filter import Provider6Filter as Filter  # noqa
    from bin_package.th2_data_services.provider import HTTPProvider6API as HTTPProviderAPI  # noqa
    from bin_package.th2_data_services.provider import CodecPipelinesAdapter  # noqa

    DEMO_PORT = "31788"  # HTTP provider v6

elif v == "0.0.4":  # v5
    from bin_package.th2_data_services.provider.v5.data_source.http import (
        HTTPProvider5DataSource as HTTPProviderDataSource,
    )  # noqa
    from bin_package.th2_data_services.provider import http  # noqa
    from bin_package.th2_data_services.provider.v5 import HTTPProvider5API as HTTPProviderAPI  # noqa
    from bin_package.th2_data_services.provider.v5.adapters.message_adapters import CodecPipelinesAdapter  # noqa
    from bin_package.th2_data_services.filter import Filter  # noqa

    DEMO_PORT = "31787"  # HTTP provider v5
