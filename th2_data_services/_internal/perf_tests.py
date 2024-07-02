#  Copyright 2023-2024 Exactpro (Exactpro Systems Limited)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import sys
from pathlib import Path
import csv
from faker import Faker

from th2_data_services.data import Data
from th2_data_services.utils.time import calculate_time


def _create_csv(filename, rows, cols):
    faker = Faker()
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        header = [f"Column {i + 1}" for i in range(cols)]
        writer.writerow(header)

        for _ in range(rows):
            row = [faker.word() for _ in range(cols)]
            writer.writerow(row)


@calculate_time(return_as_last_value=True)
def _build_cache_file(data_obj: Data, filename):
    ftype = filename.split(".")[-1]
    if ftype == "pickle":
        data_obj.build_cache(filename)
    elif ftype == "jsons":
        data_obj.to_json_lines(filename)
    elif ftype == "gz":
        data_obj.to_json_lines(filename, gzip=True)
    elif ftype == "csv":
        data_obj.to_csv(filename)


def _read_from_cache_file(filename):
    ftype = filename.split(".")[-1]
    if ftype == "pickle":
        return Data.from_cache_file(filename)
    elif ftype == "jsons":
        return Data.from_json(filename)
    elif ftype == "gz":
        return Data.from_json(filename, gzip=True)
    elif ftype == "csv":
        if "header" in filename:
            return Data.from_csv(filename, header_first_line=True)
        return Data.from_csv(filename)


@calculate_time(return_as_last_value=True)
def _iter_data_obj(do: Data):
    for o in do:
        pass


@calculate_time(return_as_last_value=True)
def _iter_data_obj_with_3_filters(do: Data):
    for o in do.filter(lambda x: True).filter(lambda x: True).filter(lambda x: True):
        pass


def _test_xx(data_obj: Data):
    filenames = [
        "cache_test.pickle",
        "cache_test.jsons",
        "cache_test.jsons.gz",
        "cache_test.csv",
        "cache_test_header.csv",
    ]
    name_to_option = {"cache_test_header.csv": "header_first_line=True"}

    try:
        # data_obj.use_cache()
        do_len = data_obj.len

        print("Store cache files for test:")
        for filename in filenames:
            print(f"  -> {filename}", end="")
            val, calc_time = _build_cache_file(data_obj, filename)
            print(f"  --  {calc_time} s")

        print()
        print(f"Data length: {do_len}")
        for filename in filenames:
            suffix = name_to_option.get(filename, "")
            if suffix:
                suffix = f" ({suffix})"
            print(f"Iterate {'.'.join(filename.split('.')[1:])}{suffix}:", end="")
            data_obj_file = _read_from_cache_file(filename)
            _, calc_time = _iter_data_obj(data_obj_file)
            print(f"  --  {calc_time} s", end="")
            _, calc_time = _iter_data_obj_with_3_filters(data_obj_file)
            print(f", with 3 filters  --  {calc_time} s")

        print()

    except:
        print("\nException")
        print("Remove cache files")
        for filename in filenames:
            p = Path(filename)
            p.unlink(missing_ok=True)

        raise

    else:
        for filename in filenames:
            p = Path(filename)
            p.unlink(missing_ok=True)


@calculate_time
def cache_files_reading_speed(data):  # noqa
    if isinstance(data, Data):
        _test_xx(data)

    elif isinstance(data, str):
        if data.endswith(".pickle"):
            data_obj = Data.from_cache_file(data)
            _test_xx(data_obj)

        elif data.endswith(".jsons"):
            data_obj = Data.from_json(data)
            _test_xx(data_obj)

        elif data.endswith(".gz"):
            data_obj = Data.from_json(data, gzip=True)
            _test_xx(data_obj)

        elif data.endswith(".csv"):
            data_obj = Data.from_csv(data)
            _test_xx(data_obj)


if __name__ == "__main__":

    if len(sys.argv) > 1:
        """
        python -m th2_data_services._internal.perf_test FILE_FOR_DATA_OBJ
        """
        arg = sys.argv[1]
        cache_files_reading_speed(arg)
    else:
        # cache_files_reading_speed()
        # cache_files_reading_speed(
        #     data=Data([1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
        # )
        # cache_files_reading_speed(
        #     data=Data.from_cache_file(
        #         "C:/Users/admin/exactpro/prj/th2/pickles/cache_2.5kk_events.pickle"
        #     ).limit(5)
        # )

        _create_csv("dataset.csv", 10_000_000, 15)
        cache_files_reading_speed("dataset.csv")

        # cache_files_reading_speed(
        #     "C:/Users/admin/exactpro/prj/th2/pickles/cache_2.5kk_events.pickle"
        # )
