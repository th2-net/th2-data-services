from collections import Generator
from typing import Tuple, List, Optional
from datetime import datetime

from th2_data_services import Data
from th2_data_services.events_tree import EventsTree
from th2_data_services.provider.v5.data_source.http import HTTPProvider5DataSource
from th2_data_services.provider.v5.commands import http as commands
from th2_data_services.provider.v5.events_tree import EventsTreeCollectionProvider5, ParentEventsTreeCollectionProvider5
from th2_data_services.provider.v5.filters.event_filters import NameFilter, TypeFilter, FailedStatusFilter
from th2_data_services.provider.v5.filters.message_filters import BodyFilter

# [0] Lib configuration
# [0.1] Interactive or Script mode
# If you use the lib in interactive mode (jupyter, ipython) it's recommended to set the special
# global parameter to True. It'll keep cache files if something went wrong.
import th2_data_services

th2_data_services.INTERACTIVE_MODE = True

# [1] Create DataSource object to connect to rpt-data-provider.
DEMO_HOST = "10.100.66.66"  # th2-kube-demo  Host port where rpt-data-provider is located.
DEMO_PORT = "30999"  # Node port of rpt-data-provider.
data_source = HTTPProvider5DataSource(f"http://{DEMO_HOST}:{DEMO_PORT}")

START_TIME = datetime(
    year=2021, month=6, day=17, hour=9, minute=44, second=41, microsecond=692724
)  # Datetime in utc format.
END_TIME = datetime(year=2021, month=6, day=17, hour=12, minute=45, second=50)

# [2] Get events or messages from START_TIME to END_TIME.
# [2.1] Get events.
events: Data = data_source.command(
    commands.GetEvents(
        start_timestamp=START_TIME,
        end_timestamp=END_TIME,
        attached_messages=True,
        # Use Filter class to apply rpt-data-provider filters.
        # Do not use multiple classes of the same type.
        filters=[
            TypeFilter("Send message"),
            NameFilter(["ExecutionReport", "NewOrderSingle"]),  # You can use multiple values.
            FailedStatusFilter(),
        ],
    )
)

# [2.2] Get messages.
messages: Data = data_source.command(
    commands.GetMessages(
        start_timestamp=START_TIME,
        end_timestamp=END_TIME,
        attached_events=True,
        stream=["demo-conn2"],
        filters=BodyFilter("195"),  # Filter message if there is a substring '195' in the body.
    )
)

# [3] Work with a Data object.
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
# or just
events.use_cache()  # If you want to activate cache.

# [3.6] Walk through data.
for event in events:
    # Do something with event (event is a dict).
    print(event)
# After first iteration the events has a cache file.
# Now they will be used in the cache in the next iteration.

# [3.7] Get number of the elements in the Data object.
number_of_events = events.len

# [3.8] Check that Data object isn't empty.
# The data source should be not empty.
assert events.is_empty is False

# [3.9] Convert Data object to the list of elements(events or messages).
# Be careful, this can take too much memory.
events_list = list(events)

# [3.10] Get event/message by id.
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

data_source.command(commands.GetEventById(desired_event))  # Returns 1 event (dict).
data_source.command(commands.GetEventsById(desired_events))  # Returns 2 events list(dict).

data_source.command(commands.GetMessageById(desired_message))  # Returns 1 message (dict).
data_source.command(commands.GetMessagesById(desired_messages))  # Returns 2 messages list(dict).

# [3.11] The cache inheritance.
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

# [3.12] Data objects joining.
# You have the following 3 Data objects.
d1 = Data([1, 2, 3])
d2 = Data(["a", {"id": 123}, "c"])
d3 = Data([7, 8, 9])
# You can join Data objects in following ways.
data_via_init = Data([d1, d2, d3])
data_via_add = d1 + d2 + d3
data_with_non_data_obj_via_init = Data([d1, ["a", {"id": 123}, "c"], d3])
data_with_non_data_obj_via_add = d1 + ["a", {"id": 123}, "c"] + d3

# [3.13] Build and read Data object cache files.
events.build_cache("cache_filename_or_path")
data_obj_from_cache = Data.from_cache_file("cache_filename_or_path")


# [4] Working with EventsTree and EventsTreeCollection.
# [4.1] Building the EventsTreeCollection.

# If you don't specify data_source for the tree then it won't recover detached events.
collection = EventsTreeCollectionProvider5(events)

# Detached events isn't empty.
assert collection.detached_events

collection = EventsTreeCollectionProvider5(events, data_source=data_source)
# Detached events are empty because they were recovered.
assert not collection.detached_events

# The collection has EventsTrees each with a tree of events.
# Using Collection and EventsTrees, you can work flexibly with events.

# [4.1.1] Get leaves of all trees.
leaves: Tuple[dict] = collection.get_leaves()

# [4.1.2] Get roots ids of all trees.
roots: List[str] = collection.get_roots_ids()

# [4.1.3] Find an event in all trees.
find_event: Optional[dict] = collection.find(lambda event: "Send message" in event["eventType"])

# [4.1.4] Find all events in all trees. There is also iterable version 'findall_iter'.
find_events: List[dict] = collection.findall(lambda event: event["successful"] is True)

# [4.1.5] Find an ancestor of the event.
ancestor: Optional[dict] = collection.find_ancestor(
    "8bbe3717-cf59-11eb-a3f7-094f904c3a62", filter=lambda event: "RootEvent" in event["eventName"]
)

# [4.1.6] Get children of the event. There is also iterable version 'get_children_iter'.
children: Tuple[dict] = collection.get_children("814422e1-9c68-11eb-8598-691ebd7f413d")

# [4.1.7] Get subtree for specified event.
subtree: EventsTree = collection.get_subtree("8e23774d-cf59-11eb-a6e3-55bfdb2b3f21")

# [4.1.8] Get full path to the event.
# Looks like [ancestor_root, ancestor_level1, ancestor_level2, event]
event_path: List[dict] = collection.get_full_path("8e2524fa-cf59-11eb-a3f7-094f904c3a62")

# [4.1.9] Get parent of the event.
parent = collection.get_parent("8e2524fa-cf59-11eb-a3f7-094f904c3a62")

# [4.1.10] Append new event to the collection.
collection.append_event(
    event={
        "eventId": "a20f5ef4-c3fe-bb10-a29c-dd3d784909eb",
        "parentEventId": "8e2524fa-cf59-11eb-a3f7-094f904c3a62",
        "eventName": "StubEvent",
    }
)

# [4.1.11] Show the entire collection.
collection.show()

# [4.2] Working with the EventsTree.
# EventsTree has the same methods as EventsTreeCollection, but only for its own tree.

# [4.2.1] Get collection trees.
trees: List[EventsTree] = collection.get_trees()
tree: EventsTree = trees[0]

# But EventsTree provides a work with the tree, but does not modify it.
# If you want to modify the tree, use EventsTreeCollections.

# [4.3] Working with ParentlessTree.
# ParentlessTree is EventsTree which has detached events with stubs.
parentless_trees: List[EventsTree] = collection.get_parentless_trees()

# [4.4] Working with ParentEventsTreeCollection.
# ParentEventsTreeCollection is a tree like EventsTreeCollection but it has only events that have references.
collection = ParentEventsTreeCollectionProvider5(events, data_source=data_source)

collection.show()
