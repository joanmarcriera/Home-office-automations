# Fiddler AI

Fiddler is an Enterprise-grade Model Performance Management (MPM) platform that has expanded to include specialized tools for LLM observability, safety monitoring, and continuous evaluation (Fiddler Auditor and Fiddler AI Observability). In the late October / November 2026 landscape, it is a primary choice for monitoring frontier models like [Gemma 3](../ai_knowledge/local_llms.md), Claude 5.1, GPT-5.5, and Gemini 4.0 in production environments using FastMCP 3.1 for ultra-low latency execution and automated tool discovery.

## What it is
Fiddler is a comprehensive AI observability and governance platform designed to provide trust and transparency for machine learning, unstructured data, and generative AI systems. It features **Fiddler Auditor**, an open-source evaluation library for red-teaming, pre-production robustness testing, and prompt stress-testing, and **Fiddler AI Observability**, which provides real-time monitoring, embedding-based drift detection, and advanced explainability (XAI) for LLMs in production. It specializes in high-fidelity monitoring of complex multi-step reasoning chains and multi-modal outputs via the MCP 3.1 Task Protocol.

## What problem it solves
For enterprises, deploying generative AI isn't just about accuracy; it's about governance, alignment, safety, and operational risk mitigation. Fiddler provides a robust framework for:
- **Toxity and Hallucination Mitigation**: Detecting factuality gaps, grounding issues, and harmful content in production streams.
- **Model Drift & Data Shifts**: Identifying when model performance degrades over time due to upstream changes or user base shifts.
- **Explainability (XAI)**: Demystifying the "black box" of frontier models by tracing feature attribution for tabular or unstructured pipelines, helping teams understand *why* an AI agent made a specific recommendation or executed a particular action.
- **Agentic Session Diagnostics**: Pinpointing exactly which step in a multi-turn agentic workflow failed or executed an unauthorized tool call.

## Where it fits in the stack
**Category**: Process & Understanding / Enterprise AI Observability
Fiddler serves as the governance, trust, and validation layer for agentic and LLM applications. It sits between the Inference Plane (e.g., [LiteLLM](../../services/litellm.md)) and application execution runtimes, leveraging FastMCP 3.1 to dynamically inject low-latency telemetry instrumentation without slowing down the core user experience.

## Typical use cases
- **Frontier LLM Safety Monitoring**: Real-time checking of inputs/outputs against PII, toxic phrases, and prompt injection attempts for models like Claude 5.1 and GPT-5.5.
- **Embedding Drift Detection**: Monitoring vector embeddings to detect semantic drift in production queries, signaling a need for database updates or prompt modifications.
- **Root Cause Analysis in RAG**: Using explainability features to trace retrieval errors versus reasoning failures.
- **Compliance & Fair Auditing**: Reviewing model decisions in regulated sectors (such as insurance, lending, and healthcare) to ensure fairness metrics are maintained.
- **Pre-deployment Red-Teaming**: Stress-testing LLM robustness using automated adversarial prompts via Fiddler Auditor.

## Strengths
- **Enterprise-Ready Governance**: Built with granular role-based access control (RBAC), multi-tenant security, and robust audit logging.
- **Multimodal & Hybrid Capabilities**: Able to monitor traditional ML models (regression, classification) and modern LLMs/VLM systems in a single dashboard.
- **Advanced Explainability**: Industry-leading feature attribution engines for tabular, text, and embedding spaces.
- **FastMCP 3.1 Native Integration**: High-efficiency server hosting and dynamic tool discovery, permitting real-time telemetry extraction.
- **Custom Metric Support**: Allows teams to define and compute bespoke evaluation metrics on live production logs.

## Limitations
- **High Complexity**: Highly feature-dense, which can introduce a steep learning curve for solo developers or early-stage startups.
- **Resource Constraints**: High-frequency, high-throughput monitoring of multi-modal streams can incur substantial compute overhead, requiring careful sampling configuration.
- **Proprietary Core**: While Fiddler Auditor is open-source, the central enterprise dashboard, monitoring engine, and explainability analytics suite require a commercial license.

## When to use it
- When deploying generative or predictive AI in highly regulated domains where model audit trails are legally mandated.
- When you require continuous, live evaluation of LLM-as-a-judge patterns or semantic embedding drift across thousands of requests per second.
- When debugging complex multi-turn autonomous agents or RAG pipelines requiring precise step-by-step diagnostic tracing.

## When not to use it
- For early-stage sandbox prototypes or simple hobby apps where basic local logging tools (e.g., [LangSmith](../benchmarking/langsmith.md) or open-source trace libraries) are sufficient.
- If you are running lightweight, localized deployments on personal devices with zero internet connectivity and minimal audit requirements.

## Getting started

To begin auditing and monitoring with Fiddler, install the client library:

```bash
pip install fiddler-client pydantic
```

Establish a session with your enterprise Fiddler cluster:

```python
import fiddler as fdl

# Initialize connection
client = fdl.FiddlerApi(
    url="https://your-org.fiddler.ai",
    org_id="enterprise_core",
    auth_token="fdl_secure_token_abc123"
)
```

## CLI examples

### fiddler-client
Validate the local installation of the Fiddler SDK:
```bash
pip show fiddler-client
```

### curl (Publishing Live Agent Telemetry)
In addition to the python client, telemetry payloads can be ingested directly via standard REST requests:
```bash
curl -X POST "https://your-org.fiddler.ai/api/v1/events" \
     -H "Authorization: Bearer fdl_secure_token_abc123" \
     -H "Content-Type: application/json" \
     -d '{
       "project_id": "customer-success",
       "model_id": "claude-5-1-agent",
       "event": {
         "input_text": "Retrieve account details for user-99.",
         "output_text": "Access denied. Insufficient permissions.",
         "safety_score": 0.99,
         "latency_ms": 142
       }
     }'
```

### python -m fiddler
Checking client CLI integration metrics:
```bash
python -m fiddler --help
```

## API examples

### Python (Telemetry Logging with Pydantic v2 & FastMCP 3.1 Schemas)
This example demonstrates registering a model schema and logging an evaluated interaction from Claude 5.1 using Pydantic v2 to guarantee type-safety and alignment with MCP 3.1 structure:

```python
import asyncio
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, EmailStr
import fiddler as fdl

# Define strict payload schemas using Pydantic v2
class LLMTelemetryPayload(BaseModel):
    query: str = Field(..., description="The user query submitted to the LLM.")
    response: str = Field(..., description="The model generated output.")
    model_version: str = Field(default="claude-5.1-sonnet", description="Frontier model version used.")
    latency_seconds: float = Field(..., ge=0.0, description="Latency of the response in seconds.")
    hallucination_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Evaluated score for hallucination probability.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Model Context Protocol v3.1 context metadata.")

# Async function to process and log telemetry to Fiddler
async def log_telemetry_event(payload_data: Dict[str, Any]) -> bool:
    try:
        # Validate input schema strictly using Pydantic v2
        validated_payload = LLMTelemetryPayload(**payload_data)

        # Setup connection to Fiddler service
        client = fdl.FiddlerApi(
            url="https://your-org.fiddler.ai",
            org_id="operations",
            auth_token="secure_token_xyz"
        )

        # Publish validated event payload
        response = client.publish_event(
            project_id="customer-care-agents",
            model_id="support-agent-v2",
            event=validated_payload.model_dump(),
            event_id=f"evt_{validated_payload.model_version}_{int(validated_payload.latency_seconds * 1000)}"
        )
        print(f"Successfully logged event. Fiddler Response: {response}")
        return True
    except Exception as e:
        print(f"Failed to log telemetry: {e}")
        return False

# Simulation execution
test_data = {
    "query": "How do I upgrade to MCP 3.1 and FastMCP?",
    "response": "Ensure you are using the latest package releases and apply custom validation schemas.",
    "model_version": "claude-5.1-sonnet",
    "latency_seconds": 0.852,
    "hallucination_score": 0.02,
    "metadata": {
        "mcp_version": "3.1",
        "fastmcp_active": True,
        "tool_routing": "identity-aware"
    }
}

asyncio.run(log_telemetry_event(test_data))
```

## Related tools / concepts
- [Arize AI](./arize-ai.md) — Enterprise-grade alternative for real-time model performance management.
- [Braintrust](./braintrust.md) — Comprehensive developer evaluation platform for LLM applications.
- [Comet Opik](./comet-opik.md) — Open-source LLM tracing, monitoring, and dataset management tool.
- [Sentry](./sentry.md) — Full stack exception tracking for generative AI applications.
- [Model Context Protocol](../automation_orchestration/mcp.md) — The universal open standard for multi-agent capabilities.
- [LiteLLM](../../services/litellm.md) — Centralized multi-model gateway used to routing model requests and collecting telemetry.
- [LLM Security & Privacy](../../knowledge_base/llm_security_privacy.md) — Core governance patterns that Fiddler actively enforces.

## Sources / references
- [Fiddler AI Corporate Portal](https://www.fiddler.ai/)
- [Fiddler Enterprise API & SDK Reference](https://docs.fiddler.ai/api)
- [Fiddler Auditor Project Repository](https://github.com/fiddler-labs/fiddler-auditor)
- [Model Context Protocol v3.1 Specification](https://modelcontextprotocol.io/specification)

## Contribution Metadata
- Last reviewed: 2026-11-05
- Confidence: high
