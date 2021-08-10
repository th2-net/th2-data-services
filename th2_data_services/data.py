from __future__ import annotations

import pickle
import pprint
from itertools import tee
from pathlib import Path
from typing import Generator, List, Union, Iterator, Callable

DataSet = Union[Iterator, Generator[dict, None, None]]


class Data:
    def __init__(self, data: DataSet, workflow: List[Callable] = None, cache=False):
        self._data = data
        self._workflow = [] if workflow is None else workflow
        self._cache_status: bool = cache
        self._len = None

    def __del__(self):
        filename = f"{str(id(self))}.pickle"
        if self.__check_cache(filename):
            path = Path("./").joinpath("temp").joinpath(filename)
            path.unlink(missing_ok=True)

    def __iter__(self) -> DataSet:
        filename = f"{str(id(self))}.pickle"

        if self._cache_status and self.__check_cache(filename):
            working_data = self.__load_file(filename)
            for record in working_data:
                yield record
        else:
            file = None
            if self._cache_status:
                filepath = f"./temp/{filename}"
                file = open(filepath, "wb")

            for record in self.__apply_workflow():
                if file is not None:
                    pickle.dump(record, file)
                yield record

            if file:
                file.close()

    def __len__(self):
        if self._len is not None:
            return self._len
        else:
            self._len = 0
            for i in self:
                self._len += 1
            return self._len

    def __check_cache(self, filename: str) -> bool:
        """Checks whether file exist.

        :param filename: Filename.
        :return: File exists or not.
        """
        path = Path("./").joinpath("temp")
        path.mkdir(exist_ok=True)
        path = path.joinpath(filename)
        return path.is_file()

    def __load_file(self, filename: str) -> Generator[dict, None, None]:
        """Loads records from pickle file.

        :param filename: Filepath.
        :return: Generator records.
        """
        path = Path("./").joinpath("temp").joinpath(filename)
        if not path.is_file():
            raise ValueError(f"{filename} isn't file.")

        if path.suffix != ".pickle":
            raise ValueError(f"File hasn't pickle extension.")

        with open(path.resolve(), "rb") as file:
            while True:
                try:
                    decoded_data = pickle.load(file)
                    yield decoded_data
                except EOFError:
                    break

    def __apply_workflow(self) -> Generator[dict, None, None]:
        """Creates generator records with apply workflow.

        :return: Generator records.
        """
        working_data, self._data = tee(self._data)
        for record in working_data:
            for step in self._workflow:
                if isinstance(record, (list, tuple)):
                    pending_records = record.copy()
                    record.clear()
                    for record_ in pending_records:
                        if step["filter"]:
                            skip_record = not step["callback"](record_)
                            if skip_record:
                                continue
                        else:
                            record_ = step["callback"](record_)
                            if record_ is None:
                                continue
                        record.append(record_)
                else:
                    if step["filter"]:
                        skip_record = not step["callback"](record)
                        if skip_record:
                            record = None
                            break
                    else:
                        record = step["callback"](record)
                        if record is None:
                            break
            if not isinstance(record, (list, tuple)):
                record = [record] if record is not None else []
            for record_ in record:
                yield record_

    def filter(self, callback: Callable) -> Data:
        """Append filter to workflow.

        :param callback: Filter function.
        """
        new_workflow = [*self._workflow.copy(), {"filter": True, "callback": callback}]
        working_data, self._data = tee(self._data)
        return Data(working_data, new_workflow, self._cache_status)

    def map(self, callback: Callable) -> Data:
        """Append transform function to workflow.

        :param callback: Transform function.
        """
        new_workflow = [*self._workflow.copy(), {"filter": False, "callback": callback}]
        working_data, self._data = tee(self._data)
        return Data(working_data, new_workflow, self._cache_status)

    def sift(self, limit: int = None, skip: int = None) -> Generator[dict, None, None]:
        """Skips and limits records.

        :param limit: Limited records.
        :param skip: Skipped records.
        :return: Generator records.
        """
        skipped = 0
        pushed = 0

        for record in self:
            if skip is not None and skipped < skip:
                skipped += 1
                continue
            if limit is not None and pushed == limit:
                break
            yield record
            pushed += 1

    def use_cache(self, status: bool) -> Data:
        """Change status cache.

        :param status: Status.
        """
        if status:
            self._cache_status = True
        else:
            self._cache_status = False

        return self

    def __str__(self):
        s = "------------- Printed first 5 records -------------\n"
        for i in self.sift(limit=5):
            s += pprint.pformat(i) + "\n"
        return s
