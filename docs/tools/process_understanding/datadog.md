# Datadog

## What it is
Datadog is an enterprise-grade observability, security, and performance analytics platform that delivers cloud-scale monitoring for applications, microservices, databases, and infrastructure. In 2027, Datadog features advanced **AI Agent Observability** and **LLM Observability** (LLMObs) suites specifically engineered to trace, monitor, and debug non-deterministic autonomous agents and reasoning loops powered by frontier models like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Gemma 4**, and **DeepSeek-V4**.

Datadog integrates deeply with the **MCP 3.1 / FastMCP 3.1** ecosystem, capturing multi-step tool calls, prompt tokens, completion latency, guardrail evaluations, and span-level trace replays across distributed agent workflows.

```mermaid
graph TD
    subgraph Agent Execution Runtime
        AgentApp[Agent Application / FastMCP Host]
        LLMProvider[Frontier Model APIs / Local vLLM]
        MCPTools[FastMCP 3.1 Tools & Resources]
    end

    subgraph Datadog Instrumentation
        DDTracer[dd-trace SDK / OpenTelemetry]
        DogStatsD[DogStatsD Daemon (UDP 8125)]
        LLMObsSDK[Datadog LLM Observability SDK]
    end

    subgraph Datadog Cloud Platform
        MetricsIngest[Metrics Pipeline]
        APMTraces[APM & Distributed Tracing]
        AgentExplorer[AI Agent Observability UI]
        LogsSecurity[Logs & Sensitive Data Scanner]
    end

    AgentApp -->|LLM Calls & Spans| LLMObsSDK
    AgentApp -->|System Traces| DDTracer
    AgentApp -->|Custom Metrics| DogStatsD

    LLMObsSDK -->|HTTPS / API| AgentExplorer
    DDTracer -->|HTTPS / OTLP| APMTraces
    DogStatsD -->|UDP| MetricsIngest

    LLMProvider -->|Token / Latency Metrics| LLMObsSDK
    MCPTools -->|Tool Span Metadata| DDTracer
```

## What problem it solves
As organizations transition from deterministic software architectures to agentic multi-model systems, traditional monitoring tools fail to explain why an autonomous agent made a specific decision or failed during a tool invocation. Datadog solves several critical operational problems:

1. **Agent Reasoning Black-Box Problem**: Standard APM traces show network HTTP calls but miss internal cognitive steps. Datadog LLMObs decomposes agent workflows into hierarchical trees of spans—identifying exact prompt inputs, tool call parameters, reasoning steps, and completion choices.
2. **Cost and Token Drift**: Multi-step agent loops can unexpectedly trigger recursive tool invocations, consuming millions of tokens. Datadog tracks token consumption (prompt vs completion), cost breakdown per model, and cached token ratios across environments in real time.
3. **Non-Deterministic Latency Diagnostics**: When an agent session stalls, Datadog isolates whether latency originated from model generation, slow FastMCP 3.1 tool execution, vector database retrieval, or network round-trips.
4. **Sensitive Data and Safety Guardrails**: Datadog Sensitive Data Scanner intercepts and redacts PII, credentials, or proprietary codebase snippets before trace payloads leave the local agent sandbox.

## Where it fits in the stack
**Category**: Process & Understanding / Enterprise AI Observability & Infrastructure Monitoring.

In the 2027 technology stack, Datadog operates as the primary telemetry control plane across all infrastructure layers—from underlying Kubernetes clusters and vector database nodes up to agent execution frameworks and FastMCP 3.1 tool invocation chains.

```
+-----------------------------------------------------------------------+
|                    Autonomous AI Agents & Workflows                   |
|                  (Claude 5.6, CrewAI, LangGraph, MCP 3.1)             |
+-----------------------------------------------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                   Datadog LLMObs & APM Tracer (dd-trace)              |
|  - Span Tree Decomposition (Agent -> Tool -> Model)                   |
|  - Token Cost & Cache Efficiency Tracking                             |
|  - Real-Time PII Redaction & Guardrail Auditing                       |
+-----------------------------------------------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                    Datadog Observability Cloud                         |
|   [LLM Explorer]   [APM Tracing]   [Metrics]   [Logs & Security]     |
+-----------------------------------------------------------------------+
```

## Typical use cases
- **Multi-Agent Session Replay**: Tracing complex multi-agent interactions (e.g. CrewAI or LangGraph crews) where an orchestrator agent delegates tasks to sub-agents and FastMCP tools, rendering the execution as a unified timeline.
- **MCP 3.1 Tool Invocation Monitoring**: Measuring latency, success/failure rates, and payload schema drift for FastMCP tool calls executed across external databases or APIs.
- **Production AI Cost Allocation**: Tagging agent traces with metadata (`env:production`, `team:analytics`, `customer_id:tenant-12`) to attribute token expenditures accurately across departments.
- **Infrastructure & GPU Node Monitoring**: Correlating high LLM latency spikes with physical Kubernetes node metrics, GPU memory utilization (NVIDIA H100/B200), and network bottlenecks.

## Strengths
- **Turnkey Enterprise AI Monitoring**: Out-of-the-box support for major LLM providers (Anthropic, OpenAI, Google Vertex, Bedrock) and orchestration frameworks with automatic span generation.
- **Unified Telemetry Dashboard**: Combines LLM reasoning traces, application logs, infrastructure metrics, and synthetic security checks in a single platform.
- **Scalability at Cloud Scale**: Capable of ingesting, indexing, and analyzing billions of telemetry events per day with configurable log retention and sampling strategies.
- **FastMCP 3.1 Standard Support**: Native parsing for Model Context Protocol spans, allowing detailed introspection into tool parameters and resource fetches.
- **Enterprise Governance & PII Masking**: Real-time pattern matching for credit card numbers, API keys, and sensitive personally identifiable information prior to cloud ingestion.

## Limitations
- **Subscription and Telemetry Costs**: Ingesting high volumes of detailed LLM spans, raw prompt logs, and custom metrics can significantly increase monthly Datadog bills if sampling filters are not configured properly.
- **Steep Initial Configuration Curve**: Setting up custom dashboards, alert thresholds, and span-level tag mappings across enterprise microservices requires dedicated platform engineering effort.
- **Proprietary SaaS Vendor Locking**: Unlike open-source telemetry tools (such as OpenTelemetry Collector or Grafana), Datadog relies on proprietary SaaS storage and query engines.

## When to use it
- When managing mission-critical enterprise applications where agent reliability, performance, and security compliance are mandatory.
- When you need a single observability dashboard that connects hardware metrics (GPUs, servers) directly to high-level AI prompt responses.
- When running large-scale multi-tenant AI systems that require strict cost attribution and data privacy masking.

## When not to use it
- For early-stage open-source projects or small personal prototypes with limited budgets (consider self-hosted [Langfuse](../process_understanding/langfuse.md) or Grafana).
- If your environment requires 100% air-gapped on-premise observability storage without any outbound SaaS network egress.

## Getting started

### Installation (Datadog Agent & Python SDKs)

#### 1. Datadog Infrastructure Agent Setup
Install the host agent on Linux / Ubuntu nodes:

```bash
# Install the Datadog Agent (v7+) with APM and DogStatsD enabled
DD_AGENT_MAJOR_VERSION=7 \
DD_API_KEY="YOUR_DATADOG_API_KEY" \
DD_SITE="datadoghq.com" \
bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
```

#### 2. Install Python Instrumentation Libraries
Install `ddtrace` alongside required dependencies:

```bash
pip install ddtrace datadog pydantic fastmcp
```

#### 3. Environment Variable Configuration
Configure tracing and LLMObs options in your environment or systemd unit:

```bash
export DD_ENV="production"
export DD_SERVICE="agentic-workflow-engine"
export DD_VERSION="3.2.1"
export DD_LLMOBS_ENABLED="1"
export DD_LLMOBS_AGENTLESS_ENABLED="0" # Route through local dd-agent
export DD_LLMOBS_SITE="datadoghq.com"
```

## CLI examples

### 1. Agent Status & Telemetry Diagnostics
Verify that the local Datadog daemon is active and accepting APM spans and DogStatsD metrics:

```bash
# Check agent status and running checks
datadog-agent status

# Verify APM tracer receiver status
datadog-agent status | grep -A 10 "APM Agent"
```

### 2. Manual DogStatsD Metric Emission
Test custom metric ingestion directly from the terminal via UDP port 8125:

```bash
# Emit a counter metric for an agent tool invocation
echo -n "mcp.tool.execution:1|c|#env:prod,tool:sql_query,status:success" | nc -w 1 -u localhost 8125

# Emit a histogram metric for LLM execution latency (e.g. 1420ms)
echo -n "llm.latency_ms:1420|h|#model:claude-5-6-sonnet,mcp_version:3.1" | nc -w 1 -u localhost 8125
```

### 3. Trace Sampling and Log Stream Testing
Trigger a synthetic trace run using `ddtrace-run`:

```bash
ddtrace-run python3 -c "
import time
from ddtrace import tracer

with tracer.trace('agent.task.execution', service='test-service') as span:
    span.set_tag('agent.id', 'agent-9021')
    time.sleep(0.1)
print('Synthetic trace submitted successfully.')
"
```

## API examples

### Python FastMCP 3.1 Server Instrumented with Datadog LLMObs
This example demonstrates a FastMCP 3.1 server where tool calls and LLM generation steps are instrumented with Datadog LLM Observability spans and custom metrics.

```python
import os
import time
from fastmcp import FastMCP
from ddtrace.llmobs import LLMObs
from ddtrace import tracer
from datadog import initialize, statsd
from pydantic import BaseModel, Field

# Initialize Datadog StatsD client
initialize(statsd_host="127.0.0.1", statsd_port=8125)

# Enable Datadog LLM Observability
LLMObs.enable(
    service="fastmcp-observability-server",
    env="production",
    ml_app="agentic-research-pipeline"
)

mcp = FastMCP("Datadog Instrumented FastMCP Server")

class VectorSearchRequest(BaseModel):
    query: str = Field(..., min_length=3, description="Search query string")
    top_k: int = Field(default=5, ge=1, le=20)

@mcp.tool()
async def execute_vector_retrieval(params: VectorSearchRequest) -> dict:
    """Executes a semantic vector search and logs performance telemetry to Datadog."""
    start_time = time.time()

    # Start a Datadog LLMObs tool span
    with LLMObs.tool(name="vector_search", ml_app="agentic-research-pipeline") as span:
        LLMObs.annotate(
            span=span,
            parameters={"query": params.query, "top_k": params.top_k},
            tags={"mcp.protocol": "3.1", "db.type": "qdrant"}
        )

        # Simulated database latency
        time.sleep(0.045)

        results = [
            {"id": "doc-101", "score": 0.92, "text": "FastMCP 3.1 supports multiplexed tool calls."},
            {"id": "doc-102", "score": 0.88, "text": "Datadog captures span trees for autonomous agents."}
        ]

        # Record output metadata
        LLMObs.annotate(span=span, output_data={"results_count": len(results)})

        duration_ms = (time.time() - start_time) * 1000
        statsd.histogram("mcp.tool.latency_ms", duration_ms, tags=["tool:vector_search", "env:prod"])
        statsd.increment("mcp.tool.invocations", tags=["tool:vector_search", "status:success"])

        return {"results": results, "latency_ms": duration_ms}

if __name__ == "__main__":
    mcp.run(transport="sse", port=8000)
```

### Production Pydantic v2 Telemetry Schema Validation for Datadog LLMObs
This production script validates Datadog LLM Observability trace payloads, token usage breakdown, and FastMCP 3.1 metadata prior to forwarding metrics to the Datadog API.

```python
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict

class SpanKind(str, Enum):
    LLM = "llm"
    AGENT = "agent"
    TOOL = "tool"
    WORKFLOW = "workflow"

class ModelProvider(str, Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GOOGLE = "google"
    LOCAL_VLLM = "local_vllm"

class TokenUsage(BaseModel):
    prompt_tokens: int = Field(..., ge=0)
    completion_tokens: int = Field(..., ge=0)
    total_tokens: int = Field(..., ge=0)
    cached_tokens: Optional[int] = Field(default=0, ge=0)

    @field_validator("total_tokens")
    @classmethod
    def validate_total(cls, v: int, info) -> int:
        p = info.data.get("prompt_tokens", 0)
        c = info.data.get("completion_tokens", 0)
        if v != (p + c):
            return p + c
        return v

class DatadogLLMTracePayload(BaseModel):
    model_config = ConfigDict(extra="ignore")

    trace_id: str = Field(..., pattern=r"^[0-9a-fA-F]{16,32}$")
    span_id: str = Field(..., pattern=r"^[0-9a-fA-F]{16,32}$")
    parent_span_id: Optional[str] = Field(default=None, pattern=r"^[0-9a-fA-F]{16,32}$")
    span_kind: SpanKind = Field(default=SpanKind.LLM)
    provider: ModelProvider = Field(default=ModelProvider.ANTHROPIC)
    model_name: str = Field(..., min_length=2)
    latency_ms: float = Field(..., ge=0.0)
    tokens: TokenUsage
    mcp_protocol_version: str = Field(default="3.1")
    tags: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("tags")
    @classmethod
    def ensure_environment_tag(cls, tags: List[str]) -> List[str]:
        if not any(t.startswith("env:") for t in tags):
            tags.append("env:production")
        return tags

# Example Usage & Verification
if __name__ == "__main__":
    raw_telemetry = {
        "trace_id": "a1b2c3d4e5f678901234567890abcdef",
        "span_id": "f0e9d8c7b6a54321",
        "span_kind": "agent",
        "provider": "anthropic",
        "model_name": "claude-5-6-sonnet",
        "latency_ms": 1280.4,
        "tokens": {
            "prompt_tokens": 1450,
            "completion_tokens": 320,
            "total_tokens": 1770,
            "cached_tokens": 800
        },
        "mcp_protocol_version": "3.1",
        "tags": ["service:agent-core", "team:ai-ops"]
    }

    trace = DatadogLLMTracePayload.model_validate(raw_telemetry)
    print(f"Validated Datadog Trace: {trace.trace_id} (Span: {trace.span_id})")
    print(f"Model: {trace.model_name} | Total Tokens: {trace.tokens.total_tokens}")
    print(f"JSON Payload:\n{trace.model_dump_json(indent=2)}")
```

## Related tools / concepts
- [Sentry](sentry.md) — Application error and crash reporting platform.
- [Langfuse](langfuse.md) — Open-source LLM engineering and observability platform.
- [PostHog](posthog.md) — Product analytics and LLM session tracking.
- [OpenTelemetry Collector](opentelemetry-collector.md) — Vendor-neutral telemetry ingestion collector.
- [Grafana Cloud](grafana-cloud.md) — Open observability and visualization suite.
- [New Relic AI](new-relic-ai.md) — Enterprise APM and AI performance monitoring.
- [AgentOps](agentops.md) — Specialized AI agent session monitoring.
- [Logfire](logfire.md) — Pythonic observability platform powered by Pydantic.
- [LangSmith](../benchmarking/langsmith.md) — Debugging and evaluation platform for LLM applications.
- [MCP 3.1](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Standardized Model Context Protocol telemetry specification.

## Sources / references
- [Datadog Official Website](https://www.datadoghq.com/)
- [Datadog AI Agent Observability Documentation](https://docs.datadoghq.com/ai_integrations/)
- [Datadog LLM Observability API Reference](https://docs.datadoghq.com/api/latest/llm-observability/)
- [Datadog Python Tracer (`ddtrace`) Repository](https://github.com/DataDog/dd-trace-py)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
