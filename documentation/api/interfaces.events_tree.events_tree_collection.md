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

Gets detached events as dict with a view {'parent_id': ['referenced event', ...]}. 



---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L192"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `append_event`

```python
append_event(event: dict) → None
```

Appends event into tree. 



**Args:**
 
 - <b>`event`</b>:  Event. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L498"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L430"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L470"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L446"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L289"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_all_events`

```python
get_all_events() → List[dict]
```

Gets all events from the trees. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L284"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_all_events_iter`

```python
get_all_events_iter() → Generator[dict, NoneType, NoneType]
```

Gets all events from the trees as iterator. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L411"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L316"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_children`

```python
get_children(id: str) → Tuple[dict]
```

Gets children for an event. 



**Args:**
 
 - <b>`id`</b>:  Event id. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the trees. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L332"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_children_iter`

```python
get_children_iter(id: str) → Generator[dict, NoneType, NoneType]
```

Gets children as iterator for an event. 



**Args:**
 
 - <b>`id`</b>:  Event id. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the trees. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L293"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_event`

```python
get_event(id: str) → Union[dict, NoneType]
```

Gets event by id. 



**Args:**
 
 - <b>`id`</b>:  Event id. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the trees. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L367"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_full_path`

```python
get_full_path(id: str, field: str = None) → List[Union[str, dict]]
```

Returns full path for an event in right order. 



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

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L309"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_leaves`

```python
get_leaves() → Tuple[dict]
```

Gets all trees leaves. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L351"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_parent`

```python
get_parent(id: str) → dict
```

Gets parent for an event. 



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

Gets parentless trees. 



**Returns:**
  Parentlees trees. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L229"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_root_by_id`

```python
get_root_by_id(id) → EventsTree
```

Gets root tree by id as EventsTree class. 



**Args:**
 
 - <b>`id`</b>:  Root id. 



**Returns:**
 Root tree. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the trees. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L221"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_roots_ids`

```python
get_roots_ids() → List[str]
```

Gets roots ids. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L518"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_subtree`

```python
get_subtree(id: str) → EventsTree
```

Gets subtree of event by id. 



**Args:**
 
 - <b>`id`</b>:  Event id. 



**Returns:**
 Subtree. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the trees. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L225"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_trees`

```python
get_trees() → List[EventsTree]
```

Gets trees as EventsTree class. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L537"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `recover_unknown_events`

```python
recover_unknown_events(data_source: IProviderDataSource) → None
```

Loads missed events and recover events. 



**Args:**
 
 - <b>`data_source`</b>:  Data Source. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree_collection.py#L246"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show`

```python
show()
```

Prints all EventsTree as tree view. 

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

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
