# Phidata (Agno)

## What it is
Phidata is a Python-native framework for building AI assistants with memory, knowledge, and tools. As of early January 2027, Phidata has fully transitioned and rebranded into the **Agno** framework (v3.x). It serves as a primary enterprise bridge for transforming raw LLMs into stateful, autonomous agents, offering native integration with the [Model Context Protocol (MCP 3.1)](../automation_orchestration/mcp.md) and FastMCP 3.1.

## What problem it solves
Phidata (Agno) addresses the "statelessness" and non-deterministic behavior of standard LLMs by providing clean, object-oriented abstractions for session management and long-term memory. It simplifies the integration of [Vector Databases](../infrastructure/pinecone.md) and relational storage like PostgreSQL, ensuring that retrieval-augmented generation (RAG) is highly performant. By supporting native tool-calling and FastMCP 3.1, it reduces the boilerplate required to connect AI agents to complex software stacks.

## Where it fits in the stack
**Agent Orchestration Framework**. It sits between the model layer (e.g., [OpenAI](../ai_knowledge/openai.md), [Anthropic](../providers/anthropic.md)) and the infrastructure/database layer, coordinating how agents retrieve data, use tools, and persist state across sessions.

## Typical use cases
- **Enterprise Knowledge Assistants**: Building agents that query internal documentation stored in PDF, CSV, or SQL formats.
- **Autonomous Research Agents**: Utilizing tools like [Tavily](../providers/tavily.md) to browse the web, summarize findings, and generate reports.
- **Stateful Support Chatbots**: Maintaining user context across multiple sessions using persistent SQL-backed storage.
- **Developer Tooling Agents**: Automating software workflows by integrating with [GitHub](../development_ops/github-pages.md) and local development environments.

## Strengths
- **Pythonic Design**: Offers an intuitive, object-oriented API that feels natural to Python developers.
- **Native FastMCP 3.1 Support**: Seamlessly integrates with MCP servers using FastMCP for rapid tool discovery and execution.
- **Optimized for Gemma 4 & Qwen 3.6**: Includes specialized prompt templates and structural handling for [Gemma 4](../ai_knowledge/local_llms.md) and [Qwen 3.6](../ai_knowledge/local_llms.md) to maximize reasoning efficiency.
- **Robust Observability**: Standard integration with [AgentOps](../process_understanding/agentops.md) for execution graphs and [ClickHouse](../process_understanding/clickhouse.md) for high-volume session telemetry.
- **Persistence Flexibility**: Out-of-the-box support for PostgreSQL, SQLite, and MongoDB.

## Limitations
- **Ecosystem Transition**: Users must transition their legacy `phi` imports to the new `agno` SDK as Phidata v1 is deprecated.
- **Orchestration Overhead**: For simple, single-turn prompts, the framework's abstractions may introduce unnecessary latency.
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
pip install agno openai duckduckgo-search pydantic
```

### Hello-World Example
Initialize a basic research agent using GPT-5.6:

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGo

# Create the assistant
agent = Agent(
    model=OpenAIChat(id="gpt-5.6"),
    tools=[DuckDuckGo()],
    description="You are a research assistant.",
    show_tool_calls=True,
    markdown=True,
)

# Run a query
agent.print_response("Summarize the impact of FastMCP 3.1 on AI agent interoperability.", stream=True)
```

## CLI examples
```bash
# Initialize a new Agno project structure
agno init

# Start Agno-managed resources (e.g., PostgreSQL for memory)
agno start

# Check the status of active agents and storage backends
agno status

# Stop all local Agno services
agno stop
```

## API examples

### Structured Agent Outputs (Python & Pydantic v2)
Agno offers native structured response validation. This example defines a strict schema using Pydantic v2 to validate a research agent's structured report on AI tools:

```python
from typing import List
from pydantic import BaseModel, Field
from agno.agent import Agent
from agno.models.openai import OpenAIChat

# Define the structured output schema
class ToolComparison(BaseModel):
    tool_name: str = Field(..., description="Name of the agentic tool.")
    primary_use_case: str = Field(..., description="Primary use case or application.")
    strengths: List[str] = Field(..., description="Key strengths of this tool.")
    limitations: List[str] = Field(..., description="Limitations or drawbacks.")
    confidence_rating: float = Field(..., description="Our confidence rating from 0.0 to 1.0.", ge=0.0, le=1.0)

class AIAnalysisReport(BaseModel):
    topic: str = Field(..., description="The main research topic.")
    summary: str = Field(..., description="High-level synthesis of findings.")
    comparisons: List[ToolComparison] = Field(..., description="List of comparative tools analyzed.")

# Initialize the Agent with a response model
agent = Agent(
    model=OpenAIChat(id="gpt-5.6"),
    response_model=AIAnalysisReport,
    description="You are an expert market analyst synthesizing tool directories.",
)

# Fetch the structured response
response = agent.run("Compare Phidata (Agno) vs Bee Agent Framework.")

# The response.content is guaranteed to be an instance of AIAnalysisReport
report: AIAnalysisReport = response.content
print(f"Report Topic: {report.topic}")
print(f"Summary: {report.summary}")
for comparison in report.comparisons:
    print(f"- {comparison.tool_name} (Confidence: {comparison.confidence_rating})")
```

## Related tools / concepts
- [Agno](agno.md) (The v2 evolution of Phidata)
- [LlamaIndex](../ai_knowledge/llamaindex.md) (Specialized in advanced data indexing for RAG)
- [LangChain](../ai_knowledge/langchain.md) (The industry-standard agent framework)
- [CrewAI](../frameworks/crewai.md) (Multi-agent workflow orchestration)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) (The standard for tool-LLM communication)

## Sources / references
- [Official Agno Website](https://www.agno.com/)
- [Agno GitHub Repository](https://github.com/agno-agi/agno)
- [Agno Documentation](https://docs.agno.com/)
- [MCP 3.1 Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
