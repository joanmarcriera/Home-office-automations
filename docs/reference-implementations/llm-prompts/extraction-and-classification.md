# Reference Implementation: LLM Prompts for Task Extraction

## Prompt Template
```text
Extract actionable tasks from the following text.

Text:
{{ocr_text}}

Return a list of JSON objects:
[
  {
    "task": "string",
    "due_date": "YYYY-MM-DD or null",
    "priority": "low/medium/high",
    "owner": "string (if mentioned)"
  }
]
```

# Reference Implementation: LLM Prompts for Classification

## Prompt Template
```text
Classify the following document into one of these categories:
[SCHOOL, ADMIN, FINANCE, MEDICAL, TECHNICAL, MISC]

Text:
{{ocr_text}}

Response: One word only.
```

## JSON Schema for Structured Output
To improve reliability with local models (e.g. `Qwen3-Coder-Next`), use **JSON Mode** or **Constrained Output** by providing a formal schema.

### Task Extraction Schema
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "task": { "type": "string" },
      "due_date": { "type": ["string", "null"], "format": "date" },
      "priority": { "enum": ["low", "medium", "high"] },
      "owner": { "type": ["string", "null"] }
    },
    "required": ["task", "due_date", "priority", "owner"]
  }
}
```

### Token-Efficiency Tip
When using local models, prefer a **minimal schema**. Removing the `owner` field or `reasoning` can reduce output tokens by 20-30% in high-volume ingestion workflows.

## Priority Selection Logic
To ensure consistent priority detection with local LLMs, use the following definitions in your system prompt or instruction block:

- **HIGH**:
    - Tasks with a due date of today or tomorrow.
    - Presence of urgency keywords: `urgent`, `asap`, `immediately`, `critical`, `deadline`.
    - Legal, financial, or medical requirements that have immediate consequences (e.g., "pay by", "court date").
- **MEDIUM**:
    - Tasks with a due date within the next 7 days.
    - Routine business or household tasks that are time-sensitive but not immediate (e.g., "schedule appointment", "weekly report").
    - Action items mentioned in meeting summaries without explicit deadlines.
- **LOW**:
    - Tasks with no due date or a date more than 7 days away.
    - "Nice-to-have" items, reading lists, or long-term research goals.
    - General suggestions or ideas (e.g., "maybe we should", "someday").

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01

## Sources / References
- https://github.com/joanmarcriera/Home-office-automations
