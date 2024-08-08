import os
import time
import random

from th2_data_services.data import Data


def get_iteration_speed_plus():
    data = Data.from_json(f"benchmark/json0.gz", gzip=True)
    for i in range(1, 122):
        data = data + Data.from_json(f"benchmark/json{i}.gz", gzip=True)

    _iterate_and_print_stats(data)


def get_iteration_speed_plus_equals():
    data = Data.from_json(f"benchmark/json0.gz", gzip=True)
    for i in range(1, 122):
        data += Data.from_json(f"benchmark/json{i}.gz", gzip=True)

    _iterate_and_print_stats(data)


def get_iteration_speed_list_comprehension():
    data = Data([Data.from_json(f"benchmark/json{i}.gz", gzip=True) for i in range(122)])

    _iterate_and_print_stats(data)


def _generate_data():
    n = 10_000
    data = Data([random.randint(1, 100_000) for _ in range(n)])
    os.makedirs("benchmark", exist_ok=True)
    data.to_json_lines(f"benchmark/json0.gz", gzip=True, overwrite=True)
    for i in range(1, 122):
        data = Data([random.randint(1, 100_000) for _ in range(n)])
        data.to_json_lines(f"benchmark/json{i}.gz", gzip=True, overwrite=True)


def _iterate_and_print_stats(data):
    start_time = time.time()
    j = 0
    for _ in data:
        j += 1

    print(f"Number of records iterated: {j}")
    print(f"Time took: {time.time() - start_time} seconds")


if __name__ == "__main__":
    _generate_data()
    print("get_iteration_speed_plus()")
    get_iteration_speed_plus()
    print("get_iteration_speed_plus_equals()")
    get_iteration_speed_plus_equals()
    print("get_iteration_speed_list_comprehension()")
    get_iteration_speed_list_comprehension()
