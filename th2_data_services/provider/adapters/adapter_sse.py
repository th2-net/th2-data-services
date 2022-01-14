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
        try:
            return json.loads(record.data)
        except json.JSONDecodeError as e:
            raise Exception(f"json.decoder.JSONDecodeError: Invalid json received.\n" f"{e}\n" f"{record.data}")
