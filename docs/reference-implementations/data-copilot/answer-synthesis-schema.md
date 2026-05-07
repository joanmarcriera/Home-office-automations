# Reference Implementation: Data Copilot Answer Synthesis

## What it is
The Data Copilot Answer Synthesis schema is a standardized JSON structure used to format the final output of an AI data analyst. It ensures that every response includes not just the raw data, but also the underlying reasoning, specific source citations, a confidence score, and recommended next steps.

## What problem it solves
Raw SQL results are often difficult for non-technical users to interpret. Furthermore, LLM-generated answers can lack transparency, making it hard to know where a number came from or how much to trust it. This schema solves the "black box" problem by forcing the model to explicitly state its sources, assumptions, and level of certainty.

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

## Where it fits in the stack
This schema is a core component of the **Reference Implementations** layer. It defines the output contract for the **Orchestration** layer (Data Copilot pipeline) and is designed to be consumed by the **Services** layer (e.g., a Chat UI or Telegram bot). It leverages the **Frameworks** layer (Pydantic) for validation.

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

## When to use it
- In any user-facing AI application where data integrity and auditability are critical.
- When you need to display AI results in a structured UI component (like a card or a table).
- When you want to programmatically monitor the "confidence" of AI answers over time.

## When not to use it
- **Internal Debugging**: Where raw text logs are sufficient for the developer.
- **Low-Stakes Chat**: For general conversational queries that don't involve data retrieval.
- **Highly Fluid Contexts**: Where the response structure needs to change drastically based on the user's personality or mood.

## Sources / References
- [OpenAI: Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## Related tools / concepts
- [Data Copilot Architecture](../../architecture/data-copilot-text-to-sql.md)
- [Data Copilot MCP Tooling](../../knowledge_base/patterns/data-copilot-mcp-tooling.md)
- [Data Copilot Agentic RAG](../../knowledge_base/patterns/data-copilot-agentic-rag.md)
- [Data Copilot SQL Validation](../../playbooks/data-copilot-sql-validation.md)
- [Tool Calling & Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md)
- [LobeHub](../services/lobehub.md) — for building custom agent interfaces

## Sources / References
- [OpenAI: Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## Contribution Metadata
- Last reviewed: 2026-04-30
- Confidence: high
- Related Issues: #190
