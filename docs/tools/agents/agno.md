# Agno

## What it is
Agno is a lightweight Python framework for building multi-modal agents with memory, knowledge, and tools. It is the successor to **Phidata v2** and focuses on high performance, scalability, and ease of use.

## What problem it solves
Agno simplifies the transition from a single agent prototype to a production-ready system. It provides a stateless, session-scoped runtime that can be served as a FastAPI backend, making it easy to deploy agents as services.

## Where it fits in the stack
[Framework / Agent / Runtime] - A performance-oriented framework for building and serving agentic software.

## Typical use cases
- High-performance multi-modal agents (Vision, Audio, Text)
- Multi-agent teams coordinating via a shared control plane
- Production-grade agents served via FastAPI

## Strengths
- **Performance**: Optimized for low latency and high throughput.
- **Stateless Runtime**: Designed to be horizontally scalable out of the box.
- **Multi-modal**: Native support for various model modalities.
- **AgentOS**: Integration with a control plane for monitoring and managing agents in production.

## Limitations
- **New Rebrand**: As the successor to Phidata, some documentation and legacy links might still refer to the old name.
- **Python Only**: Currently focused on the Python ecosystem.

## When to use it
- When building agents that need to scale horizontally in production.
- For projects requiring strong multi-modal support.
- If you liked Phidata but need more production features.

## When not to use it
- If you require a TypeScript-native framework (consider Bee Agent Framework).

## Getting started
### Installation
```bash
pip install agno openai duckduckgo-search
```

### Working Example
```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGo

# 1. Create the agent with a tool
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGo()],
    description="You are a helpful AI assistant that can search the web.",
    markdown=True
)

# 2. Run a query
agent.print_response("Tell me about the Agno framework and its search capabilities.")
```

## Licensing and cost
- **Open Source**: Yes (MIT License)
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [Phidata](phidata.md) (Predecessor)
- [Agent Protocols](../../knowledge_base/agent_protocols.md)
- [Agent Protocols (MCP)](../../knowledge_base/agent_protocols.md)
- [FastAPI](https://fastapi.tiangolo.com/)

## Sources / References
- [Official Website](https://www.agno.com/)
- [GitHub Repository](https://github.com/agno-agi/agno)
- [Documentation](https://docs.agno.com/)

## Contribution Metadata
- Last reviewed: 2026-02-28
- Confidence: high
