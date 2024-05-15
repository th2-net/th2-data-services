import os
from typing import Iterable, Any

from th2_data_services.data import Data
from th2_data_services.interfaces import IStreamAdapter


class Multiply(IStreamAdapter):
    def __init__(self, multiplier):
        self.multiplier = multiplier

    def handle(self, stream: Iterable) -> Any:
        m: dict
        for m in stream:
            for x in range(self.multiplier):
                new = m.copy()
                new["eventId"] += str(x)
                new["eventName"] += str(x)
                new["eventName"] += str(x)
                yield new


def reads_all_json_files_from_the_folder(path, return_list=False) -> Data:
    # TODO -- add files templates e.g. only  *.py files
    datas = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            datas.append(Data.from_json(file_path, gzip=True, buffer_limit=250))

    if return_list:
        return datas
    if len(datas) == 1:
        return datas[0]
    else:
        return Data(datas)


data_template = {
    "batchId": None,
    "eventId": "84db48fc-d1b4-11eb-b0fb-199708acc7bc",
    "eventName": "some event name that will have +1 every new one",
    "eventType": "Test event",
    "isBatched": False,
    "parentEventId": None,
    "body": {
        "a": 1,
        "b": [1, 2, 3],
        "c": {"x": 1, "y": 2},
        "d": 4,
    },
}
