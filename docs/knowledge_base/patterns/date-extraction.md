# Date Extraction

## What it is
Date Extraction is a specialized subset of structured data extraction focused on identifying, parsing, and normalizing temporal references (e.g., "next Tuesday," "the 5th of July," "yesterday") from unstructured text into standardized formats like ISO 8601. In 2026, this has evolved into **Temporal Reasoning**, where agents use the Model Control Protocol (MCP 3.0) to dynamically query calendars and resolve complex relative references within the context of a user's specific schedule and timezone.

## What problem it solves
Temporal data is notoriously difficult for LLMs to handle accurately because:
- **Relative References**: Words like "tomorrow" or "next week" require a reference point (the "current date") to be meaningful.
- **Ambiguous Formats**: "01/02/03" could mean different dates depending on the locale (US vs. UK vs. ISO).
- **Inconsistent Context**: Users often omit the year or use vague terms like "later this month."
- **Normalization**: Backend systems and databases require absolute timestamps, not relative strings.
- **Dynamic Scheduling**: Resolving "next available time" requires real-time access to calendar state.

## Where it fits in the stack
This pattern is critical for **Scheduling Agents**, **Calendar Integrations**, and **Timeline Analysis** tools. It sits in the **Extraction layer** of an intake pipeline and the **Reasoning layer** of an agentic loop.

## Typical use cases
- **Task Scheduling**: Parsing "remind me to call Mom at 5pm on Friday" into a structured task in [Google Tasks](../../tools/calendar_tasks/google-tasks.md) or [Todoist](../../tools/calendar_tasks/todoist.md).
- **Meeting Coordination**: Resolving "Are we free next Wednesday morning?" by extracting the intent and checking [Google Calendar](../../tools/calendar_tasks/google_calendar.md) or [Outlook](../../tools/calendar_tasks/outlook.md).
- **Log Analysis**: Normalizing relative timestamps in unstructured server logs for auditing.
- **Temporal Search**: Enabling queries like "show me emails from the first week of last May."

## Strengths
- **Programmatic Utility**: Turns human language into something a machine can schedule or query.
- **Consistency**: Eliminates locale-based confusion by enforcing ISO 8601 standards.
- **Enriched UX**: Allows users to interact with software using natural, relative timing (e.g., "next time I'm in NYC").
- **Agentic Integration**: Enables agents to act as autonomous personal assistants via MCP 3.0.

## Limitations
- **Timezone Complexity**: Handling user timezones vs. server timezones vs. UTC is a common source of bugs.
- **Calculation Errors**: LLMs can occasionally fail at complex date math (e.g., "the third Thursday after Labor Day") without chain-of-thought prompting.
- **Ambiguity**: Phrases like "next Friday" can mean different things depending on whether today is Monday or Thursday.

## When to use it
- Any time your application needs to act on a date or time provided by a user via text or voice.
- For processing historical data where the "reference date" might be different from the current system time.
- When building agents that need to manage schedules or track deadlines.

## When not to use it
- When the user is selecting a date from a UI picker (where the data is already structured).
- For simple systems where exact normalization isn't required and fuzzy matching is sufficient.

## Getting started
To implement high-accuracy date extraction:
1. **Inject Reference Context**: Always provide the current date, time, and day of the week in your System Prompt.
2. **Use Schema-First Extraction**: Define a Pydantic model with `datetime` fields using [Instructor](../../tools/frameworks/instructor.md).
3. **Handle Timezones**: Explicitly ask the model to return UTC offsets or use the user's local timezone.
4. **Leverage MCP Tools**: Use [Google Calendar](../../tools/calendar_tasks/google_calendar.md) MCP servers to resolve availability.
5. **Chain-of-Thought Math**: Encourage the model to reason through the date calculation step-by-step.

## CLI examples
Using a hypothetical date-extraction CLI tool:

```bash
# Normalize a relative date string
date-extract "next tuesday at 3pm" --reference "2026-06-24T10:00:00Z"
# Output: 2026-06-30T15:00:00Z
```

Using `curl` to query an extraction model:

```bash
curl -X POST https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {"role": "system", "content": "Today is Wednesday, June 24, 2026."},
      {"role": "user", "content": "Schedule a meeting for tomorrow at noon."}
    ],
    "response_format": { "type": "json_object" }
  }'
```

## API examples
Example using [Instructor](../../tools/frameworks/instructor.md) and Pydantic:

```python
from pydantic import BaseModel, Field
from datetime import datetime
import instructor
from openai import OpenAI

class Appointment(BaseModel):
    title: str
    start_time: datetime = Field(description="ISO 8601 format")
    end_time: datetime = Field(description="ISO 8601 format")

client = instructor.from_provider(OpenAI())

# Injected reference context is key
current_time = datetime.now().strftime("%A, %B %d, %Y %I:%M%p")

appt = client.chat.completions.create(
    model="gpt-4o",
    response_model=Appointment,
    messages=[
        {"role": "system", "content": f"Current time is {current_time}. Day is Wednesday."},
        {"role": "user", "content": "Lunch with Sarah tomorrow from 12 to 1:30"}
    ]
)
# Result: Appointment(title='Lunch with Sarah', start_time=datetime(2026, 6, 25, 12, 0), end_time=datetime(2026, 6, 25, 13, 30))
```

## Related tools / concepts
- [Instructor](../../tools/frameworks/instructor.md) — Standard for structured extraction.
- [PydanticAI](../../tools/frameworks/pydantic-ai.md) — Agent framework with built-in validation.
- [Google Calendar](../../tools/calendar_tasks/google_calendar.md) — Primary target for extracted dates.
- [Google Tasks](../../tools/calendar_tasks/google-tasks.md) — Secondary target for task-based dates.
- [Todoist](../../tools/calendar_tasks/todoist.md) — Popular task management integration.
- [Extraction and Classification](extraction-and-classification.md) — The parent pattern for date extraction.
- [Temporal Reasoning](../temporal-reasoning.md) — Advanced patterns for time-aware agents.
- [Model Context Protocol (MCP)](tool-calling-and-mcp.md) — Standard for connecting to calendar tools.

## Sources / References
- [LLMs and Date Math: Best Practices](https://github.com/jxnl/instructor/blob/main/docs/blog/posts/date-parsing.md)
- [ISO 8601 Standard](https://www.iso.org/iso-8601-date-and-time-format.html)
- [Anthropic: Contextualizing Time for Claude](https://docs.anthropic.com/claude/docs/temporal-context)
- [PydanticAI: Using Context for Dates](https://ai.pydantic.dev/concepts/context-injection/)

## Contribution Metadata
- Last reviewed: 2026-06-24
- Confidence: high
