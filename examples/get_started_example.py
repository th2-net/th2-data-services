from collections import Generator
from datetime import datetime
from typing import Tuple, List, Optional

from th2_data_services import Data
from th2_data_services.events_tree import EventsTree
from th2_data_services.provider.v5.data_source.http import HTTPProvider5DataSource
from th2_data_services.provider.v5.commands import http
from th2_data_services.filter import Filter
from th2_data_services.provider.v5.events_tree import EventsTreeCollectionProvider5, ParentEventsTreeCollectionProvider5

# [1] Create DataSource object to connect to rpt-data-provider.
DEMO_HOST = "10.64.66.66"  # th2-kube-demo  Host port where rpt-data-provider is located.
DEMO_PORT = "30999"  # Node port of rpt-data-provider.
data_source = HTTPProvider5DataSource(f"http://{DEMO_HOST}:{DEMO_PORT}")

START_TIME = datetime(
    year=2021, month=6, day=17, hour=9, minute=44, second=41, microsecond=692724
)  # object given in utc format
END_TIME = datetime(year=2021, month=6, day=17, hour=12, minute=45, second=49, microsecond=28579)

# [2] Get events or messages from START_TIME to END_TIME.
# [2.1] Get events.
events: Data = data_source.command(
    http.GetEvents(
        start_timestamp=START_TIME,
        end_timestamp=END_TIME,
        attached_messages=True,
        # Use Filter class to apply rpt-data-provider filters.
        filters=[Filter("name", "ExecutionReport"), Filter("type", "Send message")],
    )
)

# [2.2] Get messages.
messages: Data = data_source.command(
    http.GetMessages(
        start_timestamp=START_TIME,
        attached_events=True,
        stream=["demo-conn2"],
        filters=Filter("body", "195"),
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

# [4] Working with a EventsTree and EventsTreesCollections.
# [4.1] Building the EventsTreesCollection.

# If you don't specify data_source for the tree then it doesn't recover referenced events.
collection = EventsTreeCollectionProvider5(events)

# Detached events isn't empty.
assert collection.detached_events

collection = EventsTreeCollectionProvider5(events, data_source=data_source)
# Detached events is empty because the tree recover referenced events.
assert not collection.detached_events

# The collection has EventsTrees each with an tree of events.
# Using Collection and EventsTrees, you can work flexibly with events.

# [4.1.1] Get leaves of all trees.
leaves: Tuple[dict] = collection.get_leaves()

# [4.1.2] Get roots of all trees.
roots: List[str] = collection.get_roots_ids()

# [4.1.3] Find event in all trees.
find_event: Optional[dict] = collection.find(lambda event: "Send message" in event["eventType"])

# [4.1.4] Find all events in all trees.
find_events: List[dict] = collection.findall(lambda event: event["successful"] is True)

# [4.1.5] Find ancestor of event.
ancestor: Optional[dict] = collection.find_ancestor(
    "8bbe3717-cf59-11eb-a3f7-094f904c3a62", filter=lambda event: "RootEvent" in event["eventName"]
)

# [4.1.6] Get children of event.
children: Tuple[dict] = collection.get_children("814422e1-9c68-11eb-8598-691ebd7f413d")

# [4.1.7] Get subtree for specified event.
subtree: EventsTree = collection.get_subtree("8e23774d-cf59-11eb-a6e3-55bfdb2b3f21")

# [4.1.8] Get full path to the event.
# View as [ancestor_root, ancestor_level1, ancestor_level2, event]
event_path: List[dict] = collection.get_full_path("8e2524fa-cf59-11eb-a3f7-094f904c3a62")

# [4.1.9] Get parent of the event.
parent = collection.get_parent("8e2524fa-cf59-11eb-a3f7-094f904c3a62")

# [4.1.10] Append new event for the collection.
collection.append_element(
    event={
        "eventId": "a20f5ef4-c3fe-bb10-a29c-dd3d784909eb",
        "parentEventId": "8e2524fa-cf59-11eb-a3f7-094f904c3a62",
        "eventName": "StubEvent",
    }
)

# [4.1.11] Show entire collection.
collection.show()

# [4.2] Working with the EventsTree.
# EventsTree has the same methods as EventsTreeCollection, but only for its own tree.

# [4.2.1] Gets trees of collection.
trees: List[EventsTree] = collection.get_trees()
tree: EventsTree = trees[0]

# But EventsTree provides a work with the tree, but does not modify it.
# If you want to modify the tree, use EventsTreeCollections.

# [4.3] Working with ParentlessTree.
# ParentlessTree is EventsTree which has detached events with stubs.
parentless_trees: List[EventsTree] = collection.get_parentless_trees()

# [4.4] Working with ParentEventsTreesCollection.
# ParentEventsTreesCollection is tree like EventsTreesCollection but it has only events that have references.
collection = ParentEventsTreeCollectionProvider5(events, data_source=data_source)

collection.show()
