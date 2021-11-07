from typing import Union, List


def change_pipeline_message(record: dict) -> Union[List[dict], dict]:
    msg_type = record.get("messageType")
    if not msg_type:
        raise ValueError("Sorry, message doesn't have a messageType field.")

    if "/" not in msg_type:
        return record

    sub_messages = []
    fields = record["body"]["fields"]
    for index, sub_msg in enumerate(fields, start=1):
        split_msg_name = sub_msg.split("-")
        if len(split_msg_name) > 1:
            msg_type, index = "".join(split_msg_name[:-1]), int(split_msg_name[-1])
        else:
            msg_type = sub_msg

        new_record = record.copy()
        metadata = new_record["body"]["metadata"].copy()
        id_field = metadata["id"].copy()

        id_field["subsequence"] = [index]
        metadata["id"] = id_field

        body = {**fields.get(sub_msg).get("messageValue"), "metadata": metadata}
        new_record["body"] = body
        new_record["body"]["metadata"]["messageType"] = msg_type
        new_record["messageType"] = msg_type
        sub_messages.append(new_record)
    return sub_messages
