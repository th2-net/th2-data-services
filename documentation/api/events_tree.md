<!-- markdownlint-disable -->

<a href="../../th2_data_services/events_tree.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `events_tree`






---

<a href="../../th2_data_services/events_tree.py#L9"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `EventsTree`
EventsTree - is a useful wrapper for your retrieved data. 

EventsTree - is not a tree in the literal sense. It is an object with a dict 'events' inside which contains events without their body. 

EventTree contains all events inside, so it takes ~2.5Gb for 1 million events. 

Take a look at the following HTML tree to understand some important terms. 

 <body> <!-- ancestor (grandparent), but not parent -->  <div> <!-- parent & ancestor -->  <p>Hello, world!</p> <!-- child -->  <p>Goodbye!</p> <!-- sibling -->  </div>  </body> 

<a href="../../th2_data_services/events_tree.py#L30"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(data: Optional[Iterator, Generator[dict, NoneType], Data] = None)
```






---

#### <kbd>property</kbd> events





---

#### <kbd>property</kbd> unknown_events







---

<a href="../../th2_data_services/events_tree.py#L64"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `append_element`

```python
append_element(event: dict) → None
```

Append new event to events tree. 

Will update the event if event_id matches. Will remove the event from unknown_events if it in unknown_events dict. 



**Args:**
 
 - <b>`event`</b>:  Event 

---

<a href="../../th2_data_services/events_tree.py#L54"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `build_tree`

```python
build_tree(data: Optional[Iterator, Generator[dict, NoneType]]) → None
```

Build or append new events to family tree. 

:param data: Events. 

---

<a href="../../th2_data_services/events_tree.py#L46"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `clear_events`

```python
clear_events() → None
```

Clear exist events. 

---

<a href="../../th2_data_services/events_tree.py#L50"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `clear_unknown_events`

```python
clear_unknown_events() → None
```

Clear unknown events. 

---

<a href="../../th2_data_services/events_tree.py#L147"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_ancestor_by_name`

```python
get_ancestor_by_name(event: dict, event_name: str) → Union[dict, NoneType]
```

Gets event ancestor by event_name. 

:param event: Record. :param event_name: Event name. :return: Event. 

---

<a href="../../th2_data_services/events_tree.py#L166"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_ancestor_by_super_type`

```python
get_ancestor_by_super_type(
    event: dict,
    super_type: str,
    super_type_get_func: Callable[[dict, Dict[int, dict]], str]
) → Union[dict, NoneType]
```

Gets event ancestor by super_type. 

:param event: Event. :param super_type: Super type. :param super_type_get_func: Super type get function. :return: Event. 

---

<a href="../../th2_data_services/events_tree.py#L212"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_children`

```python
get_children(parent_event_id) → list
```





---

<a href="../../th2_data_services/events_tree.py#L109"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_in_ancestor_name`

```python
is_in_ancestor_name(event: dict, event_name: str)
```

Verify event has ancestor with specified event name. 

:param event: Event parent id. :param event_name: Event name. :return: True/False. 

---

<a href="../../th2_data_services/events_tree.py#L128"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_in_ancestor_type`

```python
is_in_ancestor_type(event: dict, event_type: str) → bool
```

Verify event has ancestor with specified event type. 

:param event: Event. :param event_type: Event type. :return: True/False. 

---

<a href="../../th2_data_services/events_tree.py#L197"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `recover_unknown_events`

```python
recover_unknown_events(data_source: DataSource) → None
```

Loads unknown events from data provider and recover EventsTree. 

:param data_source: DataSources. 

---

<a href="../../th2_data_services/events_tree.py#L88"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `search_unknown_parents`

```python
search_unknown_parents() → dict
```

Searches unknown events. 



**Returns:**
 
 - <b>`dict`</b>:  Unknown events. 


---

<a href="../../th2_data_services/events_tree.py#L216"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `TreeNode`





---

#### <kbd>property</kbd> ancestors

All parent nodes and their parent nodes. 

``` from anytree import Node```
``` udo = Node("Udo")``` ``` marc = Node("Marc", parent=udo)```
``` lian = Node("Lian", parent=marc)``` ``` udo.ancestors```
()
``` marc.ancestors``` (Node('/Udo'),) ``` lian.ancestors```
(Node('/Udo'), Node('/Udo/Marc'))


---

#### <kbd>property</kbd> anchestors

All parent nodes and their parent nodes - see :any:`ancestors`. 

The attribute `anchestors` is just a typo of `ancestors`. Please use `ancestors`. This attribute will be removed in the 3.0.0 release. 

---

#### <kbd>property</kbd> children

All child nodes. 

``` from anytree import Node```
``` n = Node("n")``` ``` a = Node("a", parent=n)```
``` b = Node("b", parent=n)``` ``` c = Node("c", parent=n)```
``` n.children``` (Node('/n/a'), Node('/n/b'), Node('/n/c')) 

Modifying the children attribute modifies the tree. 

**Detach** 

The children attribute can be updated by setting to an iterable. 

``` n.children = [a, b]```
``` n.children``` (Node('/n/a'), Node('/n/b')) 

Node `c` is removed from the tree. In case of an existing reference, the node `c` does not vanish and is the root of its own tree. 

``` c```
Node('/c')

**Attach**

``` d = Node("d")``` ``` d```
Node('/d')
``` n.children = [a, b, d]``` ``` n.children```
(Node('/n/a'), Node('/n/b'), Node('/n/d'))
``` d``` Node('/n/d') 

**Duplicate** 

A node can just be the children once. Duplicates cause a :any:`TreeError`: 

``` n.children = [a, b, d, a]```
Traceback (most recent call last):
     ...
anytree.node.exceptions.TreeError: Cannot add node Node('/n/a') multiple times as child.


---

#### <kbd>property</kbd> depth

Number of edges to the root `Node`. 

``` from anytree import Node```
``` udo = Node("Udo")``` ``` marc = Node("Marc", parent=udo)```
``` lian = Node("Lian", parent=marc)``` ``` udo.depth```
0
``` marc.depth``` 1 ``` lian.depth```
2


---

#### <kbd>property</kbd> descendants

All child nodes and all their child nodes. 

``` from anytree import Node```
``` udo = Node("Udo")``` ``` marc = Node("Marc", parent=udo)```
``` lian = Node("Lian", parent=marc)``` ``` loui = Node("Loui", parent=marc)```
``` soe = Node("Soe", parent=lian)``` ``` udo.descendants```
(Node('/Udo/Marc'), Node('/Udo/Marc/Lian'), Node('/Udo/Marc/Lian/Soe'), Node('/Udo/Marc/Loui'))
``` marc.descendants``` (Node('/Udo/Marc/Lian'), Node('/Udo/Marc/Lian/Soe'), Node('/Udo/Marc/Loui')) ``` lian.descendants```
(Node('/Udo/Marc/Lian/Soe'),)


---

#### <kbd>property</kbd> height

Number of edges on the longest path to a leaf `Node`. 

``` from anytree import Node```
``` udo = Node("Udo")``` ``` marc = Node("Marc", parent=udo)```
``` lian = Node("Lian", parent=marc)``` ``` udo.height```
2
``` marc.height``` 1 ``` lian.height```
0


---

#### <kbd>property</kbd> is_leaf

`Node` has no children (External Node). 

``` from anytree import Node```
``` udo = Node("Udo")``` ``` marc = Node("Marc", parent=udo)```
``` lian = Node("Lian", parent=marc)``` ``` udo.is_leaf```
False
``` marc.is_leaf``` False ``` lian.is_leaf```
True


---

#### <kbd>property</kbd> is_root

`Node` is tree root. 

``` from anytree import Node```
``` udo = Node("Udo")``` ``` marc = Node("Marc", parent=udo)```
``` lian = Node("Lian", parent=marc)``` ``` udo.is_root```
True
``` marc.is_root``` False ``` lian.is_root```
False


---

#### <kbd>property</kbd> leaves

Tuple of all leaf nodes. 

``` from anytree import Node```
``` udo = Node("Udo")``` ``` marc = Node("Marc", parent=udo)```
``` lian = Node("Lian", parent=marc)``` ``` loui = Node("Loui", parent=marc)```
``` lazy = Node("Lazy", parent=marc)``` ``` udo.leaves```
(Node('/Udo/Marc/Lian'), Node('/Udo/Marc/Loui'), Node('/Udo/Marc/Lazy'))
``` marc.leaves``` (Node('/Udo/Marc/Lian'), Node('/Udo/Marc/Loui'), Node('/Udo/Marc/Lazy')) 

---

#### <kbd>property</kbd> parent

Parent Node. 

On set, the node is detached from any previous parent node and attached to the new node. 

``` from anytree import Node, RenderTree```
``` udo = Node("Udo")``` ``` marc = Node("Marc")```
``` lian = Node("Lian", parent=marc)``` ``` print(RenderTree(udo))```
Node('/Udo')
``` print(RenderTree(marc))``` Node('/Marc') └── Node('/Marc/Lian') 

**Attach** 

``` marc.parent = udo```
``` print(RenderTree(udo))``` Node('/Udo') └── Node('/Udo/Marc')  └── Node('/Udo/Marc/Lian') 

**Detach** 

To make a node to a root node, just set this attribute to `None`. 

``` marc.is_root```
False
``` marc.parent = None``` ``` marc.is_root```
True


---

#### <kbd>property</kbd> path

Path of this `Node`. 

``` from anytree import Node```
``` udo = Node("Udo")``` ``` marc = Node("Marc", parent=udo)```
``` lian = Node("Lian", parent=marc)``` ``` udo.path```
(Node('/Udo'),)
``` marc.path``` (Node('/Udo'), Node('/Udo/Marc')) ``` lian.path```
(Node('/Udo'), Node('/Udo/Marc'), Node('/Udo/Marc/Lian'))


---

#### <kbd>property</kbd> root

Tree Root Node. 

``` from anytree import Node```
``` udo = Node("Udo")``` ``` marc = Node("Marc", parent=udo)```
``` lian = Node("Lian", parent=marc)``` ``` udo.root```
Node('/Udo')
``` marc.root``` Node('/Udo') ``` lian.root```
Node('/Udo')


---

#### <kbd>property</kbd> siblings

Tuple of nodes with the same parent. 

``` from anytree import Node```
``` udo = Node("Udo")``` ``` marc = Node("Marc", parent=udo)```
``` lian = Node("Lian", parent=marc)``` ``` loui = Node("Loui", parent=marc)```
``` lazy = Node("Lazy", parent=marc)``` ``` udo.siblings```
()
``` marc.siblings``` () ``` lian.siblings```
(Node('/Udo/Marc/Loui'), Node('/Udo/Marc/Lazy'))
``` loui.siblings``` (Node('/Udo/Marc/Lian'), Node('/Udo/Marc/Lazy')) 



---

<a href="../../th2_data_services/events_tree.py#L249"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_by_leaves_status`

```python
get_by_leaves_status(status: bool)
```





---

<a href="../../th2_data_services/events_tree.py#L246"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_by_status`

```python
get_by_status(status: bool)
```





---

<a href="../../th2_data_services/events_tree.py#L226"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show`

```python
show(fmt: Callable = None, failed_only=False, show_status=True)
```






---

<a href="../../th2_data_services/events_tree.py#L253"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `EventsTree2`
EventsTree2 - experimental tree. 

<a href="../../th2_data_services/events_tree.py#L256"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    data: Optional[Iterator, Generator[dict, NoneType], Data] = None,
    ds=None
)
```











---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
