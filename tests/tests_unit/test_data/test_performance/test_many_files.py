import os
from pathlib import Path
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


TEST_FILES_PATH = "perf_files"


def reads_all_Pickle_files_from_the_folder(path, return_list=False) -> Data:
    datas = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            datas.append(Data.from_json(file_path, gzip=True))

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


def create_files():
    """Creates 100 json-lines files"""
    files_path = Path(TEST_FILES_PATH).resolve().absolute()
    files_path.mkdir(exist_ok=True)
    files_num = 100
    file_lines_num = 5000

    for i in range(files_num):
        Data([data_template]).map_stream(Multiply(file_lines_num)).to_json_lines(
            filename=files_path / f"file_{i}.jsons", gzip=True, overwrite=True
        )


def create_1_file():
    """Creates 1 json-lines files"""
    files_path = Path(TEST_FILES_PATH).resolve().absolute()
    files_path.mkdir(exist_ok=True)
    files_num = 100
    file_lines_num = 5000 * files_num

    Data([data_template]).map_stream(Multiply(file_lines_num)).to_json_lines(
        filename=files_path / f"file_all.jsons", gzip=True, overwrite=True
    )


# def test_many_files():
#     # create_files()
#     # create_1_file()
#     data_many_files = reads_all_Pickle_files_from_the_folder(TEST_FILES_PATH)
#     print("test")
#     print(locals())
#     # print(timeit.repeat("[x for x in data_many_files]", globals=locals()))
#     all_msgs_in_1_filepath = Path(TEST_FILES_PATH) / f"file_all.jsons"
#     data_all_in_one_file = Data.from_json(all_msgs_in_1_filepath, gzip=True)
#     # print(timeit.repeat("[x for x in data_all_in_one_file]", globals=locals()))
#
#     print("just iter")
#
#     s1 = """
# for x in data_many_files:
#     pass
#     """
#
#     s2 = """
# for x in data_all_in_one_file:
#     pass
#     """
#
#     files = [str(Path(TEST_FILES_PATH) / f"file_{i}.jsons") for i in range(100)]
#     print(files)
#     s3 = f"""
# for f in files:
#     iterator = iter_json_gzip_file(f)
#     for m in iterator():
#         pass
#         """
#     s4 = f"""
# iterator = iter_json_gzip_file(all_msgs_in_1_filepath)
# for m in iterator():
#     pass
#     """
#
#     # print(timeit.repeat(s1, globals=locals(), repeat=2, number=1))
#     # print(timeit.repeat(s2, globals=locals(), repeat=2, number=1))
#     # print(timeit.repeat(s3, globals=locals(), repeat=2, number=1))
#     # print(timeit.repeat(s4, globals=locals(), repeat=2, number=1))
