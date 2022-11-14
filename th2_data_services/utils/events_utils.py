from typing import Callable, Dict, List, Tuple
from tabulate import tabulate
from datetime import datetime
from misc_utils import extract_time, print_stats_dict
import json
from collections import defaultdict


def get_frequencies(events: List[Dict], types_list: List[str]) -> List[List[str]]:
    """Gets Event Frequencies Based On EventType.

    Args:
        events (List[Dict]): TH2-Events
        types_list (List[str]): Event Types

    Returns:
        List[List[str]]: List Of Frequency Lists
    """
    freq = {}
    types_len = len(types_list)
    for event in events:
        for i, event_type in enumerate(types_list):
            if event["eventType"] == event_type:
                epoch = event["startTimestamp"]["epochSecond"]
                if epoch not in freq:
                    freq[epoch] = [0] * types_len
                freq[epoch][i] += 1

    freq_tabular = [["timestamp", *types_list]]  # Header
    for timestamp in sorted(freq.keys()):
        freq_tabular.append([datetime.fromtimestamp(timestamp).isoformat(), *freq[timestamp]])

    return freq_tabular


def get_category_totals(events: List[Dict], categorizer_lambda: Callable) -> Dict[str, int]:
    """Gets Event Category Frequency.

    Args:
        events (List[Dict]): TH2-Events
        categorizer_lambda (Callable): Transformer Function

    Returns:
        Dict: Event Categories Frequencies.
    """
    event_categories = {}
    for event in events:
        status = " [ok]" if event["successful"] else " [fail] "
        category = categorizer_lambda(event) + status
        if not (category in event_categories):
            event_categories[category] = 1
        else:
            event_categories[category] += 1

    return event_categories


def get_attached_messages_totals(events: List[Dict]) -> Dict[str, int]:
    """Gets Attached Messages Frequency.

    Args:
        events (List[Dict]): TH2-Events

    Returns:
        Dict[str, int]: Attacked Messages Frequencies.
    """
    streams = {}
    for event in events:
        for message_id in event["attachedMessageIds"]:
            key = message_id[: message_id.rindex(":")]
            if not (key in streams):
                streams[key] = 1
            else:
                streams[key] += 1

    return streams


def get_attached_message_ids_index(events: List[Dict]) -> Dict[str, list]:
    """Gets Attached Messages ID Index.

    Args:
        events (List[Dict]): TH2-Events

    Returns:
        Dict[str, list]: Attached Messages ID Indexes.
    """
    result = {}
    for event in events:
        for message_id in event["attachedMessageIds"]:
            if message_id not in result:
                result[message_id] = []
            result[message_id].append(event)

    return result


def get_event_type_totals(events: List[Dict]) -> Dict[str, int]:
    """Gets EventType Frequency.

    Args:
        events (List[Dict]): TH2-Events

    Returns:
        Dict[str, int]: EventType Frequencyies.
    """
    event_types = {}
    for event in events:
        status = " [ok]" if event["successful"] else " [fail] "
        event_type = event["eventType"] + status
        if not (event_types in event_types):
            event_types[event_type] = 1
        else:
            event_types[event_type] += 1

    return event_types


def get_events(events: List[Dict], type_: str, count: int, start: int = 0, failed: bool = False) -> List[Dict]:
    """Get Filtered Events By EventType.

    Args:
        events (List[Dict]): TH2-Events
        type_ (str): EventType
        count (int): Length Of Filtered Events
        start (int, optional): Start Iteration Index. Defaults to 0.
        failed (bool, optional): Failed Events. Defaults to False.

    Returns:
        List[Dict]: Filtered Events.
    """
    result = []
    for i, event in enumerate(events):
        if event["eventType"] == type_:
            if failed and event["successful"]:
                continue  # TODO: Figure Out How It Should Work
            if i >= start:
                result.append(event)
            if i == start + count:
                break

    return result


def get_events_by_category(
    events: List[Dict], category: str, count: int, categorizer: Callable, start=0, failed=False
) -> List[Dict]:
    """Get Filtered Events By Category.

    Args:
        events (List[Dict]): TH2-Events
        category (str): Category
        count (int): Length Of Filtered Events
        categorizer (Callable): Transformer Function
        start (int, optional): Start Iteration Index. Defaults to 0.
        failed (bool, optional): Failed Events. Defaults to False.

    Returns:
        List[Dict]: _description_
    """
    result = []
    for i, event in enumerate(events):
        if categorizer(event) == category:
            if failed and event["successful"]:
                continue
            if i >= start:
                result.append(event)
            if i == start + count:
                break

    return result


def get_roots(events: List[Dict], count: int, start: int = 0) -> List[Dict]:
    """Gets Roots From Events.

    Args:
        events (List[Dict]): TH2-Events
        count (int): Roots Count
        start (int, optional): Iteration Start Index. Defaults to 0.

    Returns:
        List[Dict]: List Of Root Events.
    """
    result = []
    for i, event in enumerate(events):
        if event["parentEventId"] is None:
            if i >= start:
                result.append(event)
            if i == start + count:
                break
    return result


def get_children_from_parent_id(events: List[Dict], parentID: str, count: int) -> Tuple[List[Dict], Dict]:
    """Gets Children From Parent ID.

    Args:
        events (List[Dict]): TH2-Events
        parentID (str): Parent ID
        count (int): Children Count

    Returns:
        Tuple[List[Dict], Dict]: Children Events, Parent Event
    """
    children = []
    resolved_parent = {}
    for i, event in enumerate(events):
        if event["eventId"] == parentID:
            resolved_parent = event
        if event["parentEventId"] == parentID:
            children.append(event)
            if i == count:
                break

    return children, resolved_parent


def get_children_from_parents(events: List[Dict], parents: List[Dict], max_events: int) -> Tuple[Dict[str, list], int]:
    """Get Children From Parents.

    Args:
        events (List[Dict]): TH2-Events
        parents (List[str]): TH2-Events
        max_events (int): Max Events For Parent

    Returns:
        Tuple(Dict[str, list], int): Parent-Children, Events Count
    """
    parentIDs = set((parent["eventId"] for parent in parents))
    result = defaultdict(list)
    events_count = 0
    for event in events:
        parentID = event["parentEventId"]
        if parentID not in parentIDs:
            continue
        events_count += 1
        if len(result[parentID]) <= max_events:
            result[parentID].append(event)

    return result, events_count


def get_children_from_parents_as_list(events: List[Dict], parents: List[Dict], max_events: int) -> List[Dict]:
    """Get Children From Parents (Unorganized).

    Args:
        events (List[Dict]): TH2-Events
        parents (List[Dict]): TH2-Events
        max_events(int): Max Events

    Returns:
        Dict[str, list]: Children Events
    """
    parentIDs = set((parent["eventId"] for parent in parents))
    result = []
    for event in events:
        parentID = event["parentEventId"]
        if parentID not in parentIDs:
            continue
        if len(result) <= max_events:
            result.append(event)

    return result


def get_event_tree_from_parent_events(
    events: List[Dict], parents: List[Dict], depth: int, max_children: int, body_to_simple_processors: Dict = None
) -> Tuple[Dict, Dict]:
    """Get Event Tree From Parent Events.

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
    stats = {"TOTAL": 0}
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
            if stats_key not in stats:
                stats[stats_key] = 0
            stats[stats_key] = stats[stats_key] + 1
            stats["TOTAL"] = stats["TOTAL"] + 1

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


def get_event_tree_from_parent(
    events: List[Dict], parentId: str, depth: int, max_children: int, body_to_simple_processors: Dict = None
) -> Dict:
    """Gets Event Tree From Parent.

    Args:
        events (List[Dict]): TH2-Events
        parentId (str): Parent ID
        depth (int): Max Iteration
        max_children (int): Max Children
        body_to_simple_processors (Dict, optional): Body Transformer Function. Defaults to None.

    Returns:
        Dict: Tree
    """
    current_children, parent = get_children_from_parent_id(events, parentId, max_children)
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
    tree, _ = get_event_tree_from_parent(sub_events, parent_id, 10, 10000, body_to_simple_processors)
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


# # # OUTPUT FUNCTIONS # # #


def print_attached_messages_totals(events):  # noqa
    d = get_attached_messages_totals(events)
    print_stats_dict(d)


def print_category_totals(events, categorizer_lambda):  # noqa
    d = get_category_totals(events, categorizer_lambda)
    print_stats_dict(d)


def print_event(event):  # noqa
    print(
        f"{extract_time(event)} > [{'ok' if event['successful'] else 'fail'}] "
        f"Type: {event['eventType']} "
        f"Name: {event['eventName']} "
        f"ID: {event['eventId']} "
        f"Parent:{event['parentEventId']} "
        f"Body:{event['body']}"
    )


def print_events_raw(events, type_, count, start=0, failed=False):  # noqa
    records = get_events(events, type_, count, start, failed)
    for r in records:
        print(r)


def print_some(events, type_, count, start=0, failed=False):  # noqa
    records = get_events(events, type_, count, start, failed)
    for r in records:
        print_event(r)


def print_events_category(events, category, count, categorizer, start=0, failed=False):  # noqa
    records = get_events_by_category(events, category, count, categorizer, start, failed)
    for r in records:
        print_event(r)


def print_roots(events, count, start=0):  # noqa
    records = get_roots(events, count, start)
    for r in records:
        print_event(r)


def print_children_raw(events, parent, count):  # noqa
    records = get_children_from_parent_id(events, parent, count)
    for r in records:
        print(r)


def print_children(events, parent, count):  # noqa
    records = get_children_from_parents_as_list(events, parent, count)
    for r in records:
        print_event(r)


def print_event_type_totals(events):  # noqa
    event_types = get_event_type_totals(events)
    print_stats_dict(event_types)


def print_frequencies(events, types):  # noqa
    tb = get_frequencies(events, types)
    print(tabulate(tb, headers="firstrow", tablefmt="grid"))


def print_children_from_parents(events, parents):  # noqa
    tree, count = get_children_from_parents(events, parents, 10000)
    print(f"####### Retrieved Children: {count}")
    for parent in parents:
        print(parent)
        print(f">>>>>>> Children: {len(tree[parent['eventId']])}")
        for c in tree[parent["eventId"]]:
            print_event(c)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")


def print_children_stats_from_parents(events, parents):  # noqa
    tree, _ = get_children_from_parents(events, parents, 10000)
    table = [["eventName", "status", "eventId", "children", "start", "end"]]  # Header
    for parent in parents:
        start_timestamp = 0
        end_timestamp = 0
        for child in tree[parent["eventId"]]:
            child_start_time_epoch = child["startTimestamp"]["epochSecond"]
            if child_start_time_epoch > end_timestamp:
                end_timestamp = child_start_time_epoch
            if start_timestamp == 0 or child_start_time_epoch < start_timestamp:
                start_timestamp = child_start_time_epoch
        table.append(
            [
                parent["eventName"],
                "[ok]" if parent["successful"] else "[fail]",
                parent["eventId"],
                str(len(tree[parent["eventId"]])),
                datetime.fromtimestamp(start_timestamp).isoformat(),
                datetime.fromtimestamp(end_timestamp).isoformat(),
            ]
        )
    print(tabulate(table, headers="firstrow", tablefmt="grid"))
