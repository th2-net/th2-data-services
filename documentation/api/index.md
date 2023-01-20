<!-- markdownlint-disable -->

# API Overview

## Modules

- [`data`](./data.md#module-data)
- [`decode_error_handler`](./decode_error_handler.md#module-decode_error_handler)
- [`events_tree`](./events_tree.md#module-events_tree)
- [`events_tree.etc_driver`](./events_tree.etc_driver.md#module-events_treeetc_driver)
- [`events_tree.event_tree`](./events_tree.event_tree.md#module-events_treeevent_tree)
- [`events_tree.event_tree_collection`](./events_tree.event_tree_collection.md#module-events_treeevent_tree_collection)
- [`events_tree.exceptions`](./events_tree.exceptions.md#module-events_treeexceptions)
- [`events_tree.parent_event_tree_collection`](./events_tree.parent_event_tree_collection.md#module-events_treeparent_event_tree_collection)
- [`exceptions`](./exceptions.md#module-exceptions)
- [`interfaces`](./interfaces.md#module-interfaces)
- [`interfaces.adapter`](./interfaces.adapter.md#module-interfacesadapter)
- [`interfaces.command`](./interfaces.command.md#module-interfacescommand)
- [`interfaces.data_source`](./interfaces.data_source.md#module-interfacesdata_source)
- [`interfaces.source_api`](./interfaces.source_api.md#module-interfacessource_api)
- [`interfaces.struct`](./interfaces.struct.md#module-interfacesstruct)
- [`interfaces.stub_builder`](./interfaces.stub_builder.md#module-interfacesstub_builder)
- [`interfaces.utils`](./interfaces.utils.md#module-interfacesutils)
- [`interfaces.utils.converter`](./interfaces.utils.converter.md#module-interfacesutilsconverter)
- [`sse_client`](./sse_client.md#module-sse_client)
- [`utils`](./utils.md#module-utils)
- [`utils.converters`](./utils.converters.md#module-utilsconverters)

## Classes

- [`data.Data`](./data.md#class-data): A wrapper for data/data_stream.
- [`etc_driver.IETCDriver`](./events_tree.etc_driver.md#class-ietcdriver)
- [`event_tree.EventTree`](./events_tree.event_tree.md#class-eventtree): EventTree is a tree-based data structure of events.
- [`event_tree_collection.EventTreeCollection`](./events_tree.event_tree_collection.md#class-eventtreecollection): EventTreeCollection objective is building 'EventsTree's and storing them.
- [`exceptions.EventAlreadyExist`](./events_tree.exceptions.md#class-eventalreadyexist)
- [`exceptions.EventIdNotInTree`](./events_tree.exceptions.md#class-eventidnotintree)
- [`exceptions.EventRootExist`](./events_tree.exceptions.md#class-eventrootexist)
- [`exceptions.FieldIsNotExist`](./events_tree.exceptions.md#class-fieldisnotexist)
- [`exceptions.TreeLoop`](./events_tree.exceptions.md#class-treeloop)
- [`parent_event_tree_collection.ParentEventTreeCollection`](./events_tree.parent_event_tree_collection.md#class-parenteventtreecollection): ParentEventTreeCollections is a class like an EventsTreeCollections.
- [`exceptions.CommandError`](./exceptions.md#class-commanderror): Exception raised for errors in the command.
- [`exceptions.EventNotFound`](./exceptions.md#class-eventnotfound)
- [`exceptions.MessageNotFound`](./exceptions.md#class-messagenotfound)
- [`adapter.IRecordAdapter`](./interfaces.adapter.md#class-irecordadapter): Interface of Adapter for record.
- [`adapter.IStreamAdapter`](./interfaces.adapter.md#class-istreamadapter): Interface of Adapter for streams.
- [`command.IAdaptableCommand`](./interfaces.command.md#class-iadaptablecommand)
- [`command.ICommand`](./interfaces.command.md#class-icommand): High level interface for Command.
- [`data_source.IDataSource`](./interfaces.data_source.md#class-idatasource)
- [`source_api.ISourceAPI`](./interfaces.source_api.md#class-isourceapi): High level interface for Source API.
- [`struct.IEventStruct`](./interfaces.struct.md#class-ieventstruct): Just to mark Event Struct class.
- [`struct.IMessageStruct`](./interfaces.struct.md#class-imessagestruct): Just to mark Message Struct class.
- [`stub_builder.IEventStub`](./interfaces.stub_builder.md#class-ieventstub): Just to mark Event Stub class.
- [`stub_builder.IMessageStub`](./interfaces.stub_builder.md#class-imessagestub): Just to mark Message Stub class.
- [`stub_builder.IStub`](./interfaces.stub_builder.md#class-istub)
- [`converter.ITimestampConverter`](./interfaces.utils.converter.md#class-itimestampconverter)
- [`sse_client.SSEClient`](./sse_client.md#class-sseclient): Patch for sseclient-py to get availability to configure decode error handler.
- [`converters.DatetimeConverter`](./utils.converters.md#class-datetimeconverter): Converts datetime objects to timestamp.
- [`converters.DatetimeStringConverter`](./utils.converters.md#class-datetimestringconverter): Converts datetime strings.
- [`converters.ProtobufTimestampConverter`](./utils.converters.md#class-protobuftimestampconverter): Converts Th2 timestamps.

## Functions

- [`decode_error_handler.handler`](./decode_error_handler.md#function-handler): Decode error handler that tries change utf-8 character to Unicode.


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
