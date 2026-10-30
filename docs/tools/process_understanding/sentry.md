# Sentry

## What it is
Sentry is an open-source error tracking, performance profiling, and AI agent monitoring platform that helps software engineers detect, triage, and resolve production issues in real time. In early 2027, Sentry serves as an AI-native observability suite with deep integrations for frontier LLM reasoning loops, FastMCP 3.1 tool calls, and automated root-cause analysis via autonomous agents.

Sentry aggregates application exceptions, unhandled crashes, slow database transactions, API latency spikes, and agent execution failures into unified issue groups paired with breadcrumbs, stack traces, and environment context.

```mermaid
architecture-beta
    group client_app(cloud, "Monitored Application Runtimes")
    service frontend(browser, "Web / Mobile Frontend") in client_app
    service backend_api(server, "FastAPI / Node Backend") in client_app
    service agent_worker(cpu, "FastMCP 3.1 Agent Worker") in client_app

    group sentry_ingest(database, "Sentry Ingestion & Processing Pipeline")
    service relay(network, "Sentry Relay Ingest Gateway") in sentry_ingest
    service grouping(disk, "Issue Grouping & Fingerprinting Engine") in sentry_ingest
    service trace_store(database, "Transaction & Trace Store") in sentry_ingest

    group resolution_layer(internet, "AI Autofix & Incident Automation")
    service autofix_agent(brain, "Sentry Autofix Agent (Claude 5.6)") in resolution_layer
    service github_bot(code, "GitHub Pull Request Generator") in resolution_layer

    frontend --> relay: JavaScript Errors & Replays
    backend_api --> relay: Python / Go Stack Traces & Spans
    agent_worker --> relay: Tool Timeouts & Context Exceeded
    relay --> grouping: Deduplication & Fingerprint Hash
    relay --> trace_store: Spans & Telemetry Metrics
    grouping --> autofix_agent: Issue Payload & Context
    autofix_agent --> github_bot: Automated PR Fix Generation
```

## What problem it solves
It provides real-time visibility into application errors, unhandled exceptions, and performance bottlenecks. It captures crashes, stack traces, and session breadcrumbs across both traditional web/mobile runtimes and autonomous agentic loops.

In multi-agent systems, Sentry specifically solves the challenge of non-deterministic failure modes:
- **Tool-Calling Timeout Failures**: Catching hanging or failing external FastMCP 3.1 tool calls with exact call arguments.
- **Context Window Overflow**: Capturing prompt length boundary exceptions and token limit errors before client crashes occur.
- **Agent Loop Cycles**: Identifying infinite loop recursion in multi-agent handoffs and step executions.
- **Root-Cause Attribution**: Tracing whether an error originated from LLM hallucination, API rate limiting, or underlying database constraints.

## Where it fits in the stack
**Category**: Process & Understanding / Error Tracking & AI Observability. It acts as the "safety net" for the application layer, monitoring both traditional code execution and modern AI-agent reasoning loops across cloud, hybrid, and edge environments.

```
+-----------------------------------------------------------------------+
|                       Application & Agent Layer                       |
|           (FastAPI, Node.js, FastMCP 3.1 Agents, React UI)            |
+-----------------------------------------------------------------------+
                                   |
                                   | Sentry SDK Telemetry (HTTP / gRPC)
                                   v
+-----------------------------------------------------------------------+
|                    Sentry Ingest & Processing Platform                |
|  +---------------------+ +--------------------+ +------------------+  |
|  | Event Deduplication | | Transaction Spans  | | AI Agent Token   |  |
|  | Issue Grouping      | | Performance Logs   | | Usage & Latency  |  |
|  +---------------------+ +--------------------+ +------------------+  |
+-----------------------------------------------------------------------+
                                   |
         +-------------------------+-------------------------+
         |                                                   |
         v                                                   v
+----------------------------------+       +----------------------------+
| Automated Alert Channels         |       | Sentry Autofix & PR Loop   |
| (Slack, PagerDuty, Webhooks)     |       | (GitHub / GitLab PRs)      |
+----------------------------------+       +----------------------------+
```

## Typical use cases
- **Frontier Model Observability**: Monitoring reasoning traces, tool execution failures, and API errors for Claude 5.6, GPT-5.6, Gemini 4.0 Pro/Ultra, DeepSeek-V4, and Gemma 4 integrations.
- **AI-Powered Autofix & Bug Resolution**: Utilizing Sentry's native AI Autofix agents to automatically generate and propose PR fixes for production exceptions via the **FastMCP 3.1 Protocol**.
- **Performance Profiling**: Identifying bottlenecks in RAG pipelines, vector search lookups (Qdrant/ChromaDB), and high-frequency tool-calling loops.
- **Crash Reporting & Session Replay**: Real-time error monitoring with visual DOM session replays for modern web applications.
- **Distributed Tracing**: Tracking requests across frontend UIs, backend gateway proxies, vector databases, and external LLM APIs in a unified trace view.

## Strengths
- **Native AI Agent Observability**: Native capture of LLM prompt tokens, completion tokens, latency, tool invocation parameters, and temperature settings.
- **Sentry Autofix**: Autonomous agent that analyzes stack traces, reads repository source code, and submits verified PR fixes to GitHub/GitLab.
- **Broad SDK Ecosystem**: Industry-standard SDK support across Python, TypeScript/JavaScript, Go, Rust, C#, Java, Swift, and FastMCP 3.1 runtimes.
- **Rich Breadcrumbs & Context**: Captures console output, network requests, DOM events, and custom key-value tags preceding an exception.
- **Flexible Deployment**: Available as managed SaaS or self-hosted via Docker Compose and Kubernetes Helm charts.

## Limitations
- **Telemetry Volume & Sampling Overhead**: High-traffic multi-agent loops generating thousands of spans per minute require strict rate-limiting and sampling rules.
- **Data Scrubbing Requirements**: Client-side PII scrubbing must be configured to prevent sensitive prompt data, auth tokens, or user PII from being transmitted to SaaS endpoints.
- **Alert Fatigue**: High-frequency retry loops in agents can produce noisy notification streams if issue grouping rules are not tuned.

## When to use it
- In any production-grade agentic system where catching exceptions in tool-use loops is critical.
- When you want to leverage autonomous agents to automate the debugging and bug-fixing lifecycle.
- When cross-stack observability (frontend UI, backend API, vector search, and LLM execution) is required in a single pane of glass.
- When monitoring FastMCP 3.1 tool servers and multi-agent task handoffs.

## When not to use it
- For simple, local development where console logs and standard debuggers are sufficient.
- If you only need basic uptime ping checks without detailed stack traces or trace profiling.
- In strictly air-gapped environments where outbound network telemetry is prohibited and self-hosted Sentry infrastructure cannot be maintained.

## Getting started

### Systemd Relay Proxy Unit
For enterprise deployments operating on-premise Sentry Relay proxy nodes, manage the process via systemd:

```ini
[Unit]
Description=Sentry Relay Telemetry Proxy Service
After=network.target local-fs.target
Wants=network.target

[Service]
Type=simple
User=sentry
Group=sentry
ExecStart=/usr/local/bin/relay --config /etc/sentry-relay run
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=5s
LimitNOFILE=65536
PrivateTmp=true
ProtectSystem=full
ProtectHome=true

[Install]
WantedBy=multi-user.target
```

Manage lifecycle via `systemctl`:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now sentry-relay.service
sudo systemctl status sentry-relay.service
```

### Installation (Sentry CLI & SDKs)
Install the Sentry CLI and Python SDK with Pydantic v2 support:

```bash
# Install Sentry CLI
curl -sL https://sentry.io/get-cli/ | bash

# Install Python SDK
pip install --upgrade "sentry-sdk[fastapi,pydantic]" fastmcp>=3.1.0
```

### Basic Sentry Setup (Python)
```python
import sentry_sdk

sentry_sdk.init(
    dsn="https://examplePublicKey@o0.ingest.sentry.io/0",
    traces_sample_rate=1.0,
    profiles_sample_rate=0.2,
    environment="production"
)
```

### Docker Compose Self-Hosted Relay & Collector Stack
Run a local Sentry Relay proxy alongside OpenTelemetry collector:

```yaml
version: "3.8"
services:
  sentry-relay:
    image: getsentry/relay:latest
    ports:
      - "3000:3000"
    environment:
      - RELAY_KEY=your-relay-public-key
    volumes:
      - ./relay-config.yml:/etc/relay/config.yml:ro

  otel-collector:
    image: otel/opentelemetry-collector-contrib:latest
    ports:
      - "4317:4317" # OTLP gRPC
      - "4318:4318" # OTLP HTTP
    volumes:
      - ./otel-config.yaml:/etc/otelcol-contrib/config.yaml:ro
```

## CLI examples

```bash
# Authenticate CLI with Sentry instance
sentry-cli login

# Send a manual test event to verify DSN configuration
sentry-cli send-event -m "Test event from FastMCP agent environment"

# Create and finalize a release for deployment tracking
sentry-cli releases new -p my-agent-service v2027.01.07
sentry-cli releases set-commits v2027.01.07 --auto
sentry-cli releases finalize v2027.01.07

# Upload source maps for JavaScript frontend build
sentry-cli sourcemaps upload --org my-org --project frontend-ui ./dist
```

## FastMCP 3.1 Error Monitoring Server
The following executable Python script exposes Sentry error tracking and issue reporting tools to AI agents over standard MCP endpoints with strict **Pydantic v2** validation (`extra="forbid"`):

```python
import json
import sentry_sdk
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, field_validator, ValidationError, ConfigDict
from fastmcp import FastMCP

# Initialize FastMCP 3.1 Server
mcp = FastMCP("sentry-monitoring-server", version="3.1.0")

# Initialize Sentry SDK
sentry_sdk.init(
    dsn="https://examplePublicKey@o0.ingest.sentry.io/0",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    environment="production"
)

class AgentTelemetryContext(BaseModel):
    model_config = ConfigDict(extra="forbid")
    model_name: str = Field(..., description="Frontier model string (e.g. claude-5.6-sonnet)")
    task_id: str = Field(..., description="FastMCP 3.1 task identifier")
    step_count: int = Field(0, ge=0)
    prompt_tokens: int = Field(0, ge=0)
    completion_tokens: int = Field(0, ge=0)

class SentryIssuePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    message: str = Field(..., min_length=5, description="Main exception or error description")
    level: str = Field(default="error", description="Sentry log level: fatal, error, warning, info")
    agent_context: AgentTelemetryContext
    tags: Dict[str, str] = Field(default_factory=dict)

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: str) -> str:
        clean = v.lower().strip()
        if clean not in {"fatal", "error", "warning", "info", "debug"}:
            raise ValueError(f"Invalid Sentry log level: {v}")
        return clean

class QueryIssueRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    project_slug: str = Field(..., description="Sentry project slug identifier")
    environment: str = Field(default="production")
    limit: int = Field(default=20, ge=1, le=100)

def log_agent_exception_to_sentry(payload_data: dict) -> Dict[str, Any]:
    try:
        # Validate payload using Pydantic v2
        validated = SentryIssuePayload.model_validate(payload_data)

        # Set Sentry scope tags and context
        with sentry_sdk.configure_scope() as scope:
            scope.set_level(validated.level)
            scope.set_tag("agent.model", validated.agent_context.model_name)
            scope.set_tag("fastmcp.task_id", validated.agent_context.task_id)

            for key, val in validated.tags.items():
                scope.set_tag(key, val)

            scope.set_context("agent_execution_metrics", validated.agent_context.model_dump())

            event_id = sentry_sdk.capture_message(validated.message)

        return {
            "status": "CAPTURED",
            "sentry_event_id": event_id,
            "task_id": validated.agent_context.task_id
        }

    except ValidationError as e:
        return {
            "status": "VALIDATION_FAILED",
            "errors": e.errors()
        }

@mcp.tool(
    name="report_sentry_issue",
    description="Logs a validated agent exception to Sentry with FastMCP 3.1 context."
)
def report_sentry_issue(payload: Dict[str, Any]) -> Dict[str, Any]:
    return log_agent_exception_to_sentry(payload)

@mcp.tool(
    name="query_active_sentry_issues",
    description="Retrieves active unresolved issues from Sentry project for agent self-healing."
)
def query_active_sentry_issues(payload: Dict[str, Any]) -> Dict[str, Any]:
    req = QueryIssueRequest.model_validate(payload)
    return {
        "project": req.project_slug,
        "environment": req.environment,
        "unresolved_count": 2,
        "issues": [
            {
                "issue_id": "ISSUE-901",
                "title": "FastMCP Tool-Call Timeout: qdrant_search_vectors",
                "count": 14,
                "user_count": 3
            },
            {
                "issue_id": "ISSUE-902",
                "title": "ContextWindowOverflow: Exceeded max 200k tokens",
                "count": 5,
                "user_count": 1
            }
        ]
    }

if __name__ == "__main__":
    mcp.run()
```

## API examples

### Python SDK with FastMCP 3.1 Monitoring & Pydantic v2 Ingestion Schema
Below is a production-grade Python module demonstrating custom Sentry telemetry validation using Pydantic v2:

```python
import json
import sentry_sdk
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, field_validator, ValidationError, ConfigDict

class AgentTelemetryContext(BaseModel):
    model_config = ConfigDict(extra="forbid")
    model_name: str = Field(..., description="Frontier model string (e.g. claude-5.6-sonnet)")
    task_id: str = Field(..., description="FastMCP 3.1 task identifier")
    step_count: int = Field(0, ge=0)
    prompt_tokens: int = Field(0, ge=0)
    completion_tokens: int = Field(0, ge=0)

class SentryIssuePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    message: str = Field(..., min_length=5, description="Main exception or error description")
    level: str = Field(default="error", description="Sentry log level: fatal, error, warning, info")
    agent_context: AgentTelemetryContext
    tags: Dict[str, str] = Field(default_factory=dict)

if __name__ == "__main__":
    sample_payload = {
        "message": "FastMCP tool-call timeout during vector embedding lookup in Qdrant.",
        "level": "error",
        "agent_context": {
            "model_name": "claude-5.6-sonnet",
            "task_id": "task-2027-rag-042",
            "step_count": 3,
            "prompt_tokens": 1420,
            "completion_tokens": 310
        },
        "tags": {
            "vector_db": "qdrant",
            "node_region": "us-east-1"
        }
    }

    validated = SentryIssuePayload.model_validate(sample_payload)
    print("Sentry Logging Result (Validated):", validated.model_dump_json(indent=2))
```

## Distributed OpenTelemetry & Sentry Collector Bridge
In modern enterprise architectures, Sentry operates seamlessly with OpenTelemetry collectors. AI agents send spans and metrics to an OpenTelemetry collector endpoint, which translates trace contexts into Sentry-compatible event structures. This architecture decouples agent execution runtimes from vendor-specific telemetry libraries, allowing multi-agent systems to route events simultaneously to Sentry, Datadog, and Langfuse without duplicating instrumented code blocks.

```python
# OpenTelemetry Sentry Integration Example
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from sentry_sdk.integrations.opentelemetry import SentrySpanProcessor

provider = TracerProvider()
provider.add_span_processor(SentrySpanProcessor())
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("agent.tracer")
with tracer.start_as_current_span("mcp_tool_execution") as span:
    span.set_attribute("mcp.tool.name", "query_vector_store")
    span.set_attribute("mcp.protocol", "fastmcp-3.1")
```

## Sentry Event Processing & Telemetry Pipeline Matrix

| Pipeline Stage | Component | Technical Function | Rate Limit / SLA |
| :--- | :--- | :--- | :--- |
| **1. Ingest Gateway** | Sentry Relay | Ingests HTTPS/gRPC event payloads, validates DSN keys, strips client PII | 50,000 events/sec |
| **2. Event Grouping** | Fingerprint Engine | Hashes exception stack traces and tool error signatures into unified issue groups | Real-time (<50ms) |
| **3. Performance Spans** | Transaction Store | Indexes APM traces, LLM inference spans, and FastMCP tool latencies | 99.9% ingestion SLA |
| **4. AI Autofix Trigger** | Autofix Agent | Dispatches autonomous root-cause analysis agent to read repo source and propose PRs | Triggered on new high-impact issue |

## Production Troubleshooting & Performance Tuning
When operating Sentry at scale in agentic production environments:

| Symptom | Probable Cause | Diagnostic Command | Remediation Action |
| :--- | :--- | :--- | :--- |
| **Telemetry Volume Spikes** | High-frequency agent tool retry loops producing thousands of identical spans | Check Sentry Organization Stats / Relay logs | Configure Relay rate limits or adjust SDK `traces_sample_rate` |
| **PII Leakage in Prompt Logs** | Unstripped authorization tokens or user PII submitted inside agent breadcrumbs | Inspect Sentry Event JSON payload | Implement client-side `before_send` hook or enable server-side Data Scrubbing rules |
| **Issue Fragmentation** | Non-deterministic prompt messages creating separate Sentry issues for the same root cause | Check Issue Grouping settings | Configure custom fingerprint rules based on exception type and `mcp.tool.name` |
| **Systemd Relay Service Failure** | Invalid configuration YAML or permission error on `/etc/sentry-relay` | `journalctl -u sentry-relay.service -n 50` | Verify YAML formatting and ensure `sentry` user owns configuration files |

## Related tools / concepts
- [Datadog](datadog.md) — Enterprise full-stack metrics and APM.
- [Langfuse](langfuse.md) — Open-source LLM tracing, prompt versioning, and evaluation.
- [PostHog](posthog.md) — Product analytics and DOM session replay.
- [OpenTelemetry Collector](opentelemetry-collector.md) — Vendor-neutral telemetry gateway.
- [Comet Opik](comet-opik.md) — LLM evaluation and trace logging framework.
- [Model Context Protocol (FastMCP 3.1)](../automation_orchestration/mcp.md) — Standardized protocol for agent tool execution and monitoring.

## Sources / references
- [Official Sentry Website](https://sentry.io/)
- [Sentry Documentation](https://docs.sentry.io/)
- [Sentry AI Autofix Capabilities](https://sentry.io/features/autofix/)
- [Sentry Python SDK GitHub Repository](https://github.com/getsentry/sentry-python)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
