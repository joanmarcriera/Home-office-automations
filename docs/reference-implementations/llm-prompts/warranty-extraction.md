# Reference Implementation: LLM Prompt for Warranty Extraction

## What it is
A specialized prompt design and JSON schema for extracting structured warranty metadata from unstructured text (OCR output). It converts raw receipt data into actionable lifecycle information like expiration dates and coverage terms.

## What problem it solves
Manual tracking of warranties is prone to failure; receipts are lost, and expiration dates are forgotten. This implementation automates the extraction of key terms, enabling a system to send proactive alerts before a warranty expires, potentially saving significant costs on repairs or replacements.

## Where it fits in the stack
This implementation operates within the **Data Extraction/Intelligence layer** of a document management pipeline. It typically follows an **OCR stage** (e.g., Tesseract, Paperless-ngx) and precedes a **Storage/Alerting stage** (e.g., Vikunja, Google Calendar, or a dedicated database).

## Typical use cases
- **Post-Purchase Automation**: Scanning a receipt immediately after a purchase to log the warranty.
- **Legacy Digitalization**: Processing a folder of "Warranty" PDFs to build a master tracking spreadsheet.
- **Insurance Audits**: Providing a structured list of covered household items and their protection status.

## Strengths
- **High Precision**: Focused extraction rules minimize "hallucination" of dates.
- **Standardized Schema**: Outputs are ready for consumption by databases and calendar APIs.
- **Calculation Logic**: Moves the burden of date math (e.g., "12 months from today") from the user to the LLM.

## Limitations
- **OCR Quality**: If the initial scan is poor, the LLM may misread dates or product names.
- **Complex Terms**: May struggle with highly technical "Limited Lifetime" vs "Full" warranty nuances without additional context.

## When to use it
- When integrating document management (Paperless-ngx) with task management (Vikunja).
- When building a "Household Inventory" agent.
- For high-value purchases (electronics, appliances, vehicles).

## When not to use it
- For low-value items where the cost of LLM processing exceeds the benefit of tracking.
- If the document is already in a structured digital format (e.g., an invoice JSON).

## Purpose
Extract warranty-specific metadata from scanned receipts or warranty cards to ensure automated tracking of coverage periods and easier troubleshooting.

## Prompt Template
```text
You are an expert at analyzing household documents. Extract warranty information from the following text.

Text:
{{ocr_text}}

### Extraction Rules:
1. **Purchase Date**: Use the date of the receipt. If missing, use current date.
2. **Warranty Duration**: Look for phrases like "1 year warranty", "12 months", "Limited lifetime", etc.
3. **Manufacturer**: Identify the brand (e.g., Samsung, Dell, Bosch).
4. **Product Name**: Identify the specific model or product name.
5. **Expiration Date**: Calculate the expiration date based on the Purchase Date and Duration. Format: YYYY-MM-DD.

Return a JSON object:
{
  "product_name": "string",
  "manufacturer": "string",
  "purchase_date": "YYYY-MM-DD",
  "warranty_duration_months": integer,
  "expiration_date": "YYYY-MM-DD",
  "is_extended_warranty": boolean,
  "notes": "string (e.g., coverage details)"
}
```

## JSON Schema for Constrained Output
```json
{
  "type": "object",
  "properties": {
    "product_name": { "type": "string" },
    "manufacturer": { "type": "string" },
    "purchase_date": { "type": "string", "format": "date" },
    "warranty_duration_months": { "type": "integer" },
    "expiration_date": { "type": "string", "format": "date" },
    "is_extended_warranty": { "type": "boolean" },
    "notes": { "type": "string" }
  },
  "required": ["product_name", "manufacturer", "purchase_date", "expiration_date"]
}
```

## n8n Workflow Integration Pattern
1. **Trigger**: Paperless-ngx Webhook (Document Added with tag `Admin/Warranty`).
2. **OCR Pull**: Fetch the full OCR text from the Paperless API.
3. **LLM Node**: Use the prompt above with `ollama` or `openai`.
4. **Logic**:
    - If `expiration_date` is found, calculate reminder date (e.g., `expiration_date - 30 days`).
5. **Target**: Create a task in **Vikunja** or an event in **Google Calendar** titled "Warranty Expiring: [Product Name]".
6. **Tagging**: Update the Paperless document metadata with the extracted product and manufacturer.

## Related tools / concepts
- [Paperless-ngx](../../services/paperless-ngx.md): The document source and OCR engine.
- [Tag Taxonomy](../../reference-implementations/paperless/tag-taxonomy.md): Organizing documents for extraction.
- [Vikunja](../../tools/calendar_tasks/vikunja.md): Destination for warranty reminders.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md): Using extracted metadata to enhance document retrieval.
- [n8n](../../services/n8n.md): Orchestrating the extraction and alerting workflow.
- [Metadata Schemas](../../reference-implementations/metadata-schemas/manuals.md): Related schemas for household documents.
- [Scan-to-Task Playbook](../../playbooks/scan-to-task.md): End-to-end guide for this workflow.

## Sources / References
- [Paperless-ngx Documentation](https://docs.paperless-ngx.com/)
- [OpenAI Structured Outputs Guide](https://platform.openai.com/docs/guides/structured-outputs)

- Last reviewed: 2026-05-11
- Confidence: high
