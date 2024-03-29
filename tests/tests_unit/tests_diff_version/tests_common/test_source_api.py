from datetime import datetime

from tests.tests_unit.tests_diff_version.conftest import Filter, HTTPProviderAPI


def test_generate_url_search_sse_events():
    api = HTTPProviderAPI(url="http://host:port")

    start_time = int(datetime.now().timestamp() * 1000)
    end_time = int(datetime.now().timestamp() * 1000)
    parent_event_id = "event_test"

    url = api.get_url_search_sse_events(
        start_timestamp=start_time,
        end_timestamp=end_time,
        attached_messages=True,
        parent_event=parent_event_id,
        keep_open=True,
    )

    assert (
        url == f"http://host:port/search/sse/events?startTimestamp={start_time}&endTimestamp={end_time}"
        f"&parentEvent={parent_event_id}&searchDirection=next&keepOpen={True}&metadataOnly=True"
        f"&attachedMessages={True}"
    )


def test_generate_url_search_sse_events_with_filters():
    api = HTTPProviderAPI(url="http://host:port")

    start_time = int(datetime.now().timestamp() * 1000)
    end_time = int(datetime.now().timestamp() * 1000)
    filter_name, filter_value = "body", "test"

    url = api.get_url_search_sse_events(
        start_timestamp=start_time, end_timestamp=end_time, filters=Filter(filter_name, filter_value).url()
    )

    assert (
        url == f"http://host:port/search/sse/events?startTimestamp={start_time}&endTimestamp={end_time}"
        f"&searchDirection=next&keepOpen=False&metadataOnly=True&attachedMessages=False&filters={filter_name}"
        f"&{filter_name}-values={filter_value}&{filter_name}-negative=False&{filter_name}-conjunct=False"
    )


def test_generate_url_search_sse_messages():
    api = HTTPProviderAPI(url="http://host:port")

    start_time = int(datetime.now().timestamp() * 1000)
    end_time = int(datetime.now().timestamp() * 1000)
    stream = ["test-stream", "test-stream2"]

    url = api.get_url_search_sse_messages(
        start_timestamp=start_time, end_timestamp=end_time, keep_open=True, stream=stream
    )

    assert (
        url == f"http://host:port/search/sse/messages?startTimestamp={start_time}&endTimestamp={end_time}"
        f"&stream={stream[0]}&stream={stream[1]}&searchDirection=next&keepOpen={True}&attachedEvents=False"
    )


def test_generate_url_search_sse_messages_with_filters():
    api = HTTPProviderAPI(url="http://host:port")

    start_time = int(datetime.now().timestamp() * 1000)
    end_time = int(datetime.now().timestamp() * 1000)
    stream = ["test-stream", "test-stream2"]
    filter_name, filter_value = "body", "test"

    url = api.get_url_search_sse_messages(
        start_timestamp=start_time,
        end_timestamp=end_time,
        keep_open=True,
        stream=stream,
        filters=Filter(filter_name, filter_value).url(),
    )

    assert (
        url == f"http://host:port/search/sse/messages?startTimestamp={start_time}&endTimestamp={end_time}"
        f"&stream={stream[0]}&stream={stream[1]}&searchDirection=next&keepOpen={True}&attachedEvents=False"
        f"&filters={filter_name}&{filter_name}-values={filter_value}&{filter_name}-negative=False&{filter_name}-conjunct=False"
    )


def test_encoding_url():
    api = HTTPProviderAPI(url="http://host:port")

    start_time = int(datetime.now().timestamp() * 1000)
    end_time = int(datetime.now().timestamp() * 1000)
    filter_name, filter_value = "test0 test1", "test2 test3"

    url = api.get_url_search_sse_events(
        start_timestamp=start_time, end_timestamp=end_time, filters=Filter(filter_name, filter_value).url()
    )

    filter_name = filter_name.split()
    filter_value = filter_value.split()

    encoded_filter_name = filter_name[0] + "%20" + filter_name[1]

    assert (
        url == f"http://host:port/search/sse/events?startTimestamp={start_time}&endTimestamp={end_time}"
        f"&searchDirection=next&keepOpen=False&metadataOnly=True&attachedMessages=False&filters="
        f"{encoded_filter_name}"
        f"&{encoded_filter_name}-values={filter_value[0] + '%20' + filter_value[1]}&"
        f"{encoded_filter_name}-negative=False&{encoded_filter_name}-conjunct=False"
    )


def test_generate_non_standart_url_search_sse_events():
    api = HTTPProviderAPI(url="http://host:port////")

    start_time = int(datetime.now().timestamp() * 1000)
    end_time = int(datetime.now().timestamp() * 1000)
    parent_event_id = "event_test"

    url = api.get_url_search_sse_events(
        start_timestamp=start_time,
        end_timestamp=end_time,
        attached_messages=True,
        parent_event=parent_event_id,
        keep_open=True,
    )

    assert (
        url == f"http://host:port/search/sse/events?startTimestamp={start_time}&endTimestamp={end_time}"
        f"&parentEvent={parent_event_id}&searchDirection=next&keepOpen={True}&metadataOnly=True"
        f"&attachedMessages={True}"
    )


def test_generate_non_standart_url_search_sse_messages_with_filters():
    api = HTTPProviderAPI(url="http://host:port/")

    start_time = int(datetime.now().timestamp() * 1000)
    end_time = int(datetime.now().timestamp() * 1000)
    stream = ["test-stream", "test-stream2"]
    filter_name, filter_value = "body", "test"

    url = api.get_url_search_sse_messages(
        start_timestamp=start_time,
        end_timestamp=end_time,
        keep_open=True,
        stream=stream,
        filters=Filter(filter_name, filter_value).url(),
    )

    assert (
        url == f"http://host:port/search/sse/messages?startTimestamp={start_time}&endTimestamp={end_time}"
        f"&stream={stream[0]}&stream={stream[1]}&searchDirection=next&keepOpen={True}&attachedEvents=False"
        f"&filters={filter_name}&{filter_name}-values={filter_value}&{filter_name}-negative=False&{filter_name}-conjunct=False"
    )


def test_count_slash_in_non_standart_url():
    api0 = HTTPProviderAPI(url="http://host:port")
    api1 = HTTPProviderAPI(url="http://host:port/")
    api4 = HTTPProviderAPI(url="http://host:port/////")
    api10 = HTTPProviderAPI(url="//////////")

    assert (
        api0._url == "http://host:port"
        and api1._url == "http://host:port"
        and api4._url == "http://host:port"
        and api10._url == ""
    )
