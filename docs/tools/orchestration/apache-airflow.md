# Apache Airflow

## What it is
Apache Airflow is an open-source platform for authoring, scheduling, and monitoring workflows as Python-defined DAGs. As of May 2026, **Airflow 3.0** is the current major release, introducing a service-oriented architecture, event-driven scheduling, and first-class AI inference support.

## What problem it solves
Airflow turns recurring operational work into versioned workflow code with dependencies, schedules, retries, logs, and a web UI. It coordinates complex data pipelines, model refreshes, and integration tasks across multi-cloud and hybrid environments.

## Where it fits in the stack
**Orchestration / Enterprise Workflow Platform**. It serves as the "brain" for batch and event-driven data operations.

## Typical use cases
- **AI Inference Execution**: Utilizing Airflow 3.0's synchronous DAG execution and ad-hoc scheduling for real-time model serving.
- **Event-Driven Pipelines**: Triggering workflows based on message queue events or external data changes rather than just time.
- **Distributed Edge Computing**: Using the **Edge Executor** to run tasks on remote devices outside the central data center.
- **Enterprise ETL/ELT**: Coordinating massive data movements between warehouses (Snowflake, BigQuery) and lakes.

## Strengths
- **Airflow 3.0 Architecture**: Decoupled DAG parsing from task execution via the new **API Server**, improving security and scalability.
- **Python-Native**: Workflows are code, enabling standard software engineering practices (Git, CI/CD, unit testing).
- **Extensive Ecosystem**: Over 100+ provider packages for nearly every modern data tool.
- **First-Class Backfills**: Managed by the scheduler with UI-based monitoring and control.

## Limitations
- **Operational Footprint**: Airflow 3.0 reduces but does not eliminate the need for a robust infrastructure (PostgreSQL, Redis, Workers).
- **Latency**: While improved in 3.0, it is still primarily designed for throughput rather than sub-millisecond real-time response.
- **Complexity**: The shift to a service-oriented architecture adds new components (API Server) to manage.

## When to use it
- You need to orchestrate complex, multi-step workflows with strict audit and retry requirements.
- You want to leverage a mature ecosystem with enterprise-grade security and monitoring.
- You are building AI/ML pipelines that require reliable data preparation and model refresh cycles.

## When not to use it
- For very simple, single-step scripts where a cron job or a basic Python script suffices.
- If you require ultra-low latency request/response handling (consider a dedicated API framework).

## Licensing and cost
- **Open Source**: Yes (Apache License 2.0)
- **Cost**: Free self-hosted; paid managed offerings (Astronomer, AWS MWAA, Google Cloud Composer).
- **Self-hostable**: Yes

## Getting started

### Docker Compose (Quickstart)
The fastest way to run Airflow 3.0 locally is using the official community Docker Compose file.

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
For production-grade self-hosting on K3s or EKS:

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
airflow tasks state my_inference_pipeline my_task_id 2026-05-31

# Test a single task instance without running the full DAG
airflow tasks test my_dag_id my_task_id 2026-05-31
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
- [Dagster](dagster.md) — For data-asset-centric orchestration.
- [Prefect](prefect.md) — For dynamic, Python-native workflows.
- [Argo Workflows](argo-workflows.md) — For Kubernetes-native container orchestration.
- [Kestra](kestra.md) — For event-driven declarative orchestration.
- [Flyte](flyte.md) — For large-scale machine learning workflows.
- [n8n](../../services/n8n.md) — For low-code automation and intake.
- [Prometheus](../benchmarking/index.md) — For monitoring Airflow metrics.
- [OpenTelemetry](../benchmarking/index.md) — For distributed tracing in Airflow 3.0.

## Backlog
- [x] Perform quarterly technical freshness audit. (Completed: 2026-05-31)

## Contribution Metadata
- Last reviewed: 2026-05-31
- Confidence: high

## Sources / References
- [Official Airflow 3.0 Documentation](https://airflow.apache.org/docs/apache-airflow/3.0.0/)
- [Astronomer: Airflow 3.0 Feature Guide](https://www.astronomer.io/blog/airflow-3/)
- [AIP-69: Edge Executor](https://cwiki.apache.org/confluence/display/AIRFLOW/AIP-69+Edge+Executor)
