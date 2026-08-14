# Playbook: Email to Calendar Automation

## What it is

Email to Calendar Automation is a specialized administrative workflow that leverages Large Language Models (LLMs), [MCP 3.1](../knowledge_base/patterns/tool-calling-and-mcp.md), and [FastMCP 3.1](../knowledge_base/patterns/tool-calling-and-mcp.md) to parse incoming emails (newsletters, flight confirmations, medical appointments) and sync them to a primary calendar. It utilizes [n8n](../services/n8n.md) as the orchestrator and [Claude 5.1](../tools/ai_knowledge/claude.md), [GPT-5.5](../tools/ai_knowledge/openai.md), or [Gemini 4.0 Pro](../tools/ai_knowledge/gemini.md) for precise temporal reasoning.

## What problem it solves

Digital calendars are often incomplete because event data is trapped in unstructured email bodies. Manually transcribing these events is time-consuming and error-prone. This playbook solves the "manual entry" problem by automating the extraction of dates, times, and locations, ensuring that the family or office calendar is always up-to-date with zero human effort.

## Where it fits in the stack

**Category**: Playbook / Personal Productivity. It sits at the **Integration and Orchestration Layer**, connecting the **Email Server** (via IMAP) to **Calendar Services** (Google Calendar, iCloud, Radicale) using **LLM Reasoning Nodes** and [Chronos MCP](../tools/automation_orchestration/chronos-mcp.md).

## Typical use cases

- **School Event Syncing**: Extracting field trip dates and early dismissal times from school newsletters.
- **Travel Itinerary Management**: Parsing flight confirmations and hotel bookings for a unified travel view.
- **Medical Appointment Tracking**: Capturing appointment details from clinic confirmation emails.
- **Utility Bill Deadlines**: Adding payment due dates from utility providers to the "Admin" calendar.

## Strengths

- **High Precision**: Uses early January 2027-class models ([Claude 5.1](../tools/ai_knowledge/claude.md), [GPT-5.5](../tools/ai_knowledge/openai.md), [Gemini 4.0 Pro](../tools/ai_knowledge/gemini.md)) for complex date/time reasoning.
- **Self-Cleaning**: Automatically tags processed emails in [Paperless-ngx](../services/paperless-ngx.md) to avoid duplicate entries.
- **Model Agnostic**: Supports routing between cloud models (GPT-5.5) and local models ([Llama 4](../tools/ai_knowledge/llama.md)) based on data sensitivity.
- **Protocol Native**: Utilizes [MCP 3.1](../knowledge_base/patterns/tool-calling-and-mcp.md) for standardized calendar tool access.

## Limitations

- **Ambiguous Language**: "Next Tuesday" extraction can fail if the email's "sent date" is not correctly passed as context to the LLM.
- **OCR Quality**: Emails containing only images of text require high-quality OCR (provided by [Paperless-ngx](../services/paperless-ngx.md)) to be effective.
- **Multi-Event Emails**: Newsletters containing multiple unrelated events require advanced chunking or multi-call extraction patterns.

## When to use it

- When you receive a high volume of schedule-impacting emails that require manual calendar entry.
- When you are already using [n8n](../services/n8n.md) and [Paperless-ngx](../services/paperless-ngx.md) for document management.
- When you need a centralized way to handle family-wide scheduling from multiple sources.

## When not to use it

- For emails with standardized calendar attachments (ICS files), which are better handled by native email client integrations.
- For extremely sensitive medical or legal scheduling if you are not running a fully local LLM stack.
- For low-volume users where manual entry is faster than setting up the automation.

## Getting started

To implement Email to Calendar Automation:

1.  **Monitor Inbox**: Set up an n8n IMAP trigger to watch a specific folder (e.g., `Automate/Calendar`).
2.  **Capture and Store**: Forward the email to [Paperless-ngx](../services/paperless-ngx.md) for archiving and OCR.
3.  **Extract with LLM**: Use the [Claude 5.1](../tools/ai_knowledge/claude.md) node in n8n with a structured prompt to return JSON.
4.  **Sync to Calendar**: Use the [Google Calendar](../tools/calendar_tasks/google_calendar.md) node or [Chronos MCP](../tools/automation_orchestration/chronos-mcp.md) to create the event.
5.  **Step-by-Step Flow**:
    ```mermaid
    flowchart TD
        A[New Email in IMAP folder] --> B[n8n Workflow Trigger]
        B --> C[Convert Email to PDF]
        C --> D[Upload to Paperless-ngx]
        D --> E[Extract Text via OCR]
        E --> F[Call LLM (Claude 5.1) for Date Extraction]
        F --> G{Event Found?}
        G -- Yes --> H[Create Calendar Event via MCP 3.1]
        G -- No --> I[Tag as Failed / Notify]
        H --> J[Update Paperless Tag: synced]
    ```

## CLI examples

### Triggering n8n Extraction via CLI
Manually testing the extraction logic for a specific document ID in Paperless:
```bash
# Execute n8n webhook with document context
curl -X POST https://n8n.local/webhook/extract-calendar-event \
     -H "Content-Type: application/json" \
     -d '{"document_id": "98765", "subject": "School Field Trip Update"}'
```

### Listing Upcoming Events via Chronos MCP
An agent using the Chronos MCP CLI to verify event creation:
```bash
# List events for the next 7 days
mcp tool call chronos-mcp list_events --start_date "2026-08-26" --end_date "2026-09-02"
```

## API examples

### n8n Extraction Prompt (JSON)
Configuring the Claude 5.1 node to return structured event data:
```json
{
  "model": "claude-5-1-opus-20260820",
  "prompt": "Extract event details from the following email text. Sent Date: {{ $json.sent_date }}. Return JSON with fields: event_name, start_date (ISO), end_date (ISO), location, and summary.",
  "text": "{{ $json.ocr_content }}"
}
```

### Google Calendar API Event Creation (Python)
Example of how an autonomous agent might finalize the event via API using strict Pydantic v2 validation:
```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ValidationError
from googleapiclient.discovery import build

class CalendarEventSchema(BaseModel):
    summary: str = Field(..., min_length=1)
    location: Optional[str] = None
    start_time: datetime = Field(...)
    end_time: datetime = Field(...)

def create_calendar_event(summary: str, location: Optional[str], start_time_str: str, end_time_str: str):
    try:
        event_data = CalendarEventSchema(
            summary=summary,
            location=location,
            start_time=datetime.fromisoformat(start_time_str),
            end_time=datetime.fromisoformat(end_time_str)
        )
    except ValidationError as e:
        print(f"Validation error: {e}")
        return None

    service = build('calendar', 'v3')
    event = {
        'summary': event_data.summary,
        'location': event_data.location,
        'start': {'dateTime': event_data.start_time.isoformat(), 'timeZone': 'America/Los_Angeles'},
        'end': {'dateTime': event_data.end_time.isoformat(), 'timeZone': 'America/Los_Angeles'},
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Event created: {event.get("htmlLink")}')
    return event.get("htmlLink")

# Example call
# create_calendar_event("School Field Trip", "City Museum", "2027-01-30T09:00:00", "2027-01-30T15:00:00")
```

## Related tools / concepts

- [n8n](../services/n8n.md): The primary workflow orchestrator.
- [Paperless-ngx](../services/paperless-ngx.md): Document archive and OCR engine.
- [Claude 5.1](../tools/ai_knowledge/claude.md): Recommended LLM for temporal reasoning.
- [Google Calendar](../tools/calendar_tasks/google_calendar.md): Default calendar target.
- [MCP 3.1](../knowledge_base/patterns/tool-calling-and-mcp.md): Standard for agentic tool use.
- [Chronos MCP](../tools/automation_orchestration/chronos-mcp.md): Specialized calendar MCP server.
- [Family Admin Automation](family-admin-automation.md): Broad household automation playbook.
- [Scan to Task](scan-to-task.md): Physical-to-digital task ingestion.
- [Temporal Reasoning](../knowledge_base/patterns/date-extraction.md): Core pattern for date parsing.

## Sources / References

- [n8n: Automating Calendar Events from Email](https://n8n.io/workflows/1234-email-to-google-calendar/)
- [Model Context Protocol (MCP) Specification](https://modelcontextprotocol.io/)
- [Google Calendar API: Events Insert](https://developers.google.com/calendar/api/v3/reference/events/insert)
- [Paperless-ngx API Documentation](https://docs.paperless-ngx.com/api/)

## Contribution Metadata

- Last reviewed: 2027-01-05
- Confidence: high
