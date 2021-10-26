def change_pipeline_messages(record):
    if "/" not in record.get("messageType"):
        return record

    sub_messages = []
    fields = record.get("body").get("fields")
    for sub_msg in fields:
        msg_type = sub_msg.split("-")[0]
        new_record = record.copy()
        metadata = new_record["body"]["metadata"].copy()

        body = {**fields.get(sub_msg), "metadata": metadata}
        new_record["body"] = body
        new_record["body"]["metadata"]["messageType"] = msg_type
        new_record["messageType"] = msg_type
        sub_messages.append(new_record)
    return sub_messages
