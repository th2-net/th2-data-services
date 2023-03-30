<!-- markdownlint-disable -->

# API Overview

## Modules

- [`th2_data_services.config`](./th2_data_services.config.md#module-th2data_servicesconfig)
- [`th2_data_services.config.config`](./th2_data_services.config.config.md#module-th2data_servicesconfigconfig)
- [`th2_data_services.data`](./th2_data_services.data.md#module-th2data_servicesdata)
- [`th2_data_services.event_tree`](./th2_data_services.event_tree.md#module-th2data_servicesevent_tree)
- [`th2_data_services.event_tree.etc_driver`](./th2_data_services.event_tree.etc_driver.md#module-th2data_servicesevent_treeetc_driver)
- [`th2_data_services.event_tree.event_tree`](./th2_data_services.event_tree.event_tree.md#module-th2data_servicesevent_treeevent_tree)
- [`th2_data_services.event_tree.event_tree_collection`](./th2_data_services.event_tree.event_tree_collection.md#module-th2data_servicesevent_treeevent_tree_collection)
- [`th2_data_services.event_tree.exceptions`](./th2_data_services.event_tree.exceptions.md#module-th2data_servicesevent_treeexceptions)
- [`th2_data_services.event_tree.parent_event_tree_collection`](./th2_data_services.event_tree.parent_event_tree_collection.md#module-th2data_servicesevent_treeparent_event_tree_collection)
- [`th2_data_services.exceptions`](./th2_data_services.exceptions.md#module-th2data_servicesexceptions)
- [`th2_data_services.interfaces`](./th2_data_services.interfaces.md#module-th2data_servicesinterfaces)
- [`th2_data_services.interfaces.adapter`](./th2_data_services.interfaces.adapter.md#module-th2data_servicesinterfacesadapter)
- [`th2_data_services.interfaces.command`](./th2_data_services.interfaces.command.md#module-th2data_servicesinterfacescommand)
- [`th2_data_services.interfaces.data_source`](./th2_data_services.interfaces.data_source.md#module-th2data_servicesinterfacesdata_source)
- [`th2_data_services.interfaces.source_api`](./th2_data_services.interfaces.source_api.md#module-th2data_servicesinterfacessource_api)
- [`th2_data_services.interfaces.struct`](./th2_data_services.interfaces.struct.md#module-th2data_servicesinterfacesstruct)
- [`th2_data_services.interfaces.stub_builder`](./th2_data_services.interfaces.stub_builder.md#module-th2data_servicesinterfacesstub_builder)
- [`th2_data_services.interfaces.utils`](./th2_data_services.interfaces.utils.md#module-th2data_servicesinterfacesutils)
- [`th2_data_services.interfaces.utils.converter`](./th2_data_services.interfaces.utils.converter.md#module-th2data_servicesinterfacesutilsconverter)
- [`th2_data_services.interfaces.utils.resolver`](./th2_data_services.interfaces.utils.resolver.md#module-th2data_servicesinterfacesutilsresolver)

## Classes

- [`config.TH2Config`](./th2_data_services.config.config.md#class-th2config)
- [`data.Data`](./th2_data_services.data.md#class-data): A wrapper for data/data_stream.
- [`etc_driver.IETCDriver`](./th2_data_services.event_tree.etc_driver.md#class-ietcdriver)
- [`event_tree.EventTree`](./th2_data_services.event_tree.event_tree.md#class-eventtree): EventTree is a tree-based data structure of events.
- [`event_tree_collection.EventTreeCollection`](./th2_data_services.event_tree.event_tree_collection.md#class-eventtreecollection): EventTreeCollection objective is building 'EventsTree's and storing them.
- [`exceptions.EventAlreadyExist`](./th2_data_services.event_tree.exceptions.md#class-eventalreadyexist)
- [`exceptions.EventIdNotInTree`](./th2_data_services.event_tree.exceptions.md#class-eventidnotintree)
- [`exceptions.EventRootExist`](./th2_data_services.event_tree.exceptions.md#class-eventrootexist)
- [`exceptions.FieldIsNotExist`](./th2_data_services.event_tree.exceptions.md#class-fieldisnotexist)
- [`exceptions.TreeLoop`](./th2_data_services.event_tree.exceptions.md#class-treeloop)
- [`parent_event_tree_collection.ParentEventTreeCollection`](./th2_data_services.event_tree.parent_event_tree_collection.md#class-parenteventtreecollection): ParentEventTreeCollections is a class like an EventsTreeCollections.
- [`exceptions.CommandError`](./th2_data_services.exceptions.md#class-commanderror): Exception raised for errors in the command.
- [`exceptions.EventNotFound`](./th2_data_services.exceptions.md#class-eventnotfound)
- [`exceptions.MessageNotFound`](./th2_data_services.exceptions.md#class-messagenotfound)
- [`adapter.IRecordAdapter`](./th2_data_services.interfaces.adapter.md#class-irecordadapter): Interface of Adapter for record.
- [`adapter.IStreamAdapter`](./th2_data_services.interfaces.adapter.md#class-istreamadapter): Interface of Adapter for streams.
- [`command.ICommand`](./th2_data_services.interfaces.command.md#class-icommand): High level interface for Command.
- [`data_source.IDataSource`](./th2_data_services.interfaces.data_source.md#class-idatasource)
- [`source_api.ISourceAPI`](./th2_data_services.interfaces.source_api.md#class-isourceapi): High level interface for Source API.
- [`struct.IEventStruct`](./th2_data_services.interfaces.struct.md#class-ieventstruct): Just to mark Event Struct class.
- [`struct.IMessageStruct`](./th2_data_services.interfaces.struct.md#class-imessagestruct): Just to mark Message Struct class.
- [`stub_builder.IEventStub`](./th2_data_services.interfaces.stub_builder.md#class-ieventstub): Just to mark Event Stub class.
- [`stub_builder.IMessageStub`](./th2_data_services.interfaces.stub_builder.md#class-imessagestub): Just to mark Message Stub class.
- [`stub_builder.IStub`](./th2_data_services.interfaces.stub_builder.md#class-istub)
- [`converter.ITimestampConverter`](./th2_data_services.interfaces.utils.converter.md#class-itimestampconverter)
- [`resolver.EventFieldsResolver`](./th2_data_services.interfaces.utils.resolver.md#class-eventfieldsresolver)
- [`resolver.MessageFieldsResolver`](./th2_data_services.interfaces.utils.resolver.md#class-messagefieldsresolver)

## Functions

- No functions


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
