<!-- markdownlint-disable -->

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `th2.data_services.event_tree.common_event_tree_collection`






---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L30"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CommonEventTreeCollection`
EventTreeCollection objective is building 'EventsTree's and storing them. 


- EventTreeCollection stores all EventsTree. You can to refer to each of them. 
- Recovery of missing events occurs when you have passed DataSource class to constructor. Otherwise, you should execute the method 'recover_unknown_events' manually. Note that there is no point in the method if the list of detached events is empty. 

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(driver: IETCDriver)
```

EventTreeCollection constructor. 



**Args:**
 
 - <b>`driver`</b>:  initialized driver object. 


---

#### <kbd>property</kbd> len_detached_events

Returns number of detached events in the collection. 

---

#### <kbd>property</kbd> len_parentless

Returns number of events in the parentless trees inside the collection. 

---

#### <kbd>property</kbd> len_trees

Returns number of events in the trees inside the collection, including parentless trees. 



---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L153"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `append_event`

```python
append_event(event: dict) → None
```

Appends event into a tree. 



**Args:**
 
 - <b>`event`</b>:  Event. 

---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L135"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `build`

```python
build(data: Iterable)
```





---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L641"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `find`

```python
find(filter: Callable, stop: Callable = None) → Union[~Event, NoneType]
```

Searches the first event match. 


- The search uses 'filter' which is a filtering function. 
- Optionally, the search uses 'stop' which is a stopping function. If 'stop' function returns 'True' then search is complete. 

This method applicable only for trees (regular or parentless), not for detached events. 



**Args:**
 
 - <b>`filter`</b>:  Filter function. 
 - <b>`stop`</b>:  Stop function. If None searches for all nodes in the trees. 



**Returns:**
 One matching event. 

---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L550"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `find_ancestor`

```python
find_ancestor(id: str, filter: Callable) → Union[~Event, NoneType]
```

Finds the ancestor of an event. 

This method applicable only for trees (regular or parentless), not for detached events. 



**Args:**
 
 - <b>`id`</b>:  Event id. 
 - <b>`filter`</b>:  Filter function 



**Returns:**
 Ancestor of Event. 

---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L616"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `findall`

```python
findall(
    filter: Callable,
    stop: Callable = None,
    max_count: int = None
) → List[~Event]
```

Searches events matches. 


- The search uses 'filter' which is a filtering function. 
- Optionally, the search uses 'stop' which is a stopping function. If 'stop' function returns 'True' then search is complete. 
- 'max_count' is a parameter that limits the search to a specified count. 

This method applicable only for trees (regular or parentless), not for detached events. 



**Args:**
 
 - <b>`filter`</b>:  Filter function. 
 - <b>`stop`</b>:  Stop function. If None searches for all nodes in the trees. 
 - <b>`max_count`</b>:  Max count of matched events. Stops searching when `max_count` will be reached. 



**Returns:**
 Matching events. 

---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L573"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `findall_iter`

```python
findall_iter(
    filter: Callable,
    stop: Callable = None,
    max_count: int = None
) → Generator[~Event, NoneType, NoneType]
```

Searches events matches as iterator. 


- The search uses 'filter' which is a filtering function. 
- Optionally, the search uses 'stop' which is a stopping function. If 'stop' function returns 'True' then search is complete. 
- 'max_count' is a parameter that limits the search to a specified count. 

This method applicable only for trees (regular or parentless), not for detached events. 



**Args:**
 
 - <b>`filter`</b>:  Filter function. 
 - <b>`stop`</b>:  Stop function. If None searches for all nodes in the trees. 
 - <b>`max_count`</b>:  Max count of matched events. Stops searching when `max_count` will be reached. 



**Yields:**
 Matching events. 

---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L346"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_all_events`

```python
get_all_events() → List[~Event]
```

Returns all events from the collection. 

---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L336"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_all_events_iter`

```python
get_all_events_iter() → Generator[~Event, NoneType, NoneType]
```

Yields all events from the collection. 

---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L523"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_ancestors`

```python
get_ancestors(id: str) → List[~Event]
```

Returns all event's ancestors in right order. 

This method applicable only for trees (regular or parentless), not for detached events. 



**Args:**
 
 - <b>`id`</b>:  Event id. 



**Returns:**
 All event's ancestors. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the trees. 

---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L388"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_children`

```python
get_children(id: str) → Tuple[~Event]
```

Returns children of the event by its id. 

This method applicable only for trees (regular or parentless), not for detached events. 



**Args:**
 
 - <b>`id`</b>:  Event id. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the trees. 

---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L412"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_children_iter`

```python
get_children_iter(id: str) → Generator[~Event, NoneType, NoneType]
```

Yields children of the event by its id. 

This method applicable only for trees (regular or parentless), not for detached events. 



**Args:**
 
 - <b>`id`</b>:  Event id. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the trees. 

---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L193"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_detached_events`

```python
get_detached_events() → List[~Event]
```

Returns detached events list. 

---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L187"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_detached_events_iter`

```python
get_detached_events_iter() → Generator[~Event, NoneType, NoneType]
```

Yields detached events. 

---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L350"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_event`

```python
get_event(id: str) → Union[~Event, NoneType]
```

Returns an event by its id. 



**Args:**
 
 - <b>`id`</b>:  Event id. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the collection. 

---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L471"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_full_path`

```python
get_full_path(id: str, field: str = None) → List[Union[str, ~Event]]
```

Returns the full path for the event by its id in the right order. 

This method applicable only for trees (regular or parentless), not for detached events. 



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

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L376"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_leaves`

```python
get_leaves() → Tuple[~Event]
```

Returns all trees leaves, including parentless trees. 

---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L380"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_leaves_iter`

```python
get_leaves_iter() → Generator[~Event, NoneType, NoneType]
```

Yields all trees leaves, including parentless trees. 

---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L440"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_parent`

```python
get_parent(id: str) → ~Event
```

Returns a parent of the event by its id. 



**Args:**
 
 - <b>`id`</b>:  Event id. 



**Raises:**
 
 - <b>`NodeIDAbsentError`</b>:  If event id is not in the trees. 

---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L724"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_parentless_tree_collection`

```python
get_parentless_tree_collection() → CommonEventTreeCollection
```

Builds and returns parentless trees by detached events as EventTreeCollection. 

Detached events will be removed from the collection. 



**Returns:**
  EventTreeCollection. 

---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L139"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_parentless_trees`

```python
get_parentless_trees() → List[~EventTreeType]
```

Builds and returns parentless trees by detached events. 

Detached events will be removed from the tree. 



**Returns:**
  List of parentless trees if they exist, otherwise empty list. 

---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L215"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_root_by_id`

```python
get_root_by_id(id) → ~Event
```

Returns the root event of a tree by id of any event in this tree. 

If event id of parentless tree is passed, stub of this parentless tree will be returnd. 



**Args:**
 
 - <b>`id`</b>:  Event id. 



**Returns:**
 Th2Event. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the trees. 

---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L197"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_roots_ids`

```python
get_roots_ids() → List[str]
```

Returns ids of all trees roots located in the collection. 

If there are parentless trees, they also will be return. 

---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L668"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_subtree`

```python
get_subtree(id: str) → ~EventTreeType
```

Returns subtree of the event by its id. 

This method applicable only for trees (regular or parentless), not for detached events. 



**Args:**
 
 - <b>`id`</b>:  Event id. 



**Returns:**
 Subtree. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the trees. 

---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L234"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_tree_by_id`

```python
get_tree_by_id(id) → ~EventTreeType
```

Returns a tree by id of any event in this tree. 

If event id of parentless tree is passed, stub of this parentless tree will be returnd. 



**Args:**
 
 - <b>`id`</b>:  Event id. 



**Returns:**
 Tree. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the trees. 

---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L206"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_trees`

```python
get_trees() → List[~EventTreeType]
```

Returns the list of trees inside the collection. 

If there are parentless trees, they also will be return. 

---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L695"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `recover_unknown_events`

```python
recover_unknown_events(preprocessor=None) → None
```

Loads missed events and finish tree building. 



**Args:**
 
 - <b>`preprocessor`</b>:  the function that will be executed for each recovered event before store. 

---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L52"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `setup_et_class`

```python
setup_et_class() → Type[CommonEventTree]
```





---

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L257"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2/data_services/event_tree/common_event_tree_collection.py#L310"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `summary`

```python
summary() → str
```

Returns the collection summary. 

The same as repr(EventTreeCollection). 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
