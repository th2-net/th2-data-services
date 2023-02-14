<!-- markdownlint-disable -->

# API Overview

## Modules

- [`th2.data_services.config`](./th2.data_services.config.md#module-th2data_servicesconfig)
- [`th2.data_services.config.config`](./th2.data_services.config.config.md#module-th2data_servicesconfigconfig)
- [`th2.data_services.data`](./th2.data_services.data.md#module-th2data_servicesdata)
- [`th2.data_services.event_tree`](./th2.data_services.event_tree.md#module-th2data_servicesevent_tree)
- [`th2.data_services.event_tree.common_event_tree`](./th2.data_services.event_tree.common_event_tree.md#module-th2data_servicesevent_treecommon_event_tree)
- [`th2.data_services.event_tree.common_event_tree_collection`](./th2.data_services.event_tree.common_event_tree_collection.md#module-th2data_servicesevent_treecommon_event_tree_collection)
- [`th2.data_services.event_tree.common_parent_event_tree_collection`](./th2.data_services.event_tree.common_parent_event_tree_collection.md#module-th2data_servicesevent_treecommon_parent_event_tree_collection)
- [`th2.data_services.event_tree.etc_driver`](./th2.data_services.event_tree.etc_driver.md#module-th2data_servicesevent_treeetc_driver)
- [`th2.data_services.event_tree.event_tree`](./th2.data_services.event_tree.event_tree.md#module-th2data_servicesevent_treeevent_tree)
- [`th2.data_services.event_tree.event_tree_collection`](./th2.data_services.event_tree.event_tree_collection.md#module-th2data_servicesevent_treeevent_tree_collection)
- [`th2.data_services.event_tree.exceptions`](./th2.data_services.event_tree.exceptions.md#module-th2data_servicesevent_treeexceptions)
- [`th2.data_services.exceptions`](./th2.data_services.exceptions.md#module-th2data_servicesexceptions)
- [`th2.data_services.interfaces`](./th2.data_services.interfaces.md#module-th2data_servicesinterfaces)
- [`th2.data_services.interfaces.adapter`](./th2.data_services.interfaces.adapter.md#module-th2data_servicesinterfacesadapter)
- [`th2.data_services.interfaces.command`](./th2.data_services.interfaces.command.md#module-th2data_servicesinterfacescommand)
- [`th2.data_services.interfaces.data_source`](./th2.data_services.interfaces.data_source.md#module-th2data_servicesinterfacesdata_source)
- [`th2.data_services.interfaces.source_api`](./th2.data_services.interfaces.source_api.md#module-th2data_servicesinterfacessource_api)
- [`th2.data_services.interfaces.struct`](./th2.data_services.interfaces.struct.md#module-th2data_servicesinterfacesstruct)
- [`th2.data_services.interfaces.stub_builder`](./th2.data_services.interfaces.stub_builder.md#module-th2data_servicesinterfacesstub_builder)
- [`th2.data_services.interfaces.utils`](./th2.data_services.interfaces.utils.md#module-th2data_servicesinterfacesutils)
- [`th2.data_services.interfaces.utils.converter`](./th2.data_services.interfaces.utils.converter.md#module-th2data_servicesinterfacesutilsconverter)

## Classes

- [`config.TH2Config`](./th2.data_services.config.config.md#class-th2config)
- [`data.Data`](./th2.data_services.data.md#class-data): A wrapper for data/data_stream.
- [`common_event_tree.CommonEventTree`](./th2.data_services.event_tree.common_event_tree.md#class-commoneventtree): EventTree is a tree-based data structure of events.
- [`common_event_tree_collection.CommonEventTreeCollection`](./th2.data_services.event_tree.common_event_tree_collection.md#class-commoneventtreecollection): EventTreeCollection objective is building 'EventsTree's and storing them.
- [`common_parent_event_tree_collection.CommonParentEventTreeCollection`](./th2.data_services.event_tree.common_parent_event_tree_collection.md#class-commonparenteventtreecollection): ParentEventTreeCollections is a class like an EventsTreeCollections.
- [`etc_driver.IETCDriver`](./th2.data_services.event_tree.etc_driver.md#class-ietcdriver)
- [`event_tree.EventTree`](./th2.data_services.event_tree.event_tree.md#class-eventtree)
- [`event_tree_collection.Th2EventTreeCollection`](./th2.data_services.event_tree.event_tree_collection.md#class-th2eventtreecollection)
- [`exceptions.EventAlreadyExist`](./th2.data_services.event_tree.exceptions.md#class-eventalreadyexist)
- [`exceptions.EventIdNotInTree`](./th2.data_services.event_tree.exceptions.md#class-eventidnotintree)
- [`exceptions.EventRootExist`](./th2.data_services.event_tree.exceptions.md#class-eventrootexist)
- [`exceptions.FieldIsNotExist`](./th2.data_services.event_tree.exceptions.md#class-fieldisnotexist)
- [`exceptions.TreeLoop`](./th2.data_services.event_tree.exceptions.md#class-treeloop)
- [`exceptions.CommandError`](./th2.data_services.exceptions.md#class-commanderror): Exception raised for errors in the command.
- [`exceptions.EventNotFound`](./th2.data_services.exceptions.md#class-eventnotfound)
- [`exceptions.MessageNotFound`](./th2.data_services.exceptions.md#class-messagenotfound)
- [`adapter.IRecordAdapter`](./th2.data_services.interfaces.adapter.md#class-irecordadapter): Interface of Adapter for record.
- [`adapter.IStreamAdapter`](./th2.data_services.interfaces.adapter.md#class-istreamadapter): Interface of Adapter for streams.
- [`command.ICommand`](./th2.data_services.interfaces.command.md#class-icommand): High level interface for Command.
- [`data_source.IDataSource`](./th2.data_services.interfaces.data_source.md#class-idatasource)
- [`source_api.ISourceAPI`](./th2.data_services.interfaces.source_api.md#class-isourceapi): High level interface for Source API.
- [`struct.IEventStruct`](./th2.data_services.interfaces.struct.md#class-ieventstruct): Just to mark Event Struct class.
- [`struct.IMessageStruct`](./th2.data_services.interfaces.struct.md#class-imessagestruct): Just to mark Message Struct class.
- [`stub_builder.IEventStub`](./th2.data_services.interfaces.stub_builder.md#class-ieventstub): Just to mark Event Stub class.
- [`stub_builder.IMessageStub`](./th2.data_services.interfaces.stub_builder.md#class-imessagestub): Just to mark Message Stub class.
- [`stub_builder.IStub`](./th2.data_services.interfaces.stub_builder.md#class-istub)
- [`converter.ITimestampConverter`](./th2.data_services.interfaces.utils.converter.md#class-itimestampconverter)

## Functions

- No functions


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
