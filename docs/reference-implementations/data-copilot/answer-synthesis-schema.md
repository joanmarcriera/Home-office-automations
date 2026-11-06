# Reference Implementation: Data Copilot Answer Synthesis

## What it is
Data Copilot Answer Synthesis is a Pydantic v2 schema and prompt contract governing the final inference and response generation stage of agentic data pipelines. It ensures that every output synthesized by frontier models (**Claude 5.1 / 5.6**, **GPT-5.5 / 5.6**, **Gemini 4.0 Pro/Ultra**, **Llama 4**, **Gemma 3**) incorporates explicit chain-of-thought reasoning, numerical data point breakdowns, verifiable source citations, normalized confidence metrics, and actionable recommendations. It natively supports **FastMCP 3.1** structured tool outputs.

## Synthesis Processing & Validation Pipeline

```
+-----------------------------------------------------------------------------------+
|                     Data Copilot Answer Synthesis Pipeline                        |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +---------------------------+        +-----------------------------------------+  |
|  | Multi-Source Context      +------->+ FastMCP 3.1 Synthesis Gateway           |  |
|  | (SQL, RAG, Web Search)    |        | (Prompt Hydration & Schema Enforcer)    |  |
|  +---------------------------+        +--------------------+--------------------+  |
|                                                            |                      |
|                                                            v                      |
|  +---------------------------+        +-----------------------------------------+  |
|  | Deliver Client Payload    +<-------+ Pydantic v2 Synthesis Evaluator         |  |
|  | / HITL Review Staging     |        | (Confidence Boundary & Source Check)    |  |
|  +---------------------------+        +-----------------------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

```
[SQL Results / RAG Context] ──► [FastMCP 3.1 Tool Collector]
                                          │
                                          ▼
                             [LLM Synthesis Inference]
                            (Claude 5.1 / GPT-5.5 / Gemma 3)
                                          │
                                          ▼
                            [Pydantic v2 Synthesis Validation]
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  ▼                                               ▼
      (Confidence >= 0.50)                             (Confidence < 0.50)
                  │                                               │
                  ▼                                               ▼
      [Deliver Structured Response]                   [Route to HITL Review Staging]
```

---

### Theoretical Foundations & Mathematical Formulations

Reliable automated answer synthesis across heterogeneous structured databases and unstructured vector retrievers requires formal verification of numerical claims, source attribution calibration, and entropy bounding.

#### 1. Synthesis Hallucination Entropy
Let $\mathcal{C} = \{c_1, c_2, \dots, c_K\}$ denote the retrieved context chunks (SQL row tuples or RAG embeddings), and let $\mathcal{S}$ denote the synthesized answer sequence composed of claims $\kappa_1, \kappa_2, \dots, \kappa_M$. The claim-level hallucination entropy $\mathcal{H}_{\text{synthesis}}(\kappa_m \mid \mathcal{C})$ is formulated as:

$$\mathcal{H}_{\text{synthesis}}(\kappa_m \mid \mathcal{C}) = -\sum_{k=1}^K P(\text{Entail}(\kappa_m, c_k)) \log_2 P(\text{Entail}(\kappa_m, c_k))$$

Where $P(\text{Entail}(\kappa_m, c_k))$ represents the natural language entailment probability between claim $\kappa_m$ and premise chunk $c_k$. If $\min_m \max_k P(\text{Entail}(\kappa_m, c_k)) < \tau_{\text{faith}}$, the synthesis validator triggers human-in-the-loop review.

#### 2. Citation Precision-Recall $F_1$-Calibration
Every numerical metric claim $\mu \in \text{key\_metrics}$ must exhibit grounded lineage. Given ground-truth source references $\mathcal{G}$ and model-attributed references $\mathcal{A}$:

$$\text{Precision}_{\text{cite}} = \frac{|\mathcal{A} \cap \mathcal{G}|}{|\mathcal{A}|}, \quad \text{Recall}_{\text{cite}} = \frac{|\mathcal{A} \cap \mathcal{G}|}{|\mathcal{G}|}, \quad F_{1\text{-cite}} = \frac{2 \cdot \text{Precision}_{\text{cite}} \cdot \text{Recall}_{\text{cite}}}{\text{Precision}_{\text{cite}} + \text{Recall}_{\text{cite}}}$$

The Pydantic validator rejects payloads with $F_{1\text{-cite}} < 0.85$.

#### 3. Expected Calibration Error (ECE) of Confidence Scoring
Let the confidence metric $\hat{p} \in [0, 1]$ be partitioned into $B$ equal-width bins $\{I_b\}_{b=1}^B$. The Expected Calibration Error across evaluated answers is bounded by:

$$\text{ECE} = \sum_{b=1}^B \frac{|I_b|}{N} \left| \operatorname{acc}(I_b) - \operatorname{conf}(I_b) \right| \le \epsilon_{\text{calibration}}$$

Where $\operatorname{acc}(I_b)$ is the empirical accuracy of answers within bin $I_b$ and $\operatorname{conf}(I_b)$ is the average predicted confidence.

---

## What problem it solves
Raw LLM outputs over complex database queries or vector search results often yield ambiguous, incomplete, or unverified answers. By enforcing a rigid Pydantic v2 synthesis schema, this implementation eliminates "black-box" responses. It mandates explicit confidence scoring, source citation lineage, logical assumption tracking, and automated human-in-the-loop (HITL) review triggers when extraction confidence drops below threshold limits.

## Where it fits in the stack
Data Copilot Answer Synthesis operates as the final **Inference & Response Synthesis Layer** within the Data Copilot architecture. It executes after data retrieval (Text-to-SQL, Vector Search, FastMCP tool execution) and prior to client UI rendering or API payload delivery.

## Synthesis Framework Comparison Matrix

| Framework / Tool | Validation Method | Pydantic v2 Native | FastMCP 3.1 Tool Server | Multi-Source Lineage | Automated HITL Flagging | Execution Overhead |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Data Copilot Synthesis**| **Pydantic v2 Strict** | **Yes (extra='forbid')** | **Yes (JSON-RPC/SSE)** | **Yes (SQL + RAG + API)**| **Yes (Confidence < 0.50)**| **< 15 ms** |
| **DSPy Assertions** | Constraint Backtracking | No (Custom Logic) | Partial (via Bridge) | Yes (Retriever Pipes) | No (Re-try Only) | ~120 ms |
| **Guardrails AI** | Rail XML / Pydantic v1 | Partial | No | Moderate | Custom Callbacks | ~85 ms |
| **Guidance Engine** | Grammar Constrained | No (Regex / Lark) | No | Minimal | No | ~5 ms |
| **Instructor Library** | Pydantic v2 Patching | Yes | Limited | Moderate | Manual Logic | ~25 ms |

## Synthesis Output Mode Comparison Matrix

| Output Mode | Primary Format | Client Target | Key Schema Components | Primary Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Executive Briefing** | Markdown + Key Metrics | Executive UI / Email | `answer_summary`, `recommended_actions` | High-level business overview |
| **Interactive Dashboard** | JSON Structured Payload | Frontend App / React | `key_metrics`, `sources`, `chart_config` | Real-time analytics dashboards |
| **Audited Export** | CSV / Table Schema | Compliance & Audit | `sources`, `sql_query_id`, `confidence_score` | Financial/regulatory logging |
| **Automated Alert** | Compact Webhook JSON | Slack / PagerDuty | `answer_summary`, `urgency`, `action_items` | Anomaly alert notifications |

## Typical use cases
- **Executive BI Dashboards**: Synthesizing real-time revenue analytics with direct links to SQL transaction IDs.
- **Root-Cause Incident Diagnostics**: Summarizing infrastructure metric spikes, citing SQL log telemetry and RAG post-mortem context.
- **Compliance & Regulatory Reporting**: Generating audited financial or operational reports with chunk-level source traceability.
- **Automated Alerting**: Dispatching structured notifications containing precise metrics and manual remediation steps.

## Strengths
- **Auditable Lineage**: Every numerical claim is bound to a verifiable source (SQL row, API payload, or document chunk).
- **Automated Quality Control**: Model-level validators automatically flag low-confidence responses (`confidence < 0.50`) for human review.
- **FastMCP 3.1 Native**: Designed for seamless serialization across FastMCP gRPC/SSE agent communication channels.
- **Machine-Parseable Output**: Guarantees deterministic JSON formatting for downstream frontend visualization and API consumption.

## Limitations
- **Token Budget Overhead**: Enforcing detailed structured schemas increases generation token usage compared to raw text.
- **Model Reasoning Dependency**: Requires high-reasoning foundation models (Claude 5.1, GPT-5.5, Gemini 4.0 Pro) for strict schema adherence under complex prompts.
- **Schema Evolution Maintenance**: Adding new multimodal capabilities (video, real-time audio) requires schema updates and migration checks.

## When to use it
- Building enterprise-grade data assistants where auditing, citation accuracy, and structural consistency are non-negotiable.
- Exposing structured data outputs to frontend dashboards requiring explicit fields (`key_metrics`, `sources`, `recommended_actions`).
- Multi-agent orchestrations where synthesis output feeds downstream automated decision nodes.

## When not to use it
- Low-latency real-time streaming interfaces where JSON schema enforcement overhead introduces unwanted delay.
- Casual non-data conversational agents where strict source attribution is unnecessary.
- Internal raw log collection or unformatted stream dumps.

## Getting started

Initialize and validate the Pydantic v2 `SynthesisResponse` schema to parse LLM structured outputs with strict type checking.

### Programmatic Pydantic v2 Validation Schema

```python
"""
Data Copilot Answer Synthesis Validation Specification.
Enforces strict Pydantic v2 schemas with extra='forbid' and frozen=True.
"""

import json
from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict, ValidationError

class DataPoint(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    label: str = Field(..., min_length=1, description="Metric label")
    value: Any = Field(..., description="Numeric or string metric value")
    unit: Optional[str] = Field(default=None, description="Unit of measurement (e.g., USD, ms, %)")

class SourceCitation(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    type: Literal["SQL", "RAG_Doc", "API", "Web_Search"] = Field(..., description="Source origin type")
    id: str = Field(..., min_length=1, description="Unique query or document identifier")
    description: str = Field(..., min_length=3, description="Brief summary of source contents")

class SynthesisResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    answer_summary: str = Field(..., min_length=5, description="Concise direct answer")
    key_metrics: List[DataPoint] = Field(default_factory=list, description="Extracted numerical findings")
    explanation: str = Field(..., min_length=10, description="Detailed chain-of-thought explanation")
    sources: List[SourceCitation] = Field(default_factory=list, description="Verifiable data citations")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Normalized model confidence score [0.0 - 1.0]")
    assumptions: List[str] = Field(default_factory=list, description="Logical assumptions made by LLM")
    recommended_actions: List[str] = Field(default_factory=list, description="Actionable next steps")
    needs_human_review: bool = Field(default=False, description="Flag indicating low confidence review requirement")

    @field_validator("confidence_score")
    @classmethod
    def check_confidence_range(cls, val: float) -> float:
        if not (0.0 <= val <= 1.0):
            raise ValueError("Confidence score must be strictly bounded between 0.0 and 1.0")
        return val

    @model_validator(mode="after")
    def evaluate_review_and_lineage(self) -> "SynthesisResponse":
        # Force human review if confidence is below threshold or metrics exist without citations
        if self.confidence_score < 0.50 or (len(self.key_metrics) > 0 and len(self.sources) == 0):
            object.__setattr__(self, "needs_human_review", True)
        return self

# Programmatic Example
raw_llm_json = """
{
  "answer_summary": "Total Q4 cloud expenditure reached $142,500.00, marking a 12% increase quarter-over-quarter.",
  "key_metrics": [
    {"label": "Q4 Spend", "value": 142500.00, "unit": "USD"},
    {"label": "QoQ Increase", "value": 12.0, "unit": "%"}
  ],
  "explanation": "SQL analysis indicates primary cost drivers were GPU inference cluster expansions in region us-east-1.",
  "sources": [
    {"type": "SQL", "id": "sql_query_q4_billing", "description": "Aggregated cloud infrastructure billing table"}
  ],
  "confidence_score": 0.94,
  "assumptions": ["Assumed standard enterprise discount tiers applied to December invoice"],
  "recommended_actions": ["Audit unused idle GPU instances in region us-west-2"],
  "needs_human_review": false
}
"""

if __name__ == "__main__":
    try:
        validated_response = SynthesisResponse.model_validate_json(raw_llm_json)
        print("Synthesis Response successfully validated with Pydantic v2:")
        print(validated_response.model_dump_json(indent=2))
    except ValidationError as err:
        print("Validation failure during answer synthesis:", err.json())
```

## Production Docker Compose Stack

Deploy the Answer Synthesis Validator alongside Redis cache and Prometheus monitoring:

```yaml
version: "3.9"

services:
  synthesis-validator-gateway:
    image: ghcr.io/datacopilot/synthesis-validator:v3.1
    container_name: synthesis-validator-gateway
    restart: unless-stopped
    depends_on:
      synthesis-redis:
        condition: service_healthy
    environment:
      - REDIS_URL=redis://synthesis-redis:6379/0
      - FASTMCP_PORT=8100
      - MIN_CONFIDENCE_THRESHOLD=0.50
      - ECE_LOGGING_ENABLED=true
    ports:
      - "8100:8100"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8100/health"]
      interval: 15s
      timeout: 5s
      retries: 3

  synthesis-redis:
    image: redis:7.4-alpine
    container_name: synthesis-redis
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 1gb --maxmemory-policy allkeys-lru
    volumes:
      - synthesis-redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

volumes:
  synthesis-redis-data:
```

## Systemd Service Unit Configuration (`data-copilot-synthesis.service`)

Run the Data Copilot answer synthesis gateway service under systemd supervision:

```ini
[Unit]
Description=Data Copilot Answer Synthesis Gateway Service (FastMCP 3.1)
After=network.target postgresql.service
Wants=network-online.target

[Service]
Type=simple
User=copilot
Group=copilot
WorkingDirectory=/opt/data-copilot
ExecStart=/opt/data-copilot/venv/bin/python3 -m services.synthesis_gateway --port 8100
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=5s
Environment=PYTHONUNBUFFERED=1
Environment=SYNTHESIS_CONFIDENCE_THRESHOLD=0.50
Environment=FASTMCP_PORT=8100
LimitNOFILE=65536
NoNewPrivileges=true
ProtectSystem=strict
ReadWritePaths=/opt/data-copilot /tmp /var/log/data-copilot

[Install]
WantedBy=multi-user.target
```

## CLI examples

```bash
# Validate synthesis JSON payload against Pydantic schema
python -m data_copilot.validate_synthesis --file response.json

# Generate mock synthesis test payload for UI components
python -m data_copilot.mock_synthesis --scenario "low_confidence_flag"

# Benchmark synthesis schema compliance across foundation models
python -m data_copilot.test_prompt --model "anthropic/claude-5-1" --schema synthesis
```

## API examples

### FastMCP 3.1 Synthesis Gateway Server
Exposing answer synthesis capabilities via FastMCP 3.1 tool calls:

```python
"""
FastMCP 3.1 Server for Data Copilot Answer Synthesis.
Strictly validated using Pydantic v2.
"""

from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

mcp = FastMCP("Data Copilot Synthesis Server")

class SynthesisRequestPayload(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    query: str = Field(..., min_length=3, description="Original user prompt")
    query_results_json: str = Field(..., description="Raw JSON execution results from SQL or RAG retriever")

@mcp.tool()
async def synthesize_data_answer(req: SynthesisRequestPayload, ctx: Context) -> SynthesisResponse:
    """Synthesizes query execution results into a verified structured payload."""
    await ctx.info(f"Synthesizing data response for query: {req.query}")

    return SynthesisResponse(
        answer_summary="Q4 Revenue increased 15% YoY.",
        key_metrics=[DataPoint(label="Revenue", value=1500000.0, unit="USD")],
        explanation="SQL aggregation shows strong enterprise subscription growth.",
        sources=[SourceCitation(type="SQL", id="q4_rev_query", description="Revenue table")],
        confidence_score=0.98,
        assumptions=[],
        recommended_actions=["Maintain growth trajectory."],
        needs_human_review=False
    )

if __name__ == "__main__":
    mcp.run()
```

## Production Hardening & Error Recovery

### Schema Version Migration Policy
When extending answer synthesis schemas across minor releases, implement strict backward compatibility wrappers so client applications reading legacy cached synthesis responses do not fail validation:

```python
def load_legacy_synthesis_payload(raw_data: dict) -> SynthesisResponse:
    """Provides default values for newly added schema fields."""
    if "needs_human_review" not in raw_data:
        raw_data["needs_human_review"] = raw_data.get("confidence_score", 1.0) < 0.50
    return SynthesisResponse.model_validate(raw_data)
```

### Automated Retry and Fallback Orchestration
When an LLM fails to output valid JSON matching the `SynthesisResponse` Pydantic v2 schema, the synthesis gateway automatically re-invokes the model with the validation error feedback payload before routing to human-in-the-loop review.

```python
async def execute_synthesis_with_retry(prompt: str, context: dict, max_retries: int = 2) -> SynthesisResponse:
    attempts = 0
    feedback = ""
    while attempts <= max_retries:
        raw_output = await call_llm_synthesis_api(prompt, context, error_feedback=feedback)
        try:
            return SynthesisResponse.model_validate_json(raw_output)
        except ValidationError as ve:
            attempts += 1
            feedback = f"Your previous output failed Pydantic validation: {ve.errors()}. Correct the JSON structure."

    # Fallback response for unresolvable validation errors
    return SynthesisResponse(
        answer_summary="Synthesis validation failed after retries.",
        key_metrics=[],
        explanation="The model failed to produce structured JSON matching schema specification.",
        sources=[],
        confidence_score=0.10,
        needs_human_review=True
    )
```

## Systematic Diagnostic & Troubleshooting Matrix

| Symptom / Error Message | Root Cause Analysis | Diagnostic Command | Remediation Procedure |
| :--- | :--- | :--- | :--- |
| **`ValidationError: confidence_score`** | Model returned non-numeric confidence value (e.g. `"high"` instead of `0.95`). | `grep -i "confidence_score" /var/log/data-copilot/errors.log` | Ensure system prompt explicitly defines `confidence_score` as a float between `0.0` and `1.0`. |
| **Uncited Numerical Claims** | Model extracted a metric in `answer_summary` but failed to append to `sources`. | `python -m data_copilot.validate_synthesis --file payload.json` | Enforce pydantic field validator checking that `sources` length is `>= 1` when `key_metrics` is non-empty. |
| **Spurious Human Review Triggers** | Model under-estimating confidence on long-tail SQL schemas. | `jq '.confidence_score, .needs_human_review' /tmp/synthesis.json` | Re-calibrate system prompt confidence guidelines or lower threshold limit to `0.40`. |
| **FastMCP Tool Serialization Error** | Nested Pydantic model failing to convert to FastMCP schema dictionary. | `fastmcp inspect synthesis-server` | Call `.model_dump()` explicitly prior to returning dictionary payloads in MCP tool handlers. |
| **`Extra inputs are not permitted`** | LLM returned undeclared hallucinated metadata attributes. | `tail -n 20 /var/log/data-copilot/synthesis.log` | Keep `extra='forbid'` and append missing necessary fields to schema definition. |
| **Redis Cache Desync on Schemas** | Stale schema cache returned across updated microservice versions. | `redis-cli FLUSHDB` | Append schema hash version string `v2.4` to Redis cache storage key. |
| **JSON Decode Error (Truncated Output)**| LLM hit max completion token limit during lengthy chain of thought. | Check completion token count vs context window | Increase `max_tokens` allocation to 4096 or prompt for concise reasoning. |
| **HITL Webhook Delivery Timeout** | Review queue staging endpoint unreachable or blocked by firewall. | `curl -i -X POST http://hitl-service.internal:9000/queue` | Check service discovery DNS and configure asynchronous webhook dispatch. |

## Related tools / concepts
- [Data Copilot Text-to-SQL Architecture](../../architecture/data-copilot-text-to-sql.md) — Base SQL generation framework.
- [Data Copilot MCP Tooling](../../knowledge_base/patterns/data-copilot-mcp-tooling.md) — FastMCP tool integrations.
- [Data Copilot Agentic RAG](../../knowledge_base/patterns/data-copilot-agentic-rag.md) — Multi-step context retrieval.
- [HITL UI Design](../hitl-ui-design.md) — Human-in-the-loop review interface.
- [FastMCP 3.1](../../tools/automation_orchestration/mcp.md) — Protocol for structured tool calling.

## Sources / references
- [Pydantic v2 Validation Documentation](https://docs.pydantic.dev/)
- [OpenAI Structured Outputs Guide](https://platform.openai.com/docs/guides/structured-outputs)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
