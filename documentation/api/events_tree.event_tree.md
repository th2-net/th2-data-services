<!-- markdownlint-disable -->

<a href="../../th2_data_services/events_tree/event_tree.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `events_tree.event_tree`






---

<a href="../../th2_data_services/events_tree/event_tree.py#L24"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `EventTree`
EventTree is a tree-based data structure of events. 


- get_x methods raise Exceptions if no result is found. 
- find_x methods return None if no result is found. 
- EventTree stores events as Nodes and interacts with them using an internal tree. 
- Note that EventTree stores only one tree.  If you want to store all trees, use EventTreeCollections. 
- EventTree contains all events in memory. 

Take a look at the following HTML tree to understand some important terms. 

```
<body> <!-- ancestor (grandparent), but not parent -->
     <div> <!-- parent & ancestor -->
         <p>Hello, world!</p> <!-- child -->
         <p>Goodbye!</p> <!-- sibling -->
     </div>
</body>
``` 

<a href="../../th2_data_services/events_tree/event_tree.py#L46"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(event_name: str, event_id: str, data: dict = None)
```

EventTree constructor. 



**Args:**
 
 - <b>`event_name`</b>:  Event Name. 
 - <b>`event_id`</b>:  Event Id. 
 - <b>`data`</b>:  Data of event. 




---

<a href="../../th2_data_services/events_tree/event_tree.py#L72"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `append_event`

```python
append_event(
    event_name: str,
    event_id: str,
    parent_id: str,
    data: dict = None
) → None
```

Appends the event to the tree. 



**Args:**
 
 - <b>`event_name`</b>:  Event Name. 
 - <b>`event_id`</b>:  Event Id. 
 - <b>`parent_id`</b>:  Parent Id. 
 - <b>`data`</b>:  Data of event. 

---

<a href="../../th2_data_services/events_tree/event_tree.py#L396"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `find`

```python
find(filter: Callable, stop: Callable = None) → Union[dict, NoneType]
```

Searches the first event match. 


- The search uses 'filter' which is a filtering function. 
- Optionally, the search uses 'stop' which is a stopping function. If 'stop' function returns 'True' then search is complete. 



**Args:**
 
 - <b>`filter`</b>:  Filter function. 
 - <b>`stop`</b>:  Stop function. If None searches for all nodes in the tree. 



**Returns:**
 One matching event. 

---

<a href="../../th2_data_services/events_tree/event_tree.py#L320"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/events_tree/event_tree.py#L370"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
 - <b>`stop`</b>:  Stop function. If None searches for all nodes in the tree. 
 - <b>`max_count`</b>:  Max count of matched events. Stops searching when `max_count` will be reached. 



**Returns:**
 Matching events. 

---

<a href="../../th2_data_services/events_tree/event_tree.py#L338"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
 - <b>`stop`</b>:  Stop function. If None searches for all nodes in the tree. 
 - <b>`max_count`</b>:  Max count of matched events. Stops searching when `max_count` will be reached. 



**Yields:**
 Matching events. 

---

<a href="../../th2_data_services/events_tree/event_tree.py#L98"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_all_events`

```python
get_all_events() → List[dict]
```

Returns all events from the tree. 

---

<a href="../../th2_data_services/events_tree/event_tree.py#L93"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_all_events_iter`

```python
get_all_events_iter() → Generator[dict, NoneType, NoneType]
```

Returns all events from the tree as iterator. 

---

<a href="../../th2_data_services/events_tree/event_tree.py#L281"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the tree. 

---

<a href="../../th2_data_services/events_tree/event_tree.py#L186"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_children`

```python
get_children(id: str) → Tuple[dict]
```

Returns children for the event by its id. 



**Args:**
 
 - <b>`id`</b>:  Event id. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the tree. 

---

<a href="../../th2_data_services/events_tree/event_tree.py#L200"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_children_iter`

```python
get_children_iter(id: str) → Generator[dict, NoneType, NoneType]
```

Returns children as iterator for the event by its id. 



**Args:**
 
 - <b>`id`</b>:  Event id. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the tree. 

---

<a href="../../th2_data_services/events_tree/event_tree.py#L102"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_event`

```python
get_event(id: str) → dict
```

Returns an event by id. 



**Args:**
 
 - <b>`id`</b>:  Event id. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the tree. 

---

<a href="../../th2_data_services/events_tree/event_tree.py#L234"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_full_path`

```python
get_full_path(id: str, field: str = None) → List[Union[str, dict]]
```

Returns the full path for the event by its id in right order. 



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
tree.get_full_path('Jane', id)
['Harry-event-id', 'Jane-event-id']

tree.get_full_path('Jane', name)
['Harry-event-name', 'Jane-event-name']

tree.get_full_path('Jane')
['Harry-event', 'Jane-event']
``` 



**Args:**
 
 - <b>`id`</b>:  Event id. 
 - <b>`field`</b>:  Field of event. 



**Returns:**
 Full path of event. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the tree. 

---

<a href="../../th2_data_services/events_tree/event_tree.py#L176"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_leaves`

```python
get_leaves() → Tuple[dict]
```

Returns all tree leaves. 

---

<a href="../../th2_data_services/events_tree/event_tree.py#L181"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_leaves_iter`

```python
get_leaves_iter() → Generator[dict, NoneType, NoneType]
```

Returns all tree leaves as iterator. 

---

<a href="../../th2_data_services/events_tree/event_tree.py#L215"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_parent`

```python
get_parent(id: str) → dict
```

Returns a parent for the event by its id. 



**Args:**
 
 - <b>`id`</b>:  Event id. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the tree. 

---

<a href="../../th2_data_services/events_tree/event_tree.py#L172"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_root`

```python
get_root() → dict
```

Returns the root event. 

---

<a href="../../th2_data_services/events_tree/event_tree.py#L164"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_root_id`

```python
get_root_id() → str
```

Returns the root id. 

---

<a href="../../th2_data_services/events_tree/event_tree.py#L168"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_root_name`

```python
get_root_name() → str
```

Returns the root name. 

---

<a href="../../th2_data_services/events_tree/event_tree.py#L418"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_subtree`

```python
get_subtree(id: str) → EventTree
```

Returns subtree of the event by its id. 



**Args:**
 
 - <b>`id`</b>:  Event id. 



**Returns:**
 Subtree. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the tree. 

---

<a href="../../th2_data_services/events_tree/event_tree.py#L439"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `merge_tree`

```python
merge_tree(
    parent_id: str,
    other_tree: 'EventTree',
    use_deepcopy: bool = False
) → None
```

Merges a EventTree to specified identifier. 



**Args:**
 
 - <b>`parent_id`</b>:  Event id to which merge. 
 - <b>`other_tree`</b>:  EventTree. 
 - <b>`use_deepcopy`</b>:  True if you need deepcopy for your objects in event. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the tree. 

---

<a href="../../th2_data_services/events_tree/event_tree.py#L454"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show`

```python
show() → None
```

Prints the EventTree as tree view. 

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

<a href="../../th2_data_services/events_tree/event_tree.py#L495"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `summary`

```python
summary() → str
```

Returns the tree summary. 

---

<a href="../../th2_data_services/events_tree/event_tree.py#L131"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `update_event_name`

```python
update_event_name(event_id: str, event_name: str) → None
```

Updates Event name in the tree. Note that it doesn't change internal data. 



**Args:**
 
 - <b>`event_id`</b>:  Event id. 
 - <b>`event_name`</b>:  Event name. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the tree. 

---

<a href="../../th2_data_services/events_tree/event_tree.py#L146"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `update_parent_link`

```python
update_parent_link(event_id: str, parent_id: str) → None
```

Updates the link to parent. 



**Args:**
 
 - <b>`event_id`</b>:  Event id. 
 - <b>`parent_id`</b>:  New parent id. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id is not in the tree. 
 - <b>`TreeLoop`</b>:  If parent id will point to the descendant event. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
