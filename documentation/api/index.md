<!-- markdownlint-disable -->

# API Overview

## Modules

- [`data`](./data.md#module-data)
- [`decode_error_handler`](./decode_error_handler.md#module-decode_error_handler)
- [`filter`](./filter.md#module-filter)
- [`interfaces`](./interfaces.md#module-interfaces)
- [`interfaces.adapter`](./interfaces.adapter.md#module-interfacesadapter)
- [`interfaces.command`](./interfaces.command.md#module-interfacescommand)
- [`interfaces.data_source`](./interfaces.data_source.md#module-interfacesdata_source)
- [`interfaces.source_api`](./interfaces.source_api.md#module-interfacessource_api)
- [`interfaces.utils`](./interfaces.utils.md#module-interfacesutils)
- [`interfaces.utils.converter`](./interfaces.utils.converter.md#module-interfacesutilsconverter)
- [`provider`](./provider.md#module-provider)
- [`provider.command`](./provider.command.md#module-providercommand)
- [`provider.exceptions`](./provider.exceptions.md#module-providerexceptions)
- [`provider.interfaces`](./provider.interfaces.md#module-providerinterfaces)
- [`provider.interfaces.command`](./provider.interfaces.command.md#module-providerinterfacescommand): Interfaces for Provider Commands.
- [`provider.interfaces.data_source`](./provider.interfaces.data_source.md#module-providerinterfacesdata_source): Interfaces for Provider Data Source.
- [`provider.interfaces.filter`](./provider.interfaces.filter.md#module-providerinterfacesfilter)
- [`provider.interfaces.source_api`](./provider.interfaces.source_api.md#module-providerinterfacessource_api)
- [`provider.interfaces.struct`](./provider.interfaces.struct.md#module-providerinterfacesstruct)
- [`provider.interfaces.stub_builder`](./provider.interfaces.stub_builder.md#module-providerinterfacesstub_builder)
- [`provider.utils`](./provider.utils.md#module-providerutils)
- [`provider.utils.converters`](./provider.utils.converters.md#module-providerutilsconverters)
- [`provider.utils.version_checker`](./provider.utils.version_checker.md#module-providerutilsversion_checker)
- [`provider.v5`](./provider.v5.md#module-providerv5)
- [`provider.v5.adapters`](./provider.v5.adapters.md#module-providerv5adapters)
- [`provider.v5.adapters.basic_adapters`](./provider.v5.adapters.basic_adapters.md#module-providerv5adaptersbasic_adapters)
- [`provider.v5.adapters.event_adapters`](./provider.v5.adapters.event_adapters.md#module-providerv5adaptersevent_adapters)
- [`provider.v5.adapters.message_adapters`](./provider.v5.adapters.message_adapters.md#module-providerv5adaptersmessage_adapters)
- [`provider.v5.commands`](./provider.v5.commands.md#module-providerv5commands)
- [`provider.v5.commands.grpc`](./provider.v5.commands.grpc.md#module-providerv5commandsgrpc)
- [`provider.v5.data_source`](./provider.v5.data_source.md#module-providerv5data_source)
- [`provider.v5.data_source.grpc`](./provider.v5.data_source.grpc.md#module-providerv5data_sourcegrpc)
- [`provider.v5.data_source.http`](./provider.v5.data_source.http.md#module-providerv5data_sourcehttp)
- [`provider.v5.filters`](./provider.v5.filters.md#module-providerv5filters)
- [`provider.v5.filters.event_filters`](./provider.v5.filters.event_filters.md#module-providerv5filtersevent_filters)
- [`provider.v5.filters.filter`](./provider.v5.filters.filter.md#module-providerv5filtersfilter)
- [`provider.v5.filters.message_filters`](./provider.v5.filters.message_filters.md#module-providerv5filtersmessage_filters)
- [`provider.v5.interfaces`](./provider.v5.interfaces.md#module-providerv5interfaces)
- [`provider.v5.interfaces.command`](./provider.v5.interfaces.command.md#module-providerv5interfacescommand)
- [`provider.v5.provider_api`](./provider.v5.provider_api.md#module-providerv5provider_api)
- [`provider.v5.provider_api.grpc`](./provider.v5.provider_api.grpc.md#module-providerv5provider_apigrpc)
- [`provider.v5.provider_api.http`](./provider.v5.provider_api.http.md#module-providerv5provider_apihttp)
- [`provider.v5.stub_builder`](./provider.v5.stub_builder.md#module-providerv5stub_builder)
- [`provider.v6`](./provider.v6.md#module-providerv6)
- [`provider.v6.commands`](./provider.v6.commands.md#module-providerv6commands)
- [`provider.v6.filters`](./provider.v6.filters.md#module-providerv6filters)
- [`provider.v6.struct`](./provider.v6.struct.md#module-providerv6struct)
- [`provider.v6.stub_builder`](./provider.v6.stub_builder.md#module-providerv6stub_builder)
- [`th2_gui_report`](./th2_gui_report.md#module-th2_gui_report)
- [`utils`](./utils.md#module-utils)
- [`utils.converters`](./utils.converters.md#module-utilsconverters)

## Classes

- [`data.Data`](./data.md#class-data): A wrapper for data/data_stream.
- [`filter.Filter`](./filter.md#class-filter): The class for using rpt-data-provider filters API.
- [`adapter.IAdapter`](./interfaces.adapter.md#class-iadapter): High level interface for Adapter.
- [`adapter.IEventAdapter`](./interfaces.adapter.md#class-ieventadapter): Interface of Adapter for events.
- [`adapter.IMessageAdapter`](./interfaces.adapter.md#class-imessageadapter): Interface of Adapter for messages.
- [`command.ICommand`](./interfaces.command.md#class-icommand): High level interface for Command.
- [`data_source.IDataSource`](./interfaces.data_source.md#class-idatasource)
- [`source_api.ISourceAPI`](./interfaces.source_api.md#class-isourceapi): High level interface for Source API.
- [`converter.ITimestampConverter`](./interfaces.utils.converter.md#class-itimestampconverter)
- [`command.ProviderAdaptableCommand`](./provider.command.md#class-provideradaptablecommand)
- [`exceptions.CommandError`](./provider.exceptions.md#class-commanderror): Exception raised for errors in the command.
- [`exceptions.EventNotFound`](./provider.exceptions.md#class-eventnotfound)
- [`exceptions.MessageNotFound`](./provider.exceptions.md#class-messagenotfound)
- [`command.IGRPCProviderCommand`](./provider.interfaces.command.md#class-igrpcprovidercommand): Interface of command for rpt-data-provider which works via GRPC.
- [`command.IHTTPProviderCommand`](./provider.interfaces.command.md#class-ihttpprovidercommand): Interface of command for rpt-data-provider which works via HTTP.
- [`command.IProviderCommand`](./provider.interfaces.command.md#class-iprovidercommand): Interface of command for rpt-data-provider.
- [`data_source.IGRPCProviderDataSource`](./provider.interfaces.data_source.md#class-igrpcproviderdatasource): Interface of DataSource that provides work with rpt-data-provider via GRPC.
- [`data_source.IHTTPProviderDataSource`](./provider.interfaces.data_source.md#class-ihttpproviderdatasource): Interface of DataSource that provides work with rpt-data-provider via HTTP.
- [`data_source.IProviderDataSource`](./provider.interfaces.data_source.md#class-iproviderdatasource)
- [`filter.IProviderFilter`](./provider.interfaces.filter.md#class-iproviderfilter)
- [`source_api.IGRPCProviderSourceAPI`](./provider.interfaces.source_api.md#class-igrpcprovidersourceapi): Interface for Source API of rpt-data-provider which works via GRPC.
- [`source_api.IHTTPProviderSourceAPI`](./provider.interfaces.source_api.md#class-ihttpprovidersourceapi): Interface for Source API of rpt-data-provider which works via HTTP.
- [`source_api.IProviderSourceAPI`](./provider.interfaces.source_api.md#class-iprovidersourceapi): Interface for Source API of rpt-data-provider.
- [`struct.IEventStruct`](./provider.interfaces.struct.md#class-ieventstruct): Just to mark Event Struct class.
- [`struct.IMessageStruct`](./provider.interfaces.struct.md#class-imessagestruct): Just to mark Message Struct class.
- [`stub_builder.IEventStub`](./provider.interfaces.stub_builder.md#class-ieventstub): Just to mark Event Stub class.
- [`stub_builder.IMessageStub`](./provider.interfaces.stub_builder.md#class-imessagestub): Just to mark Message Stub class.
- [`stub_builder.IStub`](./provider.interfaces.stub_builder.md#class-istub)
- [`converters.Th2TimestampConverter`](./provider.utils.converters.md#class-th2timestampconverter): Converts Th2 timestamps.
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
- [`grpc.GRPCProvider5DataSource`](./provider.v5.data_source.grpc.md#class-grpcprovider5datasource): DataSource class which provide work with rpt-data-provider.
- [`http.HTTPProvider5DataSource`](./provider.v5.data_source.http.md#class-httpprovider5datasource): DataSource class which provide work with rpt-data-provider.
- [`event_filters.AttachedMessageIdFilter`](./provider.v5.filters.event_filters.md#class-attachedmessageidfilter): Filters the events that are linked to the specified message id.
- [`event_filters.BodyFilter`](./provider.v5.filters.event_filters.md#class-bodyfilter): Will match the events which body contains one of the given substrings.
- [`event_filters.FailedStatusFilter`](./provider.v5.filters.event_filters.md#class-failedstatusfilter): Will match the events which status equals failed.
- [`event_filters.NameFilter`](./provider.v5.filters.event_filters.md#class-namefilter): Will match the events which name contains one of the given substrings.
- [`event_filters.PassedStatusFilter`](./provider.v5.filters.event_filters.md#class-passedstatusfilter): Will match the events which status equals passed.
- [`event_filters.TypeFilter`](./provider.v5.filters.event_filters.md#class-typefilter): Will match the events which type contains one of the given substrings.
- [`filter.Provider5EventFilter`](./provider.v5.filters.filter.md#class-provider5eventfilter): Base class for Event Filters of Provider v5.
- [`filter.Provider5Filter`](./provider.v5.filters.filter.md#class-provider5filter): General interface for Filters of Provider v5.
- [`filter.Provider5MessageFilter`](./provider.v5.filters.filter.md#class-provider5messagefilter): Base class for Message Filters of Provider v5.
- [`message_filters.AttachedEventIdsFilter`](./provider.v5.filters.message_filters.md#class-attachedeventidsfilter): Filters the messages that are linked to the specified event id.
- [`message_filters.BodyBinaryFilter`](./provider.v5.filters.message_filters.md#class-bodybinaryfilter): Will match the messages by their binary body.
- [`message_filters.BodyFilter`](./provider.v5.filters.message_filters.md#class-bodyfilter): Will match the messages by their parsed body.
- [`message_filters.TypeFilter`](./provider.v5.filters.message_filters.md#class-typefilter): Will match the messages by their full type name.
- [`command.IGRPCProvider5Command`](./provider.v5.interfaces.command.md#class-igrpcprovider5command): Interface of command for rpt-data-provider.
- [`command.IHTTPProvider5Command`](./provider.v5.interfaces.command.md#class-ihttpprovider5command): Interface of command for rpt-data-provider.
- [`grpc.BasicRequest`](./provider.v5.provider_api.grpc.md#class-basicrequest): BasicRequest(start_timestamp, end_timestamp, result_count_limit, keep_open, search_direction, filters)
- [`grpc.GRPCProvider5API`](./provider.v5.provider_api.grpc.md#class-grpcprovider5api)
- [`http.HTTPProvider5API`](./provider.v5.provider_api.http.md#class-httpprovider5api)
- [`stub_builder.Provider5EventStubBuilder`](./provider.v5.stub_builder.md#class-provider5eventstubbuilder)
- [`stub_builder.Provider5MessageStubBuilder`](./provider.v5.stub_builder.md#class-provider5messagestubbuilder)
- [`struct.GRPCProvider6EventStruct`](./provider.v6.struct.md#class-grpcprovider6eventstruct): Interface for Event of data-provider v6.
- [`stub_builder.Provider6EventStubBuilder`](./provider.v6.stub_builder.md#class-provider6eventstubbuilder)
- [`stub_builder.Provider6MessageStubBuilder`](./provider.v6.stub_builder.md#class-provider6messagestubbuilder)
- [`th2_gui_report.Th2GUIReport`](./th2_gui_report.md#class-th2guireport): Class for creating gui link by event ID or message ID.
- [`converters.DatetimeStringConverter`](./utils.converters.md#class-datetimestringconverter): Converts datetime strings.

## Functions

- [`decode_error_handler.handler`](./decode_error_handler.md#function-handler): Decode error handler that tries change utf-8 character to Unicode.
- [`version_checker.get_package_version`](./provider.utils.version_checker.md#function-get_package_version)
- [`version_checker.get_version_by_pip`](./provider.utils.version_checker.md#function-get_version_by_pip)
- [`version_checker.verify_grpc_version`](./provider.utils.version_checker.md#function-verify_grpc_version)


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
