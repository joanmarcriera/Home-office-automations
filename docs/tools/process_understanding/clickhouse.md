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

### OpenRouter Log Ingestion Schema
Before enabling OpenRouter broadcast, create the following table to receive traces:

```sql
CREATE TABLE OPENROUTER_TRACES (
    TIMESTAMP DateTime64(3, 'UTC'),
    ID String,
    MODEL String,
    APP_ID Nullable(String),
    USER_ID Nullable(String),
    PROMPT_TOKENS UInt32,
    COMPLETION_TOKENS UInt32,
    TOTAL_TOKENS UInt32,
    TOTAL_COST Float64,
    LATENCY Float64,
    STATUS String,
    REQUEST String,
    RESPONSE String
) ENGINE = MergeTree()
ORDER BY TIMESTAMP;
```

### Python Query Example
You can query your AI traces using the `clickhouse-connect` library.

```python
import clickhouse_connect

# Initialize client
client = clickhouse_connect.get_client(host='localhost', username='default', password='')

# Query top models by usage
query = """
    SELECT MODEL, count() as usage_count, sum(TOTAL_COST) as total_cost
    FROM OPENROUTER_TRACES
    GROUP BY MODEL
    ORDER BY usage_count DESC
"""
result = client.query(query)

for row in result.result_rows:
    print(f"Model: {row[0]}, Count: {row[1]}, Cost: ${row[2]:.4f}")
```

## Related tools / concepts
- [OpenRouter](../ai_knowledge/openrouter.md) (Log streaming source)
- [Snowflake](snowflake.md)
- [Datadog](datadog.md)
- [S3 / S3-Compatible Storage](../intake_storage/s3-storage.md)
- [Langfuse](langfuse.md)

## Sources / references
- [Official Website](https://clickhouse.com/)
- [ClickHouse Documentation](https://clickhouse.com/docs/en/intro)
- [OpenRouter Broadcast to ClickHouse](https://openrouter.ai/docs/guides/features/broadcast/clickhouse)

## Contribution Metadata
- Last reviewed: 2026-05-18
- Confidence: high
