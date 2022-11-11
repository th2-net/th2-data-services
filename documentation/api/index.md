<!-- markdownlint-disable -->

# API Overview

## Modules

- [`data`](./data.md#module-data)
- [`interfaces`](./interfaces.md#module-interfaces)
- [`interfaces.adapter`](./interfaces.adapter.md#module-interfacesadapter)
- [`interfaces.command`](./interfaces.command.md#module-interfacescommand)
- [`interfaces.data_source`](./interfaces.data_source.md#module-interfacesdata_source)
- [`interfaces.source_api`](./interfaces.source_api.md#module-interfacessource_api)
- [`interfaces.struct`](./interfaces.struct.md#module-interfacesstruct)
- [`interfaces.stub_builder`](./interfaces.stub_builder.md#module-interfacesstub_builder)
- [`interfaces.utils`](./interfaces.utils.md#module-interfacesutils)
- [`interfaces.utils.converter`](./interfaces.utils.converter.md#module-interfacesutilsconverter)
- [`utils`](./utils.md#module-utils)
- [`utils.converters`](./utils.converters.md#module-utilsconverters)

## Classes

- [`data.Data`](./data.md#class-data): A wrapper for data/data_stream.
- [`adapter.IAdapter`](./interfaces.adapter.md#class-iadapter): High level interface for Adapter.
- [`adapter.IEventAdapter`](./interfaces.adapter.md#class-ieventadapter): Interface of Adapter for events.
- [`adapter.IMessageAdapter`](./interfaces.adapter.md#class-imessageadapter): Interface of Adapter for messages.
- [`command.ICommand`](./interfaces.command.md#class-icommand): High level interface for Command.
- [`data_source.IDataSource`](./interfaces.data_source.md#class-idatasource)
- [`source_api.ISourceAPI`](./interfaces.source_api.md#class-isourceapi): High level interface for Source API.
- [`struct.IEventStruct`](./interfaces.struct.md#class-ieventstruct): Just to mark Event Struct class.
- [`struct.IMessageStruct`](./interfaces.struct.md#class-imessagestruct): Just to mark Message Struct class.
- [`stub_builder.IEventStub`](./interfaces.stub_builder.md#class-ieventstub): Just to mark Event Stub class.
- [`stub_builder.IMessageStub`](./interfaces.stub_builder.md#class-imessagestub): Just to mark Message Stub class.
- [`stub_builder.IStub`](./interfaces.stub_builder.md#class-istub)
- [`converter.ITimestampConverter`](./interfaces.utils.converter.md#class-itimestampconverter)
- [`converters.DatetimeStringConverter`](./utils.converters.md#class-datetimestringconverter): Converts datetime strings.

## Functions

- No functions


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
