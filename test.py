from th2_data_services.provider.v5.data_source import HTTPProvider5DataSource
from th2_data_services.provider.v5.commands import http

data_source = HTTPProvider5DataSource("http://de-th2-qa./rdp5-http/backend")


print(data_source)