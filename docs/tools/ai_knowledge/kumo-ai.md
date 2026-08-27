# Kumo AI (KumoRFM-2)

## What it is
Kumo AI is a predictive AI platform specializing in Relational Foundation Models (RFMs). Its flagship model, **KumoRFM-2**, is designed to reason directly over structured, multi-table relational schema data residing in cloud data warehouses. It represents enterprise relational databases as connected graphs, enabling predictive machine learning without manual feature engineering pipelines. In 2027, Kumo features full native integration with the **FastMCP 3.1** specification, allowing autonomous agentic workflows to issue predictive queries and incorporate forecast results into decision chains.

## What problem it solves
Traditional machine learning requires complex ETL jobs to flatten multi-table relational schema into single flat tables (feature engineering), destroying temporal and cross-table relational signals. KumoRFM-2 operates natively on foreign-key graphs across linked tables, eliminating feature maintenance costs, preserving relational context, and enabling instant zero-shot or few-shot predictions from natural language queries.

## Where it fits in the stack
**Category**: AI Assistants & Knowledge / Predictive Data Intelligence
Kumo AI operates as the predictive analytics layer above enterprise data infrastructure ([Snowflake](../process_understanding/snowflake.md), Databricks, BigQuery, [ClickHouse](../process_understanding/clickhouse.md)). It acts as a predictive engine for autonomous workflow tools like [n8n](../../services/n8n.md) and agent frameworks over **FastMCP 3.1**.

## Typical use cases
- **Zero-ETL Predictive Analytics**: Executing declarative predictive queries directly on live relational warehouse schemas without prior feature engineering.
- **Relational Churn & LTV Forecasting**: Predicting customer attrition, lifetime value (LTV), and next-best-action recommendations across multi-table transactional databases.
- **Agentic Decision Automation**: Providing predictive scores to agents (e.g., auto-routing high-churn customers to personalized retention offers).
- **Supply Chain Demand Forecasting**: Reasoning over complex multi-tier vendor, inventory, and fulfillment tables to forecast stockouts.

## Strengths
- **No Manual Feature Engineering**: Connects directly to database schemas and automatically learns graph representation features.
- **Relational Spatial Reasoning**: Preserves temporal and graph relationships across hundreds of interconnected tables.
- **Declarative Predictive SQL Syntax**: Allows data teams and AI agents to express prediction goals in simple SQL-like syntax.
- **Scalability**: Handles production workloads scaling to over 500 billion rows of enterprise data.
- **FastMCP 3.1 Compatibility**: Exposes predictive query tools directly to frontier LLMs like **Claude 5.6**, **GPT-5.6**, and **Gemini 4.0 Ultra**.

## Limitations
- **Relational Focus**: Optimized specifically for structured tabular/relational schemas rather than unstructured media or text archives.
- **Cloud Warehouse Dependency**: Requires direct connection to enterprise cloud data warehouses.
- **Managed Platform**: Proprietary SaaS platform; not available for fully offline, air-gapped self-hosting.

## When to use it
- When you need accurate predictive forecasts across complex multi-table relational data schemas.
- To reduce time-to-market for predictive ML models from months to hours.
- When equipping autonomous agents with predictive capabilities via MCP tools.

## When not to use it
- For unstructured vector search over text or images (use [ColQwen](colqwen.md) or standard RAG instead).
- For single small spreadsheets where simple regression or XGBoost is sufficient.
- When absolute offline execution is mandatory.

## Getting started

### Predictive SQL Interface Example
Connect Kumo to your Snowflake or BigQuery warehouse and issue predictive statements:

```sql
-- Predict customer churn probability over the next 30 days
PREDICT COUNT(Transactions.ID) == 0
FOR EACH Customers.ID
OVER NEXT 30 DAYS
```

## CLI examples

### 1. Execute Predictive Task via Claude Code & MCP
```bash
claude-code --mcp-server kumo-rfm "Predict the 90-day LTV for customer ID user_90123"
```

## API examples

### FastMCP 3.1 Server & Strict Pydantic v2 Prediction Schema
This executable Python script demonstrates integrating KumoRFM-2 predictive queries into a **FastMCP 3.1** server using strict **Pydantic v2** validation.

```python
import os
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError
from fastmcp import FastMCP

mcp = FastMCP("KumoRFM Predictive Analytics Server")

class RiskPrediction(BaseModel):
    entity_id: str = Field(..., alias="id", description="Unique identifier for the customer or entity")
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Predicted risk probability score")
    predicted_action: str = Field(..., description="Recommended mitigation step")

class KumoQueryResponse(BaseModel):
    query_id: str = Field(..., description="Unique Kumo predictive job execution ID")
    status: str = Field(..., description="Execution status")
    predictions: List[RiskPrediction] = Field(default_factory=list, description="Validated risk prediction records")

    class Config:
        populate_by_name = True

@mcp.tool()
def get_customer_churn_predictions(segment_id: str, threshold: float = 0.75) -> str:
    """Execute KumoRFM-2 predictive query to identify high-risk churn customers in a segment."""
    # Simulated response payload from Kumo API
    mock_payload = {
        "query_id": "kumo_job_9921a",
        "status": "COMPLETED",
        "predictions": [
            {
                "id": "cust_88291",
                "risk_score": 0.89,
                "predicted_action": "Trigger automated retention offer via n8n"
            },
            {
                "id": "cust_44102",
                "risk_score": 0.82,
                "predicted_action": "Schedule executive check-in call"
            }
        ]
    }

    try:
        response = KumoQueryResponse(**mock_payload)
        high_risk = [p for p in response.predictions if p.risk_score >= threshold]
        return f"Query {response.query_id} complete. Found {len(high_risk)} high-risk customers above threshold {threshold}. Top risk ID: {high_risk[0].entity_id} ({high_risk[0].risk_score * 100:.1f}%)"
    except ValidationError as e:
        return f"Validation error: {e.errors()}"

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [Snowflake](../process_understanding/snowflake.md) — Primary data warehouse integration partner.
- [ClickHouse](../process_understanding/clickhouse.md) — Real-time analytics database connector.
- [n8n](../../services/n8n.md) — Workflow automation runner for prediction-triggered actions.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standardized tool execution framework.

## Sources / references
- [Kumo AI Official Website](https://kumo.ai/)
- [RelBench Relational Benchmark](https://relbench.stanford.edu/)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/fastmcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
