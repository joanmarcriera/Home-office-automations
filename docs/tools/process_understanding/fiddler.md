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
pip install fiddler-client pydantic
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

### Python: Telemetry Ingestion with Pydantic v2 & FastMCP 3.1
This example demonstrates registering and validating agent execution telemetry using **Pydantic v2** (`BaseModel`, `Field`, `model_validate`) for strict type safety.

```python
import asyncio
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError
import fiddler as fdl

# Define telemetry validation schema using Pydantic v2
class LLMTelemetryPayload(BaseModel):
    query: str = Field(..., description="The user query or agent prompt input.")
    response: str = Field(..., description="The generated model output or action response.")
    model_version: str = Field(default="claude-5-1-sonnet", description="Model architecture identifier.")
    latency_seconds: float = Field(..., ge=0.0, description="End-to-end execution latency in seconds.")
    hallucination_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Evaluated factual grounding score.")
    mcp_metadata: Dict[str, Any] = Field(default_factory=dict, description="FastMCP 3.1 trace and context metadata.")

async def log_fiddler_telemetry(payload_dict: Dict[str, Any]) -> bool:
    try:
        # Validate input schema strictly with Pydantic v2
        validated = LLMTelemetryPayload.model_validate(payload_dict)

        client = fdl.FiddlerApi(
            url="https://your-org.fiddler.ai",
            org_id="agentic-ops",
            auth_token="secure_token_2027"
        )

        response = client.publish_event(
            project_id="customer-service-agents",
            model_id="support-agent-v3",
            event=validated.model_dump(),
            event_id=f"evt_{validated.model_version}_{int(validated.latency_seconds * 1000)}"
        )
        print(f"Successfully published Fiddler telemetry: {response}")
        return True
    except ValidationError as err:
        print(f"Pydantic validation error: {err}")
        return False
    except Exception as err:
        print(f"Failed to publish event to Fiddler: {err}")
        return False

# Execute simulation
sample_event = {
    "query": "How do I upgrade my mesh network node using FastMCP 3.1?",
    "response": "Deploy the updated FastMCP daemon and configure identity routing.",
    "model_version": "claude-5-1-sonnet",
    "latency_seconds": 0.412,
    "hallucination_score": 0.01,
    "mcp_metadata": {
        "mcp_version": "3.1",
        "transport": "stdio",
        "tool_name": "network_upgrade"
    }
}

asyncio.run(log_fiddler_telemetry(sample_event))
```

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
