# Dagster

Dagster is an open-source orchestrator designed for the development, production, and observation of data assets. Unlike traditional task-based orchestrators, Dagster focuses on the **Data Asset**—the persistent object (such as a database table, cloud storage file, or trained model) produced by a computation. As of early January 2027, **v1.9.12+** is the established production standard, introducing enhancements to its **Declarative Automation** engine, deep metadata integration for agentic data pipelines, and full **FastMCP 3.1** Task Protocol compatibility.

## What it is
Dagster is a data orchestrator that treats data assets as first-class citizens. By focusing on asset lineage, schemas, and data quality checks rather than raw task executions, Dagster enables teams to define *what* data should exist and *when* it should be materialized based on logical freshness policies.

## What problem it solves
It clarifies the relationship between computational code and the resulting data assets, resolving the "black box" pipeline issue. Dagster provides a unified control plane that reduces reliance on complex cron schedules, replacing them with declarative, lineage-aware materialization. Additionally, its native asset checks ensure data quality, and its testing utilities help maintain parity between local development and production environments.

## Where it fits in the stack
**Orchestration / Data Asset Management**. It serves as the coordination layer for modern data platforms, sitting above data transformation tools (dbt, SQLMesh, Spark) and below business intelligence (BI) or AI consumer applications. It is frequently employed as an orchestrator for **Agentic Data Engineering**, where reasoning models like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Gemma 4**, **DeepSeek-V4**, and **Qwen 3.6 VL** interact with the Dagster asset graph via [FastMCP 3.1 Task Protocol](../automation_orchestration/mcp.md).

## Typical use cases
- **Declarative Asset Materialization**: Automatically materializing downstream database tables as soon as upstream source files are validated or updated.
- **Continuous Quality Observability**: Running automated validation checks (such as null-value checks, row-count thresholds, and schema audits) directly inside the asset execution pipeline.
- **Agentic Pipeline Management**: Enabling AI agents to inspect, materialize, and troubleshoot data assets using standard system tools.
- **External Environment Execution (Pipes)**: Launching secure pipelines across heterogeneous compute clusters (such as Kubernetes, AWS ECS, or Snowflake) via **Dagster Pipes** while keeping a single pane of glass.

## Strengths
- **Asset-First Framework**: Tracks lineage, metadata, and data quality directly on the asset level for easier auditing.
- **Declarative Automation**: Uses high-level freshness requirements rather than explicit schedules, reducing code complexity.
- **FastMCP 3.1 Ready**: Exposes your entire data asset graph to frontier AI agents as secure, executable tools.
- **Local Developer Experience**: Features a high-performance local UI with integrated asset execution, debugging, and mock testing.
- **v1.9+ Overhauls**: Streamlined declarative automation, native powerBI/Tableau integration, and compatibility with standard metadata libraries.

## Limitations
- **Python Dependency**: Requires a strong working knowledge of Python and object decorators to declare assets.
- **Resource Footprint**: The webserver and monitoring daemons require continuous CPU/Memory resources to trace schedules and asset conditions.
- **Complexity for Basic Shell Runs**: May represent excessive overhead for simple, non-data-centric automation tasks where [Prefect](prefect.md) or [Kestra](kestra.md) would be lighter.

## When to use it
- When building a data platform where data should be treated, versioned, and audited as standard code assets.
- If you need granular visibility into data lineage and automated schema/metric testing.
- When you want downstream tables to update automatically based on upstream changes without managing manual dependency triggers.
- When designing AI-integrated platforms where autonomous agents need to analyze and execute complex data-handling graphs.

## When not to use it
- For quick, isolated shell task triggers that do not generate or modify data assets.
- If your development team primarily operates outside of Python.
- For low-latency streaming pipelines that require millisecond-scale stream processing engines (such as Flink).

## Getting started

### Installation
Deploy Dagster and its web development server locally:

```bash
pip install dagster dagster-webserver
```

### Basic Declarative Asset Example
Define a basic data asset graph in `my_data_assets.py`:

```python
from dagster import asset, AutomationCondition

@asset
def raw_user_logs():
    return [
        {"user_id": 1, "action": "login"},
        {"user_id": 2, "action": "purchase"},
        {"user_id": 3, "action": "logout"}
    ]

@asset(
    automation_condition=AutomationCondition.on_missing(),
    deps=[raw_user_logs]
)
def filtered_events(raw_user_logs):
    # Only keep active user events
    return [event for event in raw_user_logs if event["action"] != "logout"]
```

### Starting the Local Development Server
Launch the server to review the asset lineage chart:
```bash
dagster dev -f my_data_assets.py
```
Open your browser and navigate to `http://localhost:3000`.

## CLI examples
The `dagster` command surface is used to coordinate local backfills, execution states, and model registries:

```bash
# 1. List all active data assets in the workspace
dagster asset list

# 2. Force manual materialization for target assets
dagster asset materialize --asset raw_user_logs --asset filtered_events

# 3. Trigger backfills over partitioned asset scopes
dagster job backfill --job partitioned_user_job --partitions 2026-12-01,2026-12-25

# 4. Check on-premise daemon health and schedule status
dagster-daemon health_check

# 5. Connect and register Dagster assets as MCP tools (v1.9.12+)
dagster mcp register --server http://localhost:3000 --output-dir ./mcp-configs
```

## API examples
Dagster provides a GraphQL interface and a Python client for programmatic interaction. Below is an orchestration example utilizing **Pydantic v2** to programmatically trigger asset materializations and validate the run's metadata:

### 1. Python: Trigger Dagster Run and Validate Response Metadata
```python
import os
import requests
from typing import Optional, List
from pydantic import BaseModel, Field, ValidationError

# Define strict schemas matching Dagster's GraphQL API (Pydantic v2)
class DagsterRunMetadata(BaseModel):
    run_id: str = Field(..., alias="runId", description="Unique UUID for the initiated asset run")
    status: str = Field(..., description="The status of the run (e.g. STARTING, SUCCESS, FAILURE)")
    asset_keys: List[str] = Field(default=[], alias="assetKeys", description="List of target assets to materialize")

    class Config:
        populate_by_name = True

def trigger_dagster_materialization(server_url: str, repository: str, asset_name: str) -> Optional[DagsterRunMetadata]:
    endpoint = f"{server_url}/graphql"

    # GraphQL mutation to trigger manual asset run execution
    query = """
    mutation TriggerMaterialize($assetKey: [AssetKeyInput!]!) {
      launchPipelineExecution(
        executionParams: {
          selector: { repositoryLocationName: "local", repositoryName: "%s" }
          mode: "default"
        }
      ) {
        __typename
        ... on LaunchRunSuccess {
          run {
            runId
            status
          }
        }
      }
    }
    """ % repository

    payload = {
        "query": query,
        "variables": {
            "assetKey": [{"path": [asset_name]}]
        }
    }

    try:
        response = requests.post(endpoint, json=payload, timeout=5)
        response.raise_for_status()
        raw_data = response.json()

        # Handle GraphQL error payloads gracefully
        if "errors" in raw_data:
            print(f"GraphQL execution errors: {raw_data['errors']}")
            return None

        run_data = raw_data.get("data", {}).get("launchPipelineExecution", {}).get("run", {})
        if not run_data:
            print("Failed to launch pipeline execution.")
            return None

        # Build raw dict to validate using Pydantic v2
        validated_run = DagsterRunMetadata(
            runId=run_data.get("runId"),
            status=run_data.get("status"),
            assetKeys=[asset_name]
        )
        return validated_run
    except requests.exceptions.RequestException as e:
        print(f"Failed to communicate with Dagster GraphQL: {e}")
        return None
    except ValidationError as e:
        print(f"Schema validation error on run metadata: {e}")
        return None

if __name__ == "__main__":
    dagster_host = os.environ.get("DAGSTER_URL", "http://localhost:3000")
    print(f"Connecting to Dagster server at: {dagster_host}...")

    run_info = trigger_dagster_materialization(dagster_host, "my_data_repository", "filtered_events")
    if run_info:
        print(f"Successfully initiated run {run_info.run_id}")
        print(f"Target Assets: {run_info.asset_keys} | Current Status: {run_info.status}")
    else:
        print("Data materialization trigger or validation failed.")
```

## Related tools / concepts
- [Apache Airflow](apache-airflow.md) — The veteran task-based alternative.
- [Apache Hamilton](apache-hamilton.md) — Fine-grained micro-orchestrator.
- [Prefect](prefect.md) — Python-native, dynamic orchestration layer.
- [Kestra](kestra.md) — Declarative YAML orchestrator with built-in MCP tooling.
- [Flyte](flyte.md) — Kubernetes-native machine learning pipeline manager.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Protocol for model integrations.
- [n8n](../../services/n8n.md) — Visual workflow automation utility.
- [Pydantic](../frameworks/pydantic-ai.md) — Data validation framework used across modern data pipelines.

## Sources / references
- [Dagster Official Documentation](https://docs.dagster.io/)
- [Dagster v1.9 Features: Declarative Asset Orchestration](https://dagster.io/blog/dagster-1-9)
- [Model Context Protocol Specification Standards](https://modelcontextprotocol.io/)
- [Dagster Public GitHub Codebase](https://github.com/dagster-io/dagster)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
