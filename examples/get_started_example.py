from typing import Tuple, List, Optional, Generator
from datetime import datetime
from th2_data_services.utils.converters import DatetimeConverter, DatetimeStringConverter, ProtobufTimestampConverter


from th2_data_services import Data
from th2_data_services.event_tree import EventTree, EventTreeCollection, ParentEventTreeCollection
from th2_data_services_lwdp.data_source import HTTPDataSource
from th2_data_services_lwdp.commands import http as commands
from th2_data_services_lwdp.filters.event_filters import NameFilter, TypeFilter
from th2_data_services_lwdp.events_tree import HttpETCDriver

# [0] Lib configuration
# [0.1] Interactive or Script mode
# If you use the lib in interactive mode (jupyter, ipython) it's recommended to set the special
# global parameter to True. It'll keep cache files if something went wrong.
import th2_data_services

th2_data_services.INTERACTIVE_MODE = True

# Some example data
events = Data(
    [
        {
            "eventId": "demo_book_1:th2-scope:20230105135705560873000:d61e930a-8d00-11ed-aa1a-d34a6155152d_1",
            "batchId": None,
            "isBatched": False,
            "eventName": "Set of auto-generated events for ds lib testing",
            "eventType": "ds-lib-test-event",
            "endTimestamp": {"epochSecond": 1672927025, "nano": 561751000},
            "startTimestamp": {"epochSecond": 1672927025, "nano": 560873000},
            "parentEventId": None,
            "successful": True,
            "bookId": "demo_book_1",
            "scope": "th2-scope",
            "attachedMessageIds": [],
            "body": [],
        },
        {
            "eventId": "demo_book_1:th2-scope:20230105135705563522000:9adbb3e0-5f8b-4c28-a2ac-7361e8fa704c>demo_book_1:th2-scope:20230105135705563522000:d61e930a-8d00-11ed-aa1a-d34a6155152d_2",
            "batchId": "demo_book_1:th2-scope:20230105135705563522000:9adbb3e0-5f8b-4c28-a2ac-7361e8fa704c",
            "isBatched": True,
            "eventName": "Plain event 1",
            "eventType": "ds-lib-test-event",
            "endTimestamp": {"epochSecond": 1672927025, "nano": 563640000},
            "startTimestamp": {"epochSecond": 1672927025, "nano": 563522000},
            "parentEventId": "demo_book_1:th2-scope:20230105135705560873000:d61e930a-8d00-11ed-aa1a-d34a6155152d_1",
            "successful": True,
            "bookId": "demo_book_1",
            "scope": "th2-scope",
            "attachedMessageIds": [],
            "body": {"type": "message", "data": "ds-lib test body"},
        },
        {
            "eventId": "demo_book_1:th2-scope:20230105135705563522000:9adbb3e0-5f8b-4c28-a2ac-7361e8fa704c>demo_book_1:th2-scope:20230105135705563757000:d61e930a-8d00-11ed-aa1a-d34a6155152d_3",
            "batchId": "demo_book_1:th2-scope:20230105135705563522000:9adbb3e0-5f8b-4c28-a2ac-7361e8fa704c",
            "isBatched": True,
            "eventName": "Plain event 2",
            "eventType": "ds-lib-test-event",
            "endTimestamp": {"epochSecond": 1672927025, "nano": 563791000},
            "startTimestamp": {"epochSecond": 1672927025, "nano": 563757000},
            "parentEventId": "demo_book_1:th2-scope:20230105135705560873000:d61e930a-8d00-11ed-aa1a-d34a6155152d_1",
            "successful": True,
            "bookId": "demo_book_1",
            "scope": "th2-scope",
            "attachedMessageIds": [],
            "body": {"type": "message", "data": "ds-lib test body"},
        },
    ]
)

# [1] Working with a Data object.
# [1.1] Filter.
filtered_events: Data = events.filter(lambda e: e["body"] != [])  # Filter events with empty body.


# [1.2] Map.
def transform_function(record):
    return {"eventName": record["eventName"], "successful": record["successful"]}


filtered_and_mapped_events = filtered_events.map(transform_function)


# [1.3] Data pipeline.
#       Instead of doing data transformations step by step you can do it in one line.
filtered_and_mapped_events_by_pipeline = events.filter(lambda e: e["body"] != []).map(transform_function)
# Content of these two Data objects should be equal.
assert list(filtered_and_mapped_events) == list(filtered_and_mapped_events_by_pipeline)

# [1.4] Sift. Skip the first few items or limit them.
data = Data([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
items_from_11_to_end: Generator = data.sift(skip=10)
only_first_10_items: Generator = data.sift(limit=10)

# [1.5] Changing cache status.
events.use_cache(True)
# or just
events.use_cache()  # If you want to activate cache.
# [1.6] Walk through data.
for event in events:
    # Do something with event (event is a dict).
    print(event)
# After first iteration the events has a cache file.
# Now they will be used in the cache in the next iteration.

# [1.7] Get number of the elements in the Data object.
number_of_events = events.len

# [1.8] Check that Data object isn't empty.
# The data source should be not empty.
assert events.is_empty is False

# [1.9] Convert Data object to the list of elements(events or messages).
# Be careful, this can take too much memory.
events_list = list(events)

# [1.10] The cache inheritance.
# Creates a new Data object that will use cache from the events Data object.
events_filtered: Data = events.filter(lambda record: record.get("batchId"))

# New Data objects don't use their own cache by default but use the cache of the parent Data object.
# Use use_cache method to activate caching.
# After that, the Data object will create its own cache file.
events_filtered.use_cache()

list(events_filtered)  # Just to iterate Data object (cache file will be created).

filtered_events_types = events_filtered.map(lambda record: {"eventType": record.get("eventType")})

events_without_types_with_batch = filtered_events_types.filter(lambda record: not record.get("eventType"))
events_without_types_with_batch.use_cache()

# [1.11] Data objects joining.
# You have the following 3 Data objects.
d1 = Data([1, 2, 3])
d2 = Data(["a", {"id": 123}, "c"])
d3 = Data([7, 8, 9])
# You can join Data objects in following ways.
# Please note, new Data object will have cache status == False.
data_via_init = Data([d1, d2, d3])
data_via_add = d1 + d2 + d3
data_with_non_data_obj_via_init = Data([d1, ["a", {"id": 123}, "c"], d3])
data_with_non_data_obj_via_add = d1 + ["a", {"id": 123}, "c"] + d3
# You can join current Data object on place using +=.
# It will keep cache status.
d1 += d3  # d1 will become Data([1,2,3,7,8,9])

# [1.12] Build and read Data object cache files.
events.build_cache("cache_filename_or_path")
data_obj_from_cache = Data.from_cache_file("cache_filename_or_path")


# [2] Working with converters.
# There are currently three implementations of ITimestampConverter class: DatetimeConverte, DatetimeStringConverter and ProtobufTimestampConverter.
# They all implement same methods from base class.
# Note that some accuracy may be lost during conversion.
# If for example you use to_microseconds nanoseconds will be cut off instead of rounding.

# [2.1] DatetimeConverter.
# DatetimeConverter takes datetime.datetime object as input.

datetime_obj = datetime(year=2023, month=1, day=5, hour=14, minute=38, second=25, microsecond=1460)

# It has methods that return the datetime in different formas:

date_ms = DatetimeConverter.to_milliseconds(datetime_obj)
date_us = DatetimeConverter.to_microseconds(datetime_obj)
# Converting to nanoseconds justs adds three trailing zeros as datetime object doesn't have nanoseconds.
date_ns = DatetimeConverter.to_nanoseconds(datetime_obj)

# [2.2] DatetimeStringConverter
# DatetimeStringConverter takes string in "yyyy-MM-ddTHH:mm:ss[.SSSSSSSSS]Z" format.

date_string = "2023-01-05T14:38:25.00146Z"

# We have same methods as in DatetimeConverter
date_ms_from_string = DatetimeStringConverter.to_milliseconds(date_string)
date_us_from_string = DatetimeStringConverter.to_microseconds(date_string)
date_ns_from_string = DatetimeStringConverter.to_nanoseconds(date_string)

# We can also get datetime object from string
datetime_from_string = DatetimeStringConverter.to_datetime(date_string)

# [2.3] ProtobufTimestampConverter
# Protobuf timestamps must be in form {"epochSecond": seconds, "nano": nanoseconds}

protobuf_timestamp = {"epochSecond": 1672929505, "nano": 1_460_000}

date_ms_from_timestamp = ProtobufTimestampConverter.to_milliseconds(protobuf_timestamp)
date_us_from_timestamp = ProtobufTimestampConverter.to_microseconds(protobuf_timestamp)
date_ns_from_timestamp = ProtobufTimestampConverter.to_nanoseconds(protobuf_timestamp)
datetime_from_timestamp = ProtobufTimestampConverter.to_datetime(protobuf_timestamp)


# [3] Working with EventTree and EventTreeCollection.

# [3.1] Create DataSource object to connect to rpt-data-provider.
DEMO_HOST = "10.100.66.66"  # th2-kube-demo  Host port where rpt-data-provider is located.
DEMO_PORT = "30999"  # Node port of rpt-data-provider.
data_source = HTTPDataSource(f"http://{DEMO_HOST}:{DEMO_PORT}")

START_TIME = datetime(year=2021, month=6, day=17, hour=9, minute=44, second=41)  # Datetime in utc format.
END_TIME = datetime(year=2021, month=6, day=17, hour=12, minute=45, second=50)

# [3.2] Get events.
events: Data = data_source.command(
    commands.GetEventsByBookByScopes(
        book_id="demo_book_1",
        scopes=["demo_scope"],
        start_timestamp=START_TIME,
        end_timestamp=END_TIME,
        # Use Filter class to apply rpt-data-provider filters.
        # Do not use multiple classes of the same type.
        filters=[
            TypeFilter("Send message"),
            NameFilter(["ExecutionReport", "NewOrderSingle"]),  # You can use multiple values.
        ],
    )
)

# [3.3] Building the EventTreeCollection.

# If you don't specify data_source for the driver then it won't recover detached events.
driver = HttpETCDriver()
etc = EventTreeCollection(driver)
etc.build(events)

# Detached events isn't empty.
assert etc.get_detached_events()

etc = EventTreeCollection(driver)
# Detached events are empty because they were recovered.
assert not etc.get_detached_events()

# The collection has EventTrees each with a tree of events.
# Using Collection and EventTrees, you can work flexibly with events.

# [3.3.1] Get leaves of all trees.
leaves: Tuple[dict] = etc.get_leaves()

# [3.3.2] Get roots ids of all trees.
roots: List[str] = etc.get_roots_ids()

# [3.3.3] Find an event in all trees.
find_event: Optional[dict] = etc.find(lambda event: "Send message" in event["eventType"])

# [3.3.4] Find all events in all trees. There is also iterable version 'findall_iter'.
find_events: List[dict] = etc.findall(lambda event: event["successful"] is True)

# [3.3.5] Find an ancestor of the event.
ancestor: Optional[dict] = etc.find_ancestor(
    "8bbe3717-cf59-11eb-a3f7-094f904c3a62", filter=lambda event: "RootEvent" in event["eventName"]
)

# [3.3.6] Get children of the event. There is also iterable version 'get_children_iter'.
children: Tuple[dict] = etc.get_children("814422e1-9c68-11eb-8598-691ebd7f413d")

# [3.3.7] Get subtree for specified event.
subtree: EventTree = etc.get_subtree("8e23774d-cf59-11eb-a6e3-55bfdb2b3f21")

# [3.3.8] Get full path to the event.
# Looks like [ancestor_root, ancestor_level1, ancestor_level2, event]
event_path: List[dict] = etc.get_full_path("8e2524fa-cf59-11eb-a3f7-094f904c3a62")

# [3.3.9] Get parent of the event.
parent = etc.get_parent("8e2524fa-cf59-11eb-a3f7-094f904c3a62")

# [3.3.10] Append new event to the collection.
etc.append_event(
    event={
        "eventId": "a20f5ef4-c3fe-bb10-a29c-dd3d784909eb",
        "parentEventId": "8e2524fa-cf59-11eb-a3f7-094f904c3a62",
        "eventName": "StubEvent",
    }
)

# [3.3.11] Show the entire collection.
etc.show()

# [3.4] Working with the EventTree.
# EventTree has the same methods as EventTreeCollection, but only for its own tree.

# [3.4.1] Get collection trees.
trees: List[EventTree] = etc.get_trees()
tree: EventTree = trees[0]

# But EventTree provides a work with the tree, but does not modify it.
# If you want to modify the tree, use EventTreeCollections.

# [3.5] Working with ParentlessTree.
# ParentlessTree is EventTree which has detached events with stubs.
parentless_trees: List[EventTree] = etc.get_parentless_trees()

# [3.6] Working with ParentEventTreeCollection.
# ParentEventTreeCollection is a tree like EventTreeCollection, but it has only events that have references.
driver = HttpETCDriver(data_source=data_source)
etc = ParentEventTreeCollection(driver)
etc.build(events)

etc.show()

# [3.7] Build a custom EventTree
# To create an EventTree object you will need name and id, data is optional.
tree = EventTree(event_name="root event", event_id="root_id", data={"data": [1, 2, 3, 4, 5]})

# To add new node use append_event. parent_id is necessary, data is optional.
tree.append_event(event_name="A", event_id="A_id", data=None, parent_id="root_id")
