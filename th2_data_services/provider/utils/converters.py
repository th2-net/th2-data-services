from th2_data_services.interfaces.utils.converter import ITimestampConverter


class Th2TimestampConverter(ITimestampConverter[dict]):
    """Converts Th2 timestamps.

    If you request microseconds but your timestamp has nanoseconds, they will be just cut (not rounding).

    Expected timestamp format {'epochSecond': 123, 'nano': 500}.
    """

    @classmethod
    def parse_timestamp(cls, timestamp: dict) -> (str, str):
        seconds, nanoseconds = timestamp["epochSecond"], f"{timestamp['nano']:0>9}"
        return seconds, nanoseconds
