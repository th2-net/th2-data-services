from datetime import datetime
from typing import Tuple, List
from th2_data_services import Data
from th2_data_services.provider.v5.commands import http
from th2_data_services.provider.v5.data_source import HTTPProvider5DataSource
from th2_data_services.provider.v5.filters.event_filters import TypeFilter
from th2_data_services.utils import event_utils, script_report_utils
import th2_data_services


# TODO
#   1. We cannot leave it as is because ds-core doesn't know anything about provider
#   2. It's more better to create a special command for that
#   (unfortunately we cannot do it now because we cannot change Data object in the map func)
def download_events(
    start_timestamp: str,
    end_timestamp: str,
    provider_url: str,
    add_earlier_parents: bool = False,
    events_cache_file: str = "events_download.pickle",
) -> Data:
    """Downloads events.

    Args:
        start_timestamp: Download events from this timestamp
        end_timestamp: Download events till this timestamp
        provider_url: Provider url. e.g: http://localhost:8000
        add_earlier_parents: Collect parents before given timeframe
        events_cache_file: Output pickle file, defaults to "events_download.pickle"

    Returns:
        Data
    """
    th2_data_services.INTERACTIVE_MODE = True

    start = datetime.now()
    print("Data Services Events Download Started :", start)
    data_source_events = HTTPProvider5DataSource(provider_url)
    events: Data = data_source_events.command(
        http.GetEvents(
            start_timestamp=datetime.fromisoformat(start_timestamp),
            end_timestamp=datetime.fromisoformat(end_timestamp),
            attached_messages=True,
            filters=[TypeFilter(["Checkpoint for session", "Checkpoint"], negative=True)],
            # TODO: Add custom filters?
            cache=True,
        )
    )
    if add_earlier_parents:
        print("Getting prior parents list:", datetime.now())
        parents_set = event_utils.get_prior_parent_ids(events)
        all_parents_list = []
        while len(parents_set) > 0:
            print("Got prior parents ids: len = ", len(parents_set), " ", datetime.now())
            parents_list = data_source_events.command(http.GetEventsById(list(parents_set), use_stub=True))
            event_utils.print_events_raw(parents_list, "Broken_Event", 10000)
            parents_set = event_utils.get_prior_parent_ids(parents_list)
            all_parents_list.append(parents_list)

        events = Data(all_parents_list) + events
        print("Getting prior parents list - done", datetime.now())

    if events_cache_file is not None:
        events.build_cache(events_cache_file)
    end = datetime.now()
    print("Data Services Events Download Finished: ", end)
    delta = end - start
    print("Duration: ", delta.total_seconds())
    return events


def download_events_and_messages(
    start_timestamp: str,
    end_timestamp: str,
    provider_url: str,
    add_earlier_parents: bool = False,
    events_cache_file: str = "events_download.pickle",
    messages_cache_file: str = "messages.pickle",
) -> Tuple[Data, Data]:
    """Downloads events and messages.

    Args:
        start_timestamp: Download from this timestamp
        end_timestamp: Download till this timestamp
        provider_url: Provider url. e.g: http://localhost:8000
        add_earlier_parents: Collect parents before given timeframe
        events_cache_file: Output pickle file for events, defaults to "events_download.pickle"
        messages_cache_file: Output pickle file for messages, defaults to "messages.pickle"

    Returns:
        Tuple[Data, Data], Events & Messages
    """
    events = download_events(
        start_timestamp,
        end_timestamp,
        provider_url,
        add_earlier_parents=add_earlier_parents,
        events_cache_file=events_cache_file,
    )

    attached_messages_stats = event_utils.get_attached_messages_totals(events)
    sessions_set = set(session[: session.index(":")] for session in attached_messages_stats)
    print("Session list: ", sessions_set)
    start = datetime.now()
    print("Data Services Messages Download Started :", start)
    data_source_messages = HTTPProvider5DataSource(provider_url)
    messages: Data = data_source_messages.command(
        http.GetMessages(
            start_timestamp=datetime.fromisoformat(start_timestamp),
            end_timestamp=datetime.fromisoformat(end_timestamp),
            stream=list(sessions_set),
            cache=True,
        )
    )
    if messages_cache_file is not None:
        messages.build_cache(messages_cache_file)
    end = datetime.now()
    print("Data Services Messages Download Finished: ", end)
    delta2 = end - start
    print("Duration: ", delta2.total_seconds())
    return events, messages


def prepare_story_from_storage(provider_url: str, story_items: List, event_body_processors=None):  # noqa
    # TODO: Add docstrings.
    smart = set()
    messages_ids = set()
    events_ids = set()
    script_report_utils.collect_ids_for_story(story_items, smart, events_ids, messages_ids)

    if len(smart) > 0:
        raise SystemError("Smart Reports elements are not supported")

    data_source = HTTPProvider5DataSource(provider_url)
    messages = []
    if len(messages_ids) > 0:
        m_list = [s[s.index(":") + 1 :] for s in messages_ids]
        messages = data_source.command(http.GetMessagesById(m_list, True))
    events = []
    if len(events_ids) > 0:
        e_list = [s[s.index(":") + 1 :] for s in events_ids]
        events = data_source.command(http.GetEventsById(e_list, True))

    result = script_report_utils.prepare_story(
        story_items, json_path=None, events=events, event_body_processors=event_body_processors, messages=messages
    )
    return result
