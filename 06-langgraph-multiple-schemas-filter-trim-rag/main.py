from typing_extensions import TypedDict
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

class OverallState(TypedDict):
    foo: int
    baz: int

def node_1(state: OverallState) -> OverallState:
    print("---Node 1---")
    return {"baz": state['foo'] + 1}

def node_2(state: OverallState) -> OverallState:
    print("---Node 2---")
    return {"foo": state['baz'] + 1}

# Build Graph
builder: StateGraph = StateGraph(OverallState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)

# Logic
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", END)

# Add
graph: CompiledStateGraph = builder.compile()

# View
display(Image(graph.get_graph().draw_mermaid_png()))

graph.invoke({"foo": 1})


from typing_extensions import TypedDict
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

class OverallState(TypedDict):
    foo: int

class PrivateState(TypedDict):
    baz: int

def node_1(state: OverallState) -> PrivateState:
    print("---Node 1---")
    return {"baz": state['foo'] + 1}

def node_2(state: PrivateState) -> OverallState:
    print("---Node 2---")
    return {"foo": state['baz'] + 1}

# Build Graph
builder: StateGraph = StateGraph(OverallState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)

# Logic 
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", END)

# Add
graph: CompiledStateGraph = builder.compile()

# View
display(Image(graph.get_graph().draw_mermaid_png()))
graph.invoke({"foo": 1})


class OverallState(TypedDict):
    question: str
    answer: str
    notes: str  

def thinking_node(state: OverallState) -> OverallState:
    return {"answer": "bye", "notes": "... His name is Moiz"}

def answer_node(state: OverallState) -> OverallState:
    return {"answer": "Bye Moiz"}

graph: StateGraph = StateGraph(OverallState)
graph.add_node("answer_node", answer_node)
graph.add_node("thinking_node", thinking_node)

graph.add_edge(START, "thinking_node")
graph.add_edge("thinking_node", "answer_node")
graph.add_edge("answer_node", END)

graph: CompiledStateGraph = graph.compile()

display(Image(graph.get_graph().draw_mermaid_png()))
graph.invoke({"question": "hi", "answer": "", "notes": ""})


class InputState(TypedDict):
    question: str

class OutputState(TypedDict):
    answer: str

class OverallState(TypedDict):
    question: str
    answer: str
    notes: str

def thinking_node(state: InputState):
    return {"ansswer": "bye", "notes": "... his name is Moiz"}

def answer_node(state: OverallState):
    return {"answer": "Bye Moiz"}

graph: StateGraph = StateGraph(OverallState, input=InputState, output=OutputState)

graph.add_node("answer_node", answer_node)
graph.add_node("thinking_node", thinking_node)

graph.add_edge(START, "thinking_node")
graph.add_edge("thinking_node", "answer_node")
graph.add_edge("answer_node", END)

graph: CompiledStateGraph = graph.compile()

display(Image(graph.get_graph(). draw_mermaid_png()))
graph.invoke({"question": "hi"})


import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

from pprint import pprint
from langchain_core.messages import AIMessage, HumanMessage

messages = [AIMessage(f"So you said you were researching ocean mammals", name="Bot")]
messages.append(HumanMessage(f"Yes, I know about whales. But what others should I learn about? Give one line answer.", name="Moiz"))

for m in messages:
    m.pretty_print()


from langchain_google_genai import ChatGoogleGenerativeAI

llm: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
llm.invoke(messages)


from IPython.display import Image, display
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

# Node
def chat_model_node(state: MessagesState) -> MessagesState:
    return {"messages": llm.invoke(state["messages"])}

# Build Graph
builder: StateGraph = StateGraph(MessagesState)

builder.add_node("chat_model", chat_model_node)

builder.add_edge(START, "chat_model")
builder.add_edge("chat_model", END)

graph: CompiledStateGraph = builder.compile()

display(Image(graph.get_graph().draw_mermaid_png()))


output = graph.invoke({'messages': messages})
for m in output['messages']:
    m.pretty_print()


#async for m in graph.astream_events({'messages': messages}, version="v2"):
    print(m)
    # on_chain_start = start of a node's execution
    # on_chain_end = indicates the completion of node's execution
    # on_chain_stream = represent intermediate data or progress updates during a node's execution

    print("\n-----------------\n")

from langchain_core.messages import RemoveMessage

# Nodes
def filter_messages(state: MessagesState) -> MessagesState:
    # Delete all but the 2 most recent messages
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    print(delete_messages)
    return {"messages": delete_messages}

def chat_model_node(state: MessagesState) -> MessagesState:
    return {"messages": [llm.invoke(state["messages"])]}

# Build Graph
builder: StateGraph = StateGraph(MessagesState)

builder.add_node("filter", filter_messages)
builder.add_node("chat_model", chat_model_node)

builder.add_edge(START, "filter")
builder.add_edge("filter", "chat_model")
builder.add_edge("chat_model", END)

graph: CompiledStateGraph = builder.compile()

display(Image(graph.get_graph().draw_mermaid_png()))


# # Message list with a preamble
# messages = [AIMessage("Hi. ", name="Bot", ide="1")]
# messages.append(HumanMessage("Hi.", name="Moiz", id="2"))
# messages.append(AIMessage("So you were research about ocean mamals?", name="Bot", id="3"))
# messages.append(HumanMessage("Yes, I know whales, what about other should I learn?", name="Moiz", id="4"))

# # Invoke
# output = graph.invoke({'messages': messages})
# for m in output['messages']:
#     m.pretty_print()


