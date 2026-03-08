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

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01

## Sources / References
- https://github.com/joanmarcriera/Home-office-automations
