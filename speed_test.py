import cProfile
import pstats
import time
from typing import Iterable
from tabulate import tabulate
from th2_data_services import Data
from th2_data_services.interfaces import IAdapter

# data_source = HTTPDataSource(f"http://10.100.66.114:31787")
data = Data.from_cache_file("test_events2.pkl")  # 1088396 Records


# # # # # # MAP # # # # # #


def handler(event):
    if event["type"] == "eventTreeNode":
        return {"id": event["eventId"], "eventType": event["eventType"]}


class SimpleAdapter(IAdapter):
    def handle(self, event):
        if event["type"] == "eventTreeNode":
            yield {"id": event["eventId"], "eventType": event["eventType"]}

    def handle_stream(self, stream: Iterable):
        for event in stream:
            if event["type"] == "eventTreeNode":
                yield {"id": event["eventId"], "eventType": event["eventType"]}


adapter = SimpleAdapter()


def simple_gen(stream):
    for event in stream:
        if event["type"] == "eventTreeNode":
            yield {"id": event["eventId"], "eventType": event["eventType"]}


def map_plain():
    return data.map(handler)


def map_stream_adapter():
    return data.map_stream(adapter)


def map_stream_generator():
    return data.map_stream(simple_gen)


def time_map():
    times = []
    for _ in range(5):
        start1 = time.time()
        _map = map_plain()
        end1 = time.time() - start1

        start2 = time.time()
        _map = map_stream_adapter()
        end2 = time.time() - start2

        start3 = time.time()
        _map = map_stream_generator()
        end3 = time.time() - start3

        times.append([end1, end2, end3])
    print(
        tabulate(
            times,
            headers=["Map", "Map Stream (Adapter)", "Map Stream (Generator)"],
            floatfmt=".10f",
            tablefmt="github",
            showindex=range(1, 6),
        )
    )


def cprofile_map():
    for func in (map_plain, map_stream_adapter, map_stream_generator):
        profiler = cProfile.Profile()
        profiler.enable()
        map_ = func()
        profiler.disable()
        pstats.Stats(profiler).sort_stats("ncalls").print_stats(5)
        print("-" * 30)


# # # # # # MAP # # # # # #

# # # # # # FILTER # # # # # #


def simple_filter(event):
    if event["type"] == "eventTreeNode":
        return event


def filter_stream_(stream):
    for event in stream:
        if event["type"] == "eventTreeNode":
            yield event


def filter_plain():
    return data.filter(simple_filter)


def filter_stream():
    return data.filter_stream(filter_stream_)


def time_filter():
    times = []
    for _ in range(5):
        start1 = time.time()
        _filter = filter_plain()
        end1 = time.time() - start1

        start2 = time.time()
        _filter = filter_stream()
        end2 = time.time() - start2

        times.append([end1, end2])

    print(
        tabulate(times, headers=["Filter", "Filter Stream"], floatfmt=".10f", tablefmt="github", showindex=range(1, 6))
    )


def cprofile_filter():
    for func in (filter_plain, filter_stream):
        profiler = cProfile.Profile()
        profiler.enable()
        _filter = func()
        profiler.disable()
        pstats.Stats(profiler).sort_stats("ncalls").print_stats(5)
        print("-" * 30)


# # # # # # FILTER # # # # # #

if __name__ == "__main__":
    # # Filter Tests
    time_filter()
    cprofile_filter()

    # # Map Tests
    time_map()
    cprofile_map()
