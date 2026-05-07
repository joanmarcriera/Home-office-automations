# Dagster

## What it is
Dagster is a data orchestrator for building, observing, and operating data and AI pipelines. It centers the model around data assets, lineage, metadata, testing, and operational visibility rather than only task execution order.

## What problem it solves
Dagster helps teams understand what data products exist, how they are produced, when they are fresh, and which upstream assets affect them. For AI systems, this is valuable when models, agents, or retrieval pipelines depend on reliable datasets, embeddings, features, documents, or evaluation tables.

## Where it fits in the stack
**Orchestration / Data and AI pipeline control plane**.

## Typical use cases
- Data asset orchestration for analytics, ML, and AI products.
- Embedding, feature, or evaluation dataset refresh pipelines.
- dbt, Spark, warehouse, notebook, and Python job coordination.
- Data quality, freshness, and lineage tracking for AI-ready datasets.

## Strengths
- Asset-oriented model makes lineage and ownership more explicit.
- Strong local development, testing, metadata, and observability story.
- Good fit for modern data teams that need both orchestration and catalog context.
- Managed Dagster+ option reduces platform operations for teams that want SaaS.

## Limitations
- Less focused on arbitrary SaaS automation than tools such as n8n or Zapier.
- Teams moving from classic task DAGs may need to learn asset-first modeling.
- The managed product introduces vendor dependency for hosted capabilities.
- Not a general-purpose durable function engine for application workflows.

## When to use it
- You need to orchestrate data and AI pipelines where lineage, freshness, and observability matter.
- Data products are first-class operational objects.
- You want Python-based development with production-grade metadata.

## When not to use it
- The workload is mostly office SaaS automation.
- You need Kubernetes-native YAML workflows.
- You need long-running application transactions with durable event history.

## Licensing and cost
- **Open Source**: Yes (Apache License 2.0)
- **Cost**: Free open-source edition; paid Dagster+ managed platform.
- **Self-hostable**: Yes

## Related tools / concepts
- [Prefect](prefect.md)
- [Apache Airflow](apache-airflow.md)
- [Flyte](flyte.md)
- [Vector DB Comparison](../../knowledge_base/vector-db-comparison.md)

## Sources / References
- [Official website](https://dagster.io/)
- [Official documentation](https://docs.dagster.io/)
- [GitHub](https://github.com/dagster-io/dagster)

## Contribution Metadata
- Last reviewed: 2026-05-06
- Confidence: high
