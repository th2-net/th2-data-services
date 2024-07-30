#  Copyright 2023-2024 Exactpro (Exactpro Systems Limited)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from typing import List

import th2_data_services.utils
from th2_data_services.config import options
from th2_data_services.utils.converters import flatten_dict
from th2_data_services.utils.message_utils import message_utils


def prepare_story_from_storage(
    provider_url: str, story_items: List, event_body_processors=None
):  # noqa
    # TODO: Add docstrings.
    smart = set()
    messages_ids = set()
    events_ids = set()
    collect_ids_for_story(story_items, smart, events_ids, messages_ids)

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

    result = prepare_story(
        story_items,
        json_path=None,
        events=events,
        event_body_processors=event_body_processors,
        messages=messages,
    )
    return result


############################
# PrepareStory and its functions  [start]
###########################
# If I remember correct - the idea to create a function, that will help to create
# bug reports faster!
# TODO - so it can become something like BugReportUtils class


def collect_element(p, l, elements_to_collect, collected_data):  # noqa
    # TODO: Add docstrings
    for element in elements_to_collect:
        sub_list = element[element.index(":") + 1 :].split("/")
        if len(sub_list) != len(p):
            continue
        match = True
        for i in range(len(sub_list)):
            if not p[len(p) - i - 1].startswith(sub_list[i]):
                match = False
                break
        if match:
            collected_data[element] = (p, l)


def create_parallel_tables(story_item, collected_data):  # noqa
    # TODO: Add docstrings
    sub_table_names = []
    sub_table_names.extend(story_item.keys())
    keys_lists = []
    max_keys = 0
    for n in sub_table_names:
        keys_list = []
        for k, v in collected_data[story_item[n]][1].items():
            if type(v) not in [dict, list]:
                keys_list.append(k)

        if len(keys_list) > max_keys:
            max_keys = len(keys_list)
        keys_lists.append(keys_list)

    result = []
    header = []
    for s_t_n in sub_table_names:
        header.extend([s_t_n, "", " "])
    result.append(header)
    for i in range(max_keys):
        row = []
        for j in range(len(sub_table_names)):
            key = keys_lists[j][i] if i < len(keys_lists[j]) else ""
            val = (
                collected_data[story_item[sub_table_names[j]]][1][key]
                if i < len(keys_lists[j])
                else ""
            )
            row.extend([key, val, " "])
        result.append(row)
    return result


def collect_ids_for_story(story_items_list, smart, events, messages):  # noqa
    # TODO: Add docstrings
    for item in story_items_list:
        if type(item) == str:
            if item.startswith("smart:"):
                smart.add(item)
            if item.startswith("event:"):
                events.add(item)
            if item.startswith("message:"):
                messages.add(item)
            if item.startswith("message_raw:"):
                messages.add(item)
            if item.startswith("message_dict:"):
                messages.add(item)
            if item.startswith("event_dict:"):
                events.add(item)

        if type(item) == dict:
            for v in item.values():
                if v.startswith("smart:"):
                    smart.add(v)
                if v.startswith("event:"):
                    events.add(v)
                if v.startswith("message:"):
                    messages.add(v)


def prepare_story(
    story_items_list, json_path=None, events=None, event_body_processors=None, messages=None
):  # noqa
    # TODO: Add docstrings
    smart_report_elements_to_collect = set()
    events_to_collect = set()
    messages_to_collect = set()

    collect_ids_for_story(
        story_items_list, smart_report_elements_to_collect, events_to_collect, messages_to_collect
    )

    collected_data = {}
    # print(smart_report_elements_to_collect)
    if json_path is not None:
        th2_data_services.utils.json_tree.tree_walk_from_jsons(
            json_path,
            lambda p, n, l: collect_element(p, l, smart_report_elements_to_collect, collected_data),
            None,
        )
    if events is not None:
        # print("Collecting ", events_to_collect)
        for e in events:
            e_key = "event:" + e["eventId"]
            if e_key in events_to_collect:
                b = e["body"]
                if event_body_processors is not None and e["eventType"] in event_body_processors:
                    b = event_body_processors[e["eventType"]](b)
                collected_data[e_key] = (e, b)
            e_key = "event_dict:" + e["eventId"]
            if e_key in events_to_collect:
                b = e["body"]
                if event_body_processors is not None and e["eventType"] in event_body_processors:
                    b = event_body_processors[e["eventType"]](b)
                collected_data[e_key] = (e, b)

    if messages is not None:
        # print("Collecting ", messages_to_collect)
        for mm in messages:
            sub_list = message_utils.expand_message(mm)
            for m in sub_list:
                for key in messages_to_collect:
                    if m["messageId"] in key:
                        # print("Found: ", key)
                        b = {
                            "_message_type": m["messageType"],
                            "_message_session": m["sessionId"],
                            "_message_direction": m["direction"],
                            "_message_timestamp": message_utils.extract_timestamp(m),
                        }
                        b.update(
                            flatten_dict(options.MESSAGE_FIELDS_RESOLVER.get_body(m)["fields"])
                        )
                        collected_data[key] = (m, b)

    result = []
    for item in story_items_list:
        if type(item) == str:
            if (
                item.startswith("smart:")
                or item.startswith("event:")
                or item.startswith("message:")
            ):
                table = [["field", "value"]]
                l = collected_data[item]
                for k, v in l[1].items():
                    if type(v) not in [dict, list]:
                        table.append([k, str(v)])
                result.append(table)
            elif item.startswith("message_raw:"):
                result.append(message_utils.get_raw_body_str(collected_data[item][0]))
            elif item.startswith("message_dict:") or item.startswith("event_dict:"):
                result.append(collected_data[item][1])
            else:
                result.append(item)
        if type(item) == dict:
            result.append(create_parallel_tables(item, collected_data))

    return result
