<!-- markdownlint-disable -->

# API Overview

## Modules

- [`decode_error_handler`](./decode_error_handler.md#module-decode_error_handler)
- [`events_tree`](./events_tree.md#module-events_tree)
- [`events_tree.events_tree`](./events_tree.events_tree.md#module-events_treeevents_tree)
- [`events_tree.exceptions`](./events_tree.exceptions.md#module-events_treeexceptions)
- [`exceptions`](./exceptions.md#module-exceptions)
- [`sse_client`](./sse_client.md#module-sse_client)
- [`utils`](./utils.md#module-utils)

## Classes

- [`events_tree.EventsTree`](./events_tree.events_tree.md#class-eventstree): EventsTree is a tree-based data structure of events.
- [`exceptions.EventIdNotInTree`](./events_tree.exceptions.md#class-eventidnotintree)
- [`exceptions.FieldIsNotExist`](./events_tree.exceptions.md#class-fieldisnotexist)
- [`exceptions.CommandError`](./exceptions.md#class-commanderror): Exception raised for errors in the command.
- [`exceptions.EventNotFound`](./exceptions.md#class-eventnotfound)
- [`exceptions.MessageNotFound`](./exceptions.md#class-messagenotfound)
- [`sse_client.SSEClient`](./sse_client.md#class-sseclient): Patch for sseclient-py to get availability to configure decode error handler.

## Functions

- [`decode_error_handler.handler`](./decode_error_handler.md#function-handler): Decode error handler that tries change utf-8 character to Unicode.


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
