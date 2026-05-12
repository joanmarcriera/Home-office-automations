# Supermetal Benchmark

## What it is
Supermetal is a high-performance data movement and processing tool. It is often benchmarked on its ability to synchronize data between relational databases (like Postgres) and modern data lake formats (like Apache Iceberg).

## What problem it solves
It addresses the latency and complexity bottlenecks in Change Data Capture (CDC) pipelines. Traditionally, moving data from production databases to analytics platforms required complex setups involving Flink, Kafka Connect, or Spark.

## Where it fits in the stack
**Category**: Tool / Benchmark

## Typical use cases
- **Real-time CDC**: Synchronizing Postgres data to Iceberg for near-instant analytics.
- **Data Stack Consolidation**: Simplifying the infrastructure required for reliable data pipelines.

## Strengths
- **Speed**: Benchmarks show Postgres to Iceberg synchronization in as little as 13 minutes.
- **Simplicity**: Designed to replace more complex distributed computing frameworks for specific data movement tasks.
- **Performance**: Highly optimized for modern hardware and cloud-native storage.

## Limitations
- **Niche Focus**: Specifically optimized for high-speed data movement and specific target formats.

## When to use it
- When you need low-latency synchronization between production databases and an analytical data lake.
- When looking to reduce the operational overhead of Kafka/Spark-based pipelines.

## When not to use it
- For small datasets that don't justify the overhead of a dedicated CDC tool.
- If you require complex in-flight data transformations (consider [Fivetran](fivetran.md) or [dbt](dbt.md) for heavy T in ELT).

## Getting started
Supermetal operates via an API-driven connector model. To get started, deploy the Supermetal service and use the REST API to configure your source and sink connectors.

## API examples
**Create a new connector**:
```bash
curl -X POST "https://your-supermetal-instance/api/v1/connectors/my-pg-to-iceberg" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "my-pg-to-iceberg",
    "source": {
      "postgres": {
        "connection": {
          "host": "pg-host",
          "user": "sync_user",
          "password": "password",
          "database": "prod_db"
        },
        "replication_type": { "logical_replication": {} }
      }
    },
    "sink": {
      "iceberg": {
        "catalog_type": "glue",
        "database": "analytics"
      }
    }
  }'
```

**List all connectors**:
```bash
curl "https://your-supermetal-instance/api/v1/connectors"
```

## Related tools / concepts
- [Data Stack Consolidation](../../knowledge_base/landscape-overview.md)
- [AirOps](../automation_orchestration/airops.md)
- [Temporal](../orchestration/temporal.md)
- [Datadog](../process_understanding/datadog.md)
- [Grafana](../process_understanding/grafana.md)
- [ClickHouse](../process_understanding/clickhouse.md)
- [Snowflake](../process_understanding/snowflake.md)
- [Real-time Sync Engines](../../knowledge_base/real_time_sync_engines.md)

## Sources / references
- [Postgres to Iceberg in 13 minutes: How Supermetal compares](https://thenewstack.io/postgres-iceberg-cdc-benchmarks/)

## Contribution Metadata
- Last reviewed: 2026-05-18
- Confidence: high
