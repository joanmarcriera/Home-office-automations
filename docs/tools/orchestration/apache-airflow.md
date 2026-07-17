# Apache Airflow

Apache Airflow is an open-source platform for authoring, scheduling, and monitoring workflows as Python-defined DAGs. As of July 2026, **Airflow 3.0.x** is the established major release, introducing a service-oriented architecture, event-driven scheduling, dynamic orchestrating parameters via Gemma 3/Claude 5.1, and native support for the **Model Context Protocol (MCP 3.0)**.

## What it is
Apache Airflow is a workflow orchestration platform that allows users to programmatically author, schedule, and monitor workflows. Workflows are defined as Directed Acyclic Graphs (DAGs) in Python, providing a flexible, version-controlled, and highly extensible way to manage complex task dependencies and data-driven pipelines.

## What problem it solves
Airflow turns fragile, manual, or scattered operational processes into robust, versioned workflow code with built-in scheduling, retries, detailed logging, and centralized monitoring. It solves the challenges of coordinating complex dependencies and multi-stage tasks across diverse systems and multi-cloud environments, ensuring data lineage, auditing, and platform stability.

## Where it fits in the stack
**Orchestration / Enterprise Workflow Platform**. It serves as the central coordination control plane for modern data stacks and agentic pipelines. It acts as the "orchestra conductor," coordinating between ingestion engines, transformation layers (like dbt or sqlglot), ML stacks, and autonomous AI agents.

## Typical use cases
- **AI Inference & Agentic Orchestration**: Scheduling and managing multi-step agent reasoning loops with [Claude 5.1](../ai_knowledge/claude-macos.md) or [Gemma 3](../ai_knowledge/gemini-macos.md) where tasks are dynamically generated or selected.
- **Event-Driven Pipelines**: Triggering downstream pipelines instantly when external data changes or message broker events occur, replacing traditional polling.
- **Distributed Edge Computing**: Utilizing the **Edge Executor** (AIP-69) to dispatch specialized, resource-intensive AI models or extraction tasks to remote agent nodes or GPU clusters.
- **Enterprise Data Processing**: Executing large-scale, automated ETL/ELT pipelines with compliance auditing, automated failure alerts, and cross-platform dependency resolution.

## Strengths
- **Service-Oriented Architecture (Airflow 3.0)**: Fully decoupled DAG parsing via an independent API Server, dramatically enhancing security, performance, and API-first capabilities.
- **Python-Native & Extensible**: Workflows are written as pure Python, facilitating software-engineering best practices such as unit testing, continuous integration (CI/CD), and Git-based versioning.
- **MCP 3.0 Integration**: Built-in support for the Model Context Protocol, enabling Airflow to register, discover, and run workflows directly as tools exposed to AI agents.
- **Vast Integration Ecosystem**: Hundreds of pre-built provider packages for integrating with cloud providers (AWS, GCP, Azure), database warehouses, vector storage, and ML tools.
- **Edge Executor Support**: Optimized for local or specialized hardware, enabling decentralized execution of complex inference or agentic skills on specialized hardware.

## Limitations
- **Operational Footprint**: Still requires a substantial infrastructure stack (PostgreSQL metadata database, Redis message broker, Celery/Kubernetes workers) to operate reliably at enterprise scale.
- **Latency Thresholds**: Primarily optimized for reliable batch execution and high-throughput pipelines; not designed for sub-millisecond, low-latency API request/response requirements.
- **Configuration Complexity**: The new service-oriented components in Airflow 3.0 require deeper DevOps expertise to configure, secure, and monitor than legacy monolithic versions.

## When to use it
- You need to coordinate complex, multi-stage workflows with strict audit logging, retry handling, and centralized monitoring.
- You want to express pipelines as Python code to maintain testability and continuous deployment compatibility.
- You are building hybrid AI workflows that combine standard data transformation with specialized GPU/agent execution.
- You want to expose your internal data or execution pipelines to autonomous agents via standard MCP 3.0 clients.

## When not to use it
- For simple, single-step scripts or basic Cron tasks that don't have complex dependencies.
- If you require real-time, low-latency streaming processing (see Apache Flink or specialized event processors).
- If you prefer a lightweight, purely declarative YAML/JSON configuration model for workflows (see [Kestra](kestra.md)).

## Getting started

### Docker Compose (Quickstart)
The fastest way to launch a local Airflow 3.0 sandbox:

```bash
# Download the official docker-compose file
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'

# Initialize the database and create default admin credentials
docker compose up airflow-init

# Start all Airflow services
docker compose up -d
```
Once healthy, access the administrative UI at `http://localhost:8080` (default username/password: `airflow`/`airflow`).

### Helm (Kubernetes Installation)
For production-grade deployments on Kubernetes:

```bash
helm repo add apache-airflow https://airflow.apache.org
helm upgrade --install airflow apache-airflow/airflow \
  --namespace airflow \
  --create-namespace \
  --set executor=CeleryExecutor
```

## CLI examples
The modern Airflow 3.0 CLI manages the lifecycle of pipelines, connections, and agentic servers.

```bash
# List all registered and active DAGs
airflow dags list

# Trigger a DAG run manually with runtime configuration parameters
airflow dags trigger agent_orchestrated_pipeline --conf '{"temperature": 0.2}'

# Test a single task instance locally without database state side effects
airflow tasks test agent_orchestrated_pipeline execute_reasoning 2026-07-21

# Query the state of a specific pipeline run
airflow dags state agent_orchestrated_pipeline 2026-07-21

# Register an Airflow DAG workflow as a Model Context Protocol tool (v3.0.x)
airflow mcp register --dag-id agent_orchestrated_pipeline --command "airflow" --args "dags trigger"
```

## API examples
Airflow 3.0 exposes a rich REST API and fully supports Python TaskFlow API decoration for agentic workflows.

### REST API Integration
Interact with the decoupled Airflow 3.0 API Server:

```bash
# Perform a service health check
curl -X GET "http://localhost:8080/api/v1/health" \
     -u "airflow:airflow"

# Programmatically trigger a DAG execution
curl -X POST "http://localhost:8080/api/v1/dags/agent_orchestrated_pipeline/dagRuns" \
     -u "airflow:airflow" \
     -H "Content-Type: application/json" \
     -d '{"conf": {"agent_model": "claude-5.1-sonnet"}}'
```

### Dynamic Agentic TaskFlow API Example
A clean Python example showing how to build an agentic workflow in Airflow 3.0 using the TaskFlow API and the **FastMCP 3.0** SDK to expose a task to an LLM:

```python
from airflow.decorators import dag, task
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# Define a FastMCP server to host our workflow tasks
mcp = FastMCP("airflow-agent")

@task
def extract_input_context() -> str:
    return "User query regarding system logs"

@task
def run_agent_reasoning(context: str) -> str:
    # Under-the-hood reasoning using Claude 5.1 or Gemma 3
    # Exposing Airflow-managed database context via MCP tool
    return f"Processed query: {context} with decision: APPROVE"

@dag(
    schedule_interval=None,
    start_date=datetime(2026, 7, 21),
    catchup=False,
    tags=["agentic", "mcp"]
)
def agentic_orchestrator():
    context = extract_input_context()
    decision = run_agent_reasoning(context)

# Instantiation
dag_instance = agentic_orchestrator()
```

## Related tools / concepts
- [Temporal](temporal.md) — For durable, stateful, long-running function orchestration.
- [Dagster](dagster.md) — Asset-centric data orchestration that treats tables and models as first-class citizens.
- [Prefect](prefect.md) — A highly dynamic, lightweight, and Python-native orchestration alternative.
- [Argo Workflows](argo-workflows.md) — Kubernetes-native containerized workflow and parallel job orchestrator.
- [Kestra](kestra.md) — Highly declarative, event-driven, YAML-based orchestrator with first-class agent support.
- [Flyte](flyte.md) — Container-native orchestrator optimized for massive-scale ML and data lifecycles.
- [ZenML](zenml.md) — Standardized MLOps abstraction layer that runs pipelines anywhere.
- [Apache Hamilton](apache-hamilton.md) — Micro-orchestration tool for defining clean, self-documenting dataflows.
- [n8n](../../services/n8n.md) — Low-code automation tool ideal for simple intake, alerts, and notifications.
- [Claude 5.1](../ai_knowledge/claude-macos.md) — Frontier LLM utilized for executing dynamic agentic pipeline tasks.
- [Gemma 3](../ai_knowledge/gemini-macos.md) — Lightweight, localized model optimized for executing task-level orchestration logic.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standard protocol used to seamlessly bridge workflows and AI agents.

## Sources / references
- [Official Apache Airflow 3.0 Documentation](https://airflow.apache.org/docs/apache-airflow/3.0.0/)
- [Astronomer: Airflow 3.0 Architecture Feature Guide](https://www.astronomer.io/blog/airflow-3/)
- [AIP-69: Edge Executor Specification](https://cwiki.apache.org/confluence/display/AIRFLOW/AIP-69+Edge+Executor)
- [Apache Airflow GitHub Repository](https://github.com/apache/airflow)
- [Model Context Protocol (MCP) specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
