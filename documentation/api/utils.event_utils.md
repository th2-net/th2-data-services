<!-- markdownlint-disable -->

<a href="../../th2_data_services/utils/event_utils.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.event_utils`





---

<a href="../../th2_data_services/utils/event_utils.py#L13"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_category_frequencies`

```python
get_category_frequencies(
    events: List[Dict],
    categories: List[str],
    categorizer: Callable,
    aggregation_level: str = 'seconds'
) → List[List[str]]
```

Returns event frequencies based on event category. 



**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 
 - <b>`categories`</b> (List[str]):  Event Categories 
 - <b>`categorizer`</b> (Callable):  Categorizer Method 
 - <b>`aggregation_level`</b> (Optional, str):  Aggregation Level 



**Returns:**
 List[List[str]] 



**Example:**
 ``` get_category_frequencies(events=events,```
                                  categories=["Info", "ModelMatrix"],
                                  categorizer=lambda e: e["eventType"],
                                  aggregation_level="seconds" # Optional
                                  )
    [
         ['timestamp', 'Info', 'ModelMatrix'],
         ['2022-03-16T02:00:00', 4, 0],
         ['2022-03-16T02:00:31', 1, 0],
         ['2022-03-16T02:00:32', 4, 0],
         ...
    ]



---

<a href="../../th2_data_services/utils/event_utils.py#L60"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_type_frequencies`

```python
get_type_frequencies(
    events: List[Dict],
    types: List[str],
    aggregation_level='seconds'
) → List[List[str]]
```

Returns event frequencies based on event type. 



**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 
 - <b>`types`</b> (List[str]):  Event Types 
 - <b>`aggregation_level`</b> (Optional, str):  Aggregation Level 



**Returns:**
 
 - <b>`List[List[str]]`</b>:  List Of Frequency Lists 



**Example:**
 ``` get_type_frequencies(events=events, types=["Info", "ModelMatrix"])```
    [
         ['timestamp', 'Info', 'ModelMatrix'],
         ['2022-03-16T02:00:00', 4, 0],
         ['2022-03-16T02:00:31', 1, 0],
         ['2022-03-16T02:00:32', 4, 0],
         ...
    ]



---

<a href="../../th2_data_services/utils/event_utils.py#L88"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_category_totals`

```python
get_category_totals(
    events: List[Dict],
    categorizer: Callable[[Dict], str],
    ignore_status: bool = False
) → Dict[str, int]
```

Returns dictionary quantities of events for different categories. 



**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 
 - <b>`categorizer`</b> (Callable):  Categorizer function 
 - <b>`ignore_status`</b> (bool):  Concatenate status string, defaults to False. 



**Returns:**
 Dict[str, int] 



**Example:**
 ``` get_category_totals(events=events,```
                             categorizer=lambda e: e["eventType"])
         defaultdict(<class 'int'>, {'Service event [ok]': 9531, 'Info [ok]': 469})
    >>> get_category_totals(events=events,
                             categorizer=lambda e: e["eventType"],
                             ignore_status=True)
         defaultdict(<class 'int'>, {'Service event': 9531, 'Info': 469})



---

<a href="../../th2_data_services/utils/event_utils.py#L124"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_attached_messages_totals`

```python
get_attached_messages_totals(events: List[Dict]) → Dict[str, int]
```

Returns dictionary quantities of messages attached to events for each stream. 



**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 



**Returns:**
 Dict[str, int] 



**Example:**
 ``` get_attached_messages_totals(events=events)```
         defaultdict(<class 'int'>, {'envtn2_msfix5:first': 25262, 'envtn2_jpmfix1:second': 1702, ...)



---

<a href="../../th2_data_services/utils/event_utils.py#L149"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_attached_message_ids`

```python
get_attached_message_ids(events: List[Dict]) → Set[str]
```

Returns the set of unique message IDs linked to all events. 



**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 



**Returns:**
 Set[str] 



**Example:**
 ``` get_attached_message_ids(events=events)```
         {
           'demo_fix5:first:1646738629665873718',
           'demo_fixg2:second:1646736618848913837',
           ...
         }



---

<a href="../../th2_data_services/utils/event_utils.py#L175"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_prior_parent_ids`

```python
get_prior_parent_ids(events: List[Dict]) → Set[str]
```

Returns only parent events that are not present in the events. 



**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 



**Returns:**
 Set[str] 



**Example:**
 ``` get_prior_parent_ids(events=events)```
         {
             '009b3122-9ec1-ec11-91bd-ed37395ac9af',
             '014ac1d8-9ed2-ec11-ba0d-13099b4139e8',
             ...
         }



---

<a href="../../th2_data_services/utils/event_utils.py#L211"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_attached_message_ids_index`

```python
get_attached_message_ids_index(events: List[Dict]) → Dict[str, list]
```

Returns dict of lists of related events by unique message IDs. 



**Notes:**

> - This object can occupy large amount of memory for big collections of events - use with caution Keeps in memory all events that are linked to messages. - Event path from root to event, it's a string of event names separated by `/`. 
>

**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 



**Returns:**
 Dict[str, list] 



**Example:**
 ``` get_attached_message_ids_index(events=events)```
         {
             eventId: {
                 eventName: "example event name",
                 eventPath: "rootName/.../currentEventName"
             },
             ...
         }



---

<a href="../../th2_data_services/utils/event_utils.py#L249"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_type_totals`

```python
get_type_totals(events: List[Dict]) → Dict[str, int]
```

Returns dictionary quantities of events for different event types. 



**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 



**Returns:**
 Dict[str, int] 



**Example:**
 ``` get_type_totals(events=events)```
         {
             "eventType eventStatus": count,
             ...
         }



---

<a href="../../th2_data_services/utils/event_utils.py#L278"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/utils/event_utils.py#L322"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_related_events`

```python
get_related_events(
    events: List[Dict],
    messages: List[Dict],
    count: int
) → List[Dict]
```

Returns limited list of events of linked to any message within specified messages objects collection. 



**Args:**
 
 - <b>`events`</b>:  TH2-Events 
 - <b>`messages`</b>:  TH2-Messages 
 - <b>`count`</b>:  Maximum number of events to extract 



**Returns:**
 List[Dict] 



**Example:**
 ``` get_related_events(events=events,```
                            messages=messages,
                            count=10)
         [
             {**TH2-Event},
             ...
         ]



---

<a href="../../th2_data_services/utils/event_utils.py#L357"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_events_by_category`

```python
get_events_by_category(
    events: List[Dict],
    category: str,
    count: int,
    categorizer: Callable,
    start=0,
    failed=False
) → List[Dict]
```

Returns limited list of events of specific category produced by custom categorizer. 



**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 
 - <b>`category`</b> (str):  Event category to extract 
 - <b>`count`</b> (int):  Maximum number of events to extract 
 - <b>`categorizer`</b> (Callable):  Categorizer function 
 - <b>`start`</b> (int, optional):  Start iteration index, defaults to 0. 
 - <b>`failed`</b> (bool, optional):  Extract only failed events, defaults to False. 



**Returns:**
 List[Dict] 

``` # TODO: example!```
    [
         {**TH2-Event},
         ...
    ]



---

<a href="../../th2_data_services/utils/event_utils.py#L397"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_roots`

```python
get_roots(events: List[Dict], count: int, start: int = 0) → List[Dict]
```

Returns limited list of root events (events without parents). 



**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 
 - <b>`count`</b> (int):  Maximum number of events to extract 
 - <b>`start`</b> (int, optional):  Iteration Start Index, Defaults to 0. 



**Returns:**
 
 - <b>`List[Dict]`</b>:  List Of Root Events. 


---

<a href="../../th2_data_services/utils/event_utils.py#L424"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_parents`

```python
get_parents(events: List[Dict], children: List[Dict]) → List[Dict]
```

Returns all parent events of linked to any event within specified events objects collection. 



**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 
 - <b>`children`</b> (List[Dict]):  Extract Parents By Child Events 



**Returns:**
 List[Dict] 



**Example:**
 ``` get_parents(events=events, children=subevents)```
         [
             {**TH2-Event} # Parent
             ...
         ]



---

<a href="../../th2_data_services/utils/event_utils.py#L446"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_children_from_parent_id`

```python
get_children_from_parent_id(
    events: List[Dict],
    parent_id: str,
    max_events: int
) → Tuple[List[Dict], Dict]
```

Returns limited list of direct children events. 



**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 
 - <b>`parent_id`</b> (str):  Parent ID 
 - <b>`max_events`</b> (int):  Maximum number of events to extract 



**Returns:**
 
 - <b>`Tuple[List[Dict], Dict]`</b>:  Children Events, Parent Event 



**Example:**
 ``` get_children_from_parent_id(events=events,```
                                     parent_id="demo_parent_id",
                                     max_events=10)
         (
             [{**TH2-Event}, ...], # Child Events
             {**TH2-Event}         # Parent Event
         )



---

<a href="../../th2_data_services/utils/event_utils.py#L482"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_children_from_parents`

```python
get_children_from_parents(
    events: List[Dict],
    parents: List[Dict],
    max_events: int
) → Tuple[Dict[str, list], int]
```

Returns limited list of direct children events for each event in parents. 



**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 
 - <b>`parents`</b> (List[str]):  TH2-Events 
 - <b>`max_events`</b> (int):  Maximum number of events to extract from parent 



**Returns:**
 
 - <b>`Tuple`</b> (Dict[str, list], int):  Parent-Children, Events Count 



**Example:**
 ``` get_children_from_parents(events=events,```
                                   parents=parent_events,
                                   max_events=2)
         (
             {
                 "parentEvent_1": [{**TH2-ChildEvent1, **TH2-ChildEvent2}]
                 "parentEvent_2": [{**TH2-ChildEvent1, **TH2-ChildEvent2}],
                 ...
             },
             child_events_count
         )



---

<a href="../../th2_data_services/utils/event_utils.py#L520"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_children_from_parents_as_list`

```python
get_children_from_parents_as_list(
    events: List[Dict],
    parents: List[Dict],
    max_events: int
) → List[Dict]
```

Returns limited list of direct children events for each event in parents. 



**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 
 - <b>`parents`</b> (List[Dict]):  TH2-Events 
 - <b>`max_events`</b> (int):  Maximum number of events to extract 



**Returns:**
 
 - <b>`Dict[str, list]`</b>:  Children Events 



**Example:**
 ``` get_children_from_parents_as_list(events=events,```
                                           parents=parent_events,
                                           max_events=2)
         [
             {**TH2-Parent1_Child1}, {**TH2-Parent1_Child2},
             {**TH2-Parent2_Child2}, {**TH2-Parent2_Child2},
             ...
         ]



---

<a href="../../th2_data_services/utils/event_utils.py#L557"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `sublist`

```python
sublist(
    events: List[Dict],
    start_time: datetime,
    end_time: datetime
) → List[Dict]
```

Filter Events Based On Timeframe. 



**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 
 - <b>`start_time`</b> (datetime):  Start time 
 - <b>`end_time`</b> (datetime):  End time 



**Returns:**
 
 - <b>`List[Dict]`</b>:  Filtered Events. 



**Example:**
 ``` sublist(events=events,```
                 start_time=datetime.fromisoformat("2022-03-16T10:50:16"),
                 end_time=datetime.fromisoformat("2022-03-16T10:53:16"))
         [
             {**TH2-Event},
             ...
         ]



---

<a href="../../th2_data_services/utils/event_utils.py#L590"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/utils/event_utils.py#L643"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/utils/event_utils.py#L656"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_attached_messages_totals`

```python
print_attached_messages_totals(
    events: List[Dict],
    return_html: bool = False
) → Union[NoneType, str]
```

Prints Dictionary quantities of messages attached to events for each stream + direction. 



**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 
 - <b>`return_html`</b> (bool):  Return HTML Format 


---

<a href="../../th2_data_services/utils/event_utils.py#L669"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_category_totals`

```python
print_category_totals(
    events: List[Dict],
    categorizer: Callable,
    return_html: bool = False,
    ignore_status: bool = False
) → Union[NoneType, str]
```

Prints dictionary quantities of events for different categories. 



**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 
 - <b>`categorizer`</b> (Callable):  Categorizer Method 
 - <b>`return_html`</b> (bool):  Return HTML Format, defaults to False 
 - <b>`ignore_status`</b> (bool):  Get status of events, defaults to False 



**Returns:**
 Union[None, str] 


---

<a href="../../th2_data_services/utils/event_utils.py#L688"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_event`

```python
print_event(event: Dict) → None
```

Prints event in human-readable format. 



**Args:**
 
 - <b>`event`</b> (List[Dict]):  TH2-Events 


---

<a href="../../th2_data_services/utils/event_utils.py#L707"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_events_raw`

```python
print_events_raw(
    events: List[Dict],
    event_type: str,
    count: int,
    start: int = 0,
    failed: bool = False
) → None
```

Prints limited list of events of specific eventType in dictionary format. 



**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 
 - <b>`event_type`</b> (set):  Event Type To Extract 
 - <b>`count`</b> (int):  Maximum number of events to extract 
 - <b>`start`</b> (int, optional):  Start Iteration Index. Defaults to 0. 
 - <b>`failed`</b> (bool, optional):  Extract Only Failed Events. Defaults to False. 


---

<a href="../../th2_data_services/utils/event_utils.py#L724"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_some`

```python
print_some(
    events: List[Dict],
    event_type: str,
    count: int,
    start: int = 0,
    failed: bool = False
) → None
```

Prints limited list of events of specific eventType in human-readable format. 



**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 
 - <b>`event_type`</b> (set):  Event Type To Extract 
 - <b>`count`</b> (int):  Maximum number of events to extract 
 - <b>`start`</b> (int, optional):  Start Iteration Index. Defaults to 0. 
 - <b>`failed`</b> (bool, optional):  Extract Only Failed Events. Defaults to False. 


---

<a href="../../th2_data_services/utils/event_utils.py#L741"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_some_by_category`

```python
print_some_by_category(
    events: List[Dict],
    category: str,
    count: int,
    categorizer: Callable,
    start: int = 0,
    failed: bool = False
) → None
```

Print limited events by category. 



**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 
 - <b>`category`</b> (str):  Event category to extract 
 - <b>`count`</b> (int):  Maximum number of events to extract 
 - <b>`categorizer`</b> (Callable):  Categorizer function 
 - <b>`start`</b> (int, optional):  Start iteration index, defaults to 0. 
 - <b>`failed`</b> (bool, optional):  Extract only failed events, defaults to False. 


---

<a href="../../th2_data_services/utils/event_utils.py#L761"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_roots`

```python
print_roots(events: List[Dict], count: int, start: int = 0) → None
```

Prints limited list of root events (events without parents). 



**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 
 - <b>`count`</b> (int):  Maximum number of events to extract 
 - <b>`start`</b> (int, optional):  Start Iteration Index. Defaults to 0. 


---

<a href="../../th2_data_services/utils/event_utils.py#L776"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_children`

```python
print_children(
    events: List[Dict],
    parent_id: str,
    count: int,
    verbose: bool = True
)
```

Prints limited list of direct children events. 



**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 
 - <b>`parent_id`</b> (str):  Parent ID 
 - <b>`count`</b> (int):  Maximum number of events to extract 
 - <b>`verbose`</b> (bool):  Verbose output, defaults to True. 


---

<a href="../../th2_data_services/utils/event_utils.py#L793"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_type_totals`

```python
print_type_totals(
    events: List[Dict],
    return_html: bool = False
) → Union[NoneType, str]
```

Prints dictionary quantities of events for different event types. 



**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 
 - <b>`return_html`</b> (bool):  HTML format, defaults to False 



**Returns:**
 Union[None, str] 


---

<a href="../../th2_data_services/utils/event_utils.py#L808"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_type_frequencies`

```python
print_type_frequencies(
    events: List[Dict],
    event_types: List[str],
    aggregation_level: str = 'seconds',
    return_html=False
) → Union[NoneType, str]
```

Prints table of events per seconds or each second when there were events within events stream. 



**Args:**
 
 - <b>`events`</b>:  TH2-Events 
 - <b>`event_types`</b>:  List of event types to analyze 
 - <b>`aggregation_level`</b>:  Aggregation level 
 - <b>`return_html`</b>:  Return HTML format, defaults to False 


---

<a href="../../th2_data_services/utils/event_utils.py#L828"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_category_frequencies`

```python
print_category_frequencies(
    events: List[Dict],
    event_types: List[str],
    categorizer: Callable,
    aggregation_level: str = 'seconds',
    return_html: bool = False
) → Union[NoneType, str]
```

Prints table of events per seconds or each second when there were events within events stream. 



**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 
 - <b>`event_types`</b> (List[str]):  Event Types To Extract 
 - <b>`categorizer`</b> (Callable):  Categorizer function 
 - <b>`aggregation_level`</b> (str):  Aggregation Level 
 - <b>`return_html`</b>:  Return HTML Format 



**Returns:**
 Union[None, str] 


---

<a href="../../th2_data_services/utils/event_utils.py#L856"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_children_from_parents`

```python
print_children_from_parents(
    events: List[Dict],
    parents: List[Dict],
    max_events: int = 10000
) → None
```

Prints limited list of direct children events for each event in parents_list. 



**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 
 - <b>`parents`</b> (List[Dict]):  Parent TH2-Events 
 - <b>`max_events`</b> (int):  Maximum number of events to extract from each parent, default to 10'000 


---

<a href="../../th2_data_services/utils/event_utils.py#L876"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_children_stats_from_parents`

```python
print_children_stats_from_parents(
    events: List[Dict],
    parents: List[Dict],
    max_events: int = 10000,
    return_html: bool = False
) → Union[NoneType, str]
```

Prints statistics with number of children and their duration for each event in parents_list. 



**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 
 - <b>`parents`</b> (List[Dict]):  Parent TH2-Events 
 - <b>`max_events`</b> (int):  Maximum number of events to extract, default to 10'000 
 - <b>`return_html`</b> (bool):  Return HTML format, defaults to False 


---

<a href="../../th2_data_services/utils/event_utils.py#L924"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
