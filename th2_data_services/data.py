#  Copyright 2022 Exactpro (Exactpro Systems Limited)
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
import pickle
import pprint
from functools import partial
from os import rename
from pathlib import Path
from time import time
from typing import Callable, Dict, Generator, List, Optional, Union, Iterable, Iterator, Any
from weakref import finalize
import logging

logger = logging.getLogger(__name__)


class _DataLogger(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return "Data[%s] %s" % (self.extra["id"], msg), kwargs


DataGenerator = Generator[dict, None, None]
DataSet = Union[Iterator, Callable[..., DataGenerator], List[Iterator]]
WorkFlow = List[Dict[str, Union[Callable, str]]]


class Data:
    """A wrapper for data/data_stream.

    The class provides methods for working with data as a stream.

    Such approach to data analysis called streaming transformation.
    """

    def __init__(self, data: DataSet, cache: bool = False, workflow: WorkFlow = None):
        """Data constructor.

        Args:
            data: Data source. Any iterable, Data object or function that creates generator.
            cache: Set True if you want to write and read from cache.
            workflow: Workflow.
        """
        if self._is_iterables_list(data):
            self._data_stream = self._create_data_set_from_iterables(data)
        else:
            self._data_stream = data

        self._id = id(self)
        self._cache_filename = f"{self._id}_{time()}.pickle"
        self._cache_path = Path(f"./temp/{self._cache_filename}").resolve()
        self._len = None
        self._workflow = [] if workflow is None else workflow  # Normally it has empty list or one Step.
        self._length_hint = None  # The value is populated when we use limit method.
        self._cache_status = cache
        self._finalizer = finalize(self, self.__remove)
        self._logger = _DataLogger(logger, {"id": self._id})
        # It used to indicate the number of current iteration of the Data object.
        # It's required if the same instance iterates several times in for-in loops.
        self.iter_num = 0
        self.stop_iteration = None

        self._logger.info(
            "New data object with data stream = '%s', cache = '%s' initialized", id(self._data_stream), cache
        )

    def __remove(self):
        """Data class destructor."""
        if self.__is_cache_file_exists():
            self.__delete_cache()
        del self._data_stream

    def __delete_cache(self) -> None:
        """Removes cache file."""
        path = self.get_cache_filepath()
        if path.exists():
            self._logger.debug("Deleting cache file '%s'" % path)
            path.unlink()

    def __delete_pending_cache(self) -> None:
        """Removes cache file."""
        path = self.get_pending_cache_filepath()
        if path.exists():
            self._logger.debug("Deleting cache file '%s'" % path)
            path.unlink()

    def _create_data_set_from_iterables(self, iterables_list: List[Iterable]) -> DataSet:
        """Creates a generator from the list of iterables."""
        return partial(self._create_generator_data_source_from_iterables, iterables_list)

    def _create_generator_data_source_from_iterables(self, iterables_list: List[Iterable]) -> Generator:
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

    @property
    def is_empty(self) -> bool:
        """bool: Indicates that the Data object doesn't contain data."""
        for _ in self.__load_data():
            return False
        return True

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
                self._logger.debug("Successfully iterated")
                interruption = False

        finally:
            if interruption:

                if self.stop_iteration:  # When limit was reached.
                    # You can save _len in this case because iteration was stopped by limit.
                    self._logger.info("Iteration was interrupted because limit reached")

                else:  # When something went wrong but NOT StopIteration
                    self._logger.info("Iteration was interrupted")
                    # You shouldn't save _len in this case because iteration was interrupted.
                    if self.iter_num == 1:
                        self._len = None

                # Delete cache if it was interrupted and the file was not complete.
                # https://exactpro.atlassian.net/browse/TH2-3546
                if is_data_writes_cache:
                    self._logger.info("The cache file is not written to the end. Delete tmp cache file")
                    self.__delete_pending_cache()
                else:  # Data reads cache.
                    from th2_data_services import INTERACTIVE_MODE  # To escape circular import problem.

                    # Do not delete cache file if it's interactive mode and Data has read cache.
                    if not INTERACTIVE_MODE:
                        self.__delete_cache()

            self.iter_num -= 1
            self.stop_iteration = False

    def __iter__(self) -> DataGenerator:
        self.stop_iteration = False
        self.iter_num += 1
        self._logger.info("Starting iteration, iter_num = %s", self.iter_num)
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

    def __load_data(self, cache: bool = False) -> DataGenerator:
        """Loads data from cache or data.

        Args:
            cache: Flag if you what to write and read from cache.

        Returns:
            obj: Generator
        """
        if cache and self.__is_cache_file_exists():
            self._logger.info("Iterating using own cache file '%s'" % self.get_cache_filepath())
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
        filepath = self.get_cache_filepath()
        return filepath.with_name("[PENDING]" + self._cache_filename)

    def get_cache_filepath(self) -> Optional[Path]:
        """Returns filepath for a cache file."""
        return self._cache_path

    def _iterate_modified_data_stream(self, data_stream: DataGenerator, workflow: WorkFlow) -> DataGenerator:
        """Returns generator that iterates data stream with applied workflow.

        StopIteration from limit function will be handled here.
        """
        self._logger.debug("Iterating data stream = '%s'", id(data_stream))
        for record in data_stream:
            try:
                modified_records = self.__apply_workflow(record, workflow)
            except StopIteration as e:
                self._logger.debug("Handle StopIteration")
                modified_records = e.value

                if modified_records is not None:
                    if isinstance(modified_records, (list, tuple)):
                        yield from modified_records
                    else:  # Just one record.
                        yield modified_records

                # There is some magic.
                # It'll stop data stream and will be handled in the finally statements.
                # If you put return not under except block it will NOT work.
                return

            if modified_records is None:
                continue
            elif isinstance(modified_records, (list, tuple)):
                yield from modified_records
            else:  # Just one record.
                yield modified_records

    def __change_data(self, data_stream: DataGenerator, workflow: WorkFlow, cache: bool = False) -> DataGenerator:
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
            filepath.parent.mkdir(exist_ok=True)  # Create dir if does not exist.
            self._logger.debug("Recording cache file '%s'" % filepath)
            file = open(filepath, "wb")

            for modified_record in self._iterate_modified_data_stream(data_stream, workflow):
                pickle.dump(modified_record, file)
                yield modified_record

            file.close()
            rename(file.name, str(self.get_cache_filepath()))
            self._logger.debug("Cache file was created '%s'" % self.get_cache_filepath())
        else:
            yield from self._iterate_modified_data_stream(data_stream, workflow)

    def __is_cache_file_exists(self) -> bool:
        """Checks whether cache file exist."""
        path = self.get_cache_filepath()
        r = path.is_file()
        self._logger.debug("Cache file exists" if r else "Cache file doesn't exist")
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

        if filepath.suffix != ".pickle":
            raise FileNotFoundError(f"File hasn't pickle extension")

        with open(filepath, "rb") as file:
            while True:
                try:
                    decoded_data = pickle.load(file)
                    yield decoded_data
                except EOFError:
                    break

    def _process_step(self, step: dict, record):
        res = step["callback"](record)
        self._logger.debug("    - step '%s' -> %s", step["type"], res)
        return res

    def __apply_workflow(self, record: Any, workflow: WorkFlow) -> Optional[Union[dict, List[dict]]]:
        """Creates generator records with apply workflow.

        Returns:
            obj: Generator records.

        """
        self._logger.debug("Apply workflow for %s", record)
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

        self._logger.debug("-> %s", record)
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
        self._logger.info("Apply filter")
        new_workflow = [
            {"type": "filter", "callback": lambda record: record if callback(record) else None},
        ]
        return Data(data=self, workflow=new_workflow)

    def map(self, callback: Callable) -> "Data":
        """Append `transform` function to workflow.

        Args:
            callback: Transform function.

        Returns:
            Data: Data object.

        """
        self._logger.info("Apply map")
        new_workflow = [{"type": "map", "callback": callback}]
        return Data(data=self, workflow=new_workflow)

    def _build_limit_callback(self, num) -> Callable:
        self._logger.debug("Build limit callback with limit = %s", num)

        def callback(r):
            callback.pushed += 1
            if callback.pushed == num:
                callback.pushed = 0
                self._logger.debug("Limit reached - raise StopIteration")
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
        self._logger.info("Apply limit = %s", num)
        new_workflow = [{"type": "limit", "callback": self._build_limit_callback(num)}]
        data_obj = Data(data=self, workflow=new_workflow)
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

    def use_cache(self, status: bool = True) -> "Data":
        """Changes cache flag and returns self.

        Args:
            status(bool): If True the whole data stream will be saved to cache file.
            Further actions with the Data object will consume data from the cache file. True by default.

        Returns:
            Data: Data object.

        """
        self._logger.info("Cache using activated" if status else "Cache using deactivated")
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

    def __add__(self, other_data: Iterable) -> "Data":
        return Data(self._create_data_set_from_iterables([self, other_data]))
