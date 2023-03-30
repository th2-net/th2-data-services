from th2_data_services.utils.converters import ProtobufTimestampConverter


def test_to_datetime(datetime_strings):
    assert ProtobufTimestampConverter.to_datetime(datetime_strings.th2_timestamp) == datetime_strings.expected_datetime


def test_to_microseconds(datetime_strings):
    assert ProtobufTimestampConverter.to_microseconds(datetime_strings.th2_timestamp) == datetime_strings.expected_us


def test_to_nanoseconds(datetime_strings):
    assert ProtobufTimestampConverter.to_nanoseconds(datetime_strings.th2_timestamp) == datetime_strings.expected_ns


def test_to_milliseconds(datetime_strings):
    assert ProtobufTimestampConverter.to_milliseconds(datetime_strings.th2_timestamp) == datetime_strings.expected_ms
