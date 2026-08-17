# ClickHouse

## What it is
ClickHouse is an open-source, ultra-high-performance, column-oriented SQL database management system (DBMS) engineered for Online Analytical Processing (OLAP). Designed to handle massive multi-terabyte datasets and return query results in real-time, it serves as a premier analytical store for high-volume telemetry, event ingestion, agent trace logs, and vector evaluation in modern AI ecosystems in early 2027.

## What problem it solves
Traditional row-oriented transactional databases (like PostgreSQL or MySQL) struggle with storage bloat and latency spikes when aggregating millions of deeply nested trace records, LLM prompt histories, or tool execution logs. ClickHouse solves this through:
- **Ultra-Fast Query Speed**: Columnar storage layout and vectorized execution engines process scans and aggregations at multi-gigabyte-per-second throughput per CPU core.
- **Aggressive Data Compression**: Specialized compression codecs (LZ4, ZSTD, Gorilla, DoubleDelta) achieve up to 10x storage savings on structured log data.
- **High-Concurrency Ingestion**: Seamlessly ingests millions of insert events per second, facilitating real-time trace logging for high-throughput autonomous agent fleets powered by **Claude 5.1**, **GPT-5.5**, and **Llama 4**.
- **Sub-Second Analytics**: Executes analytical queries across billions of rows in milliseconds, powering real-time observability dashboards.

## Where it fits in the stack
**Data Storage and Analytics**. ClickHouse acts as the high-performance analytical engine for LLM telemetry, agent prompt logs, token cost tracking, and latency metrics in the AI Observability layer. Integrated via **FastMCP 3.1 / Model Context Protocol**, it is frequently used as a structured corporate memory repository from which autonomous agents query real-time analytical context.

## Typical use cases
- **AI Agent Telemetry Storage**: Archiving complete request, response, thought chain, and tool invocation traces from models like **Claude 5.1**, **GPT-5.5**, and **Qwen 3.8**.
- **Observability Backend Storage**: Serving as the analytical database backend for open-source AI telemetry tools like [Langfuse](langfuse.md) or [Helicone](helicone.md).
- **AI Cost & Budget Auditing**: Executing distributed aggregations across telemetry logs to track real-time token spend and cost allocation across departments or models.
- **Vector and Hybrid Search**: Storing low-dimensional vector embeddings alongside rich structured metadata for fast hybrid analytical filtering.

## Strengths
- **Analytical Optimizations**: Highly optimized vectorized functions for real-time aggregation functions like `avg()`, `quantile()`, `sum()`, and `count()`.
- **Horizontal Scalability**: Master-to-master replication and automatic sharding configurations support petabyte-scale analytical clusters.
- **OpenTelemetry Standard Ingestion**: Direct native schema compatibility with collectors like [OpenTelemetry Collector](opentelemetry-collector.md).
- **Dynamic JSON Handling**: Native, high-performance JSON data types handle dynamic nested LLM payloads directly without requiring complex schema migrations.

## Limitations
- **Not Suited for OLTP**: ClickHouse is not designed for frequent point updates, single-row deletes, or complex transactional ACID constraints.
- **Operational Complexity**: Configuring sharding keys, partition schemes, and replication topologies requires specialized database engineering.
- **Sorting-Key Dependency**: Query execution speed is heavily bound to primary sorting key definitions; poorly indexed query patterns degrade performance.

## When to use it
- When your AI infrastructure generates millions of daily model traces and requires live, sub-second interactive analytics.
- When building internal AI billing, governance, or security audit gateways where standard relational databases encounter latency bottlenecks.
- When long-term log retention costs must be minimized through column-oriented compression.
- When logging raw data streams directly from [OpenRouter](../ai_knowledge/openrouter.md) or [LiteLLM](../../services/litellm.md) for offline model distillation.

## When not to use it
- For core application databases dominated by frequent point reads and transactional CRUD operations (use PostgreSQL or MySQL).
- For small-scale projects (under a few gigabytes of logging monthly) where PostgreSQL or SQLite is sufficient.
- When a fully-managed SaaS telemetry platform eliminates the need for self-hosted database infrastructure.

## Getting started

### Installation (via Docker)
Deploy a ClickHouse server instance locally for testing or self-hosting:

```bash
docker run -d \
    --name clickhouse-server \
    -p 8123:8123 \
    -p 9000:9000 \
    -v clickhouse_data:/var/lib/clickhouse \
    clickhouse/clickhouse-server:latest
```

### LLM Telemetry Trace Schema
The following table schema is optimized for storing stream records from gateways like OpenRouter or LiteLLM:

```sql
CREATE TABLE IF NOT EXISTS OPENROUTER_TRACES (
    timestamp DateTime64(3, 'UTC'),
    trace_id String,
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
Examine compressed byte footprint versus uncompressed storage size:
```bash
clickhouse-client --query "SELECT table, formatReadableSize(sum(data_compressed_bytes)) AS compressed_size, formatReadableSize(sum(data_uncompressed_bytes)) AS raw_size FROM system.parts WHERE table = 'OPENROUTER_TRACES' GROUP BY table"
```

### Direct JSON Lines Ingestion
Stream JSON lines directly into ClickHouse tables:
```bash
cat traces.jsonl | clickhouse-client --query "INSERT INTO OPENROUTER_TRACES FORMAT JSONEachRow"
```

## API examples

### Python (clickhouse-connect) with Pydantic v2
Connect to ClickHouse and compute model latency and token metrics across **GPT-5.5** versus **Claude 5.1**:

```python
import clickhouse_connect
from pydantic import BaseModel, Field

class ModelLatencyMetric(BaseModel):
    model: str = Field(description="Name of the evaluated model")
    avg_latency_ms: float = Field(description="Average latency in milliseconds")
    total_tokens: int = Field(description="Sum of all processed tokens")
    request_count: int = Field(description="Total request count")

# Establish client connection
client = clickhouse_connect.get_client(host='localhost', port=8123)

# Analytical query comparing model performance
query = """
    SELECT
        model,
        avg(latency_ms) as avg_latency,
        sum(total_tokens) as tokens_sum,
        count() as request_count
    FROM OPENROUTER_TRACES
    GROUP BY model
    HAVING request_count > 10
    ORDER BY avg_latency DESC
    LIMIT 5
"""

result = client.query(query)

# Parse and validate using Pydantic v2
for row in result.result_rows:
    metric = ModelLatencyMetric(
        model=row[0],
        avg_latency_ms=row[1],
        total_tokens=row[2],
        request_count=row[3]
    )
    print(f"Model: {metric.model} | Avg Latency: {metric.avg_latency_ms:.1f}ms | Tokens: {metric.total_tokens} | Requests: {metric.request_count}")
```

## Related tools / concepts
- [OpenRouter](../ai_knowledge/openrouter.md) - Unified model routing gateway.
- [Langfuse](langfuse.md) - Open-source AI engineering and observability suite using ClickHouse.
- [Snowflake](snowflake.md) - Cloud data warehouse and analytics platform.
- [OpenTelemetry Collector](opentelemetry-collector.md) - High-throughput telemetry pipeline.
- [Helicone](helicone.md) - AI LLM gateway and observability dashboard.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) - Protocol for connecting agents to data/tools.
- [Claude](../ai_knowledge/claude.md) - Frontier language model suite.

## Sources / references
- [ClickHouse Official Documentation](https://clickhouse.com/docs/en/intro)
- [ClickHouse Observability Integration Guide](https://clickhouse.com/docs/en/use-cases/observability)
- [OpenRouter ClickHouse Logging Guide](https://openrouter.ai/docs/guides/features/broadcast/clickhouse)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
