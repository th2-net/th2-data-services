from datetime import datetime
from th2_data_services.interfaces import IAdapter
from th2_data_services.provider.v6.data_source import HTTPProvider6DataSource
from th2_data_services.provider.v6.commands import http

EVENT_ID_TEST_DATA_ROOT = "a26078a4-6419-11ed-bfec-b48c9dc9ebfb"
EVENT_ID_PLAIN_EVENT_1 = "a275f396-6419-11ed-a9e6-b48c9dc9ebfb"
EVENT_ID_PLAIN_EVENT_2 = "a275f397-6419-11ed-b8a7-b48c9dc9ebfb"

MESSAGE_ID_1 = "ds-lib-session1:first:1668429677955474105"
MESSAGE_ID_2 = "ds-lib-session1:first:1668429677955474106"

START_TIME = datetime(year=2022, month=11, day=14, hour=12, minute=41, second=12, microsecond=0)
END_TIME = datetime(year=2022, month=11, day=14, hour=12, minute=41, second=19, microsecond=0)


class TestAdapterForMessages(IAdapter):
    def handle(self, record: dict) -> dict:
        if record.get("id"):
            return record


HTTP_PORT = "31788"  # HTTP provider v6
GRPC_PORT = "32419"
STREAM_1 = "ds-lib-session1"
STREAM_2 = "ds-lib-session2"


data_source = HTTPProvider6DataSource("http://de-th2-qa:32154")

adapter = TestAdapterForMessages()

ds = data_source
msg_adapter = TestAdapterForMessages()

messages = ds.command(
    http.GetMessages(start_timestamp=START_TIME, end_timestamp=END_TIME, stream=["ds-lib-session1"]).apply_adapter(
        adapter.handle
    )
)
print(messages)
for message in messages:
    if message.get("id"):
        print("HELLO")
    print(message.get("id") == True)
