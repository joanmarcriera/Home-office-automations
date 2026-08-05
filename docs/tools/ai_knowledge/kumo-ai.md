# Kumo AI (KumoRFM-2)

## What it is
Kumo AI is a predictive AI platform that specializes in Relational Foundation Models (RFMs). Its flagship model, **KumoRFM-2**, is designed to reason over structured, relational data living in enterprise data warehouses. It treats the entire database as a graph, enabling advanced predictive analytics without complex feature engineering. By late November 2026, Kumo has integrated full support for the **Model Context Protocol (MCP) 3.1 / FastMCP 3.1 specifications**, allowing autonomous agents to trigger and consume predictions as part of larger automated workflows.

## What problem it solves
Traditional machine learning requires data scientists to "flatten" multi-table relational data into a single table (feature engineering), which often destroys valuable predictive signals stored in the relationships between tables. KumoRFM-2 works directly on the graph of connected tables, preserving foreign-key relationships and patterns.

## Where it fits in the stack
[AI & Knowledge](./index.md) / [Process Understanding](../process_understanding/index.md). It acts as a predictive intelligence layer on top of raw data infrastructure, serving as a "Predictive Engine" for enterprise data.

## Typical use cases
- **Zero-Training Predictions**: Point the model at a data warehouse and run predictive queries in plain English without task-specific training.
- **Relational Reasoning**: Predicting outcomes (e.g., customer churn, product demand) by analyzing patterns across multiple linked tables.
- **Large-Scale Data Science**: Scales to over 500 billion rows of relational data, suitable for massive enterprise datasets.
- **Autonomous Decisioning**: Using an agent to query Kumo for churn risk and then automatically triggering a retention workflow via [n8n](../../services/n8n.md).

## Strengths
- **No ETL/Feature Engineering**: Eliminates the need for complex data pipelines or feature stores.
- **Hierarchical In-Context Learning**: Extracts task-aware features at both individual table and cross-table levels.
- **High Performance**: Outperforms fully supervised machine learning models on relational benchmarks like [RelBench](https://relbench.stanford.edu/).
- **Predictive Querying**: Allows data teams to ask "What will happen?" instead of just "What happened?".
- **Frontier Integration**: Optimized for use with SOTA models like **Claude 5.1**, **GPT-5.5**, and **Gemini 4.0** for interpreting predictive results.

## Limitations
- **Relational Focus**: Primarily designed for structured tabular data, not unstructured text or media.
- **Enterprise Scale**: Optimized for large data warehouses ([Snowflake](../process_understanding/snowflake.md), Databricks, BigQuery); may be overkill for simple datasets.
- **Closed Platform**: Managed service; not available for local or air-gapped execution.

## When to use it
- When you need to extract predictive insights from complex, multi-table relational databases.
- To reduce the time-to-value for new data science projects from months to hours.
- When traditional tabular ML models (XGBoost, etc.) fail to capture signal from relationships.
- When you want to enable predictive capabilities for autonomous agents via MCP.

## When not to use it
- For tasks involving primarily unstructured data (text, images).
- For very small or single-table datasets where traditional ML is sufficient.
- When you require a fully open-source or local predictive stack (consider [Ludwig](../frameworks/ludwig.md)).

## Getting started
To get started with Kumo, you connect your cloud data warehouse (Snowflake, Databricks, or BigQuery) and define predictive tasks using a SQL-like interface.

### Predictive Querying Examples
```sql
-- Predict the total revenue from a customer over the next 90 days
PREDICT SUM(Transactions.Amount)
FOR EACH Users.ID
OVER NEXT 90 DAYS

-- Predict which users will not have any transactions in the next 30 days (Churn)
PREDICT COUNT(Transactions.ID) == 0
FOR EACH Users.ID
OVER NEXT 30 DAYS
```

## CLI examples
> [!NOTE]
> As of late November 2026, Kumo AI focuses on its Managed SaaS interface and REST API. There is no official standalone CLI for model management. However, developers can use the [Claude Code](../development_ops/claude-code.md) CLI with the Kumo MCP server to run predictive queries.

## API examples
Once a model is trained on Kumo, results can be retrieved via the Kumo REST API or pushed back into your data warehouse.

### Prediction Retrieval with Strict Pydantic v2 Validation (Python)
This example demonstrates how to validate Kumo predictive query results against a strict, type-safe schema in Python using Pydantic v2.

```python
import os
import requests
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError

# Define schemas with Pydantic v2
class PredictionItem(BaseModel):
    user_id: str = Field(..., alias="id", description="Unique identifier for the user or entity")
    score: float = Field(..., ge=0.0, le=1.0, description="Risk or probability score (0.0 to 1.0)")

class KumoPredictionResponse(BaseModel):
    plan_id: str = Field(..., description="The Kumo prediction plan identifier")
    status: str = Field(..., description="Job execution status (e.g., SUCCESS, RUNNING)")
    data: List[PredictionItem] = Field(default_factory=list, description="List of individual prediction scores")

    class Config:
        populate_by_name = True

def fetch_and_validate_predictions(plan_id: str, api_key: str) -> KumoPredictionResponse:
    url = f"https://api.kumo.ai/v1/plans/{plan_id}/predictions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # In a real environment, execute requests.get(url, headers=headers)
    # We simulate a valid JSON response from Kumo for verification/mock purposes
    mock_json = {
        "plan_id": plan_id,
        "status": "SUCCESS",
        "data": [
            {"id": "user_9012", "score": 0.89},
            {"id": "user_3456", "score": 0.12},
            {"id": "user_7890", "score": 0.95}
        ]
    }

    # Parse and validate the response structure under Pydantic v2
    try:
        validated_response = KumoPredictionResponse(**mock_json)
        return validated_response
    except ValidationError as e:
        print(f"Failed to validate Kumo response: {e.errors()}")
        raise

if __name__ == "__main__":
    api_key = os.environ.get("KUMO_API_KEY", "mock_key_for_testing")
    plan_id = "plan_123abc"

    try:
        response = fetch_and_validate_predictions(plan_id, api_key)
        print(f"Successfully retrieved and validated {len(response.data)} predictions.")
        for item in response.data:
            print(f"User: {item.user_id}, Churn Risk: {item.score * 100:.1f}%")
    except Exception as e:
        print("Error fetching predictions:", e)
```

## Related tools / concepts
- [Landscape Overview](../../knowledge_base/landscape-overview.md) — Market context.
- [Snowflake](../process_understanding/snowflake.md) — Primary data source.
- [ClickHouse](../process_understanding/clickhouse.md) — Real-time OLAP.
- [Sentry](../process_understanding/sentry.md) — Observability integration.
- [Datadog](../process_understanding/datadog.md) — Enterprise monitoring.
- [Grafana Cloud](../process_understanding/grafana-cloud.md) — Visualization.
- [New Relic](../process_understanding/new-relic-ai.md) — AI-native observability.
- [n8n](../../services/n8n.md) — Workflow automation.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Agent integration standard.

## Sources / references
- [Kumo's new foundation model replaces months of data science engineering](https://thenewstack.io/kumo-ai-foundation-models/)
- [RelBench Benchmark](https://relbench.stanford.edu/)
- [Official Website](https://kumo.ai/)
- **Licensing**: Proprietary enterprise SaaS.

## Contribution Metadata
- Last reviewed: 2026-11-25
- Confidence: high
