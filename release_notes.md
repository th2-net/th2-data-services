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

# v0.5.3

## BugFixes

1. [TH2-2756] Changed adapter for messages from pipeline.
2. Fixed a situation when messages were not opened from the list when we use map more that once.

# v0.6.0

## User impact and migration instructions

1. [I] The "metadataOnly" query parameter will now always be set to False in the get_X_from_data_provider methods. It's
   the option for Report Viewer front-end only.
   [M] (Optional) Remove "metadataOnly" parameter in your requests to get more logical and clean code.

## Improvements

1. [TH2-2471] The "metadataOnly" query parameter will now always be set to False in the get_X_from_data_provider
   methods.

## Features

1. You can import classes directly from th2_data_services now.
   E.g. `from th2_data_services import Data, DataSource, Filter`
2. [TH2-2755] Added new parameters to DataSource methods.
    1. get_X_from_data_provider:
        - sse_adapter=True. If True, all data will go through SSE adapter and yield dicts. Otherwise adapter will yield
          SSE Events.
    2. get_messages_from_data_provider and find_messages_by_id_from_data_provider:
        - provider_adapter=adapter_provider5. Adapter function for rpt-data-provider. If None, Data object will yield
          object from previous map function.
3. [TH2-2283] Implemented rpt-data-provider Filters API.
4. [TH2-2656] Added new optional parameter to EventsTree (ParentEventsTree) classes.
    - Set "preserve_body=True" to keep event bodies during tree building.
    - Otherwise events bodies will be omitted.

# v0.6.1

## BugFixes

1. [TH2-2858] Resolved HTTP error 414 on a client side.
2. [TH2-2851] UnicodeDecodeError is raised during events extracting if not utf-8 character in the byte stream. User will
   get original byte now.

# v0.6.2

## BugFixes

1. [TH2-2922] Fixed infinite loop in events tree.

# v0.6.3

## BugFixes

1. [TH2-3168] Fixed iterations in nested loops for Data object with limit.
2. [TH2-3336] Url now uses the utf-8 encoding.
3. [TH2-3700] Filter iterate values only once - fixed.

# v1.0.0

The main goal of the release 1.0.0 is to implement new architecture that solves many of extension's problems.
It also allows you to create your own Commands/DataSources/SourceAPIs.

## Attention

The new version has raised the major version. It means the users should update their code to work with the new DS lib.

Version 0.6.x won't have new features but will have bug fixes.

Version 1.x.y doesn't use any adapters by default, 0.6.x does. If you need the save behavior as previous,
use `CodecPipelinesAdapter` manually.

## User impact and migration instructions

1. [I] There is no more old-style DataSource class.
   [M] Use a specific class for your purposes (HTTPDataSource or GRPCDataSource).
2. [I] There are no more `get_x` methods in the DataSource classes. Instead, it has the command method. This method
   takes an object of the Command class.
   [M] So if you used `data_source.get_events_from_data_provider` use `data_source.command(GetEvents(ARGS))` instead.
   from `data_source.get_messages_from_data_provider` to `data_source.command(GetMessages(ARGS).apply_adapter(
   codec_pipeline_adapter))`
   from `find_messages_by_id_from_data_provider` to `GetMessagesById` or `GetMessageById`
   from `find_events_by_id_from_data_provider` to `GetEventsById` or `GetEventById`
   if you used broken_events parameter initialize the command with use_stub=True parameter.
3. [I] Modules structure was changed.
   [M] You need to change some import paths.
4. [I] All class constructors/methods have got explicit arguments.
   [M] Change old args names to new if required.
5. [I] Set of classes to create `EventsTree` representation was significantly changed.
   [M] Use `EventsTreesCollection` instead of `EventsTree`. `EventsTree` is a real tree structure now.
   Note, `EventsTreesCollection` has other methods, see the example to understand how to work with it.
6. [I] `EventsTree2` was removed.
   [M] Use `EventsTreesCollection` instead.
7. [I] Exceptions were updated.
   [M] Update your try-except statements

## Improvements

1. [TH2-3247] Move DS version 1.0.0 to python 3.7+
2. [TH2-3404] Exceptions were updated. Implemented library-based exceptions.
3. [TH2-3213] Old `data_source` module was removed.

## Features

1. [TH2-2465] Added the module `th2_gui_report` to create a link by event id or message id.
2. [TH2-2274] rpt-data-provider GRPC interface was implemented.
3. [TH2-3194] New `EventsTree` solution implemented. It includes the best parts from previous trees.
   The tree also got a lot of useful methods to work with it ([see doc](documentation/api/events_tree.events_tree.md)).
4. [TH2-2942] Pure Provider v5 APIs implemented: `GRPCProvider5API`, `HTTPProvider5API`.
5. [TH2-2944] Developed commands for http and grpc instead of `data_source` get/find methods.
6. [TH2-2994] Provider v5 data source classes implemented: `GRPCProvider5DataSource`, `HTTPProvider5DataSource`.
7. [TH2-2941] Interface classes implemented:  `ISourceAPI`, `IDataSource`, `ICommand`, `IAdapter`.

## BugFixes

1. [TH2-3168] Fixed iterations in nested loops for Data object with limit.
2. [TH2-3354] API Doc generator issue fixed.
3. [TH2-3216] Incorrect work of Data object with multi-looping with cache enabled fixed.

# v1.0.1

## BugFixes

1. [TH2-3470] Fixed cache in commands GetEvents and GetMessages for http-provider.
2. [TH2-3337] Url now use utf-8 encoding.
3. [TH2-3474] Parentless tree has stub event instead empty event now.
4. [TH2-3756] Change filepath for cache file due to character limit (':') in Windows

## Improvements

1. [TH2-3493] The method recover_unknown_events has become public.

# v1.0.2

## BugFixes

1. [TH2-3700] Filter iterate values only once - fixed.

# v1.0.3

## BugFixes

1. [TH2-3739] GRPCProvider5API is based on grpc v0.1.6 now.

# v1.1.0

## User impact and migration instructions

This release is not required any additional steps to use.

## Features

1. [TH2-3497] EventsTreeCollection got `get_leaves_iter` method.
2. [TH2-3497] EventsTreeCollection got `len_trees` and `len_detached_events` properties.
3. [TH2-3497] EventsTree and EventsTreeCollection got representation(`__repr__`) and `summary` methods.
4. [TH2-3558] Added module-level functions `add_stderr_logger` and `add_file_logger` to easily enable logging.
5. [TH2-3546][TH2-3583] `INTERACTIVE_MODE` - global parameter was introduced.
6. `Data.use_cache()` <- True by default.
7. Added data methods to get cache files paths `Data.get_cache_filepath()` and `Data.get_pending_cache_filepath()`.
8. [TH2-3665] Added method get_tree_by_id in ETC.
9. [TH2-3592] Added logging in EventsTreeCollection module when ETC create with detached events.
10. [TH2-3475] Implement Data objects joining
11. [TH2-3467] Added utils classes to convert timestamps.
12. [TH2-3662][TH2-3492] Added `get_detached_events_iter` and `get_detached_events` methods in EventsTreeCollections.
    * Warning: Property `detached_events` is deprecated and will be removed in the future.
13. [TH2-3496] Added get_parentless_tree_collection method in EventsTreeCollection.
14. [TH2-3905] Separate filer classes added instead of `th2_data_services.Filter` class.
    * Warning: Class `th2_data_services.Filter` is deprecated and will be removed in the future.

## Improvements

1. [TH2-3003] Added automatic attachment of example.py code in readme.md.
2. [TH2-3558] Added more debug info about Data cache using.
3. [TH2-3389] GetXById http-provider command handles 404 error status instead of JsonDecodeException.
4. [TH2-3663] Speed up len_detached_events property

## BugFixes

1. [TH2-3557][TH2-3560] Parent Data cache file will be created if you iterate a child Data object now.
2. [TH2-3545][TH2-3580] The Data object now uses an absolute path, so it doesn't lose its cache file if you change the
   working directory.
3. [TH2-3546][TH2-3583] Data cache file will not be removed if you use `INTERACTIVE_MODE` and the file is being read.
4. [TH2-3487][TH2-3585] `data = Data(source_data, cache=True).map(func)` Data object didn't write the cache in such case
   before. Fixed.
5. [TH2-3558] Used loggers name fixed. Changed to __name__.
6. [TH2-3733] Provider API class generate standard URL (without duplicate '/' and '/' before query)
7. [TH2-3598] Method get_subtree returns tree as EventsTree class.
8. [TH2-3593][TH2-3664] Method get_root_by_id returns root by any non-root ID as Th2Event.
9. [TH2-3595] When ETC creates subtree or itself ETC doesn't copy incoming data-stream.
10. [TH2-3732] Log message in http.GetMessages contains name of the stream.
11. [TH2-3734] EventsTreeCollection append_event method doesn't add duplicate event.
12. [TH2-3596][TH2-3594][TH2-3473] EventsTreeCollections. Get or find methods includes parentless results, if parentless
    exists.

# v1.1.1

## BugFixes

1. [TH2-4039] An empty filter is validated.

# v1.2.0

## User impact and migration instructions

This release implements rdp v6 support that requres new grpc version. It means you cannot connect to rdp5.grpc and
rdp6.grpc via the same environment. This DS lib version will have grpc version for rdp v6 == th2-grpc-data-provider
v1.1.0.

1. [I] The new version of grpc has been added.
   [M] If you require the rdp v6 version of the interface, you do not need to do anything.
   Otherwise, you need to reinstall th2-grpc-data-provider lib to the required one for your rdp.

More detail in [here](https://github.com/th2-net/th2-data-services/tree/dev_1.2.0#grpc-provider-warning)

## Features

1. [TH2-3083] The problem with several versions of the grpc interface is solved.
2. [TH2-3512] Provider V6 module is developed.
3. [TH2-4141] Option to disable ssl certificate for rdp5 is added.
4. [TH2-4098] Added Streams class for the param 'stream'.

# BugFixes

1. [TH2-4072] Now ETC doesn't raise a warning for missing detached_events.
2. GRPC requests (start_timestamp, end_timestamp) are now made in UTC.

# v1.2.1

# BugFixes

1. Added missing library importlib_metadata.

# v1.2.2

## BugFixes

1. [TH2-4195] EventsTree without parent raises `EventIdNotInTree` exception when trying to use `get_parent()` method.

# v1.2.3

## BugFixes

1. [TH2-4234] The library can now be run on Windows.

# v1.3.0

## User impact and migration instructions

This release implements performance bug fixes and provides Data object cache file saving and loading.

1. [I] Logging were removed from library. Only special builds will have logging.
   User cannot use `add_stderr_logger` and  `add_file_logger` logging functions.
   [M] Remove DS lib logging usage anywhere.
2. [I] Since `v1.3.0`, the library doesn't provide data source dependencies.
   [M] You should provide it manually during installation.
   You just need to add square brackets after library name and put dependency name.

      ```
      pip install th2-data-services[dependency_name]
      ```

      **Dependencies list**

      | dependency name | provider version |
      |:---------------:|:----------------:|
      |      RDP5       |        5         |
      |      RDP6       |        6         |

      **Example**

      ```
      pip install th2-data-services[rdp5]
      ```

## Features

1. [TH2-4289] Data.build_cache and Data.from_cache_file features were added.
2. Added `Data.cache_status` property

## Improvements

1. [TH2-4379] Speed improvements in json deserialization.
    - StreamingSSEAdapter will now handle bytes from sse-stream into Dict objects.
    - SSEAdapter is now deprecated class.
2. Data object will generate a warning if you put to it an object that has generator type.

## BugFixes

1. [TH2-4385] Logging in Data object slows down the ds library very much.
    - Logging was removed.
    - `add_stderr_logger` and  `add_file_logger` are not available anymore.
2. [TH2-4380] Fixed apply_adpater feature for GetMessages / GetEvents / GetEventById / GetMessageById
3. [TH2-3767] Fixed bug with limit of Data object in Windows.
4. [TH2-4460] Fixed bug where GRPC omitted fields with None value in response.

# v1.4.0

## Feature
1. [TH2-4601] Added `clear_cache` method to data object to remove cache file.

## BugFixes
1. [TH2-4603] Fix += joining feature. Now it keeps cache status.
2. [TH2-4604] `Data.from_cache_file` method has return value now.
3. [TH2-4839] Changed FileExistsError to FileNotFoundError in Data.from_cache_file method

# v2.0.0

## User impact and migration instructions

By installing the package you will no longer get RDP package.
If you want to use RDP you have to specify dependency in square brackets `[ ]`

1. [I] Adapter interface got required handle_stream method.\
   [M] Implement new method for your adapters.

2. [I] It's no longer possible to import Data object directly from
   th2_data_services package.\
   [M] All records should be changed from "from th2_data_services import Data"
   to "from th2_data_services.data import Data".

3. [I] Provider module is removed.\
   [M] You should use data source implementations, like th2-ds-source-lwdp.

4. [I] INTERACTIVE_MODE cannot be accessed like
   th2_data_services.INTERACTIVE_MODE anymore.\
   [M] It's now changed to th2_data_services.config.options.INTERACTIVE_MODE

5. [I] EventsTree renamed to EventTree\
   [M] All records should be changed to EventTree

6. [I] Message utils method `expand_message` moved into `MessageFieldResolver`.\
   [M] Implement new method in your resolver.

7. [I] Data iteration logic is changed.\
   Why? Current behavior causes problems in some cases. E.g. when we don't want
   to iterate objects inside the DataSet.

   [I.1]  Lists and tuples used in building Data objects are treated as single
   item and items inside them aren't iterated anymore.\
   [M.1] Update Data objects initialized with lists or tuples.

   [I.2] Change in iteration logic also changed how `map` function behaves.
   If `map` function returns lists or tuples their content won't be iterated
   anymore.\
   [M.2.1] If you are interest previous `map` function behavior, just update `map`
   to `map_yield`.
   
   [M.2.2] Update `data.map(mfr.expand_message)` to `data.map_yield(mfr.expand_message)`

   [I.3] Data object will not iterate over contents of its stream if any of the
   items are iterables (but not Data object).\
   It means that Data object will not iterate lists and tuples inside the
   provided DataSet and will return they as is.\
   Only exception will be if all of the items are Data objects themselves.\
   [M.3] Update nested lists in Data object initializations to either Data
   objects or switch to using addition operator.\
   [Examples]\
      `d1 = Data(['a', 'b'])`\
      a. `Data([1, 2, [3, 4], d1])` will yield 1,2,[3,4],d1.  Prev. behavior: 1,2,3,4,'a','b'\
      b. `Data([d1, d2])` where d1 and d2 are Data objects. It will yield from d1, and after that yield from d2.\
      c. You can update the example from `a` to `Data([1,2,3,4])` or to `new_data = Data([1,2]) + Data([3,4]) + d1`.\
      d. You also can return prev behaviour doing the following:  `new_data = Data([1, 2, [3, 4], d1]).map_yield(lambda r: r)`
 
8. [I] A new version of `orjson` lib require python 3.8+.
   [M] Change your python version if you use 3.7 to 3.8+.

## Features

1. [TH2-4128] pip no longer installs RDP by default
2. [TH2-4128][TH2-4738] extra dependencies can be installed using square brackets after
   package name.
   - Example: `pip install th2-data-services[lwdp]`

   Available data sources implementations:

   |  dependency name  | provider version                      |
   |:-----------------:|---------------------------------------|
   |       lwdp        | latest version of lwdp                |
   |       lwdp2       | latest version of lwdp v2             |
   |       lwdp3       | latest version of lwdp v3             |
   | utils-rpt-viewer  | latest version of utils-rpt-viewer    |
   | utils-rpt-viewer5 | latest version of utils-rpt-viewer v5 |
   |   utils-advanced  | latest version of ds-utils            |

3. [TH2-4493] Adapter interface got handle_stream method.
4. [TH2-4490] Added `map_stream` method to Data.
   - Almost same as `map`, except it's designed to handle a stream of data
     rather than a single record.
   - Method accepts a generator function or a class which implements
     IStreamAdapter with generator function.
5. [TH2-4582] IAdapter interface removed.
   - IStreamAdapter interface added to handle streams.
   - IRecordAdapter interface added to handle single record.
   - Method accepts Generator function or IStreamAdapter interface class with
     Generator function.
6. [TH2-4609] Data.filter implementation changed to use `yield`.
7. [TH2-4491] metadata attribute added to Data. It will contain request urls.
8. [TH2-4577] map method now can take either Callable function or Adapter which
   implements IRecordAdapter.
9. [TH2-4611] DatetimeConverter, ProtobufTimestampConverter converters added.
10. [TH2-4646]
   - metadata gets carried when using Data methods.
   - update_metadata method added to update metadata.
11. [TH2-4684] Tree names changed from plural to singular. (e.g Event**s**
    Tree -> EventTree)
12. [TH2-4693] Implemented namespace packages structure, allowing other th2
    libraries to be grouped together.
13. [TH2-4713] Added options module which enables user to tweak library
    settings.
14. `DummyDataSource` added.
15. [TH2-4881] `Data.from_json` method was added.
16. [TH2-4919] `Data.from_any_file` method was added.
17. [TH2-4928] `Data.from_csv` method was added.
18. [TH2-4932] `Data.to_json` method was added. Puts your data to a valid json
    object.
19. [TH2-4957] Added `gzip` option for `Data.to_json` method.
20. [TH2-4957] Added `decompress_gzip_file` function to utils.converters.
21. Added `to_csv` method to `PerfectTable` class.
22. `utils.converters.flatten_dict` converter added.
23. Added `Data.to_jsons` method that put your data object to jsons file
    (file where every line is separate json-format line. That's not a valid json
    format.)
   Renamed `to_jsons` to `to_json_lines` later.
   - to_jsons -- is deprecated now.
24. [TH2-5049] Added ExpandedMessageFieldResolver
25. [TH2-5053] Added `pickle_version` to Data.from_cache_file method.
26. `decode_base64` function added to converter utils.
27. [TH2-5156] `UniversalDatetimeStringConverter` and `UnixTimestampConverter`
    added.
28. [TH2-5167] `Data.is_sorted`, `event_utils.is_sorted`, `message_utils.is_sorted`
    and `stream_utils.is_sorted` methods were added.
29. [TH2-5176] `to_th2_timestamp` method was added for converters.
30. [TH2-5081] Added `map_yield` function, that should behave similar to
    old `map` method.
    That means that `map_yield` will iterate lists and tuples if the user map
    function returns them.
31. [TH2-5197] Added the function `read_all_pickle_files_from_the_folder` 
    to get Data object from the folder with pickle files.
32. [TH2-5213] Added `Data.to_csv` method, that converts data to valid csv.
33. [TH2-4900] Added `Data.sort` method, that also works with large amount of Data.

## BugFixes

1. [TH2-4711] EventTreeCollection max_count parameter of findall functions
   worked wrongly.
2. [TH2-4917] Readme duplicates removed.
3. [TH2-5083] Fixed comparison line formatting. Every event in block isn't
   formatted as failed now if parent is failed.
4. [TH2-5081] Fixed iteration bug for case where Data object was made using
   lists and tuple.
5. [TH2-5100] Fixed bug when we get Recursion Exception if we have too much
   number of Data objects that iterate each other.
6. [TH2-5190] Fixed Data.to_json
7. [TH2-5193] orjson versions 3.7.0 through 3.9.14 library has vulnerability
   https://devhub.checkmarx.com/cve-details/CVE-2024-27454/. 
8. [TH2-5201] Fixed DatetimeStringConverter.to_th2_timestamp() bug which occurred for inputs not ending with 'Z'.
9. [TH2-5902] Fixed bug when cache file was removed after calling data.show().
10. [TH2-5220] Fixed bug when Data.update_metadata() would change a string into a list.
11. [TH2-5101] Fixed bug when merging date objects via + or +=  overwrites the source file. 

## Improvements

1. Added vulnerabilities scanning
2. [TH2-4828] EventNotFound and MessageNotFound now return error description as
   argument instead of pre-written one.
3. [TH2-4775] Speed up `Data.build_cache` by disabling garbage collection at the
   time of storing pickle file.
4. [TH2-4901] Added gap_mode and zero_anchor parameters for message and event
   utils get_category_frequencies methods. 
   [See doc](documentation/frequencies.md)
5. [TH2-5048] Added typing hints for resolver methods.
6. [TH2-5172] Add faster implementations of the following
   ProtobufTimestampConverter functions: to_microseconds, to_milliseconds,
   to_nanoseconds.
7. [TH2-5081] `Data.__str__` was changed --> use `Data.show()` instead of `print(data)`
8. [TH2-5201] Performance improvements have been made to converters:
9. [TH2-5101] Data.update_metadata() now takes `change_type` argument (values: `update` default, `change` which denotes 
whether to update or overwrite with new values.
10. [TH2-5099] Fixed slow iteration for Data objects created with many addition operators.

Benchmark.
- 1mln iterations per test
- input: 2022-03-05T23:56:44.123456789Z

| Converter                        | Method           | Before (seconds) | After (seconds) | Improvement (rate) |
|----------------------------------|------------------|------------------|-----------------|--------------------|
| DatetimeStringConverter          | parse_timestamp  | 7.1721964        | 1.4974268       | x4.78              |
|                                  | to_datetime      | 8.9945099        | 0.1266325       | x71.02             |
|                                  | to_seconds       | 8.6180093        | 1.5360991       | x5.62              |
|                                  | to_microseconds  | 7.9066440        | 1.7628856       | x4.48              |
|                                  | to_nanoseconds   | 7.6787507        | 1.7114960       | x4.48              |
|                                  | to_milliseconds  | 7.6059985        | 1.7688387       | x4.29              |
|                                  | to_datetime_str  | 8.3861742        | 2.3781561       | x3.52              |
|                                  | to_th2_timestamp | 7.7702033        | 1.5942235       | x4.87              |
| UniversalDatetimeStringConverter | parse_timestamp  | 7.4161371        | 1.5752227       | x4.7               |
|                                  | to_datetime      | 8.2108218        | 0.1267797       | x64.76             |
|                                  | to_seconds       | 7.7745484        | 1.6453126       | x4.72              |
|                                  | to_microseconds  | 7.7569293        | 1.8240784       | x4.25              |
|                                  | to_nanoseconds   | 7.7879700        | 1.7930200       | x4.34              |
|                                  | to_milliseconds  | 7.8168710        | 1.8308856       | x4.26              |
|                                  | to_datetime_str  | 8.7388529        | 2.4592992       | x3.55              |
|                                  | to_th2_timestamp | 7.8972679        | 1.6856898       | x4.68              |

Other converters also have some not big speed improvements.

9. [TH2-5213] Extend cache_files_reading_speed with csv support.
