# Agno

## What it is
Agno (v3.x+, early January 2027) is an ultra-fast, lightweight Python framework designed for building production-grade multi-modal agents with persistent memory, semantic knowledge, and customizable tools. As the official successor to **Phidata v2**, Agno is engineered specifically for microsecond-overhead performance and horizontal scaling. It features full native compatibility with the **Model Context Protocol (MCP) 3.1** and **FastMCP 3.1 Task Protocol** specifications, optimized for early 2027 frontier models including **Gemma 4**, **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, and **DeepSeek-V4**.

## What problem it solves
Transitioning complex agentic workflows from local prototyping to scalable, highly-concurrent production setups usually introduces massive state-synchronization and latency overhead. Agno solves this by decoupling agent intelligence from agent state, providing a stateless, highly concurrent, session-scoped execution runtime. It allows developers to deploy agents as horizontally-scalable FastAPI backends while delegating conversational and transactional states to robust, multi-tenant databases (PostgreSQL, MongoDB, DynamoDB).

## Where it fits in the stack
[Layer 6: Agents & Orchestration](../../knowledge_base/ai_tooling_landscape.md#layer-6-agents-orchestration) — A high-performance, stateless orchestrator built to power high-throughput agent fleets, particularly those implementing the **FastMCP 3.1** specification.

## Typical use cases
- **Stateless Agent Services**: Hosting agents inside high-throughput FastAPI web services with horizontal autoscaling.
- **FastMCP 3.1 Tool Servers**: Launching tool-discovery servers exposing local utilities to remote orchestrators.
- **Privacy-First Local Reasoning**: Deploying agents using local weights (e.g., [Gemma 4](../ai_knowledge/local_llms.md)) via Ollama for zero-egress workflows.
- **Multi-Modal Document Intake**: Building real-time audio and vision processing engines utilizing multimodal APIs.

## Strengths
- **FastMCP 3.1 Native Integration**: Comprehensive support for MCP 3.1 standards, allowing tool and resource definitions to be auto-discovered.
- **Minimal Latency Overhead**: Extremely lean core logic compared to heavier frameworks, ideal for low-latency voice and streaming agents.
- **Clean State Separation**: Native integration with PostgreSQL (via PGVector) and other enterprise databases for session storage.
- **Pydantic v2 Alignment**: Direct, zero-cost parsing of LLM structured outputs into strict Pydantic v2 schemas.

## Limitations
- **Ecosystem Renaming**: Due to the transition from Phidata, legacy integrations, tutorials, and third-party packages might still refer to old naming structures.
- **Python-Exclusive**: Strictly bound to Python, lacking official JS/TS runtimes.

## When to use it
- When building horizontally-scalable agents served via REST or WebSocket endpoints (e.g., [FastAPI](../frameworks/fastapi.md)).
- If you require native, low-latency **FastMCP 3.1** protocol support for registering or consuming agent tools.
- When working with strict structured JSON inputs/outputs requiring high-performance parsing.

## When not to use it
- If your team primarily works with Node.js/TypeScript (consider [Bee Agent Framework](bee-agent-framework.md)).
- For massive, complex graph-based agent topologies that are more natively modeled in [LangGraph](../frameworks/langgraph.md).

## Getting started
### Installation
```bash
pip install agno openai duckduckgo-search pydantic>=2.0
```

### Basic Usage (with Gemma 4)
```python
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.duckduckgo import DuckDuckGo

# Create the agent with a search tool and local Gemma 4
agent = Agent(
    model=Ollama(id="gemma4:31b"),
    tools=[DuckDuckGo()],
    description="You are a helpful, high-performance assistant running locally.",
    markdown=True
)

# Execute the agent
agent.print_response("What are the core differences between MCP 3.1 and MCP 3.0?")
```

## CLI examples
```bash
# Initialize a new Agno workspace or configuration file
agno init

# Spin up a local serving environment hosting registered agent endpoints
agno serve --port 8000

# Inspect and manage active agent sessions stored in the DB
agno sessions list
```

## API examples

### Designing a FastMCP 3.1 Server with Pydantic v2 State Validation
This example showcases how to build a production FastMCP 3.1 server using Agno, incorporating strict Pydantic v2 validation for structured inputs and outputs.

```python
from typing import List, Optional
from pydantic import BaseModel, Field, conlist
from agno.agent import Agent
from agno.mcp.server import FastMCPServer

# 1. Define strict Pydantic v2 schemas
class LogMetadata(BaseModel):
    session_id: str = Field(..., description="Unique UUID of the execution session")
    origin_ip: str = Field("127.0.0.1", pattern=r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    confidence_score: float = Field(..., ge=0.0, le=1.0)

class LogAnalysisReport(BaseModel):
    metadata: LogMetadata
    total_lines_analyzed: int = Field(..., gt=0)
    critical_vulnerabilities: List[str] = Field(default_factory=list)
    remediation_priority: str = Field("low", pattern="^(low|medium|high|critical)$")
    resolved: bool

# 2. Define the Agent that acts as a secure log analyzer
log_agent = Agent(
    name="SecureLogAnalyzer",
    instructions="Analyze system logs and produce structural JSON matching the LogAnalysisReport model.",
    response_model=LogAnalysisReport
)

# 3. Host the Agent within a FastMCP 3.1 compliant Server
app = FastMCPServer(
    name="SecurityAnalysisEngine",
    version="1.1.0",
    agents=[log_agent]
)

if __name__ == "__main__":
    # Runs the server exposing FastMCP 3.1 capabilities
    app.run(port=8080)
```

## Related tools / concepts
- [Phidata](phidata.md) (Predecessor)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Local LLMs](../ai_knowledge/local_llms.md) (Gemma 4)
- [LangGraph](../frameworks/langgraph.md)
- [FastAPI](../frameworks/fastapi.md)
- [PydanticAI](../frameworks/pydantic-ai.md)
- [CrewAI](../frameworks/crewai.md)
- [Claude Code](../development_ops/claude-code.md)

## Sources / references
- [Official Website](https://www.agno.com/)
- [GitHub Repository](https://github.com/agno-agi/agno)
- [Agno Documentation Portal](https://docs.agno.com/)
- [FastMCP Specification Specification](https://modelcontextprotocol.io/spec/fastmcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
