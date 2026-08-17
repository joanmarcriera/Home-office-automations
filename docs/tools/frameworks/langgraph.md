# LangGraph

## What it is
LangGraph is an open-source framework built on top of LangChain for creating stateful, multi-actor, cyclic agent applications. In early January 2027, LangGraph v0.3+ is a core enterprise engine for constructing complex, resilient LLM graph workflows that leverage frontier reasoning models like **Claude 5.1**, **GPT-5.5 / GPT-5.6**, **Gemini 4.0 Pro**, and **Llama 4 Maverick**.

## What problem it solves
While standard DAG (Directed Acyclic Graph) pipelines excel at linear tasks, autonomous AI agents require loops ("reason-act-observe" cycles) to reflect, retry tools, and recover from execution errors. LangGraph provides fine-grained control over cyclic execution while maintaining full state persistence, human-in-the-loop breakpoints, and "time travel" state editing across long-running sessions.

## Where it fits in the stack
**Framework / Multi-Agent Orchestration**. It sits between foundation models and tool environments, managing execution state, memory checkpointers, and conditional edge transitions. It serves as a foundation for implementing [Multi-Agent KnowledgeOps](../../architecture/multi_agent_knowledgeops.md) design architectures.

## Typical use cases
- **Cyclic Reflection & Self-Correction**: Building agents that generate code or copy, evaluate outputs against test suites, and loop back to fix errors.
- **Human-in-the-Loop Verification**: Pausing state graph execution before high-risk actions (e.g., executing database mutations) to await human review.
- **Complex Hierarchical RAG**: Iterative retrieval, re-ranking, and query expansion loops to ensure zero-hallucination document synthesis.
- **Multi-Agent Handoffs**: Routing execution state across specialized sub-graphs (e.g., Researcher -> Drafter -> Auditor).
- **FastMCP Protocol Orchestration**: Managing parallel tool calls across multiple **Model Context Protocol (FastMCP 3.1)** servers.

## Strengths
- **Native Cycles & Recursion Controls**: Engineered specifically for loops with configurable maximum recursion depths and error boundaries.
- **Built-In State Persistence & Time Travel**: Automatic state checkpointing allows developers to inspect, rewind, and replay past states.
- **Fine-Grained Graph Mechanics**: Explicit control over graph nodes, conditional edges, and state schemas.
- **Native FastMCP 3.1 Integration**: First-class support for discovering and calling FastMCP tools and resource endpoints.

## Limitations
- **Architectural Verbosity**: Constructing simple agents requires defining explicit state models, nodes, and edges, adding initial setup code.
- **Ecosystem Dependency**: Deeply integrated with LangChain primitives, requiring familiarity with LangChain core interfaces.
- **State Serialization Overhead**: Managing large state objects across many persistence checkpoints can increase memory consumption.

## When to use it
- When you require precise control over multi-agent workflows with loops, branching, and conditional edge transitions.
- When auditability, session persistence, and time-travel debugging are essential production requirements.
- When building human-in-the-loop workflows where execution must pause at specific breakpoints.

## When not to use it
- For basic linear chains or prompt completions where simple sequential functions are sufficient.
- If you prefer a conversational, message-passing multi-agent interface over a graph structure (use [AutoGen](autogen.md) or [CrewAI](crewai.md)).

## Getting started

### 1. Installation
Install LangGraph and its core dependencies:
```bash
pip install langgraph langchain_anthropic langchain_openai pydantic
```

### 2. Define State with Pydantic v2
Define a validated state schema using Pydantic v2 and create a basic graph:

```python
from typing import List, Annotated
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END

class AgentGraphState(BaseModel):
    messages: List[str] = Field(default_factory=list)
    next_node: str = Field(default="")

def reasoning_step(state: AgentGraphState) -> dict:
    return {"messages": state.messages + ["Reasoning completed."], "next_node": "tools"}

builder = StateGraph(AgentGraphState)
builder.add_node("reasoning", reasoning_step)
builder.add_edge(START, "reasoning")
builder.add_edge("reasoning", END)
graph = builder.compile()
```

## CLI examples

### Local Development Server
Launch the local LangGraph development and visualization server:
```bash
langgraph dev
```

### Deployment to LangGraph Cloud
Deploy the graph to a managed LangGraph Cloud instance:
```bash
langgraph deploy --project agent-production-v1
```

### LangGraph CLI Installation
Install the LangGraph CLI package:
```bash
pip install langgraph-cli
```

## API examples

### Persistent Checkpointing with FastMCP 3.1 & Pydantic v2
Compile a state graph with MemorySaver checkpointers for multi-turn session persistence:

```python
from typing import List
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

class ConversationState(BaseModel):
    messages: List[str] = Field(default_factory=list)
    user_id: str

def assistant_node(state: ConversationState) -> dict:
    updated_messages = state.messages + ["Assistant response generated via Claude 5.1."]
    return {"messages": updated_messages}

# Build graph structure
builder = StateGraph(ConversationState)
builder.add_node("assistant", assistant_node)
builder.add_edge(START, "assistant")
builder.add_edge("assistant", END)

# Compile graph with persistent memory checkpointer
memory = MemorySaver()
app = builder.compile(checkpointer=memory)

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "thread_session_2027_01"}}
    initial_input = ConversationState(messages=["Hello, initialize FastMCP session."], user_id="user_42")

    # Execute graph with state persistence
    result = app.invoke(initial_input.model_dump(), config)
    print("State Result:", result)
```

## Related tools / concepts
- [LangChain](../ai_knowledge/langchain.md) - Foundational framework for LLM applications.
- [AutoGen](autogen.md) - Conversational multi-agent orchestration framework.
- [CrewAI](crewai.md) - Role-based multi-agent system library.
- [Model Context Protocol](../automation_orchestration/mcp.md) - Standard protocol for tools and resources.
- [Multi-Agent KnowledgeOps](../../architecture/multi_agent_knowledgeops.md) - Architectural framework for agentic systems.
- [DSPy](dspy.md) - Programmatic prompt compilation engine.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) - Design patterns for multi-step AI agents.

## Sources / references
- [Official LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangGraph GitHub Repository](https://github.com/langchain-ai/langgraph)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
