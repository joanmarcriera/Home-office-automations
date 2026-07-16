# Dagster

Dagster is an orchestrator designed for the development, production, and observation of data assets. Unlike task-based orchestrators, Dagster focuses on the **Data Asset**—the persistent object (table, file, model) produced by a computation. As of July 2026, **v1.9.12** is the stable release, featuring enhanced **Declarative Automation**, deep support for asset-centric orchestration in agentic data pipelines, and native **MCP 3.0** Task Protocol integration.

## What it is
Dagster is a data orchestrator that treats data assets as first-class citizens. It provides a global asset graph that tracks lineage, metadata, and data quality across the entire platform. By shifting from imperative "jobs" to declarative "assets," Dagster allows teams to define *what* data should exist and *when* it should be updated based on freshness policies.

## What problem it solves
It solves the "black box" pipeline problem where the relationship between code and data is obscured. Dagster provides a unified control plane that eliminates brittle cron schedules, replacing them with intelligent, lineage-aware automation. It ensures data quality via integrated asset checks and provides a rich development environment that matches production parity.

## Where it fits in the stack
**Orchestration / Data Asset Management**. It serves as the coordination layer for the modern data stack, sitting above transformation tools (dbt, SQLMesh) and below BI or AI consumption layers. In July 2026, it is a primary orchestrator for **Agentic Data Engineering**, where agents like [Claude 5.1](../../tools/ai_knowledge/claude-macos.md) or [Gemma 3](../../tools/ai_knowledge/gemini-macos.md) interact with the Dagster asset graph via [MCP 3.0](../automation_orchestration/mcp.md).

## Typical use cases
- **Declarative Asset Materialization**: Automatically updating downstream tables as soon as upstream raw data is available or after specific time intervals.
- **Data Quality Observability**: Running automated asset checks (row counts, null checks, schema validation) as part of the orchestration loop.
- **Agentic Data Pipelines**: Using AI agents to define, materialise, and debug assets based on natural language requirements.
- **Multi-Cloud Orchestration**: Executing code in external environments (Kubernetes, AWS Lambda, Databricks) via **Dagster Pipes** while maintaining central visibility.

## Strengths
- **Asset-Centric Architecture**: Lineage and state are tracked at the asset level, simplifying debugging and auditing.
- **Declarative Automation**: High-level policies define data freshness, reducing manual scheduling overhead.
- **MCP 3.0 Native**: Exposes the asset graph as tools for AI agents, enabling autonomous data management.
- **Development Productivity**: Rich local UI (Dagster+ or Open Source) with integrated testing and mocking capabilities.
- **v1.9+ Features**: Stable Declarative Automation, BI tool integrations (PowerBI, Tableau), and enhanced Pydantic 2.5 support.

## Limitations
- **Python-Heavy**: Requires a strong understanding of Python and decorators for defining assets.
- **Resource Usage**: The webserver and daemon require dedicated resources for persistent monitoring.
- **Complexity for Simple Tasks**: May be overkill for basic, non-data-intensive automation where [Prefect](prefect.md) or [Kestra](kestra.md) might be lighter.

## When to use it
- You are building a data platform and want to manage data as a collection of version-controlled assets.
- You need high visibility into data lineage and automated data quality checks.
- You want to use declarative policies to automate materialization across complex dependency trees.
- You are building AI systems that need to reason about and interact with a structured data graph.

## When not to use it
- For simple, isolated script execution where task-based logic (Airflow/Prefect) is sufficient.
- If you are restricted from using Python as the primary language for pipeline definition.
- For low-latency event processing where a streaming engine (Flink) is required.

## Getting started

### Installation
```bash
pip install dagster dagster-webserver
```

### Basic Asset Example
Define assets in `my_assets.py`:
```python
from dagster import asset, AutomationCondition

@asset
def raw_data():
    return [1, 2, 3]

@asset(
    automation_condition=AutomationCondition.on_missing(),
    deps=[raw_data]
)
def processed_data(raw_data):
    return [x * 10 for x in raw_data]
```

### Start the Webserver
```bash
dagster dev -f my_assets.py
```
Access the UI at `http://localhost:3000`.

## CLI examples
The `dagster` CLI handles deployments, backfills, and asset management.

```bash
# List all assets in the current workspace
dagster asset list

# Trigger a materialization for specific assets
dagster asset materialize --asset raw_data --asset processed_data

# Launch a backfill for a partitioned asset
dagster job backfill --job my_partitioned_job --partitions 2026-07-01,2026-07-21

# Verify the health of the Dagster daemon
dagster-daemon health_check

# Register Dagster assets as MCP tools (v1.9.12+)
dagster mcp register --server localhost:3000
```

## API examples
Dagster provides a GraphQL API and a Python Client for programmatic interaction.

```python
from dagster_graphql import DagsterGraphQLClient

client = DagsterGraphQLClient("localhost", port_number=3000)

# Trigger a materialization via the GraphQL Client
client.submit_job_execution(
    job_name="materialize_all_assets_job",
    repository_location_name="my_location",
    repository_name="my_repo"
)
```

**Using Declarative Automation (July 2026):**
```python
from dagster import AutomationCondition, asset

@asset(automation_condition=AutomationCondition.eager())
def highly_reactive_asset():
    """This asset materializes immediately when upstream changes."""
    return "New Data"
```

## Related tools / concepts
- [Apache Airflow](apache-airflow.md) — The traditional task-based alternative.
- [Apache Hamilton](apache-hamilton.md) — For micro-orchestration within Dagster assets.
- [Prefect](prefect.md) — A dynamic, Python-native orchestrator.
- [Kestra](kestra.md) — Declarative YAML orchestration with MCP support.
- [Flyte](flyte.md) — Kubernetes-native ML orchestration.
- [MCP](../automation_orchestration/mcp.md) — The protocol used to expose Dagster to AI agents.
- [n8n](../../services/n8n.md) — For low-code intake and alerting.
- [Claude 5.1](../../tools/ai_knowledge/claude-macos.md) — Frontier model for orchestrating Dagster assets.
- [Gemma 3](../../tools/ai_knowledge/gemini-macos.md) — Lightweight model for asset check logic.
- [Pydantic](../../tools/development_ops/pydantic.md) — Used for asset metadata and configuration.

## Sources / references
- [Dagster Official Documentation](https://docs.dagster.io/)
- [Dagster 1.9 Release: Asset-First Orchestration](https://dagster.io/blog/dagster-1-9)
- [MCP 3.0 Specification](https://modelcontextprotocol.io/)
- [GitHub Repository](https://github.com/dagster-io/dagster)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
