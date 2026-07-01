# Messages Summarization, Short Term Local Memory with Threads/Checkpointers
### ChatBot Summarization

*Rather than just trimming or filtering messages, use LLMs to produce a running summary of the conversation*

*This allow us to retain a compressed representation of the full conversation, rather than just removing it with trimming or filtering*

*We;ll incorporate this summarization into a simple ChatBot*

*And we'll equip that ChatBot with memory, supporting long-running conversations without incurring high token cost/latency*

We'll use Messages state,
- In addition to the built-in messages key, we'll now include a custom key(summary)

```
from langgraph.graph import MessagesState

class State(MessagesState):
    summary: str
```

We'll define a node to call our LLM that incorporates a summary, if it exists into the prompt
```
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
```

We'll define a node to produce a summary
- here we'll use RemoveMessage to filter our state after we've produced the summary
```
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
```

We'll add a conditional edge to determine whether to produce a summary based on the conversation length
```
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
```

### Adding Memory
*state is transient to a single graph execution*
- This limits our ability to have multi-turn conversations with interruptions, so we can use persistence to address this.

**LangGraph** can use a checkpointer to automatically save the graph state after each step.
- This built-in persistence layer gives us memory, allowing langgraph to pick up from the last state update.
- one of the easiest to work with is MemorySave, an in-memory key-value store for graph state
- just need to compile the graph with a checkpointer and our graph has memory


```
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
```

