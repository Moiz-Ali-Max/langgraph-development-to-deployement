# 01 - LangGraph Core Concepts


To use SDK of google to chat with the model, b/c langgraph doesn't have this
```
pip install langchain-google-genai langchain-core
```


### MODULE 0
**0.1: Simple Chat invoking**

**0.2: Human Message and AI Message**

**0.3: LangChain Core**

**0.4: LangChain Community**

**0.5: Search Tool (TAVILY Search API)**

- just for testing purpose to check our gemini model is working or not
- Chat models in langchain have a number of default response

**Stream**: SStream back chunks of the response

**Invoke**: Call the claim on an input
- Chat models take message as input. Messages have a role (that describes who is saying the message) and a content property


### Search Tools
- We use Tavily for this purpose
- Tavily gives us some credits where can do some web research and design the agent in a way that can do realtime web-search


### Module 01:
**State**

**Edges**

**Nodes**

**Graphs**


#### State:
State scehmas serves as the input schema for all Nodes and Edges in the graph.
- For now let's use the TypedDict class from python's typing module as our schema, which provides type hints for the keys


#### Nodes:
Nodes are functions
- Because the state is a TypedDict with schema as defined above, each node can access the key, graph_state with state['grah_state']
- Each node returns a new value of the state key graph_state
- By default, the new value returned by each node will override the prior state value


#### Edges:
Edges connect the nodes
- Normal Edges are used if you want to always go from, for example node_1 to node_2


