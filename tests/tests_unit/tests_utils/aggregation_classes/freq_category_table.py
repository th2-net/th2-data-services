from th2_data_services.utils import misc_utils
from th2_data_services.utils.converters import DatetimeStringConverter


def test_frequency_table_data_has_the_same_header_every_time(frequency_table_data, capsys):
    # tb = FrequencyCategoryTable(['timestamp', 'MessageType', 'direction', 'session'], frequency_table_data)

    tb = misc_utils.get_objects_frequencies2(
        frequency_table_data,
        categories=[],
        categorizer=lambda m: m["MessageType"],
        timestamp_function=lambda e: int(
            DatetimeStringConverter.parse_timestamp(e["timestamp"])[0]
        ),
        aggregation_level="1d",
        include_total=False,
    )
    # metrics = Category('messagetype', lambda m: m['messagetype'])
    # tb = get_category_frequencies2(frequency_table_data, metrics)
    print(tb)

    captured = capsys.readouterr()
    assert (
        captured.out
        == """+--------+-------------------+-----------------+-------------------+------------+---------------+
|        | timestamp_start   | timestamp_end   | ExecutionReport   | NewOrder   |   OrderCancel |
+========+===================+=================+===================+============+===============+
|        | 2023-08-13        | 2023-08-14      | 1                 | 1          |             2 |
+--------+-------------------+-----------------+-------------------+------------+---------------+
|        | 2023-08-14        | 2023-08-15      | 1                 | 1          |             2 |
+--------+-------------------+-----------------+-------------------+------------+---------------+
|        | 2023-08-16        | 2023-08-17      | 0                 | 2          |             3 |
+--------+-------------------+-----------------+-------------------+------------+---------------+
|        | 2023-08-17        | 2023-08-18      | 1                 | 0          |             1 |
+--------+-------------------+-----------------+-------------------+------------+---------------+
|        | 2023-08-19        | 2023-08-20      | 1                 | 1          |             0 |
+--------+-------------------+-----------------+-------------------+------------+---------------+
|        | 2023-08-20        | 2023-08-21      | 0                 | 0          |             2 |
+--------+-------------------+-----------------+-------------------+------------+---------------+
|        | 2023-08-21        | 2023-08-22      | 1                 | 3          |             0 |
+--------+-------------------+-----------------+-------------------+------------+---------------+
|        | 2023-08-22        | 2023-08-23      | 1                 | 0          |             0 |
+--------+-------------------+-----------------+-------------------+------------+---------------+
|        | 2023-08-23        | 2023-08-24      | 0                 | 3          |             0 |
+--------+-------------------+-----------------+-------------------+------------+---------------+
|        | 2023-08-24        | 2023-08-25      | 0                 | 2          |             1 |
+--------+-------------------+-----------------+-------------------+------------+---------------+
| count  |                   |                 |                   |            |            10 |
+--------+-------------------+-----------------+-------------------+------------+---------------+
| totals |                   |                 | 6                 | 13         |            11 |
+--------+-------------------+-----------------+-------------------+------------+---------------+
"""
    )


def test_frequency_table_data_has_the_same_header_every_time_with_total_column(
    frequency_table_data, capsys
):
    # tb = FrequencyCategoryTable(['timestamp', 'MessageType', 'direction', 'session'], frequency_table_data)

    tb = misc_utils.get_objects_frequencies2(
        frequency_table_data,
        categories=[],
        categorizer=lambda m: m["MessageType"],
        timestamp_function=lambda e: int(
            DatetimeStringConverter.parse_timestamp(e["timestamp"])[0]
        ),
        aggregation_level="1d",
    )
    # metrics = Category('messagetype', lambda m: m['messagetype'])
    # tb = get_category_frequencies2(frequency_table_data, metrics)
    print(tb)

    captured = capsys.readouterr()
    assert (
        captured.out
        == """+--------+-------------------+-----------------+-------------------+------------+---------------+---------+
|        | timestamp_start   | timestamp_end   | ExecutionReport   | NewOrder   | OrderCancel   |   Total |
+========+===================+=================+===================+============+===============+=========+
|        | 2023-08-13        | 2023-08-14      | 1                 | 1          | 2             |       4 |
+--------+-------------------+-----------------+-------------------+------------+---------------+---------+
|        | 2023-08-14        | 2023-08-15      | 1                 | 1          | 2             |       4 |
+--------+-------------------+-----------------+-------------------+------------+---------------+---------+
|        | 2023-08-16        | 2023-08-17      | 0                 | 2          | 3             |       5 |
+--------+-------------------+-----------------+-------------------+------------+---------------+---------+
|        | 2023-08-17        | 2023-08-18      | 1                 | 0          | 1             |       2 |
+--------+-------------------+-----------------+-------------------+------------+---------------+---------+
|        | 2023-08-19        | 2023-08-20      | 1                 | 1          | 0             |       2 |
+--------+-------------------+-----------------+-------------------+------------+---------------+---------+
|        | 2023-08-20        | 2023-08-21      | 0                 | 0          | 2             |       2 |
+--------+-------------------+-----------------+-------------------+------------+---------------+---------+
|        | 2023-08-21        | 2023-08-22      | 1                 | 3          | 0             |       4 |
+--------+-------------------+-----------------+-------------------+------------+---------------+---------+
|        | 2023-08-22        | 2023-08-23      | 1                 | 0          | 0             |       1 |
+--------+-------------------+-----------------+-------------------+------------+---------------+---------+
|        | 2023-08-23        | 2023-08-24      | 0                 | 3          | 0             |       3 |
+--------+-------------------+-----------------+-------------------+------------+---------------+---------+
|        | 2023-08-24        | 2023-08-25      | 0                 | 2          | 1             |       3 |
+--------+-------------------+-----------------+-------------------+------------+---------------+---------+
| count  |                   |                 |                   |            |               |      10 |
+--------+-------------------+-----------------+-------------------+------------+---------------+---------+
| totals |                   |                 | 6                 | 13         | 11            |      30 |
+--------+-------------------+-----------------+-------------------+------------+---------------+---------+
"""
    )
