from datetime import datetime
from importlib.metadata import version, PackageNotFoundError

v = version("th2_grpc_data_provider")

STREAM_1 = "ds-lib-session1"
STREAM_2 = "ds-lib-session2"

if v == "1.1.0":  # v6
    from th2_data_services.provider.v6.data_source.http import HTTPProvider6DataSource as HTTPProviderDataSource  # noqa
    from th2_data_services.provider.v6.data_source.grpc import GRPCProvider6DataSource as GRPCProviderDataSource
    from th2_data_services.provider.v6.commands import http, grpc  # noqa    
    from th2_data_services.provider.v6.filters.filter import Provider6Filter as Filter  # noqa
    from th2_data_services.provider.v6.provider_api import HTTPProvider6API as HTTPProviderAPI  # noqa
    from th2_data_services.provider.v6.adapters.message_adapters import CodecPipelinesAdapter  # noqa

    from .test_bodies.v6 import all_test_event_bodies, all_test_message_bodies

    EVENT_ID_TEST_DATA_ROOT = 'a26078a4-6419-11ed-bfec-b48c9dc9ebfb'
    EVENT_ID_PLAIN_EVENT_1 = 'a275f396-6419-11ed-a9e6-b48c9dc9ebfb'
    EVENT_ID_PLAIN_EVENT_2 = 'a275f397-6419-11ed-b8a7-b48c9dc9ebfb'

    MESSAGE_ID_1 = 'ds-lib-session1:first:1668429677955474105'
    MESSAGE_ID_2 = 'ds-lib-session1:first:1668429677955474106'

    START_TIME = datetime(year=2022, month=11, day=14, hour=12, minute=41, second=12, microsecond=0)
    END_TIME   = datetime(year=2022, month=11, day=14, hour=12, minute=41, second=19, microsecond=0)


    HTTP_PORT = "31788"  # HTTP provider v6
    GRPC_PORT = "32419"

elif v == "0.1.6":  # v5
    from th2_data_services.provider.v5.data_source.http import HTTPProvider5DataSource as HTTPProviderDataSource  # noqa
    from th2_data_services.provider.v5.data_source.grpc import GRPCProvider5DataSource as GRPCProviderDataSource
    from th2_data_services.provider.v5.commands import http, grpc  # noqa
    from th2_data_services.provider.v5.provider_api import HTTPProvider5API as HTTPProviderAPI  # noqa
    from th2_data_services.provider.v5.adapters.message_adapters import CodecPipelinesAdapter  # noqa
    from th2_data_services.filter import Filter  # noqa

    from .test_bodies.v5 import all_test_event_bodies, all_test_message_bodies

    EVENT_ID_TEST_DATA_ROOT = '2479e531-6017-11ed-9d54-b48c9dc9ebfa'
    EVENT_ID_PLAIN_EVENT_1 = '24aae778-6017-11ed-b87c-b48c9dc9ebfa'
    EVENT_ID_PLAIN_EVENT_2 = '24aae779-6017-11ed-9cb4-b48c9dc9ebfa'

    MESSAGE_ID_1 = 'ds-lib-session1:first:1668068118435545201'
    MESSAGE_ID_2 = 'ds-lib-session1:first:1668068118435545202'

    START_TIME = datetime(year=2022, month=11, day=9, hour=10, minute=13, second=17, microsecond=0)
    END_TIME   = datetime(year=2022, month=11, day=10, hour=8, minute=15, second=20, microsecond=0)

    HTTP_PORT = "31915"  # HTTP provider v5
    GRPC_PORT = "31916"

