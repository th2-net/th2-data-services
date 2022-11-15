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

    EVENT_ID_TEST_DATA_ROOT = '2479e531-6017-11ed-9d54-b48c9dc9ebfa'
    EVENT_ID_PLAIN_EVENT_1 = '24aae778-6017-11ed-b87c-b48c9dc9ebfa'
    EVENT_ID_PLAIN_EVENT_2 = '24aae779-6017-11ed-9cb4-b48c9dc9ebfa'
    MESSAGE_ID_1 = 'ds-lib-session1:first:1668068118435545201'
    MESSAGE_ID_2 = 'ds-lib-session1:first:1668068118435545202'

    HTTP_PORT = "31788"  # HTTP provider v6

elif v == "0.1.6":  # v5
    from th2_data_services.provider.v5.data_source.http import HTTPProvider5DataSource as HTTPProviderDataSource  # noqa
    from th2_data_services.provider.v5.data_source.grpc import GRPCProvider5DataSource as GRPCProviderDataSource
    from th2_data_services.provider.v5.commands import http, grpc  # noqa
    from th2_data_services.provider.v5.provider_api import HTTPProvider5API as HTTPProviderAPI  # noqa
    from th2_data_services.provider.v5.adapters.message_adapters import CodecPipelinesAdapter  # noqa
    from th2_data_services.filter import Filter  # noqa

    EVENT_ID_TEST_DATA_ROOT = '2479e531-6017-11ed-9d54-b48c9dc9ebfa'
    EVENT_ID_PLAIN_EVENT_1 = '24aae778-6017-11ed-b87c-b48c9dc9ebfa'
    EVENT_ID_PLAIN_EVENT_2 = '24aae779-6017-11ed-9cb4-b48c9dc9ebfa'
    MESSAGE_ID_1 = 'ds-lib-session1:first:1668068118435545201'
    MESSAGE_ID_2 = 'ds-lib-session1:first:1668068118435545202'

    HTTP_PORT = "31915"  # HTTP provider v5
    GRPC_PORT = "31916"

