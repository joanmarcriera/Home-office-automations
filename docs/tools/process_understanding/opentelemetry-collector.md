# OpenTelemetry Collector

## What it is
The OpenTelemetry (OTel) Collector is a high-performance, vendor-agnostic proxy designed to receive, process, and export telemetry data (traces, metrics, and logs). As of early January 2027, it serves as the universal standard for AI and agentic telemetry pipelines. It allows developers to unify metrics across traditional infrastructure layers and multi-agent workflows running on engines like **Claude 5.1**, **GPT-5.5**, **Llama 4**, and **Gemini 4.0 Pro**. It is open-source and highly self-hostable.

## What problem it solves
Managing telemetry in multi-agent environments often introduces high performance overheads, strict vendor lock-in, and compliance risks related to personally identifiable information (PII). The OTel Collector mitigates these concerns by providing:
- **Unified Ingestion**: A single OTLP gateway receiving telemetry signals from all microservices, eliminating the need to deploy distinct vendor-specific monitoring agents.
- **Client-Side Processing**: Real-time scrubbing of sensitive customer fields, prompt content, or API keys directly within the local network prior to routing.
- **Dynamic Routing**: A "receive once, distribute many" setup, sending trace metrics concurrently to cloud metrics providers, security databases, and local archives.
- **Sampling Governance**: Cost-defensive tail-based sampling configurations to drop redundant, successful runs and isolate only anomalous or slow multi-turn traces.
- **FastMCP 3.1 Session Instrumentation**: The ability to translate Model Context Protocol (FastMCP 3.1) connection patterns, tool invocations, and payload responses into standardized OTLP traces.

## Where it fits in the stack
The OpenTelemetry Collector sits in the **Observability Infrastructure** layer, acting as a telemetry router positioned securely between your production agent workflows (or proxies like [OpenRouter](../ai_knowledge/openrouter.md)) and target downstream monitoring platforms.

## Typical use cases
- **PII Scrubbing and Safety Guarding**: Processing incoming LLM logs to identify and redact passwords, credentials, and medical data before cloud storage.
- **System and Agentic Cross-Correlation**: Combining standard compute infrastructure telemetry (K3s CPU, memory use) with model-level latency indicators.
- **Model Cost and Tokens Aggregation**: Extracting raw token counts from model payload fields and outputting them as custom prometheus gauges.
- **Anomaly Selection (Tail Sampling)**: Dropping 95% of standard, cheap agent traces, while ensuring 100% of runs that throw exceptions or latency spikes >5000ms are preserved.

## Strengths
- **Ultimate Vendor Freedom**: Compatible with nearly every commercial and open-source observability engine on the market.
- **Architectural Extensibility**: Modular "Receivers, Processors, and Exporters" pipeline design allows developers to write custom processors in Go.
- **Incredible Efficiency**: Light memory and CPU footprint, capable of handling hundreds of thousands of events per second with sub-millisecond pipeline latency.
- **Semantic Conventions**: Standardized, industry-backed schemas for modeling traces and metric tags uniformly.

## Limitations
- **Substantial Operational Overhead**: Requires setup, management, horizontal scaling, and live-monitoring of the Collector cluster itself.
- **Complex YAML Configurations**: Fine-tuning batching, retry limits, and security layers can result in massive, hard-to-maintain YAML configurations.
- **Stateful Memory Overhead**: Stateful operations like tail-based sampling or metric accumulation require localized storage buffers, complicating container scheduling.

## When to use it
- When routing telemetry data to multiple target platforms (e.g., an enterprise cloud provider and a local database).
- When processing or sanitizing sensitive log text (like user input records) is required before leaving localized firewalls.
- When you are scaling production LLM workloads and need fine-grained control over telemetry collection budgets and trace sampling.
- When building robust multi-agent orchestration systems that demand vendor-agnostic standards.

## When not to use it
- For single-developer script prototypes where directly exporting to a single destination is easier to bootstrap.
- If your team has zero operational capacity or budget to set up and manage additional Docker or Kubernetes infrastructure.
- When utilizing a specialized platform whose distinct, closed-source agent features cannot be easily modeled via OpenTelemetry APIs.

## Getting started

### Basic Configuration (`config.yaml`)
Create an OTel Collector configuration file specifying standard OTLP ingestion, a processing batch queue, and local console and database exporters:

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: "0.0.0.0:4317"
      http:
        endpoint: "0.0.0.0:4318"

processors:
  batch:
    send_batch_size: 8192
    timeout: 1s
    send_batch_max_size: 10240
  memory_limiter:
    check_interval: 1s
    limit_percentage: 80
    spike_limit_percentage: 20

exporters:
  otlp/clickhouse:
    endpoint: "clickhouse-server:4317"
    tls:
      insecure: true
  logging:
    verbosity: detailed

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [logging, otlp/clickhouse]
    metrics:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [logging, otlp/clickhouse]
```

### Run via Docker
Launch the OpenTelemetry Collector container mapping the necessary gRPC and HTTP OTLP ports:

```bash
docker run -d \
    -p 4317:4317 \
    -p 4318:4318 \
    -v $(pwd)/config.yaml:/etc/otelcol/config.yaml \
    --name otel-collector \
    otel/opentelemetry-collector:0.118.0
```

## CLI examples

### Validate Configuration Syntax
Validate a local YAML configuration file using the built-in validator tool:

```bash
otelcol validate --config=config.yaml
```

### Starting the Collector Manually
Start the OTel collector agent with customized logging levels:

```bash
otelcol --config=config.yaml --log-level=info
```

### Querying Collector Performance Version
Query the installed runtime version specifications:

```bash
otelcol --version
```

## API examples

### Python Trace Ingestion with Pydantic v2 Payload Validation
Configure your multi-agentic application (e.g., a **Claude 5.1** task routing loop) to validate payload metadata using Pydantic v2 and ship performance traces to your local Collector instance:

```python
from pydantic import BaseModel, Field, ConfigDict
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

class AgentSpanMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model_name: str = Field(..., description="Target frontier model identifier")
    prompt_tokens: int = Field(..., ge=0, description="Token count in input prompt")
    completion_tokens: int = Field(..., ge=0, description="Token count in output completion")
    agent_id: str = Field(..., description="Unique agent identifier")

# Set up local Tracer provider
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Point exporter to local OTel Collector endpoint
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Validate metadata via Pydantic v2
metadata = AgentSpanMetadata(
    model_name="claude-5-1-sonnet",
    prompt_tokens=452,
    completion_tokens=128,
    agent_id="finance_routing_agent"
)

# Measure agent run latency and cost
with tracer.start_as_current_span("agent-task-routing-span") as span:
    span.set_attribute("llm.model", metadata.model_name)
    span.set_attribute("llm.prompt_tokens", metadata.prompt_tokens)
    span.set_attribute("llm.completion_tokens", metadata.completion_tokens)
    span.set_attribute("agent.id", metadata.agent_id)
    print("Executing core agentic task routing logic...")
```

### Node.js Custom Token Metrics Export (OTLP HTTP)
Log and increment custom metrics representing model token spend via OTLP over HTTP:

```javascript
const { MeterProvider } = require('@opentelemetry/sdk-metrics');
const { OTLPMetricExporter } = require('@opentelemetry/exporter-metrics-otlp-http');

const exporter = new OTLPMetricExporter({
  url: 'http://localhost:4318/v1/metrics',
});

const meterProvider = new MeterProvider();
const meter = meterProvider.getMeter('agentic-usage-metrics');

const tokenCounter = meter.createCounter('tokens_spent', {
  description: 'Tracks total prompt and completion token counts',
});

// Record token cost metrics for a GPT-5.5 call
tokenCounter.add(1024, { 'model.name': 'gpt-5.5-preview', 'agent.id': 'finance_routing_agent' });
```

## Related tools / concepts
- [Datadog](datadog.md) — Enterprise cloud tracing.
- [Sentry](sentry.md) — Exception tracking with native OTLP integration.
- [ClickHouse](clickhouse.md) — Relational columnar store for high-throughput traces.
- [Langfuse](langfuse.md) — Purpose-built open-source LLM tracing.
- [AgentOps](agentops.md) — High-level agent framework analysis.
- [Helicone](helicone.md) — LLM monitoring and request routing.
- [OpenRouter](../ai_knowledge/openrouter.md) — Broad-scale model routing and metric logs.
- [Grafana Cloud](grafana-cloud.md) — High-level telemetry dashboards.
- [PostHog](posthog.md) — In-app product analytics.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standardized agent tool-calling protocol.
- [Llama 4](../ai_knowledge/local_llms.md) — Monitored local execution runtime.

## Sources / references
- [OpenTelemetry Official Specification Portal](https://opentelemetry.io/)
- [OpenTelemetry Collector Repository on GitHub](https://github.com/open-telemetry/opentelemetry-collector)
- [W3C Trace Context Standard Spec](https://www.w3.org/TR/trace-context/)
- [OpenTelemetry semantic conventions for AI applications](https://opentelemetry.io/docs/specs/semconv/)

## Contribution Metadata
- Last reviewed: 2027-01-06
- Confidence: high
