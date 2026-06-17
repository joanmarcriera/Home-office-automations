# Sentry

## What it is
Sentry is an open-source error tracking and performance monitoring platform that provides real-time visibility into application health. In the June 2026 ecosystem, it has evolved into a central observability hub for both traditional software and agentic AI workflows, offering deep insights into crashes, exceptions, and slow transactions across the stack.

## What problem it solves
It solves the "observability gap" in complex distributed systems and AI agent swarms. By capturing stack traces, breadcrumbs, and environment data, Sentry enables developers and agents to diagnose bugs quickly. Its **AI-Powered Autofix** (integrated with GPT-5.5 and Claude 4.8 Opus) now suggests and can automatically apply code fixes for captured exceptions in CI/CD pipelines.

## Where it fits in the stack
**Category**: Process & Understanding / Observability & Error Tracking. It serves as the primary "feedback loop" for both human developers and autonomous coding agents like [Claude Code](../development_ops/claude-code.md).

## Typical use cases
- **AI Agent Monitoring**: Tracking tool-use failures and reasoning traces in [agentic workflows](../../knowledge_base/patterns/agentic-workflows.md).
- **Frontend/Mobile Error Tracking**: Capturing client-side crashes in React, Vue, and Flutter apps.
- **Backend Performance Profiling**: Identifying slow database queries or API calls using distributed tracing.
- **Autonomous Bug Resolution**: Using Sentry's Autofix to resolve minor production regressions without human intervention.

## Strengths
- **Native AI Integration**: First-class support for monitoring LLM costs, latency, and token usage via the Sentry AI SDK.
- **Deep Context**: Provides high-fidelity breadcrumbs leading up to an error, including user actions and log statements.
- **Extensive Ecosystem**: Over 100+ platform integrations, including native [OpenRouter integration](../providers/openrouter.md).
- **Self-Hostable**: Maintains a robust open-source core for privacy-conscious homelab deployments.

## Limitations
- **Volume Management**: Can become noisy and expensive if filtering and sampling are not correctly configured.
- **Learning Curve**: Advanced features like Metric Alerts and Custom Discover Queries require significant configuration.

## When to use it
- In any production-grade application where uptime and error resolution speed are critical.
- When deploying [autonomous agents](../agents/README.md) that require a structured feedback mechanism for self-correction.

## When not to use it
- For very small, static projects where simple console logging is sufficient.
- If you only require basic uptime monitoring (use [Uptime Kuma](../../services/uptime-kuma.md) or StatusCake).

## Getting started

### Installation (Sentry CLI)
```bash
curl -sL https://sentry.io/get-cli/ | bash
```

### SDK Integration (Python with AI Support)
```bash
pip install --upgrade sentry-sdk[ai]
```

## CLI examples

### Login and Project Setup
```bash
sentry-cli login
sentry-cli projects list
```

### Send a Test Event for Agent Verification
```bash
sentry-cli send-event -m "Agentic reasoning loop timeout" --level error
```

### Propose Autofix for a Specific Issue
```bash
# Triggers Sentry's Autofix flow for issue ID 12345
sentry-cli issues autofix 12345 --model gpt-5.5-pro
```

## API examples

### Python SDK for AI Agents
Initialize Sentry with AI monitoring enabled to track Claude 4.8 Opus performance.

```python
import sentry_sdk
from sentry_sdk.integrations.ai import AiIntegration

sentry_sdk.init(
    dsn="https://examplePublicKey@o0.ingest.sentry.io/0",
    integrations=[AiIntegration()],
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

# Capture a custom error during tool-use
with sentry_sdk.configure_scope() as scope:
    scope.set_tag("agent_model", "claude-4-8-opus-20260528")
    sentry_sdk.capture_message("Tool execution failed: Access Denied")
```

## Related tools / concepts
- [Datadog](datadog.md) — Comprehensive enterprise observability.
- [Langfuse](langfuse.md) — Specialized LLM application tracing.
- [PostHog](posthog.md) — Product analytics and session replay.
- [OpenTelemetry Collector](opentelemetry-collector.md) — Vendor-neutral telemetry.
- [New Relic AI](new-relic-ai.md) — AI-native performance management.
- [AgentOps](agentops.md) — Observability for agentic swarms.
- [Logfire](logfire.md) — Pydantic-native logging and observability.
- [Claude Code](../development_ops/claude-code.md) — AI agent that integrates with Sentry logs.
- [Uptime Kuma](../../services/uptime-kuma.md) — Simple self-hosted uptime monitoring.

## Sources / references
- [Official Website](https://sentry.io/)
- [Sentry AI Monitoring Docs](https://docs.sentry.io/product/ai-monitoring/)
- [Sentry GitHub](https://github.com/getsentry/sentry)
- [OpenRouter Logging Docs](https://openrouter.ai/docs/activity/logging)
- [Autofix Release Blog](https://sentry.io/answers/ai-powered-autofix/)

## Contribution Metadata
- Last reviewed: 2026-06-17
- Confidence: high
