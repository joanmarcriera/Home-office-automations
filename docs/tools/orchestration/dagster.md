# Dagster

## What it is
Dagster is an orchestrator designed for the development, production, and observation of data assets. Unlike task-based orchestrators, Dagster focuses on the **Data Asset**—the persistent object (table, file, model) produced by a computation. As of May 2026, **v1.9.x** is the current stable release, featuring **Declarative Automation** and enhanced BI tool integrations.

## What problem it solves
It solves the problem of "black box" data pipelines. By making assets first-class citizens, Dagster provides a global asset graph that tracks lineage, metadata, and data quality across the entire platform. It replaces complex, hard-to-maintain cron schedules with intelligent, event-based orchestration.

## Where it fits in the stack
**Orchestration / Data Asset Management**. It serves as the control plane for data platforms, integrating with warehouses, lakes, and BI tools.

## Typical use cases
- **Declarative Asset Materialization**: Automatically updating downstream tables as soon as upstream raw data is available.
- **Data Quality Observability**: Running asset checks and monitoring data freshness as part of the orchestration loop.
- **BI Orchestration**: Integrating with Looker, Power BI, and Tableau to ensure dashboards reflect the latest data.
- **Dagster Pipes**: Executing code in external environments (Kubernetes, AWS Lambda, Databricks) while maintaining visibility in the Dagster UI.

## Strengths
- **Asset-Centric**: Lineage and state are tracked at the asset level, making it easy to see *what* data was produced and *how*.
- **Declarative Automation**: High-level policies define *when* data should be updated, rather than manually scheduling jobs.
- **Development Productivity**: Rich local development environment with a powerful UI (Dagster+ or open-source webserver).
- **v1.9 Features**: Stable Declarative Automation, BI tool integrations, and Pydantic 2.0 support.

## Limitations
- **Python-Heavy**: Requires a strong understanding of Python for defining assets and configurations.
- **Resource Usage**: The webserver and daemon require dedicated resources for monitoring and scheduling.
- **Complexity for Simple Tasks**: Might be overkill for basic script execution without persistent data assets.

## When to use it
- You are building a modern data platform and want to manage data as a collection of assets.
- You need high visibility into data lineage and data quality.
- You want to use declarative policies to automate data materialization.

## When not to use it
- For simple, non-data-intensive automation where task-based logic is sufficient (use Airflow or Prefect).
- If you are restricted from using Python as the primary language for orchestration.

## Licensing and cost
- **Open Source**: Yes (Apache License 2.0)
- **Cost**: Free self-hosted; paid managed offerings (Dagster+).
- **Self-hostable**: Yes

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
dagster job backfill --job my_partitioned_job --partitions 2026-05-01,2026-05-31

# Verify the health of the Dagster daemon
dagster-daemon health_check
```

## Python examples
Using **Declarative Automation** in v1.9:

```python
from dagster import AssetSpec, AutomationCondition, asset

@asset(automation_condition=AutomationCondition.on_missing())
def my_automated_asset():
    # This asset will automatically materialize if it doesn't exist
    return "Automated data"

@asset(automation_condition=AutomationCondition.eager())
def downstream_asset(my_automated_asset):
    # This will materialize as soon as the upstream is updated
    return my_automated_asset.upper()
```

## Related tools / concepts
- [Apache Airflow](apache-airflow.md) — The traditional task-based alternative.
- [Hamilton](apache-hamilton.md) — For micro-orchestration within Dagster assets.
- [dbt](../frameworks/index.md) — Deeply integrated with Dagster for SQL transformations.
- [Prefect](prefect.md) — A dynamic, Python-native orchestrator.
- [n8n](../../services/n8n.md) — For low-code intake and alerting.
- [Great Expectations](../benchmarking/index.md) — Often used alongside Dagster for data validation.

## Backlog
- [ ] Perform quarterly technical freshness audit.

## Contribution Metadata
- Last reviewed: 2026-05-31
- Confidence: high

## Sources / References
- [Dagster Official Documentation](https://docs.dagster.io/)
- [Dagster 1.9 Release Blog](https://dagster.io/blog/dagster-1-9-spooky)
- [Declarative Automation Guide](https://docs.dagster.io/guides/automate/declarative-automation)
- [GitHub Repository](https://github.com/dagster-io/dagster)
