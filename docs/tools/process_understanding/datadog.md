# Datadog

## What it is
Datadog is an enterprise-grade observability and security platform that provides cloud-scale monitoring for applications, infrastructure, and logs.

## What problem it solves
It provides deep visibility into complex, distributed systems. It unifies metrics, traces, and logs in a single pane of glass, allowing teams to diagnose performance issues, monitor service health, and secure their cloud environments.

## Where it fits in the stack
**Category**: Process & Understanding / Observability

## Typical use cases
- Monitoring cloud-native applications (AWS, Azure, GCP).
- Centralized logging and analysis for distributed services.
- Real-time performance monitoring and alerting.
- Observability for AI/LLM applications (e.g., via OpenRouter log streaming).

## Strengths
- Extremely broad set of integrations (600+).
- Powerful dashboarding and alerting capabilities.
- Highly scalable, designed for large-scale enterprise environments.
- Strong security and compliance features.

## Limitations
- Complexity: Can be overwhelming for small projects or individuals.
- Cost: Pricing can scale rapidly with volume (logs, custom metrics, etc.).
- Learning Curve: Requires significant configuration to get the most value.

## When to use it
- In enterprise environments where centralized observability across multiple clouds and hundreds of services is required.
- When you need to correlate metrics, traces, and logs to debug complex, intermittent issues.
- For monitoring AI/LLM applications at scale, especially when combined with existing infrastructure monitoring.

## When not to use it
- For very small personal projects or startups with extremely tight budgets (consider open-source alternatives like Prometheus/Grafana first).
- If your stack is very simple (e.g., a single monolithic app) and doesn't require the depth Datadog provides.

## Getting started

### Installation (Agent)
```bash
# Install the Datadog Agent (Ubuntu/Debian)
DD_AGENT_MAJOR_VERSION=7 DD_API_KEY=<YOUR_API_KEY> DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script.sh)"
```

### Configuration
Update `/etc/datadog-agent/datadog.yaml` with your API key and site, then restart the service:
```bash
sudo systemctl restart datadog-agent
```

## CLI examples

### Check Agent Status
```bash
datadog-agent status
```

### Verify Configuration
```bash
datadog-agent configcheck
```

### Send a Metric via DogStatsD
```bash
echo -n "custom.metric:1|c" | nc -w 1 -u localhost 8125
```

## API examples

### Python (StatsD)
```python
from datadog import initialize, statsd

options = {
    'statsd_host':'127.0.0.1',
    'statsd_port':8125
}

initialize(**options)

# Increment a counter with tags
statsd.increment('agent.run.count', tags=["env:prod", "version:1.0"])
```

## Related tools / concepts
- [Sentry](sentry.md)
- [Langfuse](langfuse.md)
- [PostHog](posthog.md)
- [OpenTelemetry Collector](opentelemetry-collector.md)
- [Grafana Cloud](grafana-cloud.md)
- [New Relic AI](new-relic-ai.md)
- [Prometheus](https://prometheus.io/)
- [ELK Stack (Elasticsearch, Logstash, Kibana)](https://www.elastic.co/elastic-stack)

## Sources / References
- [Official Website](https://www.datadoghq.com/)
- [Datadog Documentation](https://docs.datadoghq.com/)
- [OpenRouter Logging Docs](https://openrouter.ai/docs/activity/logging)

## Contribution Metadata
- Last reviewed: 2026-05-24
- Confidence: high
