from typing import Generator

import orjson as json
from orjson import JSONDecodeError


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
            raise ValueError(f"json.decoder.JSONDecodeError: Invalid json received.\n" f"{e}\n" f"{self.buffer}")
        self.buffer = []

    def _decode_without_buffer(self, x: str) -> dict:
        """Decode JSON without buffer.

        Args:
            x: JSON Object

        Returns:
            dict
        """
        yield json.loads(x)

    def _decode_with_buffer(self, x: str) -> dict:
        """Decode JSON with buffer.

        Args:
            x: JSON Object

        Returns:
            dict
        """
        if len(self.buffer) < self.buffer_limit:
            self.buffer.append(x)
        else:
            yield from self.from_buffer()
            self.buffer = [x]

    def fin(self) -> Generator:
        """If buffer exists returns dicts from buffer.

        Returns:
            Generator[dict]
        """
        if self.buffer:
            yield from self.from_buffer()
