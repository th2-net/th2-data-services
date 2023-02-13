from th2.data_services.utils.converters import DatetimeConverter


def test_to_datetime(datetime_strings):
    assert datetime_strings.expected_datetime == DatetimeConverter.to_datetime(datetime_strings.datetime_obj)


def test_to_microseconds(datetime_strings):
    assert datetime_strings.expected_us == DatetimeConverter.to_microseconds(datetime_strings.datetime_obj)


def test_to_nanoseconds(datetime_strings):
    """If you request nanoseconds, last 3 number will be zeros, because datatime object doesn't have nanoseconds."""
    assert datetime_strings.expected_us * 1000 == DatetimeConverter.to_nanoseconds(datetime_strings.datetime_obj)


def test_to_milliseconds(datetime_strings):
    assert datetime_strings.expected_ms == DatetimeConverter.to_milliseconds(datetime_strings.datetime_obj)
