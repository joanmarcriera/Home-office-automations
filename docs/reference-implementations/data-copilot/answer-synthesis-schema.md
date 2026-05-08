# Reference Implementation: Data Copilot Answer Synthesis

## What it is
A Pydantic-based schema and prompt contract for the final stage of a Data Copilot, ensuring that every response includes not just raw data, but also underlying reasoning, specific source citations, confidence scores, and recommended next steps.

## What problem it solves
It prevents "lazy" agent responses (e.g., just returning a JSON array) by forcing the model to provide context, cite its sources, and suggest practical actions.

## Where it fits in the stack
It is the final **Inference Stage** of the pipeline, occurring after data retrieval and before the response is delivered to the user interface.

## Typical use cases
- Generating executive summaries from complex SQL query results.
- Providing natural language explanations for anomalies in time-series data.
- Ensuring consistency across different UI clients (Mobile, Web, Voice) by using a shared JSON contract.

## Strengths
- **Consistency**: Every response follows the same predictable structure.
- **Actionability**: Explicitly requires the model to think about "what's next" for the user.
- **Auditability**: Sources and assumptions are baked into the core schema.

## Limitations
- **Token Usage**: Structured output requires more tokens than raw text.
- **Model Requirement**: Requires a model with strong instruction-following or native structured output support.

## When to use it
- When building user-facing data assistants where trust and clarity are paramount.
- For multi-modal applications where the UI needs to parse specific fields (like `key_metrics`) for visualization.

## When not to use it
- For internal debugging logs where raw data is preferred.
- In latency-critical systems where the overhead of a synthesis LLM call is prohibitive.

## Getting started

To use the schema in your Python pipeline, initialize the Pydantic model with your LLM's JSON output.

```python
import json
from pydantic import ValidationError
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

# 1. Define the schema (see section below for full class definitions)
class DataPoint(BaseModel):
    label: str
    value: Any
    unit: Optional[str] = None

class SynthesisResponse(BaseModel):
    answer_summary: str
    key_metrics: List[DataPoint]
    explanation: str
    confidence_score: float
    recommended_actions: List[str]

# 2. Example raw JSON from LLM
raw_json = """
{
  "answer_summary": "Your electricity spend was £142.50 in March.",
  "key_metrics": [{"label": "Total Spend", "value": 142.5, "unit": "GBP"}],
  "explanation": "Calculated from energy_logs table.",
  "confidence_score": 1.0,
  "recommended_actions": ["Keep saving!"]
}
"""

# 3. Parse and Validate
try:
    data = json.loads(raw_json)
    response = SynthesisResponse(**data)
    print(f"Summary: {response.answer_summary}")
    print(f"Confidence: {response.confidence_score}")
except ValidationError as e:
    print(f"Schema validation failed: {e}")
```

## Goal
Standardize Data Copilot responses to include key metrics, explanations, sources, confidence scores, and recommended actions.

## Answer Synthesis Schema (Pydantic)

```python
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class DataPoint(BaseModel):
    label: str
    value: Any
    unit: Optional[str] = None

class Source(BaseModel):
    type: str = Field(..., description="SQL, Doc, or API")
    id: str = Field(..., description="Unique identifier (e.g., query_hash, file_path)")
    description: str

class SynthesisResponse(BaseModel):
    answer_summary: str = Field(..., description="1-2 sentence human-readable direct answer.")
    key_metrics: List[DataPoint] = Field(..., description="Numerical findings extracted from the data.")
    explanation: str = Field(..., description="The 'Why' behind the data, linking SQL results to RAG context.")
    sources: List[Source] = Field(..., description="Traceability links to SQL queries or Document paths.")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="0.0 (No idea) to 1.0 (Certain). Deducted for ambiguity.")
    assumptions: List[str] = Field(default_factory=list, description="Logical leaps the agent made (e.g., 'Assuming VAT is 20%').")
    recommended_actions: List[str] = Field(default_factory=list, description="Next steps for the user based on the findings.")
    needs_human_review: bool = Field(default=False, description="Set to True if confidence < 0.6 or data is contradictory.")
```

## Prompt Contract for Synthesis Step

When prompting the LLM for the final synthesis, the system prompt must enforce the following contract:

```markdown
### System Instructions
You are a Data Analyst Agent. Your task is to synthesize raw data results into a structured JSON response.

**Core Rules**:
1.  **Direct Answer**: Provide a 1-2 sentence summary first.
2.  **Groundedness**: Do not hallucinate sources. Every claim must have a corresponding entry in the `sources` list.
3.  **Confidence**: Assign a score. Be honest about uncertainty (e.g., if SQL and RAG are contradictory).
4.  **Actionable**: Suggest next steps that are specific and relevant to the findings.
5.  **Flag for Review**: If the confidence score is below 0.6, set `needs_human_review` to `true`.

**Negative Constraints**:
- Do not include raw SQL in the `answer_summary`.
- Do not mention table names or internal IDs to the user.
- Do not make financial advice; state "Consult your policy" if unsure.
```

## Typical use cases
- **Executive Summaries**: Providing a high-level briefing of weekly financial performance with direct links to the relevant transaction logs.
- **Root-Cause Reports**: Explaining *why* a specific metric changed, citing both SQL data points and recent project log entries.
- **Automated Alerts**: Sending a Telegram notification about a power spike that includes the appliance manual's troubleshooting section as a recommended action.
- **Audit Trails**: Maintaining a permanent, structured record of what information the AI provided to the user and which specific database queries were used to generate it.

## Example Outputs

### 1. Lookup Query (High Confidence)
**Query**: "What was my total electricity spend in March?"

```json
{
  "answer_summary": "Your total electricity spend for March 2026 was £142.50.",
  "key_metrics": [
    {"label": "Total Spend", "value": 142.50, "unit": "GBP"},
    {"label": "Usage", "value": 450, "unit": "kWh"}
  ],
  "explanation": "This data was retrieved directly from the 'energy_logs' table. No anomalies were detected for this period.",
  "sources": [
    {"type": "SQL", "id": "q_8823x", "description": "SELECT SUM(cost) FROM energy_logs WHERE month='March'"}
  ],
  "confidence_score": 1.0,
  "assumptions": [],
  "recommended_actions": ["Your spend is 5% lower than February. No action needed."]
}
```

### 2. Diagnosis Query (Medium Confidence)
**Query**: "Why is my energy bill higher than last month?"

```json
{
  "answer_summary": "Your energy bill increased by £35 primarily due to increased HVAC usage and a change in tariff.",
  "key_metrics": [
    {"label": "Bill Increase", "value": 35.0, "unit": "GBP"},
    {"label": "HVAC Runtime", "value": +12, "unit": "hours"}
  ],
  "explanation": "SQL analysis shows a 15% spike in HVAC-linked circuits. RAG analysis of your email logs indicates a tariff update from 'Eco-Saver' to 'Standard' effective March 1.",
  "sources": [
    {"type": "SQL", "id": "q_9912z", "description": "HVAC usage comparison query"},
    {"type": "Doc", "id": "email_archive/tariff_update.md", "description": "Energy provider notification"}
  ],
  "confidence_score": 0.85,
  "assumptions": [
    "Assumes 'Circuit_4' remains exclusively mapped to HVAC."
  ],
  "recommended_actions": [
    "Check for draughts in the living room.",
    "Compare 'Standard' tariff with competitors on CompareTheMarket."
  ]
}
```

## Strengths
- **Transparency**: Every claim is linked to a specific source (SQL row or document snippet).
- **Actionability**: Encourages the model to provide useful next steps rather than just passive information.
- **Machine-Parseable**: The JSON structure allows for easy integration into dashboards or automated downstream workflows.
- **Consistency**: Ensures that all Data Copilot instances across different domains return information in the same predictable format.

## Limitations
- **Token Usage**: Structured JSON outputs require more tokens than plain text responses.
- **Model Intelligence**: Requires a model with strong instruction-following capabilities to ensure the JSON matches the schema perfectly.
- **Schema Rigidity**: May need periodic updates as new types of data sources (e.g., video or audio) are added to the retrieval pipeline.

## Cheap/Free Model Fallback Strategy
Synthesis requires high instruction-following but lower reasoning than SQL generation.
- **Primary**: Claude 3.5 Haiku or GPT-4o-mini (Reliable structured output).
- **Fallback**: Qwen 2.5 7B (Local) with a strict JSON-mode system prompt and Pydantic validation on the output. If the JSON is invalid, the system should retry once with the error message.

## Related tools / concepts
- [Data Copilot Text-to-SQL Architecture](../../architecture/data-copilot-text-to-sql.md)
- [Data Copilot MCP Tooling](../../knowledge_base/patterns/data-copilot-mcp-tooling.md)
- [Data Copilot Agentic RAG](../../knowledge_base/patterns/data-copilot-agentic-rag.md)
- [Data Copilot SQL Validation](../../playbooks/data-copilot-sql-validation.md)
- [Skeleton Guide](skeleton-guide.md)
- [Tool Calling & MCP](../../knowledge_base/patterns/tool-calling-and-mcp.md)
- [LLM Prompts Index](../llm-prompts/index.md)
- [Ragas Evaluation Metrics](../../tools/process_understanding/ragas.md)

## Sources / References
- [OpenAI: Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## Contribution Metadata
- Last reviewed: 2026-06-28
- Confidence: high
- Related Issues: #190
