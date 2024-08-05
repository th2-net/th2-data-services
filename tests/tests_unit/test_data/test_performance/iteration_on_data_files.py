import os
import time
import random

from th2_data_services.data import Data


def get_iteration_speed():
    n = 10_000
    data = Data([random.randint(1, 100_000) for _ in range(n)])
    directory = "tests/tests_unit/test_data/test_performance/benchmark"
    os.makedirs(directory, exist_ok=True)
    data.to_json_lines(f"{directory}/json0.gz", gzip=True, overwrite=True)
    for i in range(1, 122):
        data = Data([random.randint(1, 100_000) for _ in range(n)])
        data.to_json_lines(f"{directory}/json{i}.gz", gzip=True, overwrite=True)

    data = Data.from_json(f"{directory}/json0.gz", gzip=True)
    for i in range(1, 122):
        data = data + Data.from_json(f"{directory}/json{i}.gz", gzip=True)

    start_time = time.time()
    j = 0
    for _ in data:
        j += 1

    print(f"Number of records: {j}")
    print(f"Time took: {time.time() - start_time} seconds")


if __name__ == "__main__":
    get_iteration_speed()
