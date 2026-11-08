# ClickHouse

## What it is
ClickHouse is an open-source, ultra-high-performance, column-oriented SQL database management system (DBMS) engineered specifically for Online Analytical Processing (OLAP). Designed to store and query multi-terabyte to petabyte-scale datasets with sub-second query latency, it serves as a premier analytical store for high-volume telemetry, event logs, agent execution traces, vector evaluations, and real-time observability in modern AI and software engineering ecosystems in early 2027.

Unlike traditional row-oriented transactional databases (e.g. PostgreSQL, MySQL) that process records row-by-row, ClickHouse stores data sequentially by column. This layout allows for extreme data compression, massive vectorized query execution, and high-throughput streaming ingestion capable of handling millions of insert events per second per node.

```
+---------------------------------------------------------------------------------------------------+
|                              CLICKHOUSE OLAP TELEMETRY ARCHITECTURE                               |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|   |  Telemetry Ingestion  |     |  ClickHouse Node      |     |  Storage Engine (MergeTree)   |   |
|   |                       |     |                       |     |                               |   |
|   | - LiteLLM / OpenRouter| --> | - Vectorized Engine   | --> | - Columnar Compression (ZSTD) |   |
|   | - OTel Collector      |     | - Primary Index / MinMax|   | - Primary Sort Key Index      |   |
|   | - FastMCP 3.1 Trace   |     | - JSON Materialized Path|   | - Partitions by Date / Month  |   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|                                                                               |                   |
|                                                                               v                   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|   |  Analytics & MCP      |     |  Query Processing     |     |  Data Access Layer            |   |
|   |                       |     |                       |     |                               |   |
|   | - Langfuse / Helicone | <-- | - FastMCP 3.1 Tool    | <-- | - Sub-Second Aggregations     |   |
|   | - Grafana / Dashboards|     | - Pydantic v2 Schema  |     | - SIMD Vectorized Scans       |   |
|   | - AI Cost Auditing    |     | - Token Spend Metrics |     | - Distributed Shard Query     |   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

## What problem it solves
Modern autonomous agent fleets, multi-agent frameworks ([Autogen](../../tools/frameworks/autogen.md), [LangGraph](../../tools/frameworks/langgraph.md)), and API gateways ([OpenRouter](../ai_knowledge/openrouter.md), [LiteLLM](../../services/litellm.md)) generate vast amounts of structured telemetry data—including prompt histories, tool invocation parameters, token usage counts, latency metrics, and reasoning chain logs. Attempting to ingest and query these high-velocity streams in standard relational databases leads to storage bloat, I/O bottlenecks, and unacceptably slow analytical query performance.

ClickHouse solves these challenges through:
- **Columnar Storage & Vectorized Query Execution**: Scans and aggregations operate directly on continuous memory blocks using SIMD CPU instruction sets (AVX-512, AVX2, ARM Neon), achieving multi-gigabyte-per-second processing per CPU core.
- **Aggressive Compression Algorithms**: Specialized per-column compression codecs (LZ4, ZSTD, Gorilla, DoubleDelta, Delta) yield 5x to 12x storage reduction on structured text and log payloads.
- **Sub-Second Analytics at Scale**: Executes complex `GROUP BY` aggregations, percentiles, and filtering across billions of rows in milliseconds without requiring pre-aggregated summary tables.
- **High-Velocity Native Ingestion**: Supports streaming ingestion from Kafka, Vector, OpenTelemetry collectors, or HTTP/gRPC pipelines with zero query lockup.

## Mathematical Formulations: Columnar Scans & Storage Compression

### 1. Vectorized SIMD Scan Acceleration Factor
In a row-oriented database, evaluating a filter predicate over column $c$ across $R$ records requires reading entire rows of size $W_{\text{row}} = \sum_{j=1}^{C} w_j$ bytes. In ClickHouse's columnar format, only the target column width $w_c$ is read from disk into CPU cache lines.

The theoretical I/O reduction factor $\mathcal{R}_{\text{I/O}}$ is formulated as:

$$
\mathcal{R}_{\text{I/O}} = \frac{R \cdot W_{\text{row}}}{R \cdot w_c} = \frac{\sum_{j=1}^{C} w_j}{w_c}
$$

For a typical LLM telemetry schema where $W_{\text{row}} \approx 1,024\text{ bytes}$ and $w_{\text{tokens}} = 4\text{ bytes}$, $\mathcal{R}_{\text{I/O}} = 256\times$.

Furthermore, SIMD vectorization processes $V$ elements per CPU clock cycle (e.g., $V = 16$ 32-bit integers on AVX-512 registers). The effective query execution throughput $\Phi_{\text{scan}}$ is:

$$
\Phi_{\text{scan}} = \frac{f_{\text{CPU}} \cdot V}{\text{CPI}_{\text{SIMD}}} \cdot \mathcal{B}_{\text{comp\_factor}}
$$

Where $f_{\text{CPU}}$ is the clock frequency and $\text{CPI}_{\text{SIMD}}$ is cycles per instruction.

### 2. Block Compression Entropy & Space Savings
ClickHouse partitions columns into compressed granules (typically 8,192 physical rows). The Shannon entropy $\mathcal{H}(C)$ of discrete column symbols determines theoretical compressibility:

$$
\mathcal{H}(C) = -\sum_{s \in \mathcal{S}} p(s) \log_2 p(s)
$$

For repetitive telemetry fields (e.g., `model`, `provider`, `status_code`), $\mathcal{H}(C) \ll 2.5\text{ bits/value}$. Applying ZSTD/LZ4 block encoding reduces physical disk consumption according to:

$$
\mathcal{S}_{\text{disk}} = \sum_{g=1}^{G} \text{len}\left( \text{Codec}\left( \text{Granule}_g \right) \right) \approx \frac{R \cdot \mathcal{H}(C)}{8} + \mathcal{O}(G)
$$

Yielding compression ratios $\rho_{\text{comp}} = \frac{\mathcal{S}_{\text{uncompressed}}}{\mathcal{S}_{\text{disk}}} \ge 8.5\times$ in production AI telemetry environments.

### 3. Sparse Index MinMax Pruning Bound
ClickHouse builds a sparse primary index storing 1 index mark every $M = 8,192$ rows. For a range query $[t_{\text{start}}, t_{\text{end}}]$, the number of granules scanned $G_{\text{scanned}}$ is bounded by:

$$
G_{\text{scanned}} \le \left\lceil \frac{R_{\text{matching}}}{M} \right\rceil + 2
$$

Eliminating up to 99.8% of unreferenced data blocks before reading data from persistent storage.

## Where it fits in the stack
**Data Storage and Analytics / AI Observability**. ClickHouse acts as the high-performance analytical storage foundation for AI telemetry, model evaluation benchmarks, LLM token billing, and agent execution tracking. Integrated via **FastMCP 3.1 / Model Context Protocol**, ClickHouse provides agents with high-speed SQL access to query real-time operational context, long-term memory logs, and system performance metrics.

## Analytical Telemetry Database Comparison Matrix

| Feature / Dimension | ClickHouse | PostgreSQL + TimescaleDB | DuckDB | InfluxDB 3.0 | Elasticsearch |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Architecture** | Distributed Columnar OLAP | Relational Row Store + Chunks | Embedded In-Process OLAP | Columnar Time-Series (Apache Arrow) | Distributed Inverted Index Document Store |
| **Ingestion Throughput** | > 1,500,000 rows/sec/node | ~ 150,000 rows/sec | ~ 400,000 rows/sec (single proc)| ~ 800,000 rows/sec | ~ 60,000 docs/sec |
| **Data Compression** | 6x - 14x (Columnar Codecs) | 3x - 5x | 4x - 8x | 5x - 10x (Parquet) | 1.5x - 2.5x (Lucene indexes) |
| **Memory Footprint** | Fixed daemon pool (1–4GB min) | Moderate (256MB–2GB) | Zero daemon (< 50MB embedded) | High (2–8GB min) | Very High (JVM heap 8–32GB) |
| **Protocol Support** | HTTP, Native TCP, FastMCP 3.1 | Postgres wire protocol | Local C / Python ABI bindings | HTTP InfluxQL / Flight SQL | REST JSON HTTP |
| **Best Suited For** | Billion-row AI traces & token billing | Small to mid-tier mixed OLTP/OLAP | Local agent scratchpad analytics | Pure metric time-series streams | Full-text token and log search |

## Typical use cases
- **AI Agent Telemetry & Log Archiving**: Archiving complete LLM requests, completions, prompt tokens, completion tokens, latency, and tool invocation parameters for models like **Claude 5.6**, **GPT-5.6**, and **Qwen 3.8**.
- **Observability Backend Store**: Serving as the primary data store for open-source AI engineering suites such as [Langfuse](langfuse.md), [Helicone](helicone.md), or SigNoz.
- **Real-Time AI Token Cost & Budget Auditing**: Executing live aggregations across billions of trace logs to analyze model token spend, cost per user, and department budget allocations.
- **Vector & Hybrid Analytical Search**: Storing embedding vectors alongside rich structured metadata for filtered similarity search and real-time hybrid retrieval.

## Strengths
- **Unrivaled Analytical Throughput**: Native support for vectorized execution engines and SIMD instructions makes ClickHouse one of the fastest open-source DBMSs for aggregations.
- **High Compression Ratios**: Column-specific encoding codecs significantly reduce cloud storage footprints and disk I/O demands.
- **Dynamic Structural JSON Support**: Modern JSON data types dynamically parse and index nested LLM payload objects without schema migration locks.
- **OpenTelemetry Standard Alignment**: Direct schema compatibility with OpenTelemetry collectors allows seamless drop-in deployment into standard enterprise observability stacks.

## Limitations
- **Not Suitable for OLTP**: ClickHouse is explicitly not designed for point lookups, single-row updates, transactional ACID guarantees, or high-frequency row deletes.
- **Primary Sorting Key Sensitivity**: Query performance is tightly bound to table primary sorting key ordering; non-indexed query access patterns require full table scans.
- **Operational Complexity**: Managing distributed sharding tables, ZooKeeper/Keeper consensus clusters, and replication topologies requires specialized database administrative knowledge.

## When to use it
- When your AI infrastructure processes millions of daily model invocations and requires live sub-second analytical reporting.
- When building self-hosted AI billing gateways, token analytics platforms, or agent observability stacks.
- When long-term log retention costs must be minimized through columnar compression algorithms.

## When not to use it
- As a transactional application database for user accounts, state management, or order processing (use PostgreSQL or MySQL).
- For small-scale projects (< 5 GB total log volume per month) where SQLite or PostgreSQL is simpler to maintain.
- When workload requirements demand complex multi-table ACID transactions across multiple records.

## Getting Started

### Deploying via Docker Compose
Run a ClickHouse server with persistent storage and HTTP/Native client ports enabled:

```yaml
version: '3.8'
services:
  clickhouse:
    image: clickhouse/clickhouse-server:24.8-alpine
    container_name: clickhouse-server
    ports:
      - "8123:8123" # HTTP REST Interface
      - "9000:9000" # Native TCP Client
    volumes:
      - clickhouse_data:/var/lib/clickhouse
      - clickhouse_logs:/var/log/clickhouse-server
    environment:
      CLICKHOUSE_DB: ai_telemetry
      CLICKHOUSE_USER: admin
      CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT: 1
    restart: unless-stopped

volumes:
  clickhouse_data:
  clickhouse_logs:
```

### Enterprise Telemetry Table Schema (MergeTree Engine)
```sql
CREATE DATABASE IF NOT EXISTS ai_telemetry;

CREATE TABLE IF NOT EXISTS ai_telemetry.llm_traces (
    timestamp DateTime64(3, 'UTC') DEFAULT now64(3),
    trace_id UUID DEFAULT generateUUIDv4(),
    model LowCardinality(String),
    provider LowCardinality(String),
    user_id String,
    prompt_tokens UInt32 CODEC(DoubleDelta, ZSTD),
    completion_tokens UInt32 CODEC(DoubleDelta, ZSTD),
    total_tokens UInt32 CODEC(DoubleDelta, ZSTD),
    cost_usd Float64 CODEC(Gorilla, ZSTD),
    latency_ms UInt32 CODEC(T64, ZSTD),
    status_code UInt16 CODEC(T64, ZSTD),
    request_payload String CODEC(ZSTD(6)),
    response_payload String CODEC(ZSTD(6)),
    metadata JSON,
    INDEX idx_model model TYPE set(100) GRANULARITY 2,
    INDEX idx_user user_id TYPE bloom_filter(0.01) GRANULARITY 1
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (timestamp, provider, model, user_id)
TTL timestamp + INTERVAL 180 DAY DELETE;
```

## CLI Examples

### Native Client Querying
Query average latency and total token consumption grouped by model using the `clickhouse-client`:

```bash
clickhouse-client --database="ai_telemetry" --query="
    SELECT
        model,
        count() as total_requests,
        round(avg(latency_ms), 2) as avg_latency_ms,
        sum(total_tokens) as aggregate_tokens,
        round(sum(cost_usd), 4) as aggregate_cost_usd
    FROM llm_traces
    WHERE timestamp >= now() - INTERVAL 7 DAY
    GROUP BY model
    ORDER BY aggregate_tokens DESC;
"
```

### Inspecting Storage Compression Ratios
Evaluate disk compression efficiency across database tables:

```bash
clickhouse-client --query="
    SELECT
        table,
        formatReadableSize(sum(data_compressed_bytes)) AS compressed,
        formatReadableSize(sum(data_uncompressed_bytes)) AS uncompressed,
        round(sum(data_uncompressed_bytes) / sum(data_compressed_bytes), 2) AS ratio
    FROM system.parts
    WHERE active AND database = 'ai_telemetry'
    GROUP BY table;
"
```

## API examples

```python
import clickhouse_connect

client = clickhouse_connect.get_client(host='localhost', port=8123, username='admin', password='')
result = client.query("SELECT model, count() FROM ai_telemetry.llm_traces GROUP BY model")
print("Model usage counts:", result.result_rows)
```

## FastMCP 3.1 Tool Implementation & Pydantic v2 Integration

The following Python script defines a complete FastMCP 3.1 tool server providing an analytical interface to ClickHouse for AI agents, backed by strict Pydantic v2 schemas:

```python
import clickhouse_connect
from datetime import datetime
from typing import List, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ConfigDict

# Initialize FastMCP 3.1 Server
mcp = FastMCP("ClickHouseAnalyticsServer", version="3.1.0")

class ModelUsageSummary(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    model: str = Field(..., min_length=1, description="Name of the evaluated AI model")
    provider: str = Field(..., min_length=1, description="LLM hosting provider (e.g. Anthropic, OpenAI)")
    total_requests: int = Field(..., ge=0, description="Total number of completed requests")
    avg_latency_ms: float = Field(..., ge=0.0, description="Average response latency in milliseconds")
    p95_latency_ms: float = Field(..., ge=0.0, description="95th percentile response latency in milliseconds")
    total_tokens: int = Field(..., ge=0, description="Sum of prompt and completion tokens")
    total_cost_usd: float = Field(..., ge=0.0, description="Total computed cost in USD")

class AnalyticsQueryRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    days_back: int = Field(7, ge=1, le=90, description="Number of past days to aggregate")
    min_requests: int = Field(1, ge=1, description="Minimum request threshold to filter results")

class QueryResultWrapper(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    query_timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    record_count: int = Field(..., ge=0)
    results: List[ModelUsageSummary] = Field(default_factory=list)

@mcp.tool()
def query_llm_cost_analytics(days_back: int = 7, min_requests: int = 1) -> str:
    """
    FastMCP tool that queries ClickHouse for aggregate LLM token usage, cost, and latency metrics.
    Returns JSON formatted array of ModelUsageSummary objects.
    """
    client = clickhouse_connect.get_client(
        host="localhost",
        port=8123,
        username="admin",
        password=""
    )

    query = f"""
        SELECT
            model,
            provider,
            count() as total_requests,
            round(avg(latency_ms), 2) as avg_latency,
            round(quantile(0.95)(latency_ms), 2) as p95_latency,
            sum(total_tokens) as total_tokens,
            round(sum(cost_usd), 4) as total_cost
        FROM ai_telemetry.llm_traces
        WHERE timestamp >= now() - INTERVAL {days_back} DAY
        GROUP BY model, provider
        HAVING total_requests >= {min_requests}
        ORDER BY total_cost DESC
    """

    result = client.query(query)

    summaries: List[ModelUsageSummary] = []
    for row in result.result_rows:
        summary = ModelUsageSummary(
            model=row[0],
            provider=row[1],
            total_requests=row[2],
            avg_latency_ms=row[3],
            p95_latency_ms=row[4],
            total_tokens=row[5],
            total_cost_usd=row[6]
        )
        summaries.append(summary)

    wrapper = QueryResultWrapper(record_count=len(summaries), results=summaries)
    return wrapper.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

## Systemd Service Unit (`clickhouse-analytics-mcp.service`)

Hardened systemd unit configuration for enterprise Linux deployments hosting the ClickHouse FastMCP analytical daemon:

```ini
[Unit]
Description=ClickHouse FastMCP 3.1 Analytics Gateway Daemon
After=network.target clickhouse-server.service
Wants=network-online.target

[Service]
Type=simple
User=clickhouse
Group=clickhouse
WorkingDirectory=/opt/clickhouse-mcp
Environment="PYTHONUNBUFFERED=1"
Environment="CLICKHOUSE_HOST=127.0.0.1"
Environment="CLICKHOUSE_PORT=8123"
ExecStart=/usr/bin/python3 /opt/clickhouse-mcp/server.py
Restart=always
RestartSec=5s
StandardOutput=journal
StandardError=journal
SyslogIdentifier=clickhouse-mcp-daemon

# Hardened Security Restrictions
ProtectSystem=strict
ProtectHome=true
NoNewPrivileges=true
PrivateTmp=true
LimitNOFILE=1048576

[Install]
WantedBy=multi-user.target
```

## Advanced Performance & Sharding Optimization

### 1. Partitioning Strategies for High-Velocity Logs
ClickHouse performance relies heavily on effective partition key design. For high-volume AI trace tables:
- **Partition Key**: `PARTITION BY toYYYYMM(timestamp)` balances part file counts while maintaining fast date-range pruning.
- **Primary Sorting Key**: `ORDER BY (timestamp, provider, model, user_id)` aligns with the most common query filtering patterns, minimizing disk seeks.
- **Data TTL**: Expire or move historical log data to lower-cost S3 / object storage tiers automatically using table lifecycle expressions:
  ```sql
  ALTER TABLE ai_telemetry.llm_traces
  MODIFY TTL timestamp + INTERVAL 30 DAY TO VOLUME 's3_cold_storage',
             timestamp + INTERVAL 365 DAY DELETE;
  ```

### 2. Materialized Views for Real-Time Pre-Aggregation
To serve sub-millisecond analytics dashboards without re-scanning raw trace tables:
```sql
CREATE TABLE IF NOT EXISTS ai_telemetry.daily_model_stats (
    date Date,
    model String,
    provider String,
    request_count SimpleAggregateFunction(sum, UInt64),
    tokens_sum SimpleAggregateFunction(sum, UInt64),
    cost_sum SimpleAggregateFunction(sum, Float64)
) ENGINE = AggregatingMergeTree()
ORDER BY (date, provider, model);

CREATE MATERIALIZED VIEW IF NOT EXISTS ai_telemetry.mv_daily_model_stats
TO ai_telemetry.daily_model_stats AS
SELECT
    toDate(timestamp) AS date,
    model,
    provider,
    count() AS request_count,
    sum(total_tokens) AS tokens_sum,
    sum(cost_usd) AS cost_sum
FROM ai_telemetry.llm_traces
GROUP BY date, model, provider;
```

### 3. Distributed Cluster Sharding DDL
For multi-node enterprise deployments handling over 100 million daily agent traces across regional clusters:

```sql
-- Create distributed table pointing across cluster shards
CREATE TABLE IF NOT EXISTS ai_telemetry.llm_traces_distributed ON CLUSTER 'ai_cluster'
AS ai_telemetry.llm_traces
ENGINE = Distributed('ai_cluster', 'ai_telemetry', 'llm_traces', rand());

-- Fast aggregate query across all cluster shards
SELECT
    provider,
    model,
    count() AS shard_requests,
    round(quantile(0.99)(latency_ms), 2) AS p99_latency_ms,
    round(sum(cost_usd), 2) AS total_usd
FROM ai_telemetry.llm_traces_distributed
WHERE timestamp >= now() - INTERVAL 24 HOUR
GROUP BY provider, model
ORDER BY total_usd DESC;
```

## Diagnostic & Troubleshooting Matrix

| Issue Code | Symptom | Diagnostic Command | Remediation Procedure |
| :--- | :--- | :--- | :--- |
| `ERR_TOO_MANY_PARTS` | Ingestion aborted: "Too many parts in all data in table" | `clickhouse-client -q "SELECT count() FROM system.parts WHERE active"` | Buffer small inserts using Vector/Kafka or buffer engine; never execute single-row `INSERT` statements. |
| `ERR_MAX_EXECUTION_TIME`| Analytics query times out after 60s | `clickhouse-client -q "SHOW PROCESSLIST"` | Verify query uses table sort key prefix (`timestamp`); avoid full table regex scans across payload text. |
| `ERR_MEMORY_LIMIT_EXCEEDED`| `DB::Exception: Memory limit (for query) exceeded` | `clickhouse-client -q "SELECT peak_memory_usage FROM system.query_log ORDER BY event_time DESC LIMIT 5"` | Increase `max_bytes_before_external_group_by` to spill intermediate hash tables to disk. |
| `ERR_CONNECTION_REFUSED`| HTTP 8123 or Native 9000 unreachable | `ss -tulpn \| grep -E '8123\|9000'` | Verify `<listen_host>0.0.0.0</listen_host>` is uncommented in `/etc/clickhouse-server/config.xml`. |
| `ERR_CORRUPT_PART` | Part checksum mismatch detected during merge | `clickhouse-client -q "SELECT * FROM system.detached_parts"` | Restore from backup replica or attach detached parts with `ALTER TABLE ... ATTACH PART`. |
| `ERR_ZOOKEEPER_DROP` | ReplicatedMergeTree enters read-only state | `clickhouse-client -q "SELECT is_readonly FROM system.replicas"` | Inspect ClickHouse Keeper / ZooKeeper ensemble quorum connectivity and journal latency. |
| `ERR_STORAGE_FULL` | Disk volume capacity reaches 95% threshold | `df -h /var/lib/clickhouse` | Trigger cold storage migration policies or execute `ALTER TABLE ... DROP PARTITION 'YYYYMM'`. |
| `ERR_FASTMCP_RPC` | FastMCP analytics query returns socket timeout | `journalctl -u clickhouse-analytics-mcp -n 30` | Check database credentials and ensure query specifies strict date boundary filters (`days_back <= 30`). |

## Related tools / concepts
- [OpenRouter](../ai_knowledge/openrouter.md): Unified AI model gateway providing high-throughput streaming events.
- [Langfuse](langfuse.md): Open-source LLM observability platform using ClickHouse as its analytical storage backend.
- [LiteLLM](../../services/litellm.md): Multi-provider proxy router logging directly into ClickHouse engines.
- [OpenTelemetry Collector](opentelemetry-collector.md): Standardized telemetry ingestion pipeline component.
- [Helicone](helicone.md): Enterprise AI LLM gateway and telemetry platform.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md): Protocol connecting autonomous agents to analytical data stores.

## Sources / references
- [ClickHouse Official Documentation](https://clickhouse.com/docs/en/intro)
- [ClickHouse Architecture and Storage Engines](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/mergetree)
- [Langfuse ClickHouse Integration Design](https://langfuse.com/docs/analytics)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
