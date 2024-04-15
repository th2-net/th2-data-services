<!-- markdownlint-disable -->

# API Overview

## Modules

- [`config`](./config.md#module-config)
- [`config.config`](./config.config.md#module-configconfig)
- [`data`](./data.md#module-data)
- [`event_tree`](./event_tree.md#module-event_tree)
- [`event_tree.etc_driver`](./event_tree.etc_driver.md#module-event_treeetc_driver)
- [`event_tree.event_tree`](./event_tree.event_tree.md#module-event_treeevent_tree)
- [`event_tree.event_tree_collection`](./event_tree.event_tree_collection.md#module-event_treeevent_tree_collection)
- [`event_tree.exceptions`](./event_tree.exceptions.md#module-event_treeexceptions)
- [`event_tree.parent_event_tree_collection`](./event_tree.parent_event_tree_collection.md#module-event_treeparent_event_tree_collection)
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
- [`interfaces.utils.resolver`](./interfaces.utils.resolver.md#module-interfacesutilsresolver)

## Classes

- [`config.TH2Config`](./config.config.md#class-th2config)
- [`data.Data`](./data.md#class-data): A wrapper for data/data_stream.
- [`data.DataWorkflow`](./data.md#class-dataworkflow)
- [`data.WfLimitRecord`](./data.md#class-wflimitrecord): WfLimitRecord(type: str, callback: Callable, limit: int)
- [`etc_driver.IETCDriver`](./event_tree.etc_driver.md#class-ietcdriver)
- [`event_tree.EventTree`](./event_tree.event_tree.md#class-eventtree): EventTree is a tree-based data structure of events.
- [`event_tree_collection.EventTreeCollection`](./event_tree.event_tree_collection.md#class-eventtreecollection): EventTreeCollection objective is building 'EventsTree's and storing them.
- [`exceptions.EventAlreadyExist`](./event_tree.exceptions.md#class-eventalreadyexist)
- [`exceptions.EventIdNotInTree`](./event_tree.exceptions.md#class-eventidnotintree)
- [`exceptions.EventRootExist`](./event_tree.exceptions.md#class-eventrootexist)
- [`exceptions.FieldIsNotExist`](./event_tree.exceptions.md#class-fieldisnotexist)
- [`exceptions.TreeLoop`](./event_tree.exceptions.md#class-treeloop)
- [`parent_event_tree_collection.ParentEventTreeCollection`](./event_tree.parent_event_tree_collection.md#class-parenteventtreecollection): ParentEventTreeCollections is a class like an EventsTreeCollections.
- [`exceptions.CommandError`](./exceptions.md#class-commanderror): Exception raised for errors in the command.
- [`exceptions.EventNotFound`](./exceptions.md#class-eventnotfound)
- [`exceptions.MessageNotFound`](./exceptions.md#class-messagenotfound)
- [`adapter.IRecordAdapter`](./interfaces.adapter.md#class-irecordadapter): Interface of Adapter for record.
- [`adapter.IStreamAdapter`](./interfaces.adapter.md#class-istreamadapter): Interface of Adapter for streams.
- [`command.ICommand`](./interfaces.command.md#class-icommand): High level interface for Command.
- [`data_source.IDataSource`](./interfaces.data_source.md#class-idatasource)
- [`source_api.ISourceAPI`](./interfaces.source_api.md#class-isourceapi): High level interface for Source API.
- [`struct.IEventStruct`](./interfaces.struct.md#class-ieventstruct): Just to mark Event Struct class.
- [`struct.IMessageStruct`](./interfaces.struct.md#class-imessagestruct): Just to mark Message Struct class.
- [`stub_builder.IEventStub`](./interfaces.stub_builder.md#class-ieventstub): Just to mark Event Stub class.
- [`stub_builder.IMessageStub`](./interfaces.stub_builder.md#class-imessagestub): Just to mark Message Stub class.
- [`stub_builder.IStub`](./interfaces.stub_builder.md#class-istub)
- [`converter.ITimestampConverter`](./interfaces.utils.converter.md#class-itimestampconverter)
- [`resolver.EventFieldResolver`](./interfaces.utils.resolver.md#class-eventfieldresolver)
- [`resolver.EventFieldResolver`](./interfaces.utils.resolver.md#class-eventfieldresolver)
- [`resolver.ExpandedMessageFieldResolver`](./interfaces.utils.resolver.md#class-expandedmessagefieldresolver)
- [`resolver.MessageFieldResolver`](./interfaces.utils.resolver.md#class-messagefieldresolver)
- [`resolver.MessageFieldResolver`](./interfaces.utils.resolver.md#class-messagefieldresolver)
- [`resolver.SubMessageFieldResolver`](./interfaces.utils.resolver.md#class-submessagefieldresolver)

## Functions

- No functions


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
