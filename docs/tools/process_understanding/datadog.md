# Datadog

## What it is
Datadog is an enterprise-grade observability and security platform that provides cloud-scale monitoring for applications, infrastructure, and logs. By late December 2026, it features dedicated **AI Agent Observability** modules designed to trace and monitor the reasoning and tool-calling behavior of autonomous agents. It integrates deeply with the **MCP 3.1** and **FastMCP 3.1** ecosystem to provide granular telemetry for agentic workflows.

## What problem it solves
It provides deep visibility into complex, distributed systems. It unifies metrics, traces, and logs in a single pane of glass, allowing teams to diagnose performance issues, monitor service health, and secure their cloud environments. Its AI-specific features solve the "black box" problem of agentic workflows by capturing full multi-step trace sessions, which is essential for debugging non-deterministic models like **Gemma 3**, **Claude 5.1**, **GPT-5.5**, or **Qwen 3.6**.

## Where it fits in the stack
**Process & Understanding / Observability**. It acts as the centralized telemetry hub for both infrastructure (servers, databases) and high-level AI services. It supports the **MCP 3.1 Task Protocol** for standardized automated benchmarking and execution monitoring.

## Typical use cases
- Monitoring cloud-native applications across AWS, Azure, and GCP.
- Centralized logging and analysis for distributed services.
- Real-time performance monitoring and alerting for autonomous agents.
- Observability for AI/LLM applications via OpenRouter or direct provider integrations.
- Monitoring automated benchmarking tasks using the MCP 3.1 Task Protocol.

## Strengths
- **Massive Integration Library**: Over 650+ integrations covering nearly every modern infrastructure component.
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

### Python (LLM Observability and Pydantic v2 Schema Validation)
This script defines a strict Pydantic v2 structure to format and pre-validate AI trace spans (complying with Datadog's late December 2026 LLMObs payload contract) before pushing telemetry to `ddtrace`.

```python
from typing import Dict, List, Literal, Optional
from pydantic import BaseModel, Field
from ddtrace import tracer
from ddtrace.llmobs import LLMObs

# 1. Define strict Datadog LLMObs schemas using Pydantic v2
class LLMModelParameters(BaseModel):
    temperature: float = Field(0.0, ge=0.0, le=2.0)
    max_tokens: int = Field(..., gt=0)
    top_p: Optional[float] = Field(None, ge=0.0, le=1.0)

class DatadogLLMSpan(BaseModel):
    span_id: str = Field(..., min_length=8)
    trace_id: str = Field(..., min_length=8)
    model_name: str = Field(..., min_length=1)
    provider_name: Literal["openai", "anthropic", "ollama", "custom"]
    input_text: str = Field(..., min_length=1)
    output_text: str = Field(..., min_length=1)
    token_metrics: Dict[str, int] = Field(
        ...,
        description="E.g., {'prompt_tokens': 120, 'completion_tokens': 350}"
    )
    model_params: LLMModelParameters
    mcp_tool_calls: List[str] = Field(default_factory=list)

# 2. Trace execution function utilizing verified payloads
def trace_validated_agent_span(span_data: DatadogLLMSpan):
    # Initialize LLM Observability
    LLMObs.enable()

    # Trace the execution utilizing Datadog's tracing library
    with tracer.trace("agent.task", resource="validated-llm-trace") as span:
        # Set standardized Datadog span tags
        span.set_tag("llm.model", span_data.model_name)
        span.set_tag("llm.provider", span_data.provider_name)
        span.set_tag("llm.prompt_tokens", span_data.token_metrics.get("prompt_tokens", 0))
        span.set_tag("llm.completion_tokens", span_data.token_metrics.get("completion_tokens", 0))
        span.set_tag("llm.trace_id", span_data.trace_id)

        # Track tool-calling telemetry under MCP 3.1
        if span_data.mcp_tool_calls:
            span.set_tag("llm.mcp_tools_used", ",".join(span_data.mcp_tool_calls))

        print(f"Datadog LLMObs Tracing enabled for span: {span_data.span_id}")

if __name__ == "__main__":
    try:
        # Create and validate the Datadog payload
        dd_payload = DatadogLLMSpan(
            span_id="span-998811",
            trace_id="trace-55442211",
            model_name="claude-5.1-sonnet",
            provider_name="anthropic",
            input_text="Research the latest FastMCP specifications.",
            output_text="FastMCP 3.1 includes high-performance transport protocols...",
            token_metrics={"prompt_tokens": 140, "completion_tokens": 280},
            model_params=LLMModelParameters(temperature=0.2, max_tokens=1024),
            mcp_tool_calls=["get_fastmcp_spec", "search_web"]
        )

        trace_validated_agent_span(dd_payload)
        print("Successfully validated and traced LLM span.")
    except Exception as e:
        print(f"Validation failed: {e}")
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
