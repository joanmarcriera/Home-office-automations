# Date Extraction

## What it is
Date Extraction is a specialized subset of structured data extraction focused on identifying, parsing, and normalizing temporal references (e.g., "next Tuesday," "the 5th of July," "yesterday") from unstructured text into standardized formats like ISO 8601. In June 2026, this has evolved into **Temporal Reasoning**, where agents maintain a "Current State" context to resolve complex relative dates across multi-step plans.

## What problem it solves
Temporal data is notoriously difficult for LLMs to handle accurately because:
- **Relative References**: Words like "tomorrow" or "next week" require a reference point (the "current date") to be meaningful.
- **Ambiguous Formats**: "01/02/03" could mean different dates depending on the locale (US vs. UK vs. ISO).
- **Inconsistent Context**: Users often omit the year or use vague terms like "later this month."
- **Normalization**: Backend systems and databases require absolute timestamps, not relative strings.
- **Agentic Planning**: Autonomous agents need precise date extraction to schedule [Temporal](../../tools/orchestration/temporal.md) workflows or update [Google Calendar](../../tools/calendar_tasks/google_calendar.md).

## Where it fits in the stack
This pattern is critical for **Scheduling Agents**, **Calendar Integrations**, and **Timeline Analysis** tools. It usually sits in the **Extraction layer** of an intake pipeline, feeding data into the [Orchestration Layer](../../tools/orchestration/index.md).

## Typical use cases
- **Autonomous Scheduling**: Parsing "remind me to buy milk tomorrow at 9am" into a structured [Task Schema](../../reference-implementations/metadata-schemas/task-schema.md).
- **Log Analysis**: Normalizing relative timestamps in unstructured server logs for forensic analysis.
- **Financial Auditing**: Extracting transaction dates from natural language descriptions or receipts for [Paperless-ngx](../../services/paperless-ngx.md).
- **Multi-Step Mission Planning**: Determining the deadlines for sub-tasks in an [Antigravity](../../tools/agents/antigravity.md) mission.

## Strengths
- **Programmatic Utility**: Turns human language into something a machine can schedule or query.
- **Consistency**: Eliminates locale-based confusion by enforcing ISO 8601 standards.
- **Enriched UX**: Allows users to interact with software using natural, relative timing.
- **Durable Scheduling**: Provides the precision required for [Temporal](../../tools/orchestration/temporal.md) workflows.

## Limitations
- **Timezone Complexity**: Handling user timezones vs. server timezones vs. UTC is a constant source of bugs.
- **Edge Cases**: Leap years, daylight savings time changes, and non-standard work weeks (e.g., "next business day").
- **Calculation Errors**: LLMs can occasionally fail at date math (e.g., calculating the date 45 days from now) without a scratchpad or tool.
- **Context Drift**: If the "system time" provided to the model is stale, all relative extractions will be incorrect.

## When to use it
- Any time your application needs to act on a date or time provided by a user via text or voice.
- For processing historical logs where the "reference date" might be the log's timestamp.
- When building [Scheduling Agents](../../tools/calendar_tasks/google_calendar.md) or [Task Managers](../../tools/calendar_tasks/google-tasks.md).

## When not to use it
- When the user is selecting a date from a UI picker (where the data is already structured).
- For simple keyword-based systems where exact normalization isn't required.
- When absolute dates are already provided in a consistent format (e.g., ISO-only logs).

## Getting started
1. **Inject System Time**: Always provide the current ISO timestamp and day of the week in the system prompt.
2. **Define a Pydantic Model**: Use [Instructor](../../tools/frameworks/instructor.md) to define a schema that includes a `datetime` object.
3. **Set Reference Date**: Use a tool like [Duckling](https://github.com/facebook/duckling) for deterministic parsing if an LLM is overkill.
4. **Implement Validation**: Ensure extracted dates are logical (e.g., a "due date" cannot be in 1970).
5. **Handle Timezones**: Explicitly request UTC or provide the user's timezone offset in the context.

## CLI examples
Using the [Ollama](../../services/ollama.md) CLI to test date extraction with a system prompt:

```bash
# Ask the model to extract a date with a reference time
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "system": "Current time is Friday, June 23, 2026, 10:00 AM UTC.",
  "prompt": "Extract the ISO date for next Tuesday at 3pm.",
  "format": "json",
  "stream": false
}'
```

Using [Duckling](https://github.com/facebook/duckling) via Docker for deterministic extraction:
```bash
# Call Duckling service to parse a relative date
curl -XPOST http://localhost:8000/parse \
     -d "text=tomorrow at 9am" \
     -d "reference_time=1782218400000" # June 23, 2026
```

## API examples
Date normalization using [PydanticAI](../../tools/frameworks/pydantic-ai.md) with system context:

```python
from pydantic import BaseModel
from datetime import datetime
from pydantic_ai import Agent

class DateResult(BaseModel):
    normalized_date: datetime
    original_text: str

# Create an agent with the current time in the system prompt
agent = Agent(
    'openai:gpt-5-5-preview',
    result_type=DateResult,
    system_prompt=f"The current date is {datetime.now().strftime('%A, %Y-%m-%d %H:%M:%S')}. Normalize user dates to ISO 8601."
)

async def run():
    result = await agent.run("Set a reminder for the third Thursday of next month")
    print(result.data.normalized_date)
```

## Related tools / concepts
- [Instructor](../../tools/frameworks/instructor.md) — For structured extraction and validation.
- [PydanticAI](../../tools/frameworks/pydantic-ai.md) — For agentic context management.
- [Duckling](https://github.com/facebook/duckling) — Deterministic temporal parser.
- [Extraction and Classification](extraction-and-classification.md) — The broader pattern for structured data.
- [Temporal](../../tools/orchestration/temporal.md) — Orchestrator that relies on precise timing.
- [Google Calendar](../../tools/calendar_tasks/google_calendar.md) — Target surface for extracted dates.
- [Google Tasks](../../tools/calendar_tasks/google-tasks.md) — Target surface for extracted tasks.
- [Task Schema](../../reference-implementations/metadata-schemas/task-schema.md) — Standardized task metadata.

## Sources / References
- [LLMs and Date Math: Best Practices](https://github.com/jxnl/instructor/blob/main/docs/blog/posts/date-parsing.md)
- [ISO 8601 Standard](https://www.iso.org/iso-8601-date-and-time-format.html)
- [Duckling: Relative Date Parsing](https://github.com/facebook/duckling)
- [PydanticAI Documentation: Result Types](https://ai.pydantic.dev/results/)

## Contribution Metadata
- Last reviewed: 2026-06-23
- Confidence: high
