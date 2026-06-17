# Sentry

## What it is
Sentry is an open-source error tracking and performance monitoring platform that helps developers see what matters and solve problems faster.

## What problem it solves
It provides real-time visibility into application errors and performance bottlenecks. It captures crashes, exceptions, and slow transactions, providing the context (stack traces, breadcrumbs, user data) needed to fix bugs quickly.

## Where it fits in the stack
**Category**: Process & Understanding / Error Tracking

## Typical use cases
- **Frontier Model Observability**: Monitoring reasoning traces and API errors for `claude-4-8-opus-20260528` and GPT-5.5 integrations.
- **AI-Powered Autofix**: Utilizing Sentry's native AI agents to automatically propose and apply code fixes for production exceptions.
- **Performance Profiling**: Identifying bottlenecks in RAG pipelines and tool-calling loops.
- **Crash Reporting**: Real-time error monitoring for multi-modal web and mobile applications.

## Strengths
- **Native AI Integration**: Features like "Autofix" use frontier models to explain errors and suggest fixes directly in PRs.
- **Deep SDK Ecosystem**: Industry-standard support for nearly every language and framework.
- **LLM-Specific Insights**: Capture prompt metadata and token usage alongside traditional error traces.
- **Actionable Context**: Provides rich breadcrumbs and stack traces to minimize "Time to Resolution."

## Limitations
- **Data Volume**: High-traffic agentic applications can quickly exhaust usage limits if sampling is not strictly configured.
- **Privacy Compliance**: Requires careful PII scrubbing when sending LLM prompts/responses to Sentry.
- **Complex Configuration**: Optimizing alerts to avoid "notification fatigue" in large-scale deployments.

## When to use it
- In any production-grade agentic system where catching exceptions in tool-use loops is critical.
- When you want to leverage AI agents to automate the debugging and bug-fixing lifecycle.

## When not to use it
- For local development where console logs and standard debuggers are sufficient.
- If you only need simple uptime monitoring without error tracking (use StatusCake or UptimeRobot).

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

### Python SDK
```python
import sentry_sdk

sentry_sdk.init(
    dsn="https://examplePublicKey@o0.ingest.sentry.io/0",
    traces_sample_rate=1.0,
)

# Capture a custom error message
sentry_sdk.capture_message("Custom application event recorded.")

# Divide by zero will be automatically captured
division_by_zero = 1 / 0
```

## Related tools / concepts
- [Datadog](datadog.md) — for full-stack observability and AI metrics
- [Langfuse](langfuse.md) — for dedicated LLM tracing and evaluation
- [PostHog](posthog.md) — for product analytics and session replay
- [OpenTelemetry Collector](opentelemetry-collector.md) — for vendor-agnostic telemetry ingestion
- [New Relic AI](new-relic-ai.md) — for APM with integrated AI assistance
- [AgentOps](agentops.md) — for specialized AI agent monitoring
- [Comet Opik](comet-opik.md) — for open-source LLM tracing and evaluation
- [WandB Weave](wandb-weave.md) — for lightweight LLM app building and tracing

## Sources / references
- [Official Website](https://sentry.io/)
- [Sentry Documentation](https://docs.sentry.io/)
- [Sentry AI Autofix](https://sentry.io/features/autofix/)
- [Sentry GitHub](https://github.com/getsentry/sentry)
- [OpenRouter Logging Docs](https://openrouter.ai/docs/activity/logging)

## Contribution Metadata
- Last reviewed: 2026-06-16
- Confidence: high
