import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

from langchain_google_genai import ChatGoogleGenerativeAI

model: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
model.invoke("Hi")

from langgraph.graph import MessagesState

class State(MessagesState):
    summary: str

from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage

# Define the logic to call the model
def call_model(state: State) -> State:

    # Get Summary if it exists
    summary = state.get("summary", "")

    # If there is summary, then we add it
    if summary:
        # Add summary to system message
        system_message = f"Sumary of conversation earlier: {summary}"

        # Append summary to any newer messages
        messages = [SystemMessage(content=system_message)] + state["messages"]

    else:
        messages = state["messages"]

    response = model.invoke(messages)
    return {"messages": response}

def summarize_conversation(state: State):

    # First we get any existing summary
    summary = state.get("summary", "")

    # Create our summarization prompt
    if summary:
        # A summary already exists
        summary_message = (
            f"This is the summary of conversation to date: {summary}\n\n"
            "Extend the summary by taking into account the new messages above:"
        )

    else:
        summary_message = "Create a summary of the conversation above:"
    
    # Add prompt to our history
    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = model.invoke(messages)

    # Delete all but the 2 most recent messages
    delete_messages = [RemoveMessage(id=m.id) for m in state['messages'][:-2]]
    return {"summary": response.content, "messages": delete_messages}

from langgraph.graph import END

# Determine whether to end or summarize the conversation
def should_continue(state: State):
    """
    Return the next node to execute
    """

    messages = state["messages"]

    # If there are more than six messages, then we summarize the conversation
    if len(messages) > 6:
        return "summarize_conversation"
    
    # Otherwise we can just end
    return END

from IPython.display import Image, display
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START
from langgraph.graph.state import CompiledStateGraph

# Define a new graph
workflow: StateGraph = StateGraph(State)
# workflow.add_node = ("conversation", call_model)
# workflow.add_node = (summarize_conversation)
workflow.add_node("conversation", call_model)
workflow.add_node("summarize_conversation", summarize_conversation)

# Set the entrypoint as conversation
workflow.add_edge(START, "conversation")
# workflow.add_conditional_edges("conversation", should_continue)
workflow.add_conditional_edges(
    "conversation",
    should_continue,
    path_map={
        "summarize_conversation": "summarize_conversation",
        END: END,
    },
)
workflow.add_edge("summarize_conversation", END)

# Compile
memory: MemorySaver = MemorySaver()
graph: CompiledStateGraph = workflow.compile(checkpointer=memory)

# View
display(Image(graph.get_graph().draw_mermaid_png()))

# Create a thread
config = {"configurable": {"thread_id": "2"}}

# Start Conversation
input_message = HumanMessage(content="Hi! I am Moiz")
output = graph.invoke({"messages": [input_message]}, config)
for m in output['messages'][-1:]:
    m.pretty_print()

input_message = HumanMessage(content="what's my name?")
output =  graph.invoke({"messages": [input_message]}, config)
for m in output['messages'][-1:]:
    m.pretty_print()

input_message = HumanMessage(content="I like SRK")
output = graph.invoke({"messages": [input_message]}, config)
for m in output['messages'][-1:]:
    m.pretty_print()


config = {"configurable": {"thread_id": "2"}}
graph_state = graph.get_state(config)
graph_state

from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver

# Connection pool for efficient database access
connection_kwargs = {"autocomes": True, "prepare_threshold": 0}

# Create a persistent connection pool
pool = ConnectionPool(conninfo=DB_URI, max_size=20, kwargs=connection_kwargs)

# Initialize PostgresSaver Checkpointer
checkpointer = PostgresSaver(pool)
checkpointer.setup() 

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
from langgraph.graph import MessagesState
from langgraph.graph import END

model: ChatGoogleGenerativeAI = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class State(MessagesState):
    summary: str

# Define the logic to call the model
def call_model(state: State) -> State:

    # Get summary if it exsits
    summary = state.get("summary", "")

    # If there is summary, then we add it
    if summary:
        # Add summary to system message
        system_message = f"Summary of conversation earlier: {summary}"

        # Append summary to newer messages
        messages = [SystemMessage(content=system_message)] + state["messages"]

    else:
        messages = state["messages"]

    response = model.invoke(messages)
    return {"messages": response}

def summarize_conversation(state: State) -> State:
    print(f"Messages before summarizing: {len(state['messages'])}")

    # First, we get any existing summary
    summary = state.get("summary", "")
    print(f"Existing Summary: {summary}")

    # Create our summarization prompt
    if summary:
        
        # A summary already exist
        summary_message = (
            f"This is summary of conversation to the date: {summary}\n\n"
            "Extend the summary by taking into account the new messages above."
        )
    
    else:
        summary_message = "Create a summary of the conversation above."

    # Add prompt to our history
    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = model.invoke(messages)

    # Summarizing Logic
    print(f"New Summary: {response.content}")

    # Delete all but the 2 most recent messages
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]

    print(f"Messages After Truncation: {len(delete_messages)}")
    return {"summary": response.content, "messages": delete_messages}

# Determine whether to end or summarize the conversation
def should_continue(state: State) -> State:
    """"Return the next node to execute"""

    messages = state["messages"]
    print(f"Message count: {len(messages)}")

    # If there are more than six messages, then we summarize the conversation
    if len(messages) > 6:
        return "summarize_conversation"
    
    # Otherwise we can just END
    return END

from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph

# Redfine workflow
workflow = StateGraph(State)
workflow.add_node("conversation", call_model)
workflow.add_node(summarize_conversation)

workflow.add_edge(START, "conversation")
workflow.add_conditional_edges("conversation", should_continue)
workflow.add_edge("summarize_conversation", END)

# Compile the workflow with POSTgreSQL checkpointer
graph = workflow.compile(checkpointer=checkpointer)

# Configuration for Thread
config = {"configurable": {"thread_id": "1"}}

# Start a conversation
input_message = HumanMessage(content="hi! I am Moiz")
output = graph.invoke({"message": [input_message]}, config)
for m in output['messages'][-1:]:
    m.pretty_print()

# Check the persisted state
graph_state = graph.get_state(config)
graph_state

# Configuration for Thread
config = {"configurable": {"thread_id": "2"}}

# Start a conversation
input_message = HumanMessage(content="What are nodes in LangGraph")
output = graph.invoke({"message": [input_message]}, config)
for m in output['messages'][-1:]:
    m.pretty_print()

# Check the persisted state
graph_state = graph.get_state(config)
graph_state

pool.close()