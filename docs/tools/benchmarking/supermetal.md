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

## Related tools / concepts
- [Data Stack Consolidation](../../knowledge_base/landscape-overview.md)
- Apache Iceberg
- Change Data Capture (CDC)

## Sources / references
- [Postgres to Iceberg in 13 minutes: How Supermetal compares](https://thenewstack.io/postgres-iceberg-cdc-benchmarks/)

## Contribution Metadata
- Last reviewed: 2026-04-16
- Confidence: high
