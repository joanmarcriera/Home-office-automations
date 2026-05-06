# Kumo AI (KumoRFM-2)

## What it is
Kumo AI is a predictive AI platform that specializes in Relational Foundation Models (RFMs). Its flagship model, **KumoRFM-2**, is designed to reason over structured, relational data living in enterprise data warehouses.

## What problem it solves
Traditional machine learning requires data scientists to "flatten" multi-table relational data into a single table (feature engineering), which often destroys valuable predictive signals stored in the relationships between tables. KumoRFM-2 works directly on the graph of connected tables, preserving foreign-key relationships.

## Where it fits in the stack
**Category**: AI Model / Data Science

## Typical use cases
- **Zero-Training Predictions**: Point the model at a data warehouse and run predictive queries in plain English without task-specific training.
- **Relational Reasoning**: Predicting outcomes (e.g., customer churn, product demand) by analyzing patterns across multiple linked tables.
- **Large-Scale Data Science**: Scales to over 500 billion rows of relational data.

## Strengths
- **No ETL/Feature Engineering**: Eliminates the need for complex data pipelines or feature stores.
- **Hierarchical In-Context Learning**: Extracts task-aware features at both individual table and cross-table levels.
- **High Performance**: Outperforms fully supervised machine learning models on relational benchmarks like RelBench.

## Limitations
- **Relational Focus**: Primarily designed for structured tabular data, not unstructured text or media.
- **Enterprise Scale**: Optimized for large data warehouses (Snowflake, Databricks); may be overkill for simple datasets.

## When to use it
- When you need to extract predictive insights from complex, multi-table relational databases.
- To reduce the time-to-value for new data science projects from months to hours.

## When not to use it
- For tasks involving primarily unstructured data (text, images).
- For very small or single-table datasets where traditional ML is sufficient.

## Related tools / concepts
- [Landscape Overview](../../knowledge_base/landscape-overview.md)
- [Snowflake](../infrastructure/snowflake.md)
- [ClickHouse](../process_understanding/clickhouse.md)
- [Sentry](../process_understanding/sentry.md)
- [Datadog](../process_understanding/datadog.md)

## Sources / references
- [Kumo's new foundation model replaces months of data science engineering](https://thenewstack.io/kumo-ai-foundation-models/)
- [RelBench Benchmark](https://relbench.stanford.edu/)

## Contribution Metadata
- Last reviewed: 2026-05-28
- Confidence: high
