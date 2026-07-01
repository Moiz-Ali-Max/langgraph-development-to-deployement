# 02 LangGraph - Tool Calling, Reducers

### Module 2
**1. tools_messages**

**2. chains_reducers**


#### 2.1 Tools Messages (Tool Calling)

##### Tools are useful whenever you want a model to interact with external system
- Externla systems (e.g., API's) often require a particular input schema or payload, rather than natural language.
- when we bind an API, for example, as a tool we given the model awareness of the required input schema.
- The model will choose to call a tool based upon the natural language input from the user.
- And it will return an output that adheres to the tool's schema.
- Many LLM providers support tool calling and tool calling interface in langchain is simple
- We can simply pass any python function into ChatModel.bind_tools(function)


#### Current Flow:
 - LLM: Call this tool
 - System: Called Tool and told LLM the result

Issue: Where is my Human Message?

Right now in response we only have AI Message

*Solutions:*
1. Proposal 1: manually add messages in call_llm using llm
2. Proposal 2: Reducer function to keep hisotry context


#### 2.2 Chains & Reducers

*In Chaining we have four concepts*
1. Using chat messages as our graph state
2. Using chat models in graph nodes
3. Binding tools to our chat model
4. Executing tool calls in graph nodes

##### Messages
Chat models can use messages which capture different roles within a conversation
- Lnagchain supports various message types including Human Messages, AI Message, System Message and Tool Message
- These represents a message from the user, from the chat model, for the chat model to instruct behavior, and from a tool call

*Each Message can be supplied with a few things*
- **contnet** which is content of the message
- **name** which is optional, means a message author
- **response_metadata** also it is optional, a dict of metadata (e.g., often populated by model provider for AI Message)


##### Tools
Tools are useful whenever you want a model to interacct with external system
- External Systems (e.g., APIs) often require a particular input schema or payload, rather than natural language
- When we bind an API, for example as a toolwe given the model awareness of the required input schema.
- The model will choose to call a tool based upon the natural language input from the user
- And it will return an output that adheres to the tool's schema
- Many LLMs provider support tool calling and tool calling interface, in langchain you can simple pass any python function into ChatModel.bind_tools(function)


##### Using messages as a state
- MessageState as a TypedDict with a single key: messages

messages is simple a list of messages (like Human Messsage, etc.,)

##### Reducers
Previously there's a minor problem that each node will return a new value for our state ey messages, but this new value will override the prior message value. As our graph runs, we want to append messages to our messages state key.

*we can use a reducer function to resolve this* 
Reducer allow us to specify how state updates are performed 
- If no reducer function is specified then it is asumed that updates to the key should override it as we saw before
- But to append messages, we can use the pre-built add_messages reducer
- This ensures that any messages are appended to the existing list of messages
- we annotate simply need to annotate our messages key with the add_messages reducer function as metadata


Since having a list of messages in graph state is so common, LangGraph has a pre-built MessageState

MessageState is defined:
- With a pre-build single messages key
- This is a list of AnyMessage objects
- It uses the add_messages reducer

we'll usually use MessageState b/c it is less verbose tahn defining a custom TypedDict


