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


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01

## Sources / References
- https://github.com/joanmarcriera/Home-office-automations
