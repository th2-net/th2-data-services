<!-- markdownlint-disable -->

<a href="../../th2_data_services/interfaces/events_tree/events_tree.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `interfaces.events_tree.events_tree`






---

<a href="../../th2_data_services/interfaces/events_tree/events_tree.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `EventsTree`
EventsTree - is a useful wrapper for your retrieved data. 


- get_x methods raise Exceptions if no result is found. 
- find_x methods return None if no result is found. 
- EventsTree stores events as Nodes and interacts with them using an internal tree. 
- EventsTree removes the 'body' field by default to save memory, but you can keep it. 
- Note that EventsTree stores only one tree.  If you want to store all trees, use EventsTreeCollections. 
- EventsTree contains all events in memory. 

Take a look at the following HTML tree to understand some important terms. 

```
<body> <!-- ancestor (grandparent), but not parent -->
     <div> <!-- parent & ancestor -->
         <p>Hello, world!</p> <!-- child -->
         <p>Goodbye!</p> <!-- sibling -->
     </div>
</body>
``` 

<a href="../../th2_data_services/interfaces/events_tree/events_tree.py#L48"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(tree: Tree)
```

EventsTree constructor. 



**Args:**
 
 - <b>`tree`</b> (treelib.Tree):  Tree. 




---

<a href="../../th2_data_services/interfaces/events_tree/events_tree.py#L56"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `append_node`

```python
append_node(node: Node, parent_id: str) → None
```

Appends a node to the tree. 



**Args:**
 
 - <b>`node`</b>:  Node. 
 - <b>`parent_id`</b>:  Parent event id. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree.py#L302"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/interfaces/events_tree/events_tree.py#L229"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/interfaces/events_tree/events_tree.py#L276"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/interfaces/events_tree/events_tree.py#L244"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../th2_data_services/interfaces/events_tree/events_tree.py#L73"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_all_events`

```python
get_all_events() → List[dict]
```

Gets all events from the tree. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree.py#L68"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_all_events_iter`

```python
get_all_events_iter() → Generator[dict, NoneType, NoneType]
```

Gets all events from the tree as iterator. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree.py#L190"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
 
 - <b>`EventIdNotInTree`</b>:  If event id not in the tree. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree.py#L107"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_children`

```python
get_children(id: str) → Tuple[dict]
```

Gets children for an event. 



**Args:**
 
 - <b>`id`</b>:  Event id. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id not in the tree. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree.py#L121"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_children_iter`

```python
get_children_iter(id: str) → Generator[dict, NoneType, NoneType]
```

Gets children as iterator for an event. 



**Args:**
 
 - <b>`id`</b>:  Event id. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id not in the tree. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree.py#L77"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_event`

```python
get_event(id: str) → dict
```

Gets event by id. 



**Args:**
 
 - <b>`id`</b>:  Event id. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id not in the tree. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree.py#L150"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_full_path`

```python
get_full_path(id: str, field: str = None) → List[Union[str, dict]]
```

Returns full path for an event in right order. 

Harry ├── Bill └── Jane  ├── Diane  │   └── Mary  └── Mark 



**Examples:**
  tree.get_full_path('Jane', id)  ['Harry-event-id', 'Jane-event-id'] 

 tree.get_full_path('Jane', name)  ['Harry-event-name', 'Jane-event-name'] 

 tree.get_full_path('Jane', event)  ['Harry-event', 'Jane-event'] 



**Args:**
 
 - <b>`id`</b>:  Event id. 
 - <b>`field`</b>:  Field of event. 



**Returns:**
 Full path of event. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id not in the tree. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree.py#L103"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_leaves`

```python
get_leaves() → Tuple[dict]
```

Gets all tree leaves. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree.py#L136"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_parent`

```python
get_parent(id: str) → dict
```

Gets parent for an event. 



**Args:**
 
 - <b>`id`</b>:  Event id. 



**Raises:**
 
 - <b>`EventIdNotInTree`</b>:  If event id not in the tree. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree.py#L99"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_root`

```python
get_root() → dict
```

Gets root event. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree.py#L95"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_root_id`

```python
get_root_id() → str
```

Gets root id. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree.py#L324"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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
 
 - <b>`EventIdNotInTree`</b>:  If event id not in the tree. 

---

<a href="../../th2_data_services/interfaces/events_tree/events_tree.py#L341"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show`

```python
show() → None
```

Prints EventsTree as tree view. 

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
