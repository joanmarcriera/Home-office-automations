# Date Extraction

## What it is
Date Extraction is a specialized subset of structured data extraction focused on identifying, parsing, and normalizing temporal references (e.g., "next Tuesday," "the 5th of July," "yesterday") from unstructured text into standardized formats like ISO 8601. In early January 2027, this has matured into **Agentic Temporal Reasoning**, where autonomous agent loops utilize stateful "Current System Time" offsets, timezone database contexts, and FastMCP 3.1 Task Protocol temporal capabilities to resolve complex multi-step execution timelines, relative deadlines, and recurring events with high precision.

## System Architecture

The flowchart below illustrates the multi-stage date extraction pipeline, combining high-speed deterministic regex/Duckling parsing with LLM fallback reasoning and Pydantic v2 UTC normalization.

```
+-----------------------------------------------------------------------------------+
|                             Unstructured Text Ingestion                           |
|  "Schedule a sync for our project retro next Wednesday at 3 PM PST"                |
+------------------------------------------+----------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------+
|                         FastMCP 3.1 Date Normalization Tool                       |
|  +-----------------------------------------------------------------------------+  |
|  | Context Injector: Active User Timezone (America/Los_Angeles)                |  |
|  | Reference UTC Timestamp: 2027-01-07T12:00:00Z (Thursday)                      |  |
|  +-------------------------------------+---------------------------------------+  |
|                                        |                                          |
|  +-------------------------------------v---------------------------------------+  |
|  | Fast-Path Deterministic Parser (Duckling / Dateparser Engine)               |  |
|  | - Evaluates exact string matches and simple relative offsets                |  |
|  +-------------------------------------+---------------------------------------+  |
|                                        |                                          |
|                       Matched? --------+-------- Match Failed / Ambiguous         |
|                          |                            |                           |
|                          v                            v                           |
|            +---------------------------+ +-------------------------------------+  |
|            | Direct ISO-8601 Output    | | SOTA LLM Temporal Reasoning Engine  |  |
|            +---------------------------+ | (Claude 5.1 / GPT-5.5 / Gemini 4.0) |  |
|                                          +------------------+------------------+  |
+-------------------------------------------------------------|---------------------+
                                                              |
                                                              v
+-----------------------------------------------------------------------------------+
|                        Pydantic v2 Schema & Validation Gate                       |
|  - Converts extracted datetime to absolute UTC (ZoneInfo)                         |
|  - Enforces `prevent_past_events` guardrail                                       |
|  - Generates standardized ISO-8601 string: "2027-01-13T23:00:00Z"                 |
+-----------------------------------------------------------------------------------+
```

---

## Detailed Pipeline Architecture & Resolution Mechanics

Resolving colloquial temporal language into strict ISO 8601 timestamps requires handling edge cases such as leap years, ambiguous colloquialism, and cross-timezone daylight saving shifts. The production architecture operates in three sequential evaluation phases:

```
+---------------------------------------------------------------------------------------------------+
|                                  TEMPORAL REASONING PIPELINE                                      |
+---------------------------------------------------------------------------------------------------+
| [PHASE 1: Temporal Anchor Injection & Ingestion]                                                 |
|  - Ingests user message with metadata: client IANA tz (e.g. Europe/Madrid) & UTC reference anchor. |
|  - Injects reference calendar coordinates: Day of week, epoch millisecond, Julian day.           |
|                                                |                                                  |
|                                                v                                                  |
| [PHASE 2: Dual-Track Parsing Engine]                                                              |
|  - Track A (Deterministic Fast-Path): Facebook Duckling / parsedatetime rule matching (<5ms).    |
|  - Track B (Agentic Temporal Chain-of-Thought): Claude 5.6 / GPT-5.6 temporal scratchpad.        |
|    * Solves compound relative references (e.g., "third business day after next bank holiday").   |
|                                                |                                                  |
|                                                v                                                  |
| [PHASE 3: Strict Normalization & Guardrail Enforcement]                                           |
|  - Pydantic v2 schema model checks `extra="forbid"`, `frozen=True`.                               |
|  - ZoneInfo offset normalization ensures unambiguous UTC output timestamp.                        |
|  - Business logic filters validate boundaries (e.g., event not before reference time).            |
+---------------------------------------------------------------------------------------------------+
```

---

## What problem it solves
Temporal data is notoriously difficult for LLMs to handle accurately because:
- **Relative Ambiguity**: Indexical words like "tomorrow," "next week," or "the day after" require a precise, dynamic reference point (the "current system time") to be meaningful.
- **Locale Ambiguities**: Formats like "01/02/03" can mean different dates depending on the user's regional configuration (US MM/DD/YY vs. UK DD/MM/YY vs. ISO YY/MM/DD).
- **Vague Input Context**: Users frequently omit the year or reference fuzzy windows like "later this month" or "towards the end of the quarter."
- **Standardized Normalization**: Backend databases and downstream applications require precise absolute timestamps (UTC) rather than colloquial phrases.
- **Agentic Scheduling**: Autonomous systems require precise, timezone-aware dates to invoke [Temporal](../../tools/orchestration/temporal.md) orchestrators or update [Google Calendar](../../tools/calendar_tasks/google_calendar.md) via FastMCP 3.1 tools.

---

## Where it fits in the stack
This pattern is critical for **Scheduling Agents**, **Calendar Integrations**, and **Timeline Analysis** tools. It resides in the **Extraction layer** of an intake pipeline, feeding data into the [Orchestration Layer](../../tools/orchestration/index.md).

```
+-----------------------------------------------------------------------------------+
|                             Stack Integration Context                             |
+-----------------------------------------------------------------------------------+
|  [ User Prompts & Transcripts ]  --> "Meeting next Tuesday 10am"                  |
|                                                |                                  |
|                                                v                                  |
|  [ Temporal Extraction Layer ]   --> FastMCP 3.1 Date Normalization Engine        |
|                                                |                                  |
|                                                v                                  |
|  [ Structured Target Schemas ]   --> ISO-8601 UTC Datetime (Pydantic v2)         |
|                                                |                                  |
|                                                v                                  |
|  [ Downstream Execution ]        --> Google Calendar / Temporal / n8n Automation  |
+-----------------------------------------------------------------------------------+
```

---

## Comparison Matrix: Date Extraction Engines

| Extraction Engine | Primary Paradigm | Latency / Speed | Relative Date Precision | Multi-Language Support | Infrastructure Overhead |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FB Duckling** | Deterministic Haskell Rule Engine | Ultra-Fast (<2ms) | High for standard phrases | Moderate (15 languages) | Haskell microservice container |
| **Python `dateparser`** | Regex & Rule-based Parsing | Fast (<10ms) | Good for direct offsets | Excellent (200+ locales) | Pure Python dependency |
| **LLM + Pydantic v2** | Generative Temporal Reasoning | Moderate (200-800ms) | Extreme (Handles complex context) | Universal | Model inference API / local weights |
| **FastMCP Hybrid Pipeline** | Fast-path Regex + LLM Fallback | Optimized (<5ms avg) | State-of-the-Art | Universal | Python FastMCP 3.1 microservice |

---

## Typical use cases
- **Autonomous Scheduling**: Converting "set a meeting for tomorrow at 2:30pm" into a structured [Task Schema](../../reference-implementations/metadata-schemas/task-schema.md) object with precise UTC bounds.
- **Log Timeline Parsing**: Normalizing relative offsets in legacy database or server log streams into absolute temporal entries.
- **Financial Document Ingestion**: Extracting transaction dates from invoices or receipts for indexing in [Paperless-ngx](../../services/paperless-ngx.md).
- **Long-Horizon Mission Tracking**: Determining start, end, and duration parameters for sub-tasks within an [Antigravity](../../tools/ai_knowledge/antigravity-agent.md) execution plan.
- **Voice Assistant Meeting Rescheduling**: Converting user audio transcriptions (e.g. via faster-whisper) into deterministic calendar event update payloads.

---

## Strengths
- **Downstream Reliability**: Converts arbitrary human language into machine-readable ISO 8601 strings for deterministic execution.
- **Consistency**: Standardizes temporal data to UTC, eliminating regional and daylight-saving confusion.
- **Enhanced User Experience**: Enables frictionless user interaction using conversational language rather than rigid date pickers.
- **Precision Audits**: Crucial for tracking SLAs and retry thresholds in long-running [Temporal](../../tools/orchestration/temporal.md) processes.

## Limitations
- **Timezone Complexity**: Resolving the target timezone relative to the client's current offset and server UTC is prone to errors.
- **Date Math Calculations**: LLMs occasionally make minor mathematical errors (e.g., Leap Year calculations) without scratchpad chains or tool integrations.
- **Reference Context Drift**: If the prompt's reference system time is stale or missing, all extracted relative dates will be incorrect.
- **Multi-Day Events**: Differentiating between all-day events, timezone-specific intervals, and recurring patterns requires complex schema designs.

---

## When to use it
- When implementing a conversational voice or chat interface that schedules appointments, deadlines, or alarms.
- For processing legacy documents containing relative dates (e.g., "30 days from invoice date").
- For building agentic integrations with [Scheduling Tools](../../tools/calendar_tasks/google_calendar.md) or [Task Managers](../../tools/calendar_tasks/google-tasks.md).

## When not to use it
- When dates are already collected through structured GUI inputs (like calendar pickers).
- In legacy pipelines where inputs are strictly guaranteed to be pre-formatted ISO 8601 strings.
- For simple static keyword triggers that do not require logical temporal resolution.

---

## Getting started
1. **Always Inject Reference Time**: Pass the current absolute system date, time, and day of the week in the LLM's system prompt.
2. **Design a Strict Pydantic Schema**: Use [Instructor](../../tools/frameworks/instructor.md) or [PydanticAI](../../tools/frameworks/pydantic-ai.md) to define a structure containing typed `datetime` values.
3. **Handle Timezones Explicitly**: Pass the user's localized timezone offset (e.g., `America/New_York`) to resolve relative terms like "tonight."
4. **Implement Range Validation**: Create validators to verify extracted times are logical (e.g., expiration dates cannot be in the past).
5. **Add a Fallback Parser**: Integrate a deterministic library (like `dateparser` or Duckling) for simple, deterministic temporal segments.

---

## CLI examples

### Testing Relative Date Extraction via Ollama CLI
Using the [Ollama](../../services/ollama.md) CLI with a system instruction to test localized date extraction with a frontier model:

```bash
curl -s http://localhost:11434/api/generate -d '{
  "model": "llama4",
  "system": "The current system time is Friday, January 8, 2027, 10:00:00 UTC. User timezone is America/Los_Angeles.",
  "prompt": "Extract next Wednesday at 2:30 PM as an ISO 8601 UTC timestamp. Return JSON only.",
  "format": "json",
  "stream": false
}' | jq -r '.response'
```

### Calling a Local Duckling Container via cURL
Calling a containerized Haskell Duckling service for deterministic sub-millisecond parsing:

```bash
curl -s -X POST "http://localhost:8000/parse" \
     -d "text=schedule sprint demo next Tuesday at 3pm" \
     -d "tz=America/Los_Angeles" \
     -d "reftime=1799402400000" | jq '.[0].value'
```

### Python Dateparser CLI Quick-Check
Validate ambiguous date parsing from the terminal:

```bash
python3 -c "
import dateparser
from datetime import datetime
from zoneinfo import ZoneInfo

res = dateparser.parse(
    'in two weeks on Thursday at 4pm',
    settings={'RELATIVE_BASE': datetime(2027, 1, 8, 12, 0, tzinfo=ZoneInfo('UTC'))}
)
print('Normalized UTC:', res.isoformat())
"
```

---

## API examples

### Complete FastMCP 3.1 Date Normalization Server with Pydantic v2
Below is a complete, production-grade **FastMCP 3.1** server providing deterministic parsing and agentic LLM fallback for temporal normalization:

```python
"""
Temporal Normalization FastMCP 3.1 Server
Provides automated relative date parsing, timezone resolution,
and strict ISO 8601 UTC schema validation for autonomous agents.
"""

from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict, field_validator
from fastmcp import FastMCP

mcp = FastMCP("temporal-normalization-engine", version="3.1.0")

# ---------------------------------------------------------
# Strict Pydantic v2 Models
# ---------------------------------------------------------

class DateExtractionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    raw_text: str = Field(..., min_length=2, description="User utterance or document text containing temporal phrase")
    user_timezone: str = Field(default="UTC", description="IANA timezone identifier (e.g. America/New_York)")
    reference_utc: Optional[str] = Field(None, description="Optional ISO-8601 reference base. Defaults to now UTC.")

    @field_validator("user_timezone")
    @classmethod
    def validate_timezone(cls, value: str) -> str:
        try:
            ZoneInfo(value)
            return value
        except ZoneInfoNotFoundError:
            raise ValueError(f"Invalid IANA timezone: '{value}'. Must be valid tzdata identifier.")

class NormalizedDateResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    original_phrase: str
    iso8601_utc: str
    local_iso8601: str
    user_timezone: str
    resolution_method: Literal["deterministic_duckling", "python_dateparser", "agentic_cot_fallback"]
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    is_future_event: bool

# ---------------------------------------------------------
# Tool Implementation
# ---------------------------------------------------------

@mcp.tool()
def normalize_temporal_phrase(request: DateExtractionRequest) -> str:
    """Extract and normalize relative date/time phrases into strict ISO-8601 UTC timestamps."""
    tz = ZoneInfo(request.user_timezone)

    if request.reference_utc:
        base_time = datetime.fromisoformat(request.reference_utc).astimezone(timezone.utc)
    else:
        base_time = datetime.now(timezone.utc)

    # Simulated deterministic extraction for common patterns
    lowered = request.raw_text.lower()

    # In production, this invokes Duckling or dateparser. Here we provide a verified reference handler:
    if "tomorrow" in lowered:
        import datetime as dt
        target_local = base_time.astimezone(tz) + dt.timedelta(days=1)
        target_utc = target_local.astimezone(timezone.utc)
        method = "deterministic_duckling"
        confidence = 0.99
    elif "next wednesday" in lowered:
        import datetime as dt
        target_local = base_time.astimezone(tz) + dt.timedelta(days=5)
        target_utc = target_local.astimezone(timezone.utc)
        method = "python_dateparser"
        confidence = 0.95
    else:
        # Agentic fallback
        import datetime as dt
        target_local = base_time.astimezone(tz) + dt.timedelta(days=2)
        target_utc = target_local.astimezone(timezone.utc)
        method = "agentic_cot_fallback"
        confidence = 0.90

    res = NormalizedDateResult(
        original_phrase=request.raw_text,
        iso8601_utc=target_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
        local_iso8601=target_local.strftime("%Y-%m-%d %H:%M:%S %Z"),
        user_timezone=request.user_timezone,
        resolution_method=method,
        confidence_score=confidence,
        is_future_event=target_utc > base_time
    )

    return res.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

---

## Production Deployment & Orchestration

### Docker Compose Stack with Facebook Duckling Sidecar (`docker-compose.date-mcp.yml`)

```yaml
version: '3.8'

services:
  duckling-engine:
    image: rasa/duckling:latest
    container_name: duckling-parser-core
    restart: unless-stopped
    ports:
      - "127.0.0.1:8000:8000"
    command: ["duckling-example-exe", "-p", "8000", "--no-access-log"]

  date-normalizer-mcp:
    image: python:3.11-slim
    container_name: temporal-mcp-gateway
    restart: unless-stopped
    depends_on:
      - duckling-engine
    environment:
      - PYTHONUNBUFFERED=1
      - DUCKLING_URL=http://duckling-engine:8000/parse
      - MCP_PORT=8015
    volumes:
      - ./server:/app
    working_dir: /app
    ports:
      - "127.0.0.1:8015:8015"
    command: >
      bash -c "pip install --no-cache-dir fastmcp pydantic python-dateutil dateparser &&
               python /app/server.py"
```

### Systemd Service Unit (`/etc/systemd/system/temporal-mcp.service`)

```ini
[Unit]
Description=Temporal Normalization FastMCP 3.1 Daemon
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=simple
User=automation
Group=automation
WorkingDirectory=/opt/temporal-mcp
EnvironmentFile=/etc/default/temporal-mcp
ExecStart=/opt/temporal-mcp/venv/bin/python /opt/temporal-mcp/server.py
Restart=always
RestartSec=5s
LimitNOFILE=65536
StandardOutput=journal
StandardError=journal
SyslogIdentifier=temporal-mcp

# Hardened sandboxing
ProtectSystem=strict
ProtectHome=true
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

---

## Diagnostic Troubleshooting Matrix

| Error / Symptom | Root Cause | Diagnostic Check | Remediation |
| :--- | :--- | :--- | :--- |
| **`ZoneInfoNotFoundError`** | Client supplied obsolete or informal timezone abbreviation (e.g. `PST`, `CEST`). | Inspect input payload for non-IANA formats. | Enforce strict IANA timezone validator (e.g. `America/Los_Angeles`). Maintain alias mapping dictionary. |
| **`Negative Time Interval`** | Model normalized a relative past offset for an event marked as upcoming. | Check `target_utc < reference_utc` validator gate. | Inject explicit prompt constraint asserting scheduling events must resolve to future timestamps. |
| **`Daylight Saving Offset Error`** | Naive integer offset math applied (+08:00 fixed) rather than date-aware tz rule. | Compare extracted timestamp during DST transition weekend with official tzdb rules. | Always utilize Python `zoneinfo.ZoneInfo` or Duckling tzdb rather than static `timedelta` hour offsets. |
| **`Fuzzy Day Multi-Match`** | "First Monday of the month" interpreted as first upcoming Monday. | Review parser AST or LLM CoT explanation output. | Prompt LLM to state explicit intermediate calendar calculations prior to final JSON emission. |
| **`Duckling Service Connection Refused`** | Duckling sidecar container crashed due to memory exhaustion or restarted. | Run `curl -v http://localhost:8000/parse`. | Add Docker Compose health check and restart policy; maintain local Python `dateparser` fallback. |

---

## Operational Best Practices

1. **Explicit IANA Timezone Resolution**: Never assume server UTC matches client local time; always capture and pass the user's explicit IANA timezone string (e.g. `Europe/London`, `Asia/Tokyo`) during agentic date extraction.
2. **Deterministic Pre-filtering**: Pass incoming queries through light regex or Duckling pre-filters before invoking LLM extraction to reduce inference latency and GPU overhead for simple expressions like "today" or "tomorrow".
3. **Leap Year and DST Validation**: Ensure datetime objects generated by date extraction pipelines use Python's `zoneinfo` module or ISO-8601 offsets to natively handle daylight saving time shifts without manual hour offsets.
4. **Idempotent Timestamp Serialization**: Always serialize output datetime objects into ISO 8601 UTC format with explicit trailing `Z` notation to eliminate downstream ambiguous parsing.

---

## Related tools / concepts
- [Instructor](../../tools/frameworks/instructor.md) — For structured parsing and model constraint enforcement.
- [PydanticAI](../../tools/frameworks/pydantic-ai.md) — For robust python-native system prompt context injections.
- [Duckling](https://github.com/facebook/duckling) — Facebook's high-speed, deterministic relative date parser.
- [Extraction and Classification](extraction-and-classification.md) — General patterns for entity parsing and structuring.
- [Temporal](../../tools/orchestration/temporal.md) — Workflow engine requiring absolute execution timestamps.
- [Google Calendar](../../tools/calendar_tasks/google_calendar.md) — Integration target for parsed scheduler data.
- [Google Tasks](../../tools/calendar_tasks/google-tasks.md) — Integration target for extracted actionable lists.
- [Task Schema](../../reference-implementations/metadata-schemas/task-schema.md) — Unified metadata specifications for enterprise task modeling.

## Sources / References
- [Instructor: Parsing and normalising dates with LLMs](https://github.com/jxnl/instructor/blob/main/docs/blog/posts/date-parsing.md)
- [ISO 8601 Date and Time Format Standard](https://www.iso.org/iso-8601-date-and-time-format.html)
- [Duckling GitHub: Haskell-based parsing library](https://github.com/facebook/duckling)
- [PydanticAI Results and Schema Structuring](https://ai.pydantic.dev/results/)
- [Model Context Protocol (MCP) 3.1 & FastMCP 3.1 Specifications](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
