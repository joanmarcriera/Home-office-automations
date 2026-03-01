# Phidata

## What it is
Phidata is a framework for building AI assistants with memory, knowledge, and tools. It allows you to turn any LLM into an "Assistant" that can store data in a database, search across local files, and take actions using Python functions.

## What problem it solves
It bridges the gap between raw LLMs and functional agents by providing out-of-the-box support for RAG (Retrieval Augmented Generation), persistent session storage, and a structured way to define tools.

## Where it fits in the stack
[Framework / Agent / Knowledge] - A comprehensive framework for building robust, knowledge-enabled agents.

## Typical use cases
- Research agents that can search the web and read PDF files
- Coding assistants with access to a local codebase
- Customer support agents with persistent memory of past conversations

## Strengths
- **Simple API**: Very easy to get started with a few lines of code.
- **Database Integration**: Built-in support for PostgreSQL, Pinecone, and more for memory/knowledge.
- **Built-in Tools**: Includes many ready-to-use tools like DuckDuckGo, Shell, and SQL.

## Limitations
- **Ecosystem**: Smaller than LangChain or LlamaIndex.
- **Transition**: Recently underwent a major rebranding/v2 transition to [Agno](agno.md).

## When to use it
- When you need to build a single agent with RAG and memory capabilities quickly.
- If you want a Python-native, lightweight framework.

## When not to use it
- For extremely complex multi-agent graphs (consider LangGraph).

## Getting started
### Installation
```bash
pip install phidata openai duckduckgo-search
```

### Working Example
```python
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo

# 1. Create the assistant with a tool
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGo()],
    description="You are a helpful assistant that can search the web.",
    show_tool_calls=True,
    markdown=True,
)

# 2. Run a query
agent.print_response("What is the latest news about AI agents?", stream=True)
```

## Licensing and cost
- **Open Source**: Yes (MIT License)
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [Agno](agno.md) (Successor to Phidata v2)
- [LlamaIndex](../ai_knowledge/llamaindex.md)
- [Agent Protocols](../../knowledge_base/agent_protocols.md)
- [Agent Protocols (MCP)](../../knowledge_base/agent_protocols.md)

## Sources / References
- [Official Website](https://www.phidata.com/)
- [GitHub Repository](https://github.com/phidata-hq/phidata)

## Contribution Metadata
- Last reviewed: 2026-03-01
- Confidence: high
