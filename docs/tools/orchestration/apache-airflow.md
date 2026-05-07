# Apache Airflow

## What it is
Apache Airflow is an open-source platform for authoring, scheduling, and monitoring workflows as Python-defined DAGs. It is a mature general-purpose orchestrator with a large provider ecosystem for databases, warehouses, cloud services, and infrastructure systems.

## What problem it solves
Airflow turns recurring operational work into versioned workflow code with dependencies, schedules, retries, logs, and a web UI. For AI and data systems, it is useful when the main problem is coordinating batch jobs, extraction steps, model refreshes, report generation, or integration tasks across many existing services.

## Where it fits in the stack
**Orchestration / Batch workflow scheduler**.

## Typical use cases
- Scheduled ETL, ELT, and reverse-ETL pipelines.
- Periodic model training, embedding refresh, or report generation jobs.
- Coordinating tasks across cloud warehouses, storage buckets, notebooks, APIs, and internal services.
- Auditable workflow operations where teams need logs, retry controls, and ownership boundaries.

## Strengths
- Very broad ecosystem of providers and operational knowledge.
- Workflows are Python code, which makes them reviewable and testable in normal development workflows.
- Strong scheduling, retry, backfill, logging, and UI support for batch workloads.
- Can run self-hosted and has many managed-service options.

## Limitations
- DAG-centric design is less natural for highly dynamic, stateful, or conversational agent loops.
- Operational footprint can be heavy compared with lighter Python-native orchestrators.
- Poor fit for low-latency request/response AI services.
- Complex deployments require careful executor, metadata database, and worker configuration.

## When to use it
- You already operate Airflow or need compatibility with a mature data-platform standard.
- Workloads are scheduled, dependency-driven, and mostly batch-oriented.
- You need many prebuilt integrations and a familiar UI for operations teams.

## When not to use it
- You need durable function semantics for long-running stateful workflows.
- The workflow shape is highly dynamic at runtime.
- You want a small embedded library inside an application rather than a platform service.

## Licensing and cost
- **Open Source**: Yes (Apache License 2.0)
- **Cost**: Free self-hosted; paid managed offerings available from vendors.
- **Self-hostable**: Yes

## Related tools / concepts
- [Temporal](temporal.md)
- [Prefect](prefect.md)
- [Dagster](dagster.md)
- [n8n](../../services/n8n.md)

## Sources / References
- [Official website](https://airflow.apache.org/)
- [Official documentation](https://airflow.apache.org/docs/)
- [GitHub](https://github.com/apache/airflow)

## Contribution Metadata
- Last reviewed: 2026-05-06
- Confidence: high
