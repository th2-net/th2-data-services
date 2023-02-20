<!-- markdownlint-disable -->

<a href="../../th2_data_services/utils/az_tree.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.az_tree`





---

<a href="../../th2_data_services/utils/az_tree.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_event_tree_from_parent_events`

```python
get_event_tree_from_parent_events(
    events: List[Dict],
    parents: List[Dict],
    depth: int,
    max_children: int,
    body_to_simple_processors: Dict = None
) → Tuple[Dict, Dict]
```

Generate tree object based on parents events list. 



**Args:**
 
 - <b>`events`</b> (Dict[List]):  TH2-Events 
 - <b>`parents`</b> (Dict[List]):  TH2-Events 
 - <b>`depth`</b> (int):  Max iteration 
 - <b>`max_children`</b> (int):  Max children 
 - <b>`body_to_simple_processors`</b> (Dict, optional):  Body transformer function, defaults to None 



**Returns:**
 
 - <b>`Tuple`</b> (Dict, Dict):  Tree, Index 



**Example:**
 ``` get_event_tree_from_parent_events(events=events,```
                                           parents=parent_events,
                                           depth=10,
                                           max_children=100)
    (
         { # tree
             "info": { "stats": EventType+Status (Frequency Table) }
             "rootId": {
                 "info": { event_details...}
                 "body" { ... } # If event has body
                 "parentId": {
                     "info": { event_details...}
                     "body" { ... } # If event has body
                     "childId": { ... }
                 }
             }
             "rootId2": { ... }
         }
         ,
         { # index
             "rootId": {
                 "info": { event_details...}
                 "body" { ... } # If event has body
                 "parentId": {
                     "info": { event_details...}
                     "body" { ... } # If event has body
                     "childId": { ... }
                 }
             }
             "rootId2": { ... }
         }
    )



---

<a href="../../th2_data_services/utils/az_tree.py#L123"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_event_tree_from_parent_id`

```python
get_event_tree_from_parent_id(
    events: List[Dict],
    parent_id: str,
    depth: int,
    max_children: int,
    body_to_simple_processors: Dict = None
) → Dict
```

Generate tree object based on parent event id. 



**Args:**
 
 - <b>`events`</b> (List[Dict]):  TH2-Events 
 - <b>`parent_id`</b> (str):  Parent ID 
 - <b>`depth`</b> (int):  Max Iteration 
 - <b>`max_children`</b> (int):  Max Children 
 - <b>`body_to_simple_processors`</b> (Dict, optional):  Body Transformer Function. Defaults to None. e.g. {eventType: processor_function} 



**Returns:**
 
 - <b>`Dict`</b>:  Tree 



**Example:**
 ``` get_event_tree_from_parent_id(events=events,```
                                       parent_id="demo_parent_id",
                                       depth=10,
                                       max_children=1000)
         { # tree
            "info": {
                 "stats": EventType+Status (Frequency Table)
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

<a href="../../th2_data_services/utils/az_tree.py#L174"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `save_tree_as_json`

```python
save_tree_as_json(
    tree: Dict,
    json_file_path: str,
    file_categorizer: Callable = None
) → None
```

Saves Tree As JSON Format. 



**Args:**
 
 - <b>`tree`</b> (Dict):  TH2-Events transformed into tree (with util methods) 
 - <b>`json_file_path`</b> (str):  JSON Path (must end with .json) 
 - <b>`file_categorizer`</b> (Callable, optional):  File categorizer function. Defaults to None. 



**Returns:**
 None (Saves File) 



**Example:**
 ``` save_tree_as_json(tree=az_tree,```
                           json_file_path="path/to/output.json",
                           # file_categorizer=lambda key, leaf: key
         )



---

<a href="../../th2_data_services/utils/az_tree.py#L219"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `transform_tree`

```python
transform_tree(
    index: Dict,
    post_processors: Dict[str, Callable[[Dict], Dict]]
) → None
```

Transform Tree. 



**Args:**
 
 - <b>`index`</b> (Dict):  TH2-Events transformed into tree index (from util functions) 
 - <b>`post_processors`</b> (Dict):  Post Processors 



**Returns:**
 None, Modifies "index" 



**Example:**
 # TODO: Add example... 


---

<a href="../../th2_data_services/utils/az_tree.py#L241"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `process_trees_from_jsons`

```python
process_trees_from_jsons(path_pattern: str, processor: Callable) → None
```

Loads JSON files locally and processes them with given function. 



**Args:**
 
 - <b>`path_pattern`</b>:  Path to json file(s) 
 - <b>`processor`</b>:  Processor function 



**Example:**
 ``` process_trees_from_jsons(```
             path_to_json_files="path/to/files.json",
             processor: # TODO: Add processor example
         )



---

<a href="../../th2_data_services/utils/az_tree.py#L267"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `tree_walk`

```python
tree_walk(
    tree: Dict,
    processor: Callable,
    tree_filter: Callable = None,
    root_path: List = []
) → None
```

Process tree by processor [Recursive method]. 



**Args:**
 
 - <b>`tree`</b>:  TH2-Events transformed into tree (from util functions) 
 - <b>`processor`</b> (Callable):  Processor function 
 - <b>`tree_filter`</b> (Callable, optional):  Tree filter function. Defaults to None. 
 - <b>`root_path`</b> (List, optional):  Root path. Defaults to []. 



**Examples:**
 ``` tree_walk(tree=az_tree,```
                   processor=lambda path, name, leaf: leaf.update({name: "/".join(path)}),
                   tree_filter=lambda path, name, leaf: "[fail]" in name),
                   # root_path=[rootName, ..., eventName])



---

<a href="../../th2_data_services/utils/az_tree.py#L297"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `tree_walk_from_jsons`

```python
tree_walk_from_jsons(
    path_pattern: str,
    processor: Callable,
    tree_filter: Callable
) → None
```

Loads JSON file(s) and processes them with given function. 



**Args:**
 
 - <b>`path_pattern`</b>:  Path to json file(s) 
 - <b>`processor`</b>:  Processor function 
 - <b>`tree_filter`</b>:  Tree filter function 



**Examples:**
 ``` tree_walk_from_jsons(```
             path_to_json_files="path/to/files.json",
             processor=lambda path, name, leaf: leaf.update({name: "/".join(path)}),
             tree_filter=lambda path, name, leaf: "[fail]" in name
         )



---

<a href="../../th2_data_services/utils/az_tree.py#L316"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `tree_update_totals`

```python
tree_update_totals(
    categorizer: Callable,
    tree: Dict,
    path: List[str],
    name: str,
    leaf: Dict
) → None
```

Updates tree by categorizer function as keys. 



**Args:**
 
 - <b>`categorizer`</b>:  Categorizer function 
 - <b>`tree`</b>:  Tree 
 - <b>`path`</b>:  Event path (from root to event) 
 - <b>`name`</b>:  Event name 
 - <b>`leaf`</b>:  Leaf (event) 



**Examples:**
 # TODO: Add example 


---

<a href="../../th2_data_services/utils/az_tree.py#L337"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `tree_get_category_totals`

```python
tree_get_category_totals(
    tree: Dict,
    categorizer: Callable,
    tree_filter: Callable
) → Dict
```

Returns category totals from tree. 



**Args:**
 
 - <b>`tree`</b>:  TH2-Events transformed into tree (from util functions) 
 - <b>`categorizer`</b>:  Categorizer function 
 - <b>`tree_filter`</b>:  Tree filter function 



**Returns:**
 Dict 



**Examples:**
 ``` tree_get_category_totals(```
             tree=az_tree,
             categorizer=lambda path, name, leaf: leaf['info']['type'] if 'info' in leaf else None,
             tree_filter=lambda path, name, leaf: "[fail]" not in name)
         {
             'Outgoing message': 941,
             'sendMessage': 95,
             ...
         }



---

<a href="../../th2_data_services/utils/az_tree.py#L365"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `tree_get_category_totals_from_jsons`

```python
tree_get_category_totals_from_jsons(
    path_pattern,
    categorizer: Callable,
    tree_filter: Callable
) → Dict
```

Returns category totals from JSON file(s). 



**Args:**
 
 - <b>`path_pattern`</b>:  Path to JSON file(s) 
 - <b>`categorizer`</b>:  Categorizer function 
 - <b>`tree_filter`</b>:  Tree filter function 



**Returns:**
 Dict 



**Examples:**
 # TODO: Add example 


---

<a href="../../th2_data_services/utils/az_tree.py#L388"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `search_tree`

```python
search_tree(
    tree: Dict,
    tree_filter: Callable[[List, str, Dict], Dict]
) → List[Dict]
```

Searches tree by filter function. 



**Args:**
 
 - <b>`tree`</b>:  TH2-Events transformed into tree (from util functions) 
 - <b>`tree_filter`</b>:  Filter function. 



**Returns:**
 List[Dict] 



**Example:**
 ``` search_tree(tree=az_tree,```
                     tree_filter=lambda path, name, leaf: "[fail]" in name)
         [
             {**TH2-Event}, # "[fail]" in eventName
             ...
         ]



---

<a href="../../th2_data_services/utils/az_tree.py#L412"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `search_tree_from_jsons`

```python
search_tree_from_jsons(
    path_to_json_files,
    tree_filter: Callable[[List, str, Dict], Dict]
) → List
```

Searches tree by filter function from JSON file(s). 



**Args:**
 
 - <b>`path_to_json_files`</b>:  JSON file(s) location 
 - <b>`tree_filter`</b>:  Filter function. 



**Returns:**
 List 



**Examples:**
 ``` search_tree_from_jsons(```
             path_to_json_files="path/to/files.json",
             tree_filter=lambda path, name, leaf: "[fail]" in name
         )





---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
