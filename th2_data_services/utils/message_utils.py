from misc_utils import print_stats_dict, extract_time
from typing import List, Dict, Callable, Set, Union


def get_category_totals(messages: List[Dict], category_list: List[Callable]) -> Dict[str, int]:
    """Get Category Frequency.

    Args:
        messages (List[Dict]): TH2-Messages
        category_list (List[Callable]): Transformer Functions

    Returns:
        Dict[str, int]: Category Frequency
    """
    result = {}
    for message in messages:
        key = " ".join([transformer(message) for transformer in category_list])
        if key not in result:
            result[key] = 1
        else:
            result[key] += 1

    return result


def get_messages(messages: Dict, max_msgs: int, start: int = 0) -> List[Dict]:
    """Get Messages.

    Args:
        messages (Dict): TH2-Messages
        max_msgs (int): Max Counter
        start (int, optional): Start Iteration Index. Defaults to 0.

    Returns:
        List[Dict]: TH2-Messages
    """
    result = []
    for i, message in enumerate(messages):
        if i >= start:
            result.append(message)
        if i >= start + max_msgs:
            break

    result.sort(key=lambda m: extract_time(m, "m"), reverse=False)

    return result


def message_fields_to_flat_dict(collection: Dict, flat_list: Dict, prefix: str) -> None:
    """Message To Flat Dict.

    Args:
        collection (Dict): Message Collection
        flat_list (Dict): Flat List
        prefix (str): Prefix
    """
    fields = collection["fields"]
    for field, content in fields.items():
        if "simpleValue" in content:
            flat_list[prefix + field] = content["simpleValue"]

        if "messageValue" in content:
            new_prefix = f"{prefix}{field}."
            message_fields_to_flat_dict(content["messageValue"], flat_list, new_prefix)

        if "listValue" in content:
            list_values = content["listValue"]["values"]
            for i, val in enumerate(list_values):
                new_prefix = f"{prefix}{field}."
                message_fields_to_flat_dict({"fields": {str(i): val}}, flat_list, new_prefix)


def message_to_dict(message: Dict) -> Dict:
    """TH2-Event -> Dict.

    Args:
        message (Dict): TH2-Event

    Returns:
        Dict: TH2-Event As Dict.
    """
    result = {}
    message_fields_to_flat_dict(message["body"], result, "")
    return result


def resolve_message_ids_set(messages: List[Dict], ids_set: Union[List[str], Set[str]]) -> Dict[str, Dict]:
    """Resolve Message IDs Set.

    Args:
        messages (List[Dict]): TH2-Messages
        ids_set (Union[List[str], Set[str]]): TH2-Messages IDs

    Returns:
        Dict[str, Dict]: Resolved Messages
    """
    result = {}
    for message in messages:
        if (msgID := message["messageId"]) in ids_set:
            result[msgID] = message
            ids_set.remove(msgID)
    return result


# # # OUTPUT FUNCTIONS # # #


def print_message(m: Dict):  # noqa
    print(
        f"{extract_time(m)} > SessionID: {m['sessionId']} "
        f"Direction: {m['direction']} "
        f"MessageType: {m['messageType']} "
        f"As Dict: {message_to_dict(m)}"
    )


def print_category_totals(messages, category_list):  # noqa
    result = get_category_totals(messages, category_list)
    print_stats_dict(result)


def print_some_raw(messages, max, start=0, maxPrint=1000):  # noqa
    result = get_messages(messages, max, start)
    mp = maxPrint if maxPrint < len(result) else len(result)
    for i in range(0, mp):
        print(result[i])


def print_some(messages, max, start=0, maxPrint=1000):  # noqa
    result = get_messages(messages, max, start)
    mp = maxPrint if maxPrint < len(result) else len(result)
    for i in range(0, mp):
        print_message(result[i])
