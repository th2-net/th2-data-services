#  Copyright 2022-2024 Exactpro (Exactpro Systems Limited)
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

import copy
import csv
from dataclasses import dataclass
import orjson as json
import gc
import pickle
import pprint
from warnings import warn
from functools import partial
from os import rename
from pathlib import Path
from time import time
from typing import (
    Callable,
    Dict,
    Generator,
    List,
    Optional,
    Union,
    Iterable,
    Iterator,
    Any,
    Generic,
)
from weakref import finalize
import types
from inspect import isgeneratorfunction
from typing import TypeVar
from th2_data_services.interfaces.adapter import IStreamAdapter, IRecordAdapter
from th2_data_services.config import options as o
from th2_data_services.utils._json import iter_json_file, iter_json_gzip_file
from th2_data_services.utils._is_sorted_result import IsSortedResult
from th2_data_services.utils.stream_utils.stream_utils import is_sorted
import gzip as gzip_

# LOG import logging

# LOG logger = logging.getLogger(__name__)


# LOG class _DataLogger(logging.LoggerAdapter):
# LOG     def process(self, msg, kwargs):
# LOG         return "Data[%s] %s" % (self.extra["id"], msg), kwargs
from th2_data_services.utils.path_utils import check_if_filename_valid, check_if_file_exists
from deprecated.classic import deprecated


DataIterValues = TypeVar("DataIterValues")
DataGenerator = Generator[DataIterValues, None, None]
DataSet = Union[Iterator, Callable[..., DataGenerator], List[Iterable], Iterable]
WorkFlow = List[Dict[str, Union[Callable, str]]]


def _build_limit_callback(num) -> Callable:
    def callback(r):
        callback.pushed += 1
        if callback.pushed > num:
            raise StopIteration(r)
        else:
            return r

    callback.limit = num
    callback.pushed = 0
    return callback


@dataclass
class WfRecord:
    type: str
    callback: Callable


@dataclass
class WfLimitRecord(WfRecord):
    limit: int


class Workflow:
    def __init__(self):
        """Data object workflow."""
        self._data: List[WfRecord] = []

    def __bool__(self):
        return bool(self._data)

    def __str__(self):
        return f"Workflow({pprint.pformat(self._data)})"

    def __repr__(self):
        return str(self)

    def add(self, wfr: WfRecord):
        """Add callback to workflow.

        Args:
            wfr: WfRecord

        Returns:
            self
        """
        self._data.append(wfr)
        return self

    # def update(self, upd_func: Callable[[List[WfRecord]], List[WfRecord]]):
    #     self._data = upd_func(self._data)

    # def _apply_record(self, record):
    #     for wfr in self._data:
    #         # print(f"apply '{wfr.type}' for '{record}'")
    #         record = wfr.callback(record)
    #         # print(f"\t --> '{record}'")
    #
    #     return record

    def apply_records(self, records):
        """Execute workflow against some stream.

        Args:
            records: some stream.

        Yields:
            workflow-handled records.
        """
        map_chain = records
        for wfr in self._data:
            if wfr.type == "map_stream":
                map_chain = wfr.callback(map_chain)
            else:
                map_chain = map(wfr.callback, map_chain)

        yield from map_chain

    def refresh_limit_callbacks(self):
        """Updates limit callbacks each time when Data object is iterated.

        It used to have the possibility to iterate the same Data object
        several times in the loops.
        """
        for wfr in self._data:
            if isinstance(wfr, WfLimitRecord):
                wfr.callback = _build_limit_callback(wfr.limit)


# TODO
#   Хочется уметь менять состояние дата объекта во время итерации


# def show_message_if_exception_decorator(callback):
#     def wrapper(stream):
#         try:
#             for record in stream:
#                 yield from callback(stream)
#         except Exception:
#             try:
#                 print("Exception during handling the message: \n" f"{pprint.pformat(record)}")
#             except UnboundLocalError:
#                 pass
#
#             raise
#
#     return wrapper


class Data(Generic[DataIterValues]):
    """A wrapper for data/data_stream.

    The class provides methods for working with data as a stream.

    Such an approach to data analysis called streaming transformation.
    """

    def __init__(
        self,
        data: DataSet,
        cache: bool = False,
        pickle_version: int = o.DEFAULT_PICKLE_VERSION,
    ):
        """Data constructor.

        Args:
            data: Data source. Any iterable, Data object or a function that creates generator.
            cache: Set True if you want to write and read from cache.
            pickle_version: Pickle protocol version. Set if using cache.

        """
        if isinstance(data, types.GeneratorType) and cache is False:
            warn(
                "Putted data has a generator type. "
                "Data object will work wrong in non-cache mode because generators "
                "are iterates only once. "
                "Expected data types: Iterator, Callable[..., DataGenerator], List[Iterator]",
                RuntimeWarning,
                stacklevel=2,
            )

        if self._is_iterables_list(data):
            self._data_stream = self._create_data_set_from_iterables(data)
        else:
            self._data_stream = data

        self._id = id(self)
        self._cache_filename = f"{self._id}_{time()}.pickle"
        self._cache_path = Path("temp", self._cache_filename).resolve().absolute()
        self._pending_cache_path = (
            self._cache_path.with_name("[PENDING]" + self._cache_filename).resolve().absolute()
        )
        self._cache_file_obj = None
        self._len = None
        self.workflow = Workflow()

        self._length_hint = None  # The value is populated when we use limit method.
        self._cache_status = cache
        # We use finalize instead of __del__ because __del__ won't be executed sometimes.
        # Read more about __del__ problems here: https://stackoverflow.com/a/2452895
        self._finalizer = finalize(self, self.__remove)
        # LOG         self._logger = _DataLogger(logger, {"id": self._id})
        # It used to indicate the number of current iteration of the Data object.
        # It's required if the same instance iterates several times in for-in loops.
        self.iter_num = 0  # Indicates what level of the loop the Data object is in.
        self._stop_iteration = None
        self._read_from_external_cache_file = False
        self.__metadata = {}
        self._pickle_version = pickle_version  # Default pickle protocol version

    # LOG         self._logger.info(
    # LOG            "New data object with data stream = '%s', cache = '%s' initialized", id(self._data_stream), cache
    # LOG        )

    def __str__(self):
        s = f"Data({id(self)}\n" f"     {self.workflow}\n" f"     metadata={self.metadata})"
        return s

    def __repr__(self):
        return str(self)

    def __bool__(self):
        for _ in self:
            return True
        return False

    def __add__(self, other_data: Iterable) -> "Data":
        """Joining feature.

        Don't keep cache status.

        e.g. data3 = data1 + data2  -- data3 will have cache_status = False.
        """
        data = Data(self._create_data_set_from_iterables([self, other_data]))
        data._set_metadata(self.metadata)
        if isinstance(other_data, Data):
            data.update_metadata(other_data.metadata)
        return data

    def __iadd__(self, other_data: Iterable) -> "Data":
        """Joining feature.

        Keeps cache status.

        e.g. data1 += data2  -- will keep the cache status of data1.
        """
        return self.__add__(other_data).use_cache(self._cache_status)

    def _set_custom_cache_destination(self, filename):
        path = Path(filename).resolve()
        self._cache_filename = path.name
        self._cache_path = path
        self._cache_status = True
        self._read_from_external_cache_file = True

    def _copy_cache_file(self, new_name):
        from shutil import copy2

        copy2(self.get_cache_filepath(), new_name)

    def __copy__(self):
        obj = Data(self._data_stream, pickle_version=self._pickle_version)
        obj._set_metadata(self.metadata)
        obj.workflow = copy.deepcopy(self.workflow)

        return obj

    def __remove(self):
        """Data class destructor."""
        if self.__is_cache_file_exists() and not self._read_from_external_cache_file:
            self.__delete_cache()
        del self._data_stream

    def __delete_cache(self) -> None:
        """Removes cache file."""
        path = self.get_cache_filepath()
        if path.exists():
            # LOG             self._logger.debug("Deleting cache file '%s'" % path)
            path.unlink()

    def __delete_pending_cache(self) -> None:
        """Removes cache file."""
        path = self.get_pending_cache_filepath()
        if path.exists():
            # LOG             self._logger.debug("Deleting cache file '%s'" % path)
            self._cache_file_obj.close()
            path.unlink()

    def _create_data_set_from_iterables(self, iterables_list: List[Iterable]) -> DataSet:
        """Creates a generator from the list of iterables."""
        return partial(self._create_generator_data_source_from_iterables, iterables_list)

    def _create_generator_data_source_from_iterables(
        self, iterables_list: List[Iterable]
    ) -> Generator:
        """Creates a generator from the list of iterables."""
        for data in iterables_list:
            yield from data

    def _is_iterables_list(self, data: DataSet) -> bool:
        if not isinstance(data, (list, tuple)):
            return False
        return all(isinstance(d, Data) for d in data)

    def __calc_len(self) -> int:
        for _ in self:
            pass
        return self._len

    def __length_hint__(self):
        """This hint used by list() to calculate the size of the bytes for the list."""
        if self._len is not None:
            return self._len
        elif self._length_hint is not None:
            return self._length_hint
        else:
            # 2**13, though 8 - is a default value in CPython.
            # We usually have large number of data.
            return 8192

    def _iter_logic(self):
        interruption = True
        if self._cache_status and self.__is_cache_file_exists():
            is_data_writes_cache = False
        else:
            # FIXME -- bug -- мы считаем что мы пишем файл, когда он уже существует а мы его просто читаем
            is_data_writes_cache = True

        try:
            for record in self.__load_data(self._cache_status):
                yield record
            else:
                # Loop successfully finished. Do not delete cache file.
                # LOG                 self._logger.debug("Successfully iterated")
                interruption = False

        finally:
            if interruption:

                if self._stop_iteration:  # When limit was reached.
                    # You can save _len in this case because iteration was stopped by limit.
                    # LOG                     self._logger.info("Iteration was interrupted because limit reached")
                    pass
                else:  # When something went wrong but NOT StopIteration
                    # LOG                     self._logger.info("Iteration was interrupted")
                    # You shouldn't save _len in this case because iteration was interrupted.
                    if self.iter_num == 1:
                        self._len = None

                # Delete cache if it was interrupted and the file was not complete.
                # https://exactpro.atlassian.net/browse/TH2-3546
                # Do not delete cache if iter_num != 1 (loop level > 1).
                if is_data_writes_cache and self.iter_num == 1:
                    # LOG                     self._logger.info("The cache file is not written to the end. Delete tmp cache file")
                    self.__delete_pending_cache()
                else:  # Data reads cache.

                    # Do not delete cache file if it reads an external cache file.
                    if not self._read_from_external_cache_file:
                        # Do not delete cache file if it's an interactive mode and Data has read cache.
                        if not o.INTERACTIVE_MODE:
                            self.__delete_cache()

            self.iter_num -= 1
            self._stop_iteration = False

    def __iter__(self) -> DataGenerator:
        self._stop_iteration = False
        self.iter_num += 1
        # LOG         self._logger.info("Starting iteration, iter_num = %s", self.iter_num)

        if self._len is None and self.iter_num == 1:
            self._len = 0
            for record in self._iter_logic():
                self._len += 1
                yield record
        else:
            # Do not calculate self._len if it is not None.
            yield from self._iter_logic()

    def _build_workflow(self, workflow: Workflow):
        """Updates limit callbacks each time when Data object is iterated.

        It used to have the possibility to iterate the same Data object
        several times in the loops.
        """
        new_workflow = copy.deepcopy(workflow)
        new_workflow.refresh_limit_callbacks()

        return new_workflow

    def _build_data_stream(self):
        return self._data_stream() if callable(self._data_stream) else self._data_stream

    def __load_data(self, cache: bool) -> DataGenerator:
        """Loads data from cache or data.

        Args:
            cache: Flag if you what to write and read from cache.

        Returns:
            obj: Generator
        """
        if cache and self.__is_cache_file_exists():
            # LOG             self._logger.info("Iterating using own cache file '%s'" % self.get_cache_filepath())
            data_stream = self.__load_file(self.get_cache_filepath())
            yield from data_stream
        else:
            data_stream = self._build_data_stream()  # we do it for every iterable data object.
            workflow = self._build_workflow(self.workflow)

            if self.__check_file_recording():
                # Do not read from the cache file if it has PENDING status (if the file is not filled yet).
                # It used to handle case when Data object iterates in the loop several times.
                cache = False

            if workflow:
                iteration_obj = workflow.apply_records(data_stream)
            else:
                iteration_obj = data_stream

            if cache:
                filepath = self.get_pending_cache_filepath()
                filepath.parent.mkdir(exist_ok=True)
                # LOG             self._logger.debug("Recording cache file '%s'" % filepath)
                self._cache_file_obj = open(filepath, "wb")

                for modified_record in iteration_obj:
                    pickle.dump(
                        modified_record, self._cache_file_obj, protocol=self._pickle_version
                    )
                    yield modified_record

                self._cache_file_obj.close()
                rename(self._cache_file_obj.name, str(self.get_cache_filepath()))
            # LOG             self._logger.debug("Cache file was created '%s'" % self.get_cache_filepath())
            else:
                yield from iteration_obj

    def __check_file_recording(self) -> bool:
        """Checks whether there is a current recording in the file.

        Returns:
            bool: File recording status.
        """
        path = self.get_pending_cache_filepath()
        return path.is_file()

    def __is_cache_file_exists(self) -> bool:
        """Checks whether cache file exist."""
        path = self.get_cache_filepath()
        r = path.is_file()
        # LOG         self._logger.debug("Cache file exists" if r else "Cache file doesn't exist")
        return r

    def __load_file(self, filepath: Path) -> DataGenerator:
        """Loads records from pickle file.

        Args:
            filepath: Filepath.

        Yields:
            obj: Generator records.
        """
        if not filepath.exists():
            raise FileNotFoundError(f"{filepath} doesn't exist")

        if not filepath.is_file():
            raise FileExistsError(f"{filepath} isn't file")

        yield from _iter_pickle_file_logic(filepath)
        # with open(filepath, "rb") as file:
        #     while True:
        #         try:
        #             decoded_data = pickle.load(file)
        #             yield decoded_data
        #         except EOFError:
        #             break
        #         except pickle.UnpicklingError:
        #             print(f"Cannot read {filepath} cache file")
        #             raise

    # def _process_step(self, step: dict, record):
    #     res = step["callback"](record)
    #     # LOG         self._logger.debug("    - step '%s' -> %s", step["type"], res)
    #     return res

    # def __apply_workflow(
    #     self, record: Any, workflow: WorkFlow
    # ) -> Optional[Union[dict, List[dict]]]:
    #     """Creates generator records with apply workflow.
    #
    #     Returns:
    #         obj: Generator records.
    #
    #     """
    #     # LOG         self._logger.debug("Apply workflow for %s", record)
    #     for step in workflow:
    #         try:
    #             # TODO -2 -- мы каждый раз делаем step["callback"](record)
    #             # TODO -3 -- по факту мы сейчас не используем воркфлоу, а ка
    #             #  каждый раз создаём новый дата объект
    #             #   у этого есть минусы -- эксепшен с итерациями,
    #             #   и когда много объектов вложены доуг в друга, это медленно работает
    #             record = self._process_step(step, record)
    #             if record is None:
    #                 break  # Break workflow iteration if step result is None.
    #         except StopIteration:
    #             raise
    #
    #     # LOG         self._logger.debug("-> %s", record)
    #     return record

    @property
    def metadata(self):
        return self.__metadata

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
        for _ in self:
            return False
        return True

    @property
    def cache_status(self) -> bool:
        return self._cache_status

    def get_pending_cache_filepath(self) -> Path:
        """Returns filepath for a pending cache file."""
        return self._pending_cache_path

    def get_cache_filepath(self) -> Path:
        """Returns filepath for a cache file."""
        return self._cache_path

    def filter(self, callback: Callable) -> "Data":
        """Append `filter` to workflow.

        Args:
            callback: Filter function.
                This function should return True or False.
                If function returns False, the record will be removed from the dataflow.

        Returns:
            Data: Data object.

        """

        def filter_yield(stream):
            try:
                for record in stream:
                    if callback(record):
                        yield record
            except Exception:
                try:
                    print("Exception during filtering the message: \n" f"{pprint.pformat(record)}")
                except UnboundLocalError:
                    pass

                raise

        new_data = self.map_stream(filter_yield)
        # TODO - rename workflow type map_stream to filter

        return new_data

    def map(self, callback_or_adapter: Union[Callable, IRecordAdapter]) -> "Data":
        """Append `transform` function to workflow.

        Args:
            callback_or_adapter: Transform function or an Adapter with IRecordAdapter
                interface implementation.
                Note:
                    - If the function returns None value, this value will be
                    pushed to the next workflow function.
                    If you want to skip None values -- use `map_stream` instead.

        Returns:
            Data: Data object.

        """
        # LOG         self._logger.info("Apply map")

        new_data = copy.copy(self)

        if isinstance(callback_or_adapter, IRecordAdapter):
            new_data.workflow.add(WfRecord(type="map", callback=callback_or_adapter.handle))
        else:
            new_data.workflow.add(WfRecord(type="map", callback=callback_or_adapter))

        return new_data

    def map_stream(
        self, adapter_or_generator: Union[IStreamAdapter, Callable[..., Generator]]
    ) -> "Data":
        """Append `stream-transform` function to workflow.

        If StreamAdapter is passed StreamAdapter.handle method will be used as a map function.

        Difference between map and map_stream:
        1. map_stream allows you return None values.
        2. map_stream allows you work with the whole stream but not with only 1 element,
            so you can implement some buffers inside handler.
        3. map_stream works slightly efficient (faster on 5-10%).

        Args:
            adapter_or_generator: StreamAdapter object or generator function.

        Returns:
            Data: Data object.

        """
        new_data = copy.copy(self)

        if isinstance(adapter_or_generator, IStreamAdapter) and isgeneratorfunction(
            adapter_or_generator.handle
        ):
            callback = adapter_or_generator.handle

        elif isgeneratorfunction(adapter_or_generator):
            callback = adapter_or_generator

        else:
            raise Exception(
                "map_stream Only accepts IStreamAdapter class with generator function or Generator function"
            )

        new_data.workflow.add(WfRecord(type="map_stream", callback=callback))

        return new_data

        # data = Data(source)
        # data._set_metadata(self.metadata)
        # return data

    def map_yield(self, callback_or_adapter: Union[Callable, IRecordAdapter]) -> "Data":
        """Maps the stream using callback function or adapter.

        Differences between map and map yield:
        1. map_yield is a wrapper function using map_stream.
        2. map_yield iterates over each item in record if callback returns
        a value, which is a list or tuple.

        Args:
            callback_or_adapter: Transform function or an Adapter with IRecordAdapter interface implementation.

        Returns:
            Data: Data object.

        """

        def generator(stream):
            for record in stream:
                modified_record = callback_or_adapter(record)
                if isinstance(modified_record, (list, tuple)):
                    for item in modified_record:
                        yield item
                else:
                    yield modified_record

        return self.map_stream(generator)

    def limit(self, num: int) -> "Data":
        """Limits the stream to `num` entries.

        Args:
            num: How many records will be provided.

        Returns:
            Data: Data object.
        """
        # LOG         self._logger.info("Apply limit = %s", num)
        data_obj = copy.copy(self)
        data_obj.workflow.add(
            WfLimitRecord(type="limit", callback=_build_limit_callback(num), limit=num)
        )
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

        for record in self:
            if skip is not None and skipped < skip:
                skipped += 1
                continue
            if limit is not None and pushed == limit:
                break
            yield record
            pushed += 1

    def is_sorted(self, get_timestamp_func: Callable[[Any], Any]) -> IsSortedResult:
        """Checks whether Data is sorted.

        Args:
            get_timestamp_func: This function is responsible for getting the timestamp.

        Returns:
            IsSortedResult: Whether data is sorted and additional info (e.g. index of the first unsorted element).
        """
        return is_sorted(self, get_timestamp_func)

    def use_cache(self, status: bool = True) -> "Data":
        """Changes cache flag and returns self.

        Args:
            status(bool): If True the whole data stream will be saved to cache file.
            Further actions with the Data object will consume data from the cache file. True by default.

        Returns:
            Data: Data object.

        """
        # LOG         self._logger.info("Cache using activated" if status else "Cache using deactivated")
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

    def show(self, n=5, print_=True):
        print("------------- Printed first 5 records -------------")
        for index, record in enumerate(self):
            if index == n:
                break
            pprint.pprint(record)

    def build_cache(self, filename, pickle_version: Optional[int] = None):
        """Creates cache file with provided name.

        Important:
            If the Data object cache status is True, it'll iterate itself. As a result the cache file
             will be created and copied.
            When you will iterate the Data object next time, it'll iterate created cache file.

            NOTE! If you build cache file, Data.cache_status was False and after that you'll set
             Data.cache_status == TRUE -- the Data object WON'T iterate build file because it doesn't
             keep the path to built cache file..

        Args:
            filename: Name or path to cache file.
            pickle_version: Pickle protocol version. Change the default value
                if you want to create pickle file with another pickle version.

        """
        path_name = Path(filename).name
        status, reason = check_if_filename_valid(path_name)
        if not status:
            raise Exception(f"Cannot build cache file. {reason}")

        if pickle_version is None:
            pickle_version = self._pickle_version

        if self.__is_cache_file_exists():
            self._copy_cache_file(filename)
        else:
            gc.disable()  # https://exactpro.atlassian.net/browse/TH2-4775
            if self._cache_status:
                _ = self.len  # Just to iterate
                self._copy_cache_file(filename)
            else:
                file = open(filename, "wb")

                for record in self:
                    pickle.dump(record, file, protocol=pickle_version)

                file.close()
            gc.enable()

    def clear_cache(self):
        """Clears related to data object cache file.

        This function won't remove external cache file.
        """
        if self._read_from_external_cache_file:
            raise Exception("It's not possible to remove external cache file via this method")
        else:
            if self.__is_cache_file_exists():
                self.__delete_cache()

    @classmethod
    def from_cache_file(cls, filename, pickle_version: int = o.DEFAULT_PICKLE_VERSION) -> "Data":
        """Creates Data object from cache file with the provided name.

        Args:
            filename: Name or path to cache file.
            pickle_version: Pickle protocol version. Change the default value
                if your pickle file was created with another pickle version.

        Returns:
            Data: Data object.

        Raises:
            FileNotFoundError if provided file does not exist.

        """
        check_if_file_exists(filename)

        path = Path(filename).resolve()
        data_obj = cls(_iter_pickle_cache_file(path, pickle_version))
        data_obj.update_metadata({"source_file": path})
        data_obj._pickle_version = pickle_version
        return data_obj

    @classmethod
    def from_json(cls, filename, buffer_limit=250, gzip=False) -> "Data[dict]":
        """Creates Data object from json-lines file with provided name.

        Args:
            filename: Name or path to cache file.
            buffer_limit: If limit is 0 buffer will not be used. Number of messages in buffer before parsing.
            gzip: Set to true if file is json file compressed using gzip.

        Returns:
            Data: Data object.

        Raises:
            FileNotFoundError if provided file does not exist.

        """
        check_if_file_exists(filename)
        if gzip:
            data = cls(iter_json_gzip_file(filename, buffer_limit))
        else:
            data = cls(iter_json_file(filename, buffer_limit))
        data.update_metadata({"source_file": filename})
        return data

    @classmethod
    def from_any_file(cls, filename, mode="r") -> "Data[str]":
        """Creates a Data object from any file with the provided name.

        It will just iterate file and return data line be line.

        Args:
            filename: Name or path to the file.
            mode: Read mode of open function.

        Returns:
            Data: Data object.

        Raises:
            FileNotFoundError if provided file does not exist.

        """
        check_if_file_exists(filename)
        data = cls(_iter_any_file(filename, mode))
        data.update_metadata({"source_file": filename})
        return data

    @classmethod
    def from_csv(
        cls,
        filename: Union[str, Path],
        header=None,
        header_first_line=False,
        mode="r",
        delimiter=",",
    ) -> "Data":
        """Creates Data object from CSV file with the provided name.

        It will iterate the CSV file as if you were doing it with CSV module.

        Args:
            filename: Name or path to the file.
            header: If provided header for csv, Data object will yield Dict[str].
                Note, if your first line is header in csv, it also will be yielded.
            header_first_line: If the first line of the csv file is header,
                it'll take header from the first line. Data object will yield
                Dict[str]. `header` argument is not required in this case.
                First line of the CSV file will be skipped (header line).
            mode: Read mode of open function.
            delimiter: CSV file delimiter.

        Note:
            If `header` provided and `header_first_line == True`,
            Data object will yield Dict[str] where key names (columns) as
            described in the `header`. First line of the CSV file will be skipped.

        Returns:
            Data: Data object.

        Raises:
            FileNotFoundError if provided file does not exist.

        """
        # TODO - bug here TH2-4930 - new data object doesn't work with limit method
        check_if_file_exists(filename)
        data = cls(_iter_csv(filename, header, header_first_line, mode, delimiter))
        data.update_metadata({"source_file": filename})
        return data

    def _set_metadata(self, metadata: Dict) -> None:
        """Set metadata of object to metadata argument.

        Args:
            metadata (dict): New Metadata

        Raises:
            Exception: If metadata isn't dict, error will be raised.
        """
        if not isinstance(metadata, Dict):
            raise Exception("metadata must be dictionary!")

        self.__metadata = copy.deepcopy(metadata)

    def update_metadata(self, metadata: Dict) -> "Data":
        """Update metadata of the object with metadata argument.

        Metadata is updated with new values, meaning previous values are kept and added with new values.

        | Example:
        | data = Data(...)
        | # data.metadata => {'num': 1, 'nums': [1], 'letters': {'a': 97}}
        | new_metadata = {'num': 9, 'nums': [7], 'letters': {'z': 122}, 'new': 'key'}
        | data.update_metadata(new_metadata)
        | # data.metadata => {'num': 9, 'nums': [1,7], 'letters': {'a': 97, 'z': 122}, 'new': 'key'}

        Args:
            metadata (dict): New Metadata

        Returns:
            Data objects (itself)

        Raises:
            Exception: If metadata isn't dict, error will be raised.
            AttributeError: If you're trying to update key value with dict which isn't a dict.
        """
        if not isinstance(metadata, Dict):
            raise Exception("metadata must be dictionary!")

        for k, v in metadata.items():
            if k in self.metadata:
                current = self.metadata[k]
                # Check For Iterable Types
                if isinstance(v, dict):
                    self.__metadata[k].update({**current, **v})
                elif isinstance(v, Iterable) and not (
                    isinstance(v, str) or isinstance(current, str)
                ):
                    if isinstance(current, Iterable):
                        self.__metadata[k] = [*current, *v]
                    else:
                        self.__metadata[k] = [current, *v]
                else:  # Single Item
                    if isinstance(current, Iterable):
                        self.__metadata[k] = [*current, v]
                    else:
                        self.__metadata[k] = v
            else:
                # Add New Item
                self.__metadata[k] = v

        return self

    def to_json(self, filename: Union[str, Path], indent: int = None, overwrite: bool = False):
        """Converts data to valid json format.

        Args:
            filename (str): Output JSON filename
            indent (int, optional): JSON format indent. Defaults to None.
            overwrite (bool, optional): Overwrite if filename exists. Defaults to False.

        NOTE:
            Data object can iterate not only dicts. So not every data can be
            saved as json.

        Raises:
            FileExistsError: If file exists and overwrite=False
        """
        if Path(filename).absolute().exists() and not overwrite:
            raise FileExistsError(
                f"{filename} already exists. If you want to overwrite current file set `overwrite=True`"
            )

        with open(filename, "w", encoding="UTF-8") as file:
            file.write("[")  # Start list
            for record in self:
                # TODO
                (json.dumps(record) + b"\n").decode()
                json.dump(record, file, indent=indent)
                file.write(",\n")
            file.seek(file.tell() - 3)  # Delete last comma for valid JSON
            file.write("]")  # Close list

    @deprecated(
        reason="Use `to_json_lines` instead. " "`to_jsons` will be removed on 2.0.0 release."
    )
    def to_jsons(
        self,
        filename: Union[str, Path],
        indent: int = None,
        overwrite: bool = False,
        gzip=False,
        compresslevel=5,
    ):
        """[DEPRECATED] Converts data to json lines.

        Every line is a valid json, but the whole file - not.

        Args:
            filename (str): Output JSON filename.
            indent (int, optional): DON'T used now.
            overwrite (bool, optional): Overwrite if filename exists. Defaults to False.
            gzip: Set to True if you want to compress the file using gzip.
            compresslevel: gzip compression level.

        Raises:
            FileExistsError: If file exists and overwrite=False
        """
        return self.to_json_lines(filename, indent, overwrite, gzip, compresslevel)

    def to_json_lines(
        self,
        filename: Union[str, Path],
        indent: int = None,
        overwrite: bool = False,
        gzip: bool = False,
        compresslevel: int = 5,
    ):
        """Converts Data to json lines.

        Every line is a valid json, but the whole file - not.

        Args:
            filename (str): Output JSON filename.
            indent (int, optional): DON'T used now.
            overwrite (bool, optional): Overwrite if filename exists. Defaults to False.
            gzip: Set to True if you want to compress the file using gzip.
            compresslevel: gzip compression level.

        NOTE:
            Data object can iterate not only dicts. So not every data can be
            saved as json.

        Raises:
            FileExistsError: If file exists and overwrite=False
        """
        if Path(filename).absolute().exists() and not overwrite:
            raise FileExistsError(
                f"{filename} already exists. If you want to overwrite current file set `overwrite=True`"
            )

        if gzip:
            with gzip_.open(filename, "wb", compresslevel=compresslevel) as f:
                for record in self:
                    f.write(json.dumps(record) + b"\n")
        else:
            with open(filename, "w", encoding="UTF-8") as file:
                for record in self:
                    file.write((json.dumps(record) + b"\n").decode())


def _iter_any_file(filename: Union[str, Path], mode="r"):
    """Returns the function that returns generators."""

    def iter_any_file_logic():
        with open(filename, mode) as data:
            while True:
                try:
                    v = data.readline()
                    if not v:
                        break

                    yield v
                except Exception:
                    print(f"Error string: {v}")
                    raise

    def iter_any_file_wrapper(*args, **kwargs):
        """Wrapper function that allows passing arguments to the generator."""
        return iter_any_file_logic(*args, **kwargs)

    return iter_any_file_wrapper


def _iter_csv(
    filename: Union[str, Path], header=None, header_first_line=False, mode="r", delimiter=","
):
    """Returns the function that returns generators."""

    def iter_logic():
        with open(filename, mode) as data:
            if header is not None and header_first_line:
                reader = csv.DictReader(data, fieldnames=header, delimiter=delimiter)
                next(reader)  # Skip first line with header.
            elif header is not None:
                reader = csv.DictReader(data, fieldnames=header, delimiter=delimiter)
            elif header_first_line:
                reader = csv.DictReader(data, delimiter=delimiter)
            else:
                reader = csv.reader(data, delimiter=delimiter)

            for row in reader:
                yield row

    def iter_wrapper(*args, **kwargs):
        """Wrapper function that allows passing arguments to the generator."""
        return iter_logic(*args, **kwargs)

    return iter_wrapper


def _iter_pickle_file_logic(filepath):
    """Generator that reads and yields decoded JSON objects from a file.

    The protocol version of the pickle is detected automatically,
    so no protocol argument is needed. Bytes past the pickled representation
    of the object are ignored.
    """
    with open(filepath, "rb") as file:
        while True:
            try:
                decoded_data = pickle.load(file)
                yield decoded_data
            except EOFError:
                break
            except pickle.UnpicklingError:
                print(f"Cannot read {filepath} cache file")
                raise


def _iter_pickle_cache_file(filepath: Path, pickle_version: int):
    def iter_json_file_wrapper(*args, **kwargs):
        """Wrapper function that allows passing arguments to the generator."""
        return _iter_pickle_file_logic(filepath)

    return iter_json_file_wrapper
