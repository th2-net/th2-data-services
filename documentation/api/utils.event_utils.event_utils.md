<!-- markdownlint-disable -->

<a href="../../th2_data_services/utils/event_utils/event_utils.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.event_utils.event_utils`





---

<a href="../../th2_data_services/utils/event_utils/event_utils.py#L20"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_some`

```python
get_some(
    events: List[Dict],
    event_type: Optional[str],
    count: int,
    start: int = 0,
    failed: bool = False
) → List[Dict]
```

Returns limited list of events of specific eventType. 



**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 
 - <b>`event_type`</b> (str):  Event Type To Extract 
 - <b>`count`</b> (int):  Maximum number of events to extract 
 - <b>`start`</b> (int, optional):  Start Iteration Index. Defaults to 0. 
 - <b>`failed`</b> (bool, optional):  Extract Only Failed Events. Defaults to False. 



**Returns:**
 List[Dict] 



**Example:**
 ``` get_some(events=events,```
                  event_type="ModelCase",
                  count=100,
                  start=0
                  failed=False)
         [
             {**TH2-Event},
             ...
         ]



---

<a href="../../th2_data_services/utils/event_utils/event_utils.py#L70"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `build_roots_cache`

```python
build_roots_cache(events: List[Dict], depth: int, max_level: int) → Dict
```

Returns event path for each event. 



**Notes:**

> Event path from root to event, it's a string of event names separated by `/` 
>

**Args:**
 
 - <b>`events`</b>:  TH2-Events 
 - <b>`depth`</b>:  Max depth to search 
 - <b>`max_level`</b>:  Max events from leaf 



**Returns:**
 Dict[str, Dict[str, str]] 



**Example:**
 ``` build_roots_cache(events=events,```
                           depth=10,
                           max_level=10)
         {
             eventId: {
                 eventName: "example event name",
                 eventPath: "rootName/.../currentEventName"
             },
             ...
         }



---

<a href="../../th2_data_services/utils/event_utils/event_utils.py#L124"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `extract_start_timestamp`

```python
extract_start_timestamp(event: Dict) → str
```

Returns string representation of events timestamp. 



**Args:**
 
 - <b>`event`</b>:  TH2-Event 



**Returns:**
 str 


---

<a href="../../th2_data_services/utils/event_utils/event_utils.py#L137"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `extract_parent_as_json`

```python
extract_parent_as_json(
    events: List[Dict],
    parent_id: str,
    json_file_path: str,
    interval_start: str,
    interval_end: str,
    body_to_simple_processors: Callable = None
)
```

Parse parent into JSON format. 



**Args:**
 
 - <b>`events`</b> (Dict):  TH2-Events 
 - <b>`parent_id`</b> (str):  Parent ID 
 - <b>`json_file_path`</b> (str):  file JSON output path 
 - <b>`interval_start`</b> (str):  Use events from this timestamp 
 - <b>`interval_end`</b> (str):  Use events till this timestamp 
 - <b>`body_to_simple_processors`</b> (Callable, optional):  Body categorizer function, defaults to None. 



**Example:**
 ``` extract_parent_as_json(```
             events=data,
             parent_id="demo_parent_id",
             json_file_path="path/to/output.json",
             interval_start="2022-03-16T08:40:16",
             interval_end="2022-03-16T14:40:16"
         )

JSON structure:
    {
         "info": {
               "stats": EventType+Status (Frequency Table),
               parent_event_details...
         }
         "child_id": {
             "info": { event_details...}
             "child_id": {
                 "info": { event_details...}
                 "body" { ... } # If event has body
                 "childId": { ... }
             }
         }
         "child_id2": { ... }
    }





---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
