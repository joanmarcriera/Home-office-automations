# Reference Implementation: LLM Prompt for Warranty Extraction

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

- Last reviewed: 2026-04-09
- Confidence: high

## Sources / References
- [Paperless Tag Taxonomy](../../reference-implementations/paperless/tag-taxonomy.md)
- [Paperless-ngx Documentation](https://docs.paperless-ngx.com/)
