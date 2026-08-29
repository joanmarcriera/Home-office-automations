# Fantastical

## What it is
A premium calendar and tasks application for macOS, iOS, iPadOS, and watchOS, widely recognized for its best-in-class natural language processing and elegant design. As of early January 2027, it serves as a primary interface for **Agentic Calendar Orchestration**, leveraging **MCP 3.1** and **FastMCP 3.1** Task Protocols for seamless integration with advanced AI models like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, and **Qwen 3.6 VL**.

## What problem it solves
Simplifies event and task creation through natural language input and provides a beautiful, unified interface for multiple calendar and task accounts. It solves the "scheduling friction" by allowing users to speak or type their intent without navigating complex forms, now enhanced by [Gemma 4](../ai_knowledge/local_llms.md) and Qwen 3.6 VL for local intent parsing.

## Where it fits in the stack
**Category**: Calendar & Tasks / Personal Productivity. It acts as the primary user interface (GUI) for the [Apple Calendar](apple-calendar.md) ecosystem, Google Calendar, and Microsoft 365, often orchestrated by [Claude 5.6](../ai_knowledge/claude.md) and GPT-5.6 via the **FastMCP 3.1 Task Protocol**.

## Typical use cases
- **Rapid Scheduling**: Creating complex events with alerts and locations using simple sentences.
- **Unified Management**: Managing iCloud, Google, Microsoft 365 (Graph), and Exchange accounts in one view.
- **Calendar Sets**: Automatically switching visible calendars based on location or Focus mode.
- **Agentic Scheduling**: Using the **Fantastical FastMCP 3.1 Connector** for [Claude Code](../development_ops/claude-code.md) and GPT-5.6 to manage events via autonomous agents.

## Strengths
- **Superior Natural Language Parsing**: Handles complex recurring rules and attendee invites via text.
- **Flexibits Premium**: Includes both Fantastical and Cardhop (contacts) for a unified productivity suite.
- **Ecosystem Integration**: Deep support for Apple-specific features like widgets, Menubar icon, and Handoff.
- **FastMCP 3.1 Support**: Native integration with agentic frameworks, allowing AI to read/write events with user-in-the-loop verification.

## Limitations
- **Subscription-Based**: Most core productivity features require a Flexibits Premium subscription.
- **Apple Ecosystem Exclusive**: No native support for Windows or Android.
- **Proprietary**: Not an open-source solution; data is synced via third-party providers or iCloud.

## When to use it
- If you are a power user on Apple devices and value speed of entry.
- When you need to manage multiple diverse calendar accounts (Work/Personal) seamlessly.
- If you want a more intuitive, visual way to interact with your schedule via [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md).

## When not to use it
- On non-Apple platforms.
- If you prefer a free, basic calendar experience (use [Apple Calendar](apple-calendar.md)).
- If you require a local-first, open-source calendar client (consider [Radicale](../../services/radicale.md)).

## Getting started
Fantastical is a client-side application. Install it via the Mac App Store or direct download from the Flexibits website.

### Installation
```bash
# On macOS via Homebrew Cask
brew install --cask fantastical
```

### Hello-world example
After installation, open Fantastical and use the natural language parser (**Cmd+N**) to create your first event:
`Meeting with Jules at 2pm tomorrow /Work` (The `/Work` suffix automatically assigns it to the "Work" calendar).

## CLI examples
While Fantastical does not provide a dedicated CLI binary, it can be controlled on macOS using the `open` command and its custom URL scheme.

```bash
# Create a new event using natural language
open "x-fantastical3://parse?sentence=Lunch%20with%20Alice%20at%201pm"

# Create a task (reminder)
open "x-fantastical3://parse?sentence=todo%20Buy%20milk%20at%205pm"

# Navigate to a specific date in the calendar
open "x-fantastical3://show?date=2027-01-08"
```

## API examples
Fantastical offers deep integration on macOS via **AppleScript** and a robust URL scheme. In early January 2027, agents such as Claude 5.6 and GPT-5.6 programmatically compile commands and validate the scheduling parameters using **Pydantic v2** prior to invoking AppleScript hooks or FastMCP interfaces.

### AppleScript with Python Wrapper and Pydantic v2
```python
import subprocess
from typing import Optional
from pydantic import BaseModel, Field, ValidationError

class FantasticalEventSchema(BaseModel):
    sentence: str = Field(..., min_length=5, description="The natural language string for the event.")
    add_immediately: bool = Field(default=True, description="Whether to commit the parsed event directly.")

def execute_fantastical_applescript(event_data: dict):
    """
    Validates natural language event string before calling Fantastical via AppleScript.
    """
    try:
        # Validate task parameters using Pydantic v2
        validated_event = FantasticalEventSchema.model_validate(event_data)

        # Build the AppleScript statement
        immediate_flag = "with add immediately" if validated_event.add_immediately else ""
        applescript_code = f'''
        tell application "Fantastical"
            parse sentence "{validated_event.sentence}" {immediate_flag}
        end tell
        '''

        # In a real macOS env:
        # subprocess.run(["osascript", "-e", applescript_code], check=True)
        print("Successfully validated and formatted Applescript payload with Pydantic v2:")
        print(applescript_code.strip())
        return True
    except ValidationError as e:
        print("Pydantic Validation Error during event parsing:")
        raise e

# Example call from Claude 5.6
agent_input = {
    "sentence": "Technical Audit with Jules at 3pm on Friday /Work",
    "add_immediately": True
}
execute_fantastical_applescript(agent_input)
```

### Fantastical FastMCP 3.1 Connector
In early January 2027, you can use the FastMCP 3.1 connector to allow [Claude Code](../development_ops/claude-code.md) to manage your schedule:
```bash
# Example agent command via Claude Code
claude "What does my Friday afternoon look like in Fantastical? If I have a gap, schedule a 1h deep work session."
```

## Related tools / concepts
- [Apple Calendar](apple-calendar.md) — The underlying system database on macOS.
- [Fastmail](fastmail.md) — High-performance backend provider often used with Fantastical.
- [Microsoft To Do](microsoft-todo.md) — Task backend supported by Fantastical.
- [Google Calendar](google_calendar.md) — Another major backend provider.
- [Claude Code](../development_ops/claude-code.md) — CLI agent that can orchestrate Fantastical via MCP.
- [Radicale](../../services/radicale.md) — Self-hosted CalDAV backend alternative.
- [Gemma 4](../ai_knowledge/local_llms.md) — Local LLM used for privacy-preserving NLP parsing.
- **Licensing**: Proprietary subscription (Flexibits Premium) for full features.

## Sources / References
- [Flexibits Fantastical Official Site](https://flexibits.com/fantastical)
- [Fantastical Release Notes](https://flexibits.com/fantastical/releasenotes)
- [Fantastical FastMCP 3.1 specification](https://mcp-registry.com/flexibits/fantastical)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
