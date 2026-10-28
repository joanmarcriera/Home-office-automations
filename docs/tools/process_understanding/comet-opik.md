# Comet Opik

## What it is
Comet Opik is an open-source, enterprise-grade LLM observability, prompt engineering, tracing, and evaluation platform. Designed for evaluating, testing, and monitoring AI applications and autonomous multi-agent networks, Opik serves as a foundational component for "Evaluation-Driven Development" (EDD).

As of early 2027, Opik features native support for the **FastMCP 3.1 Task Protocol** and OpenTelemetry standards, delivering self-hostable, low-latency execution tracing and LLM-as-a-judge scoring across frontier models including **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, and **Gemma 4**.

```
+-----------------------------------------------------------------------------------+
|                               Comet Opik Core Platform                            |
|                                                                                   |
|  +-------------------------------------+   +-----------------------------------+  |
|  | OpenTelemetry Distributed Tracing   |   | FastMCP 3.1 Protocol Collector    |  |
|  | - Agentic Session & Span Tracking   |   | - Tool Call Execution Telemetry   |  |
|  | - Token Cost & Latency Collector    |   | - MCP Task Lifecycle Spans        |  |
|  +------------------+------------------+   +-----------------+-----------------+  |
|                     |                                        |                    |
|                     v                                        v                    |
|  +-----------------------------------------------------------------------------+  |
|  |             Evaluation Engine & Golden Dataset Benchmarking                 |  |
|  |  - Built-in Evaluators (Hallucination, Moderation, Answer Relevance)        |  |
|  |  - LLM-as-a-Judge Automation & Regression Testing                           |  |
|  +--------------------------------------+--------------------------------------+  |
|                                         |                                         |
+-----------------------------------------|-----------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                         High-Throughput Storage & UI Layer                        |
|                                                                                   |
|  +-----------------------------------+     +-----------------------------------+  |
|  | ClickHouse Trace Column Store     |     | PostgreSQL Project Metadata       |  |
|  +-----------------------------------+     +-----------------------------------+  |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Developing multi-agent systems and agentic RAG workflows without observability leads to hidden failures: silent model hallucinations, agent looping, prompt regressions between model versions (e.g. migrating from GPT-5 to GPT-5.6 or Claude 5.1 to Claude 5.6), and untracked API cost inflation.

Comet Opik addresses these production challenges by providing:
- **Full-Stack Execution Tracing**: Captures nested agentic reasoning steps, tool calls, raw prompts, and model responses in a visual execution tree.
- **Evaluation-Driven Development (EDD)**: Programmatically evaluates agent outputs against "Golden Datasets" using pre-built and custom LLM-as-a-judge scoring metrics.
- **Zero-Data-Leakage Self-Hosting**: Operates on-premise or in private cloud Kubernetes clusters using ClickHouse and PostgreSQL, eliminating third-party data privacy risks.
- **FastMCP 3.1 Telemetry Sync**: Automatically captures MCP tool inputs, outputs, and execution latencies across agent networks.

## Where it fits in the stack
**Category**: Process & Understanding / Observability & Evaluation. Comet Opik sits beside agent frameworks (LangChain, AutoGen, CrewAI, FastMCP 3.1) and model gateways (Portkey, LiteLLM), logging execution telemetry into ClickHouse storage.

```
+-----------------------------------------------------------------------------------+
|                       Agentic Applications & Workflows                            |
|                                                                                   |
|   +-----------------------+   +-----------------------+   +--------------------+  |
|   | FastMCP 3.1 Agent     |   | CrewAI Multi-Agent    |   | LangChain Pipeline |  |
|   +-----------+-----------+   +-----------+-----------+   +---------+----------+  |
|               |                           |                         |             |
|               +---------------------------+-------------------------+             |
|                                           |                                       |
|                                           v                                       |
|                    OpenTelemetry / Opik SDK Tracing Middleware                    |
+-------------------------------------------+---------------------------------------+
                                            |
                                            v
+-----------------------------------------------------------------------------------+
|                            Comet Opik Observability Server                        |
|                                                                                   |
|   +---------------------------------------------------------------------------+   |
|   | Distributed Span Ingestion, Evaluation Engine & Dataset Registry          |   |
|   +---------------------------------------+-----------------------------------+   |
+-------------------------------------------|---------------------------------------+
                                            |
                                            v
+-----------------------------------------------------------------------------------+
|                     ClickHouse DB / PostgreSQL / Web Dashboard                    |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Multi-Agent Execution Tracing**: Debugging complex tool invocation chains and nested agent loops in production.
- **Automated CI/CD Prompt Regression Testing**: Running evaluation suites against candidate prompts during pull request checks.
- **RAG Grounding & Hallucination Auditing**: Scoring retrieval faithfulness and answer relevance using automated evaluators.
- **LLM Token Cost & Latency Optimization**: Tracking expenditure across different model providers (Claude 5.6, GPT-5.6, DeepSeek-V4).

## Key technical features & FastMCP 3.1 integration
- **FastMCP 3.1 Protocol Collector**: Native instrumentation decorators (`@track`) capturing tool parameters, execution duration, and tool outputs.
- **ClickHouse Columnar Storage**: Engineered for sub-second query performance over tens of millions of trace spans.
- **Built-in Metric Evaluators**: Pre-packaged evaluators for Answer Relevance, Hallucination, Toxicity, Moderation, and Context Precision.
- **OpenTelemetry Standard**: Built on native OTEL trace span specifications for seamless integration with existing enterprise APM tools.

## Strengths
- **100% Open-Source & Self-Hostable**: Complete control over data storage with Docker and Kubernetes helm charts.
- **High-Throughput Analytics**: ClickHouse backend easily handles high-frequency agentic logging streams.
- **Native Evaluation Integration**: Unifies trace monitoring with offline dataset benchmarking in a single interface.
- **Developer-Centric SDK**: Simple Python decorator (`@track`) integration requiring zero boilerplate code changes.

## Limitations
- **Database Maintenance**: Self-hosted deployments require managing ClickHouse and PostgreSQL clusters.
- **Storage Growth**: High-frequency real-time logging requires active sampling and log retention policy management.

## When to use it
- When requiring a developer-centric, open-source LLM observability and tracing engine deployable on local machines or private cloud infrastructure.
- When building multi-agent pipelines requiring high-fidelity nested execution visualization and tool call debugging.
- When wanting a single, unified workflow that handles both early developer experimentation and production monitoring.

## When not to use it
- For basic or small scale scripts where raw console print statements are sufficient for tracking model behavior.
- If requiring a fully managed SaaS solution without using the Comet cloud platform or maintaining self-hosted ClickHouse infrastructure.

## Comparison Matrix

| Feature / Metric | Comet Opik | Langfuse | Arize Phoenix | Braintrust |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Target** | Open-Source Observability & EDD | Open-Source LLM Analytics | Enterprise Model Performance | AI Developer Platform |
| **Deployment Model** | Self-Hosted / Managed Cloud | Self-Hosted / Managed Cloud | Self-Hosted / Managed Cloud | Cloud SaaS / Enterprise |
| **Storage Engine** | ClickHouse + PostgreSQL | PostgreSQL | ClickHouse / DuckDB | Hosted Cloud Engine |
| **FastMCP 3.1 Support** | Native Protocol Collector | Extension Adapter | Custom Integration | Native Client SDK |
| **Evaluation Engine** | Built-in LLM-as-a-Judge | Built-in Scoring | Phoenix Evals | Custom Python Evals |
| **OpenTelemetry Native** | Yes | Yes | Yes | Partial |

## Getting started

### Self-Hosted Setup (Docker Compose)
```bash
git clone https://github.com/comet-ml/opik.git
cd opik/deployment/docker-compose
docker-compose up -d
```

### Python SDK Installation
```bash
pip install opik pydantic>=2.0.0
```

### Configure CLI Client
```bash
opik configure --api-key LOCAL_OPIK_KEY --url http://localhost:5173/api
```

## CLI examples

```bash
# Run Opik harbor evaluation suite against local agent
opik harbor run --dataset golden-qa-v1 --agent fastmcp-agent-v3

# Check Opik server connection status
opik status

# Export evaluation dataset to local JSON
opik dataset export --name customer-support-golden --output ./dataset.json
```

## API examples

### 1. Tracing FastMCP 3.1 Tool Invocation
```python
from opik import track
from typing import Dict, Any

@track(name="fastmcp_database_lookup")
def execute_mcp_db_tool(query_str: str, max_records: int = 5) -> Dict[str, Any]:
    """Instrumented tool call execution recorded automatically in Opik."""
    # Simulate DB query
    records = [{"id": 101, "status": "active", "query": query_str}]
    return {"status": "success", "count": len(records), "records": records}

@track(name="agent_reasoning_step")
def run_agent_loop(user_prompt: str) -> str:
    db_result = execute_mcp_db_tool(user_prompt, max_records=3)
    return f"Processed query '{user_prompt}' with result: {db_result}"

if __name__ == "__main__":
    response = run_agent_loop("Find active customer contracts")
    print(response)
```

### 2. FastMCP 3.1 Protocol Server with Opik Tracing
```python
import json
from typing import Dict, Any
from opik import track
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("opik-monitored-agent")

@mcp.tool()
@track(name="coveo_search_tool")
def search_knowledge_base(query: str, user_role: str = "engineer") -> Dict[str, Any]:
    """FastMCP 3.1 tool call tracked in Comet Opik trace timeline."""
    # Simulated search execution
    results = [
        {"title": "K8s Failover Guide", "relevance": 0.95},
        {"title": "Database Recovery Plan", "relevance": 0.88}
    ]
    return {
        "status": "success",
        "query": query,
        "user_role": user_role,
        "results": results
    }

if __name__ == "__main__":
    mcp.run()
```

### 3. Strict Pydantic v2 Evaluation Result Schema
```python
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator

class OpikSpanMetric(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., description="Metric identifier e.g. hallucination")
    score: float = Field(..., ge=0.0, le=1.0, description="Normalized score 0-1")
    reason: Optional[str] = Field(None, description="LLM-as-a-judge reasoning summary")

class OpikTracePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    trace_id: str = Field(..., min_length=8, description="Unique trace identifier")
    project_name: str = Field("default", description="Opik target project")
    input_prompt: str = Field(..., description="User input prompt")
    output_response: str = Field(..., description="Agent generated response")
    metrics: List[OpikSpanMetric] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("trace_id")
    @classmethod
    def validate_trace_id(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("trace_id cannot be blank")
        return v.strip()

# Example Validation
try:
    trace = OpikTracePayload(
        trace_id="tr_908234_opik",
        project_name="Customer-Support-Evaluation",
        input_prompt="What is the refund policy for hardware products?",
        output_response="Hardware refunds are allowed within 30 days of delivery.",
        metrics=[
            OpikSpanMetric(name="answer_relevance", score=0.98, reason="Directly answers user question."),
            OpikSpanMetric(name="hallucination", score=0.02, reason="Fully grounded in policy doc.")
        ],
        metadata={"fastmcp_version": "3.1", "environment": "production"}
    )
    print("Validated Opik Trace Payload:")
    print(trace.model_dump_json(indent=2))
except Exception as err:
    print(f"Validation error: {err}")
```

## Containerized Deployment & Docker Compose Setup

Production deployments of Comet Opik combine ClickHouse for trace span metrics, PostgreSQL for project relational metadata, and Redis for trace ingestion queues. The `docker-compose.yml` manifest below launches the complete self-hosted Opik stack:

```yaml
version: "3.8"

services:
  opik-backend:
    image: ghcr.io/comet-ml/opik-backend:v1.2.0
    container_name: opik-backend
    restart: unless-stopped
    ports:
      - "5173:5173"
    environment:
      - CLICKHOUSE_URL=clickhouse:8123
      - CLICKHOUSE_USERNAME=default
      - CLICKHOUSE_PASSWORD=clickhouse_secure_pass_2027
      - POSTGRES_URL=jdbc:postgresql://opik-postgres:5432/opik
      - POSTGRES_USER=opik
      - POSTGRES_PASSWORD=opik_db_password
      - REDIS_URL=redis://opik-redis:6379
      - OPIK_LOG_LEVEL=INFO
    depends_on:
      - clickhouse
      - opik-postgres
      - opik-redis
    networks:
      - opik-network

  clickhouse:
    image: clickhouse/clickhouse-server:24.3-alpine
    container_name: opik-clickhouse
    restart: unless-stopped
    ports:
      - "8123:8123"
      - "9000:9000"
    environment:
      - CLICKHOUSE_DB=opik
      - CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT=1
      - CLICKHOUSE_PASSWORD=clickhouse_secure_pass_2027
    volumes:
      - /opt/homelab/opik/clickhouse_data:/var/lib/clickhouse
    networks:
      - opik-network

  opik-postgres:
    image: postgres:16-alpine
    container_name: opik-postgres
    restart: unless-stopped
    environment:
      - POSTGRES_DB=opik
      - POSTGRES_USER=opik
      - POSTGRES_PASSWORD=opik_db_password
    volumes:
      - /opt/homelab/opik/postgres_data:/var/lib/postgresql/data
    networks:
      - opik-network

  opik-redis:
    image: redis:7-alpine
    container_name: opik-redis
    restart: unless-stopped
    networks:
      - opik-network

networks:
  opik-network:
    driver: bridge
```

## Systemd Service Unit Specification

When managing a standalone Opik backend service on host Linux nodes, the following systemd unit (`comet-opik.service`) manages startup sequencing and recovery:

```ini
[Unit]
Description=Comet Opik LLM Observability Backend Daemon
After=network.target clickhouse.service postgresql.service redis.service
Wants=clickhouse.service postgresql.service redis.service
Documentation=https://www.comet.com/docs/opik/

[Service]
Type=simple
User=opik
Group=opik
WorkingDirectory=/opt/homelab/opik
ExecStart=/usr/local/bin/opik-server --config /etc/opik/config.yaml
Restart=always
RestartSec=5s
Environment=PYTHONUNBUFFERED=1
Environment=CLICKHOUSE_URL=http://127.0.0.1:8123
Environment=POSTGRES_URL=postgresql://opik:opik_db_password@127.0.0.1:5432/opik
LimitNOFILE=65536
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
NoNewPrivileges=true
ProtectSystem=full
ProtectHome=true
ReadWritePaths=/var/log/opik

[Install]
WantedBy=multi-user.target
```

## Diagnostic & Troubleshooting Matrix

| Symptom / Error | Root Cause | Remediation Procedure |
| :--- | :--- | :--- |
| `ClickHouseConnectionError: DB::Exception` | ClickHouse server offline or password mismatch. | Verify ClickHouse container status (`docker logs opik-clickhouse`) and test connection (`curl http://localhost:8123/ping`). |
| `OpikTraceIngestTimeout (504 Gateway Timeout)` | Redis ingestion queue saturated under high FastMCP span volume. | Increase Redis memory limit or scale Opik backend workers in `docker-compose.yml`. |
| `MissingSpanMetrics: Hallucination Score Null` | LLM-as-a-judge evaluator API key missing or rate-limited. | Verify evaluator provider credentials in `/etc/opik/config.yaml` or enable local Ollama evaluator models. |
| `Database Migration Failed on Startup` | PostgreSQL schema version mismatch after version upgrade. | Execute manual migration (`opik-server migrate --config /etc/opik/config.yaml`) and check DB permissions. |

## Related tools / concepts
- **[Arize AI](arize-ai.md)**: Enterprise model performance management and Arize Phoenix.
- **[Langfuse](langfuse.md)**: Open-source LLM observability and analytics platform.
- **[Braintrust](braintrust.md)**: Enterprise AI evaluation platform and tracing suite.
- **[ClickHouse](clickhouse.md)**: Columnar analytical database powering Opik trace storage.
- **[FastMCP 3.1 Protocol](../automation_orchestration/mcp.md)**: Standardized protocol for agentic tool execution.

## Sources / references
- [Comet Opik Official Portal](https://www.comet.com/docs/opik/)
- [Comet Opik GitHub Repository](https://github.com/comet-ml/opik)
- [Open-Source LLM Observability Best Practices](https://www.comet.com/site/blog/)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
