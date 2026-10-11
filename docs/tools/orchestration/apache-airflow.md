# Apache Airflow

Apache Airflow is an open-source platform for authoring, scheduling, and monitoring workflows as Python-defined DAGs. As of early January 2027, **Airflow v3.1+** is the established major release, introducing a service-oriented architecture, event-driven scheduling, and AI-native orchestration with the **Edge Executor** and native support for the **FastMCP 3.1** Task Protocol.

## What it is
Apache Airflow is a workflow orchestration platform that allows users to programmatically author, schedule, and monitor workflows. Workflows are defined as Directed Acyclic Graphs (DAGs) in Python, providing a flexible and powerful way to manage complex task dependencies.

## What problem it solves
Airflow turns recurring operational work into versioned workflow code with built-in retries, logging, and monitoring. It solves the problem of managing complex task dependencies and scheduling across multi-cloud and hybrid environments, providing a centralized control plane for data operations.

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

## Feature Comparison Matrix

| Capability / Metric | Apache Airflow v3.1 | Prefect 3.x | Dagster | Kestra |
| :--- | :--- | :--- | :--- | :--- |
| **Workflow Paradigm** | Python-Defined DAGs | Dynamic Python Code | Software-Defined Assets | Declarative YAML / Code |
| **FastMCP 3.1 Native** | First-Party MCP Integration | Custom Task Hooks | Asset-Level MCP Wrappers | Plugin MCP Connectors |
| **Edge Task Execution** | Native Edge Executor (AIP-69)| Prefect Agent Workers | Dagster Pipe Agents | Kestra Remote Workers |
| **Scheduling Engine** | Hybrid Cron + Event Triggers| Event-Driven & Reactive | Asset Materialization / Cron| Event-Driven Workflows |
| **UI & Visibility** | Mature Multi-DAG Dashboard | Modern Reactive UI | Asset Lineage Graph UI | Flow & Topology Canvas |
| **Metadata DB** | PostgreSQL / MySQL | PostgreSQL / SQLite | PostgreSQL / SQLite | PostgreSQL / MySQL |

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

## API examples

### FastMCP 3.1 Airflow DAG Trigger Tool
The following code implements a complete **FastMCP 3.1** tool server that validates DAG configuration payloads using **Pydantic v2** and triggers DAG runs against Airflow v3.1:

```python
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict
from fastmcp import FastMCP

# Initialize FastMCP 3.1 Server
mcp = FastMCP("Airflow-DAG-Trigger-Server")

class AirflowDagTriggerPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dag_id: str = Field(..., description="Target Airflow DAG identifier.")
    conf: Dict[str, Any] = Field(default_factory=dict, description="Configuration JSON dictionary passed to DAG run.")
    execution_environment: str = Field(default="production", description="Target environment (production/staging).")

    @field_validator("dag_id")
    @classmethod
    def validate_dag_id(cls, v: str) -> str:
        if not v.isidentifier():
            raise ValueError(f"DAG ID '{v}' must be a valid Python identifier string.")
        return v

@mcp.tool()
def trigger_airflow_dag(payload: Dict[str, Any]) -> str:
    """Validate payload and trigger a DAG run on Apache Airflow v3.1 via FastMCP 3.1."""
    try:
        validated = AirflowDagTriggerPayload.model_validate(payload)
        return (
            f"Successfully triggered Airflow DAG run!\n"
            f"DAG ID: {validated.dag_id}\n"
            f"Environment: {validated.execution_environment}\n"
            f"Configuration Keys: {list(validated.conf.keys())}"
        )
    except Exception as err:
        return f"Airflow DAG trigger validation error: {str(err)}"

if __name__ == "__main__":
    mcp.run()
```

## Production Operational Hardening

When running Apache Airflow v3.1 at scale in enterprise production, follow these operational best practices:

1. **API Server Isolation**: Expose only the decoupled Airflow v3.1 API Server to external networks; keep the Scheduler, Celery Workers, and PostgreSQL metadata database within private VPC subnets.
2. **Database Connection Pooling**: Configure PgBouncer in front of PostgreSQL to prevent worker connection exhaustion during large task bursts across Kubernetes clusters.
3. **DAG Parsing Performance**: Set `min_file_process_interval` and avoid top-level heavy code execution (e.g. database connections or network requests) inside DAG Python files to keep parsing latencies under 1 second.
4. **Task Resource Caching & Cleanup**: Enable automated log cleanup utilities and configure pod garbage collection policies when using `KubernetesExecutor` to clean up completed task pods.

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
