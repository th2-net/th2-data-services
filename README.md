Table of Contents
=================

<!--ts-->
* [Table of Contents](#table-of-contents)
* [1. Introduction](#1-introduction)
* [2. Getting started](#2-getting-started)
   * [2.1. Installation](#21-installation)
   * [2.2. Example](#22-example)
   * [2.3. Theory](#23-theory)
   * [2.4. Links](#24-links)
* [3. API](#3-api)
* [4. Examples](#4-examples)
   * [4.1. Notebooks](#41-notebooks)
   * [4.2. *.py](#42-py)
<!--te-->

# 1. Introduction

This repository is a library for creating th2-data-services applications.

Data Services is a tool for analyzing stream data
from ["Report Data Provider"](https://github.com/th2-net/th2-rpt-data-provider)
via aggregate operations. The tool allows the user to manipulate the workflow to analyze the required
data.

Current capabilities:

- Filtering stream data
- Transforming stream data


# 2. Getting started

## 2.1. Installation

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

## 2.2. Example

A good, short example is worth a thousand words.

This example works with **Events**, but you also can do the same actions with **Messages**.

[The following example as a file](examples/get_started_example.py).

```python
from collections import Generator
from th2_data_services import DataSource, Data, Filter
from datetime import datetime


# [1] Create DataSource object to connect to rpt-data-provider.
DEMO_HOST = "10.64.66.66"  # th2-kube-demo  Host port where rpt-data-provider is located.
DEMO_PORT = "30999"  # Node port of rpt-data-provider.
data_source = DataSource(f"http://{DEMO_HOST}:{DEMO_PORT}")

START_TIME = datetime(year=2021, month=6, day=17, hour=9, minute=44, second=41, microsecond=692724)  # object given in utc format
END_TIME = datetime(year=2021, month=6, day=17, hour=12, minute=45, second=49, microsecond=28579)

# [2] Get events or messages from START_TIME to END_TIME.
# [2.1] Get events.
events: Data = data_source.get_events_from_data_provider(
    startTimestamp=START_TIME,
    endTimestamp=END_TIME,
    attachedMessages=True,
    # Use Filter class to apply rpt-data-provider filters.
    filters=[  # Use the list to set multiple filters.
        Filter("name", "ExecutionReport"),
        Filter("type", "Send message")
    ],
)

# [2.2] Get messages.
messages: Data = data_source.get_messages_from_data_provider(
    startTimestamp=START_TIME,
    endTimestamp=END_TIME,
    attachedMessages=True,
    stream=["demo-conn2"],
    filters=Filter("body", "195"),
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

data_source.find_events_by_id_from_data_provider(desired_event)  # Returns 1 event (dict).
data_source.find_events_by_id_from_data_provider(desired_events)  # Returns 2 events list(dict).

data_source.find_messages_by_id_from_data_provider(desired_message)  # Returns 1 message (dict).
data_source.find_messages_by_id_from_data_provider(desired_messages)  # Returns 2 messages list(dict).

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
```

## 2.3. Theory

The library provides stream data and some tools for data manipulation.

What’s the definition of a stream?   
A short definition is "a sequence of elements from a source that supports aggregate operations."

- **Data object**: An object of `Data` class which is wrapper under stream. 
- **Sequence of elements**:
  A _Data object_ provides an interface to a sequenced set of values of a specific element type. 
  Stream inside the _Data object_ **don’t actually store** elements; they are computed on demand.
- **DataSource**: 
  Streams consume from a data-providing source ([Report Data Provider](https://github.com/th2-net/th2-rpt-data-provider)) 
  but it also can be collections, arrays, or I/O resources. 
  _DataSource object_ provides connection to _th2-rpt-provider_ or read csv files from cradle-viewer.
- **Aggregate operations**: 
  Common operations such as filter, map, find and so on. 
- **Data caching**:
  The _Data object_ provides the ability to use the cache. 
  The cache works for each _Data object_, that is, you choose which _Data object_ you want to save. 
  The _Data object_ cache is saved after the first iteration, but the iteration source may be different.
  If you don't use the cache, your source will be the data source you have in the _Data Object_. 
  But if you use the cache, your source can be the data source, the parent cache, or own cache:
  * The data source: 
  If the "Data Object" doesn't have a parent cache and its cache.
  * The parent cache: 
  If the "Data Object" has a parent cache. 
  It doesn't matter what position the parent cache has in inheritance. 
  "Data Object" understands whose cache it is and executes the part of the workflow that was not executed.
  * The own cache: 
  If it is not the first iteration of this Data object.
  
  Note that the cache state of the Data object is not inherited.
  

Furthermore, stream operations have two fundamental characteristics that make them very different 
from collection operations:

- **Pipelining**: Many stream operations return a stream themselves. 
This allows operations to be chained to form a larger pipeline.

![Data stream pipeline](documentation/img/data_stream_pipeline.png)

- **Internal iteration**: In contrast to collections, which are iterated explicitly (external iteration), 
stream operations do the iteration behind the scenes for you. Note, it doesn’t mean you cannot iterate 
the _Data object_.

  
## 2.4. Links

- [Report Data Provider](https://github.com/th2-net/th2-rpt-data-provider)
- [Th2 Data Services Utils](https://github.com/th2-net/th2-data-services-utils)



# 3. API
[Documentation](documentation/api/index.md)


# 4. Examples

## 4.1. Notebooks

- [notebook_0.ipynb](examples/notebooks/notebook_0.ipynb)

## 4.2. *.py

- [get_started_example.py](examples/get_started_example.py)
