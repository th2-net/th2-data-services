from importlib.metadata import version, PackageNotFoundError

v = version("th2_grpc_data_provider")
PORT = "31789"  # GRPC provider v6

if v == "1.1.0":  # v6
    from th2_data_services.provider.v6.data_source.http import HTTPProvider6DataSource as HTTPProviderDataSource  # noqa
    from th2_data_services.provider.v6.data_source.grpc import GRPCProvider6DataSource as GRPCProviderDataSource
    from th2_data_services.provider.v6.commands import http, grpc  # noqa
    
    from th2_data_services.provider.v6.filters.filter import Provider6Filter as Filter  # noqa
    from th2_data_services.provider.v6.provider_api import HTTPProvider6API as HTTPProviderAPI  # noqa
    from th2_data_services.provider.v6.adapters.message_adapters import CodecPipelinesAdapter  # noqa



    HTTP_PORT = "31788"  # HTTP provider v6

elif v == "0.1.6":  # v5
    from th2_data_services.provider.v5.data_source.http import HTTPProvider5DataSource as HTTPProviderDataSource  # noqa
    from th2_data_services.provider.v5.data_source.grpc import GRPCProvider5DataSource as GRPCProviderDataSource
    from th2_data_services.provider.v5.commands import http, grpc  # noqa
    from th2_data_services.provider.v5.provider_api import HTTPProvider5API as HTTPProviderAPI  # noqa
    from th2_data_services.provider.v5.adapters.message_adapters import CodecPipelinesAdapter  # noqa
    from th2_data_services.filter import Filter  # noqa

    HTTP_PORT = "31915"  # HTTP provider v5
    GRPC_PORT = "31916"

