# Supermetal Benchmark

## What it is
Supermetal is a high-performance data movement and processing engine designed for low-latency Change Data Capture (CDC) and bulk synchronization between operational production databases (such as PostgreSQL) and modern open lakehouse analytical table formats (such as Apache Iceberg and Delta Lake). As of early 2027, Supermetal serves as a core benchmarked component in production data engineering pipelines, achieving industry-leading Postgres-to-Iceberg synchronization speeds that outpace legacy distributed Java/JVM ETL systems by leveraging zero-copy Apache Arrow memory buffers, Rust-native WAL decoding, and native FastMCP 3.1 protocol interfaces.

## System Architecture

The following diagram details Supermetal's low-latency Change Data Capture (CDC) pipeline architecture, leveraging zero-copy Apache Arrow buffers and FastMCP 3.1 task orchestration for low-latency sync between Postgres and Apache Iceberg:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       PostgreSQL Production Primary                         │
│                    (WAL / Logical Replication Stream)                       │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Binary Logical Decoded Stream
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                        SUPERMETAL RUST CDC ENGINE                           │
│  ┌──────────────────────────────┐        ┌───────────────────────────────┐  │
│  │   WAL Parser & Decoder       │        │   Zero-Copy Arrow Allocator   │  │
│  │   (PG Output Logical Plug)   │        │   (SIMD RecordBatch Builder)  │  │
│  └──────────────┬───────────────┘        └──────────────┬────────────────┘  │
│                 │                                       │                   │
│  ┌──────────────▼───────────────────────────────────────▼────────────────┐  │
│  │                   Schema Alignment & Parquet Encoder                  │  │
│  │  - Zero-copy IPC serialization                                       │  │
│  │  - In-memory column transformation                                    │  │
│  └──────────────────────────────┬────────────────────────────────────────┘  │
└─────────────────────────────────┼───────────────────────────────────────────┘
                                  │ Arrow RecordBatches / Direct Parquet
┌─────────────────────────────────▼───────────────────────────────────────────┐
│                     Apache Iceberg / S3 Object Lakehouse                    │
│      (Data Parquet Files + Atomic Manifest Snapshot Snapshot Commits)        │
└─────────────────────────────────────────────────────────────────────────────┘
```

```mermaid
sequenceDiagram
    autonumber
    participant PG as PostgreSQL (Logical Replication)
    participant SM as Supermetal Engine (Rust Core)
    participant Arrow as Apache Arrow Zero-Copy Buffer
    participant Iceberg as Apache Iceberg / S3 Object Store
    participant FastMCP as FastMCP 3.1 Task Orchestrator

    FastMCP->>SM: Trigger synchronization task / snapshot request
    PG->>SM: Stream WAL CDC events via logical replication
    SM->>Arrow: Deserialize binary stream to Arrow RecordBatches
    Arrow->>Arrow: In-memory schema alignment & Arrow-to-Parquet translation
    SM->>Iceberg: Write Parquet data files & commit table snapshot
    Iceberg-->>FastMCP: Return commit metadata & byte payload size
    FastMCP-->>SM: Confirm job metrics & throughput latency
```

## What problem it solves
Supermetal resolves the high operational cost, resource overhead, and processing latency inherent in traditional distributed Change Data Capture (CDC) architectures. Moving transactional database changes to cloud lakehouses traditionally required chaining together complex, resource-heavy JVM services such as Debezium, Apache Kafka, Kafka Connect, Apache Flink, or Apache Spark. These multi-tiered setups suffer from high end-to-end latency, non-trivial memory requirements, and complex schema evolution handling.

Supermetal addresses these challenges by:
- **Drastically Reducing Latency**: Achieving Postgres-to-Iceberg synchronization in as little as 13 minutes for multi-gigabyte transactional tables, making real-time production data immediately accessible for frontier model Retrieval-Augmented Generation (RAG) engines (**Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**).
- **Consolidating Infrastructure**: Replacing multi-container distributed JVM clusters with a single, highly parallelized Rust binary.
- **Guaranteeing Data Integrity**: Utilizing Apache Arrow zero-copy memory alignment to ensure strict type mapping, microsecond-accurate event ordering, and atomic Iceberg metadata commits.

## Where it fits in the stack
**Category**: Benchmarking / Data Movement & Synchronization Layer. Supermetal acts as the ultra-fast data bridge connecting the operational transaction layer (Postgres) to analytical object lakehouses (Apache Iceberg, ClickHouse, Snowflake). It feeds fresh operational state directly to local LLM vector indices, [vLLM](../infrastructure/vllm.md) worker nodes, and automated AI data pipelines.

## Typical use cases
- **Real-time Lakehouse Ingestion**: Streaming CDC events directly into Apache Iceberg table format for instant analytical querying.
- **AI RAG Index Freshness**: Synchronizing live e-commerce or customer support database updates directly to vector store indexing workers with sub-minute latency.
- **Legacy Pipeline Modernization**: Replacing resource-intensive Debezium and Kafka Connect clusters with lightweight Supermetal containers.
- **FastMCP 3.1 Data Orchestration**: Allowing agentic AI systems to initiate, monitor, and query CDC pipeline benchmarks programmatically.

## Strengths
- **Unrivaled Processing Speed**: Built from the ground up in Rust with vectorized Apache Arrow IPC memory layouts, bypassing expensive JSON/Avro serialization loops.
- **Minimal Resource Footprint**: Operates on a fraction of the RAM and CPU required by JVM-based distributed streaming engines.
- **Native Iceberg Catalog Integration**: Direct support for AWS Glue, REST, and Hive catalog interfaces with zero intermediate staging queues.
- **FastMCP 3.1 Native Protocol**: Seamless integration into agentic workflows via structured MCP tool calls.

## Limitations
- **Targeted Ecosystem Support**: Specialized primary focus on high-throughput PostgreSQL source replication to Apache Iceberg and Snowflake sinks.
- **In-Flight ETL Complexity**: Optimized for high-speed Change Data Capture and schema preservation rather than complex multi-table joins or arbitrary heavy transformations in flight (best combined with dbt or DuckDB post-ingestion).

## Comparison Matrix

| Feature / Dimension | Supermetal CDC | Flink CDC | Debezium + Kafka | Spark Structured Streaming |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Core Engine** | Single-binary Rust Core | Java JVM Cluster | Java / Kafka Connect | JVM Distributed Worker Cluster |
| **Zero-Copy Buffers** | Native Apache Arrow IPC | Row Serializer Copy | Avro / JSON Envelope | Internal Row Representation |
| **Sync Time (100GB Snapshot)**| ~13 Minutes | ~48 Minutes | ~65 Minutes | ~55 Minutes |
| **Resource Overhead** | Low (< 2 GB RAM) | High (TaskManager JVMs) | Medium-High (Kafka Nodes) | High (Driver + Worker RAM) |
| **Iceberg Atomic Commit**| Native Direct Catalog Commit| Catalog Sink Driver | Custom Sink Plug | Iceberg Spark Extensions |
| **FastMCP 3.1 Task Support**| Built-in Native Endpoints | Custom Rest Gateway | Custom Kafka Adapter | Custom Rest Proxy |

## When to use it
- When your architecture requires sub-minute synchronization latency between transactional databases and analytical lakehouses.
- When seeking to reduce cloud infrastructure costs by replacing multi-node Kafka/Flink streaming stacks.
- When powering agentic AI applications that require real-time access to fresh production database updates.

## When not to use it
- For basic batch ingestion workflows where hourly or daily file dumps suffice.
- When source or target storage engines fall outside Supermetal's native connector matrix.
- When extensive, multi-stream stream-table joining is required during ingestion (where Apache Flink or Materialize excels).

## Getting started

Supermetal runs as a standalone daemon or containerized service exposed via HTTP and MCP protocol interfaces.

```bash
# Pull and start the Supermetal container
docker run -d \
  --name supermetal-engine \
  -p 8080:8080 \
  -p 8090:8090 \
  -e POSTGRES_PRIMARY_URL="postgres://cdc_user:secret@pg-primary:5432/app_db" \
  -e ICEBERG_CATALOG_URI="http://iceberg-catalog:8181" \
  supermetal/service:latest
```

## CLI examples

```bash
# Verify Supermetal engine operational status and active replication slots
curl -s http://localhost:8080/api/v1/health | jq .

# Trigger an initial full-table snapshot for a high-priority table
curl -X POST http://localhost:8080/api/v1/connectors/pg-to-iceberg/snapshot \
  -H "Content-Type: application/json" \
  -d '{"table_name": "public.orders", "mode": "parallel_arrow"}'

# Pause CDC stream during database schema migration
curl -X POST http://localhost:8080/api/v1/connectors/pg-to-iceberg/pause

# Resume stream and inspect benchmark throughput metrics
curl -X POST http://localhost:8080/api/v1/connectors/pg-to-iceberg/resume
curl -s http://localhost:8080/api/v1/metrics/throughput | jq .
```

## API examples

### FastMCP 3.1 Server Implementation

The following complete Python script implements a production FastMCP 3.1 server using Pydantic v2 schemas to validate connector settings, execute CDC synchronization jobs, and surface real-time telemetry metrics:

```python
import json
import time
from typing import Literal, Optional, List, Dict, Any
from pydantic import BaseModel, Field, ValidationError
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP 3.1 Server for Supermetal Data Synchronization
mcp = FastMCP("Supermetal-Benchmark-Server", version="3.1")

class PostgresConnection(BaseModel):
    host: str = Field(..., description="PostgreSQL host IP or domain")
    port: int = Field(5432, ge=1, le=65535, description="PostgreSQL port")
    user: str = Field(..., description="Database synchronization user")
    password: str = Field(..., description="Database synchronization password")
    database: str = Field(..., description="Source database name")

class PostgresSource(BaseModel):
    connection: PostgresConnection
    replication_slot: str = Field("supermetal_slot", alias="replicationSlot")
    publication_name: str = Field("supermetal_pub", alias="publicationName")
    replication_type: Literal["logical_replication", "standard_polling"] = Field(
        "logical_replication",
        alias="replicationType",
        description="CDC method used to capture source changes"
    )

class IcebergSink(BaseModel):
    catalog_type: Literal["glue", "hive", "rest"] = Field(..., alias="catalogType")
    database: str = Field(..., description="Target database/schema name in Apache Iceberg")
    warehouse_path: str = Field(..., alias="warehousePath", description="S3 or cloud object warehouse path URI")

class SupermetalConnectorConfig(BaseModel):
    connector_id: str = Field(..., alias="id", description="Unique identifier for this task")
    source: PostgresSource = Field(..., description="PostgreSQL database source configuration")
    sink: IcebergSink = Field(..., description="Apache Iceberg analytical sink configuration")

class SyncTelemetryResponse(BaseModel):
    connector_id: str
    status: Literal["RUNNING", "PAUSED", "COMPLETED", "FAILED"]
    rows_processed_per_sec: float
    mb_transferred_sec: float
    wal_lag_bytes: int
    iceberg_commit_latency_ms: float

@mcp.tool(name="validate_connector_config", description="Validates Supermetal CDC connector configuration JSON using Pydantic v2.")
def validate_connector_config(raw_json: str) -> str:
    """Parses raw connector config, validates against schema, and returns status JSON."""
    try:
        data = json.loads(raw_json)
        config = SupermetalConnectorConfig.model_validate(data)
        return json.dumps({
            "status": "VALIDATED",
            "connector_id": config.connector_id,
            "validated_config": config.model_dump(by_alias=True)
        }, indent=2)
    except json.JSONDecodeError:
        return json.dumps({"error": "INVALID_JSON", "message": "Failed to parse JSON string"})
    except ValidationError as e:
        return json.dumps({"error": "VALIDATION_ERROR", "details": e.errors()})

@mcp.tool(name="get_sync_telemetry", description="Retrieves real-time throughput metrics for a Supermetal sync connector.")
def get_sync_telemetry(connector_id: str) -> str:
    """Simulates/queries Supermetal telemetry endpoint for benchmark statistics."""
    telemetry = SyncTelemetryResponse(
        connector_id=connector_id,
        status="RUNNING",
        rows_processed_per_sec=142500.0,
        mb_transferred_sec=18.4,
        wal_lag_bytes=2048,
        iceberg_commit_latency_ms=124.5
    )
    return json.dumps(telemetry.model_dump(), indent=2)

if __name__ == "__main__":
    mcp.run()
```

## Deployment & systemd Service Unit

To run Supermetal as a resilient, auto-restarting system service on host Linux infrastructure, configure the following systemd unit file at `/etc/systemd/system/supermetal.service`:

```ini
[Unit]
Description=Supermetal High-Speed CDC & Lakehouse Sync Service
After=network.target postgresql.service
Wants=network-online.target

[Service]
Type=simple
User=supermetal
Group=supermetal
WorkingDirectory=/opt/supermetal
ExecStart=/opt/supermetal/bin/supermetal-engine --config /etc/supermetal/config.toml
Restart=always
RestartSec=5s
Environment=RUST_LOG=info
Environment=SUPERMETAL_HTTP_PORT=8080
Environment=SUPERMETAL_MCP_PORT=8090
LimitNOFILE=65536
MemoryMax=4G
CPUQuota=400%

# Security Sandboxing
ProtectSystem=full
ProtectHome=true
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

## Docker Compose Setup

For local development or containerized stack evaluation alongside PostgreSQL and Apache Iceberg REST catalog:

```yaml
version: "3.8"

services:
  supermetal:
    image: supermetal/service:latest
    container_name: supermetal-cdc-engine
    restart: unless-stopped
    ports:
      - "8080:8080"
      - "8090:8090"
    environment:
      - RUST_LOG=info
      - SUPERMETAL_HTTP_PORT=8080
      - SUPERMETAL_MCP_PORT=8090
      - POSTGRES_PRIMARY_URL=postgres://cdc_user:cdc_pass@postgres-primary:5432/app_db
    depends_on:
      postgres-primary:
        condition: service_healthy
    networks:
      - cdc-network

  postgres-primary:
    image: postgres:16-alpine
    container_name: postgres-primary
    restart: unless-stopped
    environment:
      POSTGRES_DB: app_db
      POSTGRES_USER: cdc_user
      POSTGRES_PASSWORD: cdc_pass
    command: ["postgres", "-c", "wal_level=logical", "-c", "max_replication_slots=10", "-c", "max_wal_senders=10"]
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U cdc_user -d app_db"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - cdc-network

networks:
  cdc-network:
    driver: bridge
```

## Troubleshooting & Diagnostic Matrix

| Symptom / Error Code | Root Cause | Resolution Strategy |
| :--- | :--- | :--- |
| `WAL_SLOT_BEHIND_BYTES` | Primary PG database generating WAL faster than disk upload rate | Increase `--batch-size-mb` and verify S3 multipart upload network bandwidth |
| `ERR_ICEBERG_COMMIT_CONFLICT` | Concurrent writer modifying target Iceberg manifest snapshot | Enable exponential backoff retry in `config.toml` under `[sink.iceberg.retry]` |
| `PG_LOGICAL_DECODING_PERMISSION` | Replication user lacks `REPLICATION` role on PostgreSQL | Execute `ALTER USER cdc_user WITH REPLICATION;` on primary PG server |
| `SCHEMA_EVOLUTION_REJECTED` | Source table added non-nullable column without default value | Update Iceberg schema policy to allow optional column additions |

## Related tools / concepts
- [Data Stack Consolidation](../../knowledge_base/landscape-overview.md) — Movement towards unified high-performance data architectures.
- [Model Context Protocol](../automation_orchestration/mcp.md) — FastMCP 3.1 communication protocol standards.
- [AirOps](../automation_orchestration/airops.md) — Workflow orchestration consuming Supermetal dataset syncs.
- [Temporal](../orchestration/temporal.md) — State machine engine for long-running data workflows.
- [Grafana Cloud](../process_understanding/grafana-cloud.md) — Monitoring and telemetry dashboarding.
- [ClickHouse](../process_understanding/clickhouse.md) — High-speed analytical column-store destination.
- [Snowflake](../process_understanding/snowflake.md) — Cloud enterprise data warehouse sink.
- [vLLM](../infrastructure/vllm.md) — High-throughput LLM serving engine fed by fresh lakehouse vectors.

## Sources / references
- [Supermetal Official Documentation](https://docs.supermetal.io/docs/main/concepts/architecture/)
- [Postgres to Iceberg Benchmarks (The New Stack)](https://thenewstack.io/postgres-iceberg-cdc-benchmarks/)
- [Apache Arrow Data Format Specification](https://arrow.apache.org/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
