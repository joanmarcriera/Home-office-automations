# Reference Implementation: LLM Prompt for Warranty Extraction

## What it is
A specialized prompt design and JSON schema for extracting structured warranty metadata from unstructured text (OCR output). It converts raw receipt data into actionable lifecycle information like expiration dates and coverage terms.

As of early January 2027, these prompts are optimized for SOTA frontier models such as **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, and **Qwen 3.6 VL** utilizing **Model Context Protocol (MCP) 3.1** and **FastMCP 3.1** Task Protocol payloads for strict schema validation.

## What problem it solves
Manual tracking of warranties is prone to failure; receipts are lost, and expiration dates are forgotten. This implementation automates the extraction of key terms, enabling a system to send proactive alerts before a warranty expires, potentially saving significant costs on repairs or replacements.

## Where it fits in the stack
This implementation operates within the **Data Extraction/Intelligence layer** of a document management pipeline. It typically follows an **OCR stage** (e.g., Tesseract, Paperless-ngx) and precedes a **Storage/Alerting stage** (e.g., Vikunja, Google Calendar, or a dedicated database).

## Typical use cases
- **Post-Purchase Automation**: Scanning a receipt immediately after a purchase to log the warranty.
- **Legacy Digitalization**: Processing a folder of "Warranty" PDFs to build a master tracking spreadsheet.
- **Insurance Audits**: Providing a structured list of covered household items and their protection status.

## Strengths
- **High Precision**: Focused extraction rules minimize "hallucination" of dates, especially when using SOTA frontier models like **GPT-5.6**, **Claude 5.6**, **Gemini 4.0 Ultra**, or **DeepSeek-V4**.
- **Standardized Schema**: Outputs are ready for consumption by databases and calendar APIs.
- **Calculation Logic**: Moves the burden of date math (e.g., "12 months from today") from the user to the LLM.

## Limitations
- **OCR Quality**: If the initial scan is poor, the LLM may misread dates or product names.
- **Complex Terms**: May struggle with highly technical "Limited Lifetime" vs "Full" warranty nuances without additional context. Local models like **Llama 4**, **Gemma 4**, or **Qwen 3.6 VL** are improving but may still require specific few-shot examples for these edge cases.

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
3. Use the **Anthropic Claude 5.6**, **OpenAI GPT-5.6**, or **Gemini 4.0 Ultra** API to process the OCR text using the prompt template below.
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
# Test warranty extraction with Claude 5.6
cat receipt_ocr.txt | anthropic messages create \
  --model claude-5-6-sonnet-20270105 \
  --system "You are an expert document analyzer. Output JSON only." \
  --user
```

## API examples
Example of structured output enforcement using the OpenAI Python library, integrating Pydantic v2 schemas and the custom Vikunja task creation tool.

```python
import asyncio
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import Optional
import openai
from scripts.vikunja_tool import VikunjaCreateTool

# Strict Pydantic v2 Warranty Details Schema
class WarrantyDetails(BaseModel):
    product_name: str = Field(..., min_length=2, description="The name of the purchased product.")
    manufacturer: str = Field(..., min_length=2, description="The brand or manufacturer name.")
    purchase_date: str = Field(..., description="Purchase date formatted as YYYY-MM-DD.")
    warranty_duration_months: int = Field(..., gt=0, description="Duration of warranty coverage in months.")
    expiration_date: str = Field(..., description="Calculated expiration date formatted as YYYY-MM-DD.")
    is_extended_warranty: bool = Field(default=False, description="Whether this is an extended warranty policy.")
    notes: Optional[str] = Field(None, description="Any specific coverage exclusions or details.")

    @field_validator('purchase_date', 'expiration_date')
    @classmethod
    def validate_date_string(cls, value: str) -> str:
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            raise ValueError("Dates must be formatted strictly as YYYY-MM-DD")

async def extract_and_schedule_warranty(ocr_text: str):
    client = openai.AsyncOpenAI()

    try:
        # Perform structured metadata extraction using SOTA LLM (such as GPT-5.6)
        completion = await client.beta.chat.completions.parse(
            model="gpt-5.6",
            messages=[
                {"role": "system", "content": "You are a professional metadata extraction agent specializing in warranty receipts."},
                {"role": "user", "content": ocr_text}
            ],
            response_format=WarrantyDetails
        )

        warranty = completion.choices[0].message.parsed
        if warranty and warranty.expiration_date:
            # Create a reminder in Vikunja project 5 (e.g., 'Home Admin')
            # Set due date 30 days before expiration
            from datetime import timedelta
            exp_dt = datetime.strptime(warranty.expiration_date, "%Y-%m-%d")
            reminder_dt = exp_dt - timedelta(days=30)
            due_date_str = reminder_dt.strftime("%Y-%m-%dT12:00:00Z")

            # Instantiate Vikunja tool
            vikunja = VikunjaCreateTool()
            result = await vikunja.run(
                title=f"Warranty Expiry: {warranty.manufacturer} {warranty.product_name}",
                project_id=5,
                description=f"Original Purchase: {warranty.purchase_date}\nDuration: {warranty.warranty_duration_months} months.\nNotes: {warranty.notes}",
                due_date=due_date_str,
                priority=3
            )
            print(result)
        else:
            print("No valid warranty expiration details found in OCR.")
    except ValidationError as e:
        print(f"Strict warranty metadata schema validation failed: {e}")
    except Exception as e:
        print(f"Extraction failed: {str(e)}")

if __name__ == "__main__":
    ocr_sample = "SAMSUNG Fridge RF27T purchased on 2027-01-06. Includes 12 months manufacturer warranty."
    asyncio.run(extract_and_schedule_warranty(ocr_sample))
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
- [Paperless-ngx API Documentation](https://docs.paperless-ngx.com/api/)
- [OpenAI Structured Outputs Guide](https://platform.openai.com/docs/guides/structured-outputs)
- [Anthropic JSON Mode](https://docs.anthropic.com/claude/docs/test-and-evaluate-prompts#json-mode)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
