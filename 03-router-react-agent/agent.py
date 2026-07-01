import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

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

    return a + b


def divide(a: int, b: int) -> int:
    """
    Divide a and b

    Args:
        a: first int
        b: second int
    """

    return a / b

tools = [add, multiply, divide]
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
llm_with_tools = llm.bind_tools(tools)


from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage

# System Message
sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs.")

# Node
def assistant(state: MessagesState) -> MessagesState:
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}


from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from IPython.display import Image, display
from langgraph.graph.state import CompiledStateGraph

# Graph
builder: StateGraph = StateGraph(MessagesState)

# Define nodes
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Define edges
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # if the latest message (result) from assistant is a tool call - tools_condition routes to tools
    # if the latest message (result) from assistant is not a tool call - tools_condition routes to END

    tools_condition
)

builder.add_edge("tools", "assistant")
react_graph: CompiledStateGraph = builder.compile()

# Dispaly
display(Image(react_graph.get_graph(xray=True).draw_mermaid_png()))

messages = [HumanMessage(content="Add 3 and 4. Multiply the output by 2. Divide the output by 5")]
messages = react_graph.invoke({"messages": messages})

for m in messages['messages']:
    m.pretty_print()



