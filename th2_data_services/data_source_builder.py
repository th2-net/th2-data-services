import time
from itertools import tee
from typing import Generator


class DataSourceBuilder:
    def __init__(self, data_provider):
        self._data_provider = data_provider
        self._workflow = []

    def filter(self, callback: object):
        """Append filter to workflow.

        :param callback: Filter function.
        """
        self._workflow += [{"filter": True, "callback": callback}]
        return self

    def map(self, callback):
        """Append transform function to workflow.

        :param callback: Transform function.
        """
        self._workflow += [{"filter": False, "callback": callback}]
        return self

    def build(self, skip: int = None, limit: int = None) -> Generator[dict, None, None]:
        """Gives events with applied functions.

        :param skip: Number of skip.
        :param limit: Limit.
        :return: Events.
        """
        skipped = 0
        pushed = 0
        start_time = time.time()
        working_data_provider, self._data_provider = tee(self._data_provider)

        counter = 0
        for record in working_data_provider:
            counter += 1
            for step in self._workflow:
                if isinstance(record, (list, tuple)):
                    pending_records = record.copy()
                    record.clear()
                    for record_ in pending_records:
                        if step["filter"]:
                            skip_record = not step["callback"](record_)
                            if skip_record:
                                continue
                        else:
                            record_ = step["callback"](record_)
                            if record_ is None:
                                continue
                        record.append(record_)
                else:
                    if step["filter"]:
                        skip_record = not step["callback"](record)
                        if skip_record:
                            record = None
                            break
                    else:
                        record = step["callback"](record)
                        if record is None:
                            break

            if not isinstance(record, (list, tuple)):
                record = [record] if record is not None else []
            for record_ in record:
                if skip is not None and skipped < skip:
                    skipped += 1
                    continue
                yield record_
                pushed += 1
                if limit is not None and pushed == limit:
                    break
            if limit is not None and pushed == limit:
                break

            if counter % 10000 == 0:
                print(f"Counter records: {counter}; Time: {time.time() - start_time}")
