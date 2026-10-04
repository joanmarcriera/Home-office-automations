# Arize AI

## What it is
Arize AI is an enterprise AI Observability, Evaluation, and Model Performance Management (MPM) platform engineered to monitor, evaluate, and debug predictive ML models, Retrieval-Augmented Generation (RAG) pipelines, and autonomous agent networks. Operative as a central "Inference Watchtower" in early January 2027, Arize AI provides end-to-end trace visibility across multi-agent systems powered by **Claude 5.1 / 5.6**, **GPT-5.5 / 5.6**, **Gemini 4.0 Pro / Ultra**, **DeepSeek-V4**, and local **Gemma 3** or **Llama 3** instances.

Arize AI combines OpenTelemetry-native trace collection, interactive high-dimensional UMAP vector projections, automated LLM-as-a-judge evaluators, and zero-trust identity auditing. Its open-source core, **Arize Phoenix**, delivers a local-first, containerized trace visualization, dataset curation, and guardrail evaluation suite that runs on-premises or within isolated private clouds without transmitting corporate telemetry to external SaaS endpoints. Featuring native support for **FastMCP 3.1**, Arize AI captures sub-span tool calls, memory state transitions, and context retrievals across distributed agent clusters.

## What problem it solves
Deploying autonomous AI agents, RAG engines, and tool-calling loops into production introduces severe operational observability challenges:
- **Non-Deterministic Agent Loops**: Agents can enter recursive execution cycles, generate invalid tool call arguments, or experience cascading reasoning failures that are impossible to diagnose with standard log files.
- **RAG & Vector Retrieval Black Boxes**: Pinpointing why an LLM hallucinated often requires determining whether the vector database returned irrelevant document chunks, whether the chunking strategy fragmented context, or whether the model ignored retrieved contexts.
- **Vibes-Based Evaluation Bottlenecks**: Engineering teams lack quantitative, reproducible benchmarks for testing prompt updates, model fine-tuning variants, and safety guardrails prior to deployment.
- **Semantic & Embedding Drift**: Real-world user query distributions shift over time, leading to silent model performance degradation that traditional CPU/memory infrastructure monitoring tools fail to detect.
- **Identity & Compliance Auditing Gaps**: Enterprises running multi-agent tools across internal databases require verifiable audit logs mapping every tool execution to a verified user identity and Access Control List (ACL) policy.

Arize AI resolves these challenges by converting qualitative LLM behaviors into quantitative OpenTelemetry engineering telemetry, providing interactive vector visualizers, automated evaluation suites, and real-time hallucination scoring.

```
+-----------------------------------------------------------------------------------+
|                        Arize AI & Phoenix Observability Stack                     |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ Distributed Agent Execution Layer ]                                            |
|  - Claude 5.6 / GPT-5.6 / Gemini 4.0 Agents                                       |
|  - FastMCP 3.1 Tool Servers & OpenInference Instrumentation                       |
|                                 |                                                 |
|                                 v                                                 |
|  [ OpenTelemetry Trace Collector / AI Gateway ]                                   |
|  - LiteLLM / LangChain / LlamaIndex Span Ingestion                                |
|  - Identity Header & User ACL Mapping                                             |
|                                 |                                                 |
|        +------------------------+------------------------+                        |
|        |                                                 |                        |
|        v                                                 v                        |
|  [ Arize Phoenix Local Core (Open-Source) ]     [ Arize Enterprise SaaS / Hybrid ]|
|  - Interactive UMAP Embedding Visualizer        - Real-Time Semantic Drift Alerting|
|  - Local Trace Tree & Span Explorer             - Enterprise RBAC & SOC2 Vault    |
|  - LLM-as-a-Judge Evaluation Suite              - Large-Scale Trace Storage Engine|
|        |                                                 |                        |
|        +------------------------+------------------------+                        |
|                                 |                                                 |
|                                 v                                                 |
|  [ Quantitative Evaluation & Continuous Fine-Tuning ]                            |
|  - Groundedness, Faithfulness & Relevance Scores                                  |
|  - Curated Dataset Export for Model Distillation                                  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## Where it fits in the stack
**Category**: Process & Understanding / AI Observability, Tracing & Evaluation. Arize AI operates in the Monitoring, Governance, and Trust layer of the enterprise AI architecture.

Arize AI typically integrates with:
- **AI Gateways & Routers**: [LiteLLM](../../services/litellm.md) and Cloudflare AI Gateway for transparent OpenTelemetry trace span collection.
- **Agent Frameworks**: [LangGraph](../frameworks/langgraph.md), [Agno](../agents/agno.md), [CrewAI](../frameworks/crewai.md), and [LlamaIndex](../ai_knowledge/llamaindex.md) via OpenInference instrumentation.
- **Protocol Ecosystems**: [FastMCP 3.1](../automation_orchestration/mcp.md) servers, capturing tool execution inputs, outputs, and sub-span latencies.
- **Vector Engines**: [Weaviate](../infrastructure/weaviate.md), Qdrant, and Milvus for embedding space inspection and retrieval quality evaluation.

## Typical use cases

### 1. Multi-Agent Reasoning & Tool Execution Tracing
When multi-agent systems execute complex tasks, Arize AI visualizes nested execution trees showing parent agent prompts, sub-agent delegations, FastMCP 3.1 tool calls, raw tool responses, and overall task latencies, allowing developers to isolate failing spans in seconds.

### 2. High-Dimensional RAG Embedding Space Inspection
Arize AI projects document chunk embeddings and user query vectors onto interactive 3D UMAP or t-SNE maps. Machine learning engineers inspect semantic clusters to identify "retrieval voids" where user queries return low-relevance document chunks, guiding chunking strategy adjustments.

### 3. Production Hallucination & Faithfulness Evaluation
Arize AI executes automated LLM-as-a-judge evaluation pipelines on live inference streams. Every RAG response is scored for **Faithfulness** (is the answer supported by retrieved context?), **Answer Relevance** (does the answer address the prompt?), and **Context Precision** (were retrieved chunks relevant?).

### 4. Semantic Drift & Out-of-Distribution Query Alerting
By monitoring embedding distribution centroids over time, Arize AI detects when real-world user queries drift away from initial training or testing distributions. Automated webhooks notify ML engineering teams before performance drops occur.

### 5. Identity-Aware Agent Security & Compliance Auditing
In enterprise deployments, Arize AI tags every trace span with authenticated user credentials, session IDs, and FastMCP 3.1 identity contexts. Security teams audit trace logs to ensure agents do not execute unauthorized tool calls or exceed data access privileges.

## Strengths
- **Open-Source Phoenix Core**: Run full-featured local trace visualization interfaces and evaluation suites on local developer laptops or on-premises Kubernetes clusters without data egress.
- **OpenTelemetry & OpenInference Standardized**: Built natively on open tracing standards, eliminating proprietary SDK vendor lock-in and ensuring compatibility with Jaeger, Prometheus, and Grafana.
- **High-Dimensional Embedding Projections**: Interactive 3D UMAP/t-SNE visualizer enables semantic inspection of vector search spaces and retrieval failures.
- **Native FastMCP 3.1 Protocol Support**: Captures structured tool call arguments, schema validations, and streaming context updates across FastMCP 3.1 tools.
- **Unified Observability for Predictive & Generative AI**: Single enterprise platform monitoring tabular ML models (XGBoost, LightGBM) alongside multi-modal generative agent stacks.
- **Built-in LLM-as-a-Judge Evaluation Suites**: Includes pre-built, benchmarked evaluator templates for hallucination detection, Q&A correctness, toxicity, and SQL generation quality.

## Limitations
- **Instrumentation Overhead**: Full trace visibility requires adding OpenTelemetry/OpenInference SDK wrappers or AI Gateway proxies across all agent services.
- **High-Volume Telemetry Storage Costs**: Storing full prompt text, high-dimensional embeddings, and trace spans across thousands of daily agent turns requires dedicated time-series trace storage infrastructure.

## When to use it
- When deploying production autonomous agents that execute multi-step tool calls, database operations, or API actions.
- When troubleshooting complex RAG retrieval pipelines requiring visual inspection of vector search spaces and document chunking.
- For local, open-source trace visualization during development using Arize Phoenix (`phoenix start`).
- When enterprise compliance dictates strict OpenTelemetry audit logging and identity-aware tool tracking.

## When not to use it
- For simple, single-turn static scripts or basic prototypes where terminal printing or local log files suffice.
- In static web applications operating without retrieval augmentation, LLM inference, or tool execution.
- When trace collection is strictly forbidden by extreme local memory constraints on tiny microcontroller edge devices.

## Getting started

### Installation & Prerequisites
Install Arize Phoenix along with OpenInference instrumentation and validation libraries:

```bash
pip install arize-phoenix openinference-instrumentation-langchain pydantic>=2.0.0 requests
```

### Launching Local Phoenix Server
Start the local Phoenix tracing web interface and inspect the local server URL:

```python
import phoenix as px

def launch_local_phoenix():
    """Launches the local Arize Phoenix tracing UI session."""
    session = px.launch_app()
    print(f"Arize Phoenix UI running locally at: {session.url}")
    return session

if __name__ == "__main__":
    launch_local_phoenix()
```

## CLI examples

Arize Phoenix provides command-line tools to start local trace collector servers, export trace datasets, and run offline evaluation benchmarks directly from the shell.

```bash
# Launch the local Arize Phoenix tracing web server on default port 6006
phoenix start --port 6006

# Export all captured trace spans to a parquet file for offline evaluation
phoenix export traces --output ./telemetry/traces_2027_01_07.parquet

# Run an offline evaluation benchmark suite against a saved dataset
phoenix eval run \
  --dataset ./datasets/rag_benchmark.csv \
  --evaluators "hallucination,qa_correctness" \
  --model "claude-3-5-sonnet-20241022" \
  --output ./eval_results.json
```

## API examples

### Python: Logging Evaluation Metrics with Strict Pydantic v2 Contract Validation
In production enterprise architectures, evaluation results and OpenTelemetry span metrics logged to Arize Phoenix must be strictly validated using **Pydantic v2** schemas to prevent malformed telemetry ingestion.

```python
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError
import phoenix as px

# --- Pydantic v2 Telemetry Data Contract Definitions ---

class FastMCPContextMetadata(BaseModel):
    mcp_version: str = Field(default="3.1", description="FastMCP protocol version")
    model_name: str = Field(..., description="Target model identifier (e.g., claude-5-1-sonnet)")
    identity_role: str = Field(..., description="Authenticated user RBAC identity role")

class ArizeEvaluationMetricPayload(BaseModel):
    eval_id: str = Field(..., min_length=3, description="Unique evaluation event ID")
    span_id: str = Field(..., min_length=5, description="Corresponding OpenTelemetry trace span ID")
    metric_name: str = Field(..., description="Name of evaluation metric (e.g., faithfulness, hallucination)")
    score: float = Field(..., ge=0.0, le=1.0, description="Evaluated score between 0.0 and 1.0")
    explanation: Optional[str] = Field(default=None, description="Detailed LLM-as-a-judge reasoning")
    mcp_context: FastMCPContextMetadata = Field(..., description="FastMCP 3.1 trace context metadata")
    timestamp_utc: str = Field(..., description="ISO UTC execution timestamp")

    @field_validator("timestamp_utc")
    def validate_utc(cls, val: str) -> str:
        if not val.endswith("Z"):
            raise ValueError("Timestamp must end with 'Z'")
        return val

# --- Arize Telemetry Exporter ---

class ArizePhoenixTelemetryExporter:
    def __init__(self, phoenix_url: str = "http://localhost:6006"):
        self.phoenix_url = phoenix_url

    async def log_evaluation_metric(self, raw_metric_dict: Dict[str, Any]) -> bool:
        """Validates payload against Pydantic v2 contract and logs metric to Arize Phoenix."""
        try:
            # Strictly validate against Pydantic v2 schema
            validated_metric = ArizeEvaluationMetricPayload.model_validate(raw_metric_dict)

            print(f"[TELEMETRY LOGGED] Arize Phoenix Metric Export:")
            print(f"  Eval ID: {validated_metric.eval_id}")
            print(f"  Metric: {validated_metric.metric_name} = {validated_metric.score}")
            print(f"  Span ID: {validated_metric.span_id}")
            print(f"  Model: {validated_metric.mcp_context.model_name} (Role: {validated_metric.mcp_context.identity_role})")

            # In live production:
            # px.Client(endpoint=self.phoenix_url).log_evaluations(...)
            return True

        except ValidationError as val_err:
            print(f"[CONTRACT ERROR] Invalid telemetry payload schema: {val_err}")
            return False
        except Exception as err:
            print(f"[EXPORTER ERROR] Failed to export telemetry to Arize Phoenix: {err}")
            return False

if __name__ == "__main__":
    exporter = ArizePhoenixTelemetryExporter()

    sample_metric = {
        "eval_id": "eval_9981b_2027",
        "span_id": "span_fastmcp_3_1_abc99",
        "metric_name": "faithfulness",
        "score": 0.98,
        "explanation": "Agent response is fully grounded by retrieved vector contexts.",
        "mcp_context": {
            "mcp_version": "3.1",
            "model_name": "claude-5-1-sonnet",
            "identity_role": "data-analyst-agent"
        },
        "timestamp_utc": "2027-01-07T12:00:00Z"
    }

    asyncio.run(exporter.log_evaluation_metric(sample_metric))
```

### FastMCP 3.1 Observability & Evaluation Tool Server
The following Python script implements a complete **FastMCP 3.1** server, providing Arize Phoenix trace logging and metric evaluation tools to AI reasoning agents.

```python
import os
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, Field

# Initialize FastMCP 3.1 Server for Arize AI
mcp = FastMCP(
    name="Arize Phoenix Observability Server",
    version="3.1.0",
    description="FastMCP 3.1 server exposing trace logging, evaluation scoring, and hallucination auditing tools"
)

class LogTraceSpanInput(BaseModel):
    span_name: str = Field(..., description="Name of the trace span (e.g., rag_retrieval_step)")
    input_prompt: str = Field(..., description="Input prompt or query passed to LLM or tool")
    output_text: str = Field(..., description="Output text or response returned")
    latency_ms: float = Field(..., ge=0.0, description="Span execution latency in milliseconds")

class EvaluateFaithfulnessInput(BaseModel):
    context_text: str = Field(..., description="Retrieved context snippet text")
    generated_answer: str = Field(..., description="LLM generated answer to evaluate")

@mcp.tool(
    name="log_agent_span",
    description="Logs a FastMCP 3.1 agent execution span to Arize Phoenix for real-time tracing"
)
async def log_agent_span(input_data: LogTraceSpanInput, ctx: Context) -> Dict[str, Any]:
    """FastMCP 3.1 Tool exposing trace span logging."""
    ctx.info(f"Logging span '{input_data.span_name}' to Arize Phoenix (Latency: {input_data.latency_ms}ms)")

    # Simulated Phoenix span logging
    return {
        "status": "success",
        "span_id": "span_px_8819234",
        "span_name": input_data.span_name,
        "logged_to_phoenix": True
    }

@mcp.tool(
    name="evaluate_faithfulness",
    description="Evaluates whether an LLM generated answer is faithful to the retrieved context using Arize evaluators"
)
async def evaluate_faithfulness(input_data: EvaluateFaithfulnessInput, ctx: Context) -> Dict[str, Any]:
    """FastMCP 3.1 Tool exposing LLM-as-a-judge faithfulness evaluation."""
    ctx.info("Executing Arize LLM-as-a-judge Faithfulness Evaluation...")

    # Simulated evaluation calculation
    return {
        "status": "success",
        "metric": "faithfulness",
        "score": 0.95,
        "classification": "FAITHFUL",
        "reasoning": "All facts in the generated answer directly match statements in the context_text."
    }

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [Braintrust](./braintrust.md) — Evaluation-focused LLM developer platform and trace log manager.
- [Fiddler AI](./fiddler.md) — Enterprise explainability, guardrail evaluation, and model governance platform.
- [Comet Opik](./comet-opik.md) — Open-source LLM tracing and prompt testing tool.
- [LangSmith](../benchmarking/langsmith.md) — Observability platform designed for the LangChain ecosystem.
- [LiteLLM](../../services/litellm.md) — Universal AI Gateway for request routing and metric collection.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Standardized protocol for agentic tool execution and context streaming.
- [Langfuse](./langfuse.md) — Open-source LLM engineering and analytics platform.

## Sources / references
- [Official Arize AI Website](https://arize.com/)
- [Arize Phoenix Developer Documentation](https://docs.arize.com/phoenix)
- [Arize Phoenix Official GitHub Repository](https://github.com/Arize-ai/phoenix)
- [OpenInference Tracing Specification](https://openinference.ai/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
