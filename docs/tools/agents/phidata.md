# Phidata

## What it is
Phidata is a Python-native framework for building AI assistants with memory, knowledge, and tools. As of July 2026, Phidata (and its evolved ecosystem, [Agno](agno.md)) serves as a primary bridge for transforming standard LLMs into functional, stateful agents. It enables developers to store session data in relational databases, perform Retrieval-Augmented Generation (RAG) across diverse data sources, and execute complex toolsets via the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md).

## What problem it solves
Phidata addresses the "statelessness" of raw LLMs by providing standardized abstractions for session management and long-term memory. It simplifies the integration of [Vector Databases](../infrastructure/pinecone.md) and traditional storage like PostgreSQL, ensuring that retrieval-augmented generation is performant. By supporting native tool-calling and the MCP 3.0 Task Protocol, it reduces the boilerplate required to connect AI agents to enterprise software stacks.

## Where it fits in the stack
**Agent Orchestration Framework**. It sits between the model layer (e.g., [OpenAI](../ai_knowledge/openai.md), [Anthropic](../providers/anthropic.md)) and the infrastructure layer, coordinating how agents retrieve data, use tools, and persist state.

## Typical use cases
- **Enterprise Knowledge Assistants**: Building agents that query internal documentation stored in PDF, CSV, or SQL formats.
- **Autonomous Research Agents**: Utilizing tools like [Tavily](../providers/tavily.md) to browse the web, summarize findings, and generate reports.
- **Stateful Support Chatbots**: Maintaining user context across multiple sessions using persistent SQL-backed storage.
- **Developer Tooling Agents**: Automating software workflows by integrating with [GitHub](../development_ops/github-pages.md) and local development environments.

## Strengths
- **Pythonic Design**: Offers a clean, object-oriented API that feels natural to Python developers.
- **Native MCP 3.0 Support**: Seamlessly integrates with MCP servers using FastMCP for rapid tool discovery and execution.
- **Optimized for Gemma 3**: Includes specialized prompts and handling for [Gemma 3](../ai_knowledge/local_llms.md) to maximize reasoning capabilities in open-weights environments.
- **Robust Observability**: Standard integration with [AgentOps](../process_understanding/agentops.md) for execution graphs and [ClickHouse](../process_understanding/clickhouse.md) for high-volume session telemetry.
- **Persistence Flexibility**: Out-of-the-box support for PostgreSQL, SQLite, and MongoDB.

## Limitations
- **Ecosystem Transition**: Users must navigate the rebranding and feature migration from Phidata v1 to the Agno ecosystem.
- **Orchestration Overhead**: For extremely simple, one-off scripts, the framework's abstractions may introduce unnecessary complexity.
- **Multi-Agent Scaling**: While capable, managing massive swarms of 50+ agents may require more manual tuning compared to specialized multi-agent kernels.

## When to use it
- When building production-ready agents that require persistent, database-backed memory.
- If you are leveraging the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) to connect agents to external tools.
- When working in a Python-centric environment and seeking a framework with minimal boilerplate for RAG.

## When not to use it
- For projects requiring non-Python implementations (e.g., pure TypeScript or Rust environments).
- If your agent requires low-level, custom message-passing protocols that bypass standard orchestration abstractions.
- When building extremely lightweight "hello world" scripts where raw API calls to [OpenAI](../ai_knowledge/openai.md) suffice.

## Getting started
### Installation
```bash
pip install phidata openai duckduckgo-search
```

### Hello-World Example
Initialize a basic research agent using GPT-5.5:

```python
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo

# Create the assistant
agent = Agent(
    model=OpenAIChat(id="gpt-5.5-preview"),
    tools=[DuckDuckGo()],
    description="You are a research assistant.",
    show_tool_calls=True,
    markdown=True,
)

# Run a query
agent.print_response("Summarize the impact of MCP 3.0 on AI agent interoperability.", stream=True)
```

## CLI examples
```bash
# Initialize a new Phidata project structure
phi init

# Start Phidata-managed resources (e.g., PostgreSQL for memory)
phi start

# Check the status of active agents and storage backends
phi status

# Stop all local Phidata services
phi stop
```

## API examples
Implementing an agent with persistent SQLite memory:

```python
from phi.agent import Agent
from phi.storage.agent.sqlite import SqlAgentStorage

# Define an agent with persistent storage
agent = Agent(
    storage=SqlAgentStorage(table_name="customer_support", db_file="agents.db"),
    add_history_to_messages=True,
    num_history_responses=3,
)

# The agent will remember the user ID across different script executions
agent.print_response("My user ID is 'AGENT-X'. Remember this for my next visit.")
```

## Related tools / concepts
- [Agno](agno.md) (The v2 evolution of Phidata)
- [LlamaIndex](../ai_knowledge/llamaindex.md) (Specialized in advanced data indexing for RAG)
- [LangChain](../ai_knowledge/langchain.md) (The industry-standard agent framework)
- [CrewAI](../frameworks/crewai.md) (Multi-agent workflow orchestration)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) (The standard for tool-LLM communication)

## Sources / references
- [Official Phidata Website](https://www.phidata.com/)
- [Phidata GitHub Repository](https://github.com/agno-agi/phidata)
- [Agno Documentation](https://docs.agno.com/)
- [MCP 3.0 Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
