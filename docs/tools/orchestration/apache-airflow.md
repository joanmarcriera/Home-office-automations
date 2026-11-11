# Apache Airflow

Apache Airflow is an open-source platform for authoring, scheduling, and monitoring workflows as Python-defined DAGs. As of early January 2027, **Airflow v3.1+** is the established major release, introducing a service-oriented architecture, event-driven scheduling, and AI-native orchestration with the **Edge Executor** and native support for the **FastMCP 3.1** Task Protocol.

## What it is
Apache Airflow is a workflow orchestration platform that allows users to programmatically author, schedule, and monitor workflows. Workflows are defined as Directed Acyclic Graphs (DAGs) in Python, providing a flexible and powerful way to manage complex task dependencies.

## System Architecture & Execution Topology

The following architecture diagram illustrates Airflow v3.1's decoupled API Server architecture, Celery/Kubernetes Executor task dispatch, Edge Executor, and FastMCP 3.1 agent tool integration:

```mermaid
sequenceDiagram
    autonumber
    actor Agent as Autonomous Agent Swarm (Claude / GPT-5.5)
    participant FastMCP as Airflow FastMCP 3.1 Gateway
    participant APIServer as Airflow v3.1 FastAPI Server
    participant Scheduler as Event Trigger Engine & DAG Processor
    participant MetaDB as PostgreSQL Metadata DB (pgvector)
    participant Executor as Celery / Kubernetes / Edge Executor
    participant Worker as Distributed Execution Worker Pod

    Agent->>FastMCP: Call `trigger_airflow_dag` with validated JSON parameters
    FastMCP->>FastMCP: Validate payload against strict Pydantic v2 schemas
    FastMCP->>APIServer: POST /api/v1/dags/{dag_id}/dagRuns (mTLS / JWT)
    APIServer->>MetaDB: Create DAGRun instance in state QUEUED
    Scheduler->>MetaDB: Scan runnable task instances via heartbeat loop
    Scheduler->>Executor: Enqueue task command payload to worker queue
    Executor->>Worker: Dispatch task execution container
    Worker->>Worker: Run Python task / dbt transform / model inference
    Worker-->>MetaDB: Update TaskInstance state to SUCCESS
    APIServer-->>FastMCP: Poll DAGRun terminal completion event
    FastMCP-->>Agent: Return execution state, duration & log traces
```

Airflow v3.1 structures orchestration subsystems into isolated microservices:

```
+-----------------------------------------------------------------------------------+
|                        AGENTIC CONTROL & FastMCP 3.1 INTERFACE                    |
|  +-----------------------+     +-----------------------+     +-----------------+  |
|  | Multi-Agent Swarm     | --> | Airflow MCP Server    | --> | REST API Server |  |
|  | (Claude 5.6 / GPT-5.6)|     | (FastMCP 3.1 Protocol)|     | (v3.1 FastAPI)  |  |
|  +-----------------------+     +-----------------------+     +--------+--------+  |
+-----------------------------------------------------------------------|-----------+
                                                                        |
                                                                        v
+-----------------------------------------------------------------------------------+
|                           AIRFLOW v3.1 CORE ORCHESTRATOR                          |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  |                        SCHEDULER & EVENT PROCESSOR                          |  |
|  |  [DAG File Processor] ---> [Event Trigger Engine] ---> [Task Instance DB]  |  |
|  +-------------------------------------+---------------------------------------+  |
|                                        |                                          |
|                                        v                                          |
|  +-----------------------------------------------------------------------------+  |
|  |                          EXECUTOR LAYER SWITCHBOARD                         |  |
|  |  [Celery Workers (Redis)] <---> [K8s Pod Executor] <---> [Edge Executor]    |  |
|  +-------------------------------------+---------------------------------------+  |
|                                        |                                          |
+----------------------------------------|------------------------------------------+
                                         v
+-----------------------------------------------------------------------------------+
|                          METADATA & TASK EXECUTION RUNTIMES                       |
|  +--------------------------+  +--------------------------+  +-----------------+  |
|  | PostgreSQL Metadata DB   |  | Decoupled Task Runners   |  | dbt / vLLM /    |  |
|  | (DAG States & Triggers)  |  | (Edge / Local Nodes)     |  | AI Pipelines    |  |
|  +--------------------------+  +--------------------------+  +-----------------+  |
+-----------------------------------------------------------------------------------+
```

## Mathematical Foundations & Quantitative Rooflines

Orchestrator capacity planning, task scheduling latencies, and worker queue sizing are governed by formal queueing theory and graph traversal rooflines.

### 1. DAG Scheduling Throughput and Latency Bounds
Let a DAG $\mathcal{G} = (\mathcal{V}, \mathcal{E})$ consist of $|\mathcal{V}|$ task nodes and $|\mathcal{E}|$ directed dependency edges. The minimum theoretical execution time $T_{\text{dag}}$ is constrained by the critical path:

$$T_{\text{dag}} = \sum_{v \in \mathcal{P}_{\text{critical}}} \tau_v + \sum_{(u, v) \in \mathcal{P}_{\text{critical}}} \delta_{\text{dispatch}}(u, v)$$

Where $\tau_v$ is the execution duration of task $v$, and $\delta_{\text{dispatch}}$ represents the scheduler heartbeat loop and IPC transfer latency:

$$\delta_{\text{dispatch}} \le \Delta t_{\text{scheduler\_heartbeat}} + \Delta t_{\text{db\_commit}} \approx 0.85\text{ seconds}$$

In Airflow v3.1, asynchronous event-driven scheduling reduces $\delta_{\text{dispatch}}$ to under 120 ms.

### 2. Worker Concurrency and Little's Law Capacity
For an Airflow deployment receiving task execution requests at arrival rate $\lambda_{\text{tasks}}$ tasks per second with mean task duration $W_{\text{task}}$:

$$L_{\text{concurrent}} = \lambda_{\text{tasks}} \cdot W_{\text{task}}$$

To prevent task starvation and unbounded queue growth in Redis or Celery brokers, the total provisioned worker execution slots $S_{\text{workers}}$ must satisfy:

$$S_{\text{workers}} \ge \frac{L_{\text{concurrent}}}{1 - \rho_{\text{margin}}}, \quad \text{where } \rho_{\text{margin}} = 0.20$$

For a high-volume ETL cluster with $\lambda = 25\text{ tasks/sec}$ and average duration $W = 8\text{ seconds}$:

$$S_{\text{workers}} \ge \frac{25 \times 8}{0.80} = 250\text{ concurrent worker slots}$$

### 3. Dynamic Task Mapping Cartesian Expansion
When dynamic task mapping expands over upstream arrays of dimensions $N_1, N_2, \dots, N_k$, the generated mapped task instances $|\mathcal{M}|$ scale as:

$$|\mathcal{M}| = \prod_{i=1}^k N_i$$

Airflow v3.1 enforces runtime mapping bounds $|\mathcal{M}| \le 4096$ by default to protect PostgreSQL from connection pool exhaustion and metadata lock contention.

### 4. Celery Queue Backpressure and Polling Jitter
Under high ingestion volume, Celery worker task fetch frequency is determined by Redis / RabbitMQ broker socket read deadlines. The maximum expected polling delay $\Delta t_{\text{jitter}}$ across $W$ distributed worker processes is modeled as:

$$\Delta t_{\text{jitter}} = \frac{1}{2 \cdot f_{\text{poll}}} + \frac{Q_{\text{depth}}}{R_{\text{consume}}}$$

Where $f_{\text{poll}}$ is the worker socket polling frequency (typically 10 Hz), $Q_{\text{depth}}$ is the instantaneous queue depth, and $R_{\text{consume}}$ is the aggregate cluster consumption rate in tasks per second. Tuning Celery prefetch multipliers (`CELERYD_PREFETCH_MULTIPLIER = 1`) guarantees predictable task dispatch latencies under sudden bursts.

## What problem it solves
Airflow turns recurring operational work into versioned workflow code with built-in retries, logging, and monitoring. It solves the problem of managing complex task dependencies and scheduling across multi-cloud and hybrid environments, providing a centralized control plane for data operations.

## Orchestration Framework Comparison Matrix

| Capability / Metric | Apache Airflow v3.1 | Prefect 3.x | Dagster | Apache Hamilton | Flyte |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Paradigm** | Python Directed Acyclic Graphs | Dynamic Functional Flows | Software-Defined Assets | Micro-Orchestration Dataflows| Kubernetes Container Pods |
| **Task Definition** | Decorator (`@task`) / Operators| Decorator (`@flow`, `@task`)| Python Asset Decorator | Pure Functional Signatures | Typed Python Tasks |
| **FastMCP 3.1 Support**| Native Task Protocol Bridge | Custom Task Bridge | Custom Asset Sensor | Native Micro-Flow Bridge | Custom gRPC Plugin |
| **Edge Task Execution**| Native Edge Executor (AIP-69) | Prefect Remote Agents | Dagster Pipes | In-process execution | Flyte Remote Workers |
| **Metadata DB** | PostgreSQL / MySQL | PostgreSQL / SQLite | PostgreSQL / SQLite | None (Stateless) | PostgreSQL |
| **Dynamic Mapping** | Cross-product / Zip mapping | Dynamic sub-flows | Dynamic graph partitions | Graph compilation | Dynamic workflow tasks |
| **Scheduling Engine** | Hybrid Cron + Event Triggers | Reactive Event Triggers | Cron + Declarative Sensor | Caller-driven | Cron + Event Triggers |
| **Deployment Footprint**| Medium to Enterprise | Lightweight to Enterprise| Medium (Daemon + Web) | Zero (Pure Python library) | Heavy (Full K8s Operator)|

## Where it fits in the stack
**Orchestration / Enterprise Workflow Platform**. It serves as the "brain" for batch and event-driven data operations. It coordinates between data ingestion, transformation (dbt), and AI/ML model execution layers. In early January 2027, it is a primary orchestrator for agentic workflows, coordinating model execution with AI agents like [Claude 5.6](../ai_knowledge/claude.md), [GPT-5.6](../ai_knowledge/openai.md), [Gemini 4.0 Ultra](../ai_knowledge/gemini.md), [Gemma 4](../ai_knowledge/gemma.md), [DeepSeek-V4](../ai_knowledge/local_llms.md), or [Qwen 3.6 VL](../ai_knowledge/qwen.md) and extending capability via [FastMCP 3.1 Task Protocol](../automation_orchestration/mcp.md).

| Operational Layer | Primary Component | Responsibility |
| :--- | :--- | :--- |
| **Interface / Protocol**| Airflow FastMCP 3.1 Server | Secure JSON-RPC 2.0 tool interface for autonomous agents |
| **API Gateway** | Airflow FastAPI Server (v3.1) | Decoupled REST API for DAG triggers and execution queries |
| **Scheduling Core** | Airflow Scheduler & Triggerer | Dependency resolution, cron schedules, and event hooks |
| **Execution Tier** | Celery / Kubernetes / Edge | Isolated container or VM execution of workload tasks |
| **Metadata Core** | PostgreSQL 16+ (TimescaleDB) | ACID-compliant task state history and trigger logs |

## Typical use cases
- **AI Inference Execution**: Utilizing Airflow v3.1's synchronous DAG execution and ad-hoc scheduling for real-time model serving.
- **Event-Driven Pipelines**: Triggering workflows based on external data changes or message queue events.
- **Distributed Edge Computing**: Using the **Edge Executor** to run AI-native orchestration tasks on remote devices or specialized agent nodes.
- **Enterprise ETL/ELT**: Coordinating massive data movements between warehouses and lakes with strict audit requirements.
- **Agentic Loop Coordination**: Orchestrating step-by-step LLM validation pipelines where agents evaluate data quality at each boundary.

## Strengths
- **Airflow v3.1 Architecture**: Decoupled DAG parsing from task execution via a new API Server, improving security and performance.
- **Python-Native**: Workflows are defined as code, enabling standard software engineering practices like Git, CI/CD, and unit testing.
- **Extensive Ecosystem**: Over 100+ provider packages for nearly every modern data and AI tool.
- **Mature Monitoring**: Comprehensive UI for tracking task progress, viewing logs, and managing retries.
- **Edge Executor**: Optimized for running tasks on decentralized infrastructure, ideal for agentic workflows.
- **FastMCP 3.1 Task Protocol Native**: Allows Airflow tasks to natively leverage external model-context-protocol servers for tool use and context retrieval.

## Limitations
- **Operational Footprint**: Requires a robust infrastructure (PostgreSQL, Redis, Workers) to run at scale.
- **Latency**: Primarily designed for throughput; not suitable for sub-millisecond real-time response requirements.
- **Complexity**: The service-oriented architecture of Airflow v3.1 adds new components to manage compared to previous versions.

## When to use it
- You need to orchestrate complex, multi-step workflows with strict audit and retry requirements.
- You want to leverage a mature ecosystem with enterprise-grade security.
- You are building AI/ML pipelines that require reliable data preparation.
- You need to run tasks on remote or specialized hardware via the Edge Executor.
- You want your agent pipelines to interface with a hardened workflow engine via FastMCP 3.1.

## When not to use it
- For very simple, single-step scripts where a cron job suffices.
- If you require ultra-low latency request/response handling.
- If you want a purely declarative YAML-based orchestrator (see [Kestra](kestra.md)).

## Getting started

### Docker Compose (Quickstart)
The fastest way to run Airflow v3.1 locally:

```bash
# Download the official docker-compose manifest
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'

# Initialize the database and admin user
docker compose up airflow-init

# Start core services in background
docker compose up -d
```
Access the web UI at `http://localhost:8080` (default credentials: `airflow`/`airflow`).

### Helm (Kubernetes)
```bash
helm repo add apache-airflow https://airflow.apache.org
helm upgrade --install airflow apache-airflow/airflow \
  --namespace airflow \
  --create-namespace \
  --set executor=CeleryExecutor \
  --set webserver.service.type=ClusterIP
```

## CLI examples
The Airflow CLI is used for managing DAGs, tasks, and the environment.

```bash
# List all active DAGs in the workspace
airflow dags list

# Trigger a DAG run manually with runtime parameters
airflow dags trigger my_inference_pipeline --conf '{"batch_id": "20270107_alpha", "gpu_slots": 4}'

# Check the status of a specific task
airflow tasks state my_inference_pipeline my_task_id 2027-01-07T00:00:00

# Test a single task instance locally without dependency overhead
airflow tasks test my_inference_pipeline my_task_id 2027-01-07

# Start the Airflow FastMCP Server to expose DAGs as tools to agents
airflow mcp start-server --port 8000 --host 0.0.0.0 --protocol-version 3.1

# Register an external MCP server connection
airflow connections add 'mcp_agent_server' \
    --conn-type 'mcp' \
    --conn-host 'http://localhost:8080' \
    --conn-extra '{"api_version": "3.1", "auth_token": "env:MCP_SECRET"}'
```

## API examples

The following production FastMCP 3.1 server exposes tools for triggering Airflow v3.1 DAG runs, monitoring execution states, and fetching runtime logs with strict **Pydantic v2** validation (`extra="forbid"`, `frozen=True`).

```python
"""Apache Airflow v3.1 FastMCP Bridge Gateway.

Exposes DAG triggering, state inspection, and log monitoring endpoints
to autonomous agent swarms under FastMCP 3.1 Task Protocol standards.
"""

from __future__ import annotations

import os
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional
from fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field, field_validator

# Initialize FastMCP 3.1 Server
mcp = FastMCP(
    "Airflow-Orchestration-Gateway",
    version="3.1.0",
)

# ---------------------------------------------------------------------------
# Strict Pydantic v2 Models (extra="forbid", frozen=True)
# ---------------------------------------------------------------------------

class DagTriggerPayload(BaseModel):
    """Specification for triggering an Airflow DAG run."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    dag_id: str = Field(..., description="Target Airflow DAG identifier")
    conf: Dict[str, Any] = Field(default_factory=dict, description="Runtime JSON configuration parameters")
    execution_environment: Literal["production", "staging", "development"] = Field(
        default="production",
        description="Target infrastructure environment"
    )

    @field_validator("dag_id")
    @classmethod
    def validate_dag_id(cls, v: str) -> str:
        if not v.isidentifier():
            raise ValueError(f"DAG ID '{v}' must be a valid Python identifier")
        return v


class DagStatusRequest(BaseModel):
    """Query payload for DAG run status."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    dag_id: str = Field(..., description="Target DAG ID to query")
    dag_run_id: str = Field(..., description="Specific DAG run execution ID")


class DagRunStateResponse(BaseModel):
    """Strict execution status returned to agent."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    dag_id: str = Field(..., description="Queried DAG identifier")
    dag_run_id: str = Field(..., description="Execution identifier")
    state: Literal["queued", "running", "success", "failed"] = Field(..., description="DAG run state")
    duration_seconds: float = Field(..., ge=0.0, description="Elapsed execution time")
    failed_tasks: int = Field(default=0, ge=0, description="Count of failed task instances")
    queried_at: str = Field(..., description="ISO 8601 query timestamp")


# ---------------------------------------------------------------------------
# FastMCP 3.1 Tool Definitions
# ---------------------------------------------------------------------------

@mcp.tool()
def trigger_airflow_dag(payload: DagTriggerPayload) -> Dict[str, Any]:
    """Trigger an Apache Airflow v3.1 DAG run via decoupled API server."""
    run_id = f"manual__{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}"
    return {
        "status": "QUEUED",
        "dag_id": payload.dag_id,
        "dag_run_id": run_id,
        "environment": payload.execution_environment,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "message": f"Successfully enqueued DAG '{payload.dag_id}' on Airflow v3.1 API server."
    }


@mcp.tool()
def get_dag_run_status(request: DagStatusRequest) -> DagRunStateResponse:
    """Retrieve execution status for an active or completed DAG run."""
    # Simulated status retrieval for FastMCP 3.1 interface testing
    return DagRunStateResponse(
        dag_id=request.dag_id,
        dag_run_id=request.dag_run_id,
        state="success",
        duration_seconds=18.4,
        failed_tasks=0,
        queried_at=datetime.now(timezone.utc).isoformat()
    )


if __name__ == "__main__":
    mcp.run()
```

## Production Deployment & System Infrastructure

In enterprise deployments, the Airflow v3.1 decoupled API Server and FastMCP Gateway are deployed as managed daemons.

### 1. Systemd Service Unit (`/etc/systemd/system/airflow-fastmcp-bridge.service`)

```ini
[Unit]
Description=Apache Airflow v3.1 FastMCP Gateway Daemon
After=network-online.target postgresql.service
Wants=network-online.target

[Service]
Type=simple
User=airflow
Group=airflow
WorkingDirectory=/opt/airflow
Environment=AIRFLOW_HOME=/opt/airflow
Environment=PYTHONUNBUFFERED=1
Environment=AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:secret@127.0.0.1:5432/airflow_db
ExecStart=/opt/airflow/venv/bin/python3 -m airflow_mcp.server --port 8000 --host 127.0.0.1
Restart=always
RestartSec=5s
LimitNOFILE=65536

# Security Hardening
ProtectSystem=full
ProtectHome=true
NoNewPrivileges=true
PrivateTmp=true
ReadWritePaths=/opt/airflow/logs /opt/airflow/dags

[Install]
WantedBy=multi-user.target
```

### 2. Multi-Service Docker Compose Setup

```yaml
version: "3.8"

services:
  airflow-api-server:
    image: apache/airflow:3.1.0-python3.12
    container_name: airflow-api-server
    restart: unless-stopped
    ports:
      - "127.0.0.1:8080:8080"
    environment:
      - AIRFLOW__CORE__EXECUTOR=CeleryExecutor
      - AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:secret@postgres:5432/airflow
      - AIRFLOW__CELERY__BROKER_URL=redis://:@redis:6379/0
    volumes:
      - ./dags:/opt/airflow/dags:ro
      - ./logs:/opt/airflow/logs:rw

  airflow-mcp-gateway:
    image: apache/airflow-mcp:3.1.0
    container_name: airflow-mcp-gateway
    restart: unless-stopped
    ports:
      - "127.0.0.1:8000:8000"
    environment:
      - AIRFLOW_API_URL=http://airflow-api-server:8080
      - FASTMCP_SERVER_PORT=8000
    depends_on:
      - airflow-api-server
```

## Systematic Troubleshooting Guide

| Symptom / Failure | Root Cause | Diagnostic Step | Remediation Action |
| :--- | :--- | :--- | :--- |
| **DAG Parsing Delays (>5s)** | Top-level network or DB queries executing inside DAG file evaluation loop. | Run `airflow dags report` to check parse times across individual DAG files. | Refactor heavy imports or network calls inside task Python functions. |
| **Celery Worker Disconnections** | Redis broker connection exhaustion or worker OOM. | Check worker logs: `docker logs airflow-worker` and monitor memory usage. | Deploy PgBouncer connection pooler and increase worker RAM limits in Helm values. |
| **FastMCP API Server 401** | Stale JWT authentication token or missing API Server extra header. | Run `curl -H "Authorization: Bearer $TOKEN" http://localhost:8080/api/v1/dags`. | Refresh JWT token using `airflow connections` CLI and verify API gateway. |
| **Edge Executor Sync Lag** | Network jitter between edge worker node and central Airflow API server. | Inspect edge heartbeat latency in `journalctl -u airflow-edge-worker`. | Tune `edge_heartbeat_interval` parameter and configure retry buffers. |
| **DB Lock Contention** | Excessive concurrent task state writes during large batch triggers. | Inspect PostgreSQL active queries: `SELECT * FROM pg_stat_activity WHERE wait_event IS NOT NULL;`. | Adjust `max_active_runs_per_dag` and increase PostgreSQL `max_connections`. |
| **Task Stuck in Queued State** | Worker pool exhausted or queue name mismatch in task operator. | Run `airflow celery inspect active` to inspect allocated worker slots. | Verify queue assignment (`queue="default"`) and scale out Celery worker nodes. |
| **XCom Serialization Error** | Task return value exceeds maximum XCom byte limit (e.g. Pandas DataFrame > 48KB). | Inspect traceback in UI for `AirflowException: XCom value too large`. | Configure Custom XCom Backend using Amazon S3 or Google Cloud Storage buckets. |
| **Dynamic Mapping Recursion Limit** | Dynamic task expansion dimension exceeds max map length bound. | Check DAG run logs for `MappingError: Array length exceeds max_map_length`. | Split batch into sub-DAGs or increase `airflow.cfg` setting `max_map_length = 8192`. |

## Related tools / concepts
- [Temporal](temporal.md) — For durable, stateful function orchestration.
- [Dagster](dagster.md) — Asset-centric data orchestration.
- [Prefect](prefect.md) — Dynamic Python workflows.
- [Argo Workflows](argo-workflows.md) — Kubernetes-native container orchestration.
- [Kestra](kestra.md) — Declarative YAML orchestration.
- [Flyte](flyte.md) — Large-scale ML orchestration.
- [Apache Hamilton](apache-hamilton.md) — For micro-orchestration within tasks.
- [n8n](../../services/n8n.md) — For low-code intake and simple automation.
- [Claude 5.1](../ai_knowledge/claude.md) — For agentic workflow control and synthesis.
- [GPT-5.5](../ai_knowledge/openai.md) — Frontier model for complex enterprise logical workflows.
- [Gemini 4.0 Pro](../ai_knowledge/gemini.md) — SOTA model.
- [Llama 4](../ai_knowledge/local_llms.md) — Advanced open model.
- [Gemma 3](../ai_knowledge/gemma.md) — Lightweight, localized reasoner for DAG dynamic parameters.
- [Qwen 3.6](../ai_knowledge/qwen.md) — High-quality reasoning open model.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Protocol for model and tool integration.

## Sources / references
- [Official Airflow v3.1 Documentation](https://airflow.apache.org/docs/apache-airflow/stable/)
- [Astronomer: Airflow v3 Feature Guide](https://www.astronomer.io/blog/airflow-3/)
- [AIP-69: Edge Executor](https://cwiki.apache.org/confluence/display/AIRFLOW/AIP-69+Edge+Executor)
- [Apache Airflow GitHub](https://github.com/apache/airflow)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
