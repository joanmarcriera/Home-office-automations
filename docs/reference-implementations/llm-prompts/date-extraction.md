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
- **Relative Date Complexity**: Highly complex relative dates may still confuse smaller models. Frontier models like **GPT-5.5** or **Claude 4.8** have significantly improved reasoning for complex temporal logic.

## When to use it
- When you need to extract dates from unstructured documents where the layout is not consistent.
- When the ingestion pipeline includes a human-in-the-loop (HITL) step to verify the extraction.

## When not to use it
- For documents with a fixed, known layout where simple regex or positional scraping is 100% reliable and cheaper.
- For high-volume, low-latency applications where the cost/time of LLM inference is prohibitive.

## Getting started
1. Set up an OCR engine (e.g., Tesseract or Paperless-ngx) to convert your documents to text.
2. Configure an n8n workflow to receive the OCR text.
3. Use the prompt template provided below in an LLM node (Ollama, OpenAI, or Anthropic).
4. Ensure you inject the current ISO date into the prompt to resolve relative temporal references.

### Prompt Template
```text
You are a precision administrative assistant.
Analyze the provided OCR text from a document and extract any upcoming events or deadlines.

Text:
{{ocr_text}}

Current Date: {{current_date}}

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

## CLI examples
You can test extraction from a text file using the `openai` CLI tool.

```bash
# Extract dates from a text file using GPT-5.5
cat ocr_output.txt | openai api chat.completions.create \
  -m gpt-5.5-preview \
  -g system "You are a precision administrative assistant. Return JSON." \
  -g user
```

## API examples
Integration via Python for automated pipelines using the `openai` library.

```python
import openai

def extract_dates(ocr_text, current_date):
    response = openai.chat.completions.create(
        model="gpt-5.5-preview",
        messages=[
            {"role": "system", "content": "You are a precision administrative assistant."},
            {"role": "user", "content": f"Text: {ocr_text}\nCurrent Date: {current_date}"}
        ],
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content
```

## Related tools / concepts
- [Extraction and Classification](extraction-and-classification.md) — For broader document processing beyond dates.
- [Warranty Extraction](warranty-extraction.md) — Specialized extraction for expiration dates.
- [HITL UI Design](../hitl-ui-design.md) — The recommended interface for verifying these extractions.
- [Document Preparation](../../playbooks/document-preparation-for-llm-training.md) — Best practices for cleaning OCR text.
- [n8n Error Handling](../../knowledge_base/patterns/n8n-error-handling.md) — Managing failed extraction attempts.
- [n8n Service](../../services/n8n.md) — The primary orchestration tool for this prompt.
- [Data Copilot SQL Validation](../../playbooks/data-copilot-sql-validation.md) — Related patterns for validating LLM outputs.
- [MCP](../../tools/automation_orchestration/mcp.md) — Standardized protocol for model-tool interaction.

## Sources / references
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Prompt Library](https://docs.anthropic.com/claude/docs/prompt-library)
- [ISO 8601 Date Standard](https://www.iso.org/iso-8601-date-and-time-format.html)

## Contribution Metadata
- Last reviewed: 2026-06-26
- Confidence: high
