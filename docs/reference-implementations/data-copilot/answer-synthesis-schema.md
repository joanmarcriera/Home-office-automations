# Reference Implementation: Data Copilot Answer Synthesis

## What it is
Data Copilot Answer Synthesis is a Pydantic v2 schema and prompt contract governing the final inference and response generation stage of agentic data pipelines. It ensures that every output synthesized by frontier models (**Claude 5.1 / 5.6**, **GPT-5.5 / 5.6**, **Gemini 4.0 Pro/Ultra**, **Llama 4**, **Gemma 3**) incorporates explicit chain-of-thought reasoning, numerical data point breakdowns, verifiable source citations, normalized confidence metrics, and actionable recommendations. It natively supports **FastMCP 3.1** structured tool outputs.

## What problem it solves
Raw LLM outputs over complex database queries or vector search results often yield ambiguous, incomplete, or unverified answers. By enforcing a rigid Pydantic v2 synthesis schema, this implementation eliminates "black-box" responses. It mandates explicit confidence scoring, source citation lineage, logical assumption tracking, and automated human-in-the-loop (HITL) review triggers when extraction confidence drops below threshold limits.

## Where it fits in the stack
Data Copilot Answer Synthesis operates as the final **Inference & Response Synthesis Layer** within the Data Copilot architecture. It executes after data retrieval (Text-to-SQL, Vector Search, FastMCP tool execution) and prior to client UI rendering or API payload delivery.

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

```python
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator, model_validator, ValidationError

class DataPoint(BaseModel):
    label: str = Field(..., description="Metric label")
    value: Any = Field(..., description="Numeric or string metric value")
    unit: Optional[str] = Field(default=None, description="Unit of measurement (e.g., USD, ms, %)")

class SourceCitation(BaseModel):
    type: str = Field(..., description="Source origin type: SQL, RAG_Doc, API")
    id: str = Field(..., description="Unique query or document identifier")
    description: str = Field(..., description="Brief summary of source contents")

class SynthesisResponse(BaseModel):
    answer_summary: str = Field(..., description="Concise 1-2 sentence direct answer")
    key_metrics: List[DataPoint] = Field(default_factory=list, description="Extracted numerical findings")
    explanation: str = Field(..., description="Detailed chain-of-thought explanation")
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
    def evaluate_review_requirement(self) -> "SynthesisResponse":
        if self.confidence_score < 0.50:
            self.needs_human_review = True
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
  "recommended_actions": ["Audit unused idle GPU instances in region us-west-2"]
}
"""

try:
    validated_response = SynthesisResponse.model_validate_json(raw_llm_json)
    print("Synthesis Response successfully validated with Pydantic v2:")
    print(validated_response.model_dump_json(indent=2))
except ValidationError as err:
    print("Validation failure during answer synthesis:", err.json())
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

```python
from data_copilot.synthesis import AnswerSynthesizer
from data_copilot.models import SynthesisResponse

# Instantiate synthesizer with FastMCP 3.1 support
synthesizer = AnswerSynthesizer(model="claude-5-1", use_fastmcp=True)

# Generate response from SQL execution and RAG context
execution_context = {
    "sql_results": [{"region": "us-east-1", "cost": 142500.00}],
    "rag_context": "Doc chunk: GPU cluster expansion approved Oct 2026."
}

response: SynthesisResponse = synthesizer.generate(
    user_query="What was our Q4 cloud spend and main drivers?",
    context=execution_context
)

print(f"Synthesis Confidence: {response.confidence_score}")
if response.needs_human_review:
    print("Low confidence response - Routing to HITL Review Dashboard.")
```

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
