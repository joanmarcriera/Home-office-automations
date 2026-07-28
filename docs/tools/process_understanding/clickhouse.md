# ClickHouse

## What it is
ClickHouse is an open-source, high-performance, column-oriented SQL database management system (DBMS) designed for Online Analytical Processing (OLAP). It is engineered to handle massive datasets and return query results in real-time, making it a premier choice for high-volume telemetry, event ingestion, and log analysis in complex AI ecosystems as of late 2026.

## What problem it solves
Traditional row-oriented databases (like PostgreSQL) struggle with storage bloat and slow aggregation queries when processing millions of nested trace records or model outputs. ClickHouse solves this through:
- **Ultra-Fast Query Speed**: Columnar storage layout and vectorized execution engines perform deep scans and aggregations at gigabytes-per-second rates.
- **Aggressive Data Compression**: Standard compression algorithms (LZ4, ZSTD, and specialized double-delta codecs) achieve up to 10x savings on structured log data.
- **High-Concurrency Ingestion**: Seamlessly processes millions of insert events per second, facilitating uninterrupted logging for highly-active agents like **Claude 5.1** or **GPT-5.5**.
- **Real-Time Structured Queries**: Returns sub-second aggregations across billions of rows, eliminating performance gaps in telemetry backends.

## Where it fits in the stack
**Data Storage and Analytics**. ClickHouse acts as the high-performance analytical store for LLM traces, prompt logs, token usage, and latency metrics in the AI Observability layer. With **Model Context Protocol (MCP 3.1)**, it is often configured as a structured corporate memory repository from which agents retrieve real-time context.

## Typical use cases
- **AI Agent Telemetry Storage**: Archiving complete request, response, and tool-invocation trace histories from models like **Llama 4** or **Qwen 3.6**.
- **Observability Backend Consolidation**: Powering self-hosted telemetry tools like [Langfuse](langfuse.md) or [Helicone](helicone.md) that require low-latency indexing of deep nested calls.
- **AI Cost & Budget Auditing**: Executing complex aggregations across distributed logs to monitor live token spend and request counts per user or department.
- **Vector and Hybrid Search**: Performing rapid retrieval evaluations when indexing embeddings alongside relational metadata.

## Strengths
- **Optimized for Heavy Analytical Scans**: Highly optimized for column-wise functions like `avg()`, `sum()`, and `count()`.
- **Horizontal Scalability**: Native master-to-master replication and sharding configurations support petabyte-scale storage clusters.
- **Standardized Ingestion Hooks**: Native support for standard schemas via collectors like [OpenTelemetry Collector](opentelemetry-collector.md).
- **Flexible JSON Support**: Handles dynamic, deeply-nested JSON structures directly in columns without requiring complex schema migrations.

## Limitations
- **Not Suited for Transactional Workloads**: ClickHouse is not designed for frequent point-updates or individual row deletes (OLTP).
- **High Operational Overload**: Managing production sharding, partition schemes, and backup procedures requires specialized database expertise.
- **Sorting-Key Dependency**: Query speed is heavily bound to primary key selections, making poorly indexed query patterns highly inefficient.

## When to use it
- When your AI applications generate hundreds of thousands of daily model traces and require live, interactive monitoring dashboards.
- When building custom internal AI billing or governance gateways and standard transactional databases suffer from latency bottlenecks.
- When long-term log retention costs must be minimized through efficient compression.
- When logging raw data streams directly from [OpenRouter](../ai_knowledge/openrouter.md) for future model distillation or fine-tuning workflows.

## When not to use it
- For standard application databases where frequent CRUD (Create, Read, Update, Delete) transactional operations are dominant.
- For small-scale systems (under a few gigabytes of logging monthly) where a simple, lightweight PostgreSQL or SQLite database is sufficient.
- When a fully-managed SaaS observability platform like [Datadog](datadog.md) or cloud telemetry satisfies your auditing requirements without custom host configurations.

## Getting started

### Installation (via Docker)
Deploy a ClickHouse server locally for testing or self-hosting:

```bash
docker run -d \
    --name clickhouse-server \
    -p 8123:8123 \
    -p 9000:9000 \
    -v clickhouse_data:/var/lib/clickhouse \
    clickhouse/clickhouse-server
```

### OpenRouter Trace Schema
The following table is optimized for storing stream records broadcasted from OpenRouter:

```sql
CREATE TABLE IF NOT EXISTS OPENROUTER_TRACES (
    timestamp DateTime64(3, 'UTC'),
    id String,
    model String,
    app_id Nullable(String),
    user_id Nullable(String),
    prompt_tokens UInt32,
    completion_tokens UInt32,
    total_tokens UInt32,
    total_cost Float64,
    latency_ms Float64,
    status String,
    request String,
    response String,
    -- Optimized sorting key for time and model-based queries
    INDEX idx_model model TYPE minmax GRANULARITY 3
) ENGINE = MergeTree()
ORDER BY (timestamp, model);
```

## CLI examples

### Basic DB Connection and Querying
Query total recorded traces using the native ClickHouse client:
```bash
clickhouse-client --query "SELECT count() FROM OPENROUTER_TRACES"
```

### Check Storage Efficiency and Size
Examine compressed bytes versus real storage footprints:
```bash
clickhouse-client --query "SELECT table, formatReadableSize(sum(data_compressed_bytes)) AS size FROM system.parts WHERE table = 'OPENROUTER_TRACES' GROUP BY table"
```

### Direct JSON Ingestion
Stream JSON lines directly into ClickHouse tables:
```bash
cat traces.jsonl | clickhouse-client --query "INSERT INTO OPENROUTER_TRACES FORMAT JSONEachRow"
```

## API examples

### Python (clickhouse-connect) with Pydantic v2
Connect to ClickHouse and retrieve average latencies comparing models like **GPT-5.5** versus **Claude 5.1**:

```python
import clickhouse_connect
from pydantic import BaseModel

class ModelLatencyMetric(BaseModel):
    model: str
    avg_latency_ms: float
    request_count: int

# Establish client connection
client = clickhouse_connect.get_client(host='localhost', port=8123)

# Analytical query comparing model speeds
query = """
    SELECT
        model,
        avg(latency_ms) as avg_latency,
        count() as request_count
    FROM OPENROUTER_TRACES
    GROUP BY model
    HAVING request_count > 100
    ORDER BY avg_latency DESC
    LIMIT 5
"""

result = client.query(query)

# Parse and display using validated Pydantic structures
for row in result.result_rows:
    metric = ModelLatencyMetric(model=row[0], avg_latency_ms=row[1], request_count=row[2])
    print(f"Model: {metric.model} | Avg: {metric.avg_latency_ms:.1f}ms | Count: {metric.request_count}")
```

### Node.js Integration
Asynchronously ingest model trace event objects using the official Node.js client:

```javascript
const { createClient } = require('@clickhouse/client');

const client = createClient({
  host: process.env.CLICKHOUSE_HOST || 'http://localhost:8123',
  username: 'default',
  password: '',
  database: 'default',
});

async function logModelTrace(traceObject) {
  await client.insert({
    table: 'OPENROUTER_TRACES',
    values: [traceObject],
    format: 'JSONEachRow',
  });
}
```

## Related tools / concepts
- [OpenRouter](../ai_knowledge/openrouter.md) - Unified model routing gateway.
- [Langfuse](langfuse.md) - Open-source AI engineering and observability suite.
- [Snowflake](snowflake.md) - Cloud-native data warehouse and analytics platform.
- [Datadog](datadog.md) - Full-stack cloud monitoring service.
- [OpenTelemetry Collector](opentelemetry-collector.md) - High-throughput telemetry pipeline.
- [PostHog](posthog.md) - Open-source product analytics engine utilizing ClickHouse.
- [S3 / S3-Compatible Storage](../intake_storage/s3-storage.md) - High-efficiency backup and tier-two storage.
- [Helicone](helicone.md) - AI LLM gateway and observability dashboard.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) - Standard protocol for model integration.
- [Claude](../ai_knowledge/claude.md) - Frontier language model suite.
- [Llama 4 Maverick](../ai_knowledge/local_llms.md) - Advanced local open-weight model framework.

## Sources / references
- [ClickHouse Official Documentation](https://clickhouse.com/docs/en/intro)
- [ClickHouse Observability Integration Guide](https://clickhouse.com/docs/en/use-cases/observability)
- [OpenRouter ClickHouse Logging Guide](https://openrouter.ai/docs/guides/features/broadcast/clickhouse)

## Contribution Metadata
- Last reviewed: 2026-11-01
- Confidence: high
