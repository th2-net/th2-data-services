
# v0.2.5

## Features
1. [TH2-2248] Make python 3.6 compatibility

## BugFixes
1. [TH2-2232] Lib raises "TypeError" during Data.__del__ execution
2. [TH2-2213] [DataServices]: Intermediate error in th2-rpt-data-provider when unloading events from th2-rpt-data-provider.


# v0.3.0

## Improvement
1. Refactor Utils module
2. Changing Data Workflow
3. Tests were added
4. Pre-commit was added

## Features
1. find_messages_by_id_from_data_provider and find_events_by_id_from_data_provider 
functions returns dict if arg1 == str else list. So if your request only one 
message or event it returns Dict.

2. An experimental EventsTree2 class has been added with a real tree inside.

## Bugs
1. [TH2-2323] Memory leak when we use Data object.


# v0.3.1

## Bugs
1. [TH2-2330] Data iterator have been broken in v0.3.0

# v0.4.0 dev

1. TH2-2322 Separate the lib to 2 parts
New lib with ds_utils ...


