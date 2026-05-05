# Sentry

## What it is
Sentry is an open-source error tracking and performance monitoring platform that helps developers see what matters and solve problems faster.

## What problem it solves
It provides real-time visibility into application errors and performance bottlenecks. It captures crashes, exceptions, and slow transactions, providing the context (stack traces, breadcrumbs, user data) needed to fix bugs quickly.

## Where it fits in the stack
**Category**: Process & Understanding / Error Tracking

## Typical use cases
- Real-time error monitoring for web and mobile applications.
- Performance profiling and transaction tracing.
- LLM observability and error tracking (e.g., via OpenRouter integration).

## Strengths
- Excellent developer experience with deep language and framework support.
- Open-source core with a strong community.
- Powerful error grouping and alerting.
- Provides actionable context for debugging.

## Limitations
- Can generate significant noise if not configured correctly (filtering errors).
- SaaS version has usage limits that can be reached quickly in high-traffic apps.

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
- [Datadog](datadog.md)
- [Langfuse](langfuse.md)
- [PostHog](posthog.md)
- [OpenTelemetry Collector](opentelemetry-collector.md)
- [New Relic AI](new-relic-ai.md)
- [AgentOps](agentops.md)

## Sources / References
- [Official Website](https://sentry.io/)
- [Sentry Documentation](https://docs.sentry.io/)
- [Sentry GitHub](https://github.com/getsentry/sentry)
- [OpenRouter Logging Docs](https://openrouter.ai/docs/activity/logging)

## Contribution Metadata
- Last reviewed: 2026-05-24
- Confidence: high
