# Sentry

## What it is
Sentry is an open-source error tracking and performance monitoring platform that helps developers see what matters and solve problems faster. As of late October / November 2026, it has evolved into an AI-native observability suite, offering deep integration with frontier models and autonomous agent workflows.

## What problem it solves
It provides real-time visibility into application errors and performance bottlenecks. It captures crashes, exceptions, and slow transactions, providing the context (stack traces, breadcrumbs, user data) needed to fix bugs quickly. In agentic systems, it specifically addresses the "black box" nature of LLM reasoning by capturing tool-call failures and trace telemetry.

## Where it fits in the stack
**Category**: Process & Understanding / Error Tracking. It acts as the "safety net" for the application layer, monitoring both traditional code execution and modern AI-agent reasoning loops.

## Typical use cases
- **Frontier Model Observability**: Monitoring reasoning traces and API errors for Claude 5.1, GPT-5.5, Gemini 4.0, Llama 4, Gemma 3, and Qwen 3.6 integrations.
- **AI-Powered Autofix**: Utilizing Sentry's native AI agents to automatically propose and apply code fixes for production exceptions via the **MCP 3.1 Task Protocol**.
- **Performance Profiling**: Identifying bottlenecks in RAG pipelines and high-frequency tool-calling loops.
- **Crash Reporting**: Real-time error monitoring for multi-modal web and mobile applications with integrated session replay.

## Strengths
- **Native AI Integration**: Features like "Autofix" use frontier models to explain errors and suggest fixes directly in PRs with high accuracy.
- **Deep SDK Ecosystem**: Industry-standard support for nearly every language and framework, including specialized hooks for AI SDKs.
- **LLM-Specific Insights**: Capture prompt metadata, token usage, and model versioning alongside traditional error traces.
- **Actionable Context**: Provides rich breadcrumbs and stack traces to minimize "Time to Resolution" (TTR) in autonomous systems.

## Limitations
- **Data Volume**: High-traffic agentic applications can quickly exhaust usage limits if sampling is not strictly configured.
- **Privacy Compliance**: Requires careful PII scrubbing when sending LLM prompts/responses to Sentry to remain compliant with global regulations.
- **Complexity**: Optimizing alerts to avoid "notification fatigue" in large-scale deployments requires significant initial tuning.

## When to use it
- In any production-grade agentic system where catching exceptions in tool-use loops is critical.
- When you want to leverage autonomous agents to automate the debugging and bug-fixing lifecycle.
- When cross-stack observability (frontend, backend, and AI reasoning) is required in a single pane of glass.

## When not to use it
- For simple, local development where console logs and standard debuggers are sufficient.
- If you only need simple uptime monitoring without detailed error tracking (consider StatusCake).
- In highly air-gapped environments where outbound telemetry to a SaaS platform is prohibited.

## Getting started

### Installation (Sentry CLI)
```bash
curl -sL https://sentry.io/get-cli/ | bash
```

### SDK Integration (Python)
```bash
pip install --upgrade sentry-sdk
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
In late October / November 2026, observability platforms ingest telemetry structured by strict schemas. Below is an example of structured telemetry mapping to Sentry's API model using Pydantic v2.

```python
import sentry_sdk
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

# Define Pydantic v2 models for custom telemetry payload validation
class AgentMetadata(BaseModel):
    model: str = Field(..., description="Frontier model name (e.g., claude-5.1-sonnet)")
    task_protocol: str = Field("mcp-3.1", description="Supported protocol version")
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

# Test sample structured ingestion
test_payload = {
    "event_message": "Agent tool-call timeout recorded in secondary RAG loop.",
    "severity": "warning",
    "agent_info": {
        "model": "qwen-3.6-72b",
        "task_protocol": "mcp-3.1",
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
- [Datadog](datadog.md) — for full-stack observability and AI metrics.
- [Langfuse](langfuse.md) — for dedicated LLM tracing and evaluation.
- [PostHog](posthog.md) — for product analytics and session replay.
- [OpenTelemetry Collector](opentelemetry-collector.md) — for vendor-agnostic telemetry ingestion.
- [New Relic AI](new-relic-ai.md) — for APM with integrated AI assistance.
- [AgentOps](agentops.md) — for specialized AI agent monitoring.
- [Comet Opik](comet-opik.md) — for open-source LLM tracing and evaluation.
- [WandB Weave](wandb-weave.md) — for lightweight LLM app building and tracing.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — the standard for connecting agents to tools and monitoring.

## Sources / references
- [Official Website](https://sentry.io/)
- [Sentry Documentation](https://docs.sentry.io/)
- [Sentry AI Autofix](https://sentry.io/features/autofix/)
- [Sentry GitHub](https://github.com/getsentry/sentry)
- [Observability in the Age of Agents (late October 2026)](https://sentry.engineering/blog/observability-agents-late-october-2026)

## Contribution Metadata
- Last reviewed: 2026-11-05
- Confidence: high
