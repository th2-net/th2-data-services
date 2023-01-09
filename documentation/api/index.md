<!-- markdownlint-disable -->

# API Overview

## Modules

- [`data`](./data.md#module-data)
- [`decode_error_handler`](./decode_error_handler.md#module-decode_error_handler)
- [`events_tree`](./events_tree.md#module-events_tree)
- [`events_tree.events_tree`](./events_tree.events_tree.md#module-events_treeevents_tree)
- [`events_tree.exceptions`](./events_tree.exceptions.md#module-events_treeexceptions)
- [`exceptions`](./exceptions.md#module-exceptions)
- [`interfaces`](./interfaces.md#module-interfaces)
- [`interfaces.adapter`](./interfaces.adapter.md#module-interfacesadapter)
- [`interfaces.command`](./interfaces.command.md#module-interfacescommand)
- [`interfaces.data_source`](./interfaces.data_source.md#module-interfacesdata_source)
- [`interfaces.events_tree`](./interfaces.events_tree.md#module-interfacesevents_tree)
- [`interfaces.events_tree.events_tree_collection`](./interfaces.events_tree.events_tree_collection.md#module-interfacesevents_treeevents_tree_collection)
- [`interfaces.events_tree.parent_events_tree_collection`](./interfaces.events_tree.parent_events_tree_collection.md#module-interfacesevents_treeparent_events_tree_collection)
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
- [`events_tree.EventsTree`](./events_tree.events_tree.md#class-eventstree): EventsTree is a tree-based data structure of events.
- [`exceptions.EventIdNotInTree`](./events_tree.exceptions.md#class-eventidnotintree)
- [`exceptions.FieldIsNotExist`](./events_tree.exceptions.md#class-fieldisnotexist)
- [`exceptions.CommandError`](./exceptions.md#class-commanderror): Exception raised for errors in the command.
- [`exceptions.EventNotFound`](./exceptions.md#class-eventnotfound)
- [`exceptions.MessageNotFound`](./exceptions.md#class-messagenotfound)
- [`adapter.IRecordAdapter`](./interfaces.adapter.md#class-irecordadapter): Interface of Adapter for record.
- [`adapter.IStreamAdapter`](./interfaces.adapter.md#class-istreamadapter): Interface of Adapter for streams.
- [`command.IAdaptableCommand`](./interfaces.command.md#class-iadaptablecommand)
- [`command.ICommand`](./interfaces.command.md#class-icommand): High level interface for Command.
- [`data_source.IDataSource`](./interfaces.data_source.md#class-idatasource)
- [`events_tree_collection.EventsTreeCollection`](./interfaces.events_tree.events_tree_collection.md#class-eventstreecollection): EventsTreeCollection objective is building 'EventsTree's and storing them.
- [`parent_events_tree_collection.ParentEventsTreeCollection`](./interfaces.events_tree.parent_events_tree_collection.md#class-parenteventstreecollection): ParentEventsTreeCollections is a class like an EventsTreeCollections.
- [`source_api.ISourceAPI`](./interfaces.source_api.md#class-isourceapi): High level interface for Source API.
- [`struct.IEventStruct`](./interfaces.struct.md#class-ieventstruct): Just to mark Event Struct class.
- [`struct.IMessageStruct`](./interfaces.struct.md#class-imessagestruct): Just to mark Message Struct class.
- [`stub_builder.IEventStub`](./interfaces.stub_builder.md#class-ieventstub): Just to mark Event Stub class.
- [`stub_builder.IMessageStub`](./interfaces.stub_builder.md#class-imessagestub): Just to mark Message Stub class.
- [`stub_builder.IStub`](./interfaces.stub_builder.md#class-istub)
- [`converter.ITimestampConverter`](./interfaces.utils.converter.md#class-itimestampconverter)
- [`sse_client.SSEClient`](./sse_client.md#class-sseclient): Patch for sseclient-py to get availability to configure decode error handler.
- [`converters.ProtobufTimestampConverter`](./utils.converters.md#class-protobuftimestampconverter): Converts datetime strings.

## Functions

- [`decode_error_handler.handler`](./decode_error_handler.md#function-handler): Decode error handler that tries change utf-8 character to Unicode.


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
