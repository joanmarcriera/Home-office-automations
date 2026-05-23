# Kumo AI (KumoRFM-2)

## What it is
Kumo AI is a predictive AI platform that specializes in Relational Foundation Models (RFMs). Its flagship model, **KumoRFM-2**, is designed to reason over structured, relational data living in enterprise data warehouses.

## What problem it solves
Traditional machine learning requires data scientists to "flatten" multi-table relational data into a single table (feature engineering), which often destroys valuable predictive signals stored in the relationships between tables. KumoRFM-2 works directly on the graph of connected tables, preserving foreign-key relationships and patterns.

## Where it fits in the stack
[AI & Knowledge](./index.md) / [Process Understanding](../process_understanding/index.md). It acts as a predictive intelligence layer on top of raw data infrastructure.

## Typical use cases
- **Zero-Training Predictions**: Point the model at a data warehouse and run predictive queries in plain English without task-specific training.
- **Relational Reasoning**: Predicting outcomes (e.g., customer churn, product demand) by analyzing patterns across multiple linked tables.
- **Large-Scale Data Science**: Scales to over 500 billion rows of relational data, suitable for massive enterprise datasets.

## Strengths
- **No ETL/Feature Engineering**: Eliminates the need for complex data pipelines or feature stores.
- **Hierarchical In-Context Learning**: Extracts task-aware features at both individual table and cross-table levels.
- **High Performance**: Outperforms fully supervised machine learning models on relational benchmarks like [RelBench](https://relbench.stanford.edu/).
- **Predictive Querying**: Allows data teams to ask "What will happen?" instead of just "What happened?".

## Limitations
- **Relational Focus**: Primarily designed for structured tabular data, not unstructured text or media.
- **Enterprise Scale**: Optimized for large data warehouses ([Snowflake](../process_understanding/snowflake.md), Databricks); may be overkill for simple datasets.
- **Closed Platform**: Managed service; not available for local or air-gapped execution.

## When to use it
- When you need to extract predictive insights from complex, multi-table relational databases.
- To reduce the time-to-value for new data science projects from months to hours.
- When traditional tabular ML models (XGBoost, etc.) fail to capture signal from relationships.

## When not to use it
- For tasks involving primarily unstructured data (text, images).
- For very small or single-table datasets where traditional ML is sufficient.
- When you require a fully open-source or local predictive stack.

## Getting started

### Connecting your Data Warehouse
Kumo connects directly to your cloud data warehouse. Supported providers include:
1.  **Snowflake**: Via standard credentials or Key Pair authentication.
2.  **Databricks**: Via Personal Access Token (PAT).
3.  **BigQuery**: Via Service Account JSON.

## Predictive Querying (SQL-like)
Kumo uses a SQL-like interface for defining predictive tasks. This allows analysts to define "What" they want to predict without specifying "How" to extract features.

### Example: Predicting Customer Lifetime Value (LTV)
```sql
-- Predict the total revenue from a customer over the next 90 days
PREDICT SUM(Transactions.Amount)
FOR EACH Users.ID
OVER NEXT 90 DAYS
```

### Example: Predicting Churn
```sql
-- Predict which users will not have any transactions in the next 30 days
PREDICT COUNT(Transactions.ID) == 0
FOR EACH Users.ID
OVER NEXT 30 DAYS
```

## API: Deployment and Retrieval
Once a model is trained on Kumo, results can be retrieved via the Kumo REST API or pushed back into your data warehouse.

```python
import requests
import os

KUMO_API_KEY = os.environ["KUMO_API_KEY"]
PLAN_ID = "plan_123abc"

def get_predictions(plan_id):
    url = f"https://api.kumo.ai/v1/plans/{plan_id}/predictions"
    headers = {"Authorization": f"Bearer {KUMO_API_KEY}"}

    response = requests.get(url, headers=headers)
    return response.json()

# Fetch latest predictions for high-churn-risk users
predictions = get_predictions(PLAN_ID)
for user in predictions['data']:
    print(f"User: {user['id']}, Churn Probability: {user['score']}")
```

## Licensing and cost
- **Proprietary**: Managed SaaS platform.
- **Cost**: Enterprise pricing based on data volume and compute usage.
- **Trial**: Available upon request for qualified organizations.

## Related tools / concepts
- [Landscape Overview](../../knowledge_base/landscape-overview.md)
- [Snowflake](../process_understanding/snowflake.md)
- [ClickHouse](../process_understanding/clickhouse.md)
- [Sentry](../process_understanding/sentry.md)
- [Datadog](../process_understanding/datadog.md)
- [Grafana Cloud](../process_understanding/grafana.md)
- [New Relic](../process_understanding/new-relic.md)

## Sources / references
- [Kumo's new foundation model replaces months of data science engineering](https://thenewstack.io/kumo-ai-foundation-models/)
- [RelBench Benchmark](https://relbench.stanford.edu/)
- [Official Website](https://kumo.ai/)

## Contribution Metadata
- Last reviewed: 2026-05-23
- Confidence: high
