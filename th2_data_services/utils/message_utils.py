from qa_utils import misc_utils
import base64
from tabulate import tabulate


# Extract compounded message into list of individual messages
# m: compounded message (retrieved from Data object)
# result: list of individual message objects
def expand_message(m):
    if "/" not in m["messageType"]:
        return [m]
    result = []
    fields = m["body"]["fields"]
    for k in fields.keys():
        m_type = k
        m_index = len(result)
        if "-" in k:
            m_type = k[:k.index("-")]
            #m_index = int(k[k.index("-")+1:])

        new_m = {}
        new_m.update(m)
        new_m["messageType"] = m_type
        new_m["body"] = {}
        new_m["body"]["metadata"] = {}
        new_m["body"]["metadata"].update(m["body"]["metadata"])
        new_m["body"]["metadata"]["id"] = {}
        new_m["body"]["metadata"]["id"].update(m["body"]["metadata"]["id"])
        new_m["body"]["metadata"]["messageType"] = m_type
        new_m["body"]["metadata"]["id"]["subsequence"] = [m["body"]["metadata"]["id"]["subsequence"][m_index]]
        new_m["body"]["fields"] = fields[k]["messageValue"]["fields"]
        result.append(new_m)
    return result


# Gets Dictionary quantities of events for different message categories
# parameters are: iterable messages object
# category_list: list categorizer functions
# result contains calculation for keys: "category1 category2 ... categoryN"
# result: dictionary {string: int}
def get_totals(messages, category_list, filter=None):
    result = {}
    for mess in messages:
        me = expand_message(mess)
        for m in me:
            if filter is not None and not filter(m):
                continue
            keys = []
            for f in category_list:
                keys.append(f(m))
            key = " ".join(keys)
            if key not in result:
                result[key] = 1
            else:
                result[key] = result[key] + 1

    return result


# Prints Dictionary quantities of events for different message categories
# parameters are: iterable messages object
# category_list: list categorizer functions
# result contains calculation for keys: "category1 category2 ... categoryN"
# result: table -> stdout
def print_totals(messages, category_list, filter=None):
    result = get_totals(messages,category_list, filter=filter)
    misc_utils.print_stats_dict(result)


# Gets limited list of messages from the stream
# parameters are: iterable messages object
# max: maximum messages to retrieve
# start(optional): extract events starting form this number (to investigate middle of the stream)
# result: List of message objects
def get_some(messages, max, start=0, filter=None):
    result = []
    n = 0
    for m in messages:
        exp = expand_message(m)
        for mm in exp:
            if filter is not None and not filter(mm):
                continue
            if n >= start:
                result.append(mm)
            n = n + 1
            if n >= start+max:
                break
        if n >= start + max:
            break
    result.sort(key=extract_time_for_print, reverse=False)
    return result


# Prints limited list of messages from the stream in dictionary format
# parameters are: iterable messages object
# max: maximum messages to retrieve
# start(optional): extract events starting form this number (to investigate middle of the stream)
# maxPrint(optional): maximum messages to print
# result: List of message objects in dictionary format -> stdout
def print_some_raw(messages, max, start=0, maxPrint=1000, filter=None):
    result = get_some(messages, max, start, filter=filter)
    mp = maxPrint if maxPrint < len(result) else len(result)
    for i in range(0, mp):
        print(result[i])


# Prints limited list of messages from the stream in ascii from raw binary format
# parameters are: iterable messages object
# max: maximum messages to retrieve
# start(optional): extract events starting form this number (to investigate middle of the stream)
# maxPrint(optional): maximum messages to print
# result: List of message objects in ascii from raw binary format -> stdout
def print_some_raw_source(messages, max, start=0, maxPrint=1000, filter=None):
    result = get_some(messages, max, start, filter=filter)
    mp = maxPrint if maxPrint < len(result) else len(result)
    for i in range(0, mp):
        print_message_raw_source(result[i])


# Prints limited list of messages from the stream in dictionary format
# parameters are: iterable messages object
# max: maximum messages to retrieve
# start(optional): extract events starting form this number (to investigate middle of the stream)
# maxPrint(optional): maximum messages to print
# result: List of message objects in dictionary format -> stdout
def print_some(messages, max, start=0, maxPrint=1000, filter=None):
    result = get_some(messages, max, start, filter=filter)
    mp = maxPrint if maxPrint < len(result) else len(result)
    for i in range(0, mp):
        print_message(result[i])


def message_fields2flat_dict(collection, flat_list, prefix):
    fields = collection["fields"]
    for field, content in fields.items():
        if "simpleValue" in content:
            flat_list[prefix + field] = content["simpleValue"]

        if "messageValue" in content:
            new_prefix = prefix + field + "."
            message_fields2flat_dict(content["messageValue"], flat_list, new_prefix)

        if "listValue" in content:
            list_values = content["listValue"]["values"]
            for i in range(0, len(list_values)):
                new_prefix = prefix + field + "."
                message_fields2flat_dict({"fields": {str(i): list_values[i]}}, flat_list, new_prefix)


# Converts message body tree structure
# parameters are: message object
# max: maximum messages to retrieve
# result: dictionary representing body in flat format
def message2dict(message):
    result = {}
    message_fields2flat_dict(message["body"], result, "")
    return result


def extract_time_for_print(m):
    return misc_utils.extract_time_string(m["timestamp"])


def print_message(m):
    print(extract_time_for_print(m), " > ", m["sessionId"], " ", m["direction"], " ", m["messageType"], " ", message2dict(m))


def get_raw_body_str(m):
    my_bytes = base64.b64decode(m["bodyBase64"].encode('ascii'))
    my_bytes = my_bytes.replace(b'\x01', b'.')

    raw_body = my_bytes.decode('ascii')
    return raw_body


def print_message_raw_source(m):
    raw_body = get_raw_body_str(m)
    print(extract_time_for_print(m), " > ", m["sessionId"], " ", m["direction"], " ", m["messageType"], " ", raw_body)


# Resolves set of message IDs
# parameters are: iterable messages object
# ids_set: set of messages IDs to resolve
# result: resolved IDs removed from set
def resolve_count_message_ids_set(messages, ids_set):
    for m in messages:
        if m["messageId"] in ids_set:
            ids_set.remove(m["messageId"])


# Resolves set of message IDs
# parameters are: iterable messages object
# ids_set: set of messages IDs to resolve
# result: dictionary {message_id: message object}, resolved IDs removed from set
def resolve_message_ids_set(messages, ids_set):
    result = {}
    for m in messages:
        if m["messageId"] in ids_set:
            result[m["messageId"]] = m
            ids_set.remove(m["messageId"])
    return result


def get_category_frequencies(messages, categories_list, categorizer,
                             aggregation_level="seconds", messages_filter=None):
    return misc_utils.get_objects_frequencies(messages,categories_list,categorizer,
                                              lambda m: m["timestamp"]["epochSecond"],
                                              aggregation_level=aggregation_level,
                                              object_expander=expand_message,
                                              objects_filter=messages_filter)


def print_category_frequencies(messages, categories_list, categorizer,
                               aggregation_level="seconds", messages_filter=None, return_html=False):
    result = get_category_frequencies(messages,
                                      categories_list,
                                      categorizer,
                                      aggregation_level,
                                      messages_filter=messages_filter)

    if return_html:
        return tabulate(result, headers="firstrow", tablefmt="html")
    else:
        print(tabulate(result, headers="firstrow", tablefmt="grid"))
        return None


def get_messages_examples(messages, category_list, categorizer, filter=None):
    result = {}
    cat_set = set(category_list)
    for mess in messages:
        me = expand_message(mess)
        for m in me:
            if filter is not None and not filter(m):
                continue
            c = categorizer(m)
            if c in cat_set:
                if c not in result:
                    result[c] = m
                    if len(result) == len(category_list):
                        return result

    return result
