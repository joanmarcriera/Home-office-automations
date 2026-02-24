# Reference Implementation: LLM Prompts for Date Extraction

## Prompt Template
```text
You are a precision administrative assistant.
Analyze the provided OCR text from a document and extract any upcoming events or deadlines.

Text:
{{ocr_text}}

Return ONLY a JSON object with the following fields:
{
  "event_name": "string",
  "start_date": "ISO8601 string",
  "end_date": "ISO8601 string or null",
  "location": "string or null",
  "reasoning": "brief explanation of why these dates were chosen"
}
If no event is found, return {"event_name": null}.
```

## Implementation Notes
- **Context injection**: Always provide the current year and date to the LLM to resolve relative terms like "next Tuesday".
- **Validation**: Pass the result through a JSON validator node in n8n before reaching the calendar tool.
