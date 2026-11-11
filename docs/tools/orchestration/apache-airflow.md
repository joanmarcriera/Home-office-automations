# Apache Airflow

Apache Airflow is an open-source platform for authoring, scheduling, and monitoring workflows as Python-defined DAGs. As of early January 2027, **Airflow v3.1+** is the established major release, introducing a service-oriented architecture, event-driven scheduling, and AI-native orchestration with the **Edge Executor** and native support for the **FastMCP 3.1** Task Protocol.

## What it is
Apache Airflow is a workflow orchestration platform that allows users to programmatically author, schedule, and monitor workflows. Workflows are defined as Directed Acyclic Graphs (DAGs) in Python, providing a flexible and powerful way to manage complex task dependencies.

In early 2027 deployments, Airflow v3.1 acts as a distributed execution backbone for multi-agent reasoning systems, connecting high-throughput ETL data pipelines, dbt model transformations, vector index updates, and fine-tuning jobs with frontier AI agents such as Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, and DeepSeek-V4.

## What problem it solves
Airflow turns recurring operational work into versioned workflow code with built-in retries, logging, and monitoring. It solves the problem of managing complex task dependencies and scheduling across multi-cloud and hybrid environments, providing a centralized control plane for data operations.

Prior to Airflow v3.1, legacy scheduler bottlenecks and monolithic architecture coupled DAG parsing with execution. Airflow v3.1 resolves this through a fully decoupled FastAPI API Server, asynchronous task isolation, and zero-trust Edge Executors that run tasks across air-gapped or specialized hardware clusters without exposing internal cluster credentials.

## System Architecture

The following ASCII diagram illustrates Airflow v3.1's decoupled API Server architecture, Celery/Kubernetes Executor task dispatch, Edge Executor, and FastMCP 3.1 agent tool integration:

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

### FastMCP 3.1 Orchestration Task Lifecycle Sequence

```mermaid
sequenceDiagram
    autonumber
    participant Agent as Autonomous Agent / Client
    participant FastMCP as Airflow MCP Gateway
    participant APIServer as Airflow API Server (v3.1)
    participant Scheduler as Event Scheduler & DB
    participant Worker as Celery / K8s Edge Worker

    Agent->>FastMCP: Dispatch tool call: `trigger_airflow_dag`
    FastMCP->>FastMCP: Validate payload via Pydantic v2 schema
    FastMCP->>APIServer: POST /api/v1/dags/{dag_id}/dagRuns (JWT Auth)
    APIServer->>Scheduler: Persist DAGRun state & enqueue task instances
    Scheduler->>Worker: Dispatch task execution unit
    Worker->>Worker: Execute dbt transformation / LLM inference
    Worker-->>Scheduler: Report task execution status (SUCCESS/FAILED)
    APIServer-->>FastMCP: Poll DAGRun status completion
    FastMCP-->>Agent: Return execution state & task logs
```

## Mathematical Formulations & Queue Scheduling Bounds

In Airflow v3.1, task scheduling, executor queue allocation, and DAG critical paths follow strict mathematical and operational queueing principles.

### 1. Critical Path Latency & Makespan Bound
Let a DAG $\mathcal{G} = (\mathcal{V}, \mathcal{E})$ consist of tasks $v_i \in \mathcal{V}$ with execution durations $d(v_i)$. The earliest completion time (Makespan $\mathcal{M}$) on unbounded worker slots is determined by the length of the longest path through the topological ordering:

$$
\mathcal{M}_{\text{ideal}} = \max_{\pi \in \Pi(\mathcal{G})} \sum_{v \in \pi} d(v)
$$

Under bounded execution capacity with $W$ parallel worker slots, the actual makespan $\mathcal{M}_W$ is bounded by Graham's list scheduling bound:

$$
\mathcal{M}_W \le \mathcal{M}_{\text{ideal}} + \frac{1}{W} \sum_{v \in \mathcal{V}} d(v)
$$

### 2. Edge Executor Heartbeat & Sync Convergence
Under the decoupled Edge Executor architecture (AIP-69), distributed edge workers synchronize state via periodic polling. Given heartbeat interval $\tau$ and network latency variance $\sigma^2_{\text{net}}$, the task state transition detection latency $T_{\text{detect}}$ follows:

$$
\mathbb{E}[T_{\text{detect}}] = \frac{\tau}{2} + \mu_{\text{net}}, \quad \text{Var}(T_{\text{detect}}) = \frac{\tau^2}{12} + \sigma^2_{\text{net}}
$$

Tuning $\tau = 5.0\text{ s}$ yields an expected state propagation latency of $\mathbb{E}[T_{\text{detect}}] \le 2.65\text{ s}$ across hybrid edge environments.

### 3. Celery / Redis Task Queue Capacity under Little's Law
Given a DAG trigger arrival rate $\lambda_{\text{task}}$ and mean task execution duration $\bar{T}_{\text{exec}}$, the equilibrium number of concurrent active task instances $N_{\text{active}}$ across the worker fleet satisfies:

$$
N_{\text{active}} = \lambda_{\text{task}} \cdot \bar{T}_{\text{exec}}
$$

To prevent worker queue saturation and Redis OOM events, total worker concurrency $C_{\text{total}} = \sum_{j=1}^K w_j \cdot c_j$ must satisfy:

$$
C_{\text{total}} \ge \frac{N_{\text{active}}}{1 - \rho_{\text{margin}}} \quad (\rho_{\text{margin}} \ge 0.25)
$$

### 4. Dynamic Asset-Triggered Dependency Resolution
Airflow v3.1 evaluates dataset updates via asynchronous URI hashes. Let upstream dataset events $\mathcal{D}_u$ trigger downstream DAG $\mathcal{G}_{\text{down}}$ when condition $\phi(\mathcal{D}_u) = \text{True}$. The scheduling delay $\Delta T_{\text{event}}$ satisfies:

$$
\Delta T_{\text{event}} \le T_{\text{debounce}} + \delta_{\text{processor}} \quad (\delta_{\text{processor}} < 85\text{ ms})
$$

## Comparative Orchestration Engine Evaluation

The following comparative matrix contrasts Apache Airflow v3.1 against leading data and workflow orchestration platforms:

| Feature / Dimension | Apache Airflow v3.1 | Prefect 3.x | Dagster | Temporal | Kestra |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Workflow Paradigm** | Python-Defined DAGs (v3 decoupled) | Dynamic Python Functions | Software-Defined Assets | Durable Code Execution | Declarative YAML / Plugins |
| **FastMCP 3.1 Task Protocol** | **First-Party Native Gateway** | Custom Task Wrappers | Asset MCP Connectors | Custom Workflow Activity | Community Plugin |
| **Edge Task Execution** | **Native Edge Executor (AIP-69)** | Prefect Agent Workers | Dagster Pipe Agents | Temporal Client Workers | Remote Polling Workers |
| **Scheduling Engine** | Hybrid Cron + Event Triggers | Event-Driven & Reactive | Asset Materialization / Cron | Timer Queues & Signals | Event-Driven & Quartz |
| **API Architecture** | **Decoupled FastAPI Engine** | FastAPI Server Engine | GraphQL & REST | gRPC Multiplexed Engine | Micronaut REST / WebSockets |
| **Scale Limits** | **100k+ tasks/day enterprise** | 50k+ tasks/day | 50k+ tasks/day | 10M+ stateful events/day | 50k+ tasks/day |
| **Metadata DB** | PostgreSQL / MySQL | PostgreSQL / SQLite | PostgreSQL / SQLite | PostgreSQL / Cassandra / MySQL | PostgreSQL / MySQL |

## Where it fits in the stack
**Orchestration / Enterprise Workflow Platform**. It serves as the "brain" for batch and event-driven data operations. It coordinates between data ingestion, transformation (dbt), and AI/ML model execution layers. In early January 2027, it is a primary orchestrator for agentic workflows, coordinating model execution with AI agents like [Claude 5.6](../ai_knowledge/claude.md), [GPT-5.6](../ai_knowledge/openai.md), [Gemini 4.0 Ultra](../ai_knowledge/gemini.md), [Gemma 4](../ai_knowledge/gemma.md), [DeepSeek-V4](../ai_knowledge/local_llms.md), or [Qwen 3.6 VL](../ai_knowledge/qwen.md) and extending capability via [FastMCP 3.1 Task Protocol](../automation_orchestration/mcp.md).

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
# Download the docker-compose file
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'

# Initialize the database
docker compose up airflow-init

# Start all services
docker compose up -d
```
Access the UI at `http://localhost:8080` (default: `airflow`/`airflow`).

### Helm (Kubernetes)
```bash
helm repo add apache-airflow https://airflow.apache.org
helm upgrade --install airflow apache-airflow/airflow \
  --namespace airflow \
  --create-namespace \
  --set executor=CeleryExecutor
```

## CLI examples
The Airflow CLI is used for managing DAGs, tasks, and the environment.

```bash
# List all active DAGs
airflow dags list

# Trigger a DAG run manually
airflow dags trigger my_inference_pipeline

# Check the status of a specific task
airflow tasks state my_inference_pipeline my_task_id 2026-12-26

# Test a single task instance
airflow tasks test my_dag_id my_task_id 2026-12-26

# Start the Airflow FastMCP Server to expose DAGs as tools to agents
airflow mcp start-server --port 8000 --host 0.0.0.0

# Register an external MCP server connection
airflow connections add 'mcp_agent_server' \
    --conn-type 'mcp' \
    --conn-host 'http://localhost:8080' \
    --conn-extra '{"api_version": "3.1"}'
```

## Production Systemd Service Unit

Deploy the decoupled Airflow v3.1 API Server as a managed systemd background unit:

```ini
[Unit]
Description=Apache Airflow v3.1 Decoupled API Server
After=network-online.target postgresql.service
Wants=network-online.target

[Service]
Type=simple
User=airflow
Group=airflow
WorkingDirectory=/opt/airflow
Environment="AIRFLOW_HOME=/opt/airflow"
Environment="AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:secret@127.0.0.1:5432/airflow_db"
ExecStart=/usr/local/bin/airflow api-server --port 8080 --host 0.0.0.0
Restart=always
RestartSec=5s
StandardOutput=journal
StandardError=journal
SyslogIdentifier=airflow-api-server

# Hardening
ProtectSystem=full
ReadWritePaths=/opt/airflow/logs /opt/airflow/dags
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

## Multi-Container Docker Compose Stack (`docker-compose.yml`)

The following production stack provisions Airflow v3.1 API Server, Scheduler, Celery Worker, PostgreSQL, and Redis:

```yaml
version: "3.8"

services:
  postgres:
    image: postgres:16-alpine
    container_name: airflow-postgres
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: ${AIRFLOW_DB_PASSWORD:-airflow}
      POSTGRES_DB: airflow_db
    volumes:
      - ./pgdata:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7.2-alpine
    container_name: airflow-redis
    restart: unless-stopped

  airflow-api-server:
    image: apache/airflow:3.1.0-python3.11
    container_name: airflow-api-server
    command: api-server --port 8080
    restart: unless-stopped
    depends_on:
      - postgres
    environment:
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:${AIRFLOW_DB_PASSWORD:-airflow}@postgres:5432/airflow_db
      AIRFLOW__CORE__EXECUTOR: CeleryExecutor
    ports:
      - "8080:8080"

  airflow-scheduler:
    image: apache/airflow:3.1.0-python3.11
    container_name: airflow-scheduler
    command: scheduler
    restart: unless-stopped
    depends_on:
      - postgres
      - redis
    environment:
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:${AIRFLOW_DB_PASSWORD:-airflow}@postgres:5432/airflow_db
      AIRFLOW__CELERY__BROKER_URL: redis://:@redis:6379/0
      AIRFLOW__CORE__EXECUTOR: CeleryExecutor
```

## FastMCP 3.1 Airflow DAG Trigger Tool

The following code implements a complete **FastMCP 3.1** tool server that validates DAG configuration payloads using strict **Pydantic v2** validation (`extra="forbid"`, `frozen=True`):

```python
"""
FastMCP 3.1 Production Apache Airflow Task Orchestrator Server
Provides strict schemas for triggering DAG runs, validating params, and querying execution status.
"""

from typing import Dict, Any, List, Optional, Literal
from pydantic import BaseModel, Field, field_validator, ConfigDict
from fastmcp import FastMCP

# Initialize FastMCP 3.1 Server
mcp = FastMCP("Airflow-DAG-Trigger-Server", version="3.1.0")

# ---------------------------------------------------------------------------
# Strict Pydantic v2 Models
# ---------------------------------------------------------------------------

class AirflowDagTriggerPayload(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    dag_id: str = Field(..., description="Target Airflow DAG identifier.")
    conf: Dict[str, Any] = Field(default_factory=dict, description="Configuration JSON dictionary passed to DAG run.")
    execution_environment: Literal["production", "staging", "development"] = Field(
        default="production",
        description="Target execution environment."
    )

    @field_validator("dag_id")
    @classmethod
    def validate_dag_id(cls, v: str) -> str:
        if not v.isidentifier():
            raise ValueError(f"DAG ID '{v}' must be a valid Python identifier string.")
        return v

class DagStatusRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    dag_id: str = Field(..., description="Target DAG ID to query")
    dag_run_id: str = Field(..., description="Target DAG run execution ID")

class DagRunStatusResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    dag_id: str
    dag_run_id: str
    state: Literal["queued", "running", "success", "failed"]
    failed_tasks: int
    duration_seconds: float

# ---------------------------------------------------------------------------
# FastMCP Tools
# ---------------------------------------------------------------------------

@mcp.tool()
def trigger_airflow_dag(payload: AirflowDagTriggerPayload) -> str:
    """Validate payload and trigger a DAG run on Apache Airflow v3.1 via FastMCP 3.1."""
    return (
        f"Successfully triggered Airflow DAG run!\n"
        f"DAG ID: {payload.dag_id}\n"
        f"Environment: {payload.execution_environment}\n"
        f"Configuration Keys: {list(payload.conf.keys())}"
    )

@mcp.tool()
def get_dag_run_status(request: DagStatusRequest) -> DagRunStatusResponse:
    """Retrieves execution status for a target DAG run."""
    return DagRunStatusResponse(
        dag_id=request.dag_id,
        dag_run_id=request.dag_run_id,
        state="success",
        failed_tasks=0,
        duration_seconds=14.2
    )

if __name__ == "__main__":
    mcp.run()
```

## API examples

### Python Airflow REST Client & Pydantic v2 Schema Verification
The following script illustrates direct interaction with the Airflow v3.1 REST API, validating responses using strict **Pydantic v2** models (`extra="forbid"`, `frozen=True`):

```python
import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, ConfigDict, Field

class DagRunDetail(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    dag_id: str
    dag_run_id: str
    logical_date: str
    state: str
    conf: Dict[str, Any] = Field(default_factory=dict)

def parse_dag_run_response(raw_json: str) -> DagRunDetail:
    """Parses and validates Airflow v3.1 API response payload."""
    data = json.loads(raw_json)
    return DagRunDetail.model_validate(data)

if __name__ == "__main__":
    sample_api_response = json.dumps({
        "dag_id": "daily_rag_indexing",
        "dag_run_id": "manual__2027-01-07T12:00:00+00:00",
        "logical_date": "2027-01-07T12:00:00Z",
        "state": "running",
        "conf": {"batch_size": 100}
    })
    validated = parse_dag_run_response(sample_api_response)
    print("Parsed DagRun:", validated.dag_id, "State:", validated.state)
```

## Production Operational Hardening

When running Apache Airflow v3.1 at scale in enterprise production, follow these operational best practices:

1. **API Server Isolation**: Expose only the decoupled Airflow v3.1 API Server to external networks; keep the Scheduler, Celery Workers, and PostgreSQL metadata database within private VPC subnets.
2. **Database Connection Pooling**: Configure PgBouncer in front of PostgreSQL to prevent worker connection exhaustion during large task bursts across Kubernetes clusters.
3. **DAG Parsing Performance**: Set `min_file_process_interval` and avoid top-level heavy code execution (e.g. database connections or network requests) inside DAG Python files to keep parsing latencies under 1 second.
4. **Task Resource Caching & Cleanup**: Enable automated log cleanup utilities and configure pod garbage collection policies when using `KubernetesExecutor` to clean up completed task pods.

## Diagnostic & Troubleshooting Matrix

| Operational Symptom | Root Cause Analysis | Remediation Strategy |
| :--- | :--- | :--- |
| **DAG Parsing Delays (>5s)** | Top-level network or DB queries executing inside DAG file evaluation loop. | Refactor heavy imports or network calls inside task Python functions. |
| **Celery Worker Disconnections** | Redis broker connection exhaustion or worker OOM. | Deploy PgBouncer connection pooler and increase worker RAM limits in Helm values. |
| **FastMCP API Server 401** | Stale JWT authentication token or missing API Server extra header. | Refresh JWT token using `airflow connections` CLI and verify API gateway. |
| **Edge Executor Sync Lag** | Network jitter between edge worker node and central Airflow API server. | Tune `edge_heartbeat_interval` parameter and configure retry buffers. |
| **DB Lock Contention** | Excessive concurrent task state writes during large batch triggers. | Adjust `max_active_runs_per_dag` and increase PostgreSQL `max_connections`. |
| **Zombied Task Instances** | Worker node killed by OS kernel OOM-killer without sending heartbeat. | Allocate swap memory or set stricter Docker memory limits with cgroup alerts. |
| **Log Ingestion Loss** | Decoupled API server unable to fetch remote log storage bucket credentials. | Verify IAM role or S3/GCS bucket IAM policies in Airflow connection config. |
| **Scheduler Heartbeat Timeout** | Excessive thread locking in metadata DB transaction isolation level. | Switch PostgreSQL isolation level to `READ COMMITTED` and scale DB CPU cores. |

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
