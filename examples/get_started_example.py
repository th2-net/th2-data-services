from collections import Generator
from datetime import datetime

from th2_data_services import Data
from th2_data_services.provider.v5.data_source.http import HTTPProvider5DataSource
from th2_data_services.provider.v5.commands import http
from th2_data_services.filter import Filter

# [1] Create DataSource object to connect to rpt-data-provider.
DEMO_HOST = "th2-qa"  # th2-qa  Host port where rpt-data-provider is located.
DEMO_PORT = "31299"  # Node port of rpt-data-provider.
data_source = HTTPProvider5DataSource(f"http://{DEMO_HOST}:{DEMO_PORT}")


START_TIME = datetime(year=2021, month=6, day=17, hour=9, minute=44, second=41, microsecond=692724)
END_TIME = datetime(year=2021, month=6, day=17, hour=12, minute=45, second=49, microsecond=28579)

# [2] Get events or messages from START_TIME to END_TIME.
# [2.1] Get events.
events: Data = data_source.command(
    http.GetEvents(
        start_timestamp=START_TIME,
        end_timestamp=END_TIME,
        attached_messages=True,
        # Use Filter class to apply rpt-data-provider filters.
        filters=[Filter("name", "Codec error"), Filter("type", "CodecError")],
    )
)

# [2.2] Get messages.
messages: Data = data_source.command(
    http.GetMessages(
        start_timestamp=START_TIME,
        attached_events=True,
        stream=["239.105.210.13:21006_ITCH", "arfq01fix04"],
        filters=f"{Filter('body', '195')}",
    )
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
events_from_11_to_end: Generator = events.sift(skip=10)
only_first_10_events: Generator = events.sift(limit=10)

# [3.5] Changing cache status.
events.use_cache(True)

# [3.6] Walk through data.
for event in events:
    # Do something with event (event is a dict).
    print(event)
# After first iteration the events has a cache file.
# Now they will be used the cache in following iteration.

# [3.7] Get number of the elements in the Data object.
number_of_events = events.len

# [3.8] Check that Data object isn't empty.
# The data source should be not empty.
assert events.is_empty is False

# [3.9] Convert Data object to the list of elements(events or messages).
# Be careful, this can take too much memory.
events_list = list(events)

# [3.10] Get event/message by id.
desired_event = "a1e272a3-cf69-11eb-b934-1525a25edf64"
desired_events = [
    "a1e272a3-cf69-11eb-b934-1525a25edf64",
    "a36d5864-cf69-11eb-b934-1525a25edf64",
]
desired_message = "arfq01fix04:first:1623903875361580545"
desired_messages = [
    "arfq01fix04:first:1623903875361580548",
    "arfq01fix04:second:1623903875361664548",
]

data_source.command(http.GetEventById(desired_event))  # Returns 1 event (dict).
data_source.command(http.GetEventsById(desired_events))  # Returns 2 events list(dict).

data_source.command(http.GetMessageById(desired_message))  # Returns 1 message (dict).
data_source.command(http.GetMessagesById(desired_messages))  # Returns 2 messages list(dict).

# [3.11] The cache inheritance.
# Creates a new Data object that will use cache from the events Data object.
events_with_batch = events.filter(lambda record: record.get("batchId"))

# New Data objects don't use their own cache by default but use the cache of the parent Data object.
# Use use_cache method to activate caching. After that, the Data object will create its own cache file.
events_with_batch.use_cache(True)

list(events_with_batch)

events_types_with_batch = events_with_batch.map(lambda record: {"eventType": record.get("eventType")})

events_without_types_with_batch = events_types_with_batch.filter(lambda record: not record.get("eventType"))
events_without_types_with_batch.use_cache(True)
