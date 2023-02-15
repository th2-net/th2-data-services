# %%
# %load_ext autoreload
# %autoreload 2

# %%
from th2_data_services import Data
from th2_data_services.utils import az_tree, event_utils
from datetime import datetime
import os
import json

# %% [markdown]
# ## Data

# %%
data_cache = Data.from_cache_file("./cache_2.5kk_events/cache_2.5kk_events.pickle")

# %%
events = data_cache.limit(200_000)

# %%
event = list(events.limit(1))[0]

# %%
# messages = Data.from_cache_file('./messages.pickle')

# %%
parent_events = event_utils.get_roots(events, 1000)

# %%
parent = parent_events[0]

# %% [markdown]
# # Event Utils

# %% [markdown]
# ### Get Type Totals

# %%
type_totals = event_utils.get_type_totals(events=events)
print(type_totals)

# %% [markdown]
# ### Get Type Frequencies

# %%
type_frequencies = event_utils.get_type_frequencies(
    events=events, types=["Service event", "ModelMatrix"], aggregation_level="hours"
)
print(type_frequencies)


# %% [markdown]
# ### Get Category Totals

# %%
category_totals = event_utils.get_category_totals(events=events, categorizer=lambda event: event["type"])
print(category_totals)


# %% [markdown]
# ### Get Category Frequencies

# %%
category_frequencies = event_utils.get_category_frequencies(
    events=events, categories=["Service event", "ModelMatrix"], categorizer=lambda event: event["eventType"]
)
print(category_frequencies)

# %% [markdown]
# ### Get Attached Message Ids

# %%
attached_message_ids = event_utils.get_attached_message_ids(events=events)
print(attached_message_ids)

# %% [markdown]
# ### Get Attached Messages Totals

# %%
attached_messages_totals = event_utils.get_attached_messages_totals(events=events)
print(attached_messages_totals)

# %% [markdown]
# ### Get Prior Parent Ids

# %%
prior_parent_ids = event_utils.get_prior_parent_ids(events=events)
print(prior_parent_ids)

# %% [markdown]
# ### Get Attached Message Ids Index

# %%
# Can taka a lot of time (~48sec)
attached_message_ids_index = event_utils.get_attached_message_ids_index(events=events)
print(attached_message_ids_index)

# %% [markdown]
# ### Get Roots

# %%
roots = event_utils.get_roots(events=events, count=10)
print(roots)

# %% [markdown]
# ### Get Parents

# %%
children_of_parent_1, parent_1 = event_utils.get_children_from_parent_id(events, parent["eventId"], 100)
parents = event_utils.get_parents(events=events, children=children_of_parent_1)
# or to find all parents
# parents = event_utils.get_parents(events=events, children=events)
assert [parent_1] == parents
print(parents)

# %% [markdown]
# ### Get Some

# %%
some = event_utils.get_some(events=events, event_type="ModelCase", count=10)
print(some)

# %% [markdown]
# ### Get Events By Category

# %%
events_by_category = event_utils.get_events_by_category(
    # events=events, category='ModelCase', count=10, categorizer=lambda event: event['eventType']
    # events=events, category="f0c3f6e8-fae7-40b6-8125-a16df981775d", count=10, categorizer=lambda event: event['parentEventId']
    events=events,
    category=False,
    count=10,
    categorizer=lambda event: event["successful"],
)
print(events_by_category)


# %% [markdown]
# ### Get Related Events

# %%
# # Needs events/messages from same time interval, otherwise will not match.
# related_events = event_utils.get_related_events(events=events, messages=messages, count=10)
# related_events

# %% [markdown]
# ### Get Children From Parent Id

# %%
children_from_parent_id = event_utils.get_children_from_parent_id(
    events=events, parent_id="f0c3f6e8-fae7-40b6-8125-a16df981775d", max_events=10
)
print(children_from_parent_id)


# %% [markdown]
# ### Get Children From Parents

# %%
children_from_parents, children_count = event_utils.get_children_from_parents(
    events=events, parents=parent_events, max_events=1
)
print(f"Children count: {children_count}")
print(children_from_parents)


# %% [markdown]
# ### Get Children From Parents As List

# %%
children_from_parents_as_list = event_utils.get_children_from_parents_as_list(
    events=events, parents=parent_events, max_events=1
)
print(children_from_parents_as_list)

# %% [markdown]
# ### Sublist

# %%
sublist = event_utils.sublist(
    events=events,
    start_time=datetime.fromisoformat("2022-03-16T10:50:16"),
    end_time=datetime.fromisoformat("2022-03-16T10:53:16"),
)
print(sublist)


# %% [markdown]
# ### Build Roots Cache

# %%
roots_cache = event_utils.build_roots_cache(events=events, depth=3, max_level=3)
print(roots_cache)

# %% [markdown]
# ### Extract Start Timestamp

# %%
start_timestamp = event_utils.extract_start_timestamp(event=event)
print(start_timestamp)

# %% [markdown]
# ### Print Type Totals

# %%
type_totals = event_utils.print_type_totals(
    events=events,
    # return_html=True
)
type_totals

# %% [markdown]
# ### Print Type Frequencies

# %%
type_frequencies = event_utils.print_type_frequencies(
    events=events,
    event_types=["Service event", "SendError", "sendMessage"],
    aggregation_level="hours",
    # return_html=True
)
type_frequencies

# %% [markdown]
# ### Print Category Totals

# %%
category_totals = event_utils.print_category_totals(
    events=events,
    # ignore_status=True
    categorizer=lambda event: event["eventType"],
    # # Presenting different possible use cases
    # categorizer=lambda event: event['eventName']
    # categorizer=lambda event: event['batchId']
)
category_totals

# %% [markdown]
# ### Print Category Frequencies

# %%
category_frequencies = event_utils.print_category_frequencies(
    events=events,
    event_types=["Service event", "ModelCase", "ModelMatrix"],
    categorizer=lambda event: event["eventType"],
    aggregation_level="hours",
    # return_html=True
)
category_frequencies


# %% [markdown]
# ### Print Attached Messages Totals

# %%
attached_messages_totals = event_utils.print_attached_messages_totals(
    events=events
    # return_html=True
)
attached_messages_totals


# %% [markdown]
# ### Print Roots

# %%
roots = event_utils.print_roots(events=events, count=10, start=10)
roots

# %% [markdown]
# ### Print Children

# %%
children = event_utils.print_children(
    events=events,
    parent="d2e09664-a504-11ec-a6d5-2365793d9363",
    count=10,
    # verbose=False
)
children


# %% [markdown]
# ### Print Event

# %%
event = event_utils.print_event(event=event)
event

# %% [markdown]
# ### Print Some

# %%
some = event_utils.print_some(
    events=events,
    event_type="ModelCase",
    count=10,
    # start=10,
    # failed=True,
    # verbose=False
)
some

# %% [markdown]
# ### Print Some By Category

# %%
some_by_category = event_utils.print_some_by_category(
    events=events,
    category="Service event",
    categorizer=lambda event: event["eventType"],
    count=10,
    # start=10,
    # failed=True
)
some_by_category


# %% [markdown]
# ### Print Children From Parents

# %%
children_from_parents = event_utils.print_children_from_parents(events=events, parents=parent_events, max_events=10)
children_from_parents

# %% [markdown]
# ### Print Children Stats From Parents

# %%
children_stats_from_parents = event_utils.print_children_stats_from_parents(
    events=events, parents=parent_events, max_events=10, return_html=True
)
children_stats_from_parents

# %% [markdown]
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# %% [markdown]
# # AZ Tree

# %% [markdown]
# ### Get Event Tree From Parent Id

# %%
get_event_tree_from_parent_id = az_tree.get_event_tree_from_parent_id(
    events=events,
    parent_id=parent["eventId"],
    depth=10,
    max_children=50,
    # body_to_simple_processors=None # TODO: Add examples
)
get_event_tree_from_parent_id


# %%
# Export to json for better view
if not os.path.exists("./output"):
    os.mkdir("output")
with open("./output/event_tree_from_parent_id.json", "w") as f:
    json.dump(get_event_tree_from_parent_id, f, ensure_ascii=False, indent=2)

# %% [markdown]
# ### Get Event Tree From Parent Events

# %%
get_event_tree_from_parent_events = tree, index = az_tree.get_event_tree_from_parent_events(
    events=events,
    parents=parent_events,
    depth=10,
    max_children=50,
    # body_to_simple_processors=None # TODO: Add examples
)
get_event_tree_from_parent_events

# %%
# Export to json for better view
if not os.path.exists("./output"):
    os.mkdir("output")
with open("./output/event_event_tree_from_parent_events_TREE.json", "w") as f:
    json.dump(tree, f, ensure_ascii=False, indent=2)

# %%
# Export to json for better view
if not os.path.exists("./output"):
    os.mkdir("output")
with open("./output/event_event_tree_from_parent_events_INDEX.json", "w") as f:
    json.dump(index, f, ensure_ascii=False, indent=2)

# %% [markdown]
# ### Save Tree As Json

# %%
if not os.path.exists("./output"):
    os.mkdir("output")
if not os.path.exists("./output/save_tree"):
    os.mkdir("output/save_tree")
save_tree_as_json = az_tree.save_tree_as_json(
    tree=tree,
    json_file_path="./output/save_tree/save_tree.json",
    # file_categorizer=lambda key, leaf: key # Will create lots of json files!
)


# %% [markdown]
# ### Transform Tree

# %%
# # TODO: Add examples
# transform_tree = az_tree.transform_tree(events=events)

# %% [markdown]
# ### Tree Walk

# %%
tree_walk = az_tree.tree_walk(
    tree=tree,
    processor=lambda path, name, leaf: leaf.update({name: "/".join(path)}),
    tree_filter=lambda path, name, leaf: "[fail]" in name,
)
if not os.path.exists("./output"):
    os.mkdir("output")
with open("./output/tree_walk.json", "w") as f:
    json.dump(tree, f, ensure_ascii=False, indent=2)

# %% [markdown]
# ### Tree Walk From Jsons

# %%
tree_walk_from_jsons = az_tree.tree_walk_from_jsons(
    path_pattern="output/tree_walk.json",
    processor=lambda path, name, leaf: leaf.update({name: path[-1]}),
    tree_filter=lambda path, name, leaf: "[fail]" in name,
)


# %% [markdown]
# ### Tree Walk From Jsons (Scenario 2)

# %%
results = {}
tree_walk_from_jsons = az_tree.tree_walk_from_jsons(
    path_pattern="output/tree_walk.json",
    processor=lambda path, name, leaf: results.update({path[-1]: leaf}),
    tree_filter=lambda path, name, leaf: "[fail]" in name,
)
results


# %% [markdown]
# ### Tree Update Totals

# %%
# # TODO: Add example
# tree_update_totals = az_tree.tree_update_totals(...)

# %% [markdown]
# ### Tree Get Category Totals

# %%
tree_get_category_totals = az_tree.tree_get_category_totals(
    tree=tree,
    categorizer=lambda path, name, leaf: leaf["info"]["type"] if "info" in leaf else None,
    tree_filter=lambda path, name, leaf: "[fail]" not in name,
)
tree_get_category_totals

# %% [markdown]
# ### Tree Get Category Totals From Jsons

# %%
# # TODO: Add example
tree_get_category_totals_from_jsons = az_tree.tree_get_category_totals_from_jsons(...)

# %% [markdown]
# ### Search Tree

# %%
# # TODO: Add example
search_tree = az_tree.search_tree(tree=tree, tree_filter=lambda path, name, leaf: "[fail]" not in name)

# %% [markdown]
# ### Search Tree From Jsons

# %%
# # TODO: Add example
search_tree_from_jsons = az_tree.search_tree_from_jsons(...)

# %% [markdown]
# ### Process Trees From Jsons

# %%
# # TODO: Add example
process_trees_from_jsons = az_tree.process_trees_from_jsons(...)
