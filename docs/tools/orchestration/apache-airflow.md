# Apache Airflow

Apache Airflow is an open-source platform for authoring, scheduling, and monitoring workflows as Python-defined DAGs. As of June 2026, **Airflow 3.0.x** is the established major release, introducing a service-oriented architecture, event-driven scheduling, and AI-native orchestration with the **Edge Executor**.

## What it is
Apache Airflow is a workflow orchestration platform that allows users to programmatically author, schedule, and monitor workflows. Workflows are defined as Directed Acyclic Graphs (DAGs) in Python, providing a flexible and powerful way to manage complex task dependencies.

## What problem it solves
Airflow turns recurring operational work into versioned workflow code with built-in retries, logging, and monitoring. It solves the problem of managing complex task dependencies and scheduling across multi-cloud and hybrid environments, providing a centralized control plane for data operations.

## Where it fits in the stack
**Orchestration / Enterprise Workflow Platform**. It serves as the "brain" for batch and event-driven data operations. It coordinates between data ingestion, transformation (dbt), and AI/ML model execution layers.

## Typical use cases
- **AI Inference Execution**: Utilizing Airflow 3.0's synchronous DAG execution and ad-hoc scheduling for real-time model serving.
- **Event-Driven Pipelines**: Triggering workflows based on external data changes or message queue events.
- **Distributed Edge Computing**: Using the **Edge Executor** to run AI-native orchestration tasks on remote devices or specialized agent nodes.
- **Enterprise ETL/ELT**: Coordinating massive data movements between warehouses and lakes with strict audit requirements.

## Strengths
- **Airflow 3.0 Architecture**: Decoupled DAG parsing from task execution via a new API Server, improving security and performance.
- **Python-Native**: Workflows are defined as code, enabling standard software engineering practices like Git, CI/CD, and unit testing.
- **Extensive Ecosystem**: Over 100+ provider packages for nearly every modern data and AI tool.
- **Mature Monitoring**: Comprehensive UI for tracking task progress, viewing logs, and managing retries.
- **Edge Executor**: Optimized for running tasks on decentralized infrastructure, ideal for agentic workflows.

## Limitations
- **Operational Footprint**: Requires a robust infrastructure (PostgreSQL, Redis, Workers) to run at scale.
- **Latency**: Primarily designed for throughput; not suitable for sub-millisecond real-time response requirements.
- **Complexity**: The service-oriented architecture of Airflow 3.0 adds new components to manage compared to previous versions.

## When to use it
- You need to orchestrate complex, multi-step workflows with strict audit and retry requirements.
- You want to leverage a mature ecosystem with enterprise-grade security.
- You are building AI/ML pipelines that require reliable data preparation.
- You need to run tasks on remote or specialized hardware via the Edge Executor.

## When not to use it
- For very simple, single-step scripts where a cron job suffices.
- If you require ultra-low latency request/response handling.
- If you want a purely declarative YAML-based orchestrator (see [Kestra](kestra.md)).

## Getting started

### Docker Compose (Quickstart)
The fastest way to run Airflow 3.0 locally:

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
airflow tasks state my_inference_pipeline my_task_id 2026-06-21

# Test a single task instance
airflow tasks test my_dag_id my_task_id 2026-06-21
```

## API examples
Airflow 3.0 relies heavily on its REST API for integration.

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

## Related tools / concepts
- [Temporal](temporal.md) — For durable, stateful function orchestration.
- [Dagster](dagster.md) — Asset-centric data orchestration.
- [Prefect](prefect.md) — Dynamic Python workflows.
- [Argo Workflows](argo-workflows.md) — Kubernetes-native container orchestration.
- [Kestra](kestra.md) — Declarative YAML orchestration.
- [Flyte](flyte.md) — Large-scale ML orchestration.
- [n8n](../../services/n8n.md) — For low-code intake and simple automation.

## Sources / references
- [Official Airflow 3.0 Documentation](https://airflow.apache.org/docs/apache-airflow/3.0.0/)
- [Astronomer: Airflow 3.0 Feature Guide](https://www.astronomer.io/blog/airflow-3/)
- [AIP-69: Edge Executor](https://cwiki.apache.org/confluence/display/AIRFLOW/AIP-69+Edge+Executor)
- [Apache Airflow GitHub](https://github.com/apache/airflow)

## Contribution Metadata
- Last reviewed: 2026-06-21
- Confidence: high
