# Sentry

## What it is
Sentry is an open-source error tracking and performance monitoring platform that helps developers see what matters and solve problems faster.

## What problem it solves
It provides real-time visibility into application errors and performance bottlenecks. It captures crashes, exceptions, and slow transactions, providing the context (stack traces, breadcrumbs, user data) needed to fix bugs quickly.

## Where it fits in the stack
**Category**: Tool / Process Understanding

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
- In almost any application where you want to know about errors before your users report them.
- When you need to trace performance issues across service boundaries.
- For monitoring LLM application failures and latency.

## When not to use it
- If you already have a comprehensive observability suite (like Datadog) that covers your error tracking needs.

## Licensing and cost
- **Open Source**: Yes (Self-hostable)
- **SaaS**: Yes (Freemium model)
- **Paid**: Tiered pricing based on event volume and features.

## Related tools / concepts
- [Datadog](datadog.md)
- [Langfuse](langfuse.md)
- [PostHog](posthog.md)

## Sources / References
- [Official Website](https://sentry.io/)
- [Sentry GitHub](https://github.com/getsentry/sentry)
- [OpenRouter Logging Docs](https://openrouter.ai/docs/activity/logging)

## Contribution Metadata
- Last reviewed: 2026-05-02
- Confidence: high
