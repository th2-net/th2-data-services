#  Copyright 2023-2024 Exactpro (Exactpro Systems Limited)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import json
from collections import defaultdict
from datetime import datetime
from functools import partial
from os import listdir, path
from pathlib import Path
from typing import List, Dict, Tuple, Callable

from th2_data_services.utils.path_utils import transform_filename_to_valid
from th2_data_services.utils.event_utils.event_utils import extract_start_timestamp
from th2_data_services.utils.event_utils.select import (
    get_children_from_parents_as_list,
    get_children_from_parent_id,
)


# TODO
#   1. What index is?
#   2. JsonTREE should become a class, from my point of view


# NOT STREAMING
def get_event_tree_from_parent_events(
    events: List[Dict],
    parents: List[Dict],
    depth: int,
    max_children: int,
    body_to_simple_processors: Dict = None,
) -> Tuple[Dict, Dict]:
    """Generate tree object based on parents events list.

    Args:
        events (Dict[List]): TH2-Events
        parents (Dict[List]): TH2-Events
        depth (int): Max iteration
        max_children (int): Max children
        body_to_simple_processors (Dict, optional): Body transformer function, defaults to None

    Returns:
        Tuple(Dict, Dict): Tree, Index

    Example:
        >>> get_event_tree_from_parent_events(events=events,
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
                    "time": extract_start_timestamp(child),
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
                event_type = child["eventType"]
                if event_type in body_to_simple_processors:
                    leaf["body"] = body_to_simple_processors[event_type](child["body"])

        current_children = get_children_from_parents_as_list(events, current_children, max_children)
        print(
            f"get_event_tree_from_parent - {iteration} len_children={len(current_children)} {datetime.now()}"
        )
        iteration += 1

    return tree, index


# NOT STREAMING
def get_event_tree_from_parent_id(
    events: List[Dict],
    parent_id: str,
    depth: int,
    max_children: int,
    body_to_simple_processors: Dict = None,
) -> Dict:
    """Generate tree object based on parent event id.

    Args:
        events (List[Dict]): TH2-Events
        parent_id (str): Parent ID
        depth (int): Max Iteration
        max_children (int): Max Children
        body_to_simple_processors (Dict, optional): Body Transformer Function. Defaults to None. e.g. {eventType: processor_function}

    Returns:
        Dict: Tree

    Example:
        >>> get_event_tree_from_parent_id(events=events,
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
    """
    current_children, parent = get_children_from_parent_id(events, parent_id, max_children)
    print(f"get_event_tree_from_parent - initial {datetime.now()}")
    tree, _ = get_event_tree_from_parent_events(
        events, current_children, depth, max_children, body_to_simple_processors
    )
    tree["info"].update(
        {
            "name": parent["eventName"],
            "type": parent["eventType"],
            "time": extract_start_timestamp(parent),
        }
    )
    if len(parent["body"]) != 0:
        tree["body"] = parent["body"]

    return tree


# NOT STREAMING
def save_tree_as_json(
    tree: Dict, json_file_path: str, file_categorizer: Callable = None
) -> List[str]:
    """Saves Tree As JSON Format.

    Will create a few json files in the path json_file_path.

    Args:
        tree (Dict): TH2-Events transformed into tree (with util methods)
        json_file_path (str): JSON Path (must end with .json)
        file_categorizer (Callable, optional): File categorizer function. Defaults to None.

    Returns:
        List of created filenames.

    Example:
        >>> save_tree_as_json(tree=az_tree,
                              json_file_path="path/to/output.json",
                              # file_categorizer=lambda key, leaf: key
            )
    """
    created_filenames = []
    path = Path(json_file_path).resolve().absolute().with_suffix(".json")

    path = path.parent / transform_filename_to_valid(path.name.replace(".json", "_summary.json"))

    # path = json_file_path.replace(".json", "_summary.json")
    # path_filename = json_file_path.replace(".json", "_summary.json")
    # path = path.parent / transform_filename_to_valid(path)
    arranged_tree = {}
    summary = {"stats": tree["info"]["stats"]}
    types_set = list(
        set((type_[: type_.index(" [")] for type_ in tree["info"]["stats"] if type_ != "TOTAL"))
    )
    summary["types_list"] = types_set

    created_filenames.append(str(path))

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
        path = path.parent / transform_filename_to_valid(path.name.replace(".json", f"_{key}.json"))
        # path = json_file_path.replace(".json", f"_{key}.json")
        # path = transform_filename_to_valid(path)
        with open(path, "w") as out_file:
            created_filenames.append(str(path))
            json.dump(leaf, out_file, indent=3)

    return created_filenames


# STREAMING
def transform_tree(index: Dict, post_processors: Dict[str, Callable[[Dict], Dict]]) -> None:
    """Transform Tree.

    Args:
        index (Dict): TH2-Events transformed into tree index (from util functions)
        post_processors (Dict): Post Processors

    Returns:
        None, Modifies "index"

    Example:
        # TODO: Add example...
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

    Example:
        >>> process_trees_from_jsons(
                path_to_json_files="path/to/files.json",
                processor: # TODO: Add processor example
            )
    """
    dir_path = path_pattern[: path_pattern.rindex("/")] if "/" in path_pattern else ""
    pattern = path_pattern[path_pattern.rindex("/") + 1 :] if "/" in path_pattern else path_pattern
    pattern = pattern.replace(".json", "")
    files = listdir(dir_path)
    for file in files:
        if pattern in file:
            with open(path.join(dir_path, file)) as f:
                tree = json.load(f)
                # TODO: Does data change here? How does this work?
                processor(tree)


# STREAMING
def tree_walk(
    tree: Dict, processor: Callable, tree_filter: Callable = None, root_path: List = []
) -> None:
    """Process tree by processor [Recursive method].

    Args:
        tree: TH2-Events transformed into tree (from util functions)
        processor (Callable): Processor function
        tree_filter (Callable, optional): Tree filter function. Defaults to None.
        root_path (List, optional): Root path. Defaults to [].

    Examples:
        >>> tree_walk(tree=az_tree,
                      processor=lambda path, name, leaf: leaf.update({name: "/".join(path)}),
                      tree_filter=lambda path, name, leaf: "[fail]" in name),
                      # root_path=[rootName, ..., eventName])

    """
    for name, leaf in tree.items():
        if name == "info" or type(leaf) is not dict:
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

    Examples:
        >>> tree_walk_from_jsons(
                path_to_json_files="path/to/files.json",
                processor=lambda path, name, leaf: leaf.update({name: "/".join(path)}),
                tree_filter=lambda path, name, leaf: "[fail]" in name
            )
    """
    process_trees_from_jsons(
        path_pattern, lambda tree: tree_walk(tree, processor, tree_filter=tree_filter)
    )


# STREAMING
def tree_update_totals(
    categorizer: Callable, tree: Dict, path: List[str], name: str, leaf: Dict
) -> None:
    """Updates tree by categorizer function as keys.

    Args:
        categorizer: Categorizer function
        tree: Tree
        path: Event path (from root to event)
        name: Event name
        leaf: Leaf (event)

    Examples:
        # TODO: Add example
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

    Examples:
        >>> tree_get_category_totals(
                tree=az_tree,
                categorizer=lambda path, name, leaf: leaf['info']['type'] if 'info' in leaf else None,
                tree_filter=lambda path, name, leaf: "[fail]" not in name)
            {
                'Outgoing message': 941,
                'sendMessage': 95,
                ...
            }
    """
    result = {}
    tree_walk(
        tree, processor=partial(tree_update_totals, categorizer, result), tree_filter=tree_filter
    )
    return result


# STREAMING
def tree_get_category_totals_from_jsons(
    path_pattern, categorizer: Callable, tree_filter: Callable
) -> Dict:
    """Returns category totals from JSON file(s).

    Args:
        path_pattern: Path to JSON file(s)
        categorizer: Categorizer function
        tree_filter: Tree filter function

    Returns:
        Dict

    Examples:
        # TODO: Add example
    """
    result = {}
    process_trees_from_jsons(
        path_pattern,
        lambda tree: tree_walk(
            tree, partial(tree_update_totals, categorizer, result), tree_filter=tree_filter
        ),
    )
    return result


# NOT STREAMING
def search_tree(tree: Dict, tree_filter: Callable[[List, str, Dict], Dict]) -> List[Dict]:
    """Searches tree by filter function.

    Args:
        tree: TH2-Events transformed into tree (from util functions)
        tree_filter: Filter function.

    Returns:
        List[Dict]

    Example:
        >>> search_tree(tree=az_tree,
                        tree_filter=lambda path, name, leaf: "[fail]" in name)
            [
                {**TH2-Event}, # "[fail]" in eventName
                ...
            ]
    """
    result = []
    tree_walk(tree, lambda path, name, leaf: result.append((path, leaf)), tree_filter=tree_filter)
    return result


# NOT STREAMING
def search_tree_from_jsons(
    path_to_json_files, tree_filter: Callable[[List, str, Dict], Dict]
) -> List:
    """Searches tree by filter function from JSON file(s).

    Args:
        path_to_json_files: JSON file(s) location
        tree_filter: Filter function.

    Returns:
        List

    Examples:
        >>> search_tree_from_jsons(
                path_to_json_files="path/to/files.json",
                tree_filter=lambda path, name, leaf: "[fail]" in name
            )
    """
    result = []
    process_trees_from_jsons(
        path_to_json_files,
        lambda tree: tree_walk(
            tree, lambda path, name, leaf: result.append((path, leaf)), tree_filter=tree_filter
        ),
    )
    return result
