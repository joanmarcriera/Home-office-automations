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

## Few-Shot Examples (Token-Efficient)
Providing 1-2 examples helps local models understand the expected JSON structure without significantly increasing the token count.

```text
Example 1:
Input: "Your dentist appointment is on March 15th at 2 PM."
Output: {"event_name": "Dentist Appointment", "start_date": "2026-03-15T14:00:00", "end_date": "2026-03-15T15:00:00", "location": null, "reasoning": "Direct mention of date and time."}

Example 2:
Input: "The school play is next Friday evening."
Output: {"event_name": "School Play", "start_date": "2026-03-13T18:00:00", "end_date": null, "location": "School", "reasoning": "Relative date 'next Friday' resolved from current date 2026-03-08."}
```

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01

## Sources / References
- https://github.com/joanmarcriera/Home-office-automations
