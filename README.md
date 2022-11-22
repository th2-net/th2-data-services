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
      * [GRPC provider warning](#grpc-provider-warning)
         * [Reasons for the restriction](#reasons-for-the-restriction)
   * [2.2. Example](#22-example)
   * [2.3. Short theory](#23-short-theory)
      * [Terms](#terms)
      * [Concept](#concept)
      * [Stream operations](#stream-operations)
         * [Pipelining](#pipelining)
         * [Internal iteration](#internal-iteration)
      * [Data caching](#data-caching)
         * [Forced caching](#forced-caching)
      * [EventsTree and collections](#eventstree-and-collections)
         * [EventsTree](#eventstree)
         * [Collections](#collections)
         * [Hints](#hints)
   * [2.4. Links](#24-links)
* [3. API](#3-api)
* [4. Examples](#4-examples)
   * [4.1. Notebooks](#41-notebooks)
   * [4.2. *.py](#42-py)
<!--te-->

# 1. Introduction

This repository is a library for creating th2-data-services applications.

The library used to analyze stream data using _aggregate operations_ mainly from
the ["Report Data Provider"](https://github.com/th2-net/th2-rpt-data-provider). Data Services allows you to manipulate
the stream data processing workflow using _pipelining_.

The library allows you:

- Natively connect to ["Report Data Provider"](https://github.com/th2-net/th2-rpt-data-provider) via
  `ProviderDataSource` class and extract TH2 Events/Messages via _commands_
- Work with iterable objects (list, tuple, etc including files) via _Data object_ using its features
- Manipulate the workflow to make some analysis by _Data object_ methods
- Build Event Trees (`EventsTreeCollection` class)

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

| dependency name | provider version |
|:--------:|:-------:|
|   RDP5   |    5    |
|   RDP6   |    6    |

**Example**

```
pip install th2-data-services[rdp5]
```

### GRPC provider warning
This library has ability to interact with several versions of grpc providers, but it's limited by installed version of
`th2_grpc_data_provider` package version. You can use only appropriate version of provider api, which is compatible with
installed version of `th2_grpc_data_provider`.

By default, `th2_data_services` uses the latest available version of provider api version.

#### Reasons for the restriction
1. Two different versions of `th2_grpc_data_provider` can't be installed in the same virtual environment;
2. Two different versions of package `th2_grpc_data_provider` may depend on different versions of packages `th2_grpc_common`;
3. In the case of using another package in the process of using `th2_data_services` (for example `th2_common`), 
which also depends on `th2_grpc_common`, a version conflict may occur (both at the Python level and at the Protobuf level).

## 2.2. Example

A good, short example is worth a thousand words.

This example works with **Events**, but you also can do the same actions with **Messages**.

[The following example as a file](examples/get_started_example.py).

<!-- start get_started_example.py -->
```python
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

```
<!-- end get_started_example.py -->

## 2.3. Short theory

The library provides tools for handling stream data. What’s a stream? It's a sequence of elements from a source that
supports aggregate operations.

### Terms

- **Data object**: An instance of `Data` class which is wrapper under stream.
- **Sequence of elements**:
  A _Data object_ provides an interface to a sequenced set of values of a specific element type. Stream inside the _Data
  object_ **don’t actually store** elements; they are computed on demand.
- **DataSource**:
  Any source of data. E.g. [Report Data Provider](https://github.com/th2-net/th2-rpt-data-provider), collections,
  arrays, or I/O resources.
- **ProviderDataSource**:
  The DataSource object whose source is [Report Data Provider](https://github.com/th2-net/th2-rpt-data-provider).
- **SourceAPI**:
  Each source has its own API to retrieve data. SourceAPI is a class that provide API for some data source.
- **Commands**:
  Objects that provide user-friendly interfaces for getting some data from DataSource. Commands use _SourceAPI_ to
  achieve it.
- **Adapters**:
  It's similar to function for `Data.map` method. Adoptable commands used it to update the data stream.
- **Aggregate operations**:
  Common operations such as filter, map, limit and so on.
- **Workflow**: An ordered set of _Aggregate operations_.

### Concept

The library describes the high-level interfaces `ISourceAPI`, `IDataSource`, `ICommand`, `IAdapter`.

Any data source must be described by the `IDataSource` abstract class. These can be _FileDataSource_, _CSVDataSource_, _
DBDataSource_ and other.

Usually, data sources have some kind of API. Databases - provide SQL language, when working with a file, you can read
line by line, etc. This API is described by the `ISourceAPI` class. Because different versions of the same data source
may have different API, it is better to create a class for each version.

Generally, data source APIs are hidden behind convenient interfaces. The role of these interfaces is played
by `ICommand` classes.

`IAdapter` classes transform data stream like functions for `Data.map` method. Essentially it's the same thing but more
flexible.

Thus, the native `ProviderDataSource` and the set of commands for it are described. This approach provides great
opportunities for extension. You can easily create your own unique commands for _ProviderDataSource_, as well as entire
_DataSource_ classes.

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
You can tell DS to cache data to specific cache file, which won't be deleted after script end:
```python
import datetime

from th2_data_services import Data
from th2_data_services.provider.v5.commands import http
from th2_data_services.provider.v5.data_source import HTTPProvider5DataSource


data_source = HTTPProvider5DataSource("http://HOST:PORT")
events: Data = data_source.command(
    http.GetEvents(
        start_timestamp=datetime.datetime.utcnow() - datetime.timedelta(minutes=5),
        end_timestamp=datetime.datetime.utcnow(),
        attached_messages=True,
        cache=True,
    )
)
events.build_cache("my_cache.pickle")
```

Later you can create _Data_ object from this cache file and use it as usual:
```python
from th2_data_services import Data

events = Data.from_cache_file("my_cache.pickle")

for event_id in events.filter(lambda x: x["eventType"] == "Verification").map(lambda x: x["eventId"]):
    print(event_id)
```


### EventsTree and collections

#### EventsTree

EventsTree is a tree-based data structure of events. It allows you get children and parents of event, display tree, get
full path to event etc.

Details:

* EventsTree contains all events in memory.
* To reduce memory usage an EventsTreeCollection delete the 'body' field from events, but you can preserve it specify '
  preserve_body'.
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

**EventsTreeCollection** is a collection of EventsTrees. The collection builds a few _EventsTree_ by passed _Data
object_. Although you can change the tree directly, it's better to do it through collections because they are aware of
`detached_events` and can solve some events dependencies. The collection has similar features like a single _EventsTree_
but applying them for all EventsTrees.

**ParentEventsTreeCollection** is a collection similar to EventsTreeCollection but containing only parent events that
are referenced in the data stream. It will be working data in the collection and trees of collection. The collection has
features similar to EventsTreeCollection.

Details:

* The collection has a feature to recover events. All events that are not in the received data stream, but which are
  referenced will be loaded from the data source.
* If you haven't passed a _DataSource object_ then the recovery of events will not occur.
* You can take `detached_events` to see which events are missing. It looks like `{parent_id: [events are referenced]}`
* If you want, you can build parentless trees where the missing events are stubbed instead. Just
  use `get_parentless_trees()`.

Requirements:

1. Events have to have `event_name`, `event_id`, `parent_event_id` fields, which are described in the
passed `event_struct` object.

#### Hints

* Remove all unnecessary fields from events before passing to a _collection_ to reduce memory usage.
* Use `show()` method to print the tree in tree-like view.
* Note that the `get_x` methods will raise an exception if you pass an unknown event id, unlike the `find_x` methods (
  they return None).
* If you want to know that specified event exists, use the python `in` keyword (e.g. `'event-id' in events_tree`).
* Use the python `len` keyword to get events number in the tree.

## 2.4. Links

- [Report Data Provider](https://github.com/th2-net/th2-rpt-data-provider)
- [Th2 Data Services Utils](https://github.com/th2-net/th2-data-services-utils)

# 3. API

If you are looking for classes description see the [API Documentation](documentation/api/index.md).

# 4. Examples

## 4.1. Notebooks

- [notebook_0.ipynb](examples/notebooks/notebook_0.ipynb)

## 4.2. *.py

- [get_started_example.py](examples/get_started_example.py)
