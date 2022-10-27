# How to develop data source
## Features
Technically we only need Source API for fully functional data source. Source API fetches us data from some kind of database.

But we can have other components that simplify repetitive tasks
- Data Source - Object storing or utilizing every other component in one way or other
- Commands - Collection of pre-made command classes that use SourceAPI's requests to return refined data
- Adapters - Classes/Methods that allow objects with one interface to convert to another

All of these classes are inheriting from [TH2 Core Interfaces](https://github.com/th2-net/th2-data-services/tree/master/th2_data_services/interfaces)
Now let's go over basic ideas on how to create them:

## Data Source
DataSource is the main component which ties together everything from gathering data to processing it, so that the processed data has the interface we need.

```python
class DataSource(IDataSource):
    def init(self,sourceAddress):
        self.source = SourceAPI(sourceAddress)
    
    def command(self, cmd: Command):
        return cmd.handle(data_source=self)
```
Only thing we need to initialize a DataSource object is the destination to data's source.
This sourceAddress can anything: address of remote server, path to local file on local device or maybe something else. As long as SourceAPI can use it to gather data.
During initialization, we then feed the sourceAddress to SourceAPI class and keep the object as DataSource's property.

We can manually process the data using raw data from SourceAPI, but to simplify this process we create command method for DataSource.
command method takes in a pre-made custom command class. Method then runs the command on DataSource object and returns processed data.

## SourceAPI
How SourceAPI will be structured might be different based on our needs.
But it will still follow some structure:
```python
class SourceAPI(ISourceAPI):
    def init(self, sourceAddress):
        self.connect(sourceAddress)
        
    def connect(self, sourceAddress):
        #This will vary based on what kind of source we are using
        #In the end it should return a way for us to use the source data
        self.stub = DataStub(sourceAddress)
    
    # Now we can define methods that use the source to return actual data.
    def get_item(self, arg):
        self.run_checks(arg)
        return self.stub.get_item(arg)
    # We can define other methods like this
    
    # It's good practice to check if arguments are correctly inputted
    def run_checks(arg):
        if arg is None:
            raise ValueError("arg cannot be None")
        if checkSomeProperty(arg):
            raise ValueError("arg must not have 'some property'")
```
Basically SourceAPI connects to source and reads/requests the data from it.

# Commands

Commands are a great way to call SourceAPI methods indirectly and utilizing raw data to return more meaningful data.

Let's take an example of a command that finds an element in data by it's ID.

```python
class GetItemByID(ICommand):
    def __init__(self, id):
        self.id = id
        self.adapter = OneTypeToOtherAdapter()
    
    def handle(self, data_source: DataSource):
        source: SourceAPI = data_source.source
        data = source.get_item(id)
        # If data's type is not something we want we can use adapters
        data = adapter.handle(data)
        # Here we can refine data if we need
        return data
```
This way we can create many commands that we can reuse and in the long term is better than using SourceAPI's basic methods to get data.

## Adapters
Adapters handle converting interface of one class to another.

```python
class AdapterFromXtoY(IAdapter):
    def handle(self, X):
        return convert(X)
    
    def convert(X):
        # Implementation based on what X and Y are
```
