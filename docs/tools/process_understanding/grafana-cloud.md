# Grafana Cloud

## What it is
Grafana Cloud is a fully managed observability platform that provides unified monitoring for metrics, logs, traces, and application performance. It includes hosted versions of Prometheus, Loki, Tempo, and Grafana.

## What problem it solves
It centralizes monitoring from disparate sources into a single dashboarding interface. For AI applications, it enables tracking of LLM latency, token usage, and error rates alongside traditional infrastructure metrics.

## Where it fits in the stack
**Infrastructure / Observability / Eval**.

## Typical use cases
- **Multi-source Dashboards**: Combining AWS CloudWatch, Prometheus, and LLM logs into one view.
- **Alerting**: Setting thresholds for AI response times or API error rates.
- **Log Aggregation**: Using Loki to search through distributed agent logs.

## Strengths
- **Open Standard Support**: Native support for Prometheus and OpenTelemetry.
- **Rich Visualization**: Industry-leading dashboarding capabilities.
- **Scalability**: Managed infrastructure handles high volumes of telemetry data.

## Limitations
- **Complexity**: Setting up advanced dashboards and alerts requires significant knowledge of PromQL or LogQL.
- **Data Silos**: Requires active effort to ensure all relevant data is being ingested.

## When to use it
- When you already use Grafana for infrastructure and want to add AI observability.
- When you need high-performance, long-term storage for logs and metrics.

## When not to use it
- For simple applications where basic logging is sufficient.

## Licensing and cost
- **Open Source**: The core components (Grafana, Loki, etc.) are open source (AGPLv3); the Cloud service is proprietary.
- **Cost**: Freemium (generous free tier, then usage-based).
- **Self-hostable**: Yes (via the LGTM stack).

## Related tools / concepts
- [Datadog](datadog.md)
- [New Relic AI](new-relic-ai.md)
- [OpenRouter (Log Streaming)](../ai_knowledge/openrouter.md)

## Sources / References
- [Official Website](https://grafana.com/products/cloud/)
- [Grafana Documentation](https://grafana.com/docs/)

## Contribution Metadata
- Last reviewed: 2026-05-06
- Confidence: high
