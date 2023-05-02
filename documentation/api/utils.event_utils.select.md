<!-- markdownlint-disable -->

<a href="../../th2_data_services/utils/event_utils/select.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.event_utils.select`





---

<a href="../../th2_data_services/utils/event_utils/select.py#L11"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/utils/event_utils/select.py#L45"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/utils/event_utils/select.py#L83"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/utils/event_utils/select.py#L108"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/utils/event_utils/select.py#L129"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/utils/event_utils/select.py#L164"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/utils/event_utils/select.py#L201"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/utils/event_utils/select.py#L237"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/utils/event_utils/select.py#L271"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/utils/event_utils/select.py#L297"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/utils/event_utils/select.py#L333"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
