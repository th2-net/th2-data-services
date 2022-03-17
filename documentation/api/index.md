<!-- markdownlint-disable -->

# API Overview

## Modules

- [`data`](./data.md#module-data)
- [`decode_error_handler`](./decode_error_handler.md#module-decode_error_handler)
- [`events_tree`](./events_tree.md#module-events_tree)
- [`events_tree.events_tree`](./events_tree.events_tree.md#module-events_treeevents_tree)
- [`events_tree.events_trees_collection`](./events_tree.events_trees_collection.md#module-events_treeevents_trees_collection)
- [`events_tree.exceptions`](./events_tree.exceptions.md#module-events_treeexceptions)
- [`events_tree.parent_events_trees_collection`](./events_tree.parent_events_trees_collection.md#module-events_treeparent_events_trees_collection)
- [`filter`](./filter.md#module-filter)
- [`interfaces`](./interfaces.md#module-interfaces)
- [`interfaces.adapter`](./interfaces.adapter.md#module-interfacesadapter)
- [`interfaces.command`](./interfaces.command.md#module-interfacescommand)
- [`interfaces.data_source`](./interfaces.data_source.md#module-interfacesdata_source)
- [`interfaces.source_api`](./interfaces.source_api.md#module-interfacessource_api)
- [`provider`](./provider.md#module-provider)
- [`provider.adapters`](./provider.adapters.md#module-provideradapters)
- [`provider.adapters.adapter_provider5`](./provider.adapters.adapter_provider5.md#module-provideradaptersadapter_provider5)
- [`provider.adapters.adapter_sse`](./provider.adapters.adapter_sse.md#module-provideradaptersadapter_sse)
- [`provider.command`](./provider.command.md#module-providercommand)
- [`provider.interfaces`](./provider.interfaces.md#module-providerinterfaces)
- [`provider.interfaces.command`](./provider.interfaces.command.md#module-providerinterfacescommand): Interfaces for Provider Commands.
- [`provider.interfaces.data_source`](./provider.interfaces.data_source.md#module-providerinterfacesdata_source): Interfaces for Provider Data Source.
- [`provider.interfaces.source_api`](./provider.interfaces.source_api.md#module-providerinterfacessource_api)
- [`provider.interfaces.struct`](./provider.interfaces.struct.md#module-providerinterfacesstruct)
- [`provider.interfaces.stub_builder`](./provider.interfaces.stub_builder.md#module-providerinterfacesstub_builder)
- [`provider.v5`](./provider.v5.md#module-providerv5)
- [`provider.v5.adapters`](./provider.v5.adapters.md#module-providerv5adapters)
- [`provider.v5.adapters.basic_adapters`](./provider.v5.adapters.basic_adapters.md#module-providerv5adaptersbasic_adapters)
- [`provider.v5.adapters.events_adapters`](./provider.v5.adapters.events_adapters.md#module-providerv5adaptersevents_adapters)
- [`provider.v5.adapters.messages_adapters`](./provider.v5.adapters.messages_adapters.md#module-providerv5adaptersmessages_adapters)
- [`provider.v5.command_resolver`](./provider.v5.command_resolver.md#module-providerv5command_resolver)
- [`provider.v5.commands`](./provider.v5.commands.md#module-providerv5commands)
- [`provider.v5.commands.grpc`](./provider.v5.commands.grpc.md#module-providerv5commandsgrpc)
- [`provider.v5.commands.http`](./provider.v5.commands.http.md#module-providerv5commandshttp)
- [`provider.v5.data_source`](./provider.v5.data_source.md#module-providerv5data_source)
- [`provider.v5.data_source.grpc`](./provider.v5.data_source.grpc.md#module-providerv5data_sourcegrpc)
- [`provider.v5.data_source.http`](./provider.v5.data_source.http.md#module-providerv5data_sourcehttp)
- [`provider.v5.events_tree`](./provider.v5.events_tree.md#module-providerv5events_tree)
- [`provider.v5.events_tree.events_trees_collection`](./provider.v5.events_tree.events_trees_collection.md#module-providerv5events_treeevents_trees_collection)
- [`provider.v5.events_tree.parent_events_trees_collection`](./provider.v5.events_tree.parent_events_trees_collection.md#module-providerv5events_treeparent_events_trees_collection)
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
- [`events_tree.EventsTree`](./events_tree.events_tree.md#class-eventstree): EventsTree - is a useful wrapper for your retrieved data.
- [`events_trees_collection.EventsTreesCollection`](./events_tree.events_trees_collection.md#class-eventstreescollection): EventsTreeCollection objective is building 'EventsTree's and storing them.
- [`exceptions.EventIdNotInTree`](./events_tree.exceptions.md#class-eventidnotintree)
- [`exceptions.FieldIsNotExist`](./events_tree.exceptions.md#class-fieldisnotexist)
- [`parent_events_trees_collection.ParentEventsTreesCollection`](./events_tree.parent_events_trees_collection.md#class-parenteventstreescollection): ParentEventsTreeCollections is a class like an EventsTreeCollections.
- [`filter.Filter`](./filter.md#class-filter): The class for using rpt-data-provider filters API.
- [`adapter.IAdapter`](./interfaces.adapter.md#class-iadapter): High level interface for Adapter.
- [`adapter.IEventAdapter`](./interfaces.adapter.md#class-ieventadapter): Interface of Adapter for events.
- [`adapter.IMessageAdapter`](./interfaces.adapter.md#class-imessageadapter): Interface of Adapter for messages.
- [`command.ICommand`](./interfaces.command.md#class-icommand): High level interface for Command.
- [`data_source.IDataSource`](./interfaces.data_source.md#class-idatasource)
- [`source_api.ISourceAPI`](./interfaces.source_api.md#class-isourceapi): High level interface for Source API.
- [`command.ProviderAdaptableCommand`](./provider.command.md#class-provideradaptablecommand)
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
- [`basic_adapters.AdapterGRPCObjectToDict`](./provider.v5.adapters.basic_adapters.md#class-adaptergrpcobjecttodict): GRPC Adapter decodes a GRPC object into a Dict object.
- [`basic_adapters.AdapterSSE`](./provider.v5.adapters.basic_adapters.md#class-adaptersse): SSE Adapter handle bytes from sse-stream into Dict object.
- [`events_adapters.AdapterDeleteEventWrappers`](./provider.v5.adapters.events_adapters.md#class-adapterdeleteeventwrappers): Adapter that delete unnecessary wrappers in events.
- [`messages_adapters.AdapterDeleteMessageWrappers`](./provider.v5.adapters.messages_adapters.md#class-adapterdeletemessagewrappers): Adapter that delete unnecessary wrappers in events.
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
- [`events_trees_collection.EventsTreesCollectionProvider5`](./provider.v5.events_tree.events_trees_collection.md#class-eventstreescollectionprovider5): EventsTreesCollections for data-provider v5.
- [`parent_events_trees_collection.ParentsEventsTreesCollectionProvider5`](./provider.v5.events_tree.parent_events_trees_collection.md#class-parentseventstreescollectionprovider5): ParentsEventsTreesCollection for data-provider v5.
- [`command.IGRPCProvider5Command`](./provider.v5.interfaces.command.md#class-igrpcprovider5command): Interface of command for rpt-data-provider.
- [`command.IHTTPProvider5Command`](./provider.v5.interfaces.command.md#class-ihttpprovider5command): Interface of command for rpt-data-provider.
- [`grpc.BasicRequest`](./provider.v5.provider_api.grpc.md#class-basicrequest): BasicRequest(start_timestamp, end_timestamp, result_count_limit, keep_open, search_direction, filters)
- [`grpc.GRPCProvider5API`](./provider.v5.provider_api.grpc.md#class-grpcprovider5api)
- [`http.HTTPProvider5API`](./provider.v5.provider_api.http.md#class-httpprovider5api)
- [`stub_builder.Provider5EventStubBuilder`](./provider.v5.stub_builder.md#class-provider5eventstubbuilder)
- [`stub_builder.Provider5MessageStubBuilder`](./provider.v5.stub_builder.md#class-provider5messagestubbuilder)
- [`sse_client.SSEClient`](./sse_client.md#class-sseclient): Patch for sseclient-py to get availability to configure decode error handler.
- [`th2_gui_report.Th2GUIReport`](./th2_gui_report.md#class-th2guireport): Class for create gui link by event ID or message ID.

## Functions

- [`decode_error_handler.handler`](./decode_error_handler.md#function-handler): Decode error handler that tries change utf-8 character to Unicode.
- [`adapter_provider5.adapter_provider5`](./provider.adapters.adapter_provider5.md#function-adapter_provider5): Provider 5 adapter.
- [`adapter_sse.adapter_sse`](./provider.adapters.adapter_sse.md#function-adapter_sse): SSE adapter.
- [`command_resolver.resolver_get_event_by_id`](./provider.v5.command_resolver.md#function-resolver_get_event_by_id): Resolves what 'GetEventById' command you need to use based Data Source.
- [`command_resolver.resolver_get_events_by_id`](./provider.v5.command_resolver.md#function-resolver_get_events_by_id): Resolves what 'GetEventsById' command you need to use based Data Source.


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
