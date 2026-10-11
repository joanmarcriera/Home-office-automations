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

## API examples

### FastMCP 3.1 Fiddler Observability Server Implementation
This example demonstrates a complete **FastMCP 3.1** tool server that accepts telemetry spans, validates payload inputs using **Pydantic v2**, and publishes evaluated metrics directly to Fiddler AI.

```python
import asyncio
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError, ConfigDict
from fastmcp import FastMCP
import fiddler as fdl

# Initialize FastMCP 3.1 Server
mcp = FastMCP("Fiddler-Observability-Server")

# Define strict Pydantic v2 telemetry schema
class FiddlerSpanPayload(BaseModel):
    model_config = ConfigDict(extra="forbid", freeze=True)

    project_id: str = Field(..., description="Enterprise project identifier in Fiddler.")
    model_id: str = Field(..., description="Target model or agent version identifier.")
    prompt_text: str = Field(..., description="User prompt or context input provided to model.")
    response_text: str = Field(..., description="Generated model response or action output.")
    hallucination_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Factual grounding evaluation score.")
    latency_ms: float = Field(..., ge=0.0, description="Execution duration in milliseconds.")
    mcp_trace_id: str = Field(..., description="FastMCP 3.1 correlation trace ID.")

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
            "latency_ms": validated.latency_ms,
            "mcp_trace_id": validated.mcp_trace_id
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

if __name__ == "__main__":
    mcp.run()
```

## Production Operational Hardening

When deploying Fiddler AI in enterprise production environments, adhere to the following operational best practices:

1. **Async Batch Telemetry Ingestion**: Avoid blocking agent execution loops by buffering execution spans using an in-memory queue or Redis stream before calling `publish_event`.
2. **Sampling Rules for High-Throughput Streams**: For multi-agent swarms processing thousands of tokens per second, configure probabilistic sampling (e.g., log 100% of errors/hallucinations, but sample 5% of benign responses).
3. **Guardrail Execution Latency Capping**: Set strict timeout thresholds (e.g., 50ms) on pre-generation guardrail evaluation; fall back to asynchronous post-generation auditing if latency targets are exceeded.
4. **Authentik RBAC Alignment**: Map Fiddler user roles (Admin, Auditor, Viewer) directly to enterprise SAML/OAuth groups via [Authentik](../../services/authentik.md) to ensure least-privilege compliance.

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
