from th2_data_services.data import Data
from time import time
from tabulate import tabulate
import os
from random import randint

# Just for iterating data
def iter_data(data):
    for i in data:
        None


def test_add_data_from_cache_runtime():
    data_lens = [1, 10, 100]
    file_lens = [1, 10, 100]

    for files in file_lens:
        for data_len in data_lens:
            for file in range(files):
                os.makedirs(f"test/test_{files}_files_{data_len}_len", exist_ok=True)
                li = [randint(1, 100) for i in range(data_len)]
                d = Data(li).build_cache(
                    f"test/test_{files}_files_{data_len}_len/test{file}.pickle"
                )

    print("Original Data object")

    li = [[""] + [str(len) + " items" for len in data_lens] + [f"{data_lens[-1]}/{data_lens[0]}"]]

    for files in file_lens:
        li_t = [f"{files} file"]
        for data_len in data_lens:
            d = Data([])
            for file in range(files):
                d = d + Data.from_cache_file(
                    f"test/test_{files}_files_{data_len}_len/test{file}.pickle"
                )

            st = time()
            for k in range(100):
                iter_data(d)
            li_t.append(time() - st)
        li_t.append(li_t[-1] / li_t[1])
        li.append(li_t)
    li_t = [f"{file_lens[-1]}/{file_lens[0]}"] + [
        li[-1][i + 1] / li[1][i + 1] for i in range(len(data_lens))
    ]
    li.append(li_t)

    table = tabulate(li, headers="firstrow", tablefmt="fancy_grid")
    print(table)
    assert True
