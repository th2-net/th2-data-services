from datetime import datetime
from tabulate import tabulate


def print_stats_dict(d: dict):  # noqa
    table = [["category", "count"]]
    total = 0
    for key, value in d.items():
        table.append([key, str(value)])
        total += value

    table.append(["TOTAL", str(total)])
    print(tabulate(table, headers="firstrow", tablefmt="grid"))


def extract_time(data: dict, type_: str = "event") -> str:
    """Extracts Time From TH2-Event/Message.

    Args:
        data (dict): TH2-Event/Message
        type_ (str, optional): Event/Message Identifier. Defaults to 'e'.
                      Aliases: Event - [e, ev, event], Message - [m, msg, message]

    Returns:
        str: "timestampEpoch.nanoSeconds"
    """
    if (type_ := type_.lower()) in ["e", "ev", "event"]:
        key = "startTimestamp"
    elif type_ in ["m", "msg", "message"]:
        key = "timestamp"
    else:
        raise Exception("Unknown Format!")

    timestamp = datetime.fromtimestamp(data[key]["epochSecond"])
    nano_seconds = data["startTimestamp"]["nano"]
    return f"{timestamp.isoformat()}.{nano_seconds}"
