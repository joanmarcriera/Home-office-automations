# Dagster

Dagster is an orchestrator designed for the development, production, and observation of data assets. Unlike task-based orchestrators, Dagster focuses on the **Data Asset**—the persistent object (table, file, model) produced by a computation. As of June 2026, **v1.9.x** is the stable release, featuring enhanced **Declarative Automation** and deep support for asset-centric orchestration in agentic data pipelines.

## What it is
Dagster is a data orchestrator that treats data assets as first-class citizens. It provides a global asset graph that tracks lineage, metadata, and data quality across the entire platform, moving beyond simple task scheduling to intelligent asset management.

## What problem it solves
It solves the problem of "black box" data pipelines where the relationship between code and data is obscured. By focusing on assets, Dagster ensures that developers know exactly which data objects are being updated and why. It replaces brittle cron schedules with a declarative approach to data freshness and reliability.

## Where it fits in the stack
**Orchestration / Data Asset Management**. It serves as the control plane for data platforms, coordinating work between warehouses, lakes, BI tools, and AI models. It sits above the transformation layer (like dbt) and provides a unified observability interface.

## Typical use cases
- **Declarative Asset Materialization**: Automatically updating downstream tables as soon as upstream raw data is available.
- **Data Quality Observability**: Running asset checks and monitoring data freshness as part of the orchestration loop.
- **Agentic Data Pipelines**: Using AI agents (Claude 4.8) to define and materialise assets based on natural language queries.
- **Dagster Pipes**: Executing code in external environments (Kubernetes, AWS Lambda, Databricks) while maintaining visibility in the Dagster UI.

## Strengths
- **Asset-Centric Architecture**: Lineage and state are tracked at the asset level, simplifying debugging and auditing.
- **Declarative Automation**: Define *what* data should be fresh rather than *when* a job should run.
- **Development Productivity**: Rich local development environment with a powerful UI and integrated testing tools.
- **v1.9 Features**: Stable Declarative Automation, BI tool integrations, and enhanced Pydantic 2.0 support.
- **Agent-Ready**: Exposes a structured asset graph that AI agents can reason about for automated data engineering.

## Limitations
- **Python-Heavy**: Requires a strong understanding of Python for defining assets and complex configurations.
- **Resource Usage**: The webserver and daemon require dedicated resources for monitoring and scheduling.
- **Complexity for Simple Tasks**: Might be overkill for basic script execution without persistent data assets.

## When to use it
- You are building a modern data platform and want to manage data as a collection of assets.
- You need high visibility into data lineage and data quality.
- You want to use declarative policies to automate data materialization.
- You are building AI systems that need to interact with a structured data graph.

## When not to use it
- For simple, non-data-intensive automation where task-based logic is sufficient (use Airflow or Prefect).
- If you are restricted from using Python as the primary language for orchestration.
- For low-latency event processing (use a streaming engine).

## Getting started

### Installation
```bash
pip install dagster dagster-webserver
```

### Basic Asset Example
Define an asset in `my_assets.py`:
```python
from dagster import asset

@asset
def raw_data():
    return [1, 2, 3]

@asset
def processed_data(raw_data):
    return [x * 10 for x in raw_data]
```

### Start the Webserver
```bash
dagster dev -f my_assets.py
```
Access the UI at `http://localhost:3000`.

## CLI examples
The `dagster` CLI is used for managing deployments, backfills, and local development.

```bash
# List all assets in a workspace
dagster asset list

# Trigger a materialization for specific assets
dagster asset materialize --asset raw_data --asset processed_data

# Launch a backfill for a partitioned asset
dagster job backfill --job my_partitioned_job --partitions 2026-06-01,2026-06-21

# Verify the health of the Dagster daemon
dagster-daemon health_check
```

## API examples
Dagster provides a GraphQL API for programmatic interaction with the asset graph.

```bash
# Trigger a materialization via GraphQL (cURL example)
curl -X POST http://localhost:3000/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { launchAssetMaterialization(assetKey: {path: [\"processed_data\"]}) { __typename ... on LaunchAssetMaterializationSuccess { runId } } }"
  }'
```

**Using Declarative Automation (v1.9):**
```python
from dagster import AutomationCondition, asset

@asset(automation_condition=AutomationCondition.on_missing())
def my_automated_asset():
    return "Automated data"
```

## Related tools / concepts
- [Apache Airflow](apache-airflow.md) — The traditional task-based alternative.
- [Apache Hamilton](apache-hamilton.md) — For micro-orchestration within Dagster assets.
- [Prefect](prefect.md) — A dynamic, Python-native orchestrator.
- [Temporal](temporal.md) — For durable, stateful function orchestration.
- [Kestra](kestra.md) — Declarative YAML orchestration.
- [Flyte](flyte.md) — Kubernetes-native ML orchestration.
- [n8n](../../services/n8n.md) — For low-code intake and alerting.

## Sources / references
- [Dagster Official Documentation](https://docs.dagster.io/)
- [Dagster 1.9 Release Blog](https://dagster.io/blog/dagster-1-9-spooky)
- [Declarative Automation Guide](https://docs.dagster.io/guides/automate/declarative-automation)
- [GitHub Repository](https://github.com/dagster-io/dagster)

## Contribution Metadata
- Last reviewed: 2026-06-21
- Confidence: high
