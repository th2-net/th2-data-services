<!-- markdownlint-disable -->

<a href="../../th2_data_services/data_source.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `data_source`






---

<a href="../../th2_data_services/data_source.py#L19"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `DataSource`
The class that provides methods for getting messages and events from rpt-data-provider. 

<a href="../../th2_data_services/data_source.py#L22"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(url: str, chunk_length: int = 65536)
```






---

#### <kbd>property</kbd> url

str: URL of rpt-data-provider. 



---

<a href="../../th2_data_services/data_source.py#L304"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `find_events_by_id_from_data_provider`

```python
find_events_by_id_from_data_provider(
    events_id: Union[Iterable, str]
) → Union[List[dict], dict, NoneType]
```

Gets event/events by ids. 



**Args:**
 
 - <b>`messages_id`</b>:  One str with EventID or list of EventsIDs. 



**Returns:**
 List[Event_dict] if you request a list or Event_dict. 

---

<a href="../../th2_data_services/data_source.py#L268"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `find_messages_by_id_from_data_provider`

```python
find_messages_by_id_from_data_provider(
    messages_id: Union[Iterable, str]
) → Union[List[dict], dict, NoneType]
```

Gets message/messages by ids. 



**Args:**
 
 - <b>`messages_id`</b>:  One str with MessageID or list of MessagesIDs. 



**Returns:**
 List[Message_dict] if you request a list or Message_dict. 



**Example:**
 ``` How to use.```

    >>> data_source.find_messages_by_id_from_data_provider('demo-conn1:first:1619506157132265837')
    Returns 1 message (dict).

    >>> data_source.find_messages_by_id_from_data_provider(['demo-conn1:first:1619506157132265836'])
    Returns list(dict) with 1 message.

    >>> data_source.find_messages_by_id_from_data_provider([
         'demo-conn1:first:1619506157132265836',
         'demo-conn1:first:1619506157132265833',
    ])
    Returns list(dict) with 2 messages.


---

<a href="../../th2_data_services/data_source.py#L83"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_events_from_data_provider`

```python
get_events_from_data_provider(cache: bool = False, **kwargs) → Data
```

Sends SSE request for getting events. 

For help use this readme https://github.com/th2-net/th2-rpt-data-provider#sse-requests-api on route http://localhost:8080/search/sse/events. 



**Args:**
 
 - <b>`cache`</b> (bool):  If True all requested data from rpt-data-provider will be saved to cache.  (See `use_cache` method in `Data` class). 
 - <b>`kwargs`</b>:  th2-rpt-data-provider API query options. 



**Returns:**
 
 - <b>`Data`</b>:  Data object with Events. 

---

<a href="../../th2_data_services/data_source.py#L115"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_messages_from_data_provider`

```python
get_messages_from_data_provider(cache: bool = False, **kwargs) → Data
```

Sends SSE request for getting messages. 

For help use this readme https://github.com/th2-net/th2-rpt-data-provider#sse-requests-api on route http://localhost:8080/search/sse/messages. 



**Args:**
 
 - <b>`cache`</b> (bool):  If True all requested data from rpt-data-provider will be saved to cache.  (See `use_cache` method in `Data` class). 
 - <b>`kwargs`</b>:  th2-rpt-data-provider API query options. 



**Returns:**
 
 - <b>`Data`</b>:  Data object with Messages. 

---

<a href="../../th2_data_services/data_source.py#L324"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `read_csv_file`

```python
read_csv_file(*sources: str) → Generator[str, NoneType, NoneType]
```

Gets data in a stream way from csv files. 



**Args:**
 
 - <b>`sources`</b>:  Path to files. 



**Yields:**
 
 - <b>`dict`</b>:  Csv files payload. 

---

<a href="../../th2_data_services/data_source.py#L56"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `sse_request_to_data_provider`

```python
sse_request_to_data_provider(**kwargs) → Generator[dict, NoneType, NoneType]
```

Sends SSE request to rpt-data-provider. 

It used for create custom sse-request to data-provider use this readme https://github.com/th2-net/th2-rpt-data-provider#readme. 



**Args:**
 
 - <b>`kwargs`</b>:  Query options. 



**Yields:**
 
 - <b>`dict`</b>:  SSE response data. 

---

<a href="../../th2_data_services/data_source.py#L340"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `write_to_txt`

```python
write_to_txt(data: Generator[str, NoneType, NoneType], source: str) → None
```

Writes to txt files. 



**Args:**
 
 - <b>`data`</b>:  Data. 
 - <b>`source`</b>:  Path to file. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
