from th2_data_services.utils.converters import UniversalDatetimeStringConverter


def test_to_datetime(datetime_strings):
    assert (
        UniversalDatetimeStringConverter.to_datetime(datetime_strings.datetime_string)
        == datetime_strings.expected_datetime
    )


def test_to_microseconds(datetime_strings):
    assert (
        UniversalDatetimeStringConverter.to_microseconds(datetime_strings.datetime_string)
        == datetime_strings.expected_us
    )


def test_to_nanoseconds(datetime_strings):
    assert (
        UniversalDatetimeStringConverter.to_nanoseconds(datetime_strings.datetime_string)
        == datetime_strings.expected_ns
    )


def test_to_milliseconds(datetime_strings):
    assert (
        UniversalDatetimeStringConverter.to_milliseconds(datetime_strings.datetime_string)
        == datetime_strings.expected_ms
    )


def test_to_datetime_string(datetime_strings):
    assert (
        UniversalDatetimeStringConverter.to_datetime_str(datetime_strings.datetime_string)
        == datetime_strings.expected_datestring
    )
