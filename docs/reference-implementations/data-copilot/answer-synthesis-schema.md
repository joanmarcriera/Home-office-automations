# Reference Implementation: Data Copilot Answer Synthesis

This document defines the standardized output schema for the final step of the Data Copilot pipeline. By enforcing a machine-parseable yet human-readable structure, we ensure that the Copilot provides more than just raw numbers—it provides reasoning, context, and actionable next steps.

## What it is
A standardized JSON schema and prompt contract for the "Final Synthesis" stage of an AI data analysis pipeline.

## What problem it solves
Raw data from a database is often difficult for users to interpret without context. Standardized synthesis ensures that every answer includes not just the "what" (the number), but also the "why" (the reasoning), the "how" (the source), and the "now what" (the recommended action). It prevents "naked numbers" and builds trust through transparency.

## Where it fits in the stack
**Category**: Reference Implementation. It sits at the **Output and Interaction layer** of the Data Copilot architecture, serving as the final contract between the AI and the end-user interface.

## Typical use cases
- Presenting financial reports where numbers must be accompanied by year-over-year context.
- Diagnosing hardware failures based on sensor logs and maintenance manuals.
- Answering complex "Why" questions (e.g., "Why did my sales drop in Q3?") with structured multi-source evidence.

## Strengths
- **Consistency**: Ensures a uniform user experience across different types of queries.
- **Trust**: Explicitly lists sources and assumptions, allowing users to verify the AI's logic.
- **Actionability**: Forces the model to suggest next steps, moving beyond passive reporting.
- **Machine Readable**: Allows the frontend to render custom widgets (e.g., trend lines, source badges) based on the JSON keys.

## Limitations
- **Token Usage**: Generating structured reasoning and actions consumes more output tokens than a simple text response.
- **Model Quality**: Small models may struggle to populate all fields correctly while maintaining high-quality reasoning.

## When to use it
- In any Data Copilot or "Chat with your Data" application where accuracy and trust are paramount.
- When the output needs to be consumed by other systems or automated workflows.

## When not to use it
- For extremely simple "lookup" tools (e.g., "What is the current time?") where the overhead of a full synthesis schema is unnecessary.
- In latency-critical applications where a stream-of-consciousness text response is preferred over a structured JSON block.

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

## Cheap/Free Model Fallback Strategy
Synthesis requires high instruction-following but lower reasoning than SQL generation.
- **Primary**: Claude 3.5 Haiku or GPT-4o-mini (Reliable structured output).
- **Fallback**: Qwen 2.5 7B (Local) with a strict JSON-mode system prompt and Pydantic validation on the output. If the JSON is invalid, the system should retry once with the error message.

## Related tools / concepts
- [Data Copilot Architecture](../../architecture/data-copilot-text-to-sql.md)
- [Data Copilot MCP Tooling](../../knowledge_base/patterns/data-copilot-mcp-tooling.md)
- [Data Copilot Agentic RAG](../../knowledge_base/patterns/data-copilot-agentic-rag.md)
- [Data Copilot SQL Validation](../../playbooks/data-copilot-sql-validation.md)
- [n8n Automation](../../services/n8n.md)

## Contribution Metadata
- Last reviewed: 2026-05-06
- Confidence: high
- Related Issues: #190
