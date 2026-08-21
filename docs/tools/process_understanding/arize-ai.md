# Arize AI

Arize AI is an enterprise platform for AI Observability and Model Performance Management (MPM). In January 2027, it serves as a central "Inference Watchtower" for enterprises deploying complex, autonomous agent networks powered by **Claude 5.1**, **GPT-5.5 / 5.6**, **Gemini 4.0 Pro / Ultra**, **DeepSeek-V4**, and local **Gemma 3** instances.

## What it is
Arize AI is an end-to-end AI observability, trace monitoring, and model evaluation platform designed for predictive ML models, RAG pipelines, and agentic workflows. Its open-source core, **Arize Phoenix**, provides local-first, OpenTelemetry-native tracing, interactive UMAP embedding visualization, and automated LLM-as-a-judge evaluation suites. Featuring native support for **FastMCP 3.1** and Identity-Aware Agent Routing, it provides zero-trust telemetry collection across distributed agent tool execution pipelines without exposing internal corporate security boundaries.

## What problem it solves
Managing autonomous AI agents in production introduces debugging challenges when models hallucinate, retrieval stages fail, or multi-agent loops enter recursive cycles. Arize AI converts qualitative "vibes-based" evaluations into quantitative engineering telemetry. By visualizing high-dimensional text embeddings, retrieval clusters, and multi-turn agent execution trees, developers can diagnose exact failure modes (such as ungrounded answers, retrieval context gaps, or unauthorized tool calls).

## Where it fits in the stack
**Category**: Process & Understanding / AI Observability. Arize AI operates in the Monitoring, Governance, and Trust layer. It ingests OpenTelemetry trace spans directly from AI Gateways (e.g., [LiteLLM](../../services/litellm.md)) or agent orchestration frameworks, feeding telemetry into evaluation pipelines, dataset curators, and continuous model fine-tuning loops.

## Typical use cases
- **Agent Reasoning & Tool Tracing**: Visualizing nested execution spans, tool parameters, and decision branches for Claude 5.1 and GPT-5.5 agents.
- **RAG Embedding Inspection**: Diagnosing vector retrieval failures using interactive UMAP cluster visualizers to identify document coverage gaps.
- **Production Hallucination & Faithfulness Evaluation**: Running real-time LLM-as-a-judge evaluators to score factual grounding and relevance on live data streams.
- **Semantic & Data Shift Detection**: Tracking embedding drift to detect shifts in user query distribution or domain vocabulary before model performance degrades.
- **Identity-Aware Tool Auditing**: Auditing agentic tool execution logs to ensure actions are strictly mapped to verified user identities and ACL policies.

## Strengths
- **Open-Source Phoenix Core**: Run complete trace visualization web interfaces and evaluation suites locally or on-premises without transmitting data to external SaaS clouds.
- **High-Dimensional Embedding Projections**: Interactive UMAP/t-SNE visualization for semantic inspection of vector search space.
- **OpenTelemetry Standardized**: Built on open OpenInference and OpenTelemetry standards, eliminating vendor lock-in.
- **Identity-Aware Telemetry**: Comprehensive access control auditing for multi-agent enterprise applications.
- **Unified Predictive & Generative Observability**: Single platform monitoring tabular ML models (XGBoost/LightGBM) alongside generative multi-agent systems.

## Limitations
- **Integration Footprint**: Complete trace instrumentation and custom evaluation setup require initial architectural configuration.
- **Telemetry Storage at Scale**: High-volume, real-time embedding tracing across large agent clusters requires dedicated trace storage management.

## When to use it
- When deploying production autonomous agents that execute sensitive database, API, or system actions.
- When troubleshooting complex RAG retrieval pipelines requiring visual inspection of vector search spaces and document chunking.
- When requiring a unified OpenTelemetry-based observability platform for both predictive ML and generative agent stacks.

## When not to use it
- For single-turn scripts or basic prototypes where terminal printing or simple log files suffice.
- For simple static applications operating without retrieval augmentation or multi-step tool execution.

## Getting started

Install Arize Phoenix for local tracing and evaluation:

```bash
pip install arize-phoenix pydantic
```

Launch the local Phoenix tracing server:

```python
import phoenix as px

session = px.launch_app()
print(f"Phoenix UI running at: {session.url}")
```

## CLI examples

### phoenix start
Launch the local Phoenix tracing server web interface:
```bash
phoenix start
```

### Exporting Traces via cURL
Retrieve raw trace spans from a running Phoenix server:
```bash
curl http://localhost:6006/v1/traces
```

## API examples

### Python: Programmatic Telemetry & Evaluation with Pydantic v2
This example demonstrates logging evaluation results to Arize Phoenix using **Pydantic v2** (`BaseModel`, `Field`, `model_validate`) for strict type safety.

```python
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError
import phoenix as px

class ArizeEvaluationMetric(BaseModel):
    eval_id: str = Field(..., description="Unique evaluation event identifier")
    span_id: str = Field(..., description="Corresponding OpenTelemetry trace span ID")
    metric_name: str = Field(..., description="Name of metric (e.g., faithfulness, hallucination)")
    score: float = Field(..., ge=0.0, le=1.0, description="Evaluated score between 0.0 and 1.0")
    explanation: Optional[str] = Field(None, description="Detailed reasoning for evaluation score")
    mcp_context: Dict[str, Any] = Field(default_factory=dict, description="FastMCP 3.1 trace context metadata")

async def export_arize_evaluation(eval_dict: Dict[str, Any]) -> bool:
    try:
        # Validate input schema strictly with Pydantic v2
        validated_metric = ArizeEvaluationMetric.model_validate(eval_dict)

        print(f"Exporting Arize Phoenix Telemetry at {datetime.now(timezone.utc).isoformat()}:")
        print(f"  Metric: {validated_metric.metric_name}")
        print(f"  Score: {validated_metric.score}")
        print(f"  Span ID: {validated_metric.span_id}")
        print(f"  MCP Version: {validated_metric.mcp_context.get('mcp_version')}")

        # In production, send to Phoenix client:
        # px.Client().log_evaluations(...)
        return True
    except ValidationError as err:
        print(f"Pydantic validation error: {err}")
        return False
    except Exception as err:
        print(f"Failed to export telemetry to Arize: {err}")
        return False

# Simulation execution
sample_eval = {
    "eval_id": "eval_9981b",
    "span_id": "span_fastmcp_3_1_abc",
    "metric_name": "faithfulness",
    "score": 0.98,
    "explanation": "Agent output is fully grounded by retrieved vector contexts.",
    "mcp_context": {
        "mcp_version": "3.1",
        "model": "claude-5-1-sonnet",
        "identity_role": "data-analyst-agent"
    }
}

asyncio.run(export_arize_evaluation(sample_eval))
```

## Related tools / concepts
- [Braintrust](./braintrust.md) — Evaluation-focused LLM developer platform and trace logs.
- [Fiddler AI](./fiddler.md) — Enterprise explainability, guardrail evaluation, and model governance platform.
- [Comet Opik](./comet-opik.md) — Open-source LLM tracing and prompt testing tool.
- [LangSmith](../benchmarking/langsmith.md) — Observability platform designed for the LangChain ecosystem.
- [LiteLLM](../../services/litellm.md) — Universal AI Gateway for request routing and metric collection.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Standardized protocol for agentic tool execution and context streaming.
- [Langfuse](./langfuse.md) — Open-source LLM engineering and analytics platform.

## Sources / references
- [Arize AI Official Portal](https://arize.com/)
- [Arize Phoenix Documentation](https://docs.arize.com/phoenix)
- [Arize Phoenix GitHub Repository](https://github.com/Arize-ai/phoenix)
- [OpenInference Tracing Specification](https://openinference.ai/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
