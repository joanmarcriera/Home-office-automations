# ClickHouse

## What it is
ClickHouse is an open-source, high-performance, column-oriented SQL database management system (DBMS) for online analytical processing (OLAP). It is designed to handle massive datasets and return query results in real-time.

## What problem it solves
It addresses the performance limitations of traditional row-oriented databases when performing complex analytical queries over billions of rows. ClickHouse allows for extremely fast aggregations and filters, making it ideal for real-time observability, logs, and telemetry analysis.

## Where it fits in the stack
**Category**: Process & Understanding / Analytical Database (OLAP)

## Typical use cases
- **Log Management**: Storing and querying massive volumes of application and system logs (e.g., streaming OpenRouter logs).
- **Real-Time Analytics**: Powering dashboards that require sub-second response times on large datasets.
- **Observability**: Storing and analyzing traces, metrics, and events at scale.
- **Clickstream Analysis**: Analyzing user behavior on websites and mobile apps in real-time.

## Strengths
- **Superior Query Performance**: Leverages columnar storage and parallel execution for lightning-fast SQL queries.
- **High Data Compression**: Significantly reduces storage costs by using efficient compression algorithms tailored for columnar data.
- **Scalability**: Can be deployed on a single server or scaled out to clusters handling petabytes of data.
- **Rich SQL Support**: Supports ANSI SQL, including JOINs, window functions, and complex aggregations.

## Limitations
- **Not for OLTP**: Not designed for high-frequency individual row updates or deletes (mutations).
- **Learning Curve**: Optimizing table schemas and partitioning keys for maximum performance requires specific expertise.
- **Hardware Intensive**: Performance scales well with CPU cores and fast storage (NVMe), which can increase infrastructure costs.

## Getting started

### Installation (via Docker)
```bash
docker run -d --name clickhouse-server -p 8123:8123 -p 9000:9000 clickhouse/clickhouse-server
```

### Basic SQL Example
```sql
CREATE TABLE traces (
    event_time DateTime,
    model String,
    prompt_tokens UInt32,
    completion_tokens UInt32,
    latency Float32
) ENGINE = MergeTree()
ORDER BY event_time;

INSERT INTO traces VALUES ('2026-05-08 10:00:00', 'claude-3-5-sonnet', 500, 200, 1.5);

SELECT model, AVG(latency) FROM traces GROUP BY model;
```

## Related tools / concepts
- [OpenRouter](../ai_knowledge/openrouter.md) (Log streaming destination)
- [Snowflake](snowflake.md)
- [Datadog](datadog.md)
- [S3 / S3-Compatible Storage](../intake_storage/s3-storage.md)

## Sources / references
- [Official Website](https://clickhouse.com/)
- [ClickHouse Documentation](https://clickhouse.com/docs/en/intro)
- [OpenRouter Broadcast Guide](https://openrouter.ai/docs/guides/features/broadcast/clickhouse)

## Contribution Metadata
- Last reviewed: 2026-05-08
- Confidence: high
