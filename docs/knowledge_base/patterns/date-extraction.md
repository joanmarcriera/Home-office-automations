# Date Extraction

## What it is
Date Extraction is a specialized subset of structured data extraction focused on identifying, parsing, and normalizing temporal references (e.g., "next Tuesday," "the 5th of July," "yesterday") from unstructured text into standardized formats like ISO 8601.

## What problem it solves
Temporal data is notoriously difficult for LLMs to handle accurately because:
- **Relative References**: Words like "tomorrow" or "next week" require a reference point (the "current date") to be meaningful.
- **Ambiguous Formats**: "01/02/03" could mean different dates depending on the locale (US vs. UK vs. ISO).
- **Inconsistent Context**: Users often omit the year or use vague terms like "later this month."
- **Normalization**: Backend systems and databases require absolute timestamps, not relative strings.

## Where it fits in the stack
This pattern is critical for **Scheduling Agents**, **Calendar Integrations**, and **Timeline Analysis** tools. It usually sits in the **Extraction layer** of an intake pipeline.

## Core Concepts

### 1. The Reference Date Problem
An LLM has no inherent knowledge of "today." To extract relative dates correctly, the current system time must be injected into the prompt (e.g., in the SYSTEM prompt) so the model can calculate the absolute date.

### 2. Temporal Normalization
The process of converting a natural language date into a standard format.
- **Input**: "remind me in two hours"
- **Internal Logic**: (Reference Time: 2026-06-06T10:00:00Z) + 2 hours
- **Output**: `2026-06-06T12:00:00Z`

### 3. Verification and Validation
Using schemas to ensure that extracted dates are logically sound (e.g., an expiration date cannot be in the past).

## Key Implementation Tools
- **[Instructor](../../tools/frameworks/instructor.md)**: Frequently used to define Pydantic models that handle date validation.
- **[Duckling](https://github.com/facebook/duckling)**: A Haskell library (often used via a Clojure/Java wrapper) by Meta that is excellent at parsing relative dates and durations without an LLM.
- **[PydanticAI](../../tools/frameworks/pydantic-ai.md)**: Can be used to inject the current date into the model's context for relative calculation.

## Strategies for High Accuracy

### SYSTEM_DATE Injection
Always include the current date, time, and day of the week in the system message.
> "The current date is Saturday, June 6th, 2026. All relative dates mentioned by the user should be calculated based on this reference."

### Tool-Calling vs. Direct Extraction
Instead of asking the LLM to return a string, ask it to call a `create_calendar_event` tool with specific integer fields for `year`, `month`, `day`, etc. This forces the model to perform the calculation more rigidly.

### Chain-of-Thought for Math
For complex relative dates (e.g., "the third Thursday of next month"), encourage the model to reason through the calculation step-by-step before outputting the final ISO string.

## Technical Example: Date Normalization with Instructor

```python
from pydantic import BaseModel, Field, validator
from datetime import datetime
import instructor
from openai import OpenAI

class ScheduledTask(BaseModel):
    task: str
    due_date: datetime = Field(description="ISO 8601 format")

    @validator("due_date")
    def must_be_future(cls, v):
        if v < datetime.now():
            raise ValueError("Due date must be in the future")
        return v

client = instructor.from_provider(OpenAI())

# System prompt provides the necessary context
task = client.chat.completions.create(
    model="gpt-4o",
    response_model=ScheduledTask,
    messages=[
        {"role": "system", "content": f"Current time is {datetime.now().isoformat()}"},
        {"role": "user", "content": "Remind me to buy milk tomorrow at 9am"}
    ]
)
```

## Strengths
- **Programmatic Utility**: Turns human language into something a machine can schedule or query.
- **Consistency**: Eliminates locale-based confusion by enforcing ISO standards.
- **Enriched UX**: Allows users to interact with software using natural, relative timing.

## Limitations
- **Timezone Complexity**: Handling user timezones vs. server timezones vs. UTC is a common source of bugs.
- **Edge Cases**: Leap years, daylight savings time changes, and non-standard work weeks.
- **Calculation Errors**: LLMs can occasionally fail at date math even with a reference date.

## When to use it
- Any time your application needs to act on a date or time provided by a user via text or voice.
- For processing historical logs where the "reference date" might be the log's timestamp.

## Typical use cases
- **Task Scheduling**: Parsing "remind me to call Mom at 5pm on Friday" into a structured task.
- **Log Analysis**: Normalizing relative timestamps in unstructured server logs.
- **Financial Auditing**: Extracting transaction dates from natural language descriptions or receipts.

## When not to use it
- When the user is selecting a date from a UI picker (where the data is already structured).
- For simple keyword-based systems where exact normalization isn't required.

## Related tools / concepts
- [Instructor](../../tools/frameworks/instructor.md)
- [PydanticAI](../../tools/frameworks/pydantic-ai.md)
- [Duckling](https://github.com/facebook/duckling)

## Related Patterns
- [Extraction and Classification](../../knowledge_base/patterns/extraction-and-classification.md)
- [Tool Calling](../../knowledge_base/patterns/tool-calling-and-mcp.md)

## Sources / References
- [LLMs and Date Math: Best Practices](https://github.com/jxnl/instructor/blob/main/docs/blog/posts/date-parsing.md)
- [ISO 8601 Standard](https://www.iso.org/iso-8601-date-and-time-format.html)
- [Duckling Repository](https://github.com/facebook/duckling)

## Contribution Metadata
- Last reviewed: 2026-06-06
- Confidence: high
