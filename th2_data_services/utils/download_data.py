from datetime import datetime

from th2_data_services import Data
from th2_data_services.provider.v5.commands import http
from th2_data_services.provider.v5.data_source import HTTPProvider5DataSource
from th2_data_services.provider.v5.filters.event_filters import TypeFilter
import th2_data_services
from th2_data_services.utils import event_utils
from th2_data_services.utils import script_report_utils


# TODO
#   1. We cannot leave it as is because ds-core doesn't know anything about provider
#   2. It's more better to create a special command for that
def download_events(
    str_time_start, str_time_end, ds_url, add_earlier_parents=False, events_cache_file="events_download.pickle"
):  # noqa
    th2_data_services.INTERACTIVE_MODE = True

    start = datetime.now()
    print("Data Services Events Download Started :", start)
    data_source_events = HTTPProvider5DataSource(ds_url)
    events: Data = data_source_events.command(
        http.GetEvents(
            start_timestamp=datetime.fromisoformat(str_time_start),
            end_timestamp=datetime.fromisoformat(str_time_end),
            attached_messages=True,
            filters=[TypeFilter(["Checkpoint for session", "Checkpoint"], negative=True)],
            cache=True,
        )
    )
    if add_earlier_parents:
        print("Getting prior parents list:", datetime.now())
        parents_set = event_utils.get_prior_parent_ids_set(events)
        all_parents_list = []
        while len(parents_set) > 0:
            print("Got prior parents ids: len = ", len(parents_set), " ", datetime.now())
            parents_list = data_source_events.command(http.GetEventsById(list(parents_set), use_stub=True))
            event_utils.print_some_raw(parents_list, "Broken_Event", 10000)
            parents_set = event_utils.get_prior_parent_ids_set(parents_list)
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
    str_time_start,
    str_time_end,
    ds_url,
    add_earlier_parents=False,
    events_cache_file="events_download.pickle",
    messages_cache_file="messages.pickle",
):  # noqa
    events = download_events(
        str_time_start,
        str_time_end,
        ds_url,
        add_earlier_parents=add_earlier_parents,
        events_cache_file=events_cache_file,
    )

    attached_messages_stats = event_utils.total.get_attached_messages_totals(events)
    sessions_set = set()
    for session in attached_messages_stats.keys():
        sessions_set.add(session[: session.index(":")])
    print("Session list: ", sessions_set)

    start2 = datetime.now()
    print("Data Services Messages Download Started :", start2)
    data_source_messages = HTTPProvider5DataSource(ds_url)
    messages: Data = data_source_messages.command(
        http.GetMessages(
            start_timestamp=datetime.fromisoformat(str_time_start),
            end_timestamp=datetime.fromisoformat(str_time_end),
            stream=list(sessions_set),
            cache=True,
        )
    )
    if messages_cache_file is not None:
        messages.build_cache(messages_cache_file)
    end2 = datetime.now()
    print("Data Services Messages Download Finished: ", end2)
    delta2 = end2 - start2
    print("Duration: ", delta2.total_seconds())
    return events, messages


def prepare_story_from_storage(ds_url, story_items_list, event_body_processors=None):  # noqa
    smart = set()
    messages_ids = set()
    events_ids = set()
    script_report_utils.collect_ids_for_story(story_items_list, smart, events_ids, messages_ids)

    if len(smart) > 0:
        raise SystemError("Smart Reports elements are not supported")

    data_source = HTTPProvider5DataSource(ds_url)
    messages = []
    if len(messages_ids) > 0:
        m_list = [s[s.index(":") + 1 :] for s in messages_ids]
        messages = data_source.command(http.GetMessagesById(m_list, True))
    events = []
    if len(events_ids) > 0:
        e_list = [s[s.index(":") + 1 :] for s in events_ids]
        events = data_source.command(http.GetEventsById(e_list, True))

    result = script_report_utils.prepare_story(
        story_items_list, json_path=None, events=events, event_body_processors=event_body_processors, messages=messages
    )
    return result
