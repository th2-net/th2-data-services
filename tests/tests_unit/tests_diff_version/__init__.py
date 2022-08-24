from importlib_metadata import version, PackageNotFoundError

v = version("th2_grpc_data_provider")
DEMO_PORT = "31789"  # GRPC provider v6

if v == "1.1.0":  # v6
    from th2_data_services.provider.v6.data_source.http import HTTPProvider6DataSource as HTTPProviderDataSource  # noqa
    from th2_data_services.provider.v6.commands import http  # noqa
    from th2_data_services.provider.v6.filters.filter import Provider6Filter as Filter  # noqa
    from th2_data_services.provider.v6.provider_api import HTTPProvider6API as HTTPProviderAPI  # noqa
    from th2_data_services.provider.v6.adapters.message_adapters import CodecPipelinesAdapter  # noqa

    DEMO_PORT = "31788"  # HTTP provider v6

elif v == "0.0.4":  # v5
    from th2_data_services.provider.v5.data_source.http import HTTPProvider5DataSource as HTTPProviderDataSource  # noqa
    from th2_data_services.provider.v5.commands import http  # noqa
    from th2_data_services.provider.v5.provider_api import HTTPProvider5API as HTTPProviderAPI  # noqa
    from th2_data_services.provider.v5.adapters.message_adapters import CodecPipelinesAdapter  # noqa
    from th2_data_services.filter import Filter  # noqa

    DEMO_PORT = "31787"  # HTTP provider v5
