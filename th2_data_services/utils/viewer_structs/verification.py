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

from typing import Dict


def format_comparison_line(field: Dict, failed_collection: bool = False) -> str:  # noqa
    # TODO: Add docstrings
    key_piece = "!" if field["key"] else " "
    status_piece = "? "
    no_val_or_no_group = "no_group" if failed_collection else "no_val"
    if "status" in field:
        status_piece = "# " if field["status"] == "FAILED" else "  "
    expected_piece = (
        f" [{field['expected']}]" if "expected" in field else f" [{no_val_or_no_group}]"
    )
    actual_piece = field["actual"] if "actual" in field else no_val_or_no_group
    return key_piece + status_piece + actual_piece + expected_piece


# TODO
#   1. Takes flat_list to put result in this dict.
#   It's better to create this dict inside and return as a result.
#   Now don't return anything!
#   2. We can move this function to Viewer utils and grouped to VerificationUtil class
#   3. verification_fields_to_simple_dict adds '#' to field name if Failed, but this func - NOT.
#   4. What's the idea of failed_collection ??
def verification_fields_to_flat_dict(
    collection: Dict, flat_list: Dict, prefix, failed_collection: bool = False
):  # noqa
    """
    If a field A has a sub-field B, dot notation sting will be returned.

    Examples:
        failed_collection=False
        {'hzField A': '   value [*]',
         'hzField B': '!  2531410 [2531410]',
         'hzSub message A.Field C': ' # 9 [9]'}

         failed_collection=True
         {'hzField A': ' # value [*]',
         'hzField B': '!# 2531410 [2531410]',
         'hzSub message A.Field C': ' # 9 [9]'}

    Args:
        collection: verification collection like here https://exactpro.atlassian.net/wiki/spaces/TH2/pages/63766549/rpt-viewer+supported+event+content#Verification
        flat_list: NOT a list - dict. Used just to put result to this object.
        prefix: prefix that will be added before each field name.
        failed_collection: ???

    Returns:

    """
    if "fields" not in collection:
        flat_list.update(collection)
        return

    fields = collection["fields"]
    # tag - is field name here.
    for tag, field in fields.items():
        if field["type"] == "field":
            flat_list[prefix + tag] = format_comparison_line(field, failed_collection)
        if field["type"] == "collection":
            next_failed_collection = (
                "status" in field and field["status"] == "FAILED"
            ) or failed_collection
            new_prefix = f"{prefix}{tag}."
            verification_fields_to_flat_dict(field, flat_list, new_prefix, next_failed_collection)


def check_if_verification_leaf_failed(leaf: Dict) -> bool:  # noqa
    # TODO: Add docstrings
    if "fields" not in leaf:
        return False

    fields = leaf["fields"]
    for tag, field in fields.items():
        if field["type"] == "field":
            if "status" not in field:
                return True
            if field["status"] == "FAILED":
                return True
        if field["type"] == "collection":
            if "status" in field and field["status"] == "FAILED":
                return True
            if check_if_verification_leaf_failed(field):
                return True
    return False


# TODO
#   1. Takes parent (like flat_list) to put result in this dict.
#   It's better to create this dict inside and return as a result.
#   Now don't return anything!
#   2. We can move this function to Viewer utils and grouped to VerificationUtil class
#   3. In 'verification_fields_to_flat_dict' we can provide prefix but here - NO!
def verification_fields_to_simple_dict(
    collection: Dict, parent: Dict, failed_collection: bool = False
) -> None:  # noqa
    """

    Examples:
        failed_collection=False
        {'Field A': '   value [*]',
         'Field B': '!  2531410 [2531410]',
         '# Sub message A': {'Field C': ' # 9 [9]'}}

        failed_collection=True
        {'Field A': ' # value [*]',
         'Field B': '!# 2531410 [2531410]',
         '# Sub message A': {'Field C': ' # 9 [9]'}}

    Args:
        collection: verification collection like here https://exactpro.atlassian.net/wiki/spaces/TH2/pages/63766549/rpt-viewer+supported+event+content#Verification
        parent: NOT a list - dict. Used just to put result to this object.
        failed_collection: ??

    Returns:

    """
    if "fields" not in collection:
        parent.update(collection)
        return
    fields = collection["fields"]
    for tag, field in fields.items():
        if field["type"] == "field":
            parent[tag] = format_comparison_line(field, failed_collection)
        if field["type"] == "collection":
            prefix = "# " if check_if_verification_leaf_failed(field) else "  "
            parent[prefix + tag] = {}
            next_failed_collection = "status" in field and field["status"] == "FAILED"
            verification_fields_to_simple_dict(field, parent[prefix + tag], next_failed_collection)


def simplify_body_verification(body) -> Dict:  # noqa
    # Fields -> Simple Dict
    # TODO: Add docstrings
    simple_form = {}
    tree = body[0]
    verification_fields_to_flat_dict(tree, simple_form, "")
    return simple_form


def simplify_body_verification2(body) -> Dict:  # noqa
    # Fields -> Flat Dict
    # Rename to ?
    # TODO: Is this useful?
    # TODO: Add docstrings
    simple_form = {}
    tree = body[0]
    verification_fields_to_simple_dict(tree, simple_form)
    return simple_form
