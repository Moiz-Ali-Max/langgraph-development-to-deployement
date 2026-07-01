from pprint import pprint
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

messages = [AIMessage(content=f"So you said you were researching about ai research engineers?", name="Model")]
messages.append(HumanMessage(content=f"Yes, that's right", name="Moiz"))
messages.append(AIMessage(content=f"Great! What specific aspects of ai research engineering are you interested in?", name="Model"))
messages.append(HumanMessage(content=f"I want to learn about those people who works in openai, deepmind, what are their mindset"))

for m in messages:
    m.pretty_print()


import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")



from langchain_google_genai import ChatGoogleGenerativeAI
llm: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")

simple_call = llm.invoke("Hi")
simple_call.content


def deposit_money(name: str, bank_account_no: int, amount: int) -> str:
    """
    Deposit Money in Bank Account

    Args:
        name: account holder name
        bank_account_no: bank account id
        amount: amount to be deposited

    Returns:
        str: deposit status
    """

    #Business Logic for Bank Deposit
    return f"Deposit {amount} Sucessful in {name} Account"


deposit_money(name="Moiz", bank_account_no=1122334455, amount=500)
llm_with_tools = llm.bind_tools([deposit_money])
llm_with_tools

from langchain_core.messages import HumanMessage

call = llm.invoke(
    [HumanMessage(content=f"Deposit 200 in Ahmad Account. His acc number is 5544332211", name="Muhammad")]
)

call


call = llm_with_tools.invoke(
    [HumanMessage(content=f"Deposit 200 in Ahmad Account. His acc number is 5544332211", name="junaid")]
)

call


# Building Graph
from typing_extensions import TypedDict

class LastMessageState(TypedDict):
    messages: list

# 1. too calling - LLM Node
def call_llm(state: LastMessageState):
    messages = state["messages"]
    call_response = llm_with_tools.invoke(messages)
    
    return {"messages": [call_response]}

# 2. Graph
from langgraph.graph import StateGraph, START, END
builder: StateGraph = StateGraph(LastMessageState)

# define nodes
builder.add_node("call_llm_with_tools", call_llm)

# define edges
builder.add_edge(START, "call_llm_with_tools")
builder.add_edge('call_llm_with_tools', END)

# build graph
graph = builder.compile()

from IPython.display import display, Image
display (Image(graph.get_graph().draw_mermaid_png()))

graph.invoke({"messages": [HumanMessage(content = "Hi")]})

graph.invoke({"messages": [HumanMessage(content = "Deposit 10000 in Ali account, his bank accountn num is 0011")]})
from pprint import pprint


from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

messages = [AIMessage(content=f"So you said you were researching about ai research engineers?", name="Model")]
messages.append(HumanMessage(content=f"Yes, that's right", name="Moiz"))
messages.append(AIMessage(content=f"Great! What specific aspects of ai research engineering are you interested in?", name="Model"))
messages.append(HumanMessage(content=f"I want to learn about those people who works in openai, deepmind, what are their mindset"))

for m in messages:
    m.pretty_print()


def multiply (a: int, b: int) -> int:
    """ 
    Multiply a and b

    Args:
        a: first int
        b: second int
    """
    
    return a*b

llm_with_tools: ChatGoogleGenerativeAI = llm.bind_tools([multiply])
function_call = llm_with_tools.invoke([HumanMessage(content=f"what is 2 multiply by 6", name="Moiz")])
function_call

function_call.additional_kwargs['function_call']


from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage

class MessageState(TypedDict):
    messages: list[AnyMessage]


from typing import Annotated
from langgraph.graph.message import add_messages

class MessageState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


from langgraph.graph import MessagesState

class MessagesConversationalState(MessagesState):
    pass


# Initial State
initial_messages = [AIMessage(content="Hello! How can I assist you?", name = "Model"),
                    HumanMessage(content="I'm looking for information on method acting in films", name = "Moiz")]

# new messages to ADD
new_messages = AIMessage(content="Sure, I can help with that. What specifically are you interested in?", name = "Model")

#test
add_messages(initial_messages, new_messages)


from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

# Node
def tool_calling_llm(state: MessagesConversationalState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Build Graph
builder: StateGraph = StateGraph(MessagesConversationalState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_edge(START, "tool_calling_llm")
builder.add_edge("tool_calling_llm", END)
graph: CompiledStateGraph = builder.compile()

# View
display(Image(graph.get_graph().draw_mermaid_png()))

messages = graph.invoke({"messages": HumanMessage(content="Hello!")})
for m in messages['messages']:
    m.pretty_print()

messages = graph.invoke({"messages": HumanMessage(content="Multiply 2 by 3")})
for m in messages['messages']:
    m.pretty_print()


