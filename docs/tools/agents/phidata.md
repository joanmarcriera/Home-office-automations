# Phidata

## What it is
Phidata is a Python-native framework for building AI assistants with memory, knowledge, and tools. It allows developers to transform standard LLMs into functional agents capable of storing session data in databases, performing RAG across local and remote files, and executing Python functions as tools. As of June 2026, it is widely used for creating stateful, knowledge-enabled agents that integrate with enterprise data stacks.

## What problem it solves
It solves the complexity of building production-grade agents by providing standardized abstractions for session management, vector database integration, and tool-calling. Phidata bridges the gap between raw LLM outputs and actionable software by managing the lifecycle of an agent's memory and ensuring that retrieval-augmented generation (RAG) is both performant and accurate.

## Where it fits in the stack
**Framework / Agent / Knowledge**. It sits as a development layer that orchestrates LLMs (OpenAI, Anthropic, etc.) with storage backends (PostgreSQL, Pinecone) and tool execution environments.

## Typical use cases
- **Knowledge-Based Assistants**: Building agents that can answer questions based on a massive internal library of PDFs, CSVs, or SQL databases.
- **Stateful Chatbots**: Creating customer support agents that remember user preferences and past interactions across multiple sessions.
- **Autonomous Researchers**: Agents that can search the web (via DuckDuckGo or Tavily), summarize findings, and write reports into a local filesystem.
- **Enterprise Tool-Callers**: Integrating AI into existing Python business logic to automate workflows like invoice processing or system monitoring.

## Strengths
- **Pythonic Design**: Extremely intuitive for Python developers, with minimal boilerplate required to start a new agent.
- **Persistent Memory**: Out-of-the-box support for database-backed memory (SQLite, PostgreSQL, MongoDB).
- **Flexible RAG**: Built-in connectors for various vector databases and file formats.
- **Model Agnostic**: Supports a wide range of models, including Claude 4.8 Opus and GPT-5.5.
- **Local Development**: Optimized for running and testing agents locally before cloud deployment.

## Limitations
- **Orchestration Complexity**: While great for single agents, very complex multi-agent graphs may require additional logic compared to specialized graph frameworks.
- **Ecosystem Size**: Smaller community compared to legacy frameworks like LangChain, though it is rapidly growing in the agent-centric era.

## When to use it
- When you want to build a single, highly-capable agent with RAG and long-term memory quickly.
- If you prefer a Python-native framework with a clean, object-oriented API.
- For projects where persistent session storage in a standard SQL/NoSQL database is a requirement.

## When not to use it
- For extremely complex multi-agent "swarms" that require low-level control over message passing (consider specialized multi-agent frameworks).
- If your primary focus is on a lightweight, no-config setup for a single-user agent.

## Getting started
### Installation
```bash
pip install phidata openai duckduckgo-search
```

### Basic Usage
Initialize an agent with tools and a model (e.g., GPT-5.5):

```python
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo

# 1. Create the assistant with a tool
agent = Agent(
    model=OpenAIChat(id="gpt-5.5-preview"),
    tools=[DuckDuckGo()],
    description="You are a research assistant that can search the web.",
    show_tool_calls=True,
    markdown=True,
)

# 2. Run a query
agent.print_response("What are the latest breakthroughs in fusion energy as of June 2026?", stream=True)
```

## CLI examples
```bash
# Initialize a new phidata project structure
phi init

# Start the agent environment (e.g., if using Docker-based resources)
phi start

# Stop all phidata-managed resources
phi stop

# Check the status of your running agents and storage
phi status
```

## API examples
Phidata excels at adding persistent memory to agents via SQL storage:

```python
from phi.agent import Agent
from phi.storage.agent.sqlite import SqlAgentStorage

# Create an agent that persists its conversation history
agent = Agent(
    storage=SqlAgentStorage(table_name="support_agent", db_file="memory.db"),
    add_history_to_messages=True,
    num_history_responses=5,
)

# This information will be remembered in future runs
agent.print_response("My user ID is 9876. Please remember this for my future queries.")
```

## Related tools / concepts
- [Agno](agno.md) (The evolved ecosystem for Phidata v2+)
- [LlamaIndex](../ai_knowledge/llamaindex.md) (Specialized in data indexing)
- [LangChain](../ai_knowledge/langchain.md)
- [CrewAI](../frameworks/crewai.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)

## Sources / references
- [Official Phidata Website](https://www.phidata.com/)
- [Phidata GitHub Repository](https://github.com/agno-agi/phidata)
- [Phidata Documentation](https://docs.phidata.com/)

## Contribution Metadata
- Last reviewed: 2026-06-15
- Confidence: high
