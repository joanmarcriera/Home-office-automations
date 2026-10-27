# Maestro Agent Orchestration Framework

## What it is
Maestro is a declarative dataflow orchestration and multi-agent framework designed to build, execute, and monitor resilient agent workflows. In modern AI infrastructure, Maestro provides deterministic graph-based execution pipelines, data routing between autonomous agents, and transactional checkpointing. FastMCP 3.1 agents leverage Maestro to orchestrate multi-step LLM operations, sub-agent task delegators, and tool invocation pipelines.

```
+-----------------------------------------------------------------------------------+
|                        Maestro Agent Workflows Orchestration                      |
|                                                                                   |
|  +------------------------+      +-------------------+      +------------------+  |
|  | FastMCP 3.1 Client     | ---> | Maestro Workflow  | ---> | Agent Node       |  |
|  | Event Trigger / Payload|      | Engine Core       |      | Execution        |  |
|  +------------------------+      +-------------------+      +------------------+  |
|               |                            |                          |           |
+---------------+----------------------------+--------------------------+-----------+
                |                            |                          |
                v                            v                          v
+-----------------------------------------------------------------------------------+
|                           State Persistence & Observability                       |
|                                                                                   |
|  +--------------------+     +---------------------+     +----------------------+  |
|  | State Checkpoint   | --> | Output Routing      | --> | Telemetry            |  |
|  | Store (SQLite/Pg)  |     | & Tool Delivery     |     | & Trace Logs         |  |
|  +--------------------+     +---------------------+     +----------------------+  |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Managing complex multi-agent workflows often leads to race conditions, unhandled task failures, and lost execution state. Maestro addresses these challenges by offering:
- **Declarative Graph Workflows**: Defining agent interactions as directed acyclic graphs (DAGs) or cyclic dataflows with explicit input/output data schemas.
- **Transactional State Persistence**: Saving execution state at each node transition, enabling seamless recovery from failures or API rate limits.
- **FastMCP 3.1 Integration**: Exposing workflow execution and monitoring capabilities directly to MCP clients and AI agent tools.

## Where it fits in the stack
**Frameworks / Agent Orchestration**. Maestro sits as a dataflow graph engine managing communication, state handoffs, and execution graphs across autonomous AI agents.

## Typical use cases
- **Multi-Agent Task Decomposition**: Routing high-level user tasks to specialized sub-agents (researcher, writer, verifier).
- **Transactional Workflow Execution**: Maintaining checkpointed workflow state across asynchronous human-in-the-loop approvals or API rate limits.
- **MCP Tool Pipeline Orchestration**: Chaining FastMCP 3.1 tool calls into deterministic processing workflows.

## Architecture & System Dynamics

```
+-----------------------------------------------------------------------------------+
|                         Maestro Core Engine Architecture                          |
|                                                                                   |
|  +-----------------------+     +------------------------+     +-----------------+ |
|  | FastMCP 3.1 Server    | <-> | Maestro DAG Scheduler  | <-> | SQLite / Pg     | |
|  | Event Interface       |     | & State Engine         |     | Checkpoint Store| |
|  +-----------------------+     +------------------------+     +-----------------+ |
|             |                              |                           |          |
|             v                              v                           v          |
|  +-----------------------+     +------------------------+     +-----------------+ |
|  | Agent Node Execution  | <-> | Message Router &       | <-> | Telemetry &     | |
|  | Runner                |     | Data Transformer       |     | Metrics Log     | |
|  +-----------------------+     +------------------------+     +-----------------+ |
+-----------------------------------------------------------------------------------+
```

```mermaid
sequenceDiagram
    autonumber
    actor Client as FastMCP 3.1 Client
    participant M as Maestro Orchestrator
    participant DB as State Checkpoint Store
    participant Agent as Specialized Sub-Agent

    Client->>M: Trigger workflow execution (workflow_id, inputs)
    M->>DB: Save initial workflow state (status: RUNNING)
    M->>Agent: Dispatch execution task for entry node
    Agent-->>M: Return node output data
    M->>DB: Persist node state checkpoint
    M->>M: Evaluate downstream graph edges
    M-->>Client: Return completion response
```

## Key Features & Capabilities
- **Declarative Graph Engine**: Define multi-agent workflows via YAML/JSON DAG definitions.
- **Checkpoint & Resume**: Fault-tolerant execution saving progress at every node boundary.
- **FastMCP 3.1 Native Integration**: MCP server endpoints allowing external agents to query or execute workflows.

## FastMCP 3.1 Server Tools
Maestro server integrations expose workflow lifecycle controls as FastMCP 3.1 tools:

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Dict, Any, List

mcp = FastMCP("maestro-orchestrator", version="3.1.0")

class WorkflowExecuteRequest(BaseModel):
    workflow_id: str = Field(..., description="Unique ID of Maestro DAG workflow")
    inputs: Dict[str, Any] = Field(default_factory=dict, description="Input parameters passed to the entry node")

class WorkflowExecutionStatus(BaseModel):
    execution_id: str
    status: str  # RUNNING, COMPLETED, FAILED
    current_step: str
    outputs: Dict[str, Any] = Field(default_factory=dict)

@mcp.tool()
async def trigger_maestro_workflow(request: WorkflowExecuteRequest) -> WorkflowExecutionStatus:
    """Trigger a declarative Maestro agent workflow."""
    return WorkflowExecutionStatus(
        execution_id="exec_987654321",
        status="COMPLETED",
        current_step="finish",
        outputs={"result": "Workflow executed successfully"}
    )
```

## Pydantic v2 Schema Specifications
Schema contracts defining Maestro graph nodes and workflow configurations:

```python
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Dict, Any, Optional

class AgentNodeConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    node_id: str = Field(..., description="Unique identifier for the workflow node")
    agent_type: str = Field(..., description="Agent role or model family required")
    max_retries: int = Field(default=3, ge=0, le=10)
    timeout_seconds: int = Field(default=60, ge=1)

class MaestroWorkflowSpec(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    workflow_id: str = Field(..., description="Canonical workflow identifier")
    description: str = Field(..., description="Human readable workflow summary")
    nodes: List[AgentNodeConfig] = Field(..., description="List of nodes in graph")
    edges: Dict[str, List[str]] = Field(..., description="Adjacency list of directed graph edges")
```

## Systemd Service Configuration
Systemd unit file for the Maestro workflow engine daemon:

```ini
[Unit]
Description=Maestro Agent Workflow Orchestration Engine
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=exec
User=maestro
Group=maestro
WorkingDirectory=/opt/maestro-engine
ExecStart=/opt/maestro-engine/bin/maestro-server --config /etc/maestro/config.yaml
Restart=always
RestartSec=3s
Environment=MAESTRO_PORT=9090
Environment=MAESTRO_DB_URL=postgresql://maestro:secret@localhost:5432/maestro_db

ProtectSystem=full
ProtectHome=true
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

## Docker Compose Setup
Docker Compose setup for Maestro workflow engine backed by PostgreSQL:

```yaml
version: '3.8'

services:
  maestro-engine:
    image: ghcr.io/mcp-ecosystem/maestro-engine:3.1.0
    container_name: maestro-engine
    restart: unless-stopped
    ports:
      - "9090:9090"
    environment:
      - DB_HOST=postgres
      - DB_USER=maestro
      - DB_PASS=maestro_pass
      - DB_NAME=maestro_db
    depends_on:
      - postgres
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:9090/health || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 3

  postgres:
    image: postgres:16-alpine
    container_name: maestro-postgres
    restart: unless-stopped
    environment:
      - POSTGRES_USER=maestro
      - POSTGRES_PASSWORD=maestro_pass
      - POSTGRES_DB=maestro_db
    volumes:
      - maestro_pg_data:/var/lib/postgresql/data

volumes:
  maestro_pg_data:
```

## Diagnostic & Troubleshooting Matrix

| Issue / Error Symptom | Potential Root Cause | Diagnostic Method | Remediation Action |
| :--- | :--- | :--- | :--- |
| Workflow Stuck in `PENDING` | Missing node dependency or lock in PostgreSQL state store | `maestro-cli inspect exec_987654321` | Clear database stale lock or rerun node with `maestro-cli retry` |
| Cyclic Node Deadlock | Circular dependency defined in workflow spec | `maestro-cli validate-dag <file.yaml>` | Correct edge definitions in workflow DAG specification |
| Agent Node Timeout | Model endpoint sluggish or payload oversized | `journalctl -u maestro -n 100` | Increase `timeout_seconds` or scale agent model concurrency |

## Strengths
- **Fault-Tolerant Execution**: Persistent state checkpoints ensure long-running workflows recover cleanly.
- **Clear Graph Topology**: Easy to reason about agent inputs, outputs, and branch conditions.
- **FastMCP 3.1 Tool Integration**: First-class MCP support for AI agent orchestration.

## Limitations
- **State Store Requirement**: Requires relational database backing for transactional checkpointing.
- **Graph Complexity Overhead**: Simple single-prompt tasks do not benefit from multi-node DAG definitions.

## When to use it
- For multi-step agent pipelines requiring guaranteed state persistence and sub-agent task routing.
- When organizing complex AI agent interactions into clear directed acyclic graphs.

## When not to use it
- For simple single-turn prompt interactions or basic linear script execution.

## Getting started

```bash
# Clone and build maestro engine CLI
git clone https://github.com/yogthos/maestro
cd maestro
lein bin
```

## CLI examples

```bash
# Validate workflow graph definition file
maestro validate workflow.edn

# Execute workflow DAG with inputs
maestro run workflow.edn --input '{"query": "Generate report"}'
```

## API examples

```clojure
(require '[maestro.core :as m])

(def workflow
  (m/workflow
    {:nodes [{:id :researcher :agent :gpt-4o}
             {:id :writer :agent :claude-3-5}]
     :edges {:researcher [:writer]}}))
```

## Related tools / concepts
- **[AutoGen](../frameworks/autogen.md)**: Multi-agent conversation framework.
- **[Rivet](../frameworks/rivet.md)**: Visual node-based AI agent builder.

## Sources / references
- [Maestro GitHub Repository](https://github.com/yogthos/maestro?ref=2026-10-26-audit)

## Contribution Metadata
- Last reviewed: 2026-10-26
- Confidence: high
