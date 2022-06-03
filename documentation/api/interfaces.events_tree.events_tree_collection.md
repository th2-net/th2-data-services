<!-- markdownlint-disable -->

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `interfaces.events_tree.events_tree_collection`






---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L29"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `EventsTreeCollection`
EventsTreeCollection objective is building 'EventsTree's and storing them. 


- EventsTreeCollection stores all EventsTree. You can to refer to each of them. 
- Recovery of missing events occurs when you have passed DataSource class. Otherwise you should execute the method 'recover_unknown_events'. Note that there is no point in the method if the list of detached events is empty. 

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L38"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    data: Data,
    data_source: IProviderDataSource = None,
    preserve_body: bool = False,
    stub: bool = False
)
```

EventsTreeCollection constructor. 



**Args:**
 
 - <b>`data`</b>:  Data object. 
 - <b>`data_source`</b>:  Data Source object. 
 - <b>`preserve_body`</b>:  If True it will preserve 'body' field in the Events. 
 - <b>`stub`</b>:  If True it will create stub when event is broken. 


---

#### <kbd>property</kbd> detached_events

Returns detached events as a dict with a view {'parent_id': ['referenced event', ...]}. 

---

#### <kbd>property</kbd> len_detached_events

Returns number of detached events in the collection. 

---

#### <kbd>property</kbd> len_trees

Returns number of events in the trees inside the collection. 



---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L202"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `append_event`

```python
append_event(event: dict) → None
```

Appends event into tree. 



**Args:**
 
 - <b>`event`</b>:  Event. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L551"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `find`

```python
find(filter: Callable, stop: Callable = None) → Union[dict, NoneType]
```

Searches the first event match. 


- The search uses 'filter' which is a filtering function. 
- Optionally, the search uses 'stop' which is a stopping function. If 'stop' function returns 'True' then search is complete. 



**Args:**
 
 - <b>`filter`</b>:  Filter function. 
 - <b>`stop`</b>:  Stop function. If None searches for all nodes in the trees. 



**Returns:**
 One matching event. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L483"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `find_ancestor`

```python
find_ancestor(id: str, filter: Callable) → Union[dict, NoneType]
```

Finds the ancestor of an event. 



**Args:**
 
 - <b>`id`</b>:  Event id. 
 - <b>`filter`</b>:  Filter function 



**Returns:**
 Ancestor of Event. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L523"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `findall`

```python
findall(
    filter: Callable,
    stop: Callable = None,
    max_count: int = None
) → List[dict]
```

Searches events matches. 


- The search uses 'filter' which is a filtering function. 
- Optionally, the search uses 'stop' which is a stopping function. If 'stop' function returns 'True' then search is complete. 
- 'max_count' is a parameter that limits the search to a specified count. 



**Args:**
 
 - <b>`filter`</b>:  Filter function. 
 - <b>`stop`</b>:  Stop function. If None searches for all nodes in the trees. 
 - <b>`max_count`</b>:  Max count of matched events. Stops searching when `max_count` will be reached. 



**Returns:**
 Matching events. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L499"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `findall_iter`

```python
findall_iter(
    filter: Callable,
    stop: Callable = None,
    max_count: int = None
) → Generator[dict, NoneType, NoneType]
```

Searches events matches as iterator. 


- The search uses 'filter' which is a filtering function. 
- Optionally, the search uses 'stop' which is a stopping function. If 'stop' function returns 'True' then search is complete. 
- 'max_count' is a parameter that limits the search to a specified count. 



**Args:**
 
 - <b>`filter`</b>:  Filter function. 
 - <b>`stop`</b>:  Stop function. If None searches for all nodes in the trees. 
 - <b>`max_count`</b>:  Max count of matched events. Stops searching when `max_count` will be reached. 



**Yields:**
 Matching events. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L340"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_all_events`

```python
get_all_events() → List[dict]
```

Returns all events from the trees. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L335"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_all_events_iter`

```python
get_all_events_iter() → Generator[dict, NoneType, NoneType]
```

Returns all events from the trees as iterator. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L464"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_ancestors`

```python
get_ancestors(id: str) → List[dict]
```

Returns all event's ancestors in right order. 



**Args:**
 
 - <b>`id`</b>:  Event id. 



**Returns:**
 All event's ancestors. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the trees. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L369"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_children`

```python
get_children(id: str) → Tuple[dict]
```

Returns children for the event by its id. 



**Args:**
 
 - <b>`id`</b>:  Event id. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the trees. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L385"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_children_iter`

```python
get_children_iter(id: str) → Generator[dict, NoneType, NoneType]
```

Returns children as iterator for the event by its id. 



**Args:**
 
 - <b>`id`</b>:  Event id. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the trees. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L344"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_event`

```python
get_event(id: str) → Union[dict, NoneType]
```

Returns an event by id. 



**Args:**
 
 - <b>`id`</b>:  Event id. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the trees. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L420"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_full_path`

```python
get_full_path(id: str, field: str = None) → List[Union[str, dict]]
```

Returns the full path for the event by its id in the right order. 



**Examples:**
 

Imagine we have the following tree. 

```
Harry
├── Bill
└── Jane
     ├── Diane
     │   └── Mary
     └── Mark
``` 

```
collection.get_full_path('Jane', id)
['Harry-event-id', 'Jane-event-id']

collection.get_full_path('Jane', name)
['Harry-event-name', 'Jane-event-name']

collection.get_full_path('Jane')
['Harry-event', 'Jane-event']
``` 



**Args:**
 
 - <b>`id`</b>:  Event id. 
 - <b>`field`</b>:  Field of event. 



**Returns:**
 Full path of event. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the trees. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L360"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_leaves`

```python
get_leaves() → Tuple[dict]
```

Returns all trees leaves. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L364"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_leaves_iter`

```python
get_leaves_iter() → Generator[dict, NoneType, NoneType]
```

Returns all trees leaves as iterator. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L404"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_parent`

```python
get_parent(id: str) → dict
```

Returns a parent for the event by its id. 



**Args:**
 
 - <b>`id`</b>:  Event id. 



**Raises:**
 
 - <b>`NodeIDAbsentError`</b>:  If event id is not in the trees. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L62"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_parentless_trees`

```python
get_parentless_trees() → List[EventsTree]
```

Builds and returns parentless trees by detached events. 

Detached events will be removed from the tree. 



**Returns:**
  List of parentless trees if they exist, otherwise empty list. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L239"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_root_by_id`

```python
get_root_by_id(id) → EventsTree
```

Returns a root tree by id as EventsTree class. 



**Args:**
 
 - <b>`id`</b>:  Root id. 



**Returns:**
 Root tree. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the trees. 



**Notes:**

> 1. At the moment the method returns a tree by id and duplicates the get_tree_by_id method. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L231"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_roots_ids`

```python
get_roots_ids() → List[str]
```

Returns roots ids. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L571"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_subtree`

```python
get_subtree(id: str) → EventsTree
```

Returns subtree of the event by its id. 



**Args:**
 
 - <b>`id`</b>:  Event id. 



**Returns:**
 Subtree. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the trees. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L259"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_tree_by_id`

```python
get_tree_by_id(id)
```

Returns a tree by id as EventsTree class. 



**Args:**
 
 - <b>`id`</b>:  Root id. 



**Returns:**
 Tree. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the trees. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L235"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_trees`

```python
get_trees() → List[EventsTree]
```

Returns the list of trees inside the collection. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L590"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `recover_unknown_events`

```python
recover_unknown_events(data_source: IProviderDataSource) → None
```

Loads missed events and recover events. 



**Args:**
 
 - <b>`data_source`</b>:  Data Source. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L276"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show`

```python
show()
```

Prints all EventsTrees as tree view. 

For example: 

```
Root
     |___ C01
     |    |___ C11
     |         |___ C111
     |         |___ C112
     |___ C02
     |___ C03
     |    |___ C31
``` 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L321"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `summary`

```python
summary() → str
```

Returns the collection summary. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
