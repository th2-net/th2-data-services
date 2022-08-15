<!-- markdownlint-disable -->

<a href="../../th2_data_services/provider/v6/provider_api/grpc.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `provider.v6.provider_api.grpc`






---

<a href="../../th2_data_services/provider/v6/provider_api/grpc.py"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `BasicRequest`
BasicRequest(start_timestamp, end_timestamp, result_count_limit, keep_open, search_direction, filters) 





---

<a href="../../th2_data_services/provider/v6/provider_api/grpc.py#L54"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GRPCProvider6API`




<a href="../../th2_data_services/provider/v6/provider_api/grpc.py#L55"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(url: str)
```

GRPC Provider6 API. 



**Args:**
 
 - <b>`url`</b>:  GRPC data source url. 




---

<a href="../../th2_data_services/provider/v6/provider_api/grpc.py#L372"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_event`

```python
get_event(event_id: str) → EventResponse
```

GRPC-API `getEvent` call returns a single event with the specified id. 

---

<a href="../../th2_data_services/provider/v6/provider_api/grpc.py#L390"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_event_filter_info`

```python
get_event_filter_info(filter_name: str) → FilterInfoResponse
```

GRPC-API `getEventFilterInfo` call returns event filter info. 

---

<a href="../../th2_data_services/provider/v6/provider_api/grpc.py#L386"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_events_filters`

```python
get_events_filters() → FilterNamesResponse
```

GRPC-API `getEventsFilters` call returns all the names of sse event filters. 

---

<a href="../../th2_data_services/provider/v6/provider_api/grpc.py#L377"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_message`

```python
get_message(message_id: str) → MessageGroupResponse
```

GRPC-API `getMessage` call returns a single message with the specified id. 

---

<a href="../../th2_data_services/provider/v6/provider_api/grpc.py#L395"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_message_filter_info`

```python
get_message_filter_info(filter_name: str) → FilterInfoResponse
```

GRPC-API `getMessageFilterInfo` call returns message filter info. 

---

<a href="../../th2_data_services/provider/v6/provider_api/grpc.py#L72"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_message_streams`

```python
get_message_streams() → MessageStreamsResponse
```

GRPC-API `getMessageStreams` call returns a list of message stream names. 

---

<a href="../../th2_data_services/provider/v6/provider_api/grpc.py#L382"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_messages_filters`

```python
get_messages_filters() → FilterNamesResponse
```

GRPC-API `getMessagesFilters` call returns all the names of sse message filters. 

---

<a href="../../th2_data_services/provider/v6/provider_api/grpc.py#L400"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `match_event`

```python
match_event(event_id: str, filters: List[Filter]) → MatchResponse
```

GRPC-API `matchEvent` call checks that the event with the specified id is matched by the filter. 

---

<a href="../../th2_data_services/provider/v6/provider_api/grpc.py#L405"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `match_message`

```python
match_message(message_id: str, filters: List[Filter]) → MatchResponse
```

GRPC-API `matchMessage` call checks that the message with the specified id is matched by the filter. 

---

<a href="../../th2_data_services/provider/v6/provider_api/grpc.py#L76"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `search_events`

```python
search_events(
    start_timestamp: int = None,
    end_timestamp: int = None,
    parent_event: str = None,
    search_direction: str = 'NEXT',
    resume_from_id: str = None,
    result_count_limit: int = None,
    keep_open: bool = False,
    limit_for_parent: int = None,
    metadata_only: bool = True,
    attached_messages: bool = False,
    filters: Optional[List[Filter]] = None
) → Iterable[EventSearchResponse]
```

GRPC-API `searchEvents` call creates an event or an event metadata stream that matches the filter. 



**Args:**
 
 - <b>`start_timestamp`</b>:  Sets the search starting point. Expected in nanoseconds. One of the 'start_timestamp'  or 'resume_from_id' must not absent. 
 - <b>`end_timestamp`</b>:  Sets the timestamp to which the search will be performed, starting with 'start_timestamp'.  Expected in nanoseconds. 
 - <b>`parent_event`</b>:  Match events to the specified parent. 
 - <b>`search_direction`</b>:  Sets the lookup direction. Can be 'NEXT' or 'PREVIOUS'. 
 - <b>`resume_from_id`</b>:  The last event id from which we start searching for events. 
 - <b>`result_count_limit`</b>:  Sets the maximum amount of events to return. 
 - <b>`keep_open`</b>:  Option if the search has reached the current moment,  it is necessary to wait further for the appearance of new data. 
 - <b>`limit_for_parent`</b>:  How many children events for each parent do we want to request. 
 - <b>`metadata_only`</b>:  Receive only metadata (true) or entire event (false) (without attachedMessageIds). 
 - <b>`attached_messages`</b>:  Option if you want to load attachedMessageIds additionally. 
 - <b>`filters`</b>:  Which filters to apply in a search. 



**Returns:**
 Iterable object which return events as parts of streaming response. 

---

<a href="../../th2_data_services/provider/v6/provider_api/grpc.py#L147"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `search_messages`

```python
search_messages(
    start_timestamp: int,
    end_timestamp: int = None,
    search_direction: str = 'NEXT',
    result_count_limit: int = None,
    stream: List[str] = None,
    keep_open: bool = False,
    stream_pointer: List[MessageStreamPointer] = None,
    filters: Optional[List[Filter]] = None,
    attached_events: bool = False
) → Iterable[MessageSearchResponse]
```

GRPC-API `searchMessages` call creates a message stream that matches the filter. 



**Args:**
 
 - <b>`start_timestamp`</b>:  Sets the search starting point. Expected in nanoseconds. One of the 'start_timestamp'  or 'resume_from_id' must not absent. 
 - <b>`stream`</b>:  Sets the stream ids to search in. 
 - <b>`end_timestamp`</b>:  Sets the timestamp to which the search will be performed, starting with 'start_timestamp'.  Expected in nanoseconds. 
 - <b>`search_direction`</b>:  Sets the lookup direction. Can be 'NEXT' or 'PREVIOUS'. 
 - <b>`result_count_limit`</b>:  Sets the maximum amount of messages to return. 
 - <b>`keep_open`</b>:  Option if the search has reached the current moment,  it is necessary to wait further for the appearance of new data. 
 - <b>`stream_pointer`</b>:  List of stream pointers to restore the search from.  start_timestamp will be ignored if this parameter is specified. This parameter is only received  from the provider. 
 - <b>`filters`</b>:  Which filters to apply in a search. 
 - <b>`attached_events`</b>:  If true, it will additionally load attachedEventsIds. 



**Returns:**
 Iterable object which return messages as parts of streaming response or message stream pointers. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
