from th2_data_services.utils.converters import DatetimeStringConverter


def test_to_datetime(datetime_strings):
    assert DatetimeStringConverter.to_datetime(datetime_strings.datetime_string) == datetime_strings.expected_datetime


def test_to_microseconds(datetime_strings):
    assert DatetimeStringConverter.to_microseconds(datetime_strings.datetime_string) == datetime_strings.expected_us


def test_to_nanoseconds(datetime_strings):
    assert DatetimeStringConverter.to_nanoseconds(datetime_strings.datetime_string) == datetime_strings.expected_ns
