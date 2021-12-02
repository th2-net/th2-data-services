from sseclient import Event
from urllib3.exceptions import HTTPError
import json


def adapter_sse(record: Event) -> dict:
    """SSE adapter.

    Args:
        record: SSE Event

    Returns:
        data dict
    """
    if record.event == "error":
        raise HTTPError(record.data)
    if record.event not in ["close", "keep_alive", "message_ids"]:
        record_data = json.loads(record.data)
        return record_data
