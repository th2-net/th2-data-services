from typing import List

from th2_grpc_common.common_pb2 import Direction
from th2_grpc_data_provider.data_provider_pb2 import MessageStream


class Streams:
    """General interface for composite streams of Provider v6.

    The class gives the opportunity to make list of streams with direction for each.
    """

    def __init__(self, streams: List[str], direction: str = None):
        """Streams constructor.

        Args:
            streams: List of Streams.
            direction: Direction of Streams (Only FIRST or SECOND). If None then is both directions.
        """
        self._streams = streams
        if direction is not None:
            direction = direction.upper()
            if direction not in ("FIRST", "SECOND"):
                raise ValueError("The direction must be 'FIRST' or 'SECOND'.")
        self._direction = direction

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}(" f"streams={self._streams}, " f"direction={self._direction})"

    def url(self) -> str:
        """Generates the stream part of the HTTP protocol API.

        Returns:
            str: Generated streams.
        """
        if self._direction is None:
            return "&".join([f"stream={stream}:FIRST&stream={stream}:SECOND" for stream in self._streams])
        return "&".join([f"stream={stream}:{self._direction}" for stream in self._streams])

    def grpc(self) -> List[MessageStream]:
        """Generates the grpc objects of the GRPC protocol API.

        Returns:
            List[MessageStream]: List of Stream with specified direction.
        """
        if self._direction is None:
            result = []
            for stream in self._streams:
                result += [
                    MessageStream(name=stream, direction=Direction.Value("FIRST")),
                    MessageStream(name=stream, direction=Direction.Value("SECOND")),
                ]
            return result
        return [MessageStream(name=stream, direction=Direction.Value(self._direction)) for stream in self._streams]
