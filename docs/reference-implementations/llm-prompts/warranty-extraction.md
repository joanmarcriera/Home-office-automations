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
- **High Precision**: Focused extraction rules minimize "hallucination" of dates, especially when using frontier models like **GPT-5.5**, **Claude 5.1**, **Llama 4**, **Gemma 3**, **Qwen 3.6**, or **Gemini 3.5 series**.
- **Standardized Schema**: Outputs are ready for consumption by databases and calendar APIs.
- **Calculation Logic**: Moves the burden of date math (e.g., "12 months from today") from the user to the LLM.

## Limitations
- **OCR Quality**: If the initial scan is poor, the LLM may misread dates or product names.
- **Complex Terms**: May struggle with highly technical "Limited Lifetime" vs "Full" warranty nuances without additional context. Local models like **Llama 4** are improving but may still require specific few-shot examples for these edge cases.

## When to use it
- When integrating document management (Paperless-ngx) with task management (Vikunja).
- When building a "Household Inventory" agent.
- For high-value purchases (electronics, appliances, vehicles).

## When not to use it
- For low-value items where the cost of LLM processing exceeds the benefit of tracking.
- If the document is already in a structured digital format (e.g., an invoice JSON).

## Getting started
1. Enable OCR in Paperless-ngx or your chosen ingestion tool.
2. Configure a webhook or n8n workflow to trigger when a document is tagged as `Warranty`.
3. Use the **Anthropic Claude 5.1** or **OpenAI GPT-5.5** API to process the OCR text using the prompt template below.
4. Parse the JSON output and create a task in Vikunja with a due date 30 days before the warranty expiration.

### Prompt Template
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

## CLI examples
Test the extraction logic using the `anthropic` CLI.

```bash
# Test warranty extraction with Claude 5.1
cat receipt_ocr.txt | anthropic messages create \
  --model claude-5-1-sonnet-20260715 \
  --system "You are an expert document analyzer. Output JSON only." \
  --user
```

## API examples
Example of structured output enforcement using the OpenAI Python library, utilizing Pydantic v2 schemas and modern async context handling.

```python
import asyncio
import logging
from typing import Optional
from pydantic import BaseModel, Field
import openai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WarrantyExtractor")

class WarrantySchema(BaseModel):
    product_name: str = Field(..., description="The model or exact product name")
    manufacturer: str = Field(..., description="Brand name / manufacturer")
    purchase_date: str = Field(..., description="Purchase date in YYYY-MM-DD format")
    warranty_duration_months: int = Field(..., description="Duration of warranty in months")
    expiration_date: str = Field(..., description="Calculated expiration date in YYYY-MM-DD format")
    is_extended_warranty: bool = Field(default=False)
    notes: Optional[str] = Field(None, description="Additional coverage info, limited lifetime exceptions etc.")

async def get_warranty_info(ocr_text: str) -> Optional[str]:
    """
    Uses GPT-5.5 under MCP 3.1 schemas to precisely parse receipt text into structured warranty schemas.
    """
    try:
        client = openai.AsyncOpenAI()

        response = await client.beta.chat.completions.parse(
            model="gpt-5.5-preview",
            messages=[
                {"role": "system", "content": "You are a precise invoice/receipt data extractor. Extract warranty info in structured JSON format."},
                {"role": "user", "content": ocr_text}
            ],
            response_format=WarrantySchema,
            timeout=15.0
        )

        warranty_data = response.choices[0].message.parsed
        if warranty_data:
            logger.info(f"Successfully extracted warranty for product: {warranty_data.product_name}")
            return warranty_data.model_dump_json(indent=2)
        return None
    except Exception as e:
        logger.error(f"Failed to extract warranty info: {e}")
        return None

if __name__ == "__main__":
    ocr_sample = "Store receipt: Purchased Samsung TV QN90D on 2026-08-30. Includes 24 months manufacturer warranty."
    asyncio.run(get_warranty_info(ocr_sample))
```

## Related tools / concepts
- [Paperless-ngx](../../services/paperless-ngx.md): The document source and OCR engine.
- [Tag Taxonomy](../../reference-implementations/paperless/tag-taxonomy.md): Organizing documents for extraction.
- [Vikunja](../../services/vikunja.md): Destination for warranty reminders.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md): Using extracted metadata to enhance document retrieval.
- [n8n](../../services/n8n.md): Orchestrating the extraction and alerting workflow.
- [Metadata Schemas](../../reference-implementations/metadata-schemas/manuals.md): Related schemas for household documents.
- [Scan-to-Task Playbook](../../playbooks/scan-to-task.md): End-to-end guide for this workflow.
- [MCP](../../tools/automation_orchestration/mcp.md) — Standardized protocol for model-tool interaction.

## Sources / references
- [Paperless-ngx API Reference](https://docs.paperless-ngx.com/api/)
- [OpenAI Structured Validation Guides](https://platform.openai.com/docs/guides/structured-outputs)
- [Anthropic JSON Constraints and Steering](https://docs.anthropic.com/en/docs/test-and-evaluate-prompts)

## Contribution Metadata
- Last reviewed: 2026-08-31
- Confidence: high
