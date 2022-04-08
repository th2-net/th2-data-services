import copy
import pickle
import pprint
from os import rename
from pathlib import Path
from time import time
from typing import Callable, Dict, Generator, Iterator, List, Optional, Union
from weakref import finalize

DataSet = Union[Iterator, Callable[..., Generator[dict, None, None]]]
WorkFlow = List[Dict[str, Union[Callable, str]]]
DataGenerator = Generator[dict, None, None]


class Data:
    """A wrapper for data/data_stream.

    The class provides methods for working with data as a stream.

    Such approach to data analysis called streaming transformation.
    """

    def __init__(self, data: DataSet, cache: bool = False, workflow: WorkFlow = None, parents_cache: List[str] = None):
        """
        Args:
            data: Data source.
            workflow: Workflow.
            parents_cache: Parents chain. Works as a stack.
            cache: Flag if you want write and read from cache.
        """
        self._cache_filename = f"{str(id(self))}:{time()}.pickle"
        self._len = None
        self._data = data
        self._workflow = [] if workflow is None else workflow
        self._length_hint = None  # The value is populated when we use limit method.
        self._limit_num = None
        self._cache_status = cache
        self._parents_cache = parents_cache if parents_cache else []
        self._finalizer = finalize(self, self.__remove)

    def __remove(self):
        """Data class destructor."""
        if self.__is_cache_file_exists(self._cache_filename):
            self.__delete_cache()
        del self._data

    def __delete_cache(self) -> None:
        """Removes cache file."""
        path = Path(self.__get_cache_filepath())
        path.unlink()

    @property
    def len(self) -> int:
        """int: How many records in the Data stream.

        Notes:
        1. It is a wasteful operation if you are performing it on the Data object that has never been iterated before.

        2. If you want just to check emptiness, use is_empty property instead.
        """
        return self._len if self._len is not None else self.__calc_len()

    @property
    def is_empty(self) -> bool:
        """bool: Indicates that the Data object doesn't contain data."""
        for _ in self.__load_data():
            return False
        return True

    def __calc_len(self) -> int:
        # TODO - request rpt-data-provide provide "select count"
        for _ in self:
            pass
        return self._len

    def __length_hint__(self):
        if self._len is not None:
            return self._len
        elif self._length_hint is not None:
            return self._length_hint
        else:
            # 2**13, though 8 - is a default value in CPython.
            # We usually have large number of data.
            return 8192

    def __iter__(self) -> DataSet:
        self._len = 0
        interruption = True
        try:
            for record in self.__load_data(self._cache_status):
                yield record
                self._len += 1
            else:
                # Loop fell through ..............
                interruption = False
        except StopIteration:
            return None
        finally:
            if interruption:
                if self.__is_cache_file_exists(self._cache_filename):
                    self.__delete_cache()

    def _build_workflow(self, workflow):
        new_workflow = copy.deepcopy(workflow)
        for w in new_workflow[::-1]:
            if w["type"] == "limit":
                w["callback"] = self._build_limit_callback(w["callback"].limit)

        return new_workflow

    def __load_data(self, cache: bool = False) -> DataGenerator:
        """Loads data from cache or data.

        Args:
            cache: Flag if you what write and read from cache.

        Returns:
            obj: Generator
        """
        if cache and self.__is_cache_file_exists(self._cache_filename):
            working_data = self.__load_file(self._cache_filename)
            yield from working_data
        else:
            cache_filename = self.get_last_cache()
            if cache_filename:
                working_data = self.__load_file(cache_filename)
                workflow = self.__get_unapplied_workflow(cache_filename)
            else:
                working_data = self._data() if callable(self._data) else self._data
                workflow = self._workflow

            workflow = self._build_workflow(workflow)

            if self.__check_file_recording():
                # Do not read from the cache file if it has PENDING status (if the file is not filled yet).
                cache = False

            yield from self.__change_data(working_data=working_data, workflow=workflow, cache=cache)

    def __check_file_recording(self) -> bool:
        """Checks whether there is a current recording in the file.

        Returns:
            bool: File recording status.
        """
        filename = f"[PENDING]{self._cache_filename}"
        return self.__is_cache_file_exists(filename)

    def __get_pending_cache_filepath(self) -> str:
        """Gets filepath for a cache file in pending status."""
        return f"./temp/[PENDING]{self._cache_filename}"

    def __get_cache_filepath(self) -> str:
        """Gets filepath for a cache file."""
        return f"./temp/{self._cache_filename}"

    def get_last_cache(self) -> Optional[str]:
        """Returns last existing cache.

        Returns: Cache filename
        """
        for cache_filename in self._parents_cache[::-1]:  # parents_cache works like a stack.
            if self.__is_cache_file_exists(cache_filename):
                return cache_filename
        return None

    def __get_unapplied_workflow(self, cache_filename) -> WorkFlow:
        """Returns list functions which haven't applied.

        Args:
            cache_filename: Cache filename in caches list of parents.

        Returns: Workflow which haven't applied.
        """
        cache_index = self._parents_cache[::-1].index(cache_filename)  # parents_cache works as a stack
        start_workflow = len(self._workflow) - 1 - cache_index  # each child has one more element then parent
        return self._workflow[start_workflow:]

    def __change_data(self, working_data: DataSet, workflow: WorkFlow, cache: bool = False) -> DataGenerator:
        """Applies workflow for data.

        Args:
            working_data: Data for apply workflow.
            workflow: Workflow.
            cache: Set True if you are going to write and read from the cache.

        Yields:
            obj: Generator
        """
        file = None
        if cache:
            filepath = self.__get_pending_cache_filepath()
            file = open(filepath, "wb")

        try:
            limit = False
            for record in working_data:
                modified_records = self.__apply_workflow(record, workflow)
                if modified_records is None:
                    break
                if not isinstance(modified_records, (list, tuple)):
                    modified_records = [modified_records]

                if None in modified_records:
                    limit = True
                    modified_records = modified_records[:-1]

                for modified_record in modified_records:
                    if file is not None:
                        pickle.dump(modified_record, file)
                    yield modified_record
                if limit:
                    break
        finally:
            if file:
                file.close()
                rename(file.name, self.__get_cache_filepath())

    def __is_cache_file_exists(self, filename: str) -> bool:
        """Checks whether file exist.

        Args:
            filename: Filename.

        Returns:
            File exists or not.

        """
        path = Path("./").joinpath("temp")
        path.mkdir(exist_ok=True)
        path = path.joinpath(filename)
        return path.is_file()

    def __load_file(self, filename: str) -> DataGenerator:
        """Loads records from pickle file.

        Args:
            filename: Filepath.

        Yields:
            obj: Generator records.

        """
        path = Path("./").joinpath("temp").joinpath(filename)
        if not path.exists():
            raise ValueError(f"{filename} doesn't exist.")

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

    def __apply_workflow(self, record: dict, workflow: WorkFlow) -> Optional[Union[dict, List[dict]]]:
        """Creates generator records with apply workflow.

        Returns:
            obj: Generator records.

        """
        for step in workflow:
            if isinstance(record, (list, tuple)):
                result = []
                for r in record:
                    try:
                        compute = step["callback"](r)
                        if compute is not None:
                            if not isinstance(compute, list):
                                compute = [compute]
                            result += compute
                    except StopIteration as e:
                        return [*result, None] if result else None

                record = result
                if not record:
                    record = None
                    break
            else:
                try:
                    record = step["callback"](record)
                except StopIteration as e:
                    return None
                if record is None:
                    break

        if record is None:
            record = []
        return record

    def filter(self, callback: Callable) -> "Data":
        """Append `filter` to workflow.

        Args:
            callback: Filter function.
                This function should return True or False.
                If function returns False, the record will be removed from the dataflow.

        Returns:
            Data: Data object.

        """
        new_workflow = [
            *self._workflow.copy(),
            {"type": "filter", "callback": lambda record: record if callback(record) else None},
        ]
        new_parents_cache = [*self._parents_cache, self._cache_filename]
        return Data(data=self._data, workflow=new_workflow, parents_cache=new_parents_cache)

    def map(self, callback: Callable) -> "Data":
        """Append `transform` function to workflow.

        Args:
            callback: Transform function.

        Returns:
            Data: Data object.

        """
        new_workflow = [*self._workflow.copy(), {"type": "map", "callback": callback}]
        new_parents_cache = [*self._parents_cache, self._cache_filename]
        return Data(data=self._data, workflow=new_workflow, parents_cache=new_parents_cache)

    def _build_limit_callback(self, num):
        def callback(r):
            if callback.pushed < num:
                callback.pushed += 1
                return r
            else:
                callback.pushed = 0
                raise StopIteration

        callback.limit = num
        callback.pushed = 0
        return callback

    def limit(self, num: int) -> "Data":
        """Limits the stream to `num` entries.

        Args:
            num: How many records will be provided.

        Returns:
            Data: Data object.

        """

        nwf = []
        for step in copy.deepcopy(self._workflow):
            if step["type"] == "limit":
                step["callback"] = self._build_limit_callback(step["callback"].limit)

            nwf.append(step)

        new_workflow = [*nwf, {"type": "limit", "callback": self._build_limit_callback(num)}]
        new_parents_cache = [*self._parents_cache, self._cache_filename]
        data_obj = Data(data=self._data, workflow=new_workflow, parents_cache=new_parents_cache)
        data_obj._length_hint = num
        data_obj._limit_num = num
        return data_obj

    def sift(self, limit: int = None, skip: int = None) -> Generator[dict, None, None]:
        """Skips and limits records.

        Args:
            limit: Limited records.
            skip: Skipped records.

        Yields:
            Generator records.

        """
        skipped = 0
        pushed = 0

        for record in self.__load_data():
            if skip is not None and skipped < skip:
                skipped += 1
                continue
            if limit is not None and pushed == limit:
                break
            yield record
            pushed += 1

    def use_cache(self, status: bool) -> "Data":
        """Change status cache.

        If True all requested data from rpt-data-provider will be saved to cache file.
        Further actions with Data object will be consume data from the cache file.

        Args:
            status(bool): Status.

        Returns:
            Data: Data object.

        """
        self._cache_status = status
        return self

    def find_by(self, record_field, field_values) -> Generator:
        """Get the records whose field value is written in the field_values list.

        When to use:
            You have IDs of some messages and you want get them in the stream and stop searching
            when you find all elements.

        Args:
            record_field: The record field to be searched for in the field_values list.
            field_values: List of elements among which will be searched record[record_field].

        Yields:
            dict: Generator records.

        """
        values_for_find = list(field_values)
        for record in self:
            if values_for_find:
                if record[record_field] in values_for_find:
                    values_for_find.remove(record[record_field])
                    yield record
                else:
                    continue
            else:
                break

    def write_to_file(self, file: str) -> None:
        """Writes the stream data to txt file.

        Args:
            file: Path to file.

        """
        with open(file, "w") as txt_file:
            for record in self:
                txt_file.write(f"{pprint.pformat(record)}\n" + ("-" * 50) + "\n")

    def __str__(self):
        output = "------------- Printed first 5 records -------------\n"
        for index, record in enumerate(self.__load_data()):
            if index == 5:
                break
            output += pprint.pformat(record) + "\n"
        return output

    def __bool__(self):
        for _ in self.__load_data():
            return True
        return False
