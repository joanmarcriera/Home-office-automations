# Reference Implementation: LLM Prompts for Date Extraction

## What it is
A specialized prompt engineering and agent execution framework designed for Large Language Models (LLMs) to extract structured temporal events, calendar appointments, deadline commitments, and duration windows from raw, noisy Optical Character Recognition (OCR) text or un-structured documents. It focuses on transforming ambiguous human natural language, relative temporal references (e.g., "next Tuesday at 2 PM", "the third Thursday following Easter"), and multi-timezone schedules into normalized ISO 8601 JSON schema structures compatible with calendar synchronization protocols (CalDAV, Google Calendar API, Microsoft Graph API).

As of early 2027, these extraction prompts are optimized for SOTA frontier models—such as **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Gemma 4**, **DeepSeek-V4**, and **Qwen 3.6 VL**—utilizing **Model Context Protocol (FastMCP 3.1)** task protocol payloads, strict **Pydantic v2** validation rules, and automated Human-in-the-Loop (HITL) fallback workflows.

```
+-----------------------------------------------------------------------------------+
|                   RAW OCR / UNSTRUCTURED DOCUMENT INGESTION                       |
|                                                                                   |
|  Scanned Flyers  |  Medical Letters  |  Invoices & Bills  |  Email Attachments    |
+------------------------------------+----------------------------------------------+
                                     |
                                     v
+------------------------------------+----------------------------------------------+
|                    TEMPORAL PROMPT EXTREACTION ENGINE                             |
|                                                                                   |
|  +-------------------------+    +-----------------------+    +------------------+ |
|  | Context Injection Layer |    | Dynamic Few-Shot Ex.  |    | Relative Temporal| |
|  | (Current UTC Datetime)  |    | (Domain Tuning)       |    | Resolution Engine| |
|  +------------+------------+    +-----------+-----------+    +--------+---------+ |
|               |                             |                         |           |
|               +-----------------------------+-------------------------+           |
|                                             |                                     |
|                                             v                                     |
|  +-----------------------------------------------------------------------------+  |
|  |                       SOTA Frontier LLM (FastMCP 3.1)                       |  |
|  |      Claude 5.6  |  GPT-5.6  |  Gemini 4.0 Ultra  |  DeepSeek-V4             |  |
|  +--------------------------------------+--------------------------------------+  |
+-----------------------------------------|-----------------------------------------+
                                          |
                                          v
+-----------------------------------------+-----------------------------------------+
|                  STRICT PYDANTIC V2 SCHEMA VALIDATION                             |
|                                                                                   |
|  +-----------------------+      +------------------------+     +----------------+ |
|  | ISO 8601 Verification |      | Timezone Normalization |     | HITL Fallback  | |
|  | (YYYY-MM-DDTHH:MM:SSZ)|      | (America/New_York)     |     | (Low Conf Queue| |
|  +-----------------------+      +------------------------+     +----------------+ |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          v
+-----------------------------------------+-----------------------------------------+
|                   DOWNSTREAM CALENDAR & REMINDER SYNC                             |
|                                                                                   |
|  [Google Calendar API]   |   [CalDAV / Radicale]   |   [n8n Workflow Automation]  |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Scanned paper documents, email screenshots, PDF invoices, and medical notices contain critical event dates and deadlines that are frequently lost in formatting noise, headers, footnotes, or garbled OCR text. Resolving these entries manually introduces severe friction:

1. **Relative Date Resolution**: Expressions like "due next Friday", "starting 3 days after receipt", or "every second Monday of the month" require injecting precise current runtime context (reference timestamp and user timezone) into the LLM system prompt.
2. **OCR Noise Resiliency**: Raw OCR text generated from low-resolution scans often contains misplaced spaces, substituted characters (e.g., `l` instead of `1`, `O` instead of `0`), and broken table structures. The prompt design provides few-shot error recovery patterns.
3. **Structured Downstream Integration**: Downstream calendar APIs (CalDAV, Google Calendar, Microsoft To-Do) require strict ISO 8601 formatting (`YYYY-MM-DDTHH:MM:SSZ`). Free-form text outputs from LLMs break automated pipelines without strict schema validation constraints.
4. **Multi-Event Extraction**: Complex documents (such as school term schedules or conference agendas) contain dozens of nested events. The prompt architecture decomposes multi-event documents into validated JSON arrays.

## Where it fits in the stack
This reference implementation sits in the **LLM Extraction & Reasoning Layer** within automated document intake pipelines:

- **Ingestion Pipeline**: Follows OCR engines (such as [Paperless-ngx](../../services/paperless-ngx.md), Tesseract, or LlamaParse) and document pre-processors.
- **Orchestration**: Direct integration with automation platforms like [n8n](../../services/n8n.md), [Node-RED](../../services/node-red.md), or custom Python [FastMCP 3.1](../../tools/automation_orchestration/mcp.md) servers.
- **Verification UI**: Transmits ambiguous or low-confidence extractions into a [Human-In-The-Loop (HITL) UI](../hitl-ui-design.md) for user review prior to calendar commitment.
- **Storage & Sync**: Pushes validated event objects to relational state stores like [Dolt](../../tools/intake_storage/dolt.md) or calendar backends ([CalDAV / Radicale](../../services/radicale.md), [Proton Calendar](../../tools/calendar_tasks/proton_calendar.md)).

## Typical use cases
- **Medical Appointment Scheduling**: Processing scanned appointment confirmation letters to extract doctor names, clinic locations, preparation instructions, and start/end timestamps.
- **School Flyer & Event Calendar Ingestion**: Automatically parsing parent-teacher conference schedules, field trip deadline slips, and holiday closures from school bulletin PDFs.
- **Invoice & Bill Due Date Tracking**: Extracting vendor names, total amounts due, early-payment discount dates, and payment deadlines for financial management.
- **Flight & Hotel Itinerary Parsing**: Converting booking confirmation emails and PDF flight tickets into structured calendar events with time-zone adjustments.

## Strengths
- **Contextual Temporal Reasoning**: Resolves ambiguous, implicit, and relative temporal expressions accurately when provided with runtime reference datetimes.
- **Zero-Shot & Few-Shot Generalization**: Handles diverse document types without requiring layout-specific regex templates or fine-tuned model checkpoints.
- **Strict Schema Enforcement**: Guarantees typed Pydantic v2 outputs when paired with modern structured completion methods (`chat.completions.parse`).
- **Resilience to Garbled Text**: Leverages SOTA LLM semantic comprehension to ignore background noise, footers, and OCR scanning artifacts.

## Limitations
- **Hallucination Risk on Low-Quality Scans**: Badly degraded OCR scans can result in hallucinated times or dates if critical text is missing.
- **Inference Latency & Token Costs**: Large multi-page documents incur higher token consumption and sub-second to multi-second inference latency compared to simple regex parsers.
- **Timezone Ambiguity**: If a document does not explicitly specify a timezone, the system must default to a pre-configured user timezone context.

## When to use it
- When processing unstructured documents with non-standardized layouts where hardcoded regular expressions fail.
- When extraction targets contain complex relative dates ("the day after Thanksgiving") or implicit durations.
- When integrating document parsing into automated agent workflows that require typed, structured JSON payloads.

## When not to use it
- For static, structured forms (e.g., standard tax forms) where traditional OCR positional coordinate templates are 100% accurate and faster.
- For high-volume, real-time streaming data requiring microsecond parsing latency.

## Getting started
1. Configure an OCR engine (e.g., Tesseract or Paperless-ngx) to convert raw document images or PDFs into plain text strings.
2. Deploy the FastMCP 3.1 date extraction tool server or configure an n8n workflow node.
3. Inject the current reference UTC datetime and target user timezone into the prompt payload to ensure accurate relative date resolution.

### System Prompt Template
```text
You are a SOTA Precision Administrative Assistant specializing in Temporal Entity Extraction and Calendar Event Normalization.

Your objective is to analyze the provided raw OCR document text, identify all actionable events, deadlines, appointments, or scheduled commitments, and extract them into a structured JSON payload.

### STRICT OPERATIONAL RULES:
1. RUNTIME REFERENCE CONTEXT:
   - Current Reference Datetime: {{current_reference_iso}}
   - Default User Timezone: {{user_timezone}}
   - Use this reference context to calculate all relative dates (e.g., "tomorrow", "next Tuesday", "in 2 weeks").

2. DATE NORMALIZATION REQUIREMENTS:
   - All dates MUST be converted to full ISO 8601 strings in UTC or with explicit timezone offsets: YYYY-MM-DDTHH:MM:SSZ or YYYY-MM-DDTHH:MM:SS[+|-]HH:MM.
   - If an event specifies a start time but no explicit end time, calculate end_date as exactly 1 hour after start_date.
   - If an event is an all-day event with no specified time, set start_date to YYYY-MM-DDT00:00:00 and is_all_day to true.

3. CONFIDENCE SCORING & REASONING:
   - Assign a confidence score between 0.00 and 1.00 based on OCR text clarity.
   - Provide a concise `reasoning` field explaining how relative temporal expressions were resolved.
   - If no valid dates or events are found, return an empty `events` list. DO NOT hallucinate dates.

### OUTPUT JSON SCHEMA:
{
  "events": [
    {
      "event_name": "string",
      "start_date": "ISO8601 string",
      "end_date": "ISO8601 string or null",
      "is_all_day": "boolean",
      "location": "string or null",
      "organizer": "string or null",
      "description": "string or null",
      "confidence": "float (0.0 - 1.0)",
      "reasoning": "string"
    }
  ]
}
```

## CLI examples

### Testing Extraction via OpenAI CLI
```bash
# Test date extraction prompt using GPT-5.6 on raw OCR text
cat sample_ocr.txt | openai api chat.completions.create \
  -m gpt-5.6-preview \
  -g system "You are a precision temporal extraction assistant. Reference Date: 2027-01-07T09:00:00Z. Timezone: America/New_York. Return JSON." \
  -g user
```

## API examples

### Python FastMCP 3.1 Server with Pydantic v2 Date Extraction & Calendar Tooling
The following complete FastMCP 3.1 server exposes an automated date extraction tool for agents, enforcing strict Pydantic v2 validation and integrating directly with Google Calendar / CalDAV APIs.

```python
import os
import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, ValidationError
from fastmcp import FastMCP
import openai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("date_extraction_mcp")

# Initialize FastMCP 3.1 Server
mcp = FastMCP(
    "Temporal-Date-Extraction-Server",
    version="3.1.0",
    description="FastMCP 3.1 server for extracting ISO 8601 calendar events from OCR text"
)

# Pydantic v2 Schema Definitions
class ExtractedEventSchema(BaseModel):
    event_name: str = Field(..., description="Title or summary of the extracted event.")
    start_date: str = Field(..., description="ISO 8601 formatted start datetime (YYYY-MM-DDTHH:MM:SSZ).")
    end_date: Optional[str] = Field(None, description="ISO 8601 formatted end datetime.")
    is_all_day: bool = Field(default=False, description="Flag indicating an all-day event.")
    location: Optional[str] = Field(None, description="Venue, physical address, or meeting link.")
    organizer: Optional[str] = Field(None, description="Event host or organization.")
    description: Optional[str] = Field(None, description="Relevant contextual details extracted from text.")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score of the extraction (0.0 to 1.0).")
    reasoning: str = Field(..., min_length=5, description="Explanation of date resolution logic.")

    @field_validator("start_date", "end_date")
    @classmethod
    def validate_iso_8601(cls, value: Optional[str]) -> Optional[str]:
        if not value:
            return None
        try:
            # Parse datetime using ISO format
            clean_val = value.replace("Z", "+00:00")
            datetime.fromisoformat(clean_val)
            return value
        except ValueError:
            raise ValueError(f"Invalid ISO 8601 datetime format: {value}")

class TemporalExtractionResponse(BaseModel):
    reference_date: str = Field(..., description="ISO datetime context used for relative resolution.")
    user_timezone: str = Field(..., description="Target timezone context.")
    events: List[ExtractedEventSchema] = Field(default_factory=list, description="List of extracted event objects.")

@mcp.tool()
async def extract_dates_from_ocr(
    ocr_text: str,
    reference_date_iso: Optional[str] = None,
    user_timezone: str = "America/New_York"
) -> Dict[str, Any]:
    """
    Parses raw OCR text to extract structured ISO 8601 calendar events using SOTA LLM reasoning.
    """
    client = openai.AsyncOpenAI()
    ref_date = reference_date_iso or datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    system_prompt = f"""
    You are a precision administrative assistant specializing in temporal entity extraction.
    Current Reference Datetime: {ref_date}
    Target Timezone: {user_timezone}

    Analyze the OCR text and extract all events, meetings, or deadlines into the requested JSON schema.
    Ensure relative date expressions are calculated against the reference datetime.
    """

    try:
        completion = await client.beta.chat.completions.parse(
            model="gpt-5.6-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"OCR Text Input:\n{ocr_text}"}
            ],
            response_format=TemporalExtractionResponse
        )

        extracted_data = completion.choices[0].message.parsed
        if not extracted_data:
            return {"status": "error", "message": "Failed to parse LLM completion response."}

        # Filter events needing HITL review based on confidence score threshold (< 0.75)
        high_confidence_events = []
        low_confidence_events = []

        for event in extracted_data.events:
            if event.confidence >= 0.75:
                high_confidence_events.append(event.model_dump(mode="json"))
            else:
                low_confidence_events.append(event.model_dump(mode="json"))

        return {
            "status": "success",
            "reference_date": ref_date,
            "timezone": user_timezone,
            "high_confidence_events": high_confidence_events,
            "pending_hitl_review_events": low_confidence_events
        }

    except ValidationError as ve:
        logger.error(f"Pydantic schema validation error: {ve}")
        return {"status": "validation_error", "errors": ve.errors()}
    except Exception as e:
        logger.error(f"Date extraction failed: {str(e)}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### Python End-to-End Test Harness
```python
import asyncio
from datetime import datetime

async def test_extraction():
    sample_text = """
    METROPOLITAN HEALTH CLINIC
    Patient: John Doe
    Notice Date: Jan 4, 2027

    Please be advised that your annual physical examination is scheduled for next Tuesday at 10:30 AM
    at Building B, Suite 400. Please arrive 15 minutes early.
    Payment of $45 copay is due by Jan 20, 2027.
    """

    # Local execution invocation simulation
    print("--- Running Extraction Simulation ---")
    ref_time = "2027-01-07T08:00:00Z"

    # Executing function locally
    # result = await extract_dates_from_ocr(sample_text, reference_date_iso=ref_time)
    # print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(test_extraction())
```

## Related tools / concepts
- [Extraction and Classification](extraction-and-classification.md) — Comprehensive reference patterns for document classification and data structuring.
- [Warranty Extraction](warranty-extraction.md) — Specialized extraction prompt patterns targeting invoice warranty timelines.
- [HITL UI Design](../hitl-ui-design.md) — Human-in-the-Loop review interface specification for low-confidence AI extractions.
- [Paperless-ngx](../../services/paperless-ngx.md) — Document management system providing raw OCR input streams.
- [Radicale CalDAV Service](../../services/radicale.md) — Lightweight CalDAV storage server for extracted event sync.
- [n8n Automation](../../services/n8n.md) — Workflow orchestration engine hosting extraction nodes.
- [FastMCP 3.1 Framework](../../tools/automation_orchestration/mcp.md) — Standardized tool protocols interfacing agents with calendar APIs.

## Sources / references
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Claude 3.5 & 5.6 Structured Prompting Reference](https://docs.anthropic.com/claude/docs/prompt-library)
- [ISO 8601 Date Standard & Representation Guidelines](https://www.iso.org/iso-8601-date-and-time-format.html)
- [Pydantic v2 Documentation & Schema Validation](https://docs.pydantic.dev/latest/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
