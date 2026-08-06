# Datadog

## What it is
Datadog is an enterprise-grade observability and security platform that provides cloud-scale monitoring for applications, infrastructure, and logs. By late November / December 2026, it features dedicated **AI Agent Observability** modules designed to trace and monitor the reasoning and tool-calling behavior of autonomous agents. It integrates deeply with the **MCP 3.1 / FastMCP 3.1** ecosystem to provide granular telemetry for agentic workflows.

## What problem it solves
It provides deep visibility into complex, distributed systems. It unifies metrics, traces, and logs in a single pane of glass, allowing teams to diagnose performance issues, monitor service health, and secure their cloud environments. Its AI-specific features solve the "black box" problem of agentic workflows by capturing full multi-step trace sessions, which is essential for debugging non-deterministic models like **Gemma 3**, **GPT-5.5**, or **Claude 5.1**.

## Where it fits in the stack
**Process & Understanding / Observability**. It acts as the centralized telemetry hub for both infrastructure (servers, databases) and high-level AI services. It supports the **MCP 3.1 Task Protocol** for standardized automated benchmarking and execution monitoring.

## Typical use cases
- Monitoring cloud-native applications across AWS, Azure, and GCP.
- Centralized logging and analysis for distributed services.
- Real-time performance monitoring and alerting for autonomous agents.
- Observability for AI/LLM applications via OpenRouter or direct provider integrations.
- Monitoring automated benchmarking tasks using the MCP 3.1 Task Protocol.

## Strengths
- **Massive Integration Library**: Over 600+ integrations covering nearly every modern infrastructure component.
- **Enterprise-Grade AI Monitoring**: Provides span-based trace replay for non-deterministic LLM failures.
- **Scalability**: Designed to handle trillions of data points per day across global clusters.
- **Strong Security & Compliance**: Features like sensitive data masking for logs and real-time threat detection.
- **Task Protocol Integration**: Native support for MCP 3.1 standardized tasks.

## Limitations
- **Complexity**: The sheer breadth of features can be overwhelming for small projects or individuals.
- **Cost**: Pricing scales rapidly with data volume (logs, custom metrics, and AI spans can become expensive).
- **Learning Curve**: Requires significant initial configuration and "tuning" to eliminate alert noise.

## When to use it
- In enterprise environments requiring centralized observability across multiple clouds and hundreds of services.
- When you need to correlate infrastructure metrics with high-level AI agent reasoning traces.
- For monitoring production-grade AI applications where accountability and deterministic replay are required.
- When running large-scale automated evaluations that require structured monitoring via MCP 3.1.

## When not to use it
- For very small personal projects or early-stage startups on a tight budget (consider [Langfuse](../process_understanding/langfuse.md) or self-hosted Grafana instead).
- If your stack is extremely simple (e.g., a single monolithic app) and doesn't require distributed tracing or log correlation.

## Getting started

### Installation (Agent)
The Datadog Agent is the primary way to collect telemetry.

```bash
# Install the Datadog Agent (Ubuntu/Debian)
DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=<YOUR_API_KEY> DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
```

### AI Observability Setup
Enable the `llm-obs` integration in your agent configuration or via the Datadog UI to begin capturing LLM spans.

## CLI examples

### Check Agent Status
Verify the local agent is running and communicating with Datadog.

```bash
datadog-agent status
```

### Send a Metric via DogStatsD
Manually test metric ingestion from the command line.

```bash
echo -n "agent.heartbeat:1|c|#env:prod,version:1.2" | nc -w 1 -u localhost 8125
```

## API examples

### Python (StatsD for Metrics)
Incrementing a counter with custom tags for infrastructure monitoring.

```python
from datadog import initialize, statsd

options = {
    'statsd_host':'127.0.0.1',
    'statsd_port':8125
}

initialize(**options)

# Increment a counter with tags
statsd.increment('agent.run.count', tags=["env:prod", "version:2.1"])
```

### Python: LLM Span and Metadata Validation with Strict Pydantic v2
This production script validates Datadog LLM Observability spans, token usage metrics, and MCP v3.1 context payloads prior to log-forwarding or trace-injection.

```python
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, field_validator

# 1. Define strict Pydantic v2 models for Datadog LLMObs schemas
class LLMTraceSpan(BaseModel):
    span_id: str = Field(..., pattern=r"^[0-9a-fA-F]{16,32}$")
    trace_id: str = Field(..., pattern=r"^[0-9a-fA-F]{16,32}$")
    span_kind: str = Field("llm", pattern=r"^(llm|agent|tool|workflow)$")
    model_name: str = Field(..., description="Frontier model used (e.g., gemma-3-27b, claude-5.1-sonnet)")
    prompt_tokens: int = Field(..., ge=0)
    completion_tokens: int = Field(..., ge=0)
    latency_ms: float = Field(..., ge=0.0)
    mcp_protocol: str = Field("3.1", pattern=r"^3\.[0-1]$")
    tags: List[str] = Field(default_factory=list)

    @field_validator("tags")
    @classmethod
    def ensure_environment_tag(cls, tags: List[str]) -> List[str]:
        # Validate that tags contain environment specification
        if not any(tag.startswith("env:") for tag in tags):
            tags.append("env:development")
        return tags

# 2. Trace handling simulation
def validate_datadog_span(raw_span_data: dict) -> Optional[LLMTraceSpan]:
    try:
        validated_span = LLMTraceSpan.model_validate(raw_span_data)
        return validated_span
    except Exception as e:
        print(f"Datadog Span validation failed: {e}")
        return None

if __name__ == "__main__":
    sample_raw_span = {
        "span_id": "a1b2c3d4e5f67890",
        "trace_id": "f0e9d8c7b6a54321",
        "span_kind": "agent",
        "model_name": "claude-5.1-sonnet",
        "prompt_tokens": 1250,
        "completion_tokens": 420,
        "latency_ms": 1420.5,
        "mcp_protocol": "3.1",
        "tags": ["version:3.21", "env:production"]
    }

    span = validate_datadog_span(sample_raw_span)
    if span:
        print(f"Datadog span {span.span_id} validated successfully.")
        print(f"Validated Model: {span.model_name} (Tokens: {span.prompt_tokens + span.completion_tokens})")
        print(f"Assigned Tags: {span.tags}")
```

## Related tools / concepts
- [Sentry](sentry.md)
- [Langfuse](langfuse.md)
- [PostHog](posthog.md)
- [OpenTelemetry Collector](opentelemetry-collector.md)
- [Grafana Cloud](grafana-cloud.md)
- [New Relic AI](new-relic-ai.md)
- [AgentOps](agentops.md)
- [Logfire](logfire.md)
- [LangSmith](../benchmarking/langsmith.md)
- [OpenRouter](../ai_knowledge/openrouter.md)
- [Gemma 3](../ai_knowledge/local_llms.md)
- [MCP 3.1](../../knowledge_base/patterns/tool-calling-and-mcp.md)

## Sources / References
- [Datadog Official Website](https://www.datadoghq.com/)
- [Datadog AI Agent Observability](https://www.datadoghq.com/products/ai/agent-observability/)
- [Datadog API Reference: LLM Observability](https://docs.datadoghq.com/api/latest/llm-observability/)

## Contribution Metadata
- Last reviewed: 2026-12-06
- Confidence: high
