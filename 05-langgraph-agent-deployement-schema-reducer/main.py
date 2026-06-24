import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")


from typing_extensions import TypedDict

class TypedDictState(TypedDict):
    foo: str
    bar: str


choco_bars: TypedDictState = TypedDictState(company="Choco", bar="M&Ms")
print(choco_bars["bar"])
print(choco_bars["company"])


from typing import Literal

class TypeDictState(TypedDict):
    name: str
    mood: Literal["happy", "sad"]

override_mood: TypeDictState = TypeDictState(name="Moiz", mood="mad", random_field="user")
override_mood["mood"]
print(override_mood)


import random
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

def node_1(state: TypeDictState):
    print("---Node 1---")
    return {"name": state["name"] + " is ..."}

def node_2(state: TypeDictState):
    print("---Node 2---")
    return {"mood": "mad"}

def node_3(state: TypeDictState):
    print("---Node 3---")
    return {"mood": "Sad"}

def decide_mood(state: TypeDictState) -> Literal["node_2", "node_3"]:
    # do 50/50 split
    if random.random() < 0.5:
        return "node_2"
    
    return "node_3"

# Build Graph
builder: StateGraph = StateGraph(TypeDictState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

# Logic
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

# Add
graph: CompiledStateGraph = builder.compile()

# View
display(Image(graph.get_graph().draw_mermaid_png()))
graph.invoke({"name": "Moiz"})


from dataclasses import dataclass

@dataclass
class DataClassState:
    name: str
    mood: Literal["happy", "sad"]


# no_name: DataClassState = DataClassState(mood="mad")
# print(no_name)
#TypeError: DataClassState.__init__() missing 1 reqired positional argument: 'name'

no_name: DataClassState = DataClassState(mood="mad", name="moiz")
print(no_name)


def node_1(state: DataClassState) -> dict:
    print("---Node 1---")
    return {"name": state.name + " is ..."}

def node_2(state: DataClassState) -> dict:
    print("---Node 2---")
    return {"mood": "happy"}

def node_3(state: DataClassState) -> dict:
    print("---Node 3---")
    return {"mood": "sad"}

# Build Graph
builder: StateGraph =  StateGraph(DataClassState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

# Logic
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

# Add
graph: DataClassState = builder.compile()

# View
display(Image(graph.get_graph().draw_mermaid_png()))
graph.invoke(DataClassState(name="Moiz", mood="sad"))
graph.invoke({"name": "Moiz", "mood": "still not enforced", "random_field": "user"})

from pydantic import BaseModel, field_validator, ValidationError

class PydanticState(BaseModel):
    name: str
    mood: Literal ["happy", "sad"]

    @field_validator('mood')
    @classmethod
    def validate_mood(cls, value):
        if value not in ["happy", "sad"]:
            raise ValueError("Each mood must be either happy or sad")
        
        return value
    
try:
    state = PydanticState(name="Moiz Ali", mood="mad")
except ValidationError as e:
    print("Validation Errot", e)


def node_1(state: PydanticState):
    print("---Node 1---")
    return {"name": state.name + " is ..."}

def node_2(state: PydanticState):
    print("---Node 2---")
    return {"mood": "happy"}

def node_3(state: PydanticState):
    print("---Node 3---")
    return {"mood": "sad"}

def decide_mood(state: PydanticState) -> Literal["node_2", "node_3"]:
    if random.random() < 0.5:
        return "node_2"
    
    return "node_3"

# Build Graph
builder: StateGraph = StateGraph(PydanticState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

# Logic
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

# ADD
graph: CompiledStateGraph = builder.compile()

# View
display(Image(graph.get_graph().draw_mermaid_png()))


graph.invoke(PydanticState(name="Moiz", mood="sad"))
# graph.invoke(PydanticState(name="Moiz", mood="mad")) # gives error b/c we use pydantic


from langchain_core.tools import tool

@tool
def search(query: str) -> str:
    """Call to Surf the Web"""
    # This is the placeholder for actual implementation
    # LLM don't know this

    return "The answer to your question lies within."


tools = [search]


from langgraph.prebuilt import ToolNode

tool_node: ToolNode = ToolNode(tools)

from langchain_google_genai import ChatGoogleGenerativeAI
llm: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
model: ChatGoogleGenerativeAI = llm.bind_tools(tools)


import operator
from pydantic import BaseModel
from typing import Annotated, Sequence
from langchain_core.messages import BaseMessage

class AgentState(BaseModel):
    messages: Annotated[Sequence[BaseMessage], operator.add]


# Define the function that determines whether to conitnue or not
def should_continue(state: AgentState) -> Literal["end", "continue"]:
    messages = state.messages
    last_message = messages[-1]
    # if there is no function call, then we finish
    if not last_message.tool_calls:
        return "end"
    
    # otherwise, we continue
    else:
        return "continue"
    
# Define the function that calls the model
def call_model(state: AgentState):
    messages = state.messages
    response = model.invoke(messages)

    # we return a list, b/c this will get added to the existing list
    return {"messages": [response]}


from langgraph.graph import StateGraph, START, END

# Define a new graph
workflow: StateGraph = StateGraph(AgentState)

# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("action", tool_node)

# Set the entrypoint as agent
# means this node is the first one called
workflow.add_edge(START, "agent")

# We now add a conditional edge
workflow.add_conditional_edges(
    # First we define the start node, we use 'agent'
    # Means these are te edges taken after the 'agent' node is called
    "agent",

    # Next we pass in the function that will determine which node is called next
    should_continue,
    # Finally we pass in the mapping
    # The keys are strings, and the value are other nodes
    # END is a special node marking that the graph should finish
    # What will happen is we will call 'should_continue', and then the output of that
    # Will be matched against the keys in this mapping
    # Based om which one it matches, that node will then be called
    {
        # if 'tools', then we call the tool_node
        "continue": "action",
        # otherwise, we finsih
        "end": END,
    }
)

# We now add a normal edge from 'tools' to 'agent'
# Means that after 'tools' is called, 'agent' node is called next
workflow.add_edge("action", "agent")

# then compile it
# this compiles it into runnables
# means we can use it as you would any other runnables
app: CompiledStateGraph = workflow.compile()
app.get_graph()

from IPython.display import Image, display

display(Image(app.get_graph().draw_mermaid_png()))

from langchain_core.messages import HumanMessage

inputs = {"messages": [HumanMessage(content="Search the tool for what is the weather in Isb")]}
for chunk in app.stream(inputs, stream_mode="values"):
    chunk["messages"][-1].pretty_print()

from typing_extensions import TypedDict
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

class State(TypedDict):
    foo: int

def node_1(state: State) -> dict:
    print("---Node 1---")
    return {"foo": state['foo'] + 1}

# Build Graph
builder: StateGraph = StateGraph(State)
builder.add_node("node_1", node_1)

# Logic
builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)

# Add
graph: CompiledStateGraph = builder.compile()

# View
display(Image(graph.get_graph().draw_mermaid_png()))
graph.invoke(State(foo = 1))


def node_1(state: State):
    print("---Node 1---")
    return {"foo": [state['foo'][-1] + 1]}

def node_2(state: State):
    print("---Node 2---")
    return {"foo": [state["foo"][-1] + 1]}

def node_3(state: State):
    print("---Node 3---")
    return {"foo": [state['foo'][-1] + 1]}

# Build Graph
builder: StateGraph = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

# Logic
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_1", "node_3")
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

# Add
graph: CompiledStateGraph = builder.compile()

# View
display(Image(graph.get_graph().draw_mermaid_png()))
#graph.invoke({"foo": [1]})

try:
    graph.invoke({"foo": None})
except Exception as e:
    print(f"TypeError occured: {e}")

def reduce_list(left: list | None, right: list | None) -> list:
    """
    Safely combine two lists, handling cases where either or both inputs might be None.

    Args:
        left (list | None): The first list to combine, or None.
        right (list | None): The second list to combine, or None.

    Returns:
        list: A new list containing all elements from both input lists.
            If an input is None, it's treated as an empty list
    """

    if not left:
        left = []
    if not right:
        right = []  
    
    return left + right

class DefaultState(TypedDict):
    foo: Annotated[list[int], add]

class CustomReducerState(TypedDict):
    foo: Annotated[list[int], reduce_list]


def reduce_list(left: list | None, right: list | None) -> list:
    """
    Safely combine two lists, handling cases where either or both inputs might be None.

    Args:
        left (list | None): The first list to combine, or None.
        right (list | None): The second list to combine, or None.

    Returns:
        list: A new list containing all elements from both input lists.
            If an input is None, it's treated as an empty list
    """

    if not left:
        left = []
    if not right:
        right = []  
    
    return left + right

class DefaultState(TypedDict):
    foo: Annotated[list[int], add]

class CustomReducerState(TypedDict):
    foo: Annotated[list[int], reduce_list]


def node_1(state: DefaultState):
    print("---Node 1---")
    return {"foo": [2]}

# Build Graph
builder: StateGraph = StateGraph(DefaultState)
builder.add_node("node_1", node_1)

# Logic
builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)

# ADD
graph: CompiledStateGraph = builder.compile()

# View
display(graph.get_graph().draw_mermaid_png())

try:
    print(graph.invoke({"foo": None}))
except Exception as e:
    print(f"TypeError occurred: {e}" )


def node_1(state: CustomReducerState):
    print("---Node 1---")
    return {"foo": [2]}

# Build Graph   
builder: StateGraph = StateGraph(CustomReducerState)
builder.add_node("node1_1", node_1)

# Logic
builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)

# ADD
graph: CompiledStateGraph = builder.compile()

# View
display(Image(graph.get_graph().draw_mermaid_png()))

try:
    print(graph.invoke({"foo": None}))
except Exception as e:
    print(f"TypeError occured: {e}")


from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import MessagesState
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

# Define a custom TypedDict that includes a list of messages with add_messages reducer
class CustomMessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    added_key_1: str
    added_key_2: str

# Use MessagesState which includes the messages key with add_messages reducer
class ExtendedMessagesState(MessagesState):
    # Add any keys needed beyond messages, which is pre-built
    added_key_1: str
    added_key_2: str


from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage, HumanMessage

# Initial State
initial_messages = [
    AIMessage(content="Hello! How can I assist you?", name="Model"),
    HumanMessage(content="I'm looking for information on marine biology", name="Moiz")
]

# new message to add
new_message = AIMessage(content="Sure, I can help with that. What specifically are you interested in?", name="Model")

# Test
add_messages(initial_messages, new_message)


# Initial State
initial_messages = [
    AIMessage(content="HI! How can I assist you", name="model", id=2),
    HumanMessage(content="I'm looking for information on Marine Biology", name="Moiz", id=2)
]

# New messages to add
new_message = HumanMessage(content="I'm looking for information on sp3 hybridization", name="Moiz", id=2)

# Test 
add_messages(initial_messages, new_message)

from langchain_core.messages import RemoveMessage

# Message List
messages = [AIMessage("Hi", name="Bot", id="1")]
messages.append(HumanMessage("Hi", name="Moiz", id="2"))
messages.append(AIMessage("So you said you were researching ocean mammals?", name="Bot", id="3"))
messages.append(HumanMessage("Yes, I know about whales. But what others should I learn about?", name="Moiz", id="4"))

# Isolate messages to delete
delete_messages = [RemoveMessage(id=m.id) for m in messages[:-2]] # Select all the elements of list except last 2
print(delete_messages)





