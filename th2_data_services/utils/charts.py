from th2_data_services.data import Data
from th2_data_services.utils.message_utils.frequencies import get_category_frequencies
from th2_data_services.config import options
from matplotlib.axis import Axis
from matplotlib.figure import Figure
from matplotlib.pyplot import subplots
from datetime import datetime
from typing import Iterable, List, Tuple


DEFAULT_CHART_WIDTH = 15.0
DEFAULT_CHART_HEIGHT = 5.5


def _fill_gaps(arr: Iterable, start: int, end: int, timestamp_gap: datetime = None) -> List:
    """Fills gaps inside arrays for line chart data.

    Args:
        arr (Iterable): Line data
        start (int): Gap start index
        end (int): Gap end index
        timestamp_gap (datetime, optional): Datetime objects gap. Defaults to None.

    Returns:
        List: Line data with gaps patched
    """
    filler_count = end - start
    filler = [None] * (filler_count - 1)
    if filler == []:
        return arr

    if not isinstance(arr, list):
        arr = list(arr)

    if timestamp_gap and isinstance(arr[0], datetime):
        start_timestamp = arr[start - 1]
        filler = [
            start_timestamp + timestamp_gap * i
            for i in range(1, filler_count)
        ]

    arr = arr[:start] + filler + arr[start:]

    return arr


def message_rate(
    data: Data,
    categories: List[str] = None,
    aggregation_level: str = "1hour",
    fig_width: float = DEFAULT_CHART_WIDTH,
    fig_height: float = DEFAULT_CHART_HEIGHT,
    output_file: str = None
) -> Tuple[Figure, Axis]:
    """Generates message rates chart.

    Args:
        data (Data): TH2-Messages
        categories (List[str], optional): Categories to draw. Defaults to None (All).
        aggregation_level (str, optional): Aggregation level. Defaults to "1hour".
        fig_width (float, optional): Chart width. Defaults to DEFAULT_CHART_WIDTH.
        fig_height (float, optional): Chart height. Defaults to DEFAULT_CHART_HEIGHT.
        output_file (str, optional): Chart output file. Defaults to None.

    Returns:
        Tuple[Figure, Axis]: matplotlib.pyplot.subplots
    """
    category_frequencies = get_category_frequencies(
        data,
        categories,
        options.MESSAGE_FIELDS_RESOLVER.get_type,
        aggregation_level=aggregation_level
    )
    categories = category_frequencies.get_categories()

    fig, ax = subplots()

    timestamps = [
        datetime.fromisoformat(timestamp)
        for timestamp in category_frequencies.get_column("timestamp")
    ]
    timestamp_gaps = []
    timestamp_gap_index = 0
    timestamp_gap = timestamps[1] - timestamps[0]
    X_axis = [timestamps[0]]
    for i, (prev_timestamp, next_timestamp) in enumerate(zip(timestamps, timestamps[1:])):
        if next_timestamp - prev_timestamp != timestamp_gap:
            timestamp_gaps.append([i+1])
            while prev_timestamp != next_timestamp:
                prev_timestamp += timestamp_gap
                i += 1
            timestamp_gaps[timestamp_gap_index].append(i+1)
            timestamp_gap_index += 1
        X_axis.append(next_timestamp)

    for category in categories:
        X = _fill_gaps(X_axis, 0, 0)
        Y = _fill_gaps(category_frequencies.get_column(category), 0, 0)
        gap_step = 0
        for gap in timestamp_gaps:
            start, end = map(lambda i: i+gap_step, gap)
            X = _fill_gaps(X, start, end, timestamp_gap)
            Y = _fill_gaps(Y, start, end, timestamp_gap)
            gap_step += end - start - 1
        ax.plot(X, Y, label=category)

    ax.set_xlabel("Timestamp")
    ax.set_ylabel("mps")
    ax.legend(bbox_to_anchor=(1.0, 0.5))
    ax.grid(True)
    ax.set_xticks(X)
    ax.set_xticklabels(X, rotation=35)

    fig.set_size_inches(fig_width, fig_height)
    fig.autofmt_xdate()
    if output_file:
        fig.savefig(output_file)

    return fig, ax
