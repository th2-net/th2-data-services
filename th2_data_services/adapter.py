from warnings import warn
from typing import Union, List


def change_pipeline_message(record: dict) -> Union[List[dict], dict]:
    msg_type = record.get("messageType")
    if not msg_type:
        warn("Please note, some messages don't have a messageType field.", stacklevel=3)
        return record

    if "/" not in msg_type:
        return record

    sub_messages = []
    fields = record["body"]["fields"]
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

        body = {**fields.get(sub_msg).get("messageValue"), "metadata": metadata}
        new_record["body"] = body
        new_record["body"]["metadata"]["messageType"] = sub_msg_type
        new_record["messageType"] = sub_msg_type
        new_record["messageId"] = f"{record['messageId']}.{index}"
        sub_messages.append(new_record)
    return sub_messages
