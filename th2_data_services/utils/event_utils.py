from functools import partial
from os import listdir, path
from typing import Callable, Dict, List, Tuple, Set, Union
from datetime import datetime
from th2_data_services.utils import misc_utils
import json
from collections import defaultdict
from tabulate import tabulate

# TODO -
#   1. events: List[Dict] -- should be Iterable[Th2Event], where Th2Event = Dict. It can be changed in the future
#   2. IDEA - it's difficult to understand what you will get when read some functions. I think add examples
#   3. Rename all docstrings word Gets to Returns. That's different things.


def get_category_frequencies(
    events: List[Dict], categories: List[str], categorizer: Callable, aggregation_level: str = "seconds"
) -> List[List[str]]:
    """Gets Event Frequencies Based On Event Category.

    Args:
        events (List[Dict]): TH2-Events
        categories (List[str]): Event Categories
        categorizer (Callable): Categorizer Method
        aggregation_level (Optional, str): Aggregation Level

    Returns:
        List[List[str]]
    """
    return misc_utils.get_objects_frequencies(
        events,
        categories,
        categorizer,
        lambda e: e["startTimestamp"]["epochSecond"],
        aggregation_level=aggregation_level,
    )


# TODO - slava
#   Do we really need it? Why user cannot just use this one line?
#   Maybe better to have prepared list of categorizers? e.g. in form of Adapters.
#   get_category_frequencies(events, types_list, EventCategorizer.type)
#   or idea to creat class TypeFrequences
#   GetFrequences.by_type_category
#   GetFrequences.by_name_category
#   GetFrequences.by_category
def get_type_frequencies(events: List[Dict], types_list: List[str], aggregation_level="seconds") -> List[List[str]]:
    """Returns Event Frequencies Based On EventType.

    Args:
        events (List[Dict]): TH2-Events
        types_list (List[str]): Event Types
        aggregation_level (Optional, str): Aggregation Level

    Returns:
        List[List[str]]: List Of Frequency Lists
    """
    return get_category_frequencies(events, types_list, lambda e: e["eventType"], aggregation_level)


# USEFUL
# STREAMING
# TODO - NOT-READY -- event["successful"] should be updated by resolver
# categorizer - expects that it will return str
# --
# example
# eu.get_category_totals(d2, lambda e: e["eventType"])
# defaultdict(<class 'int'>, {'Service event [ok]': 9531, 'Info [ok]': 469})
# eu.get_category_totals(d2, lambda e: 'aaa')
# defaultdict(<class 'int'>, {'aaa [ok]': 10000})
def get_category_totals(events: List[Dict], categorizer: Callable, ignore_status: bool = False) -> Dict[str, int]:
    """Gets Dictionary quantities of events for different categories.

    Args:
        events (List[Dict]): TH2-Events
        categorizer (Callable): Transformer function
        ignore_status (bool): Concatenate status string, defaults to False.

    Returns:
        Dict[str, int]
    """
    event_categories = defaultdict(int)
    for event in events:
        category = categorizer(event)
        if not ignore_status:
            status = " [ok]" if event["successful"] else " [fail]"
            category += status
        else:
            event_categories[category] += 1

    return event_categories


# USEFUL
# STREAMING
# TODO - NOT-READY -- event["attachedMessageIds"] should be updated by resolver
# example
# eu.get_attached_messages_totals(d1)
# defaultdict(<class 'int'>, {'envtn2_msfix5:first': 25262, 'envtn2_jpmfix1:second': 1702, 'env2_gscofixg2:second': 1702,...
def get_attached_messages_totals(events: List[Dict]) -> Dict[str, int]:
    """Returns Dictionary quantities of messages attached to events for each stream.

    Args:
        events (List[Dict]): TH2-Events

    Returns:
        Dict[str, int]
    """
    streams = defaultdict(int)
    for event in events:
        for message_id in event["attachedMessageIds"]:
            key = message_id[: message_id.rindex(":")]
            streams[key] += 1

    return streams


# USEFUL
# STREAMING
# TODO - NOT-READY -- event["attachedMessageIds"] should be updated by resolver
def get_attached_message_ids(events: List[Dict]) -> Set[str]:
    """Returns the set of unique message IDs linked to all events.

    Args:
        events (List[Dict]): TH2-Events

    Returns:
        Set[str]
    """
    return set(message_id for event in events for message_id in event["attachedMessageIds"])


# USEFUL
# TODO - NOT-READY -- event["parentEventId, eventId"] should be updated by resolver
# TODO - It returns only parent events that not present in the events.
#   Perhaps we need to find better name
# we use something similar in our EventTree
def get_prior_parent_ids(events: List[Dict]) -> Set[str]:
    """Returns only parent events that not present in the events.

    Args:
        events (List[Dict]): TH2-Events

    Returns:
        Set[str]
    """
    all_event_ids = set()
    parent_ids = set()
    for event in events:
        parent_id = event["parentEventId"]
        event_id = event["eventId"]
        if parent_id is not None and not parent_id in all_event_ids:
            parent_ids.add(parent_id)
        if event_id in parent_ids:
            parent_ids.remove(event_id)
        all_event_ids.add(event_id)

    return parent_ids


# USEFUL
# NOT STREAMING - keeps events
# TODO - NOT-READY -- event["attachedMessageIds"] should be updated by resolver
# BE AWARE!! - it can it all your memory
# O(N*M)
def get_attached_message_ids_index(events: List[Dict]) -> Dict[str, list]:
    """Gets dict of lists of related events by unique message IDs.

    Note:
        This object can occupy large amount of memory for big collections of events - use with caution
        Keeps in memory all events that are linked to messages.

    Args:
        events (List[Dict]): TH2-Events

    Returns:
        Dict[str, list]
    """
    result = defaultdict(list)
    for event in events:
        for message_id in event["attachedMessageIds"]:
            result[message_id].append(event)

    return result


# USEFULL ??? Do we need ignore status??
# partly the same as get_category_totals and WO ignore status
# Because it's the same we can you get_category_totals inside
#
# STREAMING
# TODO - NOT-READY -- event["successful"] should be updated by resolver
def get_type_totals(events: List[Dict]) -> Dict[str, int]:
    """Gets dictionary quantities of events for different event types.

    Args:
        events (List[Dict]): TH2-Events

    Returns:
        Dict[str, int]
    """
    event_types = defaultdict(int)
    for event in events:
        status = " [ok]" if event["successful"] else " [fail] "
        event_type = event["eventType"] + status
        event_types[event_type] += 1

    return event_types


# TODO - USEFUL ???
#   What the example of this? look very rarely need to use
# Will return list! Perhaps it's better to return Data?
def get_events(events: List[Dict], event_type: str, count: int, start: int = 0, failed: bool = False) -> List[Dict]:
    """Gets limited list of events of specific eventType.

    Args:
        events (List[Dict]): TH2-Events
        event_type (str): Event Type To Extract
        count (int): Maximum number of events to extract
        start (int, optional): Start Iteration Index. Defaults to 0.
        failed (bool, optional): Extract Only Failed Events. Defaults to False.

    Returns:
        List[Dict]
    """
    result = []
    limit = start + count
    counter = 0
    for event in events:
        if event["eventType"] == event_type:
            if failed and event["successful"]:
                continue
            if counter >= start:
                result.append(event)
            counter += 1
            if counter == limit:
                break

    return result


def get_related_events(events: List[Dict], messages: List[Dict], count: int) -> List[Dict]:
    """Gets limited list of events of linked to any message within specified messages objects collection.

    Args:
        events: TH2-Events
        messages: TH2-Messages
        count: Maximum number of events to extract

    Returns:
        List[Dict]
    """
    result = []
    msg_ids = set(message["messageId"] for message in messages)

    for event in events:
        for msg_id in event["attachedMessageIds"]:
            if msg_id in msg_ids:
                result.append(event)
                if len(result) == count:
                    return result

    return result


def get_events_by_category(
    events: List[Dict], category: str, count: int, categorizer: Callable, start=0, failed=False
) -> List[Dict]:
    """Gets limited list of events of specific category produced by custom categorizer.

    Args:
        events (List[Dict]): TH2-Events
        category (str): Event Category To Extract
        count (int): Maximum number of events to extract
        categorizer (Callable): Transformer Function
        start (int, optional): Start Iteration Index. Defaults to 0.
        failed (bool, optional): Extract Only Failed Events. Defaults to False.

    Returns:
        List[Dict]
    """
    result = []
    limit = start + count
    counter = 0
    for event in events:
        if categorizer(event) == category:
            if failed and event["successful"]:
                continue
            if counter >= start:
                result.append(event)
            counter += 1
            if counter == limit:
                break

    return result


def get_roots(events: List[Dict], count: int, start: int = 0) -> List[Dict]:
    """Gets limited list of root events (events without parents).

    Args:
        events (List[Dict]): TH2-Events
        count (int): Maximum number of events to extract
        start (int, optional): Iteration Start Index, Defaults to 0.

    Returns:
        List[Dict]: List Of Root Events.
    """
    result = []
    limit = start + count
    counter = 0
    for event in events:
        if event["parentEventId"] is None:
            if counter >= start:
                result.append(event)
            counter += 1
            if counter == limit:
                break

    return result


def get_parents(events: List[Dict], children: List[Dict]):
    """Gets all parent events of linked to any event within specified events objects collection.

    Args:
        events (List[Dict]): TH2-Events
        children (List[Dict]): Extract Parents By Child Events

    """
    parent_ids = set(child["parentEventId"] for child in children)
    return [event for event in events if event["eventId"] in parent_ids]


def get_children_from_parent_id(events: List[Dict], parent_id: str, max_events: int) -> Tuple[List[Dict], Dict]:
    """Gets limited list of direct children events.

    Args:
        events (List[Dict]): TH2-Events
        parent_id (str): Parent ID
        max_events (int): Maximum number of events to extract

    Returns:
        Tuple[List[Dict], Dict]: Children Events, Parent Event
    """
    children = []
    resolved_parent = {}
    counter = 0
    for event in events:
        if event["eventId"] == parent_id:
            resolved_parent = event
        if event["parentEventId"] == parent_id:
            children.append(event)
            counter += 1
            if counter == max_events:
                break

    return children, resolved_parent


def get_children_from_parents(events: List[Dict], parents: List[Dict], max_events: int) -> Tuple[Dict[str, list], int]:
    """Gets limited list of direct children events for each event in parents.

    Args:
        events (List[Dict]): TH2-Events
        parents (List[str]): TH2-Events
        max_events (int): Maximum number of events to extract

    Returns:
        Tuple(Dict[str, list], int): Parent-Children, Events Count
    """
    parent_ids = set(parent["eventId"] for parent in parents)
    result = defaultdict(list)
    events_count = 0
    for event in events:
        parent_id = event["parentEventId"]
        if parent_id not in parent_ids:
            continue
        events_count += 1
        if len(result[parent_id]) <= max_events:
            result[parent_id].append(event)

    return result, events_count


def get_children_from_parents_as_list(events: List[Dict], parents: List[Dict], max_events: int) -> List[Dict]:
    """Gets limited list of direct children events for each event in parents.

    Args:
        events (List[Dict]): TH2-Events
        parents (List[Dict]): TH2-Events
        max_events(int): Maximum number of events to extract

    Returns:
        Dict[str, list]: Children Events
    """
    parent_ids = set(parent["eventId"] for parent in parents)
    result = []
    parents_counts = defaultdict(int)
    for event in events:
        parent_id = event["parentEventId"]
        if parent_id not in parent_ids:
            continue
        if parents_counts[parent_id] <= max_events:
            result.append(event)
        parents_counts[parent_id] += 1

    return result


def get_event_tree_from_parent_events(
    events: List[Dict], parents: List[Dict], depth: int, max_children: int, body_to_simple_processors: Dict = None
) -> Tuple[Dict, Dict]:
    """Generate tree object based on parents events list.

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


def get_event_tree_from_parent_id(
    events: List[Dict], parent_id: str, depth: int, max_children: int, body_to_simple_processors: Dict = None
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


def sublist(events: List[Dict], start_time: datetime, end_time: datetime) -> List[Dict]:
    """Filter Events Based On Timeframe.

    Args:
        events (List[Dict]): TH2-Events
        start_time (datetime): Start
        end_time (datetime): End Time

    Returns:
        List[Dict]: Filtered Events.
    """
    result = []
    start_time = datetime.timestamp(start_time)
    end_time = datetime.timestamp(end_time)
    for event in events:
        event_time = event["startTimestamp"]["epochSecond"]
        if start_time <= event_time <= end_time:
            result.append(event)

    return result


def extract_parent_as_json(
    events: Dict,
    parent_id: str,
    json_file_path: str,
    interval_start: str,
    interval_end: str,
    body_to_simple_processors: Callable = None,
):
    """Parse Parent Into JSON Format.

    Args:
        events (Dict): TH2-Events
        parent_id (str): Parent ID
        json_file_path (str): JSON Output Path
        interval_start (str): Interval Start
        interval_end (str): Interval End
        body_to_simple_processors (Callable, optional): Body Transformer Function. Defaults to None.
    """
    sub_events = sublist([events], datetime.fromisoformat(interval_start), datetime.fromisoformat(interval_end))
    print(f"Sublist Length = {len(sub_events)}")
    tree, _ = get_event_tree_from_parent_id(sub_events, parent_id, 10, 10000, body_to_simple_processors)
    types_set = list(set((type_[: type_.index(" [")] for type_ in tree["info"]["stats"] if type_ != "TOTAL")))
    tree["info"]["types_list"] = types_set

    with open(json_file_path, "w") as file:
        json.dump(tree, file, indent=3)


def save_tree_as_json(tree: Dict, json_file_path: str, file_categorizer: Callable = None) -> None:
    """Saves Tree As JSON Format.

    Args:
        tree (Dict): Collection Of Data
        json_file_path (str): JSON Path (Must End With .json)
        file_categorizer (Callable, optional): File Categorizer. Defaults to None.

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
        path = json_file_path.replace(".json", f"_{key}.json")
        with open(path, "w") as out_file:
            json.dump(leaf, out_file, indent=3)


def transform_tree(index: Dict, post_processors: Dict[str, Callable]) -> None:
    """Transform Tree.

    Args:
        index (Dict): Index Dict
        post_processors (Dict): Post Processors

    Returns:
        None (Modifies Index Dict)
    """
    for leaf in index.values():
        leaf_type = leaf["info"]["type"]
        if leaf_type in post_processors:
            modified_leaf = post_processors[leaf_type](leaf)
            leaf.clear()
            leaf.update(modified_leaf)


def process_trees_from_jsons(path_pattern: str, processor: Callable) -> None:  # noqa
    # TODO: Add Docstings
    dir_path = path_pattern[: path_pattern.rindex("/")] if "/" in path_pattern else ""
    pattern = path_pattern[path_pattern.rindex("/") + 1 :] if "/" in path_pattern else path_pattern
    pattern = pattern.replace(".json", "")
    files = listdir(dir_path)
    for file in files:
        if pattern in file:
            with open(path.join(dir_path, file)) as f:
                tree = json.load(f)
                processor(tree)


def tree_walk(tree: Dict, processor: Callable, tree_filter: Callable = None, root_path: List = []) -> None:  # noqa
    # TODO: Add Docstings
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


def tree_walk_from_jsons(path_pattern, processor, tree_filter):  # noqa
    # TODO: Add Docstings
    process_trees_from_jsons(path_pattern, lambda tree: tree_walk(tree, processor, tree_filter=tree_filter))


def tree_update_totals(categorizer, result, p, n, l):  # noqa
    # TODO: Add Docstings
    category = categorizer(p, n, l)
    if category not in result:
        result[category] = 1
    else:
        result[category] += 1


def tree_get_category_totals(tree, categorizer, tree_filter):  # noqa
    # TODO: Add Docstings
    result = {}
    tree_walk(tree, partial(tree_update_totals, categorizer, result), tree_filter=tree_filter)
    return result


def tree_get_category_totals_from_jsons(path_pattern, categorizer, tree_filter):  # noqa
    # TODO: Add Docstings
    result = {}
    process_trees_from_jsons(
        path_pattern,
        lambda tree: tree_walk(tree, partial(tree_update_totals, categorizer, result), tree_filter=tree_filter),
    )

    return result


def search_tree(tree, filter_lambda):  # noqa
    # TODO: Add Docstings
    result = []
    tree_walk(tree, lambda p, n, l: result.append((p, l)), tree_filter=filter_lambda)
    return result


def search_tree_from_jsons(path_pattern, filter_lambda):  # noqa
    # TODO: Add Docstings
    result = []
    process_trees_from_jsons(
        path_pattern, lambda tree: tree_walk(tree, lambda p, n, l: result.append((p, l)), tree_filter=filter_lambda)
    )
    return result


def build_roots_cache(events, depth, max_level):  # noqa
    # TODO: Add Docstings
    result = {}
    level = 1
    prev_levels = get_roots(events, max_level)
    print("First level :", len(prev_levels))
    for prev_level in prev_levels:
        result[prev_level["eventId"]] = {"eventName": prev_level["eventName"], "eventPath": prev_level["eventName"]}
    while level < depth:
        next_levels = get_children_from_parents_as_list(events, prev_levels, max_level)
        print("Next level :", len(next_levels))
        for next_level in next_levels:
            event_id = next_level["eventId"]
            parent_id = next_level["parentEventId"]
            result[event_id] = {
                "eventName": next_level["eventName"],
                "eventPath": result[parent_id]["eventPath"] + "/" + next_level["eventName"],
            }
        prev_level = next_levels
        level += 1
    return result


def extract_time(event) -> str:
    """Gets string representation of events timestamp.

    Args:
        event: TH2-Event

    Returns:
        str
    """
    return misc_utils.extract_time_string(event["startTimestamp"])


def print_attached_messages_totals(events: List[Dict], return_html: bool = False) -> Union[None, str]:
    """Prints Dictionary quantities of messages attached to events for each stream + direction.

    Args:
        events (List[Dict]): TH2-Events
        return_html (bool): Return HTML Format

    """
    data = get_attached_messages_totals(events)
    return misc_utils.print_stats_dict(data, return_html)


def print_category_totals(
    events: List[Dict], categorizer: Callable, return_html: bool = False, ignore_status: bool = False
) -> Union[None, str]:
    """Prints Dictionary quantities of events for different categories.

    Args:
        events (List[Dict]): TH2-Events
        categorizer (Callable): Categorizer Method
        return_html (bool): Return HTML Format, defaults to False
        ignore_status (bool): Get status of events, defaults to False

    Returns:
        Union[None, str]
    """
    data = get_category_totals(events, categorizer, ignore_status=ignore_status)
    return misc_utils.print_stats_dict(data, return_html)


def print_event(event: Dict) -> None:
    """Prints event in human-readable format.

    Args:
        event (List[Dict]): TH2-Events

    """
    print(
        f"{extract_time(event)} > [{'ok' if event['successful'] else 'fail'}] "
        f"Type: {event['eventType']} "
        f"Name: {event['eventName']} "
        f"ID: {event['eventId']} "
        f"Parent:{event['parentEventId']} "
        f"Body:{event['body']}"
    )


def print_events_raw(events: List[Dict], event_type: str, count: int, start: int = 0, failed: bool = False) -> None:
    """Prints limited list of events of specific eventType in dictionary format.

    Args:
        events (List[Dict]): TH2-Events
        event_type (set): Event Type To Extract
        count (int): Maximum number of events to extract
        start (int, optional): Start Iteration Index. Defaults to 0.
        failed (bool, optional): Extract Only Failed Events. Defaults to False.

    """
    records = get_events(events, event_type, count, start, failed)
    for r in records:
        print(r)


def print_some(events: List[Dict], event_type: str, count: int, start: int = 0, failed: bool = False) -> None:
    """Prints limited list of events of specific eventType in human-readable format.

    Args:
        events (List[Dict]): TH2-Events
        event_type (set): Event Type To Extract
        count (int): Maximum number of events to extract
        start (int, optional): Start Iteration Index. Defaults to 0.
        failed (bool, optional): Extract Only Failed Events. Defaults to False.

    """
    records = get_events(events, event_type, count, start, failed)
    for r in records:
        print_event(r)


def print_some_by_category(
    events: List[Dict], category: str, count: int, categorizer: Callable, start: int = 0, failed: bool = False
):  # noqa
    # TODO: Add Docstings
    records = get_events_by_category(events, category, count, categorizer, start, failed)
    for r in records:
        print_event(r)


def print_roots(events: List[Dict], count: int, start: int = 0) -> None:
    """Prints limited list of root events (events without parents).

    Args:
        events (List[Dict]): TH2-Events
        count (int): Maximum number of events to extract
        start (int, optional): Start Iteration Index. Defaults to 0.

    """
    records = get_roots(events, count, start)
    for r in records:
        print_event(r)


def print_children(events: List[Dict], parent: str, count: int, verbose: bool = True):
    """Prints limited list of direct children events.

    Args:
        events (List[Dict]): TH2-Events
        parent (str): Parent ID
        count (int): Maximum number of events to extract
        verbose (bool): Verbose output, defaults to True.

    """
    records = get_children_from_parent_id(events, parent, count)
    fprint = print_event if verbose is True else print
    for r in records:
        fprint(r)


def print_type_totals(events: List[Dict], return_html: bool = False) -> Union[None, str]:
    """Prints dictionary quantities of events for different event types.

    Args:
        events (List[Dict]): TH2-Events
        return_html (bool): HTML format, defaults to False

    Returns:
        Union[None, str]
    """
    event_types = get_type_totals(events)
    return misc_utils.print_stats_dict(event_types)


def print_type_frequencies(
    events: List[Dict], event_types: List[str], aggregation_level: str = "seconds", return_html=False
) -> Union[None, str]:
    """Prints table of events per seconds or each second when there were events within events stream.

    Args:
        events: TH2-Events
        event_types: List of event types to analyze
        aggregation_level: Aggregation level
        return_html: Return HTML format, defaults to False

    """
    table = get_type_frequencies(events, event_types)
    if return_html:
        return tabulate(table, headers="firstrow", tablefmt="html")
    else:
        print(tabulate(table, headers="firstrow", tablefmt="grid"))


def print_category_frequencies(
    events: List[Dict],
    event_types: List[str],
    categorizer: Callable,
    aggregation_level: str = "seconds",
    return_html: bool = False,
) -> Union[None, str]:
    """Prints table of events per seconds or each second when there were events within events stream.

    Args:
        events (List[Dict]): TH2-Events
        event_types (List[str]): Event Types To Extract
        categorizer (Callable): Transformer Function
        aggregation_level (str): Aggregation Level
        return_html: Return HTML Format

    Returns:
        Union[None, str]
    """
    data = get_category_frequencies(events, event_types, categorizer, aggregation_level)
    return misc_utils.print_stats_dict(data, return_html)


def print_children_from_parents(events: List[Dict], parents: List[Dict], max_events: int = 10_000) -> None:
    """Prints limited list of direct children events for each event in parents_list.

    Args:
        events (List[Dict]): TH2-Events
        parents (List[Dict]): Parent TH2-Events
        max_events (int): Maximum number of events to extract, default to 10'000

    """
    tree, count = get_children_from_parents(events, parents, max_events)
    print(f"####### Retrieved Children: {count}")
    for parent in parents:
        print(parent)
        print(f">>>>>>> Children: {len(tree[parent['eventId']])}")
        for child in tree[parent["eventId"]]:
            print_event(child)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")


def print_children_stats_from_parents(
    events: List[Dict], parents: List[Dict], max_events: int = 10_000, return_html: bool = False
) -> Union[None, str]:
    """Prints statistics with number of children and their duration for each event in parents_list.

    Args:
        events (List[Dict]): TH2-Events
        parents (List[Dict]): Parent TH2-Events
        max_events (int): Maximum number of events to extract, default to 10'000
        return_html (bool): Return HTML format, defaults to False

    """
    tree, _ = get_children_from_parents(events, parents, max_events)
    table = [["eventName", "status", "eventId", "child_pass", "child_fail", "start", "end"]]  # Header
    for parent in parents:
        start_timestamp, end_timestamp = 0, 0
        events_passed, events_failed = 0, 0
        for child in tree[parent["eventId"]]:
            child_start_time_epoch = child["startTimestamp"]["epochSecond"]
            if child_start_time_epoch > end_timestamp:
                end_timestamp = child_start_time_epoch
            if start_timestamp == 0 or child_start_time_epoch < start_timestamp:
                start_timestamp = child_start_time_epoch

            if child["successful"]:
                events_passed += 1
            else:
                events_failed += 1

        table.append(
            [
                parent["eventName"],
                "[ok]" if parent["successful"] else "[fail]",
                events_passed,
                events_failed,
                datetime.fromtimestamp(start_timestamp).isoformat(),
                datetime.fromtimestamp(end_timestamp).isoformat(),
                datetime.fromtimestamp(end_timestamp).isoformat(),
            ]
        )

    if return_html:
        return tabulate(table, headers="firstrow", tablefmt="html")
    else:
        print(tabulate(table, headers="firstrow", tablefmt="grid"))
