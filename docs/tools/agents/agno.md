# Agno

## What it is
Agno is a lightweight Python framework for building multi-modal agents with memory, knowledge, and tools. It is the successor to **Phidata v2** and focuses on high performance, scalability, and ease of use. In June 2026, it is widely used for serving agents optimized for **Claude 4.8 Opus** and **GPT-5.5** via FastAPI backends.

## What problem it solves
Agno simplifies the transition from a single agent prototype to a production-ready system. It provides a stateless, session-scoped runtime that can be served as a FastAPI backend, making it easy to deploy agents as horizontally scalable services while maintaining complex agent state in external databases.

## Where it fits in the stack
[Layer 6: Agents & Orchestration](../../knowledge_base/ai_tooling_landscape.md#layer-6-agents-orchestration) — A performance-oriented framework for building and serving agentic software.

## Typical use cases
- **High-performance multi-modal agents**: Native support for Vision, Audio, and Text models from providers like Anthropic and OpenAI.
- **Multi-agent teams**: Coordinating specialized agents via a shared control plane or orchestrator.
- **Production-grade agents**: Serving agent logic via FastAPI for integration into web or mobile applications.

## Strengths
- **Performance**: Optimized for low latency and high throughput, critical for the fast inference speeds of 2026 frontier models.
- **Stateless Runtime**: Designed to be horizontally scalable out of the box, delegating state management to robust backends.
- **Multi-modal**: Native support for various model modalities, allowing for seamless integration of multimodal reasoning.
- **AgentOS Integration**: Works with a control plane for monitoring, logging, and managing agents in production environments.

## Limitations
- **New Rebrand**: As the successor to Phidata, some documentation and legacy links might still refer to the old name.
- **Python Only**: Currently focused exclusively on the Python ecosystem.

## When to use it
- When building agents that need to scale horizontally in production.
- For projects requiring strong multi-modal support across different model families.
- If you require a performance-oriented alternative to heavier orchestration frameworks.

## When not to use it
- If you require a TypeScript-native framework (consider Bee Agent Framework).
- For very simple, synchronous scripts where the overhead of a framework isn't justified.

## Getting started
### Installation
```bash
pip install agno openai duckduckgo-search
```

### Basic Usage
```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGo

# 1. Create the agent with a tool
agent = Agent(
    model=OpenAIChat(id="gpt-5.5"),
    tools=[DuckDuckGo()],
    description="You are a helpful AI assistant that can search the web.",
    markdown=True
)

# 2. Run a query
agent.print_response("Tell me about the Agno framework and its search capabilities.")
```

## CLI examples
```bash
# Initialize an Agno project
agno init

# Start the Agno serving environment (FastAPI based)
agno serve

# Manage agent sessions via the CLI
agno sessions list
```

## API examples
```python
from agno.agent import Agent
from agno.models.anthropic import Anthropic

# Create an agent with session-aware memory and Claude 4.8
agent = Agent(
    model=Anthropic(id="claude-4-8-opus-20260528"),
    description="You are a high-fidelity reasoning assistant.",
    add_history_to_messages=True,
    num_history_responses=3,
)

# Execute and get Python response object
response = agent.run("Analyze the following system logs for anomalies...")
print(response.content)
```

## Related tools / concepts
- [Phidata](phidata.md) (Predecessor)
- [Agent Protocols (MCP)](../../knowledge_base/agent_protocols.md)
- [LangGraph](../frameworks/langgraph.md)
- [FastAPI](../frameworks/fastapi.md)
- [PydanticAI](../frameworks/pydantic-ai.md)
- [CrewAI](../frameworks/crewai.md)
- [Claude Code](../development_ops/claude-code.md)

## Sources / references
- [Official Website](https://www.agno.com/)
- [GitHub Repository](https://github.com/agno-agi/agno)
- [Documentation](https://docs.agno.com/)

## Contribution Metadata
- Last reviewed: 2026-06-15
- Confidence: high
