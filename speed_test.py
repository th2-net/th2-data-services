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
        ...

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
        map1 = map_plain()
        map1_len = map1.len
        end1 = time.time() - start1

        start2 = time.time()
        map2 = map_stream_adapter()
        map2_len = map2.len
        end2 = time.time() - start2

        start3 = time.time()
        map3 = map_stream_generator()
        map3_len = map3.len
        end3 = time.time() - start3

        times.append([end1, end2, end3])

    print(
        tabulate(
            times,
            headers=["Map", "Map Stream (Adapter)", "Map Stream (Generator)"],
            floatfmt=".5f",
            tablefmt="github",
            showindex=range(1, 6),
        ),
        "\n",
    )


def cprofile_map():
    for func in (map_plain, map_stream_adapter, map_stream_generator):
        profiler = cProfile.Profile()
        profiler.enable()
        map_ = func()
        map_len = map_.len
        profiler.disable()
        pstats.Stats(profiler).sort_stats("ncalls").print_stats(10)
        print("-" * 30, "\n")


# # # # # # MAP # # # # # #

# # # # # # FILTER # # # # # #


def simple_filter(event):
    return event["type"] == "eventTreeNode"


def filter_plain():
    return data.filter(simple_filter)


def filter_stream():
    return data.filter_stream(simple_filter)


def time_filter():
    times = []
    for _ in range(5):
        start1 = time.time()
        filter1 = filter_plain()
        filter1_len = filter1.len
        end1 = time.time() - start1

        start2 = time.time()
        filter2 = filter_stream()
        filter2_len = filter2.len
        end2 = time.time() - start2

        times.append([end1, end2])

    print(
        tabulate(times, headers=["Filter", "Filter Stream"], floatfmt=".5f", tablefmt="github", showindex=range(1, 6)),
        "\n",
    )


def cprofile_filter():
    for func in (filter_plain, filter_stream):
        profiler = cProfile.Profile()
        profiler.enable()
        _filter = func()
        _filter_len = _filter.len
        profiler.disable()
        pstats.Stats(profiler).sort_stats("ncalls").print_stats(10)
        print("-" * 30, "\n")


# # # # # # FILTER # # # # # #

if __name__ == "__main__":
    # # Map Tests
    time_map()
    cprofile_map()

    # # Filter Tests
    time_filter()
    cprofile_filter()
