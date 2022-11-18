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
    from th2_data_services.provider.v6.struct import http_provider6_message_struct as message_struct

    from .test_bodies.v6 import all_test_event_bodies, all_test_message_bodies

    EVENT_ID_TEST_DATA_ROOT = "a26078a4-6419-11ed-bfec-b48c9dc9ebfb"
    EVENT_ID_PLAIN_EVENT_1 = "a275f396-6419-11ed-a9e6-b48c9dc9ebfb"
    EVENT_ID_PLAIN_EVENT_2 = "a275f397-6419-11ed-b8a7-b48c9dc9ebfb"

    MESSAGE_ID_1 = "ds-lib-session1:first:1668429677955474105"
    MESSAGE_ID_2 = "ds-lib-session1:first:1668429677955474106"

    START_TIME = datetime(year=2022, month=11, day=14, hour=12, minute=41, second=12, microsecond=0)
    END_TIME = datetime(year=2022, month=11, day=14, hour=12, minute=41, second=19, microsecond=0)

    HTTP_PORT = "32154"  # HTTP provider v6
    GRPC_PORT = "32419"

elif v == "0.1.6":  # v5
    from th2_data_services.provider.v5.data_source.http import HTTPProvider5DataSource as HTTPProviderDataSource  # noqa
    from th2_data_services.provider.v5.data_source.grpc import GRPCProvider5DataSource as GRPCProviderDataSource
    from th2_data_services.provider.v5.commands import http, grpc  # noqa
    from th2_data_services.provider.v5.provider_api import HTTPProvider5API as HTTPProviderAPI  # noqa
    from th2_data_services.provider.v5.adapters.message_adapters import CodecPipelinesAdapter  # noqa
    from th2_data_services.provider.v5.struct import provider5_message_struct as message_struct
    from th2_data_services.filter import Filter  # noqa

    from .test_bodies.v5 import all_test_event_bodies, all_test_message_bodies

    START_TIME = datetime(year=2022, month=11, day=16, hour=12, minute=53, second=1, microsecond=0)
    END_TIME = datetime(year=2022, month=11, day=16, hour=12, minute=53, second=8, microsecond=0)

    EVENT_ID_TEST_DATA_ROOT = "9daac0e5-65ad-11ed-a742-b48c9dc9ebfb"
    EVENT_ID_PLAIN_EVENT_1 = "9e02c395-65ad-11ed-83f9-b48c9dc9ebfb"
    EVENT_ID_PLAIN_EVENT_2 = "9e02c396-65ad-11ed-819d-b48c9dc9ebfb"

    MESSAGE_ID_1 = "ds-lib-session1:first:1668603186732416805"
    MESSAGE_ID_2 = "ds-lib-session1:first:1668603186732416806"

    HTTP_PORT = "31915"  # HTTP provider v5
    GRPC_PORT = "31916"
