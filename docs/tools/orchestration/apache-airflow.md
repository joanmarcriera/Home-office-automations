# Apache Airflow

Apache Airflow is an open-source platform for authoring, scheduling, and monitoring workflows as Python-defined DAGs. As of December 2026, **Airflow v3.1+** is the established major release, introducing a service-oriented architecture, event-driven scheduling, and AI-native orchestration with the **Edge Executor** and native support for the **FastMCP 3.1** Task Protocol.

## What it is
Apache Airflow is a workflow orchestration platform that allows users to programmatically author, schedule, and monitor workflows. Workflows are defined as Directed Acyclic Graphs (DAGs) in Python, providing a flexible and powerful way to manage complex task dependencies.

## What problem it solves
Airflow turns recurring operational work into versioned workflow code with built-in retries, logging, and monitoring. It solves the problem of managing complex task dependencies and scheduling across multi-cloud and hybrid environments, providing a centralized control plane for data operations.

## Where it fits in the stack
**Orchestration / Enterprise Workflow Platform**. It serves as the "brain" for batch and event-driven data operations. It coordinates between data ingestion, transformation (dbt), and AI/ML model execution layers. In late November/December 2026, it is a primary orchestrator for agentic workflows, coordinating model execution with AI agents like [Claude 5.1](../ai_knowledge/claude-macos.md), [GPT-5.5](../ai_knowledge/gpt-model.md), [Gemini 4.0 Pro](../ai_knowledge/gemini-macos.md), [Llama 4](../ai_knowledge/llama.md), [Gemma 3](../ai_knowledge/gemini-macos.md), or [Qwen 3.6](../ai_knowledge/qwen.md) and extending capability via [FastMCP 3.1](../automation_orchestration/mcp.md).

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
Airflow v3.1 relies heavily on its REST API for integration.

```bash
# Health check via API Server
curl -X GET "http://localhost:8080/api/v1/health" \
     -u "airflow:airflow"

# Trigger a DAG run with configuration JSON
curl -X POST "http://localhost:8080/api/v1/dags/my_dag_id/dagRuns" \
     -u "airflow:airflow" \
     -H "Content-Type: application/json" \
     -d '{"conf": {"input_path": "s3://bucket/data.csv"}}'
```

### DAG Run Context Validation with Strict Pydantic v2 Schema
The following robust Python example uses **Pydantic v2** to programmatically validate incoming DAG run configuration payloads before parsing them in an Airflow task, guaranteeing robust typing and preventing runtime errors on execution.

```python
import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ValidationError, model_validator

# 1. Define Airflow DAG configuration schema
class AirflowDagConfig(BaseModel):
    batch_id: str = Field(..., pattern="^batch-[0-9]+$")
    environment: str = Field(..., pattern="^(development|staging|production)$")
    model_preferences: List[str] = Field(default_factory=lambda: ["gpt-5.5", "claude-5.1"])
    max_active_runs: int = Field(default=5, ge=1, le=20)
    meta_parameters: Optional[Dict[str, Any]] = None

    @model_validator(mode="after")
    def check_prod_restrictions(self) -> "AirflowDagConfig":
        if self.environment == "production" and self.max_active_runs > 10:
            raise ValueError("Production runs are capped at a maximum of 10 concurrent active runs for stability.")
        return self

# 2. Example representation of Airflow dynamic DagRun conf payload
raw_conf = {
    "batch_id": "batch-347",
    "environment": "production",
    "model_preferences": ["claude-5.1", "qwen-3.6", "gemma-3"],
    "max_active_runs": 8,
    "meta_parameters": {"retries": 3, "timeout": 300}
}

# 3. Validate conf payload using Pydantic v2
try:
    validated_conf = AirflowDagConfig.model_validate(raw_conf)
    print("Airflow DagRun configuration is valid!")
    print(f"Target Environment: {validated_conf.environment}")
    print(f"Models selected: {', '.join(validated_conf.model_preferences)}")
except ValidationError as e:
    print(f"Airflow Configuration Validation failed with errors: {e.json()}")
```

## Related tools / concepts
- [Temporal](temporal.md) — For durable, stateful function orchestration.
- [Dagster](dagster.md) — Asset-centric data orchestration.
- [Prefect](prefect.md) — Dynamic Python workflows.
- [Argo Workflows](argo-workflows.md) — Kubernetes-native container orchestration.
- [Kestra](kestra.md) — Declarative YAML orchestration.
- [Flyte](flyte.md) — Large-scale ML orchestration.
- [Apache Hamilton](apache-hamilton.md) — For micro-orchestration within tasks.
- [n8n](../../services/n8n.md) — For low-code intake and simple automation.
- [Claude 5.1](../ai_knowledge/claude-macos.md) — For agentic workflow control and synthesis.
- [GPT-5.5](../ai_knowledge/gpt-model.md) — Frontier model for complex enterprise logical workflows.
- [Gemini 4.0 Pro](../ai_knowledge/gemini-macos.md) — SOTA model.
- [Llama 4](../ai_knowledge/llama.md) — Advanced open model.
- [Gemma 3](../ai_knowledge/gemini-macos.md) — Lightweight, localized reasoner for DAG dynamic parameters.
- [Qwen 3.6](../ai_knowledge/qwen.md) — High-quality reasoning open model.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Protocol for model and tool integration.

## Sources / references
- [Official Airflow v3.1 Documentation](https://airflow.apache.org/docs/apache-airflow/stable/)
- [Astronomer: Airflow v3 Feature Guide](https://www.astronomer.io/blog/airflow-3/)
- [AIP-69: Edge Executor](https://cwiki.apache.org/confluence/display/AIRFLOW/AIP-69+Edge+Executor)
- [Apache Airflow GitHub](https://github.com/apache/airflow)

## Contribution Metadata
- Last reviewed: 2026-12-26
- Confidence: high
