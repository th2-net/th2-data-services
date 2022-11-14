from datetime import datetime
from th2_data_services.provider.v5.data_source import GRPCProvider5DataSource, HTTPProvider5DataSource
from th2_data_services.provider.v5.commands import http, grpc

START_TIME_EVENT = datetime(year=2022, month=11, day=9, hour=10, minute=13, second=17, microsecond=0)
END_TIME_EVENT   = datetime(year=2022, month=11, day=9, hour=10, minute=13, second=24, microsecond=0)

START_TIME_MESSAGE = datetime(year=2022, month=11, day=10, hour=8, minute=15, second=11, microsecond=0)
END_TIME_MESSAGE   = datetime(year=2022, month=11, day=10, hour=8, minute=15, second=20, microsecond=0)

data_source = GRPCProvider5DataSource("de-th2-qa:31916")


events = data_source.command(
        grpc.GetMessages(
            start_timestamp=START_TIME_MESSAGE,
            end_timestamp=END_TIME_MESSAGE,
            stream=["ds-lib-session1", "ds-lib-session2"]
        )
    )

print(list(events))