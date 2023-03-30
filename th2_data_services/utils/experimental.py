#  Copyright 2023 Exactpro (Exactpro Systems Limited)
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

from th2_data_services.provider.v5.commands import http
from th2_data_services.provider.v5.data_source import HTTPProvider5DataSource
from th2_data_services.utils import script_report_utils


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
