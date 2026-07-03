# Agno

## What it is
Agno is a lightweight Python framework for building multi-modal agents with memory, knowledge, and tools. As the successor to **Phidata v2**, it emphasizes high performance and scalability. By July 2026, Agno has integrated full support for **FastMCP 3.0** and is optimized for the latest frontier models including **Gemma 3**, **Claude 4.8**, and **GPT-5.5**.

## What problem it solves
Agno simplifies the transition from a single agent prototype to a production-ready system. It provides a stateless, session-scoped runtime that can be served as a FastAPI backend, making it easy to deploy agents as horizontally scalable services while maintaining complex agent state in external databases.

## Where it fits in the stack
[Layer 6: Agents & Orchestration](../../knowledge_base/ai_tooling_landscape.md#layer-6-agents-orchestration) — A performance-oriented framework for building and serving agentic software.

## Typical use cases
- **FastMCP Tool Servers**: Building and hosting tool-rich servers using the **FastMCP 3.0** protocol for seamless discovery by other agents.
- **High-performance multi-modal agents**: Native support for Vision, Audio, and Text models from providers like Anthropic and OpenAI.
- **Edge Intelligence**: Deploying lightweight agents using [Gemma 3](../ai_knowledge/local_llms.md) for local-first or privacy-preserving workflows.
- **Production-grade agents**: Serving agent logic via FastAPI for integration into web or mobile applications.

## Strengths
- **FastMCP 3.0 Integration**: Native support for the Model Context Protocol (MCP) 3.0 standard for tool and resource discovery.
- **Performance**: Optimized for low latency and high throughput, critical for the fast inference speeds of 2026 frontier models.
- **Stateless Runtime**: Designed to be horizontally scalable out of the box, delegating state management to robust backends.
- **Multi-modal**: Native support for various model modalities, allowing for seamless integration of multimodal reasoning.

## Limitations
- **New Rebrand**: As the successor to Phidata, some documentation and legacy links might still refer to the old name.
- **Python Only**: Currently focused exclusively on the Python ecosystem.

## When to use it
- When building agents that need to scale horizontally in production.
- For projects requiring strong multi-modal support across different model families.
- If you require native **FastMCP 3.0** support for building tool-enabled services.

## When not to use it
- If you require a TypeScript-native framework (consider [Bee Agent Framework](bee-agent-framework.md)).
- For very simple, synchronous scripts where the overhead of a framework isn't justified.

## Getting started
### Installation
```bash
pip install agno openai duckduckgo-search
```

### Basic Usage (with Gemma 3)
```python
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.duckduckgo import DuckDuckGo

# 1. Create the agent with a tool and Gemma 3 via Ollama
agent = Agent(
    model=Ollama(id="gemma3:27b"),
    tools=[DuckDuckGo()],
    description="You are a helpful AI assistant running locally.",
    markdown=True
)

# 2. Run a query
agent.print_response("What is the latest status of the MCP 3.0 Task Protocol?")
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
### Creating a FastMCP Server with Agno
```python
from agno.agent import Agent
from agno.mcp.server import FastMCPServer

# Define an agent that will act as a tool provider
tool_agent = Agent(
    name="LogAnalyzer",
    instructions="Analyze logs for security patterns",
    tools=[...]
)

# Host the agent via FastMCP 3.0
app = FastMCPServer(agents=[tool_agent])

if __name__ == "__main__":
    app.run(port=8000)
```

## Related tools / concepts
- [Phidata](phidata.md) (Predecessor)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Local LLMs](../ai_knowledge/local_llms.md) (Gemma 3)
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
- Last reviewed: 2026-07-21
- Confidence: high
