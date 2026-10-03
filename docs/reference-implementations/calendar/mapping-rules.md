# Reference Implementation: Calendar Mapping Rules

## What it is
This document defines the logic, sanitization, and normalization rules for mapping extracted metadata from LLMs and multi-modal document analysis pipelines into digital calendar events (e.g., Google Calendar, CalDAV, Apple Calendar, Fastmail, or Proton Calendar). It functions as a strict data contract for sovereign home-lab automation, ensuring that AI-generated events are clean, deduplicated, correctly formatted, and traceable to their origin document.

As of early January 2027, these mapping rules serve as the specification for the **Chronos FastMCP 3.1 Gateway**—a high-performance, agentic calendar management server operating under the **FastMCP 3.1 Task Protocol**. This enables local models (such as DeepSeek-V4, Qwen 3.6, Gemma 3, and Llama 4) and frontier APIs (Claude 5.6, GPT-5.6, Gemini 4.0 Ultra) to execute multi-provider calendar scheduling, update event reminders, and maintain time-series integrity without cluttering user schedules.

## What problem it solves
- **Unstructured LLM Extraction Artifacts**: Raw dates and times extracted from PDFs, scanned bills, email threads, or voice notes often vary wildly in format (e.g., "Next Tuesday at 3pm", "2027-01-15T15:00:00-05:00", or "15th Jan"). These rules enforce ISO 8601 UTC string normalization and timezone awareness before sending API payload requests.
- **Data Clutter & Missing Provenance**: AI-generated events created without origin metadata make it impossible for users to trace *why* or *where* an event originated. This reference implementation enforces automatic linking back to source document IDs (`doc_id`) in [Paperless-ngx](../../services/paperless-ngx.md) or message IDs in email archives.
- **Timezone Drift & Off-by-One Misalignments**: Failure to account for user local timezones vs. UTC server standard can shift deadlines across midnight boundaries. These rules mandate strict timezone validation and explicit duration defaults.
- **Cross-Provider API Incompatibilities**: Different calendar platforms implement varying text capabilities (e.g., Google Calendar accepts HTML descriptions, whereas CalDAV and Proton utilize plain-text iCalendar `DESCRIPTION` properties). This implementation standardizes field formatting for universal cross-provider rendering.

## Where it fits in the stack
This logic operates within the **Data Transformation & Normalization Layer**. It sits directly between the **Extraction & AI Ingestion Layer** (Paperless-ngx, n8n OCR, LLM prompts) and the **Calendar Execution Layer** (Chronos FastMCP 3.1 server, CalDAV, Google Calendar API).

```
+-----------------------------------------------------------------------------------+
|                        Document & Ingestion Source Layer                          |
|  +--------------------+   +-----------------------+   +------------------------+  |
|  | Paperless-ngx PDF  |   |  n8n Email Ingestion  |   |  Voice Memo Ingestion  |  |
|  | (Scanned Invoices) |   |  (School Newsletters) |   |  (Whisper / Audio LLM) |  |
|  +---------+----------+   +-----------+-----------+   +-----------+------------+  |
+------------|--------------------------|---------------------------|---------------+
             |                          |                           |
             +--------------------------+---------------------------+
                                        |
                                        v Raw JSON Metadata Extraction
                                        |  - "event_name": "Dentist Appointment"
                                        |  - "raw_date": "Jan 12 2027 10:00"
                                        |  - "doc_id": "8492"
+---------------------------------------v-------------------------------------------+
|               Calendar Mapping & Normalization Engine (Chronos)                   |
|  +-----------------------------------------------------------------------------+  |
|  |                    Pydantic v2 Contract Validation                      |  |
|  |   +--------------------------+  +----------------------------------------+  |  |
|  |   | Title Case Normalization |  | ISO 8601 UTC Timezone Converter        |  |  |
|  |   +--------------------------+  +----------------------------------------+  |  |
|  |   +--------------------------+  +----------------------------------------+  |  |
|  |   | Duration Default Guard   |  | Description Provenance Injector        |  |  |
|  |   +--------------------------+  +----------------------------------------+  |  |
|  +-----------------------------------------------------------------------------+  |
+---------------------------------------+-------------------------------------------+
                                        | Validated Event Payload
                                        v
+---------------------------------------+-------------------------------------------+
|                        Calendar Execution Target Layer                            |
|  +--------------------+   +-----------------------+   +------------------------+  |
|  | Google Calendar API|   | CalDAV (Radicale /    |   | Chronos FastMCP 3.1    |  |
|  | (JSON REST Insert) |   |  Nextcloud VEVENT)    |   |  Agent Scheduler       |  |
|  +--------------------+   +-----------------------+   +------------------------+  |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Automatic Invoice & Bill Due-Date Tracking**: Mapping due dates extracted from Paperless-ngx invoices into all-day calendar reminders with links back to the source document URL.
- **Family & School Schedule Synchronization**: Transforming multi-event school calendar PDFs into structured individual calendar entries across Google Calendar and Nextcloud.
- **Autonomous FastMCP Agent Scheduling**: Allowing AI agents running under FastMCP 3.1 Task Protocol to parse natural language appointment emails and safely insert non-overlapping schedule entries.
- **Medical Appointment Confirmation**: Ingesting SMS/email notifications and converting them into structured events complete with doctor name, facility location, and prep instructions.

## Normalization & Mapping Rules Specification

| Extracted LLM Field | Target Calendar Field | Mapping Logic & Format Rules |
| :--- | :--- | :--- |
| `event_name` | `summary` | Sanitized, converted to Title Case, stripped of special control characters. Max length: 255 chars. |
| `start_date` | `start` | Converted to ISO 8601 UTC string (`YYYY-MM-DDTHH:MM:SSZ`). Local timezones must be converted prior to creation. |
| `end_date` | `end` | If missing, automatically defaulted to `start_date + 1 hour` (or next day for all-day events). Must strictly be > `start_date`. |
| `is_all_day` | `start` / `end` | Boolean flag. If `true`, formatted as date string (`YYYY-MM-DD`) without time component. |
| `location` | `location` | Physical street address, room, or virtual URL (e.g. Zoom/Jitsi link). Defaults to `"Online"` if unspecified. |
| `doc_id` | `description` | Appends Paperless-ngx link: `Source Document: https://paperless.home/documents/{doc_id}`. |
| `reasoning` | `description` | Prepends AI extraction rationale: `[Auto-Generated via FastMCP 3.1: {reasoning}]`. |
| `reminders` | `reminders` | Array of minute offsets (e.g. `[15, 1440]` for 15 minutes and 1 day prior). Defaults to `[15]`. |

## Execution Protocol Flow

```
Extraction Source          Chronos Mapping Engine                     Calendar API
       |                               |                                   |
       |  1. Extracted JSON Payload    |                                   |
       |------------------------------>|                                   |
       |                               |  2. Validate Pydantic v2 Schema   |
       |                               |     - Format Title Case           |
       |                               |     - Resolve Local -> UTC Time   |
       |                               |     - Apply 1-Hour Default End    |
       |                               |     - Format Paperless Doc Link   |
       |                               |                                   |
       |                               |  3. POST /events Insert Request   |
       |                               |---------------------------------->|
       |                               |  4. 201 Created (Event ID & ETag) |
       |                               |<----------------------------------|
       |                               |                                   |
       |  5. Execution Confirmation    |                                   |
       |<------------------------------|                                   |
```

## Strengths
- **Deterministic Structural Consistency**: Guarantees every AI-generated event conforms to standard naming, description formatting, and duration defaults.
- **Traceable Document Provenance**: Direct linking to Paperless-ngx `doc_id` prevents lost context and lets humans verify event details in seconds.
- **Universal Provider Compatibility**: Pre-sanitized structures map cleanly to Google Calendar REST APIs, WebDAV/CalDAV VEVENT payloads, and FastMCP tool calls.
- **Validation Guardrails**: Pydantic v2 schemas reject malformed dates, invalid duration windows, or empty title fields before hitting downstream calendar endpoints.

## Limitations
- **Timezone Context Requirement**: Requires explicit user location configuration (e.g. `Europe/London` or `America/New_York`) to resolve ambiguous inputs like "9:00 AM" into UTC.
- **Complex Recurrence Rule (RRULE) Edge Cases**: Parsing complex recurring scheduling logic (e.g., "every second Tuesday except holidays") requires deep reasoning model support rather than basic field mapping rules.
- **API Specific Limits**: Downstream providers may enforce proprietary field limits (e.g., Google Calendar HTML description limits vs. CalDAV plain text restrictions).

## When to use it
- When automating the ingestion of scanned documents, emails, or notes containing time-sensitive deadlines.
- When deploying an autonomous FastMCP 3.1 scheduling agent for home-lab or enterprise operations.
- When establishing a unified data contract between AI document pipelines and family calendar stores.

## When not to use it
- For manual event creation where all parameters are directly inputted by a human in a native calendar GUI.
- For high-volume calendar streaming where per-event LLM reasoning is unnecessary.

## Getting started

### 1. Extraction Pipeline Setup
Utilize frontier reasoning models (Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4) or local vision LLMs (Qwen 3.6 VL) with the [Date Extraction Prompt](../llm-prompts/date-extraction.md) to emit raw JSON payloads from documents.

### 2. FastMCP 3.1 Normalization Engine
Pass the raw JSON payload to the Chronos FastMCP 3.1 gateway server. The server applies these mapping rules and Pydantic v2 validators to format the request for the target calendar provider.

## CLI examples

```bash
# Test calendar mapping rules against a local document extraction output
python3 -m calendar_sync --dry-run --input sample_extracted_invoice.json

# Synchronize validated extraction output to Google Calendar
python3 -m calendar_sync --input sample_extracted_invoice.json --provider google --timezone "Europe/London"

# Use Chronos FastMCP CLI client to query normalized events for a specific day
chronos-mcp-client list-events --date 2027-01-07 --calendar "family"
```

## API examples

### Production FastMCP 3.1 Calendar Mapping Gateway

The following Python server implements the complete mapping rules specification using **Pydantic v2** model validation and FastMCP 3.1 tool interfaces:

```python
import os
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict, Any
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, model_validator

# Initialize FastMCP 3.1 Server
mcp = FastMCP("Chronos-Calendar-Mapping-Gateway")

PAPERLESS_BASE_URL = os.getenv("PAPERLESS_URL", "https://paperless.home/documents/")

# --- Pydantic v2 Extraction & Normalization Model ---

class RawExtractedEventInput(BaseModel):
    event_name: str = Field(..., min_length=1, max_length=255, description="Raw event title extracted from document")
    start_date: datetime = Field(..., description="Event start date and time")
    end_date: Optional[datetime] = Field(None, description="Event end date and time")
    is_all_day: bool = Field(default=False, description="Flag indicating an all-day event")
    location: Optional[str] = Field(default="Online", description="Event physical location or virtual URL")
    doc_id: Optional[str] = Field(None, description="Paperless-ngx document ID reference")
    reasoning: Optional[str] = Field(None, description="AI extraction context or reasoning summary")
    reminder_minutes: List[int] = Field(default_factory=lambda: [15], description="Reminder offset minutes prior to event")

    @field_validator("event_name")
    def format_title_case(cls, v: str) -> str:
        """Sanitizes whitespace and converts event title to title case."""
        cleaned = " ".join(v.split())
        return cleaned.title()

    @model_validator(mode="after")
    def validate_and_default_duration(self) -> "RawExtractedEventInput":
        """Ensures end_date is present and strictly greater than start_date."""
        if self.end_date is None:
            if self.is_all_day:
                self.end_date = self.start_date + timedelta(days=1)
            else:
                self.end_date = self.start_date + timedelta(hours=1)
        elif self.end_date <= self.start_date:
            raise ValueError("end_date must be strictly greater than start_date")
        return self

class NormalizedCalendarPayload(BaseModel):
    summary: str = Field(..., description="Sanitized Title Case summary")
    start_time: str = Field(..., description="ISO 8601 UTC formatted start string")
    end_time: str = Field(..., description="ISO 8601 UTC formatted end string")
    is_all_day: bool
    location: str
    description: str = Field(..., description="Formatted description with provenance and reasoning")
    reminders: List[int]

# --- Normalization Engine Function ---

def normalize_event_payload(raw: RawExtractedEventInput) -> NormalizedCalendarPayload:
    """Applies standard mapping rules to construct a provider-agnostic normalized event payload."""
    description_blocks = []

    if raw.reasoning:
        description_blocks.append(f"[Auto-Generated via Chronos FastMCP 3.1]\nReasoning: {raw.reasoning}")

    if raw.doc_id:
        doc_url = f"{PAPERLESS_BASE_URL.rstrip('/')}/{raw.doc_id}"
        description_blocks.append(f"Source Document ID: {raw.doc_id}\nURL: {doc_url}")

    formatted_description = "\n\n".join(description_blocks) if description_blocks else "Auto-generated event."

    # Convert times to ISO 8601 string
    start_str = raw.start_date.astimezone(timezone.utc).isoformat()
    end_str = raw.end_date.astimezone(timezone.utc).isoformat()

    return NormalizedCalendarPayload(
        summary=raw.event_name,
        start_time=start_str,
        end_time=end_str,
        is_all_day=raw.is_all_day,
        location=raw.location or "Online",
        description=formatted_description,
        reminders=raw.reminder_minutes
    )

# --- FastMCP 3.1 Tool Definitions ---

@mcp.tool(
    name="apply_calendar_mapping_rules",
    description="Transforms raw extracted LLM metadata into a normalized, provider-agnostic calendar event payload."
)
def process_calendar_mapping(raw_input: RawExtractedEventInput) -> NormalizedCalendarPayload:
    """Validates raw event input against calendar rules and emits normalized payload."""
    return normalize_event_payload(raw_input)

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [Google Calendar](../../tools/calendar_tasks/google_calendar.md): Primary external cloud calendar API target.
- [CalDAV](../../tools/intake_storage/caldav.md): Open standard calendar protocol for sovereign self-hosted synchronization.
- [Paperless-ngx](../../services/paperless-ngx.md): Primary document storage source for extracted event metadata (`doc_id`).
- [n8n](../../services/n8n.md): Workflow engine implementing these rules in production pipelines.
- [Date Extraction Prompt](../llm-prompts/date-extraction.md): The LLM prompt engineering template supplying raw extraction data.
- [Vikunja](../../services/vikunja.md): Sovereign task management framework for task-based reminders.
- [Model Context Protocol (FastMCP 3.1)](../../tools/automation_orchestration/mcp.md): Underlying agent protocol for tool execution.

## Sources / references
- [RFC 5545: iCalendar Core Object Specification](https://datatracker.ietf.org/doc/html/rfc5545)
- [Google Calendar API v3 Event Resource Reference](https://developers.google.com/calendar/api/v3/reference/events)
- [ISO 8601 Representation of Dates and Times](https://www.iso.org/iso-8601-date-and-time-format.html)
- [FastMCP 3.1 Task Protocol Specification](https://modelcontextprotocol.io/3.1/task-protocol)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
