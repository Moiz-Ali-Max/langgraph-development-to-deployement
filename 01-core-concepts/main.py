import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()


os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.5
)


results = llm.invoke("Hi! I am Moiz Ali Afzaal")
results


from langchain_core.messages import HumanMessage

#Creating a Human Message
msg = HumanMessage(content="what is the capital of Australia?", name="Moiz Ali Afzaal")

#Message List
messages = [msg]

#Invoke he model with a list of messages
results = llm.invoke(messages)
results


from langchain_core.messages import HumanMessage, AIMessage

messages = [
    HumanMessage(content="Hi! My name is Moiz Ali Afzaal", name="HumanMessage"),
    AIMessage(content="Hi! How can I help you?", name="AIMessage"),
    HumanMessage(content="What is the capital if Australia?", name="HumanMessage"),
    AIMessage(content="The capital of Australia is Canberra", name="AIMessage"),
    HumanMessage(content="What is my name?", name="HumanMessage")
]

results = llm.invoke(messages)
results


results.content


import os
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
load_dotenv()

tavily_search = TavilySearchResults(max_results=2)
search_web = tavily_search.invoke("Is python, fastapi, langchain, langraph, mcp, docker are enough to build a strong saas application?")
search_web


from typing_extensions import TypedDict

class LearningState(TypedDict):
    prompt: str


isb_state = LearningState(prompt="Hello, I'm Moiz From Islamabad")


print(isb_state)
print(isb_state['prompt'])
print(isb_state['prompt'] + "and I am an AI Product Engineer") #we just added a new string to the existing prompt in the learning state. This is how we can update the learning state with new information.
print(type(isb_state))


def node_1(state: LearningState) -> LearningState:
    print("Node 1: State", state)
    return {"prompt": state['prompt'] + "and I am an AI Product Engineer"}

def node_2(state: LearningState) -> LearningState:
    print("Node 2: State", state)
    return {"prompt": state['prompt'] + "NICE!"}


from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph #type

#Build Graph
builder: StateGraph = StateGraph(state_schema=LearningState)


print(type(builder))

#Nodes
builder.add_node(node_1)
builder.add_node(node_2)

# Simple Edges Logic
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", END)

# Add - Compile
graph: CompiledStateGraph = builder.compile()
print(graph)
print(graph.get_graph())

# View
display(Image(graph.get_graph().draw_mermaid_png()))
graph.invoke({"prompt" : "Hi"})


import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")


from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize and instance of the Chat Google Generative AI with specific parameters
llm: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
)


# Import the AIMessage class currently will be used for typing
from langchain_core.messages.ai import AIMessage

ai_msg: AIMessage = llm.invoke("HI!")
print(ai_msg.content)
print(type(ai_msg))


from typing_extensions import TypedDict

class FirstLlmAgentCall(TypedDict):
    prompt: str
    output: str


def node_1(state: FirstLlmAgentCall):
    print("Node 1", state)
    prompt = state['prompt']
    ai_msg: AIMessage = llm.invoke(prompt)
    return {"output": ai_msg.content}

moiz_greet_message = node_1(FirstLlmAgentCall(prompt = "Hello, I'm Moiz from Islamabad"))
print(moiz_greet_message)


from IPython.display import Image, display
from langgraph .graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph #type

#Build Graph
builder: StateGraph = StateGraph(state_schema = FirstLlmAgentCall)

#Define Nodes
builder.add_node("node_1", node_1)

#Add Edges
builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)

#Compile Graph
graph: CompiledStateGraph = builder.compile()

# View
display(Image(graph.get_graph().draw_mermaid_png()))
result = graph.invoke({"prompt": "Give me actual reason why langgraph and MCP is enough to make a strong saas application? is it actually enought or not? Forget about backend dev which I have done with python and fastapi, and frontend in reaact"})
print(result)


# Just another helper function to view response better
import textwrap
from IPython.display import display, Markdown

def to_markdown(text) -> Markdown:
    text: str = text.replace(".", " *")
    return Markdown(textwrap.indent(text, "> ", predicate = lambda _: True))

print("PROMPT: ", result['prompt'])
to_markdown(result['output'])


# State
from typing_extensions import TypedDict

class State(TypedDict):
    user_input: str


# Nodes
def node_1(state: State) -> State:
    print("Node 1", state)
    return {"user_input": state['user_input'] + " I am"}

def node_2(state: State) -> State:
    print("Node 2", state)
    return {"user_input": state['user_input'] + " Happy!"}

def node_3(state: State) -> State:
    print("Node 3", state)
    return {"user_input": state['user_input'] + " sad!"}


# before graph
import random
random.random()

import random
number: float = random.random()

if number < 0.5:
 print("The random number is less than 0.5")
else:
 print("The random number is greater than or equal to 0.5")

import random
from typing import Literal

def decide_mood(state: State) -> Literal["node_2", "node_3"]:
    user_input = state['user_input']

    if random.random() < 0.5:
        return "node_2"

    return "node_3"

# Graph Construction
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

#Build Graph
builder: StateGraph = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

# Logic
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

#ADD
graph: CompiledStateGraph = builder.compile()

#View
display(Image(graph.get_graph().draw_mermaid_png()))
graph.invoke({"user_input" : "Hi! I am Moiz"})



