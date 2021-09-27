from th2_data_services.data_source import DataSource
from th2_data_services.data import Data
from datetime import datetime

# [1] Create DataSource object to connect to rpt-data-provider.
DEMO_HOST = "10.64.66.66"  # th2-kube-demo  Host port where rpt-data-provider is located.
DEMO_PORT = "30999"  # Node port of rpt-data-provider.
data_source = DataSource(f"http://{DEMO_HOST}:{DEMO_PORT}")

START_TIME = datetime(year=2021, month=6, day=17, hour=12, minute=44, second=41, microsecond=692724)
END_TIME = datetime(year=2021, month=6, day=17, hour=15, minute=45, second=49, microsecond=28579)

# [2] Get events from START_TIME to END_TIME.
events: Data = data_source.get_events_from_data_provider(
    startTimestamp=START_TIME,
    endTimestamp=END_TIME,
    metadataOnly=False,
    attachedMessages=True,
)

# [3] Work with your Data object.
# [3.1] Filter.
filtered_events: Data = events.filter(lambda e: e["body"] != [])  # Filter events with empty body.

# [3.2] Map.
def transform_function(record):
    return {"eventName": record["eventName"], "successful": record["successful"]}


filtered_and_mapped_events = filtered_events.map(transform_function)

# [3.3] Data pipeline.
#       Instead of doing data transformations step by step you can do it in one line.
filtered_and_mapped_events_by_pipeline = events.filter(lambda e: e["body"] != []).map(transform_function)

# Content of these two Data objects should be equal.
assert list(filtered_and_mapped_events) == list(filtered_and_mapped_events_by_pipeline)

# [3.4] Sift. Skip the first few items or limit them.
events_from_11_to_end: Data = events.sift(skip=10)
only_first_10_events: Data = events.sift(limit=10)

# [3.5] Walk through data.
for event in events:
    # Do something with event (event is a dict).
    print(event)

# [3.6] Get number of the elements in the Data object.
number_of_events = len(events)

# [3.7] Convert Data object to the list of elements(events or messages).
# Be careful, this can take too much memory.
events_list = list(events)

# [3.8] Get event/message by id.
desired_event = "9ce8a2ff-d600-4366-9aba-2082cfc69901:ef1d722e-cf5e-11eb-bcd0-ced60009573f"
desired_events = [
    "deea079b-4235-4421-abf6-6a3ac1d04c76:ef1d3a20-cf5e-11eb-bcd0-ced60009573f",
    "a34e3cb4-c635-4a90-8f42-37dd984209cb:ef1c5cea-cf5e-11eb-bcd0-ced60009573f",
]
desired_message = "demo-conn1:first:1619506157132265837"
desired_messages = [
    "demo-conn1:first:1619506157132265836",
    "demo-conn1:first:1619506157132265833",
]

data_source.find_events_by_id_from_data_provider(desired_event)  # Returns 1 event (dict).
data_source.find_events_by_id_from_data_provider(desired_events)  # Returns 2 events list(dict).

data_source.find_messages_by_id_from_data_provider(desired_message)  # Returns 1 message (dict).
data_source.find_messages_by_id_from_data_provider(desired_messages)  # Returns 2 messages list(dict).
