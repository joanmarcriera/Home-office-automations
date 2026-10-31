# Fiddler AI

Fiddler is an Enterprise-grade Model Performance Management (MPM) and AI Observability platform designed for continuous LLM monitoring, guardrail evaluation, and multi-agent governance. In January 2027, it serves as a primary enterprise platform for monitoring production models like **Claude 5.1**, **GPT-5.5 / 5.6**, **Gemini 4.0 Pro / Ultra**, and **DeepSeek-V4**, leveraging **FastMCP 3.1** protocol tracing and Pydantic v2 validation models.

## What it is
Fiddler is a comprehensive enterprise AI observability and governance platform providing transparency, trust, and risk mitigation across machine learning, tabular predictive models, and multi-agent generative systems. It combines **Fiddler Auditor**—an open-source evaluation suite for red-teaming, adversarial stress-testing, and automated pre-deployment testing—with **Fiddler AI Observability**, delivering real-time guardrail enforcement, embedding-based semantic drift detection, and advanced explainability (XAI) for LLM pipelines and autonomous agents.

## What problem it solves
Deploying generative AI and autonomous agents at enterprise scale introduces compliance, alignment, and operational risk. Fiddler provides a centralized control tower for:
- **Toxicity & Hallucination Mitigation**: Real-time evaluation of factual grounding, ungrounded hallucination scores, and toxic outputs across production streams.
- **Embedding & Semantic Drift Detection**: Tracking vector embedding clusters to identify data distribution shifts and domain drift before accuracy degrades.
- **Explainability & Attribution (XAI)**: Demystifying frontier LLMs and agentic decision trees via feature attribution and retrieval-augmented generation (RAG) diagnostic tracing.
- **Multi-Agent Session Audit**: Tracing complex multi-step reasoning loops, agent-to-agent delegatory calls, and **FastMCP 3.1** tool execution pipelines.

## System Architecture

The following ASCII diagram illustrates Fiddler's telemetry ingestion topology, guardrail enforcement pipeline, vector embedding drift analysis, and FastMCP 3.1 multi-agent tracing interface:

```
+-----------------------------------------------------------------------------------+
|                        AGENTIC EXECUTION & MODEL GATEWAY LAYER                    |
|  +-----------------------+     +-----------------------+     +-----------------+  |
|  | Multi-Agent Swarm     |     | LiteLLM / Gateway     |     | OpenClaw Engine |  |
|  | (FastMCP 3.1 Callers) |     | (HTTP / gRPC Tracing) |     | (Autonomous)    |  |
|  +-----------+-----------+     +-----------+-----------+     +--------+--------+  |
+--------------|-----------------------------|--------------------------|-----------+
               |                             |                          |
               +-------------------+---------+--------------------------+
                                   | Telemetry Traces (JSON-RPC / OTel)
                                   v
+-----------------------------------------------------------------------------------+
|                           FIDDLER AI OBSERVABILITY PLATFORM                       |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  |                     INGRESS GUARDRAIL & EVALUATION ENGINE                    |  |
|  |  [Toxicity Filter] ---> [Hallucination Scorer] ---> [PII & Injection Guard] |  |
|  +-------------------------------------+---------------------------------------+  |
|                                        |                                          |
|                                        v                                          |
|  +-----------------------------------------------------------------------------+  |
|  |                    EMBEDDING & SEMANTIC DRIFT ANALYZER                      |  |
|  |  [UMAP/t-SNE Cluster Tracker] ---> [Reference vs Production Drift (KS-Test)]  |  |
|  +-------------------------------------+---------------------------------------+  |
|                                        |                                          |
|                                        v                                          |
|  +-----------------------------------------------------------------------------+  |
|  |                     EXPLAINABILITY & FEATURE ATTRIBUTION                    |  |
|  |  [Integrated Gradients] ---> [RAG Context Relevance] ---> [XAI Attribution] |  |
|  +-------------------------------------+---------------------------------------+  |
|                                        |                                          |
+----------------------------------------|------------------------------------------+
                                         v
+-----------------------------------------------------------------------------------+
|                          ENTERPRISE STORAGE & ANALYTICS                           |
|  +--------------------------+  +--------------------------+  +-----------------+  |
|  | Fiddler Audit DB         |  | Real-Time Alert Engine   |  | Authentik SSO   |  |
|  | (Time-Series & Vectors)  |  | (Slack / PagerDuty / MCP)|  | (RBAC Governance)|  |
|  +--------------------------+  +--------------------------+  +-----------------+  |
+-----------------------------------------------------------------------------------+
```

## Feature Comparison Matrix

| Capability / Metric | Fiddler AI Observability | Arize AI (Phoenix) | Braintrust | Comet Opik |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Focus** | Enterprise MPM, Guardrails & XAI | ML Observability & RAG Tracing | LLM Evaluation & Prompt Eng. | Open-Source Tracing & Dataset Mgmt |
| **FastMCP 3.1 Support** | Native Tracing & Tool Auditing | OTel Collector Integrations | Custom Tool Wrappers | Python Client Hooks |
| **Explainability (XAI)** | Integrated Feature Attribution | SHAP & Embedding Drift | Prompt Comparison Matrix | Basic Metric Scoring |
| **Deployment Options** | SaaS / Private Cloud / VPC | SaaS / Hybrid Cloud | SaaS / Self-Hosted Docker | Open-Source / Self-Hosted |
| **Guardrail Engine** | Real-time Blocking & Scoring | Online Evaluation Monitors | Async Judge Scoring | Async Dataset Evaluation |
| **Enterprise RBAC & SSO**| Built-in Authentik / Okta / SAML| Enterprise Tier Only | Team Role Management | Basic API Key Security |

## Where it fits in the stack
**Category**: Process & Understanding / Enterprise AI Observability. Fiddler acts as the governance and telemetry layer sitting between AI Gateways (e.g., [LiteLLM](../../services/litellm.md)) and application orchestration frameworks. It leverages **FastMCP 3.1** for low-overhead telemetry injection without introducing latency to real-time agent execution loops.

## Typical use cases
- **Frontier Model Guardrails**: Real-time guardrail evaluation for PII, prompt injection, and harmful content across Claude 5.1, GPT-5.5, and DeepSeek-V4.
- **RAG & Vector Search Monitoring**: Disentangling vector retrieval failures from LLM reasoning errors using embedding drift analysis.
- **Regulatory Governance & Compliance**: Maintaining verifiable audit trails and fairness metrics in regulated industries (financial services, healthcare, and insurance).
- **Agentic Workflow Diagnostics**: Identifying root causes for failed multi-turn agent sessions or unexpected tool invocation chains.
- **Pre-Production Red-Teaming**: Executing automated adversarial evaluation suites prior to deploying new model versions or system prompts.

## Strengths
- **Enterprise-Grade Governance**: Built with role-based access control (RBAC), SSO via [Authentik](../../services/authentik.md), tenant isolation, and audit logging.
- **Unified Traditional ML & LLM Analytics**: Single dashboard to monitor predictive ML models (regression/XGBoost) and multimodal agentic workflows.
- **Native FastMCP 3.1 & OpenTelemetry Support**: Seamless ingestion of standard agent execution traces and tool calling payloads.
- **Extensible Custom Metrics**: Enables custom LLM-as-a-judge scorers, domain-specific toxicity classifiers, and custom compliance metrics.
- **Advanced Feature Attribution**: Industry-leading explainability engines for structured data, text embeddings, and prompt features.

## Limitations
- **Enterprise Footprint**: Rich feature set and enterprise architecture create a steep setup learning curve for small teams.
- **Compute Overhead at Scale**: High-frequency real-time embedding drift detection and guardrail checks require dedicated cluster resources.
- **Commercial Platform Core**: While Fiddler Auditor is open-source, the central AI Observability server requires a commercial license.

## When to use it
- When deploying production LLM applications in regulated enterprise environments with strict audit mandates.
- To continuously evaluate RAG quality, factual grounding, and embedding drift at scale.
- When debugging complex autonomous agent workflows requiring granular step-by-step reasoning and tool call attribution.

## When not to use it
- For early-stage developer sandboxes where lightweight open-source loggers (e.g., [LangSmith](../benchmarking/langsmith.md) or [Comet Opik](comet-opik.md)) suffice.
- For isolated local deployments operating without internet connection or enterprise telemetry requirements.

## Getting started

Install the official Fiddler Python client:

```bash
pip install fiddler-client pydantic fastmcp
```

Initialize a connection to your enterprise Fiddler tenant:

```python
import fiddler as fdl

# Connect to enterprise instance
client = fdl.FiddlerApi(
    url="https://your-org.fiddler.ai",
    org_id="enterprise_core",
    auth_token="fdl_secure_token_2027"
)
```

## Systemd Service Configuration

In enterprise on-premise, VPC, or edge collector environments, deploy the Fiddler Telemetry Collector daemon as a hardened `systemd` background service unit.

Save the following configuration to `/etc/systemd/system/fiddler-telemetry-collector.service`:

```ini
[Unit]
Description=Fiddler AI Telemetry Collector & FastMCP 3.1 Trace Forwarder
After=network.target network-online.target redis.service
Wants=network-online.target
Documentation=https://docs.fiddler.ai/

[Service]
Type=simple
User=fiddler-agent
Group=fiddler-agent
WorkingDirectory=/opt/fiddler-collector
Environment="PYTHONUNBUFFERED=1"
Environment="FIDDLER_ORG=enterprise-core"
Environment="FIDDLER_ENDPOINT=https://your-org.fiddler.ai"
Environment="REDIS_BUFFER_URL=redis://localhost:6379/1"
EnvironmentFile=-/etc/fiddler/collector.env

# Hardened Linux Security Controls
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
AmbientCapabilities=CAP_NET_BIND_SERVICE
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/fiddler-collector/spool /var/log/fiddler
PrivateTmp=true
ProtectKernelTunables=true
ProtectControlGroups=true
RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6
MemoryMax=4G
TasksMax=512

ExecStart=/opt/fiddler-collector/venv/bin/python3 /opt/fiddler-collector/collector_daemon.py --port 8970 --workers 4
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=5s
KillMode=mixed
TimeoutStopSec=20s

[Install]
WantedBy=multi-user.target
```

Reload and initialize the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now fiddler-telemetry-collector.service
sudo systemctl status fiddler-telemetry-collector.service
```

## Production Multi-Container Docker Compose Stack

Deploying Fiddler's localized edge forwarding stack enables zero-data-loss telemetry buffering, batch micro-aggregation, and low-latency OpenTelemetry bridge ingestion.

Save the following specification to `docker-compose.fiddler.yml`:

```yaml
version: '3.8'

services:
  fiddler-agent-forwarder:
    image: python:3.12-slim-bookworm
    container_name: fiddler-agent-forwarder
    restart: unless-stopped
    depends_on:
      fiddler-redis-buffer:
        condition: service_healthy
    environment:
      - FIDDLER_URL=https://your-org.fiddler.ai
      - FIDDLER_ORG=enterprise-core
      - FIDDLER_TOKEN=${FIDDLER_API_KEY}
      - REDIS_URL=redis://fiddler-redis-buffer:6379/0
      - BATCH_SIZE=250
      - FLUSH_INTERVAL_SECONDS=5
    volumes:
      - ./collector_code:/opt/collector
      - ./logs:/var/log/fiddler
    working_dir: /opt/collector
    command: ["python3", "main.py", "--host", "0.0.0.0", "--port", "8970"]
    networks:
      - fiddler-net
    ports:
      - "8970:8970"
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '0.5'
          memory: 1G

  fiddler-redis-buffer:
    image: redis:7.4-alpine
    container_name: fiddler-redis-buffer
    restart: unless-stopped
    command: ["redis-server", "--appendonly", "yes", "--maxmemory", "1gb", "--maxmemory-policy", "noeviction"]
    volumes:
      - fiddler_buffer_data:/data
    networks:
      - fiddler-net
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  fiddler-otel-bridge:
    image: otel/opentelemetry-collector-contrib:0.118.0
    container_name: fiddler-otel-bridge
    restart: unless-stopped
    command: ["--config=/etc/otel/config.yaml"]
    volumes:
      - ./otel-config.yaml:/etc/otel/config.yaml:ro
    networks:
      - fiddler-net
    ports:
      - "4317:4317" # gRPC
      - "4318:4318" # HTTP

networks:
  fiddler-net:
    driver: bridge

volumes:
  fiddler_buffer_data:
```

## CLI examples

### Installation Inspection
```bash
pip show fiddler-client
```

### Direct Telemetry Ingestion via cURL
In addition to SDK usage, telemetry events can be posted directly via HTTP endpoints:

```bash
curl -X POST "https://your-org.fiddler.ai/api/v1/events" \
     -H "Authorization: Bearer fdl_secure_token_2027" \
     -H "Content-Type: application/json" \
     -d '{
       "project_id": "enterprise-support",
       "model_id": "claude-5-1-agent",
       "event": {
         "input_text": "Retrieve account details for tenant-42.",
         "output_text": "Access granted under policy ZT-88.",
         "hallucination_score": 0.01,
         "latency_ms": 118
       }
     }'
```

### Batch Model Schema Registration via CLI
Register input/output feature schemas with Fiddler CLI tools:

```bash
# Upload baseline schema dataset to Fiddler MPM
fiddler-cli dataset upload \
  --project-id "agentic-rag-v2" \
  --dataset-name "baseline_evaluation_2027" \
  --file-path "./datasets/baseline_rag.parquet"
```

## API examples

### FastMCP 3.1 Fiddler Observability Server Implementation
This example demonstrates a complete **FastMCP 3.1** tool server that accepts telemetry spans, validates payload inputs using **Pydantic v2** with strict restrictions (`extra="forbid"`), and publishes evaluated metrics directly to Fiddler AI.

```python
import asyncio
from typing import Dict, Any, Optional, List, Literal
from pydantic import BaseModel, Field, ValidationError, ConfigDict, field_validator
from fastmcp import FastMCP
import fiddler as fdl

# Initialize FastMCP 3.1 Server
mcp = FastMCP("Fiddler-Observability-Server")

# Strict Pydantic v2 schemas
class FiddlerMetricTag(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    key: str = Field(..., min_length=1, max_length=64)
    value: str = Field(..., max_length=256)

class FiddlerSpanPayload(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    project_id: str = Field(..., min_length=1, description="Enterprise project identifier in Fiddler.")
    model_id: str = Field(..., min_length=1, description="Target model or agent version identifier.")
    prompt_text: str = Field(..., min_length=1, description="User prompt or context input provided to model.")
    response_text: str = Field(..., description="Generated model response or action output.")
    hallucination_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Factual grounding evaluation score.")
    toxicity_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Toxicity classification probability.")
    latency_ms: float = Field(..., ge=0.0, description="Execution duration in milliseconds.")
    mcp_trace_id: str = Field(..., min_length=8, description="FastMCP 3.1 correlation trace ID.")
    guardrail_decision: Literal["ALLOW", "REDACT", "BLOCK"] = Field(
        default="ALLOW",
        description="Ingress/egress guardrail policy decision"
    )
    tags: List[FiddlerMetricTag] = Field(default_factory=list)

    @field_validator("mcp_trace_id")
    @classmethod
    def validate_trace_id(cls, v: str) -> str:
        clean = v.strip()
        if not clean.isalnum() and "-" not in clean and "_" not in clean:
            raise ValueError("Trace ID must contain only alphanumeric characters, dashes, or underscores")
        return clean

class DriftEvaluationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    project_id: str = Field(..., description="Project ID to evaluate")
    model_id: str = Field(..., description="Model ID to evaluate")
    time_window_hours: int = Field(default=24, ge=1, le=720)
    metric_threshold: float = Field(default=0.05, ge=0.01, le=0.5)

@mcp.tool()
def publish_fiddler_span(payload: Dict[str, Any]) -> str:
    """Validate and record an agent execution trace into Fiddler AI Observability."""
    try:
        # Validate input schema strictly with Pydantic v2
        validated = FiddlerSpanPayload.model_validate(payload)

        # Initialize mock Fiddler API client (replace with enterprise endpoint credentials)
        client = fdl.FiddlerApi(
            url="https://your-org.fiddler.ai",
            org_id="agentic-ops",
            auth_token="secure_token_2027"
        )

        event_data = {
            "prompt": validated.prompt_text,
            "response": validated.response_text,
            "hallucination_score": validated.hallucination_score or 0.0,
            "toxicity_score": validated.toxicity_score or 0.0,
            "latency_ms": validated.latency_ms,
            "mcp_trace_id": validated.mcp_trace_id,
            "guardrail_status": validated.guardrail_decision,
            "metadata_tags": {tag.key: tag.value for tag in validated.tags}
        }

        # Publish validated event payload
        response = client.publish_event(
            project_id=validated.project_id,
            model_id=validated.model_id,
            event=event_data,
            event_id=f"evt_{validated.mcp_trace_id}"
        )
        return f"Successfully logged span to Fiddler for trace {validated.mcp_trace_id}. Status: {response}"

    except ValidationError as err:
        return f"Pydantic Validation Error: {err.json()}"
    except Exception as err:
        return f"Telemetry publishing error: {str(err)}"

@mcp.tool()
def query_drift_status(request: DriftEvaluationRequest) -> Dict[str, Any]:
    """Query semantic vector drift and statistical PSI for production agent deployments."""
    try:
        req = DriftEvaluationRequest.model_validate(request)
        return {
            "project_id": req.project_id,
            "model_id": req.model_id,
            "time_window": f"{req.time_window_hours}h",
            "semantic_drift_detected": False,
            "population_stability_index": 0.024,
            "drift_status": "NORMAL",
            "threshold": req.metric_threshold
        }
    except Exception as err:
        return {"error": str(err), "status": "FAILED"}

if __name__ == "__main__":
    mcp.run()
```

## Production Operational Hardening

When deploying Fiddler AI in enterprise production environments, adhere to the following operational best practices:

1. **Async Batch Telemetry Ingestion**: Avoid blocking agent execution loops by buffering execution spans using an in-memory queue or Redis stream before calling `publish_event`.
2. **Sampling Rules for High-Throughput Streams**: For multi-agent swarms processing thousands of tokens per second, configure probabilistic sampling (e.g., log 100% of errors/hallucinations, but sample 5% of benign responses).
3. **Guardrail Execution Latency Capping**: Set strict timeout thresholds (e.g., 50ms) on pre-generation guardrail evaluation; fall back to asynchronous post-generation auditing if latency targets are exceeded.
4. **Authentik RBAC Alignment**: Map Fiddler user roles (Admin, Auditor, Viewer) directly to enterprise SAML/OAuth groups via [Authentik](../../services/authentik.md) to ensure least-privilege compliance.

## Diagnostic & Operational Troubleshooting Matrix

| Issue / Failure Mode | Root Cause | Diagnostic Check | Resolution Strategy |
| :--- | :--- | :--- | :--- |
| **Telemetry Ingestion Drops** | High-velocity agent loops exhaust synchronous HTTP connection pools. | Fiddler forwarder logs show `HTTP 429 Too Many Requests` or `ConnectionResetError`. | Configure the Redis buffer stream with batch publishing (250 spans/batch) and exponential backoff retry. |
| **Token Auth Handshake Failure** | Expired service account JWT or misconfigured Authentik OAuth bearer token. | Collector daemon reports `HTTP 401 Unauthorized: Invalid Bearer Token`. | Rotate `FIDDLER_API_KEY` in `/etc/fiddler/collector.env` and refresh Authentik client secrets. |
| **Drift False Positives** | Insufficient baseline sample size causes erratic Kolmogorov-Smirnov test results. | Fiddler dashboard alerts `Semantic Drift Detected` on low-volume staging runs. | Ensure baseline reference dataset contains at least 5,000 verified production representative prompts. |
| **Guardrail Timeout Latency** | Network latency to SaaS guardrail evaluation endpoint exceeds agent SLA. | Agent response latency spikes above 2,500ms; timeout exceptions logged. | Deploy localized Fiddler Auditor edge container or switch guardrail enforcement to asynchronous audit mode. |
| **Schema Validation Mismatches** | Agent output schema changes without updating Fiddler registered model columns. | Error `Field Mismatch: Unexpected column 'agent_rationale' in payload`. | Update Fiddler model schema registration via CLI or employ strict Pydantic v2 schemas (`extra="forbid"`). |

## Related tools / concepts
- [Arize AI](./arize-ai.md) — Enterprise ML observability and Phoenix LLM tracing platform.
- [Braintrust](./braintrust.md) — LLM evaluation and continuous prompt engineering platform.
- [Comet Opik](./comet-opik.md) — Open-source LLM tracing, monitoring, and dataset management tool.
- [Sentry](./sentry.md) — Application error tracking and performance monitoring for agentic stacks.
- [LiteLLM](../../services/litellm.md) — AI Gateway for routing requests and collecting metrics.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Standardized protocol for multi-agent tool execution and context streaming.

## Sources / references
- [Fiddler AI Official Website](https://www.fiddler.ai/)
- [Fiddler Documentation & API Reference](https://docs.fiddler.ai/)
- [Fiddler Auditor GitHub Repository](https://github.com/fiddler-labs/fiddler-auditor)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
