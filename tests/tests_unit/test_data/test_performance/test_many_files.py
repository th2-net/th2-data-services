import os
import timeit
from pathlib import Path
from typing import Iterable, Any

# from profilehooks import profile

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
        filename=f"file_all.jsons", gzip=True, overwrite=True
    )


# @profile
def many_files():

    # create_files()
    # create_1_file()
    pass

    data_many_files = reads_all_Pickle_files_from_the_folder(TEST_FILES_PATH)
    data_many_files_datas_list = reads_all_Pickle_files_from_the_folder(
        TEST_FILES_PATH, return_list=True
    )
    print("test")
    files = [str(Path(TEST_FILES_PATH) / f"file_{i}.jsons") for i in range(100)]
    # print(locals())
    # print(timeit.repeat("[x for x in data_many_files]", globals=locals()))
    all_msgs_in_1_filepath = f"file_all.jsons"
    data_all_in_one_file = Data.from_json(all_msgs_in_1_filepath, gzip=True)
    # print(timeit.repeat("[x for x in data_all_in_one_file]", globals=locals()))

    print("just iter")

    # x = data_many_files.map(lambda x: x['eventName']).limit(1)
    x = data_many_files.limit(2)
    y = x.limit(3)
    # x.show()
    # y.show()

    # print(x)
    # print(y)
    # #
    # for m in x:
    #     print("X: " + str(x.workflow._data[0].callback.pushed))
    #     # print(m)
    #     for n in y:
    #         print("\tY limit2: " +str(y.workflow._data[0].callback.pushed))
    #         # print(n)
    #         # print("Y limit3: " +str(y.workflow._data[1].callback.pushed))
    #
    # return

    d1 = Data([1, 2, 3])
    # d2 = d1.filter(lambda x: x == 1 or x == 2)
    # from tests.tests_unit.utils import double_generator
    # d3 = d2.map_stream(double_generator)
    #
    def map_read_failure(e):
        if e != 1:
            return e["a"]

    # print(list(d1.map(map_read_failure)))

    def fun_map(s):
        for m in s:
            raise KeyError
            yield x + "12"

    # print(list(d1.map_stream(fun_map)))
    #
    # for m in d1.map(map_read_failure):
    #     print(m)
    # for m in d2:
    #     print(m)
    # for m in d3:
    #     print(m)

    # return

    # cnt1 = 0
    #
    # for f in files:
    #     iterator = iter_json_gzip_file(f, buffer_limit=0)
    #     for m in iterator():
    #         cnt1 += 1

    # print(cnt1)
    # return
    # cnt2 = 0
    # print(len(data_many_files_datas_list))
    # return
    # for f in data_many_files_datas_list:
    #     for x in f:
    #         cnt2 += 1
    # print(cnt2)
    # print(data_many_files.len)
    # return

    s1 = """
for x in data_many_files:
    pass
    """
    s1_filters = """
for x in data_many_files.filter(lambda x: True).filter(lambda x: True).filter(lambda x: True):
    pass
    """

    s2 = """
for x in data_all_in_one_file.filter(lambda x: True):
    pass
    """

    print(files)
    s3 = f"""
for f in files:
    iterator = iter_json_gzip_file(f, buffer_limit=0)
    for m in iterator():
        pass
        """
    s4 = f"""
iterator = iter_json_gzip_file(all_msgs_in_1_filepath)
for m in iterator():
    pass
    """
    s5_iterate_every_data_file_separatelly = f"""
for f in data_many_files_datas_list:
    for x in f.filter(lambda x: True):
        pass
    """

    print(timeit.repeat(s2, globals=locals(), repeat=2, number=1))
    print(timeit.repeat(s1, globals=locals(), repeat=5, number=1))
    print(timeit.repeat(s1_filters, globals=locals(), repeat=5, number=1))
    # print(timeit.repeat(s5_iterate_every_data_file_separatelly, globals=locals(), repeat=2, number=1))
    # print(timeit.repeat(s3, globals=locals(), repeat=2, number=1))
    # print(timeit.repeat(s4, globals=locals(), repeat=2, number=1))


# many_files()
