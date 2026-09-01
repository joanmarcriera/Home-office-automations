# Date Extraction

## What it is
Date Extraction is a specialized subset of structured data extraction focused on identifying, parsing, and normalizing temporal references (e.g., "next Tuesday," "the 5th of July," "yesterday") from unstructured text into standardized formats like ISO 8601. In early January 2027, this has matured into **Agentic Temporal Reasoning**, where autonomous agent loops utilize stateful "Current System Time" offsets, timezone database contexts, and FastMCP 3.1 Task Protocol temporal capabilities to resolve complex multi-step execution timelines, relative deadlines, and recurring events with high precision.

## What problem it solves
Temporal data is notoriously difficult for LLMs to handle accurately because:
- **Relative Ambiguity**: Indexical words like "tomorrow," "next week," or "the day after" require a precise, dynamic reference point (the "current system time") to be meaningful.
- **Locale Ambiguities**: Formats like "01/02/03" can mean different dates depending on the user's regional configuration (US MM/DD/YY vs. UK DD/MM/YY vs. ISO YY/MM/DD).
- **Vague Input Context**: Users frequently omit the year or reference fuzzy windows like "later this month" or "towards the end of the quarter."
- **Standardized Normalization**: Backend databases and downstream applications require precise absolute timestamps (UTC) rather than colloquial phrases.
- **Agentic Scheduling**: Autonomous systems require precise, timezone-aware dates to invoke [Temporal](../../tools/orchestration/temporal.md) orchestrators or update [Google Calendar](../../tools/calendar_tasks/google_calendar.md) via FastMCP 3.1 tools.

## Where it fits in the stack
This pattern is critical for **Scheduling Agents**, **Calendar Integrations**, and **Timeline Analysis** tools. It resides in the **Extraction layer** of an intake pipeline, feeding data into the [Orchestration Layer](../../tools/orchestration/index.md).

## Typical use cases
- **Autonomous Scheduling**: Converting "set a meeting for tomorrow at 2:30pm" into a structured [Task Schema](../../reference-implementations/metadata-schemas/task-schema.md) object with precise UTC bounds.
- **Log Timeline Parsing**: Normalizing relative offsets in legacy database or server log streams into absolute temporal entries.
- **Financial Document Ingestion**: Extracting transaction dates from invoices or receipts for indexing in [Paperless-ngx](../../services/paperless-ngx.md).
- **Long-Horizon Mission Tracking**: Determining start, end, and duration parameters for sub-tasks within an [Antigravity](../../tools/agents/antigravity.md) execution plan.

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

## When to use it
- When implementing a conversational voice or chat interface that schedules appointments, deadlines, or alarms.
- For processing legacy documents containing relative dates (e.g., "30 days from invoice date").
- For building agentic integrations with [Scheduling Tools](../../tools/calendar_tasks/google_calendar.md) or [Task Managers](../../tools/calendar_tasks/google-tasks.md).

## When not to use it
- When dates are already collected through structured GUI inputs (like calendar pickers).
- In legacy pipelines where inputs are strictly guaranteed to be pre-formatted ISO 8601 strings.
- For simple static keyword triggers that do not require logical temporal resolution.

## Getting started
1. **Always Inject Reference Time**: Pass the current absolute system date, time, and day of the week in the LLM's system prompt.
2. **Design a Strict Pydantic Schema**: Use [Instructor](../../tools/frameworks/instructor.md) or [PydanticAI](../../tools/frameworks/pydantic-ai.md) to define a structure containing typed `datetime` values.
3. **Handle Timezones Explicitly**: Pass the user's localized timezone offset (e.g., `America/New_York`) to resolve relative terms like "tonight."
4. **Implement Range Validation**: Create validators to verify extracted times are logical (e.g., expiration dates cannot be in the past).
5. **Add a Fallback Parser**: Integrate a deterministic library (like `dateparser` or Duckling) for simple, deterministic temporal segments.

## CLI examples
Using the [Ollama](../../services/ollama.md) CLI with a system instruction to test localized date extraction with a frontier model:

```bash
# Extract relative date from user text with a provided reference timestamp
curl http://localhost:11434/api/generate -d '{
  "model": "llama4",
  "system": "The current system time is Friday, December 25, 2026, 14:00 UTC.",
  "prompt": "Extract next Monday at 10 AM as an ISO 8601 UTC timestamp. Return JSON only.",
  "format": "json",
  "stream": false
}'
```

Calling a local Duckling service via curl for high-speed, deterministic parsing:
```bash
# Query Duckling parser with absolute reference time
curl -X POST http://localhost:8000/parse \
     -d "text=tomorrow at noon" \
     -d "reference_time=1798207200000" # Milliseconds for December 25, 2026
```

## API examples
Temporal reasoning and date extraction using [PydanticAI](../../tools/frameworks/pydantic-ai.md) with timezone-aware validation in Python (Pydantic v2.13+):

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field, field_validator
from pydantic_ai import Agent

# Define the target structured date extraction schema
class TemporalEvent(BaseModel):
    normalized_utc: datetime = Field(description="The extracted event timestamp normalized to UTC")
    event_title: str = Field(description="Fleshed out name or purpose of the event")
    confidence_score: float = Field(ge=0.0, le=1.0)

    # Validate that scheduled events are not set in the past
    @field_validator("normalized_utc")
    @classmethod
    def prevent_past_events(cls, value: datetime) -> datetime:
        now_utc = datetime.now(ZoneInfo("UTC"))
        if value < now_utc:
            raise ValueError("The extracted date cannot be in the past.")
        return value

# Define current context to inject into agent execution
current_time_str = datetime.now(ZoneInfo("UTC")).strftime("%A, %Y-%m-%d %H:%M:%S UTC")

# Initialize the PydanticAI Agent with SOTA late December 2026 model (Claude 5.1 / GPT-5.5 / Gemini 4.0 Pro era)
agent = Agent(
    'openai:gpt-5-5-preview',
    result_type=TemporalEvent,
    system_prompt=(
        f"You are an expert temporal reasoning assistant. The current system time is exactly "
        f"{current_time_str}. Use this exact timestamp to normalize relative references "
        f"(e.g., 'tomorrow', 'next Tuesday') to an absolute ISO 8601 UTC date."
    )
)

async def extract_meeting_time(user_query: str) -> TemporalEvent:
    # Run the agentic extraction loop (PydanticAI automatically handles self-correction/retries)
    result = await agent.run(user_query)
    return result.data

# Example invocation
# query: "Schedule a sync for our project retro next Wednesday at 3 PM PST"
# result.normalized_utc -> Normalized absolute datetime object in UTC timezone
```

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
