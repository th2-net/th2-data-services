<!-- markdownlint-disable -->

<a href="../../th2_data_services/provider/v5/commands/http.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `provider.v5.commands.http`




**Global Variables**
---------------
- **UNICODE_REPLACE_HANDLER**


---

<a href="../../th2_data_services/provider/v5/commands/http.py#L35"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetEventById`
A Class-Command for request to rpt-data-provider. 

It retrieves the event by id. 



**Returns:**
 
 - <b>`dict`</b>:  Th2 event. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L44"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(id: str)
```

GetEventById constructor. 



**Args:**
 
 - <b>`id`</b>:  Event id. 




---

<a href="../../th2_data_services/provider/v5/commands/http.py#L55"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: HTTPProvider5DataSource) → dict
```





---

<a href="../../th2_data_services/provider/v5/commands/http.py#L73"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `use_stub`

```python
use_stub()
```






---

<a href="../../th2_data_services/provider/v5/commands/http.py#L78"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetEventsById`
A Class-Command for request to rpt-data-provider. 

It retrieves the events by ids. 



**Returns:**
 
 - <b>`List[dict]`</b>:  Th2 events. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L87"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(ids: List[str])
```

GetEventsById constructor. 



**Args:**
 
 - <b>`ids`</b>:  Event id list. 




---

<a href="../../th2_data_services/provider/v5/commands/http.py#L98"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: HTTPProvider5DataSource)
```





---

<a href="../../th2_data_services/provider/v5/commands/http.py#L113"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `use_stub`

```python
use_stub()
```






---

<a href="../../th2_data_services/provider/v5/commands/http.py#L118"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetEventsSSEBytes`
A Class-Command for request to rpt-data-provider. 

It searches events stream by options. 



**Returns:**
 
 - <b>`Iterable[dict]`</b>:  Stream of Th2 events. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L127"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    start_timestamp: datetime,
    end_timestamp: datetime = None,
    parent_event: str = None,
    search_direction: str = 'next',
    resume_from_id: str = None,
    result_count_limit: int = None,
    keep_open: bool = False,
    limit_for_parent: int = None,
    attached_messages: bool = False,
    filters: (<class 'Filter'>, List[Filter]) = None
)
```

GetEventsSSEBytes constructor. 



**Args:**
 
 - <b>`start_timestamp`</b>:  Start timestamp of search. 
 - <b>`end_timestamp`</b>:  End timestamp of search. 
 - <b>`parent_event`</b>:  Match events to the specified parent. 
 - <b>`search_direction`</b>:  Search direction. 
 - <b>`resume_from_id`</b>:  Event id from which search starts. 
 - <b>`result_count_limit`</b>:  Result count limit. 
 - <b>`keep_open`</b>:  If the search has reached the current moment.  It is need to wait further for the appearance of new data.  the one closest to the specified timestamp. 
 - <b>`limit_for_parent`</b>:  How many children events for each parent do we want to request. 
 - <b>`attached_messages`</b>:  Gets messages ids which linked to events. 
 - <b>`filters`</b>:  Filters using in search for messages. 




---

<a href="../../th2_data_services/provider/v5/commands/http.py#L174"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: HTTPProvider5DataSource)
```






---

<a href="../../th2_data_services/provider/v5/commands/http.py#L198"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetEventsSSEEvents`
A Class-Command for request to rpt-data-provider. 

It searches events stream by options. 



**Returns:**
 
 - <b>`Iterable[dict]`</b>:  Stream of Th2 events. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L207"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    start_timestamp: datetime,
    end_timestamp: datetime = None,
    parent_event: str = None,
    search_direction: str = 'next',
    resume_from_id: str = None,
    result_count_limit: int = None,
    keep_open: bool = False,
    limit_for_parent: int = None,
    attached_messages: bool = False,
    filters: (<class 'Filter'>, List[Filter]) = None,
    char_enc: str = 'utf-8',
    decode_error_handler: str = 'unicode_replace'
)
```

GetEventsSSEEvents constructor. 



**Args:**
 
 - <b>`start_timestamp`</b>:  Start timestamp of search. 
 - <b>`end_timestamp`</b>:  End timestamp of search. 
 - <b>`parent_event`</b>:  Match events to the specified parent. 
 - <b>`search_direction`</b>:  Search direction. 
 - <b>`resume_from_id`</b>:  Event id from which search starts. 
 - <b>`result_count_limit`</b>:  Result count limit. 
 - <b>`keep_open`</b>:  If the search has reached the current moment.  It is need to wait further for the appearance of new data.  the one closest to the specified timestamp. 
 - <b>`limit_for_parent`</b>:  How many children events for each parent do we want to request. 
 - <b>`attached_messages`</b>:  Gets messages ids which linked to events. 
 - <b>`filters`</b>:  Filters using in search for messages. 
 - <b>`char_enc`</b>:  Encoding for the byte stream. 
 - <b>`decode_error_handler`</b>:  Registered decode error handler. 




---

<a href="../../th2_data_services/provider/v5/commands/http.py#L255"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: HTTPProvider5DataSource)
```






---

<a href="../../th2_data_services/provider/v5/commands/http.py#L275"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetEvents`
A Class-Command for request to rpt-data-provider. 

It searches events stream by options. 



**Returns:**
 
 - <b>`Iterable[dict]`</b>:  Stream of Th2 events. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L284"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    start_timestamp: datetime,
    end_timestamp: datetime = None,
    parent_event: str = None,
    search_direction: str = 'next',
    resume_from_id: str = None,
    result_count_limit: int = None,
    keep_open: bool = False,
    limit_for_parent: int = None,
    attached_messages: bool = False,
    filters: (<class 'Filter'>, List[Filter]) = None,
    cache: bool = False
)
```

GetEvents constructor. 



**Args:**
 
 - <b>`start_timestamp`</b>:  Start timestamp of search. 
 - <b>`end_timestamp`</b>:  End timestamp of search. 
 - <b>`parent_event`</b>:  Match events to the specified parent. 
 - <b>`search_direction`</b>:  Search direction. 
 - <b>`resume_from_id`</b>:  Event id from which search starts. 
 - <b>`result_count_limit`</b>:  Result count limit. 
 - <b>`keep_open`</b>:  If the search has reached the current moment.  It is need to wait further for the appearance of new data.  the one closest to the specified timestamp. 
 - <b>`limit_for_parent`</b>:  How many children events for each parent do we want to request. 
 - <b>`attached_messages`</b>:  Gets messages ids which linked to events. 
 - <b>`filters`</b>:  Filters using in search for messages. 
 - <b>`cache`</b>:  If True, all requested data from rpt-data-provider will be saved to cache. 




---

<a href="../../th2_data_services/provider/v5/commands/http.py#L329"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: HTTPProvider5DataSource) → Data
```






---

<a href="../../th2_data_services/provider/v5/commands/http.py#L353"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetMessageById`
A Class-Command for request to rpt-data-provider. 

It retrieves the message by id. 



**Returns:**
 
 - <b>`dict`</b>:  Th2 message. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L362"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(id: str)
```

GetMessageById constructor. 



**Args:**
 
 - <b>`id`</b>:  Message id. 




---

<a href="../../th2_data_services/provider/v5/commands/http.py#L373"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: HTTPProvider5DataSource)
```





---

<a href="../../th2_data_services/provider/v5/commands/http.py#L391"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `use_stub`

```python
use_stub()
```






---

<a href="../../th2_data_services/provider/v5/commands/http.py#L396"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetMessagesById`
A Class-Command for request to rpt-data-provider. 

It retrieves the messages by ids. 



**Returns:**
 
 - <b>`List[dict]`</b>:  Th2 messages. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L405"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(ids: List[str])
```

GetMessagesById constructor. 



**Args:**
 
 - <b>`ids`</b>:  Message id list. 




---

<a href="../../th2_data_services/provider/v5/commands/http.py#L416"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: HTTPProvider5DataSource)
```





---

<a href="../../th2_data_services/provider/v5/commands/http.py#L431"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `use_stub`

```python
use_stub()
```






---

<a href="../../th2_data_services/provider/v5/commands/http.py#L436"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetMessagesSSEBytes`
A Class-Command for request to rpt-data-provider. 

It searches messages stream by options. 



**Returns:**
 
 - <b>`Iterable[dict]`</b>:  Stream of Th2 messages. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L445"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    start_timestamp: datetime,
    stream: List[str],
    end_timestamp: datetime = None,
    resume_from_id: str = None,
    search_direction: str = 'next',
    result_count_limit: int = None,
    keep_open: bool = False,
    message_id: List[str] = None,
    attached_events: bool = False,
    lookup_limit_days: int = None,
    filters: (<class 'Filter'>, List[Filter]) = None
)
```

GetMessagesSSEBytes constructor. 



**Args:**
 
 - <b>`start_timestamp`</b>:  Start timestamp of search. 
 - <b>`end_timestamp`</b>:  End timestamp of search. 
 - <b>`stream`</b>:  Alias of messages. 
 - <b>`resume_from_id`</b>:  Message id from which search starts. 
 - <b>`search_direction`</b>:  Search direction. 
 - <b>`result_count_limit`</b>:  Result count limit. 
 - <b>`keep_open`</b>:  If the search has reached the current moment.  It is need to wait further for the appearance of new data. 
 - <b>`message_id`</b>:  List of message IDs to restore search. If given, it has  the highest priority and ignores stream (uses streams from ids), startTimestamp and resumeFromId. 
 - <b>`attached_events`</b>:  If true, additionally load attached_event_ids 
 - <b>`lookup_limit_days`</b>:  The number of days that will be viewed on  the first request to get the one closest to the specified timestamp. 
 - <b>`filters`</b>:  Filters using in search for messages. 




---

<a href="../../th2_data_services/provider/v5/commands/http.py#L498"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(
    data_source: HTTPProvider5DataSource
) → Generator[dict, NoneType, NoneType]
```






---

<a href="../../th2_data_services/provider/v5/commands/http.py#L533"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetMessagesSSEEvents`
A Class-Command for request to rpt-data-provider. 

It searches messages stream by options. 



**Returns:**
 
 - <b>`Iterable[dict]`</b>:  Stream of Th2 messages. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L542"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    start_timestamp: datetime,
    stream: List[str],
    end_timestamp: datetime = None,
    resume_from_id: str = None,
    search_direction: str = 'next',
    result_count_limit: int = None,
    keep_open: bool = False,
    message_id: List[str] = None,
    attached_events: bool = False,
    lookup_limit_days: int = None,
    filters: (<class 'Filter'>, List[Filter]) = None,
    char_enc: str = 'utf-8',
    decode_error_handler: str = 'unicode_replace'
)
```

GetMessagesSSEEvents constructor. 



**Args:**
 
 - <b>`start_timestamp`</b>:  Start timestamp of search. 
 - <b>`end_timestamp`</b>:  End timestamp of search. 
 - <b>`stream`</b>:  Alias of messages. 
 - <b>`resume_from_id`</b>:  Message id from which search starts. 
 - <b>`search_direction`</b>:  Search direction. 
 - <b>`result_count_limit`</b>:  Result count limit. 
 - <b>`keep_open`</b>:  If the search has reached the current moment.  It is need to wait further for the appearance of new data. 
 - <b>`message_id`</b>:  List of message IDs to restore search. If given, it has  the highest priority and ignores stream (uses streams from ids), startTimestamp and resumeFromId. 
 - <b>`attached_events`</b>:  If true, additionally load attached_event_ids 
 - <b>`lookup_limit_days`</b>:  The number of days that will be viewed on  the first request to get the one closest to the specified timestamp. 
 - <b>`filters`</b>:  Filters using in search for messages. 
 - <b>`char_enc`</b>:  Character encode that will use SSEClient. 
 - <b>`decode_error_handler`</b>:  Decode error handler. 




---

<a href="../../th2_data_services/provider/v5/commands/http.py#L593"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(
    data_source: HTTPProvider5DataSource
) → Generator[dict, NoneType, NoneType]
```






---

<a href="../../th2_data_services/provider/v5/commands/http.py#L615"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetMessages`
A Class-Command for request to rpt-data-provider. 

It searches messages stream by options. 



**Returns:**
 
 - <b>`Iterable[dict]`</b>:  Stream of Th2 messages. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L624"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    start_timestamp: datetime,
    stream: List[str],
    end_timestamp: datetime = None,
    resume_from_id: str = None,
    search_direction: str = 'next',
    result_count_limit: int = None,
    keep_open: bool = False,
    message_id: List[str] = None,
    attached_events: bool = False,
    lookup_limit_days: int = None,
    filters: (<class 'Filter'>, List[Filter]) = None,
    char_enc: str = 'utf-8',
    decode_error_handler: str = 'unicode_replace',
    cache: bool = False
)
```

GetMessages constructor. 



**Args:**
 
 - <b>`start_timestamp`</b>:  Start timestamp of search. 
 - <b>`end_timestamp`</b>:  End timestamp of search. 
 - <b>`stream`</b>:  Alias of messages. 
 - <b>`resume_from_id`</b>:  Message id from which search starts. 
 - <b>`search_direction`</b>:  Search direction. 
 - <b>`result_count_limit`</b>:  Result count limit. 
 - <b>`keep_open`</b>:  If the search has reached the current moment.  It is need to wait further for the appearance of new data. 
 - <b>`message_id`</b>:  List of message IDs to restore search. If given, it has  the highest priority and ignores stream (uses streams from ids), startTimestamp and resumeFromId. 
 - <b>`attached_events`</b>:  If true, additionally load attached_event_ids 
 - <b>`lookup_limit_days`</b>:  The number of days that will be viewed on  the first request to get the one closest to the specified timestamp. 
 - <b>`filters`</b>:  Filters using in search for messages. 
 - <b>`char_enc`</b>:  Encoding for the byte stream. 
 - <b>`decode_error_handler`</b>:  Registered decode error handler. 
 - <b>`cache`</b>:  If True, all requested data from rpt-data-provider will be saved to cache. 




---

<a href="../../th2_data_services/provider/v5/commands/http.py#L678"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: HTTPProvider5DataSource) → Data
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
