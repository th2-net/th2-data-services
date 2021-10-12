import pickle
import pprint
from pathlib import Path
from time import time
from typing import Callable, Dict, Generator, Iterator, List, Optional, Union

DataSet = Union[Iterator, Callable[..., Generator[dict, None, None]]]
WorkFlow = List[Dict[str, Union[Callable, str]]]
DataGenerator = Generator[dict, None, None]


class Data:
    """A wrapper for data/data_stream.

    The class provides methods for working with data as a stream.

    Such approach to data analysis called streaming transformation.

    Attributes:
        data: Data source which you will transform.
        instance_cache: Flag for save cache in pickle-file for each Data instance.
                        It saves on hard disk in folder "temp".
                        Note that cache DOESN'T DELETE after work.
                        Can change its status with the use_cache function.
        stream_cache: Flag for save cache in pickle-file for only Data source.
                        It saves on hard disk in folder "temp".
                        Note that cache DOESN'T DELETE after work.
                        It does not change its status after the class is created.
    """

    def __init__(self, data: DataSet, instance_cache: bool = False, stream_cache: bool = False, workflow: WorkFlow = None, parents_cache: List[str] = None):
        """
        Args:
            data: Data source.
            workflow: Workflow.
            parents_cache: Caches sequence. Works as a stack.
            instance_cache: Flag if you want write and read from cache of Data instance.
            stream_cache: Flag if you want write and read from cache of source.
        """
        self._cache_filename = f"{str(id(self))}:{time()}.pickle"
        self._len = None
        self._data = data
        self._workflow = [] if workflow is None else workflow
        self._len = None
        self._length_hint = None  # The value is populated when we use limit method.
        self._instance_cache = instance_cache
        self._stream_cache = stream_cache
        self._parents_cache = [] if parents_cache is None else parents_cache

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
        try:
            for record in self.__load_data(self._instance_cache, self._stream_cache):
                yield record
                self._len += 1
        except StopIteration:
            return None

    def __load_data(self, instance_cache: bool = False, stream_cache: bool = False) -> DataGenerator:
        """Loads data from instance cache, stream cache or data.

        Args:
            instance_cache: Flag if you what write and read from cache of Data instance.
            stream_cache: Flag if you what write and read from cache of source.

        Returns:
            dict: Generator
        """
        if (instance_cache or stream_cache) and self.__check_cache(self._cache_filename):
            working_data = self.__load_file(self._cache_filename)
            yield from working_data
        else:
            working_data = self._data() if callable(self._data) else self._data
            workflow = self._workflow

            cache_filename = self.get_last_cache()
            if cache_filename:
                working_data = self.__load_file(cache_filename)
                workflow = self.__get_unapplied_workflow(cache_filename)
                if stream_cache:
                    workflow = self._workflow
                    stream_cache = False

            yield from self.__change_data(working_data=working_data, workflow=workflow, instance_cache=instance_cache, stream_cache=stream_cache)

    def get_last_cache(self) -> Optional[str]:
        """Returns last existing cache.

        Returns: Cache filename
        """
        for cache_filename in self._parents_cache[::-1]:  # parents_cache works as a stack
            if self.__check_cache(cache_filename):
                return cache_filename
        return None

    def __get_unapplied_workflow(self, cache_filename) -> WorkFlow:
        """Returns list functions which haven't applied.

        Args:
            cache_filename: Cache filename in caches list of instance.

        Returns: Workflow which haven't applied.
        """
        cache_index = self._parents_cache[::-1].index(cache_filename)  # parents_cache works as a stack
        start_workflow = len(self._workflow) - 1 - cache_index  # each child has one more element then parent
        return self._workflow[start_workflow:]

    def __change_data(self, working_data: DataSet, workflow: WorkFlow, instance_cache: bool = False, stream_cache: bool = False) -> DataGenerator:
        """Applies workflow for data.

        Args:
            working_data: Data for apply workflow.
            workflow: Workflow.
            instance_cache: Flag if you use cache for each instance of class.
            stream_cache: Flag if you use cache only for source data.

        Returns:
            dict: Generator
        """
        stream_file, instance_file = None, None
        if instance_cache:
            filepath = f"./temp/{self._cache_filename}"
            instance_file = open(filepath, "wb")
        if stream_cache:
            stream_cache_name = self._parents_cache[0] if self._parents_cache else self._cache_filename
            filepath = f"./temp/{stream_cache_name}"
            stream_file = open(filepath, "wb")

        try:
            for record in working_data:
                if stream_file is not None:
                    pickle.dump(record, stream_file)
                modified_records = self.__apply_workflow(record, workflow)
                if modified_records is None:
                    break
                if not isinstance(modified_records, (list, tuple)):
                    modified_records = [modified_records]
                for modified_record in modified_records:
                    if instance_file is not None:
                        pickle.dump(modified_record, instance_file)
                    yield modified_record
        finally:
            if instance_file:
                instance_file.close()
            if stream_file:
                stream_file.close()

    def __check_cache(self, filename: str) -> bool:
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
            dict: Generator records.

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

        Yields:
            dict: Generator records.

        """
        for step in workflow:
            if isinstance(record, (list, tuple)):
                record = [r for r in record if step["callback"](r) is not None]
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
        new_workflow = [*self._workflow.copy(), {"type": "filter", "callback": lambda record: record if callback(record) else None}]
        new_parents_cache = [*self._parents_cache, self._cache_filename] if self._instance_cache else self._parents_cache
        if self._stream_cache and not self._parents_cache:
            new_parents_cache = [self._cache_filename]
        return Data(data=self._data, workflow=new_workflow, instance_cache=self._instance_cache, stream_cache=self._stream_cache, parents_cache=new_parents_cache)

    def map(self, callback: Callable) -> "Data":
        """Append `transform` function to workflow.

        Args:
            callback: Transform function.

        Returns:
            Data: Data object.

        """
        new_workflow = [*self._workflow.copy(), {"type": "map", "callback": callback}]
        new_parents_cache = [*self._parents_cache, self._cache_filename] if self._instance_cache else self._parents_cache
        if self._stream_cache and not self._parents_cache:
            new_parents_cache = [self._cache_filename]
        return Data(data=self._data, workflow=new_workflow, instance_cache=self._instance_cache, stream_cache=self._stream_cache, parents_cache=new_parents_cache)

    def limit(self, num: int) -> "Data":
        """Limits the stream to `num` entries.

        Args:
            num: How many records will be provided.

        Returns:
            Data: Data object.

        """

        def callback(r):
            if callback.pushed < num:
                callback.pushed += 1
                return r
            else:
                callback.pushed = 0
                raise StopIteration

        callback.pushed = 0

        new_workflow = [*self._workflow.copy(), {"type": "limit", "callback": callback}]
        new_parents_cache = [*self._parents_cache, self._cache_filename] if self._instance_cache else self._parents_cache
        if self._stream_cache and not self._parents_cache:
            new_parents_cache = [self._cache_filename]
        data_obj = Data(data=self._data, workflow=new_workflow, instance_cache=self._instance_cache, stream_cache=self._stream_cache, parents_cache=new_parents_cache)
        data_obj._length_hint = num
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
        """Change status instance_cache.

        If True all requested data from rpt-data-provider will be saved to instance_cache file.
        Further actions with Data object will be consume data from the instance_cache file.

        Args:
            status(bool): Status.

        Returns:
            Data: Data object.

        """
        self._instance_cache = status
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
