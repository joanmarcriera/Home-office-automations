# Datadog

## What it is
Datadog is an enterprise-grade observability and security platform that provides cloud-scale monitoring for applications, infrastructure, and logs. As of 2026, it features dedicated **AI Agent Observability** modules designed to trace and monitor the reasoning and tool-calling behavior of autonomous agents.

## What problem it solves
It provides deep visibility into complex, distributed systems. It unifies metrics, traces, and logs in a single pane of glass, allowing teams to diagnose performance issues, monitor service health, and secure their cloud environments. Its AI-specific features solve the "black box" problem of agentic workflows by capturing full multi-step trace sessions.

## Where it fits in the stack
**Process & Understanding / Observability**. It acts as the centralized telemetry hub for both infrastructure (servers, databases) and high-level AI services.

## Typical use cases
- Monitoring cloud-native applications across AWS, Azure, and GCP.
- Centralized logging and analysis for distributed services.
- Real-time performance monitoring and alerting for autonomous agents.
- Observability for AI/LLM applications via OpenRouter or direct provider integrations.

## Strengths
- **Massive Integration Library**: Over 600+ integrations covering nearly every modern infrastructure component.
- **Enterprise-Grade AI Monitoring**: Provides span-based trace replay for non-deterministic LLM failures.
- **Scalability**: Designed to handle trillions of data points per day across global clusters.
- **Strong Security & Compliance**: Features like sensitive data masking for logs and real-time threat detection.

## Limitations
- **Complexity**: The sheer breadth of features can be overwhelming for small projects or individuals.
- **Cost**: Pricing scales rapidly with data volume (logs, custom metrics, and AI spans can become expensive).
- **Learning Curve**: Requires significant initial configuration and "tuning" to eliminate alert noise.

## When to use it
- In enterprise environments requiring centralized observability across multiple clouds and hundreds of services.
- When you need to correlate infrastructure metrics with high-level AI agent reasoning traces.
- For monitoring production-grade AI applications where accountability and deterministic replay are required.

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

### Python (LLM Observability)
Tracing an agentic tool call using the Datadog `ddtrace` library.

```python
from ddtrace import tracer
from ddtrace.llmobs import LLMObs

# Initialize LLM Observability
LLMObs.enable()

with tracer.trace("agent.task", resource="research-summary") as span:
    # Logic for your AI agent task
    span.set_tag("model", "gpt-5.5")
    span.set_tag("tokens", 1050)
    print("Agent task complete.")
```

## Related tools / concepts
- [Sentry](sentry.md)
- [Langfuse](langfuse.md)
- [PostHog](posthog.md)
- [OpenTelemetry Collector](opentelemetry-collector.md)
- [Grafana Cloud](grafana-cloud.md)
- [New Relic AI](new-relic-ai.md)
- [AgentOps](agentops.md)
- [LangSmith](../benchmarking/langsmith.md)
- [OpenRouter](../ai_knowledge/openrouter.md)

## Sources / References
- [Datadog Official Website](https://www.datadoghq.com/)
- [Datadog AI Agent Observability](https://www.datadoghq.com/products/ai/agent-observability/)
- [Datadog API Reference: LLM Observability](https://docs.datadoghq.com/api/latest/llm-observability/)

## Contribution Metadata
- Last reviewed: 2026-06-16
- Confidence: high
