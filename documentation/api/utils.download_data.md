<!-- markdownlint-disable -->

<a href="../../th2_data_services/utils/download_data.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.download_data`





---

<a href="../../th2_data_services/utils/download_data.py#L11"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `download_events`

```python
download_events(
    start_timestamp: str,
    end_timestamp: str,
    provider_url: str,
    add_earlier_parents: bool = False,
    events_cache_file: str = 'events_download.pickle'
) → Data
```

Downloads events. 



**Args:**
 
 - <b>`start_timestamp`</b>:  Download events from this timestamp 
 - <b>`end_timestamp`</b>:  Download events till this timestamp 
 - <b>`provider_url`</b>:  Provider url. e.g: http://localhost:8000 
 - <b>`add_earlier_parents`</b>:  Collect parents before given timeframe 
 - <b>`events_cache_file`</b>:  Output pickle file, defaults to "events_download.pickle" 



**Returns:**
 Data 


---

<a href="../../th2_data_services/utils/download_data.py#L67"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `download_events_and_messages`

```python
download_events_and_messages(
    start_timestamp: str,
    end_timestamp: str,
    provider_url: str,
    add_earlier_parents: bool = False,
    events_cache_file: str = 'events_download.pickle',
    messages_cache_file: str = 'messages.pickle'
) → Tuple[Data, Data]
```

Downloads events and messages. 



**Args:**
 
 - <b>`start_timestamp`</b>:  Download from this timestamp 
 - <b>`end_timestamp`</b>:  Download till this timestamp 
 - <b>`provider_url`</b>:  Provider url. e.g: http://localhost:8000 
 - <b>`add_earlier_parents`</b>:  Collect parents before given timeframe 
 - <b>`events_cache_file`</b>:  Output pickle file for events, defaults to "events_download.pickle" 
 - <b>`messages_cache_file`</b>:  Output pickle file for messages, defaults to "messages.pickle" 



**Returns:**
 Tuple[Data, Data], Events & Messages 


---

<a href="../../th2_data_services/utils/download_data.py#L119"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `prepare_story_from_storage`

```python
prepare_story_from_storage(
    provider_url: str,
    story_items: List,
    event_body_processors=None
)
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
