# LangGraph

## What it is
LangGraph is a library for building stateful, multi-actor applications with LLMs, built on top of LangChain. It allows you to create complex agent workflows using a graph-based approach where nodes represent actions and edges represent the flow of control.

## What problem it solves
While standard LangChain chains are great for linear workflows, they struggle with cyclic graphs often needed for autonomous agents (e.g., "reason-act-observe" loops). LangGraph provides the control needed for these loops while maintaining state across multiple steps.

## Where it fits in the stack
[Framework / Agent / Orchestration] - It sits between the LLM and the tools, managing the execution logic of the agent.

## Typical use cases
- Multi-agent collaboration (e.g., a researcher agent and a writer agent)
- Agents with human-in-the-loop requirements
- Complex RAG pipelines that require iterative refinement

## Strengths
- **Cycles and Recursion**: Built specifically to handle loops in agent logic, essential for autonomous agents that need to reflect and retry.
- **Persistence & Time Travel**: Built-in support for saving state (checkpointers), allowing for session resumption and "time travel" to inspect or modify past states.
- **Granular Control**: Fine-grained control over the flow of the agent (nodes and edges), unlike more "black-box" agent frameworks.
- **Human-in-the-loop**: Native primitives for interrupting execution for human approval, editing state, or manual intervention.

## Advanced Technical Patterns

### 1. Persistence and Checkpointers
LangGraph uses checkpointers to save the state of the thread after every node execution. This enables session persistence and error recovery.

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# Use a SQLite database for persistent memory
memory = SqliteSaver.from_conn_string(":memory:")

# Compile the graph with checkpointer
graph = graph_builder.compile(checkpointer=memory)

# Run with a thread_id to maintain state across calls
config = {"configurable": {"thread_id": "user_session_123"}}
graph.invoke({"messages": [("user", "My name is Jules.")]}, config)

# Later, the agent will remember the name
response = graph.invoke({"messages": [("user", "What is my name?")]}, config)
```

### 2. Multi-Agent Collaboration (Handoffs)
You can define nodes that represent different specialized agents and use edges to route between them based on task requirements.

```python
def call_researcher(state):
    # Logic for researcher agent
    return {"messages": [("assistant", "I have found the data...")]}

def call_writer(state):
    # Logic for writer agent
    return {"messages": [("assistant", "The report is ready.")]}

builder = StateGraph(State)
builder.add_node("researcher", call_researcher)
builder.add_node("writer", call_writer)

# Logic to transition from research to writing
builder.add_edge("researcher", "writer")
```

### 3. Human-in-the-Loop (Approval Pattern)
LangGraph allows you to set "breakpoints" where the execution pauses until a human provides input or approval.

```python
# Compile with a breakpoint before the 'tools' node
graph = builder.compile(checkpointer=memory, interrupt_before=["tools"])

# The graph will stop execution before calling a tool
# You can then inspect the state and choose to proceed or modify
graph.invoke(input_data, config)

# After human review, resume execution:
graph.invoke(None, config)
```

## Limitations
- **Steep Learning Curve**: Requires understanding of graph theory concepts and LangChain's ecosystem.
- **Verbose**: Implementing simple agents can feel more verbose compared to higher-level frameworks.

## When to use it
- When you need a highly customized agent workflow with specific loops and state transitions.
- When you are already invested in the LangChain ecosystem.

## When not to use it
- For simple, linear LLM chains.
- If you prefer a more "magic" out-of-the-box multi-agent experience (like CrewAI).

## CLI examples
```bash
# Install the LangGraph CLI
pip install langgraph-cli

# Start the LangGraph development server
langgraph dev

# Deploy a graph to LangGraph Cloud (requires configuration)
langgraph deploy
```

## Getting started
### Installation
```bash
pip install langgraph langchain_openai langchain-community duckduckgo-search
```

### Working Example
```python
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun

# 1. Define the state
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 2. Initialize tools and LLM
tools = [DuckDuckGoSearchRun()]
tool_node = ToolNode(tools)
llm = ChatOpenAI(model="gpt-4o").bind_tools(tools)

# 3. Define the node logic
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

# 4. Build the graph
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

# Conditional edges for tool calling
def route_tools(state: State):
    if state["messages"][-1].tool_calls:
        return "tools"
    return END

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", route_tools)
graph_builder.add_edge("tools", "chatbot")

graph = graph_builder.compile()

# 5. Run a query
for event in graph.stream({"messages": [("user", "Search for the current price of Bitcoin.")]}):
    for value in event.values():
        if "messages" in value:
            print(value["messages"][-1].content)
```

## Licensing and cost
- **Open Source**: Yes (MIT License)
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [LangChain](../ai_knowledge/langchain.md)
- [Agent Protocols (MCP)](../../knowledge_base/agent_protocols.md)
- [CrewAI](../frameworks/crewai.md)

## Sources / References
- [Official Documentation](https://langchain-ai.github.io/langgraph/)
- [GitHub Repository](https://github.com/langchain-ai/langgraph)

## Contribution Metadata
- Last reviewed: 2026-05-17
- Confidence: high
