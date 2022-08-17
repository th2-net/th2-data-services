from th2_data_services.provider.v5.utils.converters import Th2TimestampConverter


def test_to_datetime(datetime_strings):
    assert Th2TimestampConverter.to_datetime(datetime_strings.th2_timestamp) == datetime_strings.expected_datetime


def test_to_microseconds(datetime_strings):
    assert Th2TimestampConverter.to_microseconds(datetime_strings.th2_timestamp) == datetime_strings.expected_us


def test_to_nanoseconds(datetime_strings):
    assert Th2TimestampConverter.to_nanoseconds(datetime_strings.th2_timestamp) == datetime_strings.expected_ns
