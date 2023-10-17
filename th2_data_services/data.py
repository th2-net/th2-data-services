#  Copyright 2022-2023 Exactpro (Exactpro Systems Limited)
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
import io
import json
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
import gzip as gzip_

# LOG import logging

# LOG logger = logging.getLogger(__name__)


# LOG class _DataLogger(logging.LoggerAdapter):
# LOG     def process(self, msg, kwargs):
# LOG         return "Data[%s] %s" % (self.extra["id"], msg), kwargs
from th2_data_services.utils.path_utils import check_if_filename_valid, check_if_file_exists

DataIterValues = TypeVar("DataIterValues")
DataGenerator = Generator[DataIterValues, None, None]
DataSet = Union[Iterator, Callable[..., DataGenerator], List[Iterator]]
WorkFlow = List[Dict[str, Union[Callable, str]]]


class Data(Generic[DataIterValues]):
    """A wrapper for data/data_stream.

    The class provides methods for working with data as a stream.

    Such approach to data analysis called streaming transformation.
    """

    def __init__(
        self,
        data: DataSet,
        cache: bool = False,
        workflow: WorkFlow = None,
        pickle_version: int = o.DEFAULT_PICKLE_VERSION,
    ):
        """Data constructor.

        Args:
            data: Data source. Any iterable, Data object or a function that creates generator.
            cache: Set True if you want to write and read from cache.
            workflow: Workflow.
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
        self._workflow = (
            [] if workflow is None else workflow
        )  # Normally it has empty list or one Step.
        self._length_hint = None  # The value is populated when we use limit method.
        self._cache_status = cache
        # We use finalize instead of __del__ because __del__ won't be executed sometimes.
        # Read more about __del__ problems here: https://stackoverflow.com/a/2452895
        self._finalizer = finalize(self, self.__remove)
        # LOG         self._logger = _DataLogger(logger, {"id": self._id})
        # It used to indicate the number of current iteration of the Data object.
        # It's required if the same instance iterates several times in for-in loops.
        self.iter_num = 0  # Indicates what level of the loop the Data object is in.
        self.stop_iteration = None
        self._read_from_external_cache_file = False
        self.__metadata = {}
        self._pickle_version = pickle_version  # Default pickle protocol version

    # LOG         self._logger.info(
    # LOG            "New data object with data stream = '%s', cache = '%s' initialized", id(self._data_stream), cache
    # LOG        )

    @property
    def metadata(self):
        return self.__metadata

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

        return all([isinstance(d, (Data, tuple, list)) for d in data])

    @property
    def len(self) -> int:
        """int: How many records in the Data stream.

        Notes:
        1. It is a wasteful operation if you are performing it on the Data object that has never been iterated before.

        2. If you want just to check emptiness, use is_empty property instead.
        """
        return self._len if self._len is not None else self.__calc_len()

    # Actually it should be a function, not a property.
    @property
    def is_empty(self) -> bool:
        """bool: Indicates that the Data object doesn't contain data."""
        for _ in self:
            return False
        return True

    @property
    def cache_status(self) -> bool:
        return self._cache_status

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

                if self.stop_iteration:  # When limit was reached.
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
            self.stop_iteration = False

    def __iter__(self) -> DataGenerator:
        self.stop_iteration = False
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

    def _build_workflow(self, workflow):
        """Updates limit callbacks each time when Data object is iterated.

        It used to have possibility iterate the same Data object several times in the loops.
        """
        new_workflow = copy.deepcopy(workflow)
        for w in new_workflow[::-1]:
            if w["type"] == "limit":
                w["callback"] = self._build_limit_callback(w["callback"].limit)

        return new_workflow

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
            data_stream = self._data_stream() if callable(self._data_stream) else self._data_stream
            workflow = self._build_workflow(self._workflow)

            if self.__check_file_recording():
                # Do not read from the cache file if it has PENDING status (if the file is not filled yet).
                # It used to handle case when Data object iterates in the loop several times.
                cache = False

            yield from self.__change_data(data_stream=data_stream, workflow=workflow, cache=cache)

    def __check_file_recording(self) -> bool:
        """Checks whether there is a current recording in the file.

        Returns:
            bool: File recording status.
        """
        path = self.get_pending_cache_filepath()
        return path.is_file()

    def get_pending_cache_filepath(self) -> Path:
        """Returns filepath for a pending cache file."""
        return self._pending_cache_path

    def get_cache_filepath(self) -> Path:
        """Returns filepath for a cache file."""
        return self._cache_path

    def _iterate_modified_data_stream(
        self, data_stream: DataGenerator, workflow: WorkFlow
    ) -> DataGenerator:
        """Returns generator that iterates data stream with applied workflow.

        StopIteration from limit function will be handled here.
        """
        # LOG         self._logger.debug("Iterating data stream = '%s'", id(data_stream))
        for record in data_stream:
            try:
                modified_records = self.__apply_workflow(record, workflow)
            except StopIteration as e:
                # LOG                 self._logger.debug("Handle StopIteration")
                modified_records = e.value

                if modified_records is not None:
                    if isinstance(modified_records, (list, tuple)):
                        yield from modified_records
                    else:  # Just one record.
                        yield modified_records

                # There is some magic.
                # It'll stop data stream and will be handled in the finally statements.
                # If you put return not under except block it will NOT work.
                #
                # It happens because python returns control to data_stream here due to `yield`.
                return

            if modified_records is None:
                continue
            elif isinstance(modified_records, (list, tuple)):
                yield from modified_records
            else:  # Just one record.
                yield modified_records

    def __change_data(
        self, data_stream: DataGenerator, workflow: WorkFlow, cache: bool
    ) -> DataGenerator:
        """Applies workflow for data.

        Args:
            data_stream: Data for apply workflow.
            workflow: Workflow.
            cache: Set True if you are going to write and read from the cache.

        Yields:
            obj: Generator
        """
        if cache:
            filepath = self.get_pending_cache_filepath()
            filepath.parent.mkdir(exist_ok=True)  # Create dir if it does not exist.
            # LOG             self._logger.debug("Recording cache file '%s'" % filepath)
            self._cache_file_obj = open(filepath, "wb")

            for modified_record in self._iterate_modified_data_stream(data_stream, workflow):
                pickle.dump(modified_record, self._cache_file_obj, protocol=self._pickle_version)
                yield modified_record

            self._cache_file_obj.close()
            rename(self._cache_file_obj.name, str(self.get_cache_filepath()))
        # LOG             self._logger.debug("Cache file was created '%s'" % self.get_cache_filepath())
        else:
            yield from self._iterate_modified_data_stream(data_stream, workflow)

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

    def _process_step(self, step: dict, record):
        res = step["callback"](record)
        # LOG         self._logger.debug("    - step '%s' -> %s", step["type"], res)
        return res

    def __apply_workflow(
        self, record: Any, workflow: WorkFlow
    ) -> Optional[Union[dict, List[dict]]]:
        """Creates generator records with apply workflow.

        Returns:
            obj: Generator records.

        """
        # LOG         self._logger.debug("Apply workflow for %s", record)
        for step in workflow:
            if isinstance(record, (list, tuple)):
                result = []
                for r in record:
                    step_res = None
                    try:
                        step_res = self._process_step(step, r)
                    except StopIteration as e:
                        step_res = e.value
                        raise StopIteration(result if result else None)
                    finally:
                        if step_res is not None:
                            if isinstance(step_res, (list, tuple)):
                                result += step_res  # To make flat list.
                            else:
                                result.append(step_res)

                record = result
                if not record:
                    record = None
                    break  # Break iteration if step result is None.
            else:
                try:
                    record = self._process_step(step, record)
                    if record is None:
                        break  # Break workflow iteration if step result is None.
                except StopIteration:
                    raise

        # LOG         self._logger.debug("-> %s", record)
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

        def get_source(handler):
            yield from handler(self)

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

        source = partial(get_source, filter_yield)
        data = Data(source)
        data._set_metadata(self.metadata)
        return data

    def map(self, callback_or_adapter: Union[Callable, IRecordAdapter]) -> "Data":
        """Append `transform` function to workflow.

        Args:
            callback_or_adapter: Transform function or an Adapter with IRecordAdapter
                interface implementation.
                If the function returns None value, this value will be skipped from OUT stream.
                If you don't want skip None values -- use `map_stream`.

        Returns:
            Data: Data object.

        """
        # LOG         self._logger.info("Apply map")
        if isinstance(callback_or_adapter, IRecordAdapter):
            new_workflow = [{"type": "map", "callback": callback_or_adapter.handle}]
        else:
            new_workflow = [{"type": "map", "callback": callback_or_adapter}]
        data = Data(data=self, workflow=new_workflow)
        data._set_metadata(self.metadata)
        return data

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

        def get_source(handler):
            yield from handler(self)

        if isinstance(adapter_or_generator, IStreamAdapter) and isgeneratorfunction(
            adapter_or_generator.handle
        ):
            source = partial(get_source, adapter_or_generator.handle)
        elif isgeneratorfunction(adapter_or_generator):
            source = partial(get_source, adapter_or_generator)
        else:
            raise Exception(
                "map_stream Only accepts IStreamAdapter class with generator function or Generator function"
            )
        data = Data(source)
        data._set_metadata(self.metadata)
        return data

    def _build_limit_callback(self, num) -> Callable:
        # LOG         self._logger.debug("Build limit callback with limit = %s", num)

        def callback(r):
            callback.pushed += 1
            if callback.pushed == num:
                callback.pushed = 0
                # LOG                 self._logger.debug("Limit reached - raise StopIteration")
                raise StopIteration(r)
            else:
                return r

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
        # LOG         self._logger.info("Apply limit = %s", num)
        # def get_source(handler):
        #     try:
        #         yield from handler(self)
        #     except StopIteration as e:
        #
        #         # There is some magic.
        #         # It'll stop data stream and will be handled in the finally statements.
        #         # If you put return not under except block it will NOT work.
        #         #
        #         # It happens because python returns control to data_stream here due to `yield`.
        #         return
        #
        # def filter_yield(stream):
        #     callback = self._build_limit_callback(num)
        #     for record in stream:
        #         if callback(record):
        #             yield record
        #
        # source = partial(get_source, filter_yield)
        # data = Data(source)
        # data._length_hint = num
        # data._set_metadata(self.metadata)
        # return data

        new_workflow = [{"type": "limit", "callback": self._build_limit_callback(num)}]
        data_obj = Data(data=self, workflow=new_workflow)
        data_obj._length_hint = num
        data_obj._set_metadata(self.metadata)
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

    def __str__(self):
        output = "------------- Printed first 5 records -------------\n"
        for index, record in enumerate(self):
            if index == 5:
                break
            output += pprint.pformat(record) + "\n"
        return output

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

    def build_cache(self, filename):
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

        """
        path_name = Path(filename).name
        status, reason = check_if_filename_valid(path_name)
        if not status:
            raise Exception(f"Cannot build cache file. {reason}")

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
                    pickle.dump(record, file, protocol=self._pickle_version)

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
        """Creates Data object from cache file with provided name.

        Args:
            filename: Name or path to cache file.
            pickle_version: Pickle protocol version. Change default value
                if your pickle file was created with another pickle version.

        Returns:
            Data: Data object.

        Raises:
            FileNotFoundError if provided file does not exist.

        """
        check_if_file_exists(filename)
        data_obj = cls([], cache=True)
        data_obj._set_custom_cache_destination(filename=filename)
        data_obj.update_metadata({"source_file": filename})
        data_obj._pickle_version = pickle_version
        return data_obj

    @classmethod
    def from_json(cls, filename, buffer_limit=250, gzip=False) -> "Data[dict]":
        """Creates Data object from json file with provided name.

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
        """Creates Data object from any file with provided name.

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
        cls, filename, header=None, header_first_line=False, mode="r", delimiter=","
    ) -> "Data":
        """Creates Data object from any file with provided name.

        It will iterate the CSV file as if you were doing it with CSV module.

        Args:
            filename: Name or path to the file.
            header: If provided header for csv, Data object will yield Dict[str].
            header_first_line: If the first line of the csv file is header, it'll take header from
                                the first line. Data object will yield Dict[str].
                                `header` argument is not required in this case.
            mode: Read mode of open function.
            delimiter: CSV file delimiter.

        Returns:
            Data: Data object.

        Raises:
            FileNotFoundError if provided file does not exist.

        """
        # TODO - bug here TH2-4930 - new data object doesn't work with limit method
        check_if_file_exists(filename)
        data = cls(_iter_csv(filename, header, header_first_line, mode, delimiter))
        data.update_metadata({"source_file": filename})

        # TH2-4930
        # TODO - should be deleted after bugfix
        if header is None and not header_first_line:

            def limit(*args, **kwargs):
                raise RuntimeError(
                    "The data object that was get by using 'from_csv' "
                    "cannot work with 'limit' method. Known issue TH2-4930."
                )

            data.limit = limit

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
        """Update metadata of object with metadata argument.

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

    def to_json(self, filename: str, indent: int = None, overwrite: bool = False):
        """Converts data to json format.

        Args:
            filename (str): Output JSON filename
            indent (int, optional): JSON format indent. Defaults to None.
            overwrite (bool, optional): Overwrite if filename exists. Defaults to False.

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
                json.dump(record, file, indent=indent)
                file.write(",\n")
            file.seek(file.tell() - 3)  # Delete last comma for valid JSON
            file.write("]")  # Close list

    def to_jsons(self, filename: str, indent: int = None, overwrite: bool = False, gzip=False):
        if Path(filename).absolute().exists() and not overwrite:
            raise FileExistsError(
                f"{filename} already exists. If you want to overwrite current file set `overwrite=True`"
            )

        if gzip:
            with gzip_.open(filename, "wb") as f:
                with io.TextIOWrapper(f, encoding="utf-8") as encode:
                    for record in self:
                        json_str = json.dumps(record, indent=indent)
                        encode.write(json_str + "\n")
        else:
            with open(filename, "w", encoding="UTF-8") as file:
                for record in self:
                    json.dump(record, file, indent=indent)
                    file.write("\n")


def _iter_any_file(filename, mode="r"):
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


def _iter_csv(filename, header=None, header_first_line=False, mode="r", delimiter=","):
    """Returns the function that returns generators."""

    def iter_logic():
        with open(filename, mode) as data:
            if header is not None:
                reader = csv.DictReader(data, fieldnames=header)
            elif header_first_line:
                reader = csv.DictReader(data)
            else:
                reader = csv.reader(data, delimiter=delimiter)

            for row in reader:
                yield (row,)  # Because if provide just a list it will iterate it.

    def iter_wrapper(*args, **kwargs):
        """Wrapper function that allows passing arguments to the generator."""
        return iter_logic(*args, **kwargs)

    return iter_wrapper
