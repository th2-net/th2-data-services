<!-- markdownlint-disable -->

# API Overview

## Modules

- [`data`](./data.md#module-data)
- [`decode_error_handler`](./decode_error_handler.md#module-decode_error_handler)
- [`events_tree`](./events_tree.md#module-events_tree)
- [`events_tree.events_tree`](./events_tree.events_tree.md#module-events_treeevents_tree)
- [`events_tree.exceptions`](./events_tree.exceptions.md#module-events_treeexceptions)
- [`filter`](./filter.md#module-filter)
- [`interfaces`](./interfaces.md#module-interfaces)
- [`interfaces.adapter`](./interfaces.adapter.md#module-interfacesadapter)
- [`interfaces.command`](./interfaces.command.md#module-interfacescommand)
- [`interfaces.data_source`](./interfaces.data_source.md#module-interfacesdata_source)
- [`interfaces.events_tree`](./interfaces.events_tree.md#module-interfacesevents_tree)
- [`interfaces.events_tree.events_tree_collection`](./interfaces.events_tree.events_tree_collection.md#module-interfacesevents_treeevents_tree_collection)
- [`interfaces.events_tree.parent_events_tree_collection`](./interfaces.events_tree.parent_events_tree_collection.md#module-interfacesevents_treeparent_events_tree_collection)
- [`interfaces.source_api`](./interfaces.source_api.md#module-interfacessource_api)
- [`provider`](./provider.md#module-provider)
- [`provider.adapters`](./provider.adapters.md#module-provideradapters)
- [`provider.adapters.adapter_sse`](./provider.adapters.adapter_sse.md#module-provideradaptersadapter_sse)
- [`provider.command`](./provider.command.md#module-providercommand)
- [`provider.exceptions`](./provider.exceptions.md#module-providerexceptions)
- [`provider.interfaces`](./provider.interfaces.md#module-providerinterfaces)
- [`provider.interfaces.command`](./provider.interfaces.command.md#module-providerinterfacescommand): Interfaces for Provider Commands.
- [`provider.interfaces.data_source`](./provider.interfaces.data_source.md#module-providerinterfacesdata_source): Interfaces for Provider Data Source.
- [`provider.interfaces.source_api`](./provider.interfaces.source_api.md#module-providerinterfacessource_api)
- [`provider.interfaces.struct`](./provider.interfaces.struct.md#module-providerinterfacesstruct)
- [`provider.interfaces.stub_builder`](./provider.interfaces.stub_builder.md#module-providerinterfacesstub_builder)
- [`provider.v5`](./provider.v5.md#module-providerv5)
- [`provider.v5.adapters`](./provider.v5.adapters.md#module-providerv5adapters)
- [`provider.v5.adapters.basic_adapters`](./provider.v5.adapters.basic_adapters.md#module-providerv5adaptersbasic_adapters)
- [`provider.v5.adapters.event_adapters`](./provider.v5.adapters.event_adapters.md#module-providerv5adaptersevent_adapters)
- [`provider.v5.adapters.message_adapters`](./provider.v5.adapters.message_adapters.md#module-providerv5adaptersmessage_adapters)
- [`provider.v5.command_resolver`](./provider.v5.command_resolver.md#module-providerv5command_resolver)
- [`provider.v5.commands`](./provider.v5.commands.md#module-providerv5commands)
- [`provider.v5.commands.grpc`](./provider.v5.commands.grpc.md#module-providerv5commandsgrpc)
- [`provider.v5.commands.http`](./provider.v5.commands.http.md#module-providerv5commandshttp)
- [`provider.v5.data_source`](./provider.v5.data_source.md#module-providerv5data_source)
- [`provider.v5.data_source.grpc`](./provider.v5.data_source.grpc.md#module-providerv5data_sourcegrpc)
- [`provider.v5.data_source.http`](./provider.v5.data_source.http.md#module-providerv5data_sourcehttp)
- [`provider.v5.events_tree`](./provider.v5.events_tree.md#module-providerv5events_tree)
- [`provider.v5.events_tree.events_tree_collection`](./provider.v5.events_tree.events_tree_collection.md#module-providerv5events_treeevents_tree_collection)
- [`provider.v5.events_tree.parent_events_tree_collection`](./provider.v5.events_tree.parent_events_tree_collection.md#module-providerv5events_treeparent_events_tree_collection)
- [`provider.v5.interfaces`](./provider.v5.interfaces.md#module-providerv5interfaces)
- [`provider.v5.interfaces.command`](./provider.v5.interfaces.command.md#module-providerv5interfacescommand)
- [`provider.v5.provider_api`](./provider.v5.provider_api.md#module-providerv5provider_api)
- [`provider.v5.provider_api.grpc`](./provider.v5.provider_api.grpc.md#module-providerv5provider_apigrpc)
- [`provider.v5.provider_api.http`](./provider.v5.provider_api.http.md#module-providerv5provider_apihttp)
- [`provider.v5.stub_builder`](./provider.v5.stub_builder.md#module-providerv5stub_builder)
- [`sse_client`](./sse_client.md#module-sse_client)
- [`th2_gui_report`](./th2_gui_report.md#module-th2_gui_report)

## Classes

- [`data.Data`](./data.md#class-data): A wrapper for data/data_stream.
- [`events_tree.EventsTree`](./events_tree.events_tree.md#class-eventstree): EventsTree is a tree-based data structure of events.
- [`exceptions.EventIdNotInTree`](./events_tree.exceptions.md#class-eventidnotintree)
- [`exceptions.FieldIsNotExist`](./events_tree.exceptions.md#class-fieldisnotexist)
- [`filter.Filter`](./filter.md#class-filter): The class for using rpt-data-provider filters API.
- [`adapter.IAdapter`](./interfaces.adapter.md#class-iadapter): High level interface for Adapter.
- [`adapter.IEventAdapter`](./interfaces.adapter.md#class-ieventadapter): Interface of Adapter for events.
- [`adapter.IMessageAdapter`](./interfaces.adapter.md#class-imessageadapter): Interface of Adapter for messages.
- [`command.ICommand`](./interfaces.command.md#class-icommand): High level interface for Command.
- [`data_source.IDataSource`](./interfaces.data_source.md#class-idatasource)
- [`events_tree_collection.EventsTreeCollection`](./interfaces.events_tree.events_tree_collection.md#class-eventstreecollection): EventsTreeCollection objective is building 'EventsTree's and storing them.
- [`parent_events_tree_collection.ParentEventsTreeCollection`](./interfaces.events_tree.parent_events_tree_collection.md#class-parenteventstreecollection): ParentEventsTreeCollections is a class like an EventsTreeCollections.
- [`source_api.ISourceAPI`](./interfaces.source_api.md#class-isourceapi): High level interface for Source API.
- [`adapter_sse.SSEAdapter`](./provider.adapters.adapter_sse.md#class-sseadapter): SSE Adapter handles bytes from sse-stream into Dict object.
- [`command.ProviderAdaptableCommand`](./provider.command.md#class-provideradaptablecommand)
- [`exceptions.CommandError`](./provider.exceptions.md#class-commanderror): Exception raised for errors in the command.
- [`exceptions.DataSourceNotFound`](./provider.exceptions.md#class-datasourcenotfound): Exception raised for errors when EventsTree need DataSource for execution.
- [`exceptions.EventNotFound`](./provider.exceptions.md#class-eventnotfound)
- [`exceptions.MessageNotFound`](./provider.exceptions.md#class-messagenotfound)
- [`command.IGRPCProviderCommand`](./provider.interfaces.command.md#class-igrpcprovidercommand): Interface of command for rpt-data-provider which works via GRPC.
- [`command.IHTTPProviderCommand`](./provider.interfaces.command.md#class-ihttpprovidercommand): Interface of command for rpt-data-provider which works via HTTP.
- [`command.IProviderCommand`](./provider.interfaces.command.md#class-iprovidercommand): Interface of command for rpt-data-provider.
- [`data_source.IGRPCProviderDataSource`](./provider.interfaces.data_source.md#class-igrpcproviderdatasource): Interface of DataSource that provides work with rpt-data-provider via GRPC.
- [`data_source.IHTTPProviderDataSource`](./provider.interfaces.data_source.md#class-ihttpproviderdatasource): Interface of DataSource that provides work with rpt-data-provider via HTTP.
- [`data_source.IProviderDataSource`](./provider.interfaces.data_source.md#class-iproviderdatasource)
- [`source_api.IGRPCProviderSourceAPI`](./provider.interfaces.source_api.md#class-igrpcprovidersourceapi): Interface for Source API of rpt-data-provider which works via GRPC.
- [`source_api.IHTTPProviderSourceAPI`](./provider.interfaces.source_api.md#class-ihttpprovidersourceapi): Interface for Source API of rpt-data-provider which works via HTTP.
- [`source_api.IProviderSourceAPI`](./provider.interfaces.source_api.md#class-iprovidersourceapi): Interface for Source API of rpt-data-provider.
- [`struct.IEventStruct`](./provider.interfaces.struct.md#class-ieventstruct): Just to mark Event Struct class.
- [`struct.IMessageStruct`](./provider.interfaces.struct.md#class-imessagestruct): Just to mark Message Struct class.
- [`stub_builder.IEventStub`](./provider.interfaces.stub_builder.md#class-ieventstub): Just to mark Event Stub class.
- [`stub_builder.IMessageStub`](./provider.interfaces.stub_builder.md#class-imessagestub): Just to mark Message Stub class.
- [`stub_builder.IStub`](./provider.interfaces.stub_builder.md#class-istub)
- [`basic_adapters.GRPCObjectToDictAdapter`](./provider.v5.adapters.basic_adapters.md#class-grpcobjecttodictadapter): GRPC Adapter decodes a GRPC object into a Dict object.
- [`event_adapters.DeleteEventWrappersAdapter`](./provider.v5.adapters.event_adapters.md#class-deleteeventwrappersadapter): Adapter that deletes unnecessary wrappers in events.
- [`message_adapters.CodecPipelinesAdapter`](./provider.v5.adapters.message_adapters.md#class-codecpipelinesadapter): Adapter for codec-pipeline messages from provider v5.
- [`message_adapters.DeleteMessageWrappersAdapter`](./provider.v5.adapters.message_adapters.md#class-deletemessagewrappersadapter): Adapter that deletes unnecessary wrappers in messages.
- [`grpc.GetEventById`](./provider.v5.commands.grpc.md#class-geteventbyid): A Class-Command for request to rpt-data-provider.
- [`grpc.GetEventByIdGRPCObject`](./provider.v5.commands.grpc.md#class-geteventbyidgrpcobject): A Class-Command for request to rpt-data-provider.
- [`grpc.GetEvents`](./provider.v5.commands.grpc.md#class-getevents): A Class-Command for request to rpt-data-provider.
- [`grpc.GetEventsById`](./provider.v5.commands.grpc.md#class-geteventsbyid): A Class-Command for request to rpt-data-provider.
- [`grpc.GetEventsGRPCObjects`](./provider.v5.commands.grpc.md#class-geteventsgrpcobjects): A Class-Command for request to rpt-data-provider.
- [`grpc.GetMessageById`](./provider.v5.commands.grpc.md#class-getmessagebyid): A Class-Command for request to rpt-data-provider.
- [`grpc.GetMessageByIdGRPCObject`](./provider.v5.commands.grpc.md#class-getmessagebyidgrpcobject): A Class-Command for request to rpt-data-provider.
- [`grpc.GetMessages`](./provider.v5.commands.grpc.md#class-getmessages): A Class-Command for request to rpt-data-provider.
- [`grpc.GetMessagesById`](./provider.v5.commands.grpc.md#class-getmessagesbyid): A Class-Command for request to rpt-data-provider.
- [`grpc.GetMessagesGRPCObject`](./provider.v5.commands.grpc.md#class-getmessagesgrpcobject): A Class-Command for request to rpt-data-provider.
- [`http.GetEventById`](./provider.v5.commands.http.md#class-geteventbyid): A Class-Command for request to rpt-data-provider.
- [`http.GetEvents`](./provider.v5.commands.http.md#class-getevents): A Class-Command for request to rpt-data-provider.
- [`http.GetEventsById`](./provider.v5.commands.http.md#class-geteventsbyid): A Class-Command for request to rpt-data-provider.
- [`http.GetEventsSSEBytes`](./provider.v5.commands.http.md#class-geteventsssebytes): A Class-Command for request to rpt-data-provider.
- [`http.GetEventsSSEEvents`](./provider.v5.commands.http.md#class-geteventssseevents): A Class-Command for request to rpt-data-provider.
- [`http.GetMessageById`](./provider.v5.commands.http.md#class-getmessagebyid): A Class-Command for request to rpt-data-provider.
- [`http.GetMessages`](./provider.v5.commands.http.md#class-getmessages): A Class-Command for request to rpt-data-provider.
- [`http.GetMessagesById`](./provider.v5.commands.http.md#class-getmessagesbyid): A Class-Command for request to rpt-data-provider.
- [`http.GetMessagesSSEBytes`](./provider.v5.commands.http.md#class-getmessagesssebytes): A Class-Command for request to rpt-data-provider.
- [`http.GetMessagesSSEEvents`](./provider.v5.commands.http.md#class-getmessagessseevents): A Class-Command for request to rpt-data-provider.
- [`grpc.GRPCProvider5DataSource`](./provider.v5.data_source.grpc.md#class-grpcprovider5datasource): DataSource class which provide work with rpt-data-provider.
- [`http.HTTPProvider5DataSource`](./provider.v5.data_source.http.md#class-httpprovider5datasource): DataSource class which provide work with rpt-data-provider.
- [`events_tree_collection.EventsTreeCollectionProvider5`](./provider.v5.events_tree.events_tree_collection.md#class-eventstreecollectionprovider5): EventsTreesCollections for data-provider v5.
- [`parent_events_tree_collection.ParentEventsTreeCollectionProvider5`](./provider.v5.events_tree.parent_events_tree_collection.md#class-parenteventstreecollectionprovider5): ParentEventsTreeCollection for data-provider v5.
- [`command.IGRPCProvider5Command`](./provider.v5.interfaces.command.md#class-igrpcprovider5command): Interface of command for rpt-data-provider.
- [`command.IHTTPProvider5Command`](./provider.v5.interfaces.command.md#class-ihttpprovider5command): Interface of command for rpt-data-provider.
- [`grpc.BasicRequest`](./provider.v5.provider_api.grpc.md#class-basicrequest): BasicRequest(start_timestamp, end_timestamp, result_count_limit, keep_open, search_direction, filters)
- [`grpc.GRPCProvider5API`](./provider.v5.provider_api.grpc.md#class-grpcprovider5api)
- [`http.HTTPProvider5API`](./provider.v5.provider_api.http.md#class-httpprovider5api)
- [`stub_builder.Provider5EventStubBuilder`](./provider.v5.stub_builder.md#class-provider5eventstubbuilder)
- [`stub_builder.Provider5MessageStubBuilder`](./provider.v5.stub_builder.md#class-provider5messagestubbuilder)
- [`sse_client.SSEClient`](./sse_client.md#class-sseclient): Patch for sseclient-py to get availability to configure decode error handler.
- [`th2_gui_report.Th2GUIReport`](./th2_gui_report.md#class-th2guireport): Class for creating gui link by event ID or message ID.

## Functions

- [`decode_error_handler.handler`](./decode_error_handler.md#function-handler): Decode error handler that tries change utf-8 character to Unicode.
- [`command_resolver.resolver_get_event_by_id`](./provider.v5.command_resolver.md#function-resolver_get_event_by_id): Resolves what 'GetEventById' command you need to use based Data Source.
- [`command_resolver.resolver_get_events_by_id`](./provider.v5.command_resolver.md#function-resolver_get_events_by_id): Resolves what 'GetEventsById' command you need to use based Data Source.


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
