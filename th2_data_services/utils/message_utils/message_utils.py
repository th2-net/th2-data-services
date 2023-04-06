#  Copyright 2023 Exactpro (Exactpro Systems Limited)
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
import base64
from collections import defaultdict

# from th2_data_services import MESSAGE_FIELDS_RESOLVER
from typing import Callable, Dict, Iterable, List, Set
import th2_data_services.utils.display
import th2_data_services.utils.time
from th2_data_services.utils._types import Th2Message

from th2_data_services.config import options


# # NOT STREAMABLE
# Extract compounded message into list of individual messages
# m: compounded message (retrieved from Data object)
# result: list of individual message objects
def expand_message(message: Th2Message) -> Iterable[Th2Message]:
    """Extract compounded message into list of individual messages.

    Args:
        message: TH2-Message

    Returns:
        Iterable[Th2Message]
    """
    if "/" not in options.MESSAGE_FIELDS_RESOLVER.get_type(message):
        return [message]
    result = []
    fields = options.MESSAGE_FIELDS_RESOLVER.get_body(message)["fields"]
    for k in fields.keys():
        msg_index = len(result)
        msg_type = k
        if "-" in k:
            msg_type = msg_type[: msg_type.index("-")]
            # TODO: Remove or keep this line?
            # m_index = int(k[k.index("-") + 1:])

        new_msg = {}
        new_msg.update(message)
        new_msg["messageType"] = msg_type
        new_msg["body"] = {}
        new_msg["body"]["metadata"] = {}
        new_msg["body"]["metadata"].update(options.MESSAGE_FIELDS_RESOLVER.get_body(message)["metadata"])
        new_msg["body"]["metadata"]["id"] = {}
        new_msg["body"]["metadata"]["id"].update(options.MESSAGE_FIELDS_RESOLVER.get_body(message)["metadata"]["id"])
        new_msg["body"]["metadata"]["messageType"] = msg_type
        new_msg["body"]["metadata"]["id"]["subsequence"] = [
            options.MESSAGE_FIELDS_RESOLVER.get_body(message)["metadata"]["id"]["subsequence"][msg_index]
        ]
        new_msg["body"]["fields"] = fields[k]["messageValue"]["fields"]
        result.append(new_msg)

    return result


# # STREAMABLE
# Gets Dictionary quantities of events for different message categories
# parameters are: iterable messages object
# category_list: list categorizer functions
# result contains calculation for keys: "category1 category2 ... categoryN"
# result: dictionary {string: int}
def get_totals(
    messages: Iterable[Th2Message], categorizers: List[Callable[[Dict], str]], filter_: Callable = None
) -> Dict[str, int]:
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
def print_totals(messages: Iterable[Th2Message], categorizers: List[Callable], filter_: Callable = None) -> None:
    """Prints dictionary quantities of events for different message categories.

    Args:
        messages: TH2-Messages
        categorizers: List of categorizer functions
        filter_: Filter functon, defaults to None

    """
    result = get_totals(messages, categorizers, filter_)
    th2_data_services.utils.display.print_stats_dict(result)


# NOT STREAMABLE
# TODO - Can we have single function for events and messages?
def get_some(
    messages: Iterable[Th2Message], max_count: int, start: int = 0, filter_: Callable = None
) -> Iterable[Th2Message]:
    """Returns limited list of messages from the stream.

    Args:
        messages: TH2-Messages
        max_count: Maximum messages to retrieve
        start: Extract events starting form this number, defaults to 0
        filter_: Filter function, defaults to None

    Returns:
        Iterable[Th2Message]
    """
    result = []
    counter = 0
    limit = start + max_count

    for message in messages:
        expanded_messages = expand_message(message)
        for expanded_message in expanded_messages:
            if filter_ is not None and not filter_(expanded_message):
                continue
            if counter >= start:
                result.append(expanded_message)
            counter += 1
            if counter >= limit:
                break
        if counter >= limit:
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
def print_some_raw(messages: Iterable[Th2Message], max_count: int, start: int = 0, filter_: Callable = None) -> None:
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
def print_some_raw_source(
    messages: Iterable[Th2Message], max_count: int, start: int = 0, filter_: Callable = None
) -> None:
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
def print_some(messages: Iterable[Th2Message], max_count: int, start: int = 0, filter_: Callable = None) -> None:
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
# TODO - We will not use this in the future, I think, because LwDP can provide JSON_PARSED immediately.
def message_fields_to_flat_dict(message: dict, result: Dict, prefix: str):  # noqa
    # Actual if provider returns data in Protobuf style
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
# TODO - We will not use this in the future, I think, because LwDP can provide JSON_PARSED immediately.
def message_to_dict(message: Th2Message):
    """Converts message body to dict.

    Args:
        message: TH2-Message

    Returns:
        Dict
    """
    if "simpleBody" in message:
        return message["simpleBody"]

    result = {}
    message_fields_to_flat_dict(options.MESSAGE_FIELDS_RESOLVER.get_body(message), result, "")
    return result


# STREAMABLE
def extract_time(message: Th2Message) -> str:
    """Extracts timestamp from message.

    Args:
        message: TH2-Message

    Returns:
        str
    """
    return th2_data_services.utils.time.extract_timestamp(options.MESSAGE_FIELDS_RESOLVER.get_timestamp(message))


# STREAMABLE
def print_message(message: Th2Message) -> None:
    """Print message (verbose).

    Args:
        message: TH2-Message

    """
    print(
        f"{extract_time(message)} > {options.MESSAGE_FIELDS_RESOLVER.get_session_id(message)} "
        f"{options.MESSAGE_FIELDS_RESOLVER.get_direction(message)} "
        f"{options.MESSAGE_FIELDS_RESOLVER.get_type(message)} "
        f"{message_to_dict(message)}"
    )


# STREAMABLE
# Todo: Is This Useful
def get_raw_body_str(message: Dict):  # noqa
    my_bytes = base64.b64decode(options.MESSAGE_FIELDS_RESOLVER.get_body_base64(message).encode("ascii"))
    my_bytes = my_bytes.replace(b"\x01", b".")
    raw_body = my_bytes.decode("ascii")
    return raw_body


# STREAMABLE
# TODO: Is This Useful?
def print_message_raw_source(message: Th2Message) -> None:  # noqa
    raw_body = get_raw_body_str(message)
    print(
        f"{extract_time(message)} > {options.MESSAGE_FIELDS_RESOLVER.get_session_id(message)} "
        f"{options.MESSAGE_FIELDS_RESOLVER.get_direction(message)} "
        f"{options.MESSAGE_FIELDS_RESOLVER.get_type(message)} "
        f"{raw_body}"
    )


# STREAMABLE
# TODO: Is This Useful?
# Resolves set of message IDs
# parameters are: iterable messages object
# ids_set: set of messages IDs to resolve
# result: resolved IDs removed from set
def resolve_count_message_ids(messages: Iterable[Th2Message], ids: Set) -> None:
    """Resolves set of message IDs count. Modifies `ids`.

    Args:
        messages: TH2-Messages
        ids: Set of messages IDs to resolve

    Returns:
        None, Modifies `ids`
    """
    for message in messages:
        if options.MESSAGE_FIELDS_RESOLVER.get_id(message) in ids:
            ids.remove(options.MESSAGE_FIELDS_RESOLVER.get_id(message))


# NOT STREAMABLE
# Resolves set of message IDs
# parameters are: iterable messages object
# ids_set: set of messages IDs to resolve
# result: dictionary {message_id: message object}, resolved IDs removed from set
def resolve_message_ids(messages: Iterable[Th2Message], ids: Set) -> Dict[str, Th2Message]:
    """Resolves set of message IDs. Modifies `ids`.

    Args:
        messages: TH2-Messages
        ids: Set of messages IDs to resolve

    Returns:
        Dict[str, Th2Message]
    """
    result = {}
    for message in messages:
        msg_id = options.MESSAGE_FIELDS_RESOLVER.get_id(message)
        if msg_id in ids:
            result[msg_id] = message
            ids.remove(msg_id)

    return result


# TODO
#   COMMENTED - because we don't need it more. We will return classes that have good representation!
#   THIS PEACE OF CODE WILL BE REMOVED SOON
# def print_category_frequencies(
#     messages: Iterable[Th2Message],
#     categories: List[str],
#     categorizer: Callable,
#     aggregation_level: str = "seconds",
#     filter_: Callable = None,
#     return_html=False,
# ) -> Union[None, str]:  # noqa
#     # TODO: Add Descriptive Docstrings
#     result = get_category_frequencies(messages, categories, categorizer, aggregation_level, filter_)
#
#     if return_html:
#         return tabulate(result, headers="firstrow", tablefmt="html")
#     else:
#         print(tabulate(result, headers="firstrow", tablefmt="grid"))
#         return None


# NOT STREAMABLE
# TODO: Is This Useful?
def get_messages_examples(
    messages: Iterable[Th2Message], categories: List[str], categorizer: Callable, filter_: Callable = None
) -> Dict:  # noqa
    # TODO: Add Docstrings
    # It returns {category_name: message}
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
