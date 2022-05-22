from typing import Optional

from _pytest.logging import LogCaptureFixture

from th2_data_services import Data


class LogsChecker:
    def __init__(self, caplog: LogCaptureFixture):
        self.caplog: LogCaptureFixture = caplog

    @property
    def messages(self):
        return self.caplog.messages

    def _exception_message(self, msg):
        return f"\n" f"Expected: {msg}, \n" f"Whole messages: \n" + "\n".join(self.messages)

    def cache_file_created(self, data: Data):
        path = data.get_cache_filepath()
        msg = f"Data[{data._id}] Cache file was created '{path}'"
        assert msg in self.messages, self._exception_message(msg)

    def used_own_cache_file(self, data: Data):
        path = data.get_cache_filepath()
        msg = f"Data[{data._id}] Iterating using own cache file '{path}'"
        assert msg in self.messages, self._exception_message(msg)


def iterate_data(data: Data, *, to_return=True) -> Optional[list]:
    if to_return:
        return list(data)
    else:
        for _ in data:
            pass


def iterate_data_and_do_checks(data: Data, log_checker: LogsChecker) -> list:
    r = iterate_data(data, to_return=True)  # Just to iterate and create cache files.
    assert is_cache_file_exists(data)
    log_checker.cache_file_created(data)
    return r


def is_cache_file_exists(data_obj: Data) -> bool:
    return data_obj.get_cache_filepath().is_file()


def is_pending_cache_file_exists(data_obj: Data) -> bool:
    return data_obj.get_pending_cache_filepath().is_file()