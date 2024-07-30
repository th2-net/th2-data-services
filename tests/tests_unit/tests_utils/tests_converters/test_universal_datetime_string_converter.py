from th2_data_services.utils.converters import UniversalDatetimeStringConverter


def test_to_datetime(universal_datetime_strings):
    assert (
        UniversalDatetimeStringConverter.to_datetime(universal_datetime_strings.datetime_string)
        == universal_datetime_strings.expected_datetime
    )


def test_to_seconds(universal_datetime_strings):
    assert (
        UniversalDatetimeStringConverter.to_seconds(universal_datetime_strings.datetime_string)
        == universal_datetime_strings.expected_s
    )


def test_to_microseconds(universal_datetime_strings):
    assert (
        UniversalDatetimeStringConverter.to_microseconds(universal_datetime_strings.datetime_string)
        == universal_datetime_strings.expected_us
    )


def test_to_nanoseconds(universal_datetime_strings):
    assert (
        UniversalDatetimeStringConverter.to_nanoseconds(universal_datetime_strings.datetime_string)
        == universal_datetime_strings.expected_ns
    )


def test_to_milliseconds(universal_datetime_strings):
    assert (
        UniversalDatetimeStringConverter.to_milliseconds(universal_datetime_strings.datetime_string)
        == universal_datetime_strings.expected_ms
    )


def test_to_datetime_string(universal_datetime_strings):
    assert (
        UniversalDatetimeStringConverter.to_datetime_str(universal_datetime_strings.datetime_string)
        == universal_datetime_strings.expected_datestring
    )


def test_to_th2_timestamp(universal_datetime_strings):
    assert (
        UniversalDatetimeStringConverter.to_th2_timestamp(
            universal_datetime_strings.datetime_string
        )
        == universal_datetime_strings.expected_th2_timestamp
    )
