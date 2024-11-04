# How to develop DataSource implementation
## Features
Technically we only need `SourceAPI` for fully functional data source.
It fetches us data from some kind of database.
`SourceAPI` is a class that provide API for some _data source_.

But we can have other components that simplify repetitive tasks:
- **DataSource** - object storing or utilizing every other component in one way or other
- **Commands** - collection of pre-made command classes that use `SourceAPI`'s requests to return refined data
- **Adapters** - classes/methods that allow objects with one interface to convert to another

All of these classes are inheriting from [th2 core interfaces](https://github.com/th2-net/th2-data-services/tree/master/th2_data_services/interfaces).
Now let's go over basic ideas on how to create them:

## DataSource
`DataSource` is the main component which ties together everything from gathering data to processing it, so that the processed data has the interface we need.

`DataSource` is an intermediate link between the `SourceAPI` and `Commands`.
It's the place where you initialize everything in the correct way, check the connection
and do all preparatory work.

```python
class DataSource(IDataSource):
    def init(self,source_address, *other_args):
        self.api = SourceAPI(source_address)
        ...

    def command(self, cmd: ICommand):
        return cmd.handle(data_source=self.api)
```

You can manually process the data using raw data from `SourceAPI`, but to simplify this process
we usually use _command_ interface.
The _command_ method takes in a pre-made custom command object then runs it and returns processed data.

## SourceAPI
How `SourceAPI` will be structured might be different based on your needs.

The `ISourceAPI` interface does not restrict the contents of this class in any way.
The key idea is that the class should repeat the API of the original source as much as possible.

To a greater extent, this is necessary so that the IDE tells you what parameters
the source API has and does not have to look for it in the source documentation every time.

It can have any methods that you need. E.g.:

```python
class SourceAPI(ISourceAPI):
    def init(self, source_address):
        self.source_address = source_address
        ...

    def get_item(self):
        ...
```
Basically `SourceAPI` connects to _data source_ and reads/requests the data from it.

## Adapters
Adapters handle converting interface of one type to another.

```python
class AdapterFromXtoY(IAdapter):
    def handle(self, X):
        Y = # Implementation based on what X and Y are
        return Y
```

## Commands

`Commands` are a great way to call `SourceAPI` methods indirectly and utilizing raw data to return more meaningful data.

Let's take an example of a command that finds an element in data by its ID.

```python
class GetItemByID(ICommand):
    def __init__(self, id):
        self.id = id
        self.adapter = AdapterFromXtoY()

    def handle(self, data_source: DataSource):
        api: SourceAPI = data_source.api
        item = api.get_item(id)
        # If data's type is not something we want we can update it.
        data = some_processing_with_item(item)
        # E.g. we can apply adapters.
        data = self.adapter.handle(data)

        return data
```
This way we can create many `Commands` that we can reuse and in the long term is better than using `SourceAPI`'s basic methods to get data.
