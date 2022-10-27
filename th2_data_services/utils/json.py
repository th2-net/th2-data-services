import orjson as json
from orjson import JSONDecodeError


class BufferedJSONProcessor:
    def __init__(self, buffer_limit=250):
        self.buffer = []
        self.buffer_limit = buffer_limit
        if buffer_limit == 0:
            self.decode = self._decode_without_buffer
        else:
            self.decode = self._decode_with_buffer

    def from_buffer(self):
        try:
            for i in json.loads("[" + ','.join(self.buffer) + "]"):
                yield i
        except JSONDecodeError as e:
            raise ValueError(f"json.decoder.JSONDecodeError: Invalid json received.\n" f"{e}\n" f"{self.buffer}")
        self.buffer = []

    def _decode_without_buffer(self, x: str):
        yield json.loads(x)

    def _decode_with_buffer(self, x: str):
        if len(self.buffer) < self.buffer_limit:
            self.buffer.append(x)
        else:
            yield from self.from_buffer()
            self.buffer = [x]

    def fin(self):
        if self.buffer:
            yield from self.from_buffer()
