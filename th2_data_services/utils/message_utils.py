import base64
from collections import defaultdict
from typing import List, Dict, Callable, Set, Union

from th2_data_services.utils import misc_utils
from tabulate import tabulate


# # NOT STREAMABLE
# Extract compounded message into list of individual messages
# m: compounded message (retrieved from Data object)
# result: list of individual message objects
def expand_message(message: Dict) -> List[Dict]:
    """Extract compounded message into list of individual messages.

    Args:
        message: TH2-Message

    Returns:
        List[Dict]
    """
    if "/" not in message["messageType"]:
        return [message]
    result = []
    fields = message["body"]["fields"]
    for msg_type in fields.keys():
        msg_index = len(result)
        if "-" in msg_type:
            msg_type = msg_type[: msg_type.index("-")]
            # TODO: Remove or keep this line?
            # m_index = int(k[k.index("-") + 1:])

        new_msg = {}
        new_msg.update(message)
        new_msg["messageType"] = msg_type
        new_msg["body"] = {}
        new_msg["body"]["metadata"] = {}
        new_msg["body"]["metadata"].update(message["body"]["metadata"])
        new_msg["body"]["metadata"]["id"] = {}
        new_msg["body"]["metadata"]["id"].update(message["body"]["metadata"]["id"])
        new_msg["body"]["metadata"]["messageType"] = msg_type
        new_msg["body"]["metadata"]["id"]["subsequence"] = [message["body"]["metadata"]["id"]["subsequence"][msg_index]]
        new_msg["body"]["fields"] = fields[msg_type]["messageValue"]["fields"]
        result.append(new_msg)

    return result


# # STREAMABLE
# Gets Dictionary quantities of events for different message categories
# parameters are: iterable messages object
# category_list: list categorizer functions
# result contains calculation for keys: "category1 category2 ... categoryN"
# result: dictionary {string: int}
def get_totals(messages: List[Dict], categorizers: List[Callable], filter_: Callable = None) -> Dict[str, int]:
    """Returns dictionary quantities of events for different message categories.

    Args:
        messages: TH2-Messages
        categorizers: List of categorizer functions
        filter_: Filter functon, defaults to None

    Returns:
        Dict[str, int]
    """
    result = defaultdict(int)
    for message in messages:
        expanded_messages = expand_message(message)
        for expanded_message in expanded_messages:
            if filter_ is not None and not filter_(expanded_message):
                continue
            keys = []
            for categorizer in categorizers:
                keys.append(categorizer(expanded_message))
            key = " ".join(keys)
            result[key] += 1

    return result


# STREAMABLE
# Prints Dictionary quantities of events for different message categories
# parameters are: iterable messages object
# category_list: list categorizer functions
# result contains calculation for keys: "category1 category2 ... categoryN"
# result: table -> stdout
def print_totals(messages: List[Dict], categorizers: List[Callable], filter_: Callable = None) -> None:
    """Prints dictionary quantities of events for different message categories.

    Args:
        messages: TH2-Messages
        categorizers: List of categorizer functions
        filter_: Filter functon, defaults to None

    """
    result = get_totals(messages, categorizers, filter_)
    misc_utils.print_stats_dict(result)


# NOT STREAMABLE
# Gets limited list of messages from the stream
# parameters are: iterable messages object
# max: maximum messages to retrieve
# start(optional): extract events starting form this number (to investigate middle of the stream)
# result: List of message objects
def get_some(messages: List[Dict], max_count: int, start: int = 0, filter_: Callable = None) -> List[Dict]:
    """Returns limited list of messages from the stream.

    Args:
        messages: TH2-Messages
        max_count: Maximum messages to retrieve
        start: Extract events starting form this number, defaults to 0
        filter_: Filter function, defaults to None

    Returns:
        List[Dict]
    """
    result = []
    counter = 0
    max_count += start
    for message in messages:
        expanded_messages = expand_message(message)
        for expanded_message in expanded_messages:
            if filter_ is not None and not filter_(expanded_message):
                continue
            if counter >= start:
                result.append(expanded_message)
            counter += 1
            if counter >= max_count:
                break
        if counter >= max_count:
            break
    result.sort(key=extract_time, reverse=False)

    return result


# NOT STREAMABLE
# Prints limited list of messages from the stream in dictionary format
# parameters are: iterable messages object
# max: maximum messages to retrieve
# start(optional): extract events starting form this number (to investigate middle of the stream)
# maxPrint(optional): maximum messages to print
# result: List of message objects in dictionary format -> stdout
def print_some_raw(messages: List[Dict], max_count: int, start: int = 0, filter_: Callable = None) -> None:
    """Prints limited list of messages from the stream in dictionary format.

    Args:
        messages: TH2-Messages
        max_count: Maximum messages to retrieve
        start: Extract events starting form this number, defaults to 0
        filter_: Filter function, defaults to None

    """
    result = get_some(messages, max_count, start, filter_)
    max_count = max(max_count + 1, len(result))
    for i in range(max_count):
        print(result[i])


# NOT STREAMABLE
# Prints limited list of messages from the stream in ascii from raw binary format
# parameters are: iterable messages object
# max: maximum messages to retrieve
# start(optional): extract events starting form this number (to investigate middle of the stream)
# maxPrint(optional): maximum messages to print
# result: List of message objects in ascii from raw binary format -> stdout
def print_some_raw_source(messages: List[Dict], max_count: int, start: int = 0, filter_: Callable = None) -> None:
    """Prints limited list of messages from the stream in ascii from raw binary format.

    Args:
        messages: TH2-Messages
        max_count: Maximum messages to retrieve
        start: Extract events starting form this number, defaults to 0
        filter_: Filter function, defaults to None

    """
    result = get_some(messages, max_count, start, filter_)
    max_count = max(max_count + 1, len(result))
    for i in range(max_count):
        print_message_raw_source(result[i])


# NOT STREAMABLE
# Prints limited list of messages from the stream in dictionary format
# parameters are: iterable messages object
# max: maximum messages to retrieve
# start(optional): extract events starting form this number (to investigate middle of the stream)
# maxPrint(optional): maximum messages to print
# result: List of message objects in dictionary format -> stdout
def print_some(messages: List[Dict], max_count: int, start: int = 0, filter_: Callable = None) -> None:
    """Prints limited list of messages from the stream in dictionary format.

    Args:
        messages: TH2-Messages
        max_count: Maximum messages to retrieve
        start: Extract events starting form this number, defaults to 0
        filter_: Filter function, defaults to None

    """
    result = get_some(messages, max_count, start, filter_)
    max_count = max(max_count + 1, len(result))
    for i in range(max_count):
        print_message(result[i])


# STREAMABLE
def message_fields_to_flat_dict(message: Dict, result: Dict, prefix: str):  # noqa
    # TODO: Add Docstings
    for field, content in message["fields"].items():
        if "simpleValue" in content:
            result[prefix + field] = content["simpleValue"]

        if "messageValue" in content:
            new_prefix = f"{prefix}{field}."
            message_fields_to_flat_dict(content["messageValue"], result, new_prefix)

        if "listValue" in content:
            list_values = content["listValue"]["values"]
            for i in range(len(list_values)):
                new_prefix = f"{prefix}{field}."
                message_fields_to_flat_dict({"fields": {str(i): list_values[i]}}, result, new_prefix)


# STREAMABLE
# Converts message body tree structure
# parameters are: message object
# max: maximum messages to retrieve # TODO: Add Argument?
# result: dictionary representing body in flat format
def message_to_dict(message: Dict):
    """Converts message body to dict.

    Args:
        message: TH2-Message

    Returns:
        Dict
    """
    result = {}
    message_fields_to_flat_dict(message["body"], result, "")
    return result


# STREAMABLE
def extract_time(message: Dict) -> str:
    """Extracts timestamp from message.

    Args:
        message: TH2-Message

    Returns:
        str
    """
    return misc_utils.extract_timestamp(message["timestamp"])


# STREAMABLE
def print_message(message: Dict) -> None:
    """Print message (verbose).

    Args:
        message: TH2-Message

    """
    print(
        f"{extract_time(message)} > {message['sessionId']} {message['direction']} "
        f"{message['messageType']} {message_to_dict(message)}"
    )


# STREAMABLE
# Todo: Is This Useful?
def get_raw_body_str(m):  # noqa
    my_bytes = base64.b64decode(m["bodyBase64"].encode("ascii"))
    my_bytes = my_bytes.replace(b"\x01", b".")

    raw_body = my_bytes.decode("ascii")
    return raw_body


# STREAMABLE
# TODO: Is This Useful?
def print_message_raw_source(message: Dict) -> None:  # noqa
    raw_body = get_raw_body_str(message)
    print(
        f"{extract_time(message)} > {message['sessionId']} {message['direction']} "
        f"{message['messageType']} {raw_body}"
    )


# STREAMABLE
# TODO: Is This Useful?
# Resolves set of message IDs
# parameters are: iterable messages object
# ids_set: set of messages IDs to resolve
# result: resolved IDs removed from set
def resolve_count_message_ids(messages: List[Dict], ids: Set) -> None:
    """Resolves set of message IDs. # TODO: Update Description.

    Args:
        messages: TH2-Messages
        ids: Set of messages IDs to resolve

    Returns:
        None, Modifies `ids`
    """
    for message in messages:
        if message["messageId"] in ids:
            ids.remove(message["messageId"])


# NOT STREAMABLE
# Resolves set of message IDs
# parameters are: iterable messages object
# ids_set: set of messages IDs to resolve
# result: dictionary {message_id: message object}, resolved IDs removed from set
def resolve_message_ids(messages: List[Dict], ids: Set) -> Dict[str, Dict]:
    """Resolves set of message IDs. # TODO: Update Description.

    Args:
        messages: TH2-Messages
        ids: Set of messages IDs to resolve

    Returns:
        Dict[str, Dict]
    """
    result = {}
    for message in messages:
        msg_id = message["messageId"]
        if msg_id in ids:
            result[msg_id] = message
            ids.remove(msg_id)

    return result


# NOT STREAMABLE
def get_category_frequencies(
    messages: List[Dict],
    categories: List[str],
    categorizer: Callable,
    aggregation_level: str = "seconds",
    filter_: Callable = None,
):  # noqa
    # TODO: Add Descriptive Docstrings
    return misc_utils.get_objects_frequencies(
        messages,
        categories,
        categorizer,
        lambda message: message["timestamp"]["epochSecond"],
        aggregation_level=aggregation_level,
        object_expander=expand_message,
        objects_filter=filter_,
    )


# NOT STREAMABLE
def print_category_frequencies(
    messages: List[Dict],
    categories: List[str],
    categorizer: Callable,
    aggregation_level: str = "seconds",
    filter_: Callable = None,
    return_html=False,
) -> Union[None, str]:  # noqa
    # TODO: Add Descriptive Docstrings
    result = get_category_frequencies(messages, categories, categorizer, aggregation_level, filter_)

    if return_html:
        return tabulate(result, headers="firstrow", tablefmt="html")
    else:
        print(tabulate(result, headers="firstrow", tablefmt="grid"))
        return None


# NOT STREAMABLE
# TODO: Is This Useful?
def get_messages_examples(
    messages: List[Dict], categories: List[str], categorizer: Callable, filter_: Callable = None
) -> Dict:  # noqa
    # TODO: Add Docstrings
    result = {}
    categories = set(categories)
    for message in messages:
        expanded_messages = expand_message(message)
        for expanded_message in expanded_messages:
            if filter_ is not None and not filter_(expanded_message):
                continue
            c = categorizer(expanded_message)  # ???
            if c in categories:
                if c not in result:
                    result[c] = expanded_message
                    if len(result) == len(categories):
                        return result

    return result
