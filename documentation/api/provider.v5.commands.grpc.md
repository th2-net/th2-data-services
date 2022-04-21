<!-- markdownlint-disable -->

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `provider.v5.commands.grpc`






---

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetEventByIdGRPCObject`
A Class-Command for request to rpt-data-provider. 

It retrieves the event by id as GRPC object. 



**Returns:**
 
 - <b>`EventData`</b>:  Th2 event. 

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L50"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(id: str)
```

GetEventByIdGRPCObject constructor. 



**Args:**
 
 - <b>`id`</b>:  Event id. 




---

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L60"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: GRPCProvider5DataSource) → EventData
```






---

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L68"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetEventById`
A Class-Command for request to rpt-data-provider. 

It retrieves the event by id. 



**Returns:**
 
 - <b>`dict`</b>:  Th2 event. 



**Raises:**
 
 - <b>`EventNotFound`</b>:  If event by Id wasn't found. 

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L80"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(id: str, use_stub=False)
```

GetEventById constructor. 



**Args:**
 
 - <b>`id`</b>:  Event id. 
 - <b>`use_stub`</b>:  If True the command returns stub instead of exception. 




---

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L94"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: GRPCProvider5DataSource) → dict
```






---

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L110"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetEventsById`
A Class-Command for request to rpt-data-provider. 

It retrieves the events by id. 



**Returns:**
 
 - <b>`List[dict]`</b>:  Th2 events. 



**Raises:**
 
 - <b>`EventNotFound`</b>:  If any event by Id wasn't found. 

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L122"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(ids: List[str], use_stub=False)
```

GetEventsById constructor. 



**Args:**
 
 - <b>`ids`</b>:  Events ids. 
 - <b>`use_stub`</b>:  If True the command returns stub instead of exception. 




---

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L134"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: GRPCProvider5DataSource) → List[dict]
```






---

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L144"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetEventsGRPCObjects`
A Class-Command for request to rpt-data-provider. 

It searches events stream as GRPC object by options. 



**Returns:**
 
 - <b>`Iterable[EventData]`</b>:  Stream of Th2 events. 

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L153"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    start_timestamp: datetime,
    end_timestamp: datetime = None,
    parent_event: str = None,
    search_direction: str = 'NEXT',
    resume_from_id: str = None,
    result_count_limit: int = None,
    keep_open: bool = False,
    limit_for_parent: int = None,
    attached_messages: bool = False,
    filters: List[Filter] = None
)
```

GetEventsGRPCObjects constructor. 



**Args:**
 
 - <b>`start_timestamp`</b>:  Start timestamp of search. 
 - <b>`end_timestamp`</b>:  End timestamp of search. 
 - <b>`resume_from_id`</b>:  Event id from which search starts. 
 - <b>`parent_event`</b>:  Match events to the specified parent. 
 - <b>`search_direction`</b>:  Search direction. 
 - <b>`result_count_limit`</b>:  Result count limit. 
 - <b>`keep_open`</b>:  If the search has reached the current moment.  It is need to wait further for the appearance of new data.  the one closest to the specified timestamp. 
 - <b>`limit_for_parent`</b>:  How many children events for each parent do we want to request. 
 - <b>`attached_messages`</b>:  Gets messages ids which linked to events. 
 - <b>`filters`</b>:  Filters using in search for messages. 




---

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L196"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: GRPCProvider5DataSource) → Iterable[EventData]
```






---

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L221"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetEvents`
A Class-Command for request to rpt-data-provider. 

It searches events stream by options. 



**Returns:**
 
 - <b>`Iterable[dict]`</b>:  Stream of Th2 events. 

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L230"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    start_timestamp: datetime,
    end_timestamp: datetime = None,
    parent_event: str = None,
    search_direction: str = 'NEXT',
    resume_from_id: str = None,
    result_count_limit: int = None,
    keep_open: bool = False,
    limit_for_parent: int = None,
    attached_messages: bool = False,
    filters: List[Filter] = None,
    cache: bool = False
)
```

GetEvents constructor. 



**Args:**
 
 - <b>`start_timestamp`</b>:  Start timestamp of search. 
 - <b>`end_timestamp`</b>:  End timestamp of search. 
 - <b>`resume_from_id`</b>:  Event id from which search starts. 
 - <b>`parent_event`</b>:  Match events to the specified parent. 
 - <b>`search_direction`</b>:  Search direction. 
 - <b>`result_count_limit`</b>:  Result count limit. 
 - <b>`keep_open`</b>:  If the search has reached the current moment.  It is need to wait further for the appearance of new data.  the one closest to the specified timestamp. 
 - <b>`limit_for_parent`</b>:  How many children events for each parent do we want to request. 
 - <b>`attached_messages`</b>:  Gets messages ids which linked to events. 
 - <b>`filters`</b>:  Filters using in search for messages. 
 - <b>`cache`</b>:  If True, all requested data from rpt-data-provider will be saved to cache. 




---

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L279"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: GRPCProvider5DataSource) → Data
```






---

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L303"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetMessageByIdGRPCObject`
A Class-Command for request to rpt-data-provider. 

It retrieves the message by id as GRPC Object. 



**Returns:**
 
 - <b>`MessageData`</b>:  Th2 message. 

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L312"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(id: str)
```

GetMessageByIdGRPCObject constructor. 



**Args:**
 
 - <b>`id`</b>:  Message id. 




---

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L322"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: GRPCProvider5DataSource) → MessageData
```






---

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L329"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetMessageById`
A Class-Command for request to rpt-data-provider. 

It retrieves the message by id. 



**Returns:**
 
 - <b>`dict`</b>:  Th2 message. 



**Raises:**
 
 - <b>`MessageNotFound`</b>:  If message by id wasn't found. 

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L341"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(id: str, use_stub=False)
```

GetMessageById constructor. 



**Args:**
 
 - <b>`id`</b>:  Message id. 
 - <b>`use_stub`</b>:  If True the command returns stub instead of exception. 




---

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L355"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: GRPCProvider5DataSource) → dict
```






---

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L370"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetMessagesById`
A Class-Command for request to rpt-data-provider. 

It retrieves the messages by id. 



**Returns:**
 
 - <b>`List[dict]`</b>:  Th2 messages. 



**Raises:**
 
 - <b>`MessageNotFound`</b>:  If any message by id wasn't found. 

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L382"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(ids: List[str], use_stub=False)
```

GetMessagesById constructor. 



**Args:**
 
 - <b>`ids`</b>:  Messages id. 
 - <b>`use_stub`</b>:  If True the command returns stub instead of exception. 




---

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L394"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: GRPCProvider5DataSource) → List[dict]
```






---

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L404"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetMessagesGRPCObject`
A Class-Command for request to rpt-data-provider. 

It searches messages stream as GRPC object by options. 



**Returns:**
 
 - <b>`Iterable[MessageData]`</b>:  Stream of Th2 messages. 

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L413"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    start_timestamp: datetime,
    stream: List[str],
    end_timestamp: datetime = None,
    resume_from_id: str = None,
    search_direction: str = 'NEXT',
    result_count_limit: int = None,
    keep_open: bool = False,
    filters: List[Filter] = None
)
```

GetMessagesGRPCObject constructor. 



**Args:**
 
 - <b>`start_timestamp`</b>:  Start timestamp of search. 
 - <b>`end_timestamp`</b>:  End timestamp of search. 
 - <b>`stream`</b>:  Alias of messages. 
 - <b>`resume_from_id`</b>:  Message id from which search starts. 
 - <b>`search_direction`</b>:  Search direction. 
 - <b>`result_count_limit`</b>:  Result count limit. 
 - <b>`keep_open`</b>:  If the search has reached the current moment.  It is need to wait further for the appearance of new data. 
 - <b>`filters`</b>:  Filters using in search for messages. 




---

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L448"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: GRPCProvider5DataSource) → List[MessageData]
```






---

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L470"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetMessages`
A Class-Command for request to rpt-data-provider. 

It searches messages stream by options. 



**Returns:**
 
 - <b>`Iterable[dict]`</b>:  Stream of Th2 messages. 

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L479"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    start_timestamp: datetime,
    stream: List[str],
    end_timestamp: datetime = None,
    resume_from_id: str = None,
    search_direction: str = 'NEXT',
    result_count_limit: int = None,
    keep_open: bool = False,
    filters: List[Filter] = None,
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
 - <b>`filters`</b>:  Filters using in search for messages. 
 - <b>`cache`</b>:  If True, all requested data from rpt-data-provider will be saved to cache. 




---

<a href="../../th2_data_services/provider/v5/commands/grpc.py#L520"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `handle`

```python
handle(data_source: GRPCProvider5DataSource) → Data
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
