# Reference Implementation: LLM Prompts for Date Extraction

## What it is
A specialized prompt template designed for Large Language Models (LLMs) to extract structured event and date information from raw OCR (Optical Character Recognition) text. It focuses on converting unstructured human language into a precise JSON format compatible with calendar APIs.

## What problem it solves
Scanned documents (receipts, school flyers, medical letters) contain critical dates that are often buried in noise. Manual entry is error-prone and tedious. This prompt automates the extraction process, handling relative dates (e.g., "next Tuesday") and implicit context that traditional regex-based scrapers miss.

## Where it fits in the stack
This implementation sits in the **LLM reasoning layer** of the ingestion pipeline. It is typically invoked by [n8n](../../services/n8n.md) after a document has been OCR'd and before the data is passed to the [HITL UI](../hitl-ui-design.md) or a calendar synchronization script.

## Typical use cases
- **Automated Scheduling**: Extracting appointment dates from medical referral letters and adding them to a family calendar.
- **Deadline Tracking**: Identifying due dates on utility bills or tax documents to trigger automated reminders.
- **School Calendar Ingestion**: Processing flyers for school events (plays, holidays, parent-teacher conferences) from a scanned image.

## Strengths
- **Contextual Awareness**: Can resolve relative dates if provided with the "current date" context.
- **Noise Resilience**: Effective at ignoring boilerplate text, headers, and footers common in OCR output.
- **Structured Output**: Guarantees a JSON response for easy downstream processing.

## Limitations
- **Hallucination Risk**: LLMs may occasionally "invent" dates if the OCR text is highly garbled or ambiguous.
- **Token Usage**: Long documents with a lot of irrelevant text can consume significant prompt tokens.
- **Relative Date Complexity**: Highly complex relative dates (e.g., "the third Thursday after the first full moon") may still confuse smaller models.

## When to use it
- When you need to extract dates from unstructured documents where the layout is not consistent.
- When the ingestion pipeline includes a human-in-the-loop (HITL) step to verify the extraction.

## When not to use it
- For documents with a fixed, known layout where simple regex or positional scraping is 100% reliable and cheaper.
- For high-volume, low-latency applications where the cost/time of LLM inference is prohibitive.

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

## Related tools / concepts
- [Extraction and Classification](extraction-and-classification.md) — For broader document processing beyond dates.
- [Warranty Extraction](warranty-extraction.md) — Specialized extraction for expiration dates.
- [HITL UI Design](../hitl-ui-design.md) — The recommended interface for verifying these extractions.
- [Document Preparation](../../playbooks/document-preparation-for-llm-training.md) — Best practices for cleaning OCR text.
- [n8n Error Handling](../../knowledge_base/patterns/n8n-error-handling.md) — Managing failed extraction attempts.
- [n8n Service](../../services/n8n.md) — The primary orchestration tool for this prompt.
- [Data Copilot SQL Validation](../../playbooks/data-copilot-sql-validation.md) — Related patterns for validating LLM outputs.

## Sources / References
- [Home Office Automations](https://github.com/joanmarcriera/Home-office-automations)
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-05-11
