This repository is a library for creating th2-data-services applications.

🛠 An open source tool for analyzing stream data.

Data Services is a tool for analyzing stream data
from ["Report Data Provider"](https://github.com/th2-net/th2-rpt-data-provider)
via filtering, transformation and parsing. The tool allows the user to manipulate the workflow to analyze the required
data.

Current capabilities:

- Filtering stream data
- Transforming stream data



Table of Contents
=================

<!--ts-->
* [Table of Contents](#table-of-contents)
* [1. Introduction](#1-introduction)
* [2. Getting started](#2-getting-started)
   * [2.1. Installation](#21-installation)
   * [2.2. Example](#22-example)
   * [2.3. Links](#23-links)
* [3. Idea](#3-idea)
* [4. API](#4-api)
   * [4.1. DataSource](#41-datasource)
   * [4.2. Data](#42-data)
      * [4.2.1. Data pipelines](#421-data-pipelines)
      * [4.2.2. Cache](#422-cache)
   * [4.3. Events Trees](#43-events-trees)
      * [4.3.1. EventsTree](#431-eventstree)
      * [4.3.2. EventsTree2](#432-eventstree2)
* [5. Examples](#5-examples)
   * [5.1. Notebooks](#51-notebooks)
   * [5.2. *.py](#52-py)
<!--te-->

# 1. Introduction

What is what.

# 2. Getting started

## 2.1. Installation

- From PyPI (pip)   
  This package can be found on [PyPI](https://pypi.org/project/th2-data-services/ "th2-data-services").
    ```
    pip install th2-data-services
    ```

- From Source   
  TBU

## 2.2. Example

A good, short example is worth a thousand words.

This example works with **Events**, but you also can do the same actions with **Messages**.

[The same example in the file](examples/get_started_example.py).

    from th2_data_services.data_source import DataSource
    from th2_data_services.data import Data
    from datetime import datetime
    
    # [1] Create DataSource object to connect to rpt-data-provider.
    DEMO_HOST = "10.64.66.66"  # th2-kube-demo  Host port where rpt-data-provider is located.
    DEMO_PORT = "30999"  # Node port of rpt-data-provider.
    data_source = DataSource(F"http://{DEMO_HOST}:{DEMO_PORT}")
    
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
    filtered_events: Data = events.filter(lambda e: e['body'] != [])  # Filter events with empty body.
    
    # [3.2] Map.
    def transform_function(record):
        return {
            "eventName": record["eventName"],
            "successful": record["successful"]
        }
    
    filtered_and_mapped_events = filtered_events.map(transform_function)
    
    # [3.3] Data pipeline.
    #       Instead of doing data transformations step by step you can do it in one line.
    filtered_and_mapped_events_by_pipeline = events\
                                                .filter(lambda e: e['body'] != [])\
                                                .map(transform_function)
    
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
    desired_event = '9ce8a2ff-d600-4366-9aba-2082cfc69901:ef1d722e-cf5e-11eb-bcd0-ced60009573f'
    desired_events = [
        'deea079b-4235-4421-abf6-6a3ac1d04c76:ef1d3a20-cf5e-11eb-bcd0-ced60009573f',
        'a34e3cb4-c635-4a90-8f42-37dd984209cb:ef1c5cea-cf5e-11eb-bcd0-ced60009573f',
    ]
    desired_message = 'demo-conn1:first:1619506157132265837'
    desired_messages = [
        'demo-conn1:first:1619506157132265836',
        'demo-conn1:first:1619506157132265833',
    ]
    
    data_source.find_events_by_id_from_data_provider(desired_event)  # Returns 1 event (dict).
    data_source.find_events_by_id_from_data_provider(desired_events)  # Returns 2 events list(dict).
    
    data_source.find_messages_by_id_from_data_provider(desired_message)  # Returns 1 message (dict).
    data_source.find_messages_by_id_from_data_provider(desired_messages)  # Returns 2 messages list(dict).

## 2.3. Links

- [Report Data Provider](https://github.com/th2-net/th2-rpt-data-provider)
- [Th2 DS Utils](https://github.com/th2-net/th2-data-services-utils)

# 3. Idea

Ключевые идеи, такие как Пайплайны обработки данных.

Что из себя представляет Дата объект

# 4. API
[Documentation](documentation/api/index.md)

## 4.1. DataSource

The **data_source** module provides the `DataSource` class which can connect to **th2-rpt-provider**
or read csv files from cradle-viewer.

An example of connecting to Report Data Provider for getting events:

```
data_source = DataSources("http://localhost:8000")

# You can change anything in sse_request_to_data_provider. 
# Arguments gets based on route for th2-rpt-data-provider.
# This example shows pull the events.
events = data_source.get_events_from_data_provider(
    startTimestamp=datetime(year=2021, month=1, day=1, hour=1, minute=0),
    endTimestamp=datetime(year=2021, month=1, day=1, hour=1, minute=10),
    metadataOnly=False
)
```

The example shows basic query options:

- startTimestamp specifies the start time
- endTimestamp specifies the end time
- metaDataOnly specifies whether we need a body in events.

An example request for messages:

```
messages = data_source.get_messages_from_data_provider(
    startTimestamp=datetime(year=2021, month=1, day=1, hour=1, minute=0),
    endTimestamp=datetime(year=2021, month=1, day=1, hour=1, minute=10),
    stream=["myStream", "myStream2"]
)
```

The example shows basic query options:

- startTimestamp specifies the start time
- endTimestamp specifies the end time
- stream specifies the messages stream

In both examples, messages and events return as the Data class.

```
events = events.filter(...).map(...)
messages = messages.map(...).filter(...)
```

DataSource can take any connecting settings which are described
in [th2-rpt-data-provider](https://github.com/th2-net/th2-rpt-data-provider)

An example of loading data from csv files pulled from cradle-viewer:

```
data = DataSource.read_csv_file("file1.csv", "file2.csv")
```

If you want, you can enable cache with the help of a flag, you can do the following:

```
messages = data_source.get_messages_from_data_provider(
    cache=True,
    . . . . .
)
events = data_source.get_events_from_data_provider(
    cache=True,
    . . . . .
)
```

## 4.2. Data

The data module provides the Data class which builds the data stream workflow.

Data has two functions for the workflow:

- Filter
- Map

A simple example:

```
def transform(record):
    return {
        "eventName": record.get("eventName"),
        "eventId": record.get("eventId")
    }
    
def is_verification(record) -> bool:
    return record.get("eventType) == "Verification"

output_data = Data(working_data) \
    .map(transform) \
    .filter(is_verification)
    
for record in output_data:
    print(record)
```

The example shows the use of filtering and transforming data:

- transform shows how we can change data.
- is_verification shows how we can filter data.

You can receive or skip part of the data.

```
for record in output_data.sift(limit=10, skip=5):
    print(record)
```

Cache can be enabled with the help of the flag:

```
data.use_cache(True)
# or
data = Data(data, cache=True)
```

### 4.2.1. Data pipelines

        (Картинка из презентации кводу про дата флоу)
        - map
        - filter
        - sift

### 4.2.2. Cache

        Как использовать и как работает. 

## 4.3. Events Trees

### 4.3.1. EventsTree

The events_tree module provides the EventsTree class which helps with events and their parent events.

EventsTree has two objects:

- events
- unknown_events

'events' is a dictionary with "event id -> event body" pairs.

'unknown_events' is a dictionary which has events that don't exist in the given stream and builds "unknown event id ->
the count of events that have this event" pairs.

EventsTree also has several functions for checking the event ancestor or returning it.

A simple example:

```
events_tree = EventsTree(data)

event_ancestor = events_tree.get_ancestor_by_name(record, "Test Case")
status = events_tree.is_in_ancestor_name(record, "Test Case")
```

If EventsTree has unknown events, then you can get the missing events:

```
events_tree.recover_unknown_events(data_source)
```

        Нет смысла передавать сюда генератор ивентов с бади, т.к. они будут удаляться

### 4.3.2. EventsTree2

TBU

# 5. Examples

## 5.1. Notebooks

- [notebook_0.ipynb](examples/notebooks/notebook_0.ipynb)

## 5.2. *.py

- [get_started_example.py](examples/get_started_example.py)