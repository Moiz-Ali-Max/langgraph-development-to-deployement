# 06 LangGraph: Multiple Schemas, Filtering, Trimming, RAG
### Multiple Schemas
There are cases where we may want a bit more control over this
- Internal nodes may pass information that is not required in the graph's input/output
- We may also want to use different input/output schemas for the graph. The output might, for example, only contain output key

##### Private State
This is useful for anything needed as part of the intermediate working logic of the graph, but not relevant for the overall graph input or output
- We'll define an OverallState and a PrivateState
    - node_2 uses PrivateState as input, but writes out to OverallState

*baz is only included in PrivateState*

*node_2 uses PrivateState as input, but writes out to OverallState*

- So we can see that baz is excluded from the graph output because it is not in OverallState

##### Input/Output Schema
By default, Stategraph takes in a single schema and all nodes are expected to communicate with that schema
- However it is also possible to define explicit input and output schema for a graph.
- Often, in these cases, we define an "internal" schema that contains all keys relevant to graph operations
- But we use specific input and output schemas to constrain the input and output


*let's use a specific input and output schema with our graph*
- Here input and output schemas perform filtering on what keys are permitted on the input and output of the graph
- In addition, we can use a type hint  state: InputState to specify the input schema of each of our nodes.

### Trim Filter Messages

*We can run our chat model in a simple graph with MessageState*

##### Reducer
A practical challenege when working with messages is managing long-running conversations.
- Long running conversations result in high token usage and latency if we are not careful b/c we pass a growing list of messages to the model


##### Filtering Messages
If we don't need or want to modify the graph state, we can just filter the messages you pass to the chat model
- for example, just pass in a filtered list: llm.invoke(messages[-1:]) to the model

##### Trim Messages
Another approach is to trim messages based upon a set number of tokens.
- This restricts the message history to a specific number of tokens
- While filtering only returns a post-hoc subset of the messages between agents, trimming restricts the number of tokens that a chat model can use to respond.


