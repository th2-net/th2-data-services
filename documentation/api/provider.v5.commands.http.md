<!-- markdownlint-disable -->

<a href="../../th2_data_services/provider/v5/commands/http.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `provider.v5.commands.http`




**Global Variables**
---------------
- **UNICODE_REPLACE_HANDLER**


---

<a href="../../th2_data_services/provider/v5/commands/http.py#L47"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetEventById`
A Class-Command for request to rpt-data-provider. 

It retrieves the event by id with `attachedMessageIds` list. 



**Returns:**
 
 - <b>`dict`</b>:  Th2 event. 



**Raises:**
 
 - <b>`EventNotFound`</b>:  If event by Id wasn't found. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L59"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(id: str, use_stub=False)
```

GetEventById constructor. 



**Args:**
 
 - <b>`id`</b>:  Event id. 
 - <b>`use_stub`</b>:  If True the command returns stub instead of exception. 




---

<a href="../../th2_data_services/provider/v5/commands/http.py#L71"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: HTTPProvider5DataSource) → dict
```






---

<a href="../../th2_data_services/provider/v5/commands/http.py#L88"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetEventsById`
A Class-Command for request to rpt-data-provider. 

It retrieves the events by ids with `attachedMessageIds` list. 



**Returns:**
 
 - <b>`List[dict]`</b>:  Th2 events. 



**Raises:**
 
 - <b>`EventNotFound`</b>:  If any event by Id wasn't found. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L100"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(ids: List[str], use_stub=False)
```

GetEventsById constructor. 



**Args:**
 
 - <b>`ids`</b>:  Event id list. 
 - <b>`use_stub`</b>:  If True the command returns stub instead of exception. 




---

<a href="../../th2_data_services/provider/v5/commands/http.py#L112"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: HTTPProvider5DataSource)
```






---

<a href="../../th2_data_services/provider/v5/commands/http.py#L121"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetEventsSSEBytes`
A Class-Command for request to rpt-data-provider. 

It searches events stream by options. 



**Returns:**
 
 - <b>`Iterable[dict]`</b>:  Stream of Th2 events. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L130"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
    filters: Union[Filter, Provider5EventFilter, Sequence[Union[Filter, Provider5EventFilter]]] = None
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

<a href="../../th2_data_services/provider/v5/commands/http.py#L173"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: HTTPProvider5DataSource)
```






---

<a href="../../th2_data_services/provider/v5/commands/http.py#L197"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetEventsSSEEvents`
A Class-Command for request to rpt-data-provider. 

It searches events stream by options. 



**Returns:**
 
 - <b>`Iterable[dict]`</b>:  Stream of Th2 events. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L206"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
    filters: Union[Filter, Provider5EventFilter, Sequence[Union[Filter, Provider5EventFilter]]] = None,
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

<a href="../../th2_data_services/provider/v5/commands/http.py#L254"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: HTTPProvider5DataSource)
```






---

<a href="../../th2_data_services/provider/v5/commands/http.py#L274"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetEvents`
A Class-Command for request to rpt-data-provider. 

It searches events stream by options. 



**Returns:**
 
 - <b>`Iterable[dict]`</b>:  Stream of Th2 events. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L283"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
    filters: Union[Filter, Provider5EventFilter, Sequence[Union[Filter, Provider5EventFilter]]] = None,
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

<a href="../../th2_data_services/provider/v5/commands/http.py#L328"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: HTTPProvider5DataSource) → Data
```






---

<a href="../../th2_data_services/provider/v5/commands/http.py#L352"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetMessageById`
A Class-Command for request to rpt-data-provider. 

It retrieves the message by id. 

Please note, Provider5 doesn't return `attachedEventIds`. It will be == []. It's expected that Provider7 will be support it. 



**Returns:**
 
 - <b>`dict`</b>:  Th2 message. 



**Raises:**
 
 - <b>`MessageNotFound`</b>:  If message by id wasn't found. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L367"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(id: str, use_stub=False)
```

GetMessageById constructor. 



**Args:**
 
 - <b>`id`</b>:  Message id. 
 - <b>`use_stub`</b>:  If True the command returns stub instead of exception. 




---

<a href="../../th2_data_services/provider/v5/commands/http.py#L379"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: HTTPProvider5DataSource) → dict
```






---

<a href="../../th2_data_services/provider/v5/commands/http.py#L396"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetMessagesById`
A Class-Command for request to rpt-data-provider. 

It retrieves the messages by ids. 

Please note, Provider5 doesn't return `attachedEventIds`. It will be == []. It's expected that Provider7 will be support it. 



**Returns:**
 
 - <b>`List[dict]`</b>:  Th2 messages. 



**Raises:**
 
 - <b>`MessageNotFound`</b>:  If any message by id wasn't found. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L411"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(ids: List[str], use_stub=False)
```

GetMessagesById constructor. 



**Args:**
 
 - <b>`ids`</b>:  Message id list. 
 - <b>`use_stub`</b>:  If True the command returns stub instead of exception. 




---

<a href="../../th2_data_services/provider/v5/commands/http.py#L423"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: HTTPProvider5DataSource) → List[dict]
```






---

<a href="../../th2_data_services/provider/v5/commands/http.py#L432"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetMessagesSSEBytes`
A Class-Command for request to rpt-data-provider. 

It searches messages stream by options. 



**Returns:**
 
 - <b>`Iterable[dict]`</b>:  Stream of Th2 messages. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L441"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
    filters: Union[Filter, Provider5MessageFilter, Sequence[Union[Filter, Provider5MessageFilter]]] = None
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

<a href="../../th2_data_services/provider/v5/commands/http.py#L490"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(
    data_source: HTTPProvider5DataSource
) → Generator[dict, NoneType, NoneType]
```






---

<a href="../../th2_data_services/provider/v5/commands/http.py#L524"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetMessagesSSEEvents`
A Class-Command for request to rpt-data-provider. 

It searches messages stream by options. 



**Returns:**
 
 - <b>`Iterable[dict]`</b>:  Stream of Th2 messages. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L533"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
    filters: Union[Filter, Provider5MessageFilter, Sequence[Union[Filter, Provider5MessageFilter]]] = None,
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

<a href="../../th2_data_services/provider/v5/commands/http.py#L584"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(
    data_source: HTTPProvider5DataSource
) → Generator[dict, NoneType, NoneType]
```






---

<a href="../../th2_data_services/provider/v5/commands/http.py#L606"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetMessages`
A Class-Command for request to rpt-data-provider. 

It searches messages stream by options. 



**Returns:**
 
 - <b>`Iterable[dict]`</b>:  Stream of Th2 messages. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L615"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
    filters: Union[Filter, Provider5MessageFilter, Sequence[Union[Filter, Provider5MessageFilter]]] = None,
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

<a href="../../th2_data_services/provider/v5/commands/http.py#L669"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: HTTPProvider5DataSource) → Data
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
