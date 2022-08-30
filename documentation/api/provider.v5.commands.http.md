<!-- markdownlint-disable -->

<a href="../../th2_data_services/provider/v5/commands/http.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `provider.v5.commands.http`




**Global Variables**
---------------
- **UNICODE_REPLACE_HANDLER**


---

<a href="../../th2_data_services/provider/v5/commands/http.py#L48"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetEventById`
A Class-Command for request to rpt-data-provider. 

It retrieves the event by id with `attachedMessageIds` list. 



**Returns:**
 
 - <b>`dict`</b>:  Th2 event. 



**Raises:**
 
 - <b>`EventNotFound`</b>:  If event by Id wasn't found. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L60"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(id: str, use_stub: bool = False, certification: bool = True)
```

GetEventById constructor. 



**Args:**
 
 - <b>`id`</b>:  Event id. 
 - <b>`use_stub`</b>:  If True the command returns stub instead of exception. 
 - <b>`certification`</b>:  Checking the ssl certificate. 




---

<a href="../../th2_data_services/provider/v5/commands/http.py#L73"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: HTTPProvider5DataSource) → dict
```






---

<a href="../../th2_data_services/provider/v5/commands/http.py#L90"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetEventsById`
A Class-Command for request to rpt-data-provider. 

It retrieves the events by ids with `attachedMessageIds` list. 



**Returns:**
 
 - <b>`List[dict]`</b>:  Th2 events. 



**Raises:**
 
 - <b>`EventNotFound`</b>:  If any event by Id wasn't found. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L102"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(ids: List[str], use_stub: bool = False, certification: bool = True)
```

GetEventsById constructor. 



**Args:**
 
 - <b>`ids`</b>:  Event id list. 
 - <b>`use_stub`</b>:  If True the command returns stub instead of exception. 
 - <b>`certification`</b>:  Checking the ssl certificate. 




---

<a href="../../th2_data_services/provider/v5/commands/http.py#L115"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: HTTPProvider5DataSource)
```






---

<a href="../../th2_data_services/provider/v5/commands/http.py#L126"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetEventsSSEBytes`
A Class-Command for request to rpt-data-provider. 

It searches events stream by options. 



**Returns:**
 
 - <b>`Iterable[dict]`</b>:  Stream of Th2 events. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L135"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
    certification: bool = True
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
 - <b>`certification`</b>:  Checking the ssl certificate. 




---

<a href="../../th2_data_services/provider/v5/commands/http.py#L181"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: HTTPProvider5DataSource)
```






---

<a href="../../th2_data_services/provider/v5/commands/http.py#L205"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetEventsSSEEvents`
A Class-Command for request to rpt-data-provider. 

It searches events stream by options. 



**Returns:**
 
 - <b>`Iterable[dict]`</b>:  Stream of Th2 events. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L214"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
    decode_error_handler: str = 'unicode_replace',
    certification: bool = True
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
 - <b>`certification`</b>:  Checking the ssl certificate. 




---

<a href="../../th2_data_services/provider/v5/commands/http.py#L264"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: HTTPProvider5DataSource)
```






---

<a href="../../th2_data_services/provider/v5/commands/http.py#L285"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetEvents`
A Class-Command for request to rpt-data-provider. 

It searches events stream by options. 



**Returns:**
 
 - <b>`Iterable[dict]`</b>:  Stream of Th2 events. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L294"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
    cache: bool = False,
    certification: bool = True
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
 - <b>`certification`</b>:  Checking the ssl certificate. 




---

<a href="../../th2_data_services/provider/v5/commands/http.py#L341"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: HTTPProvider5DataSource) → Data
```






---

<a href="../../th2_data_services/provider/v5/commands/http.py#L366"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetMessageById`
A Class-Command for request to rpt-data-provider. 

It retrieves the message by id. 

Please note, Provider5 doesn't return `attachedEventIds`. It will be == []. It's expected that Provider7 will be support it. 



**Returns:**
 
 - <b>`dict`</b>:  Th2 message. 



**Raises:**
 
 - <b>`MessageNotFound`</b>:  If message by id wasn't found. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L381"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(id: str, use_stub: bool = False, certification: bool = True)
```

GetMessageById constructor. 



**Args:**
 
 - <b>`id`</b>:  Message id. 
 - <b>`use_stub`</b>:  If True the command returns stub instead of exception. 
 - <b>`certification`</b>:  Checking the ssl certificate. 




---

<a href="../../th2_data_services/provider/v5/commands/http.py#L394"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: HTTPProvider5DataSource) → dict
```






---

<a href="../../th2_data_services/provider/v5/commands/http.py#L411"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetMessagesById`
A Class-Command for request to rpt-data-provider. 

It retrieves the messages by ids. 

Please note, Provider5 doesn't return `attachedEventIds`. It will be == []. It's expected that Provider7 will be support it. 



**Returns:**
 
 - <b>`List[dict]`</b>:  Th2 messages. 



**Raises:**
 
 - <b>`MessageNotFound`</b>:  If any message by id wasn't found. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L426"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(ids: List[str], use_stub: bool = False, certification: bool = True)
```

GetMessagesById constructor. 



**Args:**
 
 - <b>`ids`</b>:  Message id list. 
 - <b>`use_stub`</b>:  If True the command returns stub instead of exception. 
 - <b>`certification`</b>:  Checking the ssl certificate. 




---

<a href="../../th2_data_services/provider/v5/commands/http.py#L439"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: HTTPProvider5DataSource) → List[dict]
```






---

<a href="../../th2_data_services/provider/v5/commands/http.py#L450"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetMessagesSSEBytes`
A Class-Command for request to rpt-data-provider. 

It searches messages stream by options. 



**Returns:**
 
 - <b>`Iterable[dict]`</b>:  Stream of Th2 messages. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L459"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
    certification: bool = True
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
 - <b>`certification`</b>:  Checking the ssl certificate. 




---

<a href="../../th2_data_services/provider/v5/commands/http.py#L511"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(
    data_source: HTTPProvider5DataSource
) → Generator[dict, NoneType, NoneType]
```






---

<a href="../../th2_data_services/provider/v5/commands/http.py#L545"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetMessagesSSEEvents`
A Class-Command for request to rpt-data-provider. 

It searches messages stream by options. 



**Returns:**
 
 - <b>`Iterable[dict]`</b>:  Stream of Th2 messages. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L554"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
    certification: bool = True
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
 - <b>`certification`</b>:  Checking the ssl certificate. 




---

<a href="../../th2_data_services/provider/v5/commands/http.py#L608"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(
    data_source: HTTPProvider5DataSource
) → Generator[dict, NoneType, NoneType]
```






---

<a href="../../th2_data_services/provider/v5/commands/http.py#L631"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetMessages`
A Class-Command for request to rpt-data-provider. 

It searches messages stream by options. 



**Returns:**
 
 - <b>`Iterable[dict]`</b>:  Stream of Th2 messages. 

<a href="../../th2_data_services/provider/v5/commands/http.py#L640"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
    cache: bool = False,
    certification: bool = True
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
 - <b>`certification`</b>:  Checking the ssl certificate. 




---

<a href="../../th2_data_services/provider/v5/commands/http.py#L697"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: HTTPProvider5DataSource) → Data
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
