from th2_data_services.utils.converters import UnixTimestampConverter


def test_to_datetime(datetime_strings):
    assert (
        UnixTimestampConverter.to_datetime(datetime_strings.expected_ns)
        == datetime_strings.expected_datetime
    )


def test_to_seconds(datetime_strings):
    assert (
        UnixTimestampConverter.to_seconds(datetime_strings.expected_ns)
        == datetime_strings.expected_s
    )


def test_to_microseconds(datetime_strings):
    assert (
        UnixTimestampConverter.to_microseconds(datetime_strings.expected_ns)
        == datetime_strings.expected_us
    )


def test_to_nanoseconds(datetime_strings):
    assert (
        UnixTimestampConverter.to_nanoseconds(datetime_strings.expected_ns)
        == datetime_strings.expected_ns
    )


def test_to_milliseconds(datetime_strings):
    assert (
        UnixTimestampConverter.to_milliseconds(datetime_strings.expected_ns)
        == datetime_strings.expected_ms
    )


def test_to_datetime_string(datetime_strings):
    assert (
        UnixTimestampConverter.to_datetime_str(datetime_strings.expected_ns)
        == datetime_strings.expected_datestring
    )


def test_to_th2_timestamp(datetime_strings):
    assert (
        UnixTimestampConverter.to_th2_timestamp(datetime_strings.expected_ns)
        == datetime_strings.expected_th2_timestamp
    )
