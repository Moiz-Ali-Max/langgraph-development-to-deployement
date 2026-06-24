# Module 2

### Schema
When we defined a langgraph StateGraph, we use a state schema
- The state schema represents the strucutre and types of data that our graph will use.
- All nodes are expected to communicate with that schema
- Langgraph offers flexbility in how you define your state schema, accomodating various python types and validation approaches


##### TypedDict
Previously, we used TypedDict class from python's typing module, it allows to specify keys and their corresponding value types

*But these are type hints*

- They can used by static type checkers (like mypy), but they are not enforced at runtime

*We can use our defined state class (e.g., TypedDictState) in LangGraph by simply passing it to StateGraph*

- and we can think about each state key just a "channel" in our graph.
- Previosuly we saw, we overwrite the value of a specified key or "channel" in each node

##### Dataclass
Python's dataclass provide another way to define strucutre data
- Dataclasses offer a concise syntax for creating classes that are primarily used to store data

To access the keys of a dataclass, we just need to modify the subscripting used in node_1:
- We use state.name for the dataclass state rather than state ["name] for the TypedDict above
- Here'a a catch, in each node we still return a dictionary to perform the state updates

*This is possible b/c LangGraph stores each key of your state object separately*

The object returned by the node only needs to have keys (attributes) that match those in the state

*In this case, the dataclass has key **name** so we can update it by passing a dict from our node, just as we did when state was a TypedDict*

##### Pydantic
Previously TypedDict and Dataclasses, they provide type hints but don't enforce types at runtime
- Means we could potentially assign invalid values without raising an error
- *For example we set mood to mad even though our type hint specifies mood: list[Literal["happy", "sad"]]*

Pydantic is a data validation and settings management ibrary using python type annotations
- It's particularly well-suited for defining state schemas in Langgraph due to it's validation capabilities.
- Pydantic can perform validation to check wether data confirms to the specified types and contraints at runtime


*We can use Pydantic State in our graoh seamlessly*

##### Custom Reducer
To address cases like that we can also define custom reducers
- E.g., define custom reducer logic to combine lists and handle cases where either or both of the inputs might be None

