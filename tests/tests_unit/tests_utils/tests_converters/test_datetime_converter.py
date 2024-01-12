from th2_data_services.utils.converters import DatetimeConverter


def test_to_datetime(datetime_strings):
    assert (
        DatetimeConverter.to_datetime(datetime_strings.datetime_obj)
        == datetime_strings.expected_datetime
    )


def test_to_microseconds(datetime_strings):
    assert (
        DatetimeConverter.to_microseconds(datetime_strings.datetime_obj)
        == datetime_strings.expected_us
    )


def test_to_nanoseconds(datetime_strings):
    """If you request nanoseconds, last 3 number will be zeros, because datatime object doesn't have nanoseconds."""
    assert (
        DatetimeConverter.to_nanoseconds(datetime_strings.datetime_obj)
        == datetime_strings.expected_us * 1000
    )


def test_to_milliseconds(datetime_strings):
    assert (
        DatetimeConverter.to_milliseconds(datetime_strings.datetime_obj)
        == datetime_strings.expected_ms
    )


def test_to_datetime_string(datetime_strings):
    assert (
        DatetimeConverter.to_datetime_str(datetime_strings.datetime_obj)
        == datetime_strings.expected_datestring[:-3] + "000"
    )
