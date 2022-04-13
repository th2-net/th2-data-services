<!-- markdownlint-disable -->

<a href="../../th2_data_services/provider/v5/provider_api/http.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `provider.v5.provider_api.http`




**Global Variables**
---------------
- **UNICODE_REPLACE_HANDLER**


---

<a href="../../th2_data_services/provider/v5/provider_api/http.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `HTTPProvider5API`




<a href="../../th2_data_services/provider/v5/provider_api/http.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    url: str,
    chunk_length: int = 65536,
    decode_error_handler: str = 'unicode_replace',
    char_enc: str = 'utf-8'
)
```

HTTP Provider5 API. 



**Args:**
 
 - <b>`url`</b>:  HTTP data source url. 
 - <b>`chunk_length`</b>:  How much of the content to read in one chunk. 
 - <b>`char_enc`</b>:  Encoding for the byte stream. 
 - <b>`decode_error_handler`</b>:  Registered decode error handler. 




---

<a href="../../th2_data_services/provider/v5/provider_api/http.py#L235"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `execute_request`

```python
execute_request(url: str) → Response
```

Sends a GET request to provider. 



**Args:**
 
 - <b>`url`</b>:  Url for a get request to rpt-data-provider. 



**Returns:**
 
 - <b>`requests.Response`</b>:  Response data. 

---

<a href="../../th2_data_services/provider/v5/provider_api/http.py#L211"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `execute_sse_request`

```python
execute_sse_request(url: str) → Generator[bytes, NoneType, NoneType]
```

Create stream connection. 



**Args:**
 
 - <b>`url`</b>:  Url. 



**Yields:**
 
 - <b>`str`</b>:  Response stream data. 

---

<a href="../../th2_data_services/provider/v5/provider_api/http.py#L97"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_url_event_filter_info`

```python
get_url_event_filter_info(filter_name: str) → str
```

SSE-API `filters/sse-events/{filter_name}` call returns filter info. 

https://github.com/th2-net/th2-rpt-data-provider#filters-api 

---

<a href="../../th2_data_services/provider/v5/provider_api/http.py#L83"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_url_events_filters`

```python
get_url_events_filters() → str
```

SSE-API `/filters/sse-events` call returns all names of sse event filters. 

https://github.com/th2-net/th2-rpt-data-provider#filters-api 

---

<a href="../../th2_data_services/provider/v5/provider_api/http.py#L56"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_url_find_event_by_id`

```python
get_url_find_event_by_id(event_id: str) → str
```

REST-API `event` call returns a single event with the specified id. 

---

<a href="../../th2_data_services/provider/v5/provider_api/http.py#L60"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_url_find_events_by_id`

```python
get_url_find_events_by_id(*ids) → str
```

REST-API `events` call returns a list of events with the specified ids. 

Note, at a time you can request no more eventSearchChunkSize. 

Deprecated, use `get_url_find_event_by_id` instead. 

---

<a href="../../th2_data_services/provider/v5/provider_api/http.py#L72"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_url_find_message_by_id`

```python
get_url_find_message_by_id(message_id: str) → str
```

REST-API `message` call returns a single message with the specified id. 

---

<a href="../../th2_data_services/provider/v5/provider_api/http.py#L104"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_url_match_event_by_id`

```python
get_url_match_event_by_id(event_id: str, filters: str = '') → str
```

REST-API `match/event/{id}` call returns boolean value. 

Checks that event with the specified id is matched by filter. 

https://github.com/th2-net/th2-rpt-data-provider#filters-api 

---

<a href="../../th2_data_services/provider/v5/provider_api/http.py#L113"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_url_match_message_by_id`

```python
get_url_match_message_by_id(message_id: str, filters: str = '') → str
```

REST-API `match/message/{id}` call returns boolean value. 

Checks that message with the specified id is matched by filter. 

https://github.com/th2-net/th2-rpt-data-provider#filters-api 

---

<a href="../../th2_data_services/provider/v5/provider_api/http.py#L90"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_url_message_filter_info`

```python
get_url_message_filter_info(filter_name: str) → str
```

SSE-API `filters/sse-messages/{filter name}` call returns filter info. 

https://github.com/th2-net/th2-rpt-data-provider#filters-api 

---

<a href="../../th2_data_services/provider/v5/provider_api/http.py#L52"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_url_message_streams`

```python
get_url_message_streams() → str
```

REST-API `messageStreams` call returns a list of message stream names. 

---

<a href="../../th2_data_services/provider/v5/provider_api/http.py#L76"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_url_messages_filters`

```python
get_url_messages_filters() → str
```

SSE-API `filters/sse-messages` call returns all names of sse message filters. 

https://github.com/th2-net/th2-rpt-data-provider#filters-api 

---

<a href="../../th2_data_services/provider/v5/provider_api/http.py#L122"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_url_search_sse_events`

```python
get_url_search_sse_events(
    start_timestamp: int,
    end_timestamp: Optional[int] = None,
    parent_event: Optional[str] = None,
    resume_from_id: Optional[str] = None,
    search_direction: Optional[str] = 'next',
    result_count_limit: Union[int, float] = None,
    keep_open: Optional[bool] = False,
    limit_for_parent: Union[int, float] = None,
    metadata_only: Optional[bool] = True,
    attached_messages: Optional[bool] = False,
    filters: Optional[str] = None
) → str
```

REST-API `search/sse/events` call create a sse channel of event metadata that matches the filter. 

https://github.com/th2-net/th2-rpt-data-provider#sse-requests-api 

---

<a href="../../th2_data_services/provider/v5/provider_api/http.py#L165"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_url_search_sse_messages`

```python
get_url_search_sse_messages(
    start_timestamp: int,
    stream: List[str],
    end_timestamp: Optional[int] = None,
    resume_from_id: Optional[str] = None,
    search_direction: Optional[str] = 'next',
    result_count_limit: Union[int, float] = None,
    keep_open: bool = False,
    message_id: Optional[List[str]] = None,
    attached_events: bool = False,
    lookup_limit_days: Union[int, float] = None,
    filters: Optional[str] = None
) → str
```

REST-API `search/sse/messages` call create a sse channel of messages that matches the filter. 

https://github.com/th2-net/th2-rpt-data-provider#sse-requests-api 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
