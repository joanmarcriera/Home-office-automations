# LangGraph

## What it is
LangGraph is a library for building stateful, multi-actor applications with LLMs, built on top of LangChain. In June 2026, it is a critical framework for creating complex, cyclic agent workflows that leverage the reasoning capabilities of Claude 4.8 Opus and GPT-5.5.

## What problem it solves
While standard LangChain chains are great for linear workflows, they struggle with cyclic graphs often needed for autonomous agents (e.g., "reason-act-observe" loops). LangGraph provides the control needed for these loops while maintaining state across multiple steps, enabling persistence, human-in-the-loop patterns, and advanced error recovery.

## Where it fits in the stack
**Framework / Agent Orchestration**. It sits between the LLM and the tools, managing the execution logic, state, and persistence of the agentic application. It serves as the primary engine for [Multi-Agent KnowledgeOps](../../architecture/multi_agent_knowledgeops.md) implementations.

## Typical use cases
- **Multi-agent collaboration**: Orchestrating specialized agents (e.g., Researcher, Writer, Reviewer) with complex handoff logic.
- **Human-in-the-loop**: Applications requiring manual approval or state editing before proceeding with tool use.
- **Complex RAG**: Iterative retrieval and refinement loops for high-accuracy document processing.
- **Stateful Assistants**: Building long-running conversations that persist across sessions with full "time travel" capabilities.
- **MCP Orchestration**: Managing tool calls to multiple [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) servers.

## Strengths
- **Cycles and Recursion**: Built specifically to handle loops in agent logic, essential for reflection and retry patterns.
- **Persistence & Time Travel**: Built-in support for saving state (checkpointers), allowing for session resumption and auditing.
- **Granular Control**: Fine-grained control over the flow (nodes and edges), unlike "black-box" agent frameworks.
- **Human-in-the-loop**: Native primitives for interrupting execution for human intervention or approval.
- **Native MCP 3.0 Support**: Seamless integration with the Model Context Protocol for unified tool and resource access.

## Limitations
- **Learning Curve**: Requires understanding of graph theory concepts and the broader LangChain ecosystem.
- **Verbosity**: Implementing simple agents can feel more verbose compared to higher-level frameworks like [CrewAI](crewai.md).
- **Overhead**: Managing state and checkpointers adds architectural complexity to simple applications.

## When to use it
- When you need a highly customized agent workflow with specific loops and state transitions.
- When persistence and session management are core requirements.
- When you are already invested in the LangChain ecosystem and require advanced agentic patterns.

## When not to use it
- For simple, linear LLM chains where a basic pipeline is sufficient.
- If you prefer a more "out-of-the-box" multi-agent experience with less configuration.
- For low-latency micro-tasks where the state management overhead is unnecessary.

## Getting started

### 1. Installation
Install LangGraph and its dependencies:
```bash
pip install langgraph langchain_anthropic langchain_openai
```

### 2. Define State
Create a TypedDict to represent the state of your graph.

### 3. Build Graph
```python
from langgraph.graph import StateGraph, START, END

builder = StateGraph(State)
builder.add_node("chatbot", chatbot_node)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)
graph = builder.compile()
```

## CLI examples

### 1. Start Development Server
```bash
langgraph dev
```

### 2. Deploy to LangGraph Cloud
```bash
langgraph deploy --project my-agent-project
```

### 3. Install LangGraph CLI
```bash
pip install langgraph-cli
```

## API examples

### Persistence with Checkpointers
LangGraph enables session persistence across multiple invocations using checkpointers.

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# Setup persistent memory
memory = SqliteSaver.from_conn_string(":memory:")
graph = builder.compile(checkpointer=memory)

# Run with a thread_id
config = {"configurable": {"thread_id": "session_456"}}
graph.invoke({"messages": [("user", "Remember my name is Jules.")]}, config)
```

### Human-in-the-loop Breakpoints
Interrupt execution to allow for human review.

```python
# Compile with a breakpoint before the 'tools' node
graph = builder.compile(checkpointer=memory, interrupt_before=["tools"])

# Execution will pause here; resume by invoking with None
graph.invoke(input_data, config)
```

## Related tools / concepts
- [LangChain](../ai_knowledge/langchain.md) — The foundational framework.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standardized tool calling.
- [CrewAI](crewai.md) — Role-based multi-agent alternative.
- [AutoGen](autogen.md) — Microsoft's multi-agent framework.
- [DSPy](dspy.md) — Programmatic prompt optimization.
- [Haystack](haystack.md) — Modular LLM pipelines.
- [Smolagents](smolagents.md) — Minimalist agent library from Hugging Face.
- [Plandex](../development_ops/plandex.md) — AI coding engine.
- [LangSmith](../benchmarking/langsmith.md) — Observability and evaluation.

## Sources / References
- [Official Documentation](https://langchain-ai.github.io/langgraph/)
- [GitHub Repository](https://github.com/langchain-ai/langgraph)
- [LangGraph Persistence Guide](https://langchain-ai.github.io/langgraph/how-tos/persistence/)
- [LangGraph MCP Integration](https://langchain-ai.github.io/langgraph/how-tos/mcp/)

## Contribution Metadata
- Last reviewed: 2026-06-28
- Confidence: high
