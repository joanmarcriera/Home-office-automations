# Sentry

## What it is
Sentry is an open-source error tracking, performance profiling, and AI agent monitoring platform that helps software engineers detect, triage, and resolve production issues in real time. In early 2027, Sentry serves as an AI-native observability suite with deep integrations for frontier LLM reasoning loops, FastMCP 3.1 tool calls, and automated root-cause analysis.

## What problem it solves
It provides real-time visibility into application errors, unhandled exceptions, and latency bottlenecks. It captures crashes, stack traces, and session breadcrumbs across both traditional web/mobile runtimes and autonomous agentic loops. In multi-agent systems, Sentry specifically solves the challenge of non-deterministic failure modes by tracking tool timeouts, context overflow errors, and model reasoning exceptions.

## Where it fits in the stack
**Category**: Process & Understanding / Error Tracking. It acts as the "safety net" for the application layer, monitoring both traditional code execution and modern AI-agent reasoning loops across cloud and edge environments.

## Typical use cases
- **Frontier Model Observability**: Monitoring reasoning traces, tool execution failures, and API errors for Claude 5.1, GPT-5.5/5.6, Gemini 4.0 Pro/Ultra, DeepSeek-V4, and Gemma 3 integrations.
- **AI-Powered Autofix & Bug Resolution**: Utilizing Sentry's native AI Autofix agents to automatically generate and propose PR fixes for production exceptions via the **FastMCP 3.1 Protocol**.
- **Performance Profiling**: Identifying bottlenecks in RAG pipelines, vector search lookups, and high-frequency tool-calling loops.
- **Crash Reporting & Replay**: Real-time error monitoring with visual session replays for modern web and mobile applications.

## Strengths
- **Native AI Integration**: Sentry Autofix leverages frontier models to diagnose root causes and write pull requests with automated test coverage.
- **Deep SDK Ecosystem**: Industry-standard support for Python, TypeScript, Go, Rust, and specialized hooks for Vercel AI SDK and FastMCP 3.1 runtimes.
- **LLM-Specific Insights**: Capture prompt metadata, token usage, latency distribution, and model versioning alongside traditional stack traces.
- **Actionable Context**: Provides rich breadcrumbs, span attributes, and environment tags to minimize Time to Resolution (TTR).

## Limitations
- **Data Volume & Egress**: High-traffic agentic applications generating dense trace spans require strict sampling rules to avoid exceeding quota budgets.
- **Privacy Compliance & PII Scrubbing**: Requires careful client-side PII scrubbing when sending LLM prompts/responses to Sentry to maintain enterprise compliance.
- **Notification Noise**: High-velocity agentic retries can generate noisy alert channels without properly configured issue grouping rules.

## When to use it
- In any production-grade agentic system where catching exceptions in tool-use loops is critical.
- When you want to leverage autonomous agents to automate the debugging and bug-fixing lifecycle.
- When cross-stack observability (frontend, backend, and AI reasoning) is required in a single pane of glass.

## When not to use it
- For simple, local development where console logs and standard debuggers are sufficient.
- If you only need simple uptime ping checks without detailed error tracking or trace profiling.
- In highly air-gapped environments where outbound telemetry to a SaaS platform is prohibited and self-hosted Sentry infra cannot be maintained.

## Getting started

### Installation (Sentry CLI)
```bash
curl -sL https://sentry.io/get-cli/ | bash
```

### SDK Integration (Python)
```bash
pip install --upgrade sentry-sdk pydantic>=2.0.0
```

## CLI examples

### Login to Sentry
```bash
sentry-cli login
```

### Send a Test Event
```bash
sentry-cli send-event -m "Test message from CLI"
```

### Manage Releases
```bash
sentry-cli releases new -p <PROJECT_NAME> <VERSION_NUMBER>
```

## API examples

### Python SDK with AI Monitoring and Pydantic v2 Ingest Validation
In early 2027, observability platforms ingest telemetry structured by strict schemas. Below is an example of structured telemetry mapping to Sentry's API model using Pydantic v2.

```python
import sentry_sdk
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError

# Define Pydantic v2 models for custom telemetry payload validation
class AgentMetadata(BaseModel):
    model: str = Field(..., description="Frontier model name (e.g., claude-5.1-sonnet, gpt-5.5, deepseek-v4)")
    task_protocol: str = Field("fastmcp-3.1", description="Supported protocol version")
    step_count: int = Field(0, ge=0)

class TelemetryPayload(BaseModel):
    event_message: str = Field(..., min_length=5)
    severity: str = Field("error", description="Event severity level")
    agent_info: AgentMetadata = Field(..., description="Details of the executing agent")
    extra_tags: Optional[Dict[str, Any]] = None

# Initialize traditional Sentry SDK
sentry_sdk.init(
    dsn="https://examplePublicKey@o0.ingest.sentry.io/0",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0, # Enable profiling for RAG performance
)

def report_agent_event(payload_data: dict):
    try:
        # Validate payload using Pydantic v2 model_validate
        validated = TelemetryPayload.model_validate(payload_data)

        # Capture custom event with validated AI context
        with sentry_sdk.configure_scope() as scope:
            scope.set_tag("severity", validated.severity)
            scope.set_context("ai_agent", validated.agent_info.model_dump())
            if validated.extra_tags:
                for k, v in validated.extra_tags.items():
                    scope.set_extra(k, v)

            sentry_sdk.capture_message(validated.event_message)
        print(f"Sentry event captured and validated for: {validated.agent_info.model}")
    except ValidationError as e:
        print(f"Telemetry validation failed: {e.errors()}")

# Test sample structured ingestion
test_payload = {
    "event_message": "Agent tool-call timeout recorded in secondary RAG loop.",
    "severity": "warning",
    "agent_info": {
        "model": "deepseek-v4",
        "task_protocol": "fastmcp-3.1",
        "step_count": 4
    },
    "extra_tags": {
        "node_id": "homelab-node-01",
        "latency_ms": 12450
    }
}

report_agent_event(test_payload)
```

## Related tools / concepts
- [Datadog](datadog.md) — Full-stack observability and enterprise AI metrics.
- [Langfuse](langfuse.md) — Open-source LLM tracing and prompt evaluation.
- [PostHog](posthog.md) — Product analytics and user session replay.
- [OpenTelemetry Collector](opentelemetry-collector.md) — Vendor-agnostic telemetry collection.
- [Comet Opik](comet-opik.md) — Open-source LLM evaluation and trace logging.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Universal protocol for tool execution and agent monitoring (FastMCP 3.1).

## Sources / references
- [Official Website](https://sentry.io/)
- [Sentry Documentation](https://docs.sentry.io/)
- [Sentry AI Autofix Features](https://sentry.io/features/autofix/)
- [Sentry GitHub Repository](https://github.com/getsentry/sentry)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
