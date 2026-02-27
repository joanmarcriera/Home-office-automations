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
- **Cycles and Recursion**: Built specifically to handle loops in agent logic.
- **Persistence**: Built-in support for saving and loading the state of the graph.
- **Granular Control**: Fine-grained control over the flow of the agent, unlike more "black-box" agent frameworks.

## Limitations
- **Steep Learning Curve**: Requires understanding of graph theory concepts and LangChain's ecosystem.
- **Verbose**: Implementing simple agents can feel more verbose compared to higher-level frameworks.

## When to use it
- When you need a highly customized agent workflow with specific loops and state transitions.
- When you are already invested in the LangChain ecosystem.

## When not to use it
- For simple, linear LLM chains.
- If you prefer a more "magic" out-of-the-box multi-agent experience (like CrewAI).

## Getting started
### Installation
```bash
pip install langgraph langchain_openai
```

### Working Example
```python
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)
llm = ChatOpenAI(model="gpt-4o")

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

# Run the agent
for event in graph.stream({"messages": [("user", "What is LangGraph?")]}):
    for value in event.values():
        print(value["messages"][-1].content)
```

## Licensing and cost
- **Open Source**: Yes (MIT License)
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [LangChain](../ai_knowledge/langchain.md)
- [Agent Protocols](../../knowledge_base/agent_protocols.md)
- [CrewAI](../frameworks/crewai.md)

## Sources / References
- [Official Documentation](https://langchain-ai.github.io/langgraph/)
- [GitHub Repository](https://github.com/langchain-ai/langgraph)

## Contribution Metadata
- Last reviewed: 2026-02-27
- Confidence: high
