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

from typing import List, Dict

from th2_data_services.config import options
from th2_data_services.utils.converters import flatten_dict
from th2_data_services.utils.event_utils import event_utils
from datetime import datetime
import th2_data_services.utils.json_tree

# TODO
#   1. Takes flat_list to put result in this dict.
#   It's better to create this dict inside and return as a result.
#   Now don't return anything!
from th2_data_services.utils.viewer_structs.verification import (
    verification_fields_to_flat_dict,
    verification_fields_to_simple_dict,
    simplify_body_verification,
)


def tag_rows_to_flat_dict(collection: Dict, flat_list: Dict, prefix: str) -> None:  # noqa
    """

    rows are used in 'Tree table', 'Table'  but not in the Verification (uses fields)

    Args:
        collection: 'Tree table' or 'Table'
        flat_list: NOT a list - dict. Used just to put result to this object.
        prefix:

    Returns:

    """
    rows: dict = collection["rows"]
    # tag - field name
    for tag, row in rows.items():
        if row["type"] == "row":
            # TODO: Remove comment?
            # flat_list[prefix+tag] = row["columns"]["fieldValue"]
            columns_values = [str(column) for column in row["columns"].values()]
            flat_list[prefix + tag] = ",".join(columns_values)
        if row["type"] == "collection":
            new_prefix = f"{prefix}{tag}."
            tag_rows_to_flat_dict(row, flat_list, new_prefix)


# TODO - looks really strange that we use space before '#' in such strings
#   REQUIRE CLARIFICATION
def item_status_fail(str_irem) -> bool:  # noqa
    # TODO: Add docstrings
    if len(str_irem) < 2:
        return False
    if str_irem[1] == "#":
        return True

    return False


############################
# Simplify functions set  [start]
###########################
#


def simplify_body_outgoing_message(body) -> Dict:  # noqa
    # TODO: Add docstrings
    simple_form = {}
    tree = body[0]
    tag_rows_to_flat_dict(tree, simple_form, "")
    return simple_form


# TODO - do we really have to iterate over tree_table(body) like a list?
#   Why do we expect that it'll be a list?
def simplify_body_tree_table_list(body) -> Dict:  # noqa
    # TODO: Add docstrings
    simple_form = {}
    for element in body:
        tag_rows_to_flat_dict(element, simple_form, "")
    return simple_form


############################
# Simplify functions set  [end]
###########################


def enrich_events_tree_with_attached_messages(index, messages, filter_lambda) -> Dict:  # noqa
    # This function expects the message will be without list in the body.
    #     So expected message format is:
    #         {
    #         ..
    #         body: {fields: {}, metadata: {}}
    #         }
    # TODO: Add docstrings
    resolved_messages = {}
    leaves = []
    for name, leaf in index.items():
        if filter_lambda(name, leaf):
            if "attachedMessageIds" in leaf["info"]:
                leaves.append(leaf)
                for msg_id in leaf["info"]["attachedMessageIds"]:
                    resolved_messages[msg_id] = {}

    print("Messages to resolve: ", len(resolved_messages))
    print("Leaves to update: ", len(leaves))

    for m in messages:
        if m["messageId"] in resolved_messages:
            resolved_messages[m["messageId"]] = (
                flatten_dict(options.MESSAGE_FIELDS_RESOLVER.get_body(m)),
                m["bodyBase64"],
            )

    for leaf in leaves:
        raw_messages = []
        for i in range(0, len(leaf["info"]["attachedMessageIds"])):
            leaf["message " + str(i)] = resolved_messages[leaf["info"]["attachedMessageIds"][i]][0]
            raw_messages.append(resolved_messages[leaf["info"]["attachedMessageIds"][i]][1])
        leaf["info"]["raw"] = raw_messages


def find_child_by_type(leaf: Dict, type: str) -> List:  # noqa
    """Finds child by type.

    Args:
        leaf: Child leaf
        type: Type to match

    Returns:
        List
    """
    result = []
    for name, child in leaf.items():
        if "info" in child:
            if child["info"]["type"] == type:
                result.append((name, child))

    return result


def find_child_by_types(leaf, types):
    """Finds child by type.

    Args:
        leaf: Child leaf
        types: List of types to match

    Returns:
        List
    """
    result = []
    for name, child in leaf.items():
        if "info" in child:
            if child["info"]["type"] in types:
                result.append((name, child))

    return result


# TODO: Should it be in this file, or perhaps misc?
def id_tags() -> List[str]:  # noqa
    return [
        "ClOrdID",
        "OrigClOrdID",
        "NegotiationID",
        "QuoteRespID",
        "QuoteID",
        "OrderID",
        "TrdMatchID",
        "IOIID",
        "QuoteReqID",
        "RegulatoryTradeID",
        "QuoteMsgID",
        "TradeReportID",
        "ClientOrderID",
        "OriginalClientOrderID",
    ]


# TODO: Should it be in this file, or perhaps misc?
def defining_tags() -> List[str]:  # noqa
    return [
        "OrdStatus",
        "ExecType",
        "header.MsgType",
        "LeavesQty",
        "QuoteRespType",
        "QuoteStatus",
        "QuoteType",
        "CxlRejReason",
        "Text",
        "IOITransType",
        "QuoteRequestRejectReason",
        "TrdRptStatus",
        "OrderStatus",
        "header.MessageType",
        "LeavesQuantity",
        "ReasonText",
    ]


def format_expected_event(expected_event_str: str, alias_by_id: Dict) -> str:  # noqa
    # TODO: Add docstrings
    for k, v in alias_by_id.items():
        expected_event_str = expected_event_str.replace(k, v)

    return expected_event_str


def format_actual_event(actual_message_dict, actual_message_str, alias_by_id):  # noqa
    # TODO: Add docstrings
    updated_str = actual_message_str
    for k in id_tags():
        if k in actual_message_dict:
            v = actual_message_dict[k]
            if v in alias_by_id:
                v = alias_by_id[v]
            updated_str += ", {0}={1}".format(k, v)

    for k in defining_tags():
        if k in actual_message_dict:
            updated_str += ", {0}={1}".format(k, actual_message_dict[k])

    return updated_str


def find_corresponding_missing_filter(expectation_string, verifications_list):  # noqa
    # TODO: Add docstrings

    for item in verifications_list:
        if item[1]["info"]["type"] != "Filter":
            continue

        found = True
        keys_found = 0
        tags = item[1]["body"]
        for k, v in tags.items():
            if "EQUAL" not in v:
                continue
            if "True" not in v:
                continue

            keys_found = keys_found + 1
            stripped_val = v[v.index("'") + 1 : v.rindex("'")]
            if "." in k:
                if k[k.rindex(".") + 1 :] + "=" + stripped_val not in expectation_string:
                    found = False
                    break
            elif k + "=" + stripped_val not in expectation_string:
                found = False
                break
        if keys_found == 0 and "=" not in expectation_string:
            return item
        if found and keys_found > 0:
            return item

    return None


def find_corresponding_verification(
    expectation_string, verifications_list, already_used_verifications_set
):  # noqa
    # TODO: Add docstrings
    for item in verifications_list:
        found = True
        keys_found = 0
        if item[0] in already_used_verifications_set:
            continue
        tags = item[1]["body"]
        # print(expectation_string)
        for k, v in tags.items():
            if v[0] == "!":
                keys_found = keys_found + 1
                stripped_val = v[3 : v.index("[") - 1]
                # print(k, "=", v, "=", stripped_val)
                if "." in k:
                    if k[k.rindex(".") + 1 :] + "=" + stripped_val not in expectation_string:
                        found = False
                        break
                elif k + "=" + stripped_val not in expectation_string:
                    found = False
                    break
        if keys_found == 0 and "=" not in expectation_string:
            return item
        if found and keys_found > 0:
            return item
    return None


def process_step_request_id(request_tags, alias_by_id, custom_id_tags):  # noqa
    # TODO: Add docstrings
    request_id = ""
    for k in custom_id_tags:
        if k in request_tags:
            v = request_tags[k]
            if len(v) < 3:
                # very short value
                if request_id != "":
                    request_id += ","
                request_id += k + "=" + v
                continue
            if v in alias_by_id:
                alias = alias_by_id[v]
            else:
                alias = "R" + str(len(alias_by_id) + 1)
                alias_by_id[v] = alias
            if request_id != "":
                request_id += ","
            request_id += k + "=" + alias

    return request_id


def get_val_from_verification(formatted_val):  # noqa
    # TODO: Add docstrings
    value = formatted_val[3:]
    if " [" in value:
        value = value[: value.index(" [")]
    return value


def extract_ids_from_dict(
    fields, is_this_request, is_this_verification, custom_id_tags, r_result, i_result
):  # noqa
    # TODO: Add docstrings
    for id_field in custom_id_tags:
        if id_field in fields:
            v = fields[id_field]
            if is_this_verification:
                v = get_val_from_verification(v)
            if len(v) > 3:
                if (v not in r_result) and (v not in i_result):
                    if is_this_request:
                        alias = "O" + str(len(r_result) + 1)
                        r_result[v] = alias
                    else:
                        alias = "I" + str(len(i_result) + 1)
                        i_result[v] = alias


def matrix_model_test_case_analyze_ids(report_leaf, custom_id_tags):  # noqa
    # TODO: Add docstrings
    r_result = {}
    i_result = {}
    for step_name, step_leaf in report_leaf.items():
        if step_name in ["info", "body"]:
            continue
        if "multiSendMessage" in step_name:
            messages = find_child_by_type(step_leaf, "Outgoing message")
            for sub_step_name, sub_step in messages:
                extract_ids_from_dict(
                    sub_step["body"], True, False, custom_id_tags, r_result, i_result
                )
        if "place" in step_name:
            outgoing = find_child_by_type(step_leaf, "Outgoing message")
            if len(outgoing) != 0:
                extract_ids_from_dict(
                    outgoing[0][1]["body"], True, False, custom_id_tags, r_result, i_result
                )
            for sub_leaf_name, sub_leaf in step_leaf.items():
                if "response" in sub_leaf_name and "Received" in sub_leaf_name:
                    extract_ids_from_dict(
                        sub_leaf["body"], False, False, custom_id_tags, r_result, i_result
                    )
        if "Check sequence rule" in step_name:
            actual_messages_leaf = find_child_by_type(step_leaf, "preFiltering")[0][1]
            for v, v_leaf in actual_messages_leaf.items():
                if v in ["info", "body"]:
                    continue
                extract_ids_from_dict(
                    v_leaf["body"], False, True, custom_id_tags, r_result, i_result
                )

    result = {}
    result.update(r_result)
    result.update(i_result)
    return result


def matrix_model_test_case_processor(report_leaf):  # noqa
    # TODO: Add docstrings
    customization_dict = None  # TODO: What is customization_dict?
    custom_id_tags = []
    if customization_dict is not None and "id_tags" in customization_dict:
        custom_id_tags = customization_dict["id_tags"]
    else:
        custom_id_tags = id_tags()

    requests = []
    alias_by_id = matrix_model_test_case_analyze_ids(report_leaf, custom_id_tags)
    check_rules = []
    for step_name, step_leaf in report_leaf.items():
        if step_name in ["info", "body"]:
            continue
        if "place" in step_name:
            outgoing = find_child_by_type(step_leaf, "Outgoing message")
            if len(outgoing) == 0:
                print("Error in place order Event")
                print(report_leaf["info"]["name"])
                print(step_name)
                message = {"body": {}}
            else:
                message = outgoing[0][1]

            more_info = {}
            if "[fail]" in step_name:
                more_info["fail"] = True
            request_data = {
                "REQ_MORE_INFO": more_info,
                "REQ_orig_name": step_name,
                "REQ_id": process_step_request_id(message["body"], alias_by_id, custom_id_tags),
                "REQ_event": step_leaf["info"]["id"],
            }

            for sub_leaf_name, sub_leaf in step_leaf.items():
                if sub_leaf_name in ["info", "body"]:
                    continue
                if sub_leaf["info"]["type"] in ["Send message", "Outgoing message"]:
                    continue
                if sub_leaf["info"]["type"] == "message":
                    more_info["response"] = sub_leaf["body"]
                    continue
                more_info[sub_leaf_name] = sub_leaf

            request_data.update(message["body"])
            request_data["TH2_event"] = step_leaf["info"]["id"]
            requests.append(request_data)
        if "multiSendMessage" in step_name:
            messages = find_child_by_type(step_leaf, "Outgoing message")
            for sub_step_name, sub_step in messages:
                request_data = {
                    "REQ_orig_name": sub_step_name,
                    "REQ_id": process_step_request_id(
                        sub_step["body"], alias_by_id, custom_id_tags
                    ),
                    "TH2_event": sub_step["info"]["id"],
                }
                request_data.update(sub_step["body"])
                requests.append(request_data)
        if "Check sequence rule" in step_name:
            actual_messages_leaf = find_child_by_type(step_leaf, "preFiltering")[0][1]
            check_rule_actual_messages = []
            for v, v_leaf in actual_messages_leaf.items():
                if v in ["info", "body"]:
                    continue

                check_rule_actual = {"TH2_event": v_leaf["info"]["id"]}
                if "attachedMessageIds" in v_leaf["info"]:
                    check_rule_actual["EVN_attached_msg_id"] = v_leaf["info"]["attachedMessageIds"][
                        0
                    ]
                for tag, val in v_leaf["body"].items():
                    check_rule_actual[tag] = get_val_from_verification(val)
                check_rule_actual_messages.append(check_rule_actual)

            i_summary = 0
            i_extra = 0
            sequence_leaf = find_child_by_type(step_leaf, "checkSequence")[0][1]
            expected_leaf = find_child_by_type(step_leaf, "checkMessages")[0][1]
            verifications = find_child_by_types(expected_leaf, ["Verification", "Filter"])
            matched_messages_ids = set()
            for v in verifications:
                if "attachedMessageIds" in v[1]["info"]:
                    for m_id in v[1]["info"]["attachedMessageIds"]:
                        matched_messages_ids.add(m_id)

            summary = {}
            already_used_verifications = set()
            for r in sequence_leaf["body"][1]["rows"]:
                i_summary = i_summary + 1
                if r["expectedMessage"] != "" and r["actualMessage"] != "":
                    ver = find_corresponding_verification(
                        r["expectedMessage"], verifications, already_used_verifications
                    )
                    if ver is None:
                        match_status = " [??]"
                    else:
                        match_status = " [ok]" if "[ok]" in ver[0] else " [fail]"
                        already_used_verifications.add(ver[0])

                    summary_key = (
                        str(i_summary)
                        + match_status
                        + " Match "
                        + format_expected_event(r["expectedMessage"], alias_by_id)
                    )
                    if ver is None:
                        summary[summary_key] = {
                            "#Error": "Cant find corresponding verification",
                            "#ExpectedMessage": r["expectedMessage"],
                        }
                    else:
                        summary[summary_key] = ver[1]["body"]
                        summary[summary_key]["TH2_event"] = ver[1]["info"]["id"]
                elif r["expectedMessage"] != "" and r["actualMessage"] == "":
                    missing_key = (
                        str(i_summary)
                        + " [fail] Missing "
                        + format_expected_event(r["expectedMessage"], alias_by_id)
                    )
                    missing_filter = find_corresponding_missing_filter(
                        r["expectedMessage"], verifications
                    )
                    if missing_filter is None:
                        summary[missing_key] = {
                            "#Error": "Cant find corresponding filter",
                            "#ExpectedMessage": r["expectedMessage"],
                        }
                    else:
                        summary[missing_key] = missing_filter[1]["body"]
                        summary[missing_key]["TH2_event"] = missing_filter[1]["info"]["id"]

                elif r["actualMessage"] != "" and r["expectedMessage"] == "":
                    next_extra_found = False
                    while (not next_extra_found) and i_extra < len(check_rule_actual_messages):
                        m_id = check_rule_actual_messages[i_extra]["EVN_attached_msg_id"]
                        if m_id not in matched_messages_ids:
                            next_extra_found = True
                        else:
                            i_extra = i_extra + 1
                    if i_extra < len(check_rule_actual_messages):
                        extra_key = (
                            str(i_summary)
                            + " [fail] Extra "
                            + format_actual_event(
                                check_rule_actual_messages[i_extra], r["actualMessage"], alias_by_id
                            )
                        )
                        summary[extra_key] = check_rule_actual_messages[i_extra]
                        i_extra = i_extra + 1
                    else:
                        extra_key = str(i_summary) + " [fail] Extra " + r["actualMessage"] + "[??]"
                        summary[extra_key] = {"#Error": "Cant find actual message"}

            check_rules.append({"actual_messages": check_rule_actual_messages, "summary": summary})

    result = {"view_instruction": "summary_and_tree", "key_ids": alias_by_id}
    n = 1
    for r in requests:
        str_status = "[ok] "
        if "REQ_MORE_INFO" in r and "fail" in r["REQ_MORE_INFO"] and r["REQ_MORE_INFO"]["fail"]:
            str_status = "[fail] "
        r["view_instruction"] = "table"
        name = r["REQ_orig_name"]
        name = name[name.index("]") + 2 :]
        if " with id:" in name:
            name = name[: name.index(" with id:")]
        result[str(n) + " " + str_status + name + " " + r["REQ_id"]] = r
        n = n + 1

    for cr in check_rules:
        for line in cr["summary"].keys():
            result[str(n) + " " + line[line.index(" ") + 1 :]] = cr["summary"][line]
            cr["summary"][line]["view_instruction"] = "table"
            n = n + 1

    result["TH2_event"] = report_leaf["info"]["id"]
    return result


def generate_generic_tree_and_index(events, parents_filter):  # noqa
    # TODO: Add docstrings
    filtered = events.filter(parents_filter)
    parents = event_utils.get_roots(filtered, 10000)
    if len(parents) == 0:
        raise SystemError("Reports parents not found")

    print("Generating report for: ", len(parents), " parents")
    return generate_generic_tree_and_index_from_parents_list(events, parents)


# TODO
#   1. Hardcoded values -- it's better to move them to function parameters with that values
def generate_generic_tree_and_index_from_parents_list(events, parents):  # noqa
    # TODO: Add docstrings
    tree, index = th2_data_services.utils.json_tree.get_event_tree_from_parent_events(
        events,
        parents,
        depth=10,
        max_children=1000000,
        body_to_simple_processors={
            "Outgoing message": simplify_body_outgoing_message,
            "message": simplify_body_outgoing_message,
            "Verification": simplify_body_verification,
            "Filter": simplify_body_tree_table_list,
        },
    )

    return tree, index


def generate_model_matrix_tree_and_index(events, parents_filter, extra=None):  # noqa
    # TODO: Add docstrings
    tree, index = generate_generic_tree_and_index(events, parents_filter)
    th2_data_services.utils.json_tree.transform_tree(
        index,
        {
            "ModelCase": matrix_model_test_case_processor
            if extra is None
            else extra_post_processor(matrix_model_test_case_processor, extra)
        },
    )
    return tree, index


def generate_matrix_json_report_limited_batches(
    events, reports_path, parents_filter, par_btch_len, extra=None
):  # noqa
    # TODO: Add docstrings
    post_processors = {
        "ModelCase": matrix_model_test_case_processor
        if extra is None
        else extra_post_processor(matrix_model_test_case_processor, extra)
    }

    generate_generic_json_report_limited_batches(
        events, reports_path, parents_filter, par_btch_len, post_processors
    )


def extra_post_processor(main_processor, extra_processor):  # noqa
    # TODO: Add docstrings
    return lambda report_leaf: extra_processor(main_processor(report_leaf))


def generate_generic_json_report_limited_batches(
    events, reports_path: str, parents_filter, par_btch_len, post_processors_dict=None
):  # noqa
    # TODO: Add return value -- paths
    # TODO: Add docstrings
    filtered = events.filter(parents_filter)
    parents = event_utils.get_some(filtered, event_type=None, max_count=10000)
    if len(parents) == 0:
        raise SystemError("Reports parents not found")

    n_steps = (len(parents) // par_btch_len) + 1
    print("Building ", len(parents), "trees in ", n_steps, " steps")
    for i in range(n_steps):
        print("Step", i + 1)
        number_base = i * par_btch_len
        batch_end = (
            (i + 1) * par_btch_len if (i + 1) * par_btch_len < len(parents) else len(parents)
        )
        sublist = parents[number_base:batch_end]
        tree, index = generate_generic_tree_and_index_from_parents_list(events, sublist)
        if post_processors_dict is not None:
            print("Post processing ", datetime.now())
            th2_data_services.utils.json_tree.transform_tree(index, post_processors_dict)
        tree_shtrikh = {}
        for k, v in tree.items():
            if k == "info":
                tree_shtrikh[k] = v
                continue

            if " " not in k:
                print("$$$$ " + k)
            k_shtrikh = str(int(k[: k.index(" ")]) + number_base) + k[k.index(" ") :]
            tree_shtrikh[k_shtrikh] = v

        print("Saving json ", datetime.now())
        th2_data_services.utils.json_tree.save_tree_as_json(
            tree_shtrikh, reports_path, lambda n, l: n
        )


def generate_generic_json_report(events, reports_path: str, parents_filter, one_file=False):  # noqa
    # TODO: Add docstrings
    tree, index = generate_generic_tree_and_index(events, parents_filter)
    th2_data_services.utils.json_tree.save_tree_as_json(
        tree, reports_path, lambda n, l: "all" if one_file else n
    )


def generate_model_matrix_json_report(
    events, reports_path: str, parents_filter, one_file=False
):  # noqa
    # TODO: Add docstrings
    tree, index = generate_model_matrix_tree_and_index(events, parents_filter)

    th2_data_services.utils.json_tree.save_tree_as_json(
        tree, reports_path, lambda n, l: "all" if one_file else n
    )


############################
# PrepareStory and its functions  [end]
###########################


ver_dict = {
    "type": "verification",
    "fields": {
        "Field A": {
            "type": "field",
            "operation": "NOT_EMPTY",
            "status": "PASSED",
            "key": False,
            "actual": "value",
            "expected": "*",
        },
        "Field B": {
            "type": "field",
            "operation": "EQUAL",
            "status": "PASSED",
            "key": True,
            "actual": "2531410",
            "expected": "2531410",
        },
        "Sub message A": {
            "type": "collection",
            "operation": "EQUAL",
            "key": False,
            "actual": "1",
            "expected": "1",
            "fields": {
                "Field C": {
                    "type": "field",
                    "operation": "NOT_EQUAL",
                    "status": "FAILED",
                    "key": False,
                    "actual": "9",
                    "expected": "9",
                }
            },
        },
    },
}

tree_table = {
    "type": "treeTable",
    "name": "tableName",  # this one is optional
    "rows": {
        "Row A with some custom name": {
            "type": "row",
            "columns": {
                "Column 1 with some custom name": "some text (A1)",
                "Column 2": "some text (A2)",
            },
        },
        "Row B with some other name": {
            "type": "collection",
            "rows": {
                "Row BA": {
                    "type": "row",
                    "columns": {
                        "Column 1 with some custom name": "some text (BA1)",
                        "Column 2": "some text (BA2)",
                    },
                },
                "Row BB": {
                    "type": "row",
                    "columns": {
                        "Column 1 with some custom name": "some text (BB1)",
                        "Column 2": "some text (BB2)",
                    },
                },
            },
        },
    },
}


def test_verification_fields_to_flat_dict():  # noqa
    flat_list = {}
    verification_fields_to_flat_dict(
        collection=ver_dict, flat_list=flat_list, prefix="hz", failed_collection=True
    )
    print(flat_list)
    """
    failed_collection=False
    {'hzField A': '   value [*]',
     'hzField B': '!  2531410 [2531410]',
     'hzSub message A.Field C': ' # 9 [9]'}

     failed_collection=True
     {'hzField A': ' # value [*]',
     'hzField B': '!# 2531410 [2531410]',
     'hzSub message A.Field C': ' # 9 [9]'}
    """


def test_verification_fields_to_simple_dict():  # noqa
    flat_list = {}
    verification_fields_to_simple_dict(
        collection=ver_dict, parent=flat_list, failed_collection=True
    )
    print(flat_list)
    """
    failed_collection=False
    {'Field A': '   value [*]',
     'Field B': '!  2531410 [2531410]',
     '# Sub message A': {'Field C': ' # 9 [9]'}}

    failed_collection=True
    {'Field A': ' # value [*]',
     'Field B': '!# 2531410 [2531410]',
     '# Sub message A': {'Field C': ' # 9 [9]'}}
    """


def test_simplify_body_tree_table_list():  # noqa
    # TODO - expects tree_table - like a list
    r = simplify_body_tree_table_list([tree_table])
    print(r)
    """
    {'Row A with some custom name': 'some text (A1),some text (A2)',
     'Row B with some other name.Row BA': 'some text (BA1),some text (BA2)',
     'Row B with some other name.Row BB': 'some text (BB1),some text (BB2)'}
    """


if __name__ == "__main__":
    # test_verification_fields_to_flat_dict()
    test_verification_fields_to_simple_dict()
