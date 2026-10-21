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

## Systemd Service Unit Configuration

To run the Agno Agent Gateway as a managed systemd unit on a Linux host, place the following configuration file at `/etc/systemd/system/agno-agent-gateway.service`:

```ini
[Unit]
Description=Agno Agent Fleet Gateway & FastMCP 3.1 Server
After=network-online.target postgresql.service redis.service
Wants=network-online.target
Requires=postgresql.service

[Service]
Type=simple
User=agno
Group=agno
WorkingDirectory=/opt/agno-gateway
Environment="PATH=/opt/agno-gateway/venv/bin:/usr/bin"
Environment="AGNO_ENV=production"
Environment="AGNO_LOG_LEVEL=INFO"
Environment="DATABASE_URL=postgresql://agno_user:secure_pass@localhost:5432/agno_db"
Environment="REDIS_URL=redis://localhost:6379/0"

ExecStart=/opt/agno-gateway/venv/bin/uvicorn server:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --loop uvloop \
    --http h11

Restart=always
RestartSec=5s
LimitNOFILE=65536
MemoryAccounting=true
MemoryHigh=16G
MemoryMax=32G

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now agno-agent-gateway.service
sudo systemctl status agno-agent-gateway.service
```

## Getting started

### Installation
Install Agno alongside required model providers and vector dependencies:

```bash
pip install agno openai duckduckgo-search pydantic>=2.0 pgvector fastmcp
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
This complete production code showcases how to build a FastMCP 3.1 server using Agno, incorporating strict Pydantic v2 validation for structured inputs and outputs.

```python
import sys
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ValidationError
from fastmcp import FastMCP
from agno.agent import Agent
from agno.mcp.server import FastMCPServer

# Initialize FastMCP 3.1 Tool Gateway
mcp = FastMCP(
    name="Agno-Security-Analysis-Gateway",
    instructions="FastMCP 3.1 gateway hosting stateless Agno security analysis agents."
)

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

class AnalysisResponse(BaseModel):
    status: str = Field(..., description="Execution status: 'success' or 'error'")
    report: Optional[LogAnalysisReport] = Field(None, description="Validated security report payload")
    error_message: Optional[str] = Field(None, description="Error message if validation or agent failed")

# 2. Instantiate the Agno Agent with structured response modeling
log_agent = Agent(
    name="SecureLogAnalyzer",
    instructions=(
        "Analyze system logs and produce structural JSON matching "
        "the LogAnalysisReport model under strict Pydantic v2 rules."
    ),
    response_model=LogAnalysisReport
)

@mcp.tool()
def analyze_security_logs(target_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executes security log analysis via Agno agent using FastMCP 3.1 and Pydantic v2 verification.
    """
    try:
        audit_target = AuditTarget.model_validate(target_payload)

        # Execute agent query
        raw_response = log_agent.run(
            f"Perform level {audit_target.scan_depth} log audit for host {audit_target.hostname} in {audit_target.environment}"
        )

        validated_report = LogAnalysisReport.model_validate(raw_response.content)

        return AnalysisResponse(
            status="success",
            report=validated_report
        ).model_dump()

    except ValidationError as val_err:
        return AnalysisResponse(
            status="error",
            error_message=f"Pydantic v2 Schema Violation: {val_err.errors()}"
        ).model_dump()
    except Exception as ex:
        return AnalysisResponse(
            status="error",
            error_message=f"Agno Agent Execution Error: {str(ex)}"
        ).model_dump()

if __name__ == "__main__":
    mcp.run()
```

## Production Hardening & Operational Rules

1. **Database Session Store**: Always configure PostgreSQL with `pgvector` for agent session storage; avoid relying solely on in-memory storage for multi-worker FastAPI deployments.
2. **FastMCP Protocol Standard**: Use FastMCP 3.1 explicit tool signatures with Pydantic v2 schemas to ensure interoperability across remote agent clusters.
3. **Connection Pooling**: Set PostgreSQL connection pool size (`pool_size=20`, `max_overflow=10`) in Agno storage settings to avoid database exhaustion under concurrent agent flows.
4. **Error Boundaries**: Wrap all LLM and tool calls inside exception handling blocks returning structured JSON error payloads.

## Troubleshooting Matrix

| Issue / Symptom | Root Cause | Remediation Procedure |
| :--- | :--- | :--- |
| **`PostgreSQL Session Lock Error`** | Concurrent workers attempting to modify the same session record simultaneously | Ensure unique session UUIDs per client or configure row-level optimistic locking. |
| **`FastMCP 3.1 Schema Validation Failure`** | Agent tool payload missing required Pydantic v2 field or pattern match mismatch | Inspect input dictionary against Pydantic model schemas and add defaults for optional fields. |
| **`High Initial Latency on Worker Startup`** | Model embedding weight loading or database migration check blocking startup | Pre-initialize model connections in FastAPI `lifespan` handler before listening. |
| **`ImportError: No module named agno`** | Legacy package imports referencing `phidata` instead of `agno` | Replace `from phidata import ...` with `from agno import ...` in codebase. |
| **`PGVector Distance Calculation Timeout`** | Missing vector index on knowledge base embedding columns | Execute `CREATE INDEX ON embeddings USING hnsw (embedding vector_cosine_ops);` in PostgreSQL. |

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
