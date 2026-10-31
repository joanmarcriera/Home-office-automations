# Logfire

## What it is
**Logfire** is Pydantic's enterprise observability, structured tracing, and telemetry platform tailored specifically for Python applications, FastAPI microservices, and multi-agent LLM pipelines. Built natively on top of OpenTelemetry standards and backed by a high-performance, columnar ClickHouse database engine, Logfire provides zero-boilerplate, high-density visibility into Pydantic v2 data validation hierarchies, SQL database queries, HTTP client transactions, and agentic tool invocation spans.

Unlike traditional logging infrastructure that treats events as unstructured text strings or detached JSON objects, Logfire treats execution state as interactive, tree-structured span graphs. Every Pydantic model validation failure, LLM token chunk, vector database query, and FastMCP 3.1 protocol message is captured with microsecond precision and mapped to standard OpenTelemetry semantic conventions.

## What problem it solves
Modern multi-agent architectures and asynchronous microservices introduce deep visual complexity and failure opacity:
- **Nested Agent Execution Opacity**: Debugging multi-step agent loops, tool calling recursions, and fallback paths is notoriously difficult using standard text logs. Logfire automatically renders tool calls, LLM prompt payloads, and completion spans in an interactive hierarchy.
- **Data Schema & Validation Drift**: Debugging schema mismatch errors across API boundaries often requires logging sensitive payloads or writing custom exception middleware. Logfire instruments Pydantic v2 model instantiation directly, capturing exact validation error locations, input payloads, and schema diffs.
- **Telemetry Configuration Fatigue**: Configuring OpenTelemetry collectors, span processors, metric readers, and OTLP exporters usually demands hundreds of lines of boilerplate code. Logfire simplifies this down to `logfire.configure()` with automated library hooks.
- **Vendor Lock-in Risk**: Proprietary tracing SDKs trap observability data inside single SaaS silos. Logfire is 100% OpenTelemetry native; spans can be routed simultaneously to self-hosted Jaeger/Grafana instances, Datadog, or the Logfire Cloud console.

## Architecture & Data Flow

```mermaid
sequenceDiagram
    autonumber
    actor Client as FastMCP 3.1 Client
    participant FastAPI as FastAPI Gateway
    participant Pydantic as Pydantic v2 Runtime
    participant Agent as Pydantic AI / LLM
    participant Logfire as Logfire SDK / OTLP
    participant ClickHouse as ClickHouse DB / UI

    Client->>FastAPI: POST /api/v1/agent/run
    FastAPI->>Logfire: Auto-instrumentation (HTTP Span Start)
    FastAPI->>Pydantic: Validate AgentTaskRequest
    Pydantic-->>Logfire: Capture Model Schema & Validation Span
    FastAPI->>Agent: Execute Agent Tool Workflow
    Agent->>Logfire: Start Span "agent.tool_call" (prompt, tokens)
    Agent-->>FastAPI: Return Validated Result
    FastAPI->>Logfire: HTTP Span End (200 OK)
    Logfire->>Logfire: Batch Spans via Async OTLP Exporter
    Logfire->>ClickHouse: Stream OTLP Protobuf Spans (ClickHouse Ingestion)
    ClickHouse-->>Client: Visual Trace Tree & SQL Dashboard
```

## Where it fits in the stack
**Category**: Process Understanding / Observability & Telemetry. Operating at the **Telemetry & Observability Layer**, Logfire acts as the central nervous system connecting Python execution runtimes, FastMCP 3.1 agent nodes, web frameworks ([FastAPI](../frameworks/fastapi.md)), and model orchestrators ([Pydantic AI](../frameworks/pydantic-ai.md), [Instructor](../frameworks/instructor.md)) to local or enterprise cloud dashboards.

## Key Features & Functional Modules
- **Auto-Instrumentation Matrix**: One-line hook support for `fastapi`, `httpx`, `requests`, `openai`, `anthropic`, `sqlalchemy`, `psycopg`, `asyncio`, and `pydantic`.
- **High-Performance SQL Search**: Query trace spans directly in the cloud console or local CLI using standard ANSI SQL syntax powered by ClickHouse.
- **Pydantic v2 Deep Inspection**: Inspect individual model fields, schema validation rules, default value overrides, and serialization timings.
- **OpenTelemetry Standard Compliance**: Export data seamlessly via standard OTLP over HTTP/Protobuf or gRPC to any OTLP-compliant collector.
- **FastMCP 3.1 Protocol Tracing**: Instrument Model Context Protocol servers to log client session handshakes, tool registrations, and resource requests.
- **Adaptive Sampling & Tail Latency Rules**: Filter high-volume healthcheck pings while guaranteeing 100% retention on span error traces and slow LLM generations.
- **Integrated Sensitive Data Masking**: Native regex and Pydantic field-level redaction rules to prevent API keys and PII from leaving runtime boundaries.

## Typical use cases
- **Multi-Agent Execution Tracing**: Visualizing agent tool calling cascades, memory retrieval spans, and prompt token usage in real time.
- **API Schema Debugging**: Identifying real-time field validation errors and bad payload requests in FastAPI microservices.
- **Database Query Performance Auditing**: Tracking SQL query latency, parameter binding, and connection pool starvation across SQLAlchemy or AsyncPG sessions.
- **Production LLM Cost Tracking**: Aggregating input/output token counts and API costs across Anthropic, OpenAI, and local vLLM model routes.
- **Cross-Service Trace Propagation**: Correlating incoming user HTTP web requests down to sub-agent FastMCP function calls using W3C trace context headers.

## Strengths
- **Native Pydantic v2 Integration**: Captures rich validation telemetry without custom wrapper functions.
- **Zero-Boilerplate Setup**: Auto-configures standard library loggers (`logging`, `structlog`, `loguru`) to emit structured trace spans.
- **OpenTelemetry Native**: Guarantees zero vendor lock-in through standardized OTLP protocol formats.
- **Interactive Tree Visualization**: High-density UI designed specifically for software engineers and ML engineers.
- **Local Dev Console**: Provides zero-cloud local web dashboard for fast offline agent debugging.

## Limitations
- **Python Ecosystem Primacy**: Full auto-instrumentation capabilities are tailored primarily for Python runtimes.
- **SaaS Retention Limits**: Free cloud tiers enforce fixed rate limits and retention windows unless self-hosting or exporting via OTLP.
- **Sampling Strategy Configuration**: High-throughput distributed systems require explicit tail-sampling rules to avoid excess telemetry volume.

## When to use it
- When developing Python applications using Pydantic, Pydantic AI, FastAPI, or FastMCP 3.1.
- When requiring detailed validation error telemetry and nested span trees for AI workflows.
- When standardizing enterprise observability on OpenTelemetry-compliant infrastructure.

## When not to use it
- For non-Python software stacks (e.g., pure TypeScript/Node.js or Go microservices).
- When simple stdout file logging without trace aggregation or dashboard visualization meets all requirements.

## Systemd Service Configuration
When self-hosting an OpenTelemetry Collector or local Logfire OTLP relay daemon on Linux servers, systemd manages background exporter services:

```ini
[Unit]
Description=Logfire OTLP Telemetry Collector Service
After=network.target

[Service]
Type=simple
User=logfire
Group=logfire
WorkingDirectory=/opt/logfire
Environment="PATH=/opt/logfire/venv/bin:/usr/local/bin:/usr/bin"
Environment="LOGFIRE_PROJECT_NAME=enterprise-agent-core"
Environment="LOGFIRE_TOKEN=lfr_live_xxxxxxxxxxxx"
Environment="LOGFIRE_ADVANCED_OTLP_ENDPOINT=http://127.0.0.1:4318"
ExecStart=/opt/logfire/venv/bin/python3 -m logfire_collector_daemon
Restart=always
RestartSec=5s
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

## Docker Compose Multi-Container Stack
For organizations hosting an on-premise OpenTelemetry collection infrastructure with ClickHouse storage and local Logfire OTLP ingestion:

```yaml
version: "3.8"

services:
  otel-collector:
    image: otel/opentelemetry-collector-contrib:0.105.0
    container_name: logfire-otel-collector
    restart: unless-stopped
    command: ["--config=/etc/otelcol-contrib/config.yaml"]
    volumes:
      - ./otel-config.yaml:/etc/otelcol-contrib/config.yaml:ro
    ports:
      - "4317:4317"   # OTLP gRPC receiver
      - "4318:4318"   # OTLP HTTP receiver
      - "8888:8888"   # Collector internal metrics
    depends_on:
      clickhouse:
        condition: service_healthy
    networks:
      - telemetry-net

  clickhouse:
    image: clickhouse/clickhouse-server:24.3-alpine
    container_name: logfire-clickhouse-db
    restart: unless-stopped
    ports:
      - "8123:8123"   # HTTP interface
      - "9000:9000"   # Native protocol
    environment:
      - CLICKHOUSE_DB=logfire_telemetry
      - CLICKHOUSE_USER=logfire_admin
      - CLICKHOUSE_PASSWORD=SecureClickhousePass2027!
    volumes:
      - clickhouse_data:/var/lib/clickhouse
    networks:
      - telemetry-net
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:8123/ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis-cache:
    image: redis:7-alpine
    container_name: logfire-span-cache
    restart: unless-stopped
    command: ["redis-server", "--maxmemory", "512mb", "--maxmemory-policy", "volatile-lru"]
    ports:
      - "6379:6379"
    networks:
      - telemetry-net
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

networks:
  telemetry-net:
    driver: bridge

volumes:
  clickhouse_data:
```

## OpenTelemetry Collector Configuration (`otel-config.yaml`)
Connecting self-hosted multi-agent runtimes to ClickHouse storage and secondary OTLP sinks:

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 5s
    send_batch_size: 10000
  memory_limiter:
    check_interval: 1s
    limit_percentage: 75
    spike_limit_percentage: 20

exporters:
  clickhouse:
    endpoint: tcp://clickhouse:9000?database=logfire_telemetry&username=logfire_admin&password=SecureClickhousePass2027!
    ttl: 720h
    compress: lz4
  logging:
    loglevel: warn

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [clickhouse, logging]
```

## Configuration & Feature Summary

| Feature / Setting | Parameter / Env Variable | Default Value | Description |
| :--- | :--- | :--- | :--- |
| Project Identifier | `LOGFIRE_PROJECT_NAME` / `project_name` | None | Defines the destination project in the Logfire dashboard. |
| Write Token | `LOGFIRE_TOKEN` / `token` | None | Secret API write token for authentication. |
| OTLP Endpoint | `LOGFIRE_ADVANCED_OTLP_ENDPOINT` | Logfire Cloud | Custom OTLP collector URL for self-hosted Jaeger/Grafana setups. |
| Console Output | `console` | `ConsoleOptions()` | Controls terminal stdout/stderr rich output formatting. |
| Pydantic Plugin | `pydantic_plugin` | Enabled | Auto-instruments all Pydantic v2 model instantiations. |
| Code Source Logging | `code_source` | Enabled | Captures code line numbers and Git commit metadata with spans. |

## Getting started

### Installation
Install the Logfire SDK alongside Pydantic v2 and FastAPI dependencies:
```bash
pip install "logfire[fastapi,httpx,openai,pydantic]"
```

### Authentication & CLI Verification
Authenticate your development environment with your Logfire account:
```bash
logfire auth
```

### Initializing Logfire in Python
Initialize Logfire at the application entry point:
```python
import logfire

# Configure project and auto-instrumentation options
logfire.configure(
    project_name="enterprise-agent-core",
    send_to_logfire=True,
)
logfire.info("Logfire instrumentation initialized successfully.")
```

## CLI examples

### 1. Authenticate Environment
```bash
logfire auth
```

### 2. Verify Logfire Setup & Connectivity
```bash
logfire check
```

### 3. List Active Logfire Projects
```bash
logfire projects list
```

### 4. Query Spans via CLI SQL Interface
```bash
logfire query "SELECT span_name, duration_ms, attributes FROM spans WHERE duration_ms > 500 LIMIT 10"
```

## API examples

### 1. FastAPI & Pydantic v2 Model Validation Tracing
The following example demonstrates instrumenting a FastAPI application with Pydantic v2 validation schema tracking and custom span context:

```python
import logfire
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import List, Optional

# Initialize Logfire
logfire.configure(project_name="agent-gateway-service")

app = FastAPI(title="Logfire-Instrumented Agent Gateway")
logfire.instrument_fastapi(app)
logfire.instrument_pydantic()

class TaskSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str = Field(..., description="Unique alphanumeric identifier")
    description: str = Field(..., min_length=5, max_length=500)
    priority: int = Field(default=1, ge=1, le=5)
    assignee_email: EmailStr

class WorkflowResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str
    status: str
    processed_steps: int
    execution_time_sec: float

@app.post("/v1/tasks/run", response_model=WorkflowResult)
async def run_agent_task(payload: TaskSpec):
    with logfire.span("agent.task_execution", task_id=payload.task_id, priority=payload.priority) as span:
        logfire.info("Starting task execution for {email}", email=payload.assignee_email)

        if payload.priority == 5:
            logfire.warn("High priority task detected: {task_id}", task_id=payload.task_id)

        # Simulate business logic processing
        steps_completed = 4
        execution_time = 0.42

        span.set_attribute("steps_completed", steps_completed)
        span.set_attribute("execution_time", execution_time)

        return WorkflowResult(
            task_id=payload.task_id,
            status="completed",
            processed_steps=steps_completed,
            execution_time_sec=execution_time
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

### 2. FastMCP 3.1 Multi-Agent Tool Tracing & Pydantic AI Integration
This pattern illustrates tracing FastMCP 3.1 agent tool invocations, structured output schemas, and custom OTLP span metrics with strict Pydantic v2 schemas (`extra="forbid"`):

```python
import asyncio
import logfire
from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Any, List
from mcp.server.fastmcp import FastMCP

mcp_server = FastMCP("LogfireFastMCPTracingServer")

# Configure Logfire with custom OTLP exporter support
logfire.configure(
    project_name="fastmcp-agent-server",
    pydantic_plugin=logfire.PydanticPlugin(record="all")
)

class MCPToolParams(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str = Field(..., description="Search query string")
    max_results: int = Field(default=5, ge=1, le=20)
    filters: Dict[str, str] = Field(default_factory=dict)
    include_metadata: bool = Field(default=True)

class MCPToolResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str
    matches_found: int
    data: List[str]
    latency_ms: float

@mcp_server.tool()
async def execute_kb_vector_search(raw_params_json: str) -> str:
    """FastMCP 3.1 tool handler instrumented with Logfire OpenTelemetry spans."""
    with logfire.span("fastmcp.tool_invocation", tool_name="kb_vector_search") as span:
        # Validate parameters through Pydantic v2
        params = MCPToolParams.model_validate_json(raw_params_json)
        span.set_attribute("validated_query", params.query)
        span.set_attribute("max_results", params.max_results)

        logfire.info("Executing FastMCP 3.1 tool with query: {query}", query=params.query)

        # Simulate external vector DB query
        start_ts = asyncio.get_event_loop().time()
        await asyncio.sleep(0.05)
        results = ["doc_101", "doc_202", "doc_303"][:params.max_results]
        elapsed = (asyncio.get_event_loop().time() - start_ts) * 1000

        response = MCPToolResponse(
            query=params.query,
            matches_found=len(results),
            data=results,
            latency_ms=round(elapsed, 2)
        )
        logfire.info("FastMCP tool completed successfully. Matches: {count}", count=response.matches_found)
        return response.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp_server.run()
```

## Diagnostic & Troubleshooting Matrix

| Symptom / Issue | Root Cause | Diagnostic Command / Log Check | Resolution Strategy |
| :--- | :--- | :--- | :--- |
| **Spans Missing in Logfire UI** | Invalid `LOGFIRE_TOKEN` or blocked outbound OTLP HTTP/4318 connection | `logfire check` / verify standard error logs for 401 Unauthorized | Run `logfire auth` to generate new token or verify firewall allows outbound HTTPS to `logfire-api.pydantic.dev`. |
| **High Memory / Overhead in Async Loop** | Unbatched span processing overloading asyncio event loop | Check OTLP exporter batch queue settings in `logfire.configure()` | Enable background batching processors (`send_to_logfire=True`) or adjust sampling rate for high-frequency logs. |
| **Pydantic Validation Spans Truncated** | Record mode set to `minimal` or `summary` instead of `all` | Check `logfire.configure(pydantic_plugin=...)` setup | Set `pydantic_plugin=logfire.PydanticPlugin(record='all')` to capture full model payload attributes. |
| **Duplicate Spans in Multi-Process Workers** | Forked Gunicorn/Uvicorn processes sharing single Logfire client instance | Check tracer provider initialization in worker process logs | Call `logfire.configure()` inside post-fork worker hooks (`post_fork` in Gunicorn config) rather than root module. |
| **OTLP gRPC Backpressure & Dropped Spans** | Collector buffer queue overflow under high LLM token streaming load | Inspect collector metrics at `:8888/metrics` for `otelcol_exporter_enqueue_failed_spans` | Scale OTLP collector replicas, increase `queue_size` in batch processor, or configure local Redis buffering. |
| **ClickHouse Ingestion Saturation** | Micro-batch inserts creating excessive tiny parts in ClickHouse merge tree | Query `SELECT count() FROM system.parts WHERE active` | Configure OTLP collector ClickHouse exporter with `timeout: 5s` and `send_batch_size: 10000` to buffer block inserts. |

## Related tools / concepts
- [Datadog](datadog.md) — Enterprise APM and log management platform.
- [OpenTelemetry Collector](opentelemetry-collector.md) — Standardized vendor-neutral telemetry proxy.
- [Pydantic AI](../frameworks/pydantic-ai.md) — Production agent framework built on Pydantic v2.
- [FastAPI](../frameworks/fastapi.md) — Asynchronous Python web framework.
- [Instructor](../frameworks/instructor.md) — Structured LLM outputs library powered by Pydantic.
- [W&B Weave](wandb-weave.md) — LLM evaluation and trace logging system.

## Sources / references
- [Pydantic Logfire Official Documentation](https://docs.pydantic.dev/logfire/)
- [Pydantic Logfire GitHub Repository](https://github.com/pydantic/logfire)
- [FastAPI Observability Guide with Logfire](https://fastapi.tiangolo.com/tutorial/telemetry/)
- [OpenTelemetry Python SDK Documentation](https://opentelemetry.io/docs/languages/python/)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
