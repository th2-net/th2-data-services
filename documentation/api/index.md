<!-- markdownlint-disable -->

# API Overview

## Modules

- [`data`](./data.md#module-data)
- [`decode_error_handler`](./decode_error_handler.md#module-decode_error_handler)
- [`interfaces`](./interfaces.md#module-interfaces)
- [`interfaces.adapter`](./interfaces.adapter.md#module-interfacesadapter)
- [`interfaces.command`](./interfaces.command.md#module-interfacescommand)
- [`interfaces.source_api`](./interfaces.source_api.md#module-interfacessource_api)
- [`interfaces.utils`](./interfaces.utils.md#module-interfacesutils)
- [`interfaces.utils.converter`](./interfaces.utils.converter.md#module-interfacesutilsconverter)
- [`provider`](./provider.md#module-provider)
- [`provider.exceptions`](./provider.exceptions.md#module-providerexceptions)
- [`provider.utils`](./provider.utils.md#module-providerutils)
- [`provider.utils.version_checker`](./provider.utils.version_checker.md#module-providerutilsversion_checker)
- [`provider.v6`](./provider.v6.md#module-providerv6)
- [`provider.v6.commands`](./provider.v6.commands.md#module-providerv6commands)
- [`provider.v6.filters`](./provider.v6.filters.md#module-providerv6filters)
- [`sse_client`](./sse_client.md#module-sse_client)
- [`th2_gui_report`](./th2_gui_report.md#module-th2_gui_report)
- [`utils`](./utils.md#module-utils)
- [`utils.categorizers`](./utils.categorizers.md#module-utilscategorizers)
- [`utils.json`](./utils.json.md#module-utilsjson)
- [`utils.misc_utils`](./utils.misc_utils.md#module-utilsmisc_utils)

## Classes

- [`data.Data`](./data.md#class-data): A wrapper for data/data_stream.
- [`adapter.IAdapter`](./interfaces.adapter.md#class-iadapter): High level interface for Adapter.
- [`adapter.IEventAdapter`](./interfaces.adapter.md#class-ieventadapter): Interface of Adapter for events.
- [`adapter.IMessageAdapter`](./interfaces.adapter.md#class-imessageadapter): Interface of Adapter for messages.
- [`command.ICommand`](./interfaces.command.md#class-icommand): High level interface for Command.
- [`source_api.ISourceAPI`](./interfaces.source_api.md#class-isourceapi): High level interface for Source API.
- [`converter.ITimestampConverter`](./interfaces.utils.converter.md#class-itimestampconverter)
- [`exceptions.CommandError`](./provider.exceptions.md#class-commanderror): Exception raised for errors in the command.
- [`exceptions.EventNotFound`](./provider.exceptions.md#class-eventnotfound)
- [`exceptions.MessageNotFound`](./provider.exceptions.md#class-messagenotfound)
- [`sse_client.SSEClient`](./sse_client.md#class-sseclient): Patch for sseclient-py to get availability to configure decode error handler.
- [`th2_gui_report.Th2GUIReport`](./th2_gui_report.md#class-th2guireport): Class for creating gui link by event ID or message ID.
- [`categorizers.EventCategorizer`](./utils.categorizers.md#class-eventcategorizer)
- [`json.BufferedJSONProcessor`](./utils.json.md#class-bufferedjsonprocessor)

## Functions

- [`decode_error_handler.handler`](./decode_error_handler.md#function-handler): Decode error handler that tries change utf-8 character to Unicode.
- [`version_checker.get_package_version`](./provider.utils.version_checker.md#function-get_package_version)
- [`version_checker.get_version_by_pip`](./provider.utils.version_checker.md#function-get_version_by_pip)
- [`version_checker.verify_grpc_version`](./provider.utils.version_checker.md#function-verify_grpc_version)
- [`misc_utils.analyze_stream_sequence`](./utils.misc_utils.md#function-analyze_stream_sequence)
- [`misc_utils.create_qty_distribution`](./utils.misc_utils.md#function-create_qty_distribution)
- [`misc_utils.extract_time_string`](./utils.misc_utils.md#function-extract_time_string)
- [`misc_utils.get_category_measurement_p`](./utils.misc_utils.md#function-get_category_measurement_p)
- [`misc_utils.get_category_totals_p`](./utils.misc_utils.md#function-get_category_totals_p)
- [`misc_utils.get_objects_frequencies`](./utils.misc_utils.md#function-get_objects_frequencies)
- [`misc_utils.print_measurement_dict`](./utils.misc_utils.md#function-print_measurement_dict)
- [`misc_utils.print_stats_dict`](./utils.misc_utils.md#function-print_stats_dict)
- [`misc_utils.process_objects_stream`](./utils.misc_utils.md#function-process_objects_stream)
- [`misc_utils.time_interval_filter_seconds_precision`](./utils.misc_utils.md#function-time_interval_filter_seconds_precision)
- [`misc_utils.time_slice_object_filter`](./utils.misc_utils.md#function-time_slice_object_filter)
- [`misc_utils.timestamp_aggregation_key`](./utils.misc_utils.md#function-timestamp_aggregation_key)
- [`misc_utils.timestamp_delta_us`](./utils.misc_utils.md#function-timestamp_delta_us)
- [`misc_utils.update_int_measurement`](./utils.misc_utils.md#function-update_int_measurement)


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
