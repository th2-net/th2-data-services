[![](https://img.shields.io/badge/python-3.7+-g.svg)](https://www.python.org/downloads/)
[![](https://img.shields.io/github/v/release/th2-net/th2-data-services)](https://github.com/th2-net/th2-data-services/releases/latest)



Table of Contents
=================

<!--ts-->
* [Table of Contents](#table-of-contents)
* [1. Introduction](#1-introduction)
* [2. Getting started](#2-getting-started)
   * [2.1. Installation](#21-installation)
      * [Core](#core)
      * [Data sources (providers)](#data-sources-providers)
   * [2.2. Example](#22-example)
   * [2.3. Short theory](#23-short-theory)
      * [Terms](#terms)
      * [Concept](#concept)
      * [Stream operations](#stream-operations)
         * [Pipelining](#pipelining)
         * [Internal iteration](#internal-iteration)
      * [Data caching](#data-caching)
         * [Forced caching](#forced-caching)
      * [EventTree and collections](#eventtree-and-collections)
         * [EventTree](#eventtree)
         * [Collections](#collections)
         * [Hints](#hints)
      * [FieldsResolver](#fieldsresolver)
   * [2.4. Links](#24-links)
* [3. Best practices](#3-best-practices)
* [4. Official DataSource implementations](#4-official-datasource-implementations)
* [5. API](#5-api)
* [6. Examples](#6-examples)
<!--te-->

# 1. Introduction

This repository is a library for creating th2-data-services applications.
Data Services allows you to manipulate the stream data processing workflow using pipelining.

The library's features:

- Provides core interface for developing data source implementations
- Work with iterable objects (list, tuple, etc including files) via _Data object_ using its features
- Manipulate the workflow to make some analysis by _Data object_ methods
- Use timestamp converter implementations or use base class to create custom converters
- Build Event Trees (EventTree, EventTreeCollection and ParentEventTreeCollection classes)

Workflow manipulation tools allows you:

- Filtering stream data (`Data.filter` method)
- Transforming stream data (`Data.map` method)
- Limiting the number of processed streaming data (`Data.limit` method)

There is also another part of _data services_

- [th2-data-services-utils](https://github.com/th2-net/th2-data-services-utils). It's a set of tools to perform the most
  common analysis tasks.

# 2. Getting started

## 2.1. Installation

### Core

- From PyPI (pip)
  This package can be found on [PyPI](https://pypi.org/project/th2-data-services/ "th2-data-services").
    ```
    pip install th2-data-services
    ```

- From Source
    ```
    git clone https://github.com/th2-net/th2-data-services
    pip install th2-data-services/
    ```

### Data sources (providers)

Since `v1.3.0`, the library doesn't provide data source dependencies.

You should provide it manually during installation.
You just need to add square brackets after library name and put dependency name.

```
pip install th2-data-services[dependency_name]
```

**Dependencies list**

|  dependency name  | provider version                      |
|:-----------------:|---------------------------------------|
|       lwdp        | latest version of lwdp                |
|       lwdp2       | latest version of lwdp v2             |
|       lwdp3       | latest version of lwdp v3             |
| utils-rpt-viewer  | latest version of utils-rpt-viewer    |
| utils-rpt-viewer5 | latest version of utils-rpt-viewer v5 |
|   utils-advanced  | latest version of ds-utils            |

**Example**

```
pip install th2-data-services[lwdp1]
```

## 2.2. Example

A good, short example is worth a thousand words.

This example shows basic usage of library's features.

[The following example as a file](examples/get_started_example.py).

<!-- start get_started_example.py -->

from typing import Tuple, List, Optional, Generator
from datetime import datetime

from th2_data_services.data import Data
from th2_data_services.dummy import DummyDataSource
from th2_data_services.event_tree import (
    EventTree,
    EventTreeCollection,
    ParentEventTreeCollection,
    IETCDriver,
)
from th2_data_services.interfaces import IDataSource
from th2_data_services.utils.converters import (
    DatetimeConverter,
    DatetimeStringConverter,
    ProtobufTimestampConverter,
    Th2TimestampConverter,
)

######################################
# [0] Lib configuration
######################################

# [0.1] Interactive or Script mode
# If you use the lib in interactive mode (jupyter, ipython) it's recommended to set the special
# global parameter to True. It'll keep cache files if something went wrong.
from th2_data_services.config import options

options.INTERACTIVE_MODE = True

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
        {
            "eventId": "fake-eventId",
            "batchId": "fake-batchId",
            "isBatched": True,
            "eventName": "Fake event",
            "eventType": "ds-lib-test-event",
            "endTimestamp": {"epochSecond": 1672927035, "nano": 563791000},
            "startTimestamp": {"epochSecond": 1672927325, "nano": 563757000},
            "parentEventId": "not_exists_in_the_events_stream",
            "successful": False,
            "bookId": "demo_book_1",
            "scope": "th2-scope",
            "attachedMessageIds": [],
            "body": {"type": "message", "data": "ds-lib test body"},
        },
    ]
)

######################################
# [1] Working with a Data object.
######################################

# [1.1] Filter.
filtered_events: Data = events.filter(lambda e: e["body"] != [])  # Filter events with empty body.


# [1.2] Map.
def transform_function(record):
    return {"eventName": record["eventName"], "successful": record["successful"]}


filtered_and_mapped_events = filtered_events.map(transform_function)

# [1.3] Data pipeline.
#       Instead of doing data transformations step by step you can do it in one line.
filtered_and_mapped_events_by_pipeline = events.filter(lambda e: e["body"] != []).map(
    transform_function
)
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

events_without_types_with_batch = filtered_events_types.filter(
    lambda record: not record.get("eventType")
)
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

# [1.13] Check if Data is sorted.
# That will return an object `is_sorted` that contains information
#   1. status -- sorted or not
#   2. first_unsorted -- the index of the first unsorted element
is_sorted = events.is_sorted(lambda e: e["startTimestamp"]["epochSecond"])

# You can use this object as usual bool variable.
if is_sorted:
    print("events Data obj is sorted!")

# [1.14] Use `Data.show()` to look at the first N messages in the stream.
data_with_non_data_obj_via_add.show(n=6)
# Will print
# ------------- Printed first 6 records -------------
# [1] ------
# 1
# [2] ------
# 2
# [3] ------
# 3
# [4] ------
# 'a'
# [5] ------
# {'id': 123}
# [6] ------
# 'c'

# [1.15] You can remove the cache file of the Data object, if required.
data_obj_from_cache.clear_cache()


# [1.16] Get the message by its ID from the Data object in one line.
msg = next(data_obj_from_cache.find_by(record_field="MessageId", field_values=["msg-id"]))

# [1.17] Update metadata for Data objects.
# d1.metadata - {}
d1.update_metadata({"a": 1, "b": [10], "c": {"a": 100}})
# d1.metadata - {'a': 1, 'b': [10], 'c': {'a': 100}}
d1.update_metadata({"a": 2, "b": 20, "c": {"a": 200, "b": 300}})
# d1.metadata - {'a': 2, 'b': [10, 20], 'c': {'a': 200, 'b': 300}}
# d1.update_metadata({"a": {}}) - This throws AttributeError: 'int' object has no attribute 'update'.
# To set key whose value is of non-dict type to dict we can use change_type="change" argument.
d1.update_metadata({"a": {}}, change_type="change")
# d1.metadata - {'a': {}, 'b': [10, 20], 'c': {'a': 200, 'b': 300}}
# change_type can be either 'update' (default) or 'change' - overwrite existing value or create a new one if it
# doesn't exist.

######################################
# [2] Working with converters.
######################################
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

######################################
# [3] Working with EventTree and EventTreeCollection.
######################################
# Can be useful if you have data-stream with < 100k elements, otherwise it
# takes too much RAM.

# [3.1] Build a custom EventTree
# To create an EventTree object you need to provide name, id and data of the root event.
tree = EventTree(event_name="root event", event_id="root_id", data={"data": [1, 2, 3, 4, 5]})

# To add new node use append_event. parent_id is necessary, data is optional.
tree.append_event(event_name="A", event_id="A_id", data=None, parent_id="root_id")

# [3.3] Building the EventTreeCollection.
data_source: IDataSource  # You should init DataSource object. E.g. from LwDP module.
data_source = DummyDataSource()  # Note! We use fake DS here.
# ETCDriver here is a stub, actually the lib doesn't have such a class.
# You can take it in LwDP module or create yourself class if you have some special events structure.
from th2_data_services.data_source.lwdp.event_tree import HttpETCDriver as ETCDriver

# If you don't specify data_source for the driver then it won't recover detached events.
driver: IETCDriver  # You should init ETCDriver object. E.g. from LwDP module or your custom class.
driver = ETCDriver(data_source=data_source, use_stub=True)

etc = EventTreeCollection(driver)
etc.build(events)
etc.show()
# It'll print the following:
# Set of auto-generated events for ds lib testing
# ├── Plain event 1
# └── Plain event 2

print(etc)
# EventTreeCollection(trees=1, events=3[trees=3, detached=0])

# Detached events isn't empty.
assert etc.get_detached_events()  # returns list of detached_events.

# recover_unknown_events -- used to recover some events parents.
# That won't work with DummyDataSource, so was commented
# etc.recover_unknown_events()

# After that the detached events should be empty because they were recovered.
# assert not etc.get_detached_events()

# -----

# The collection has EventTrees each with a tree of events.
# Using Collection and EventTrees, you can work flexibly with events.

# [3.3.1] Get leaves of all trees.
leaves: Tuple[dict] = etc.get_leaves()  # Returns a tuple of leaves events

# [3.3.2] Get roots ids of all trees.
roots: List[str] = etc.get_roots_ids()
# Returns the list of root Ids:
# ['demo_book_1:th2-scope:20230105135705560873000:d61e930a-8d00-11ed-aa1a-d34a6155152d_1']

# [3.3.3] Find an event in all trees.
find_event: Optional[dict] = etc.find(lambda event: "Send message" in event["eventType"])

# [3.3.4] Find all events in all trees. There is also iterable version 'findall_iter'.
find_events: List[dict] = etc.findall(lambda event: event["successful"] is True)

# [3.3.5] Find an ancestor of the event.
ancestor: Optional[dict] = etc.find_ancestor(
    "demo_book_1:th2-scope:20230105135705560873000:d61e930a-8d00-11ed-aa1a-d34a6155152d_1",
    filter=lambda event: "RootEvent" in event["eventName"],
)

# [3.3.6] Get children of the event. There is also iterable version 'get_children_iter'.
children: Tuple[dict] = etc.get_children(
    "demo_book_1:th2-scope:20230105135705560873000:d61e930a-8d00-11ed-aa1a-d34a6155152d_1"
)

# [3.3.7] Get subtree for specified event.
subtree: EventTree = etc.get_subtree(
    "demo_book_1:th2-scope:20230105135705560873000:d61e930a-8d00-11ed-aa1a-d34a6155152d_1"
)

# [3.3.8] Get full path to the event.
# Looks like [ancestor_root, ancestor_level1, ancestor_level2, event]
event_path: List[dict] = etc.get_full_path(
    "demo_book_1:th2-scope:20230105135705560873000:d61e930a-8d00-11ed-aa1a-d34a6155152d_1"
)

# [3.3.9] Get parent of the event.
parent = etc.get_parent(
    "demo_book_1:th2-scope:20230105135705560873000:d61e930a-8d00-11ed-aa1a-d34a6155152d_1"
)

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
# It'll print the following:
# Set of auto-generated events for ds lib testing
# ├── Plain event 1
# └── Plain event 2

# As you can see, nothing was changed, but we added the new event!
# let's look at the summary.

print(etc.summary())  # the same as just print(etc)
# EventTreeCollection(trees=1, events=5[trees=3, detached=2])
# You can see that it was added to detached. That's why you don't see the event
# via `show()`. `show()` prints only Trees!
# Use `etc.get_parentless_trees()` to convert detached events to trees.
# More information below in the corresponding section.

# --------------
# [3.4] Working with the EventTree.
# EventTree has the same methods as EventTreeCollection, but only for its own tree.

# [3.4.1] Get a collection of trees.
trees: List[EventTree] = etc.get_trees()
tree: EventTree = trees[0]

# But EventTree provides a work with the tree, but does not modify it.
# If you want to modify the tree, use EventTreeCollections.

# [3.5] Working with ParentlessTree.
# ParentlessTree is an EventTree that has detached events with stubs.
parentless_trees: List[EventTree] = etc.get_parentless_trees()
print("parentless_trees contains:")
print(parentless_trees)
# [EventTree(name='<BrokenEvent>', root_id='not_exists_in_the_events_stream', events=2),
#  EventTree(name='<BrokenEvent>', root_id='8e2524fa-cf59-11eb-a3f7-094f904c3a62', events=2)]

print("\n" "etc after `get_parentless_trees`:")
print(etc.summary())
# EventTreeCollection(trees=3[regular=1, parentless=2], events=7[trees=7, detached=0])'
etc.show()
# Set of auto-generated events for ds lib testing
# ├── Plain event 1
# └── Plain event 2
# <BrokenEvent>
# └── Fake event
# <BrokenEvent>
# └── StubEvent    <--- the event that was added above

# [3.6] Working with ParentEventTreeCollection.
# ParentEventTreeCollection is a tree collection like EventTreeCollection,
# but it has only events that have references.
data_source: IDataSource  # You should init DataSource object. E.g. from LwDP module.
data_source = DummyDataSource()  # Note! We use fake DS here.
# ETCDriver here is a stub, actually the lib doesn't have such a class.
# You can take it in LwDP module or create yourself class if you have some special events structure.
from th2_data_services.data_source.lwdp.event_tree import HttpETCDriver as ETCDriver

driver = ETCDriver(data_source=data_source)
petc = ParentEventTreeCollection(driver)
petc.build(events)

petc.show()
petc.summary()

######################################
# [4] Field Resolvers
######################################
# Please read `Field Resolvers` block in readme first.

# [4.1] Usage example from client code
from th2_data_services.data_source import (
    lwdp,
)  # lwdp data_source initialize th2_data_services.config during import.
from th2_data_services.config import options as o_
from th2_data_services.data_source.lwdp.stub_builder import http_message_stub_builder

fake_data = [
    http_message_stub_builder.build({"messageId": "a", "messageType": "Root"}),
    http_message_stub_builder.build({"messageId": "b", "messageType": "New"}),
    http_message_stub_builder.build({"messageId": "c", "messageType": "Amend"}),
    http_message_stub_builder.build({"messageId": "d", "messageType": "Cancel"}),
]
fake_data_obj = Data(fake_data)

for m in fake_data_obj:
    o_.mfr.expand_message(m)  # mfr - stands for MessageFieldResolver
# or
for m in fake_data_obj.map(o_.mfr.expand_message):
    pass

# [4.2] Libraries usage.
# Don't import exact resolvers implementation in your code, please.
# Allow your client to do it instead.
# Just import `options` from `th2_data_services.config` and use it.
from th2_data_services.config import options as o_

for m in fake_data_obj:
    o_.mfr.expand_message(m)
# or
for m in fake_data_obj.map(o_.mfr.expand_message):
    pass

# More tech details:
#   In this case, there is no line `from th2_data_services.data_source import lwdp `
#   because we should not choose for the user which a data source to use.
#   We do not know what he will choose, therefore, we must simply access
#   the interface, which will be initialized by the user.

######################################
# [5] Using utility functions.
######################################
from th2_data_services.utils.event_utils.frequencies import get_category_frequencies2
from th2_data_services.utils.event_utils.totals import get_category_totals2
from th2_data_services.utils.category import Category
from th2_data_services.utils.event_utils.event_utils import is_sorted

# [5.1] Get the quantities of events for different categories.
metrics = [
    Category("date", lambda m: Th2TimestampConverter.to_datetime(m["startTimestamp"]).date()),
    Category("status", lambda m: m["successful"]),
]
category_totals = get_category_totals2(events, metrics)
print(category_totals)
"""
+--------+------------+----------+---------+
|        | date       | status   |   count |
+========+============+==========+=========+
|        | 2023-01-05 | True     |       3 |
+--------+------------+----------+---------+
|        | 2023-01-05 | False    |       1 |
+--------+------------+----------+---------+
| count  |            |          |       2 |
+--------+------------+----------+---------+
| totals |            | 1/1      |       4 |
+--------+------------+----------+---------+
"""

# [5.2] Get the number of events with status successful.
category = Category("status", lambda m: m["successful"])
category_frequencies = get_category_frequencies2(events, category)
print(category_frequencies)
"""
+--------+---------------------+---------------------+---------+--------+
|        | timestamp_start     | timestamp_end       | False   |   True |
+========+=====================+=====================+=========+========+
|        | 2023-01-05T13:57:05 | 2023-01-05T13:57:06 | 0       |      3 |
+--------+---------------------+---------------------+---------+--------+
|        | 2023-01-05T14:02:05 | 2023-01-05T14:02:06 | 1       |      0 |
+--------+---------------------+---------------------+---------+--------+
| count  |                     |                     |         |      2 |
+--------+---------------------+---------------------+---------+--------+
| totals |                     |                     | 1       |      3 |
+--------+---------------------+---------------------+---------+--------+
"""

# [5.3] Check if events are sorted.
result = is_sorted(events)
print(result)
```
<!-- end get_started_example.py -->

## 2.3. Short theory

The library provides tools for handling stream data. What's a stream? It's a sequence of elements from a source that
supports aggregate operations.

### Terms

- **Data object**: An instance of `Data` class which is wrapper under stream.
- **Sequence of elements**:
  A _Data object_ provides an interface to a sequenced set of values of a specific element type. Stream inside the _Data
  object_ **dont actually store** elements; they are computed on demand.
- **data source** (exactly in small letters):
  Any source of data. E.g. [Lightweight Data Provider](https://github.com/th2-net/th2-lw-data-provider), collections,
  arrays, or I/O resources.
- **DataSource**:
  A class that is an intermediate link between the SourceAPI and Commands.
- **SourceAPI**:
  Each source has its own API to retrieve data. SourceAPI is a class that provide API for some data source.
- **Commands**:
  Classes that provide user-friendly interfaces for getting some data from DataSource. Commands use _SourceAPI_ to
  achieve it.
- **Adapters**:
  It's similar to function for `Data.map` method. Adoptable commands used it to update the data stream.
- **Aggregate operations**:
  Common operations such as filter, map, limit and so on.
- **Workflow**: An ordered set of _Aggregate operations_.

### Concept

The library describes the high-level interfaces `ISourceAPI`, `IDataSource`, `ICommand`, `IAdapter`.

Any data source must be described by the `IDataSource` abstract class. These can be _FileDataSource_,
_CSVDataSource_, _DBDataSource_ and other.

Usually, data sources have some kind of API. Databases - provide SQL language, when working with a file, you can read
line by line, etc. This API is described by the `ISourceAPI` class. Because different versions of the same data source
may have different API, it is better to create a class for each version.

Generally, data source APIs are hidden behind convenient interfaces. The role of these interfaces is played
by `ICommand` classes.

`IAdapter` classes transform data stream like functions for `Data.map` method. Essentially it's the same thing but more
flexible.

For example, LwDP DataSource(https://github.com/th2-net/th2-ds-source-lwdp) uses these abstract classes to build its implementation.You can easily create your own unique commands for _LwDP DataSource_, as well as entire
_DataSource_ classes. [Here is a documentation](documentation/datasource.md) on how to implement these interfaces.

![Data stream pipeline](documentation/img/concept.png)

### Stream operations

Furthermore, stream operations have two fundamental characteristics that make them very different from collection
operations: _Pipelining_ and _Internal iteration_.

#### Pipelining

Many stream operations return a stream themselves. This allows operations to be chained to form a larger pipeline.

![Data stream pipeline](documentation/img/data_stream_pipeline.png)

#### Internal iteration

In contrast to collections, which are iterated explicitly (external iteration), stream operations do the iteration
behind the scenes for you. Note, it doesn't mean you cannot iterate the _Data object_.


### Data iteration

The Data object constructor method takes in as argument either an iterator over objects or a generator function.
The Data object iterator handles each item in this iterator or generator as they are, meaning it doesn't try to read the content of item or return them modified in any way, instead returns the item itself.
The only exception to this is when Data object is built using iterator or generator over other Data objects. Note that this iterator or generator must only be yielding Data objects and nothing else. If we build from a mix of Data objects and some other types, Data objects' content won't be read and instead it will be returned as Data object itself.

Small example to demonstrate:

```python
from th2_data_services.data import Data

d1 = Data([1,2,3])
d2 = Data([4,5,6])

only_data_objects = Data([d1,d2]) # Will iterate as 1,2,3,4,5,6
data_and_list = Data([d1,[4,5,6]]) # Will iterate as d1, [4,5,6]
data_and_numbers = Data([d1,4,5,6]) # Will iterate as d1,4,5,6
lists_only = Data([1,2,3],[4,5,6]) # Will iterate as [1,2,3],[4,5,6]

# If we want to iterate over content of list of lists, we should first create Data objects from them,
# then use them to construct new Data object as in case of d1 and d2, creating 'only_data_objects' in this example.
```
 

### Data caching

The _Data object_ provides the ability to use the cache. The cache works for each _Data object_, that is, you choose
which _Data object_ you want to save. The _Data object_ cache is saved after the first iteration, but the iteration
source may be different.

If you don't use the cache, your source will be the data source you have in the _Data Object_. But if you use the cache,
your source can be the data source, the parent cache, or own cache:

* The data source:
  If the _Data Object_ doesn't have a parent cache and its cache.
* The parent cache:
  If the _Data Object_ has a parent cache. It doesn't matter what position the parent cache has in inheritance.
  _Data Object_ understands whose cache it is and executes the part of the workflow that was not executed.
* The own cache:
  If it is not the first iteration of this Data object.

Note that the cache state of the Data object is not inherited.

#### Forced caching
You can tell DS to cache data to specific cache file, which won't be deleted after script end.
You can see example in 1.12 section of [get_started_example](examples/get_started_example.py).


### EventTree and collections

#### EventTree

`EventTree` is a tree-based data structure of events. It allows you get children and parents of event,
display tree, get full path to event etc.

Details:

* `EventTree` contains all events in memory.
* Tree has some important terms:
    1. _Ancestor_ is any relative of the event up the tree (grandparent, parent etc.).
    2. _Parent_ is only the first relative of the event up the tree.
    3. _Child_ is the first relative of the event down the tree.

Take a look at the following HTML tree to understand them.

   ```
    <body> <!-- ancestor (grandparent), but not parent -->
        <div> <!-- parent & ancestor -->
            <p>Hello, world!</p> <!-- child -->
            <p>Goodbye!</p> <!-- sibling -->
        </div>
    </body>
   ```

#### Collections

**EventTreeCollection** is a collection of EventTrees. The collection builds a few _EventTree_ by passed _Data
object_. Although you can change the tree directly, it's better to do it through collections because they are aware of
`detached_events` and can solve some events dependencies. The collection has similar features like a single _EventTree_
but applying them for all _EventTrees_.

**ParentEventTreeCollection** is a collection similar to _EventTreeCollection_ but containing only parent events that
are referenced in the data stream. The collection has features similar to _EventTreeCollection_.

Details:

* To use ET collections you need to initialize them by _ETCDriver_. Data sources usually provide them.
  You can create it by yourself depending on your data structure.
* The collection has a feature to recover events. All events that are not in the received data stream, but which are
  referenced will be loaded from the data source.
* You can take `detached_events` to see which events are missing.
* If you want, you can build parentless trees where the missing events are stubbed instead. Just
  use `get_parentless_trees()`.

Requirements:

1. Events provided to ETC have to have `event_name`, `event_id`, `parent_event_id` fields. They
can have another names (it resolves in the driver).

#### Hints

* Remove all unnecessary fields from events before passing to a _collection_ to reduce memory usage.
* Use `show()` method to print the tree in tree-like view.
* Note that the `get_x` methods will raise an exception if you pass an unknown event id, unlike the `find_x` methods (
  they return None).
* If you want to know that specified event exists, use the python `in` keyword (e.g. `'event-id' in events_tree`).
* Use the python `len` keyword to get events number in the tree.

### Field Resolvers
Interface can be found in `th2_data_services/interfaces/utils/resolver.py`.  
All data-sources should implement them.

The idea of using resolvers:
It solves the problem of having a few DataSources with similar data,
but with different ways to get it.

These classes provide you getter methods.
Using these classes allows you to freely switch between different data
formats and don't change your code.

Resolvers solve the problem of data-format migration.
- fields place can be changed
- fields names can be changed

Resolvers can work only with one event/message.
It means, if your message has sub-messages (like th2-messages in lwdp) it 
won't work, because resolver will not know with which sub-message should it work. 

**Workaround**  
1. Expand all your messages -> `new_d = your_data.map(MessageFieldResolver.expand_message)`
2. Use `ExpandedMessageFieldResolver` instead of usual `MessageFieldResolver` when 
    you take fields for expanded messages.

**Implementation advice:**
1. raise NotImplementedError -- if your Implementation doesn't support this getter.

**Performance impact:**
- It a bit slower than using naked field access `dict['key']`.

## 2.4. Links

- [Report Data Provider](https://github.com/th2-net/th2-rpt-data-provider)
- [Th2 Data Services Utils](https://github.com/th2-net/th2-data-services-utils)

# 3. Best practices
Depending on how you work with `Data object`, it can be slow of fast.
As with a relational database, you can write a query that will return data slowly or quickly,
the same when working with a `Data object`.

Follow the rules to make your work with Data object fast:
1. Use `Data.use_cache()` if you iterate data more than one time.
2. Try to don't iterate one `Data object` inside the other one.
   If you should to do it, use short `Data object` first and long `Data object` inside the loop.
   It'll allow you open the cache file or create a request to `Data source` less number of times.

# 4. Official DataSource implementations

- [Lightweight Data Provider Data Source](https://github.com/th2-net/th2-ds-source-lwdp)


# 5. API

If you are looking for classes description see the [API Documentation](documentation/api/index.md).

# 6. Examples

- [get_started_example.py](examples/get_started_example.py)
