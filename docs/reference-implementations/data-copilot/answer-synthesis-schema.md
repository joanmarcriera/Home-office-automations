# Reference Implementation: Data Copilot Answer Synthesis

This document defines the standardized output schema for the final step of the Data Copilot pipeline. By enforcing a machine-parseable yet human-readable structure, we ensure that the Copilot provides more than just raw numbers—it provides reasoning, context, and actionable next steps.

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
    answer_summary: str = Field(..., description="Human-readable concise answer")
    key_metrics: List[DataPoint]
    explanation: str = Field(..., description="Detailed reasoning and context")
    sources: List[Source]
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    assumptions: List[str] = Field(default_factory=list)
    recommended_actions: List[str] = Field(default_factory=list)
```

## Prompt Contract for Synthesis Step

When prompting the LLM for the final synthesis, the system prompt must enforce the following contract:

```markdown
### System Instructions
You are a Data Analyst Agent. Your task is to synthesize raw data results into a structured JSON response.

1.  **Summary**: Provide a 1-2 sentence direct answer.
2.  **Metrics**: Extract the most relevant numerical findings.
3.  **Context**: Explain *why* the data looks this way based on provided RAG context.
4.  **Confidence**: Assign a score (0.0 to 1.0). Deduct points for missing sources or ambiguous joins.
5.  **Actions**: Suggest what the user should do next based on the data (e.g., "Review your electricity usage during peak hours").
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

## Sources / References
- [OpenAI: Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## Related tools / concepts
- [Data Copilot Architecture](../../architecture/data-copilot-text-to-sql.md)
- [Data Copilot MCP Tooling](../../knowledge_base/patterns/data-copilot-mcp-tooling.md)
- [Data Copilot Agentic RAG](../../knowledge_base/patterns/data-copilot-agentic-rag.md)
- [Data Copilot SQL Validation](../../playbooks/data-copilot-sql-validation.md)

## Contribution Metadata
- Last reviewed: 2026-04-26
- Confidence: high
- Related Issues: #190
