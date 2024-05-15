import timeit


def compare_times(datetime_strings):
    datetime_string = datetime_strings.datetime_string
    datetime_obj = datetime_strings.datetime_obj
    th2_timestamp = datetime_strings.th2_timestamp
    expected_ns = datetime_strings.expected_ns

    globals = {
        "datetime_string": datetime_string,
        "datetime_obj": datetime_obj,
        "th2_timestamp": th2_timestamp,
        "expected_ns": expected_ns,
    }

    params = {
        "DatetimeStringConverter": "datetime_string",
        "DatetimeConverter": "datetime_obj",
        "ProtobufTimestampConverter": "th2_timestamp",
        "UniversalDatetimeStringConverter": "datetime_string",
        "UnixTimestampConverter": "expected_ns",
    }

    converters = [
        "DatetimeStringConverter",
        "DatetimeConverter",
        "ProtobufTimestampConverter",
        "UniversalDatetimeStringConverter",
        "UnixTimestampConverter",
    ]

    for i, converter in enumerate(converters):
        param = params[converter]
        print(f"[{i + 1}] {converter}")
        print("input:", globals[param])
        setup = f"from th2_data_services.utils.converters import {converter}"
        print(
            "1. .parse_timestamp:",
            timeit.timeit(f"{converter}.parse_timestamp({param})", setup=setup, globals=globals),
        )
        print(
            "2. .to_datetime:",
            timeit.timeit(f"{converter}.to_datetime({param})", setup=setup, globals=globals),
        )
        print(
            "3. .to_seconds:",
            timeit.timeit(f"{converter}.to_seconds({param})", setup=setup, globals=globals),
        )
        print(
            "4. .to_microseconds:",
            timeit.timeit(f"{converter}.to_microseconds({param})", setup=setup, globals=globals),
        )
        print(
            "5. .to_nanoseconds:",
            timeit.timeit(f"{converter}.to_nanoseconds({param})", setup=setup, globals=globals),
        )
        print(
            "6. .to_milliseconds:",
            timeit.timeit(f"{converter}.to_milliseconds({param})", setup=setup, globals=globals),
        )
        print(
            "7. .to_datetime_str:",
            timeit.timeit(f"{converter}.to_datetime_str({param})", setup=setup, globals=globals),
        )
        print(
            "8. .to_th2_timestamp:",
            timeit.timeit(f"{converter}.to_th2_timestamp({param})", setup=setup, globals=globals),
        )


if __name__ == "__main__":
    print("#" * 50)
    print("This benchmark shows how many seconds takes every converter operation in seconds.")
    print("#" * 50)

    from tests.tests_unit.tests_utils.tests_converters.conftest import converter_test_cases

    for case in converter_test_cases:
        compare_times(case)
