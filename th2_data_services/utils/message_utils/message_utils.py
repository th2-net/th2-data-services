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

import base64
from collections import defaultdict
from th2_data_services.config import options
from typing import Callable, Dict, Iterable, List, Set

from deprecated.classic import deprecated

import th2_data_services.utils.display
import th2_data_services.utils.time
from th2_data_services.utils._types import Th2Message
from th2_data_services.utils.converters import flatten_dict
from th2_data_services.utils._is_sorted_result import IsSortedResult


# DON'T USE `options` like this. By default MESSAGE_FIELDS_RESOLVER.expand_message == None
# It will bring to errors.
# expand_message = options.MESSAGE_FIELDS_RESOLVER.expand_message

# STREAMABLE
def get_totals(
    messages: Iterable[Th2Message],
    categorizers: List[Callable[[Dict], str]],
    filter_: Callable = None,
) -> Dict[str, int]:
    """Returns dictionary quantities of events for different message categories.

    The result contains calculation for keys: "category1 category2 ... categoryN".

    Warnings:
        expand_message function is not backward-compatible.
        If you use it in your scripts, there is no guarantee that everything will
        work if you change data-source because different data-sources has different
        messages structure.

    Args:
        messages: TH2-Messages - iterable messages object.
        categorizers: List of categorizer functions
        filter_: Filter functon, defaults to None

    Returns:
        Dict[str, int]
        like - {str_value_that_was_by_categorizer_func: cnt}
    """
    result = defaultdict(int)
    for message in messages:
        expanded_messages: List[Dict[str, str]] = options.mfr.expand_message(message)
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
def print_totals(
    messages: Iterable[Th2Message], categorizers: List[Callable], filter_: Callable = None
) -> None:
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
) -> List[Th2Message]:
    """Returns limited list of messages from the stream.

    Warnings:
        expand_message function is not backward-compatible.
        If you use it in your scripts, there is no guarantee that everything will
        work if you change data-source because different data-sources has different
        messages structure.

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
        expanded_messages: List[Dict[str, str]] = options.mfr.expand_message(message)
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
def print_some_raw(
    messages: Iterable[Th2Message], max_count: int, start: int = 0, filter_: Callable = None
) -> None:
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
def print_some(
    messages: Iterable[Th2Message], max_count: int, start: int = 0, filter_: Callable = None
) -> None:
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
@deprecated(
    "This function only make sense if you have data in Protobuf style format.\n"
    "Use DS-LwDP>=2.0.2.* to get messages in JSON-PARSED format.\n"
    "Use `th2_data_services.utils.converters.flatten_dict` instead of this function."
)
def message_fields_to_flat_dict(message: dict, result: Dict, prefix: str):  # noqa
    # Actual if provider returns data in Protobuf style
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
                message_fields_to_flat_dict(
                    {"fields": {str(i): list_values[i]}}, result, new_prefix
                )


def message_to_dict(message: Th2Message):
    """The function was moved to recon-lw repository.

    Args:
        message: 123

    Returns:
        None
    """
    raise Exception(
        "'message_to_dict' function was moved to recon-lw repository. \n"
        "Please notify th2 DEV team if you don't not agree."
    )


# STREAMABLE
def extract_time(message: Th2Message) -> str:
    """Extracts timestamp from message.

    Args:
        message: TH2-Message

    Returns:
        str
    """
    return th2_data_services.utils.time.extract_timestamp(
        options.MESSAGE_FIELDS_RESOLVER.get_timestamp(message)
    )


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
        f"{flatten_dict(options.MESSAGE_FIELDS_RESOLVER.get_body(message))}"
    )


# STREAMABLE
# Todo: Is This Useful
def get_raw_body_str(message: Dict):  # noqa
    my_bytes = base64.b64decode(
        options.MESSAGE_FIELDS_RESOLVER.get_body_base64(message).encode("ascii")
    )
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


# NOT STREAMABLE
# TODO: Is This Useful?
def get_messages_examples(
    messages: Iterable[Th2Message],
    categories: List[str],
    categorizer: Callable,
    filter_: Callable = None,
) -> Dict:  # noqa
    """TODO: Add Docstrings

    Warnings:
        expand_message function is not backward-compatible.
        If you use it in your scripts, there is no guarantee that everything will
        work if you change data-source because different data-sources has different
        messages structure.

    Args:
        messages:
        categories:
        categorizer:
        filter_:

    Returns:
        {category_name: message}
    """

    result = {}
    categories = set(categories)
    for message in messages:
        expanded_messages: List[Dict[str, str]] = options.mfr.expand_message(message)
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


def is_sorted(messages: Iterable[Th2Message]) -> IsSortedResult:
    """Checks whether messages are sorted.

    Args:
        messages (Dict): Th2-Messages

    Returns:
        IsSortedResult: Whether messages are sorted and additional info (e.g. index of the first unsorted element).
    """
    is_sorted_result = IsSortedResult()
    flag = True
    previous_timestamp = None
    i = 0
    for message in messages:
        if flag:
            previous_timestamp = options.mfr.get_timestamp(message)
            flag = False
        current_timestamp = options.MESSAGE_FIELDS_RESOLVER.get_timestamp(message)
        if previous_timestamp["epochSecond"] > current_timestamp["epochSecond"] or (
            previous_timestamp["epochSecond"] == current_timestamp["epochSecond"]
            and previous_timestamp["nano"] > current_timestamp["nano"]
        ):
            is_sorted_result.status = False
            is_sorted_result.first_unsorted = i
            break
        previous_timestamp = current_timestamp
        i += 1

    return is_sorted_result
