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

from typing import Generator
import gzip

import orjson as json
from orjson import JSONDecodeError

from th2_data_services.utils.decode_error_handler import UNICODE_REPLACE_HANDLER


def iter_json_file(filename, buffer_limit=250):
    """Returns the function that returns generators."""

    def iter_json_file_logic():
        """Generator that reads and yields decoded JSON objects from a file."""
        json_processor = BufferedJSONProcessor(buffer_limit)

        with open(filename, "r") as data:
            while True:
                try:
                    v = data.readline()
                    if not v:
                        break

                    yield from json_processor.decode(v)
                except ValueError:
                    print(len(json_processor.buffer))
                    print(f"Error string: {v}")
                    raise
            yield from json_processor.fin()

    def iter_json_file_wrapper(*args, **kwargs):
        """Wrapper function that allows passing arguments to the generator."""
        return iter_json_file_logic(*args, **kwargs)

    return iter_json_file_wrapper


def iter_json_gzip_file(filename, buffer_limit=250):
    """Returns the function that returns generators."""

    def iter_json_gzip_file_logic():
        """Generator that reads and yields decoded JSON objects from a file."""
        json_processor = BufferedJSONProcessor(buffer_limit)

        if buffer_limit != 0:
            finished = False
            with gzip.open(filename, "r") as data:
                while True:
                    try:
                        for _ in range(buffer_limit):
                            v = data.readline().decode("utf-8", UNICODE_REPLACE_HANDLER)
                            if not v:
                                finished = True
                                break
                            json_processor.buffer.append(v)

                        yield from json_processor.from_buffer()

                        if finished:
                            break

                    except ValueError:
                        print(len(json_processor.buffer))
                        print(f"Error string: {v}")
                        raise

                yield from json_processor.fin()
        else:
            with gzip.open(filename, "r") as data:
                while True:
                    try:
                        v = data.readline().decode("utf-8", UNICODE_REPLACE_HANDLER)
                        if not v:
                            break

                        yield from json_processor.decode(v)

                    except ValueError:
                        print(len(json_processor.buffer))
                        print(f"Error string: {v}")
                        raise

    def iter_json_gzip_file_wrapper(*args, **kwargs):
        """Wrapper function that allows to rerun generator one more time."""
        return iter_json_gzip_file_logic(*args, **kwargs)

    return iter_json_gzip_file_wrapper


class BufferedJSONProcessor:
    def __init__(self, buffer_limit: int = 250):
        """BufferedJSONProcessor constructor.

        Args:
            buffer_limit: By default 250. If limit is 0 buffer will not be used.
        """
        self.buffer = []
        self.buffer_limit = buffer_limit
        if buffer_limit == 0:
            self.decode = self._decode_without_buffer
        else:
            self.decode = self._decode_with_buffer

    def from_buffer(self) -> Generator:
        """Transforms JSON objects to dict objects.

        Returns:
            Generator[dict]
        """
        try:
            for i in json.loads("[" + ",".join(self.buffer) + "]"):
                yield i
        except JSONDecodeError as e:
            raise ValueError(
                f"json.decoder.JSONDecodeError: Invalid json received.\n" f"{e}\n" f"{self.buffer}"
            )
        finally:
            # Prevents StopIteration issues
            self.buffer = []

    def _decode_without_buffer(self, x: str) -> Generator:
        """Decode JSON without buffer.

        Args:
            x: JSON Object

        Returns:
            dict
        """
        yield json.loads(x)

    def _decode_with_buffer(self, x: str) -> Generator:
        """Decode JSON with buffer.

        Args:
            x: JSON Object

        Returns:
            dict
        """
        # for i in range(self.buffer_limit):

        # # FIXME -- we check len every message. It can take a lot of time
        # if len(self.buffer) < self.buffer_limit:
        #     self.buffer.append(x)
        # else:
        #     yield from self.from_buffer()
        #     self.buffer = [x]

        yield from self.from_buffer()
        self.buffer = [x]

    def fin(self) -> Generator:
        """If buffer exists, returns dicts from buffer.

        Returns:
            Generator[dict]
        """
        if self.buffer:
            yield from self.from_buffer()
