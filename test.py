from datetime import datetime
from th2_data_services.provider.v6.data_source import HTTPProvider6DataSource
from th2_data_services.provider.v6.commands import http, grpc

START_TIME = datetime(year=2022, month=11, day=14, hour=12, minute=41, second=12, microsecond=0)
END_TIME   = datetime(year=2022, month=11, day=14, hour=12, minute=41, second=19, microsecond=0)
MESSAGE_ID_1 = 'ds-lib-session1:first:1668068118436646201'

data_source = HTTPProvider6DataSource("http://de-th2-qa:32154")

events = data_source.command(http.GetEvents(start_timestamp=START_TIME,end_timestamp=END_TIME))
print(events.len)