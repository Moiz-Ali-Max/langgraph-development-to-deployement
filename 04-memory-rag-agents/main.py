import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")


from langchain_google_genai import ChatGoogleGenerativeAI

def multiply(a: int, b: int) -> int:
    """
    Multiply a and b

    Args:
        a: first int
        b: second int
    """

    return a * b

def add(a: int, b: int) -> int:
    """
    Add a and b

    Args:
        a: first int
        b: second int
    """

def divide(a: int, b: int) -> float:
    """ 
    Divie a and b

    Args:
        a: first int
        b: second int
    """
    return a / b

tools = [add, multiply, divide]
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
llm_with_tools = llm.bind_tools(tools)  


from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# System Message
sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs")

# Node
def assistant(state: MessagesState) -> MessagesState:
    return {"messages": [llm_with_tools.invoke([sys_msg] + state['messages'])]}


from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode
from IPython.display import Image, display
from langgraph.graph.state import CompiledStateGraph

# Graph
builder: StateGraph = StateGraph(MessagesState)

# Define nodes
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Define Edges
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # if the latest message (result) from assistant is a tool call - tools_condition rotues to tools
    # if the latest message (result) from assistant is not a tool call - tools_condition routes to END
    tools_condition
)

builder.add_edge("tools", "assistant")
react_graph: CompiledStateGraph = builder.compile()

# Image
display(Image(react_graph.get_graph(xray=True).draw_mermaid_png()))


messages = [HumanMessage(content="Add 3 and 4")]
messages = react_graph.invoke({"messages": messages})
for m in messages['messages']:
    m.pretty_print()


messages = [HumanMessage(content="Multiply that by 2")]
messages = react_graph.invoke({"messages": messages})
for m in messages['messages']:
    m.pretty_print()


from langgraph.checkpoint.memory import MemorySaver

memory: MemorySaver = MemorySaver()
react_graph_memory: CompiledStateGraph = builder.compile(checkpointer=memory)


# Full Graph is this;
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode
from IPython.display import Image, display
from langgraph.graph.state import CompiledStateGraph

# Graph
builder: StateGraph = StateGraph(MessagesState)

# Define nodes
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Define Edges
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # if the latest message (result) from assistant is a tool call - tools_condition rotues to tools
    # if the latest message (result) from assistant is not a tool call - tools_condition routes to END
    tools_condition
)

builder.add_edge("tools", "assistant")
react_graph: CompiledStateGraph = builder.compile(checkpointer=memory)

# Image
display(Image(react_graph.get_graph(xray=True).draw_mermaid_png()))


# Specify a thread
config = {"configurable": {"thread_id": "1"}}

# Specify an input
messages = [HumanMessage(content="Add 3 and 4")]

# Run
messages = react_graph_memory.invoke({"messages": messages}, config)
for m in messages["messages"]:
    m.pretty_print()


