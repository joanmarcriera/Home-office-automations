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

## When to use it
- In any production application (web, mobile, server) to catch and resolve crashes before users report them.
- When you need deep context (stack traces, environment variables) to debug issues in remote environments.

## When not to use it
- For local development where console logs and standard debuggers are sufficient.
- If you only need simple uptime monitoring without error tracking (use StatusCake or UptimeRobot).

## Getting started

### Installation
You can install the Sentry CLI for administrative tasks or use the language-specific SDKs for application monitoring.

```bash
# Install Sentry CLI
curl -sL https://sentry.io/get-cli/ | bash

# Install Python SDK
pip install --upgrade sentry-sdk
```

### Hello-world example
Initialize Sentry in a Python script to verify error capturing:

```python
import sentry_sdk

# Initialize with your DSN
sentry_sdk.init(dsn="https://your-dsn@sentry.io/project-id")

# This will be captured and sent to Sentry
sentry_sdk.capture_message("Hello Sentry!")
```

## CLI examples

### Authentication
Authenticate the CLI with your Sentry account:
```bash
sentry-cli login
```

### Send a manual event
Send a test message directly from the terminal to verify your DSN:
```bash
export SENTRY_DSN="https://your-dsn@sentry.io/project-id"
sentry-cli send-event -m "Test message from CLI"
```

### Proactive Release Management
Create a new release and notify Sentry of a deployment:
```bash
sentry-cli releases new -p my-project v1.0.0
sentry-cli releases set-commits --auto v1.0.0
sentry-cli releases finalize v1.0.0
```

## API examples

### AI Monitoring (June 2026)
Sentry provides specialized tracking for AI agents and LLM calls.

```python
import sentry_sdk
from sentry_sdk.ai.monitoring import track_llm_call

sentry_sdk.init(dsn="SENTRY_DSN", traces_sample_rate=1.0)

@track_llm_call(provider="openai", model="gpt-4o")
def get_completion(prompt):
    # Your LLM logic here
    return "Response"
```

### Manual Exception Capturing
Explicitly capture exceptions in try-except blocks for better context.

```python
import sentry_sdk

try:
    complex_operation()
except Exception as e:
    sentry_sdk.set_tag("operation_type", "data_sync")
    sentry_sdk.capture_exception(e)
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
