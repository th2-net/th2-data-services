#  Copyright 2022 Exactpro (Exactpro Systems Limited)
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

from warnings import warn
from typing import Union, List


def adapter_provider5(record: dict) -> Union[List[dict], dict]:
    """Provider 5 adapter.

    Args:
        record: Th2Message dict.

    Returns:
        Th2Message dict.
    """
    msg_type = record.get("messageType")
    if not msg_type:
        warn(
            "Please note, some messages don't have a messageType field. Perhaps a codec doesn't decode some messages.",
            stacklevel=3,
        )
        return record

    if "/" not in msg_type:
        return record

    body = record["body"]
    if not body:
        return record

    sub_messages = []
    fields = body["fields"]
    if not fields:
        return record

    for sub_msg in fields:
        split_msg_name = sub_msg.split("-")
        if len(split_msg_name) > 1:
            sub_msg_type, index = "".join(split_msg_name[:-1]), int(split_msg_name[-1])
        else:
            index = msg_type.split("/").index(sub_msg) + 1
            sub_msg_type = sub_msg

        new_record = record.copy()

        metadata = new_record["body"]["metadata"].copy()
        id_field = metadata["id"].copy()
        id_field["subsequence"] = [index]
        metadata["id"] = id_field

        body_fields = fields[sub_msg]
        metadata.update(body_fields.get("metadata", {}))

        body = {"metadata": metadata}
        if body_fields.get("messageValue"):
            body = {**body_fields["messageValue"], **body}
        elif body_fields.get("fields"):
            body = {**body_fields["fields"], **body}
        else:
            body = {"fields": {}, **body}

        new_record["body"] = body
        new_record["body"]["metadata"]["messageType"] = sub_msg_type
        new_record["messageType"] = sub_msg_type
        new_record["messageId"] = f"{record['messageId']}.{index}"
        sub_messages.append(new_record)
    return sub_messages
