import json
from collections import defaultdict
from datetime import datetime
from functools import partial
from os import listdir, path
from typing import List, Dict, Tuple, Callable

from th2_data_services.utils.event_utils import (
    extract_time,
    get_children_from_parents_as_list,
    get_children_from_parent_id,
)


# TODO
#   1. What index is?
#   2.


# NOT STREAMING
def get_event_tree_from_parent_events(
    events: List[Dict], parents: List[Dict], depth: int, max_children: int, body_to_simple_processors: Dict = None
) -> Tuple[Dict, Dict]:
    """Generate tree object based on parents events list.

    | "tree" structure:
    | {
    |     "info": { "stats": EventType+Status (Frequency Table) }
    |     "rootId": {
    |         "info": { event_details...}
    |         "body" { ... } # If event has body
    |         "parentId": {
    |             "info": { event_details...}
    |             "body" { ... } # If event has body
    |             "childId": { ... }
    |         }
    |     }
    |     "rootId2": { ... }
    | }
    |
    | "index" structure:
    | {
    |     "rootId": {
    |         "info": { event_details...}
    |         "body" { ... } # If event has body
    |         "parentId": {
    |             "info": { event_details...}
    |             "body" { ... } # If event has body
    |             "childId": { ... }
    |         }
    |     }
    |     "rootId2": { ... }
    | }

    Args:
        events (Dict[List]): TH2-Events
        parents (Dict[List]): TH2-Events
        depth (int): Max Iteration
        max_children (int): Max Children
        body_to_simple_processors (Dict, optional): Body Transformer Function, Defaults To None

    Returns:
        Tuple(Dict, Dict): Tree, Index
    """
    index = {}
    iteration = 0
    stats = defaultdict(int, TOTAL=0)
    tree = {"info": {"stats": stats}}
    current_children = parents
    while len(current_children) > 0 and iteration < depth:
        for child in current_children:
            leaf = {
                "info": {
                    "name": child["eventName"],
                    "type": child["eventType"],
                    "id": child["eventId"],
                    "time": extract_time(child),
                },
                "body": child["body"],
            }
            if len(child["attachedMessageIds"]) > 0:
                leaf["info"]["attachedMessageIds"] = child["attachedMessageIds"]

            if iteration == 0:
                dt = tree
            else:
                dt = index[child["parentEventId"]]

            child_event_status = "[ok]" if child["successful"] else "[fail]"
            leaf_index = len(dt)

            if "body" in dt:
                leaf_index -= 1

            child_event_str = f"{leaf_index} {child_event_status} {child['eventName']}"
            dt[child_event_str] = leaf
            index[child["eventId"]] = leaf

            # Calculating stats
            stats_key = f"{child['eventType']} {child_event_status}"
            stats[stats_key] += 1
            stats["TOTAL"] += 1

            # Simplifying body
            if len(child["body"]) == 0:
                leaf.pop("body")

            if body_to_simple_processors is not None:
                if (eventType := child["eventType"]) in body_to_simple_processors:
                    leaf["body"] = body_to_simple_processors[eventType](child["body"])

        current_children = get_children_from_parents_as_list(events, current_children, max_children)
        print(f"get_event_tree_from_parent - {iteration} len_children={len(current_children)} {datetime.now()}")
        iteration += 1

    return tree, index


# NOT STREAMING
def get_event_tree_from_parent_id(
    events: List[Dict], parent_id: str, depth: int, max_children: int, body_to_simple_processors: Dict = None
) -> Dict:
    """Generate tree object based on parent event id.

    | "tree" structure:
    | {
    |     "info": {
    |           "stats": EventType+Status (Frequency Table)
    |           parent_event_details...
    |     }
    |     "child_id": {
    |         "info": { event_details...}
    |         "child_id": {
    |             "info": { event_details...}
    |             "body" { ... } # If event has body
    |             "childId": { ... }
    |         }
    |     }
    |     "child_id2": { ... }
    | }

    Args:
        events (List[Dict]): TH2-Events
        parent_id (str): Parent ID
        depth (int): Max Iteration
        max_children (int): Max Children
        body_to_simple_processors (Dict, optional): Body Transformer Function. Defaults to None. e.g. {eventType: processor_function}

    Returns:
        Dict: Tree
    """
    current_children, parent = get_children_from_parent_id(events, parent_id, max_children)
    print(f"get_event_tree_from_parent - initial {datetime.now()}")
    tree, _ = get_event_tree_from_parent_events(
        events, current_children, depth, max_children, body_to_simple_processors
    )
    tree["info"].update({"name": parent["eventName"], "type": parent["eventType"], "time": extract_time(parent)})
    if len(parent["body"]) != 0:
        tree["body"] = parent["body"]

    return tree


# NOT STREAMING
def save_tree_as_json(tree: Dict, json_file_path: str, file_categorizer: Callable = None) -> None:
    """Saves Tree As JSON Format.

    Args:
        tree (Dict): TH2-Events transformed into tree (with util methods)
        json_file_path (str): JSON Path (must end with .json)
        file_categorizer (Callable, optional): File categorizer function. Defaults to None.

    Returns:
        None (Saves File)
    """
    path = json_file_path.replace(".json", "_summary.json")
    arranged_tree = {}
    summary = {"stats": tree["info"]["stats"]}
    types_set = list(set((type_[: type_.index(" [")] for type_ in tree["info"]["stats"] if type_ != "TOTAL")))
    summary["types_list"] = types_set

    with open(path, "w") as summary_file:
        json.dump(summary, summary_file, indent=3)

    if file_categorizer is not None:
        for key, leaf in tree.items():
            if key == "info" or key == "body":
                continue
            category = file_categorizer(key, leaf)
            if category not in arranged_tree:
                arranged_tree[category] = {}
            arranged_tree[file_categorizer(key, leaf)][key] = leaf
    else:
        arranged_tree["tree"] = tree

    for key, leaf in arranged_tree.items():
        # TODO: [WINDOWS] Fix file name. key may contain `:` which is invalid symbol in filename.
        path = json_file_path.replace(".json", f"_{key}.json")
        with open(path, "w") as out_file:
            json.dump(leaf, out_file, indent=3)


# STREAMING
def transform_tree(index: Dict, post_processors: Dict[str, Callable]) -> None:
    """Transform Tree.

    Args:
        index (Dict): TH2-Events transformed into tree index (from util functions)
        post_processors (Dict): Post Processors

    Returns:
        None, Modifies "index"
    """
    for leaf in index.values():
        leaf_type = leaf["info"]["type"]
        if leaf_type in post_processors:
            modified_leaf = post_processors[leaf_type](leaf)
            leaf.clear()
            leaf.update(modified_leaf)


# STREAMING? | Depends On `processor`
def process_trees_from_jsons(path_pattern: str, processor: Callable) -> None:
    """Loads JSON files locally and processes them with given function.

    Args:
        path_pattern: Path to json file(s)
        processor: Processor function

    """
    dir_path = path_pattern[: path_pattern.rindex("/")] if "/" in path_pattern else ""
    pattern = path_pattern[path_pattern.rindex("/") + 1 :] if "/" in path_pattern else path_pattern
    pattern = pattern.replace(".json", "")
    files = listdir(dir_path)
    for file in files:
        if pattern in file:
            with open(path.join(dir_path, file)) as f:
                tree = json.load(f)
                processor(tree)


# STREAMING
def tree_walk(tree: Dict, processor: Callable, tree_filter: Callable = None, root_path: List = []) -> None:
    """Process tree by processor [Recursive method].

    Args:
        tree: TH2-Events transformed into tree (from util functions)
        processor (Callable): Processor function
        tree_filter (Callable, optional): Tree filter function. Defaults to None.
        root_path (List, optional): Root path. Defaults to [].
    """
    for name, leaf in tree.items():
        if name == "info":
            continue
        if type(leaf) is not dict:
            continue
        new_path = [name, *root_path]
        if tree_filter is not None:
            if tree_filter(new_path, name, leaf):
                processor(new_path, name, leaf)
        else:
            processor(new_path, name, leaf)

        tree_walk(leaf, processor, tree_filter=tree_filter, root_path=new_path)


# STREAMING
def tree_walk_from_jsons(path_pattern: str, processor: Callable, tree_filter: Callable) -> None:
    """Loads JSON file(s) and processes them with given function.

    Args:
        path_pattern: Path to json file(s)
        processor: Processor function
        tree_filter: Tree filter function

    """
    process_trees_from_jsons(path_pattern, lambda tree: tree_walk(tree, processor, tree_filter=tree_filter))


# STREAMING
def tree_update_totals(categorizer: Callable, tree: Dict, path: List[str], name: str, leaf: Dict) -> None:
    """Updates tree by categorizer function as keys.

    Args:
        categorizer: Categorizer function
        tree: Tree
        path: Event path (from root to event)
        name: Event name
        leaf: Leaf (event)
    """
    category = categorizer(path, name, leaf)
    if category not in tree:
        tree[category] = 1
    else:
        tree[category] += 1


# STREAMING
def tree_get_category_totals(tree: Dict, categorizer: Callable, tree_filter: Callable) -> Dict:
    """Returns category totals from tree.

    Args:
        tree: TH2-Events transformed into tree (from util functions)
        categorizer: Categorizer function
        tree_filter: Tree filter function

    Returns:
        Dict
    """
    result = {}
    tree_walk(tree, partial(tree_update_totals, categorizer, result), tree_filter=tree_filter)
    return result


# STREAMING
def tree_get_category_totals_from_jsons(path_pattern, categorizer: Callable, tree_filter: Callable) -> Dict:
    """Returns category totals from JSON file(s).

    Args:
        path_pattern: Path to JSON file(s)
        categorizer: Categorizer function
        tree_filter: Tree filter function

    Returns:
        Dict
    """
    result = {}
    process_trees_from_jsons(
        path_pattern,
        lambda tree: tree_walk(tree, partial(tree_update_totals, categorizer, result), tree_filter=tree_filter),
    )
    return result


# NOT STREAMING
def search_tree_from_jsons(path_pattern, tree_filter: Callable[[List, str, Dict], Dict]) -> List:
    """Searches tree by filter function from JSON file(s).

    Args:
        path_pattern: JSON file(s) location
        tree_filter: Filter function.
        |   e.g. `tree_filter = lambda path, name, leaf: "[fail]" in name`

    Returns:
        List
    """
    result = []
    process_trees_from_jsons(
        path_pattern,
        lambda tree: tree_walk(tree, lambda path, name, leaf: result.append((path, leaf)), tree_filter=tree_filter),
    )
    return result


# NOT STREAMING
def search_tree(tree: Dict, tree_filter: Callable[[List, str, Dict], Dict]) -> List:
    """Searches tree by filter function.

    Args:
        tree: TH2-Events transformed into tree (from util functions)
        tree_filter: Filter function.
        |   e.g. `tree_filter = lambda path, name, leaf: "[fail]" in name`

    Returns:
        List
    """
    result = []
    tree_walk(tree, lambda path, name, leaf: result.append((path, leaf)), tree_filter=tree_filter)
    return result
