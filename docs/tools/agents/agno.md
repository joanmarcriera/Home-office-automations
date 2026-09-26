# Agno

## What it is
Agno (v3.x+, early January 2027) is an ultra-fast, lightweight Python framework designed for building production-grade multi-modal agents with persistent memory, semantic knowledge, and customizable tools. As the official successor to **Phidata v2**, Agno is engineered specifically for microsecond-overhead performance and horizontal scaling. It features full native compatibility with the **Model Context Protocol (MCP 3.1)** and **FastMCP 3.1 Task Protocol** specifications, optimized for early 2027 frontier models including **Gemma 4**, **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, and **DeepSeek-V4**.

Agno decouples the agent reasoning core from session state management, enabling developers to build stateless, event-driven agent architectures served over FastAPI and scaled horizontally across Kubernetes clusters.

```mermaid
sequenceDiagram
    autonumber
    actor Client as API Client / Web Frontend
    participant FastServer as Agno FastAPI Gateway
    participant AgentCore as Agno Agent Engine
    participant VectorDB as PGVector / Knowledge Store
    participant FastMCP as Remote FastMCP 3.1 Server
    participant Model as LLM Endpoint (Gemma 4 / GPT-5.6)

    Client->>FastServer: POST /agents/security-analyst/run (Session ID + Prompt)
    FastServer->>AgentCore: Load Agent Config & Context
    AgentCore->>VectorDB: Query Session State & Vector Context
    VectorDB-->>AgentCore: Return Vector Embeddings & Chat History
    AgentCore->>FastMCP: Discover Available MCP 3.1 Tools
    FastMCP-->>AgentCore: Tool Schema Specifications
    AgentCore->>Model: Execute Inference Request (Prompt + Context + Tools)
    Model-->>AgentCore: Return Response / Structured Tool Calls
    AgentCore->>FastMCP: Dispatch Tool Execution (if required)
    FastMCP-->>AgentCore: Return Execution Results
    AgentCore->>VectorDB: Persist Updated Session State
    AgentCore-->>FastServer: Format Pydantic v2 Structured Output
    FastServer-->>Client: Stream Response / Return JSON Payload
```

## What problem it solves
Transitioning complex agentic workflows from local prototyping to scalable, highly-concurrent production setups usually introduces massive state-synchronization and latency overhead. Frameworks that couple session memory directly into single-process runtimes fail under peak API loads and fail to support horizontal autoscaling.

Agno solves this by decoupling agent intelligence from agent state, providing a stateless, highly concurrent, session-scoped execution runtime:
- **High Latency Overhead**: Replaces heavy runtime abstractions with lean Python primitives, achieving sub-millisecond core engine dispatch latency.
- **State Coupling**: Delegates session memory and semantic vectors to multi-tenant databases (PostgreSQL/PGVector, MongoDB, DynamoDB), making agent workers completely stateless.
- **Protocol Incompatibility**: Implements native **FastMCP 3.1** protocol support, allowing Agno agents to both host tool servers and consume remote MCP tool registries seamlessly.

## Where it fits in the stack
[Layer 6: Agents & Orchestration](../../knowledge_base/ai_tooling_landscape.md#layer-6-agents-orchestration) — A high-performance, stateless orchestrator built to power high-throughput agent fleets, particularly those implementing the **FastMCP 3.1** specification.

```
+-----------------------------------------------------------------------+
|                        API Gateway / Ingress                          |
|                     (FastAPI / NGINX / Envoy)                         |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                         Agno Execution Engine                         |
|           - Stateless Agent Workers & Session Dispatcher              |
|           - Pydantic v2 Schema Validation Engine                      |
|           - FastMCP 3.1 Tool Discovery Router                         |
+-----------------------------------------------------------------------+
                |                                      |
                v                                      v
+-------------------------------+      +--------------------------------+
|     State & Memory Layer      |      |   FastMCP 3.1 Tool Ecosystem   |
| (PostgreSQL / PGVector / Redis)|      | (Local Tools / Remote MCP Hub) |
+-------------------------------+      +--------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                    Frontier Intelligence Engines                      |
|         (Gemma 4 / Claude 5.6 / GPT-5.6 / Gemini 4.0 Ultra)           |
+-----------------------------------------------------------------------+
```

## Typical use cases
- **Stateless Agent Microservices**: Hosting agents inside high-throughput FastAPI web services with horizontal container autoscaling.
- **FastMCP 3.1 Tool Servers**: Launching tool-discovery servers exposing local enterprise databases and internal APIs to remote orchestrators.
- **Privacy-First Local Reasoning**: Deploying agents using open weights (e.g., [Gemma 4](../ai_knowledge/local_llms.md)) via Ollama or vLLM for zero-egress enterprise workflows.
- **Multi-Modal Document Processing Engines**: Building real-time audio, vision, and document analysis pipelines powered by multi-modal LLM APIs.

## Strengths
- **FastMCP 3.1 Native Integration**: Comprehensive support for MCP 3.1 standards, allowing tool and resource definitions to be auto-discovered across networks.
- **Minimal Latency Overhead**: Extremely lean core logic compared to heavier frameworks, ideal for low-latency voice, streaming, and real-time agent services.
- **Clean State Separation**: Native integration with PostgreSQL (via PGVector), Redis, and cloud-native databases for session state storage.
- **Pydantic v2 Alignment**: Direct, zero-cost parsing of LLM structured outputs into strict Pydantic v2 schemas.

## Limitations
- **Ecosystem Renaming**: Due to the transition from Phidata v2 to Agno, legacy integrations, community tutorials, and third-party packages may still reference old naming structures.
- **Python-Exclusive Ecosystem**: Strictly bound to Python 3.10+, lacking official JavaScript/TypeScript runtimes.
- **Graph Complexity**: For highly complex, cyclic, directed graph agent topologies, specialized graph frameworks like LangGraph may offer more explicit state transition diagrams.

## When to use it
- When building horizontally-scalable agents served via REST or WebSocket endpoints (e.g., [FastAPI](../frameworks/fastapi.md)).
- If you require native, low-latency **FastMCP 3.1** protocol support for registering or consuming agent tools.
- When working with strict structured JSON inputs/outputs requiring high-performance parsing with Pydantic v2.

## When not to use it
- If your development team works exclusively in Node.js/TypeScript (consider [Bee Agent Framework](bee-agent-framework.md)).
- For complex graph-based agent topologies requiring state machine branching and manual breakpoint debugging (consider [LangGraph](../frameworks/langgraph.md)).

## Getting started

### Installation
Install Agno alongside required model providers and vector dependencies:

```bash
pip install agno openai duckduckgo-search pydantic>=2.0 pgvector
```

### Basic Usage (Local Gemma 4 Agent)
Create and run a local agent equipped with search capabilities:

```python
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.duckduckgo import DuckDuckGo

# Initialize agent with local Gemma 4 weights
agent = Agent(
    model=Ollama(id="gemma4:31b"),
    tools=[DuckDuckGo()],
    description="High-performance local agent executing over Agno runtime.",
    markdown=True
)

# Execute query
agent.print_response("What are the key performance enhancements in FastMCP 3.1?")
```

## CLI examples

### 1. Initializing an Agno Workspace
Create a standardized Agno project directory with predefined configuration files and database connectors:

```bash
agno init --project-name security-agent-fleet --template fastapi
```

### 2. Serving Agno Agents via Built-in CLI
Launch a multi-worker production serving instance hosting registered agent endpoints:

```bash
agno serve --port 8000 --workers 4 --env production
```

### 3. Inspecting Active Sessions and Memory Store
Query active user session records and inspect stored conversation state in PostgreSQL:

```bash
agno sessions list --db-url "postgresql://user:pass@localhost:5432/agno_db" --limit 10
```

## API examples

### Python (FastMCP 3.1 Server with Pydantic v2 Schema Validation)
This example showcases how to build a production FastMCP 3.1 server using Agno, incorporating strict Pydantic v2 validation for structured inputs and outputs.

```python
import sys
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ValidationError
from agno.agent import Agent
from agno.mcp.server import FastMCPServer

# 1. Define strict Pydantic v2 input and output schemas
class AuditTarget(BaseModel):
    hostname: str = Field(..., description="Target server FQDN or IP address")
    environment: str = Field("production", pattern="^(development|staging|production)$")
    scan_depth: int = Field(2, ge=1, le=5, description="Vulnerability scan recursion level")

class LogMetadata(BaseModel):
    session_id: str = Field(..., description="Unique UUID of the execution session")
    origin_ip: str = Field("127.0.0.1", description="Source IP address")
    confidence_score: float = Field(..., ge=0.0, le=1.0)

class LogAnalysisReport(BaseModel):
    metadata: LogMetadata
    target: AuditTarget
    total_lines_analyzed: int = Field(..., gt=0)
    critical_vulnerabilities: List[str] = Field(default_factory=list)
    remediation_priority: str = Field("low", pattern="^(low|medium|high|critical)$")
    resolved: bool

# 2. Instantiate the Agno Agent with structured response modeling
log_agent = Agent(
    name="SecureLogAnalyzer",
    instructions=(
        "Analyze system logs and produce structural JSON matching "
        "the LogAnalysisReport model under strict Pydantic v2 rules."
    ),
    response_model=LogAnalysisReport
)

# 3. Host the Agent within a FastMCP 3.1 compliant Server
app = FastMCPServer(
    name="SecurityAnalysisEngine",
    version="3.1.0",
    agents=[log_agent]
)

def validate_and_process_report(raw_json: Dict[str, Any]) -> LogAnalysisReport:
    """Utility function to demonstrate strict Pydantic v2 validation."""
    report = LogAnalysisReport.model_validate(raw_json)
    return report

if __name__ == "__main__":
    # Local validation demonstration
    sample_report_data = {
        "metadata": {
            "session_id": "sess_agno_9921",
            "origin_ip": "192.168.1.100",
            "confidence_score": 0.96
        },
        "target": {
            "hostname": "sec-gateway-01.internal",
            "environment": "production",
            "scan_depth": 3
        },
        "total_lines_analyzed": 45000,
        "critical_vulnerabilities": ["CVE-2027-1042: FastMCP Buffer Underflow"],
        "remediation_priority": "high",
        "resolved": False
    }

    validated_result = validate_and_process_report(sample_report_data)
    print("--- Agno Log Report Validated ---")
    print(f"Session ID: {validated_result.metadata.session_id}")
    print(f"Target Host: {validated_result.target.hostname}")
    print(f"Vulnerabilities: {validated_result.critical_vulnerabilities}")

    # Launch server when specified
    if "--serve" in sys.argv:
        app.run(port=8080)
```

## Related tools / concepts
- [Phidata](phidata.md) — Agno predecessor framework.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Agent context standard.
- [Local LLMs](../ai_knowledge/local_llms.md) — Local open weights execution (Gemma 4).
- [LangGraph](../frameworks/langgraph.md) — Graph-based agent orchestration.
- [FastAPI](../frameworks/fastapi.md) — High-performance Python web framework.
- [PydanticAI](../frameworks/pydantic-ai.md) — Structured agent framework.
- [CrewAI](../frameworks/crewai.md) — Multi-agent role-playing platform.
- [Claude Code](../development_ops/claude-code.md) — CLI coding agent.

## Sources / references
- [Agno Official Website](https://www.agno.com/)
- [Agno GitHub Repository](https://github.com/agno-agi/agno)
- [Agno Documentation Portal](https://docs.agno.com/)
- [FastMCP Specification v3.1](https://modelcontextprotocol.io/spec/fastmcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
