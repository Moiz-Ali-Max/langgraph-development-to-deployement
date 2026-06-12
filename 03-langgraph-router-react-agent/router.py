import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")


from langchain_google_genai import ChatGoogleGenerativeAI

def multiply(a: int, b: int) -> int:
    """
    Mmultiply a and b

    Args:
        a: first int
        b: second int
    """

    return a * b


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
llm_with_tools = llm.bind_tools([multiply])


from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langgraph.graph.state import CompiledStateGraph

# Node
def tool_calling_llm(state: MessagesState) -> MessagesState:
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Build Graph
builder: StateGraph = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode([multiply]))
builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges(
    "tool_calling_llm",
    # if the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # if the latest message (result) from assistant is not a tool call -> tools_consition routes to END

    tools_condition,
)
builder.add_edge("tools", END)
graph: CompiledStateGraph = builder.compile()

# View
display(Image(graph.get_graph().draw_mermaid_png()))


from langchain_core.messages import HumanMessage
messages = [HumanMessage(content="Hi Gemini")]
messages = graph.invoke({"messages": messages})
for m in messages['messages']:
    m.pretty_print()


from langchain_core.messages import HumanMessage
messages = [HumanMessage(content="Hi Gemini, product 5 and 5")]
messages = graph.invoke({"messages": messages})
for m in messages['messages']:
    m.pretty_print()


