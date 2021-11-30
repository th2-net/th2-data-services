# v0.2.5

## Features

1. [TH2-2248] Make python 3.6 compatibility

## BugFixes

1. [TH2-2232] Lib raises "TypeError" during Data.__del__ execution
2. [TH2-2213] [DataServices]: Intermediate error in th2-rpt-data-provider when unloading events from
   th2-rpt-data-provider.

# v0.3.0

## Improvements

1. Refactor Utils module
2. Changing Data Workflow
3. Tests were added
4. Pre-commit was added

## Features

1. find_messages_by_id_from_data_provider and find_events_by_id_from_data_provider functions returns dict if arg1 == str
   else list. So if your request only one message or event it returns Dict.

2. An experimental EventsTree2 class has been added with a real tree inside.


## BugFixes

1. [TH2-2323] Memory leak when we use Data object.

# v0.3.1

## BugFixes

1. [TH2-2330] Data iterator have been broken in v0.3.0

# v0.4.1

## Improvements

1. [TH2-2322] The lib was separated to 2 parts. New lib with ds_utils posted
   in [here](https://github.com/th2-net/th2-data-services-utils)
2. [TH2-2335] A pipeline was created that sends a packet to PyPi for the branch with the pypi_ prefix.

## BugFixes

1. [TH2-2299] Error and keep_alive status were handled.

# v0.5.0

## User impact and migration instructions

1. [I] You no longer need to enter UTC time corrected for local time. DataSource methods now expect UTC time.  
   [M] Change the time to UTC in all your scripts.
2. [I] The last "messageIds" message in the messages stream will be ignored.  
   [M] If you do checks for the last message, you can delete them.
3. [I] _DataSource.write_to_txt_ was moved to Data. The name has been changed to _write_to_file_.  
   [M] If you use _write_to_file_ function, change the corresponding class and method.
4. [I] _len(Data)_ functionality was removed. The _Data.len_ property is now used.  
   [M] Change _len(Data)_ to _Data.len_ for your functions.
5. [I] The codec-pipeline wrapper-messages are now split into sub-messages.  
   [M] If you use wrapper-messages for your statistics then adapt functions for sub-messages (now they look like a usual
   message)

## Improvements

1. [TH2-2427] Refactoring
    - Reduced waiting time of connection check.
    - The last "messageIds" message in the message stream will be ignored. Lib user will not get it.
    - DataSource.write_to_txt was moved to Data. The name has been changed to write_to_file.
    - Up requirement libs versions.
2. len(Data) functionality was removed because it has side effects when we use list(Data)
   and too expensive to use. **Please use Data.len property instead.**
3. [TH2-2474] Use of cache was revised.
4. [TH2-2553] The time that have given in some method of data_source module now will expect in utc format.
5. [TH2-2601] Unit tests were added in CI.

## Features

1. Added Data.limit(num) method to use in the pipeline.
2. Added Data.write_to_file(filename) due to TH2-2427.
3. Added Data.len property to use instead of len(Data)
4. Added Data.is_empty property
5. [TH-2420] Added adapter for codecs pipeline.
6. [TH2-2575] Added ParentEventsTree class in events tree module.
7. [TH2-2577] Added optional arguments (stub_if_broken_event: bool) in find_events_by_id_from_data_provider method of
   data_source module. If stub_if_broken_event is True and some ids is not available on data provider: method return
   stub inside.

## BugFixes

1. [TH2-2424] Cache function was fixed.
2. [TS-766] Fixed case when Data Services cannot recover more than 64 unknown events.
3. [TH2-2419] find_X_by_id_from_data_provider functions return expected objects

# v0.5.1

## Improvements

1. [TH2-2724] The user can be able to deal with problematic messages.


# v0.5.2

## BugFixes

1. [TH2-2731] Fixed a problem with using map function with list of records.

# v0.6.0

## Features

1. [TH2-2283] Implemented rpt-data-provider Filters API.
