from th2_data_services.utils import misc_utils
from th2_data_services.utils.converters import DatetimeStringConverter


def test_frequency_table_data(frequency_table_data):
    # tb = FrequencyCategoryTable(['timestamp', 'MessageType', 'direction', 'session'], frequency_table_data)

    tb = misc_utils.get_objects_frequencies2(
        frequency_table_data,
        categories=[],
        categorizer=lambda m: m["MessageType"],
        # TODO -- we shouldn't know internal structure!!! - epochSeconds
        timestamp_function=lambda e: int(
            DatetimeStringConverter.parse_timestamp(e["timestamp"])[0]
        ),
        aggregation_level="1s",
    )
    # metrics = Category('messagetype', lambda m: m['messagetype'])
    # tb = get_category_frequencies2(frequency_table_data, metrics)
    print(tb)
