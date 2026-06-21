# Fantastical

## What it is
A premium calendar and tasks application for macOS, iOS, iPadOS, and watchOS, widely recognized for its best-in-class natural language processing and elegant design. In June 2026, it serves as a primary interface for **Agentic Calendar Orchestration**.

## What problem it solves
Simplifies event and task creation through natural language input and provides a beautiful, unified interface for multiple calendar and task accounts. It solves the "scheduling friction" by allowing users to speak or type their intent without navigating complex forms.

## Where it fits in the stack
**Category**: Calendar & Tasks / Personal Productivity. It acts as the primary user interface (GUI) for the [Apple Calendar](apple-calendar.md) ecosystem, Google Calendar, and Microsoft 365, often enhanced by **Claude 4.8** or **GPT-5.5** via MCP 3.0.

## Typical use cases
- **Rapid Scheduling**: Creating complex events with alerts and locations using simple sentences.
- **Unified Management**: Managing iCloud, Google, Microsoft 365 (Graph), and Exchange accounts in one view.
- **Calendar Sets**: Automatically switching visible calendars based on location or Focus mode.
- **Agentic Scheduling (June 2026)**: Using the **Fantastical MCP 3.0 Connector** for [Claude Code](../development_ops/claude-code.md) to manage events via chat.

## Strengths
- **Superior Natural Language Parsing**: Handles complex recurring rules and attendee invites via text.
- **Flexibits Premium**: Includes both Fantastical and Cardhop (contacts) for a unified productivity suite.
- **Ecosystem Integration**: Deep support for Apple-specific features like widgets, Menubar icon, and Handoff.
- **MCP 3.0 Support**: Native integration with agentic frameworks, allowing AI to read/write events with user-in-the-loop verification.

## Limitations
- **Subscription-Based**: Most core productivity features require a Flexibits Premium subscription.
- **Apple Ecosystem Exclusive**: No native support for Windows or Android.
- **Proprietary**: Not an open-source solution; data is synced via third-party providers or iCloud.

## When to use it
- If you are a power user on Apple devices and value speed of entry.
- When you need to manage multiple diverse calendar accounts (Work/Personal) seamlessly.
- If you want a more intuitive, visual way to interact with your schedule.

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
open "x-fantastical3://show?date=2026-12-25"
```

## API examples
Fantastical offers deep integration on macOS via **AppleScript** and a robust URL scheme.

### AppleScript (macOS)
This pattern allows agents to interact with Fantastical directly.
```applescript
tell application "Fantastical"
    -- Parse and add an event immediately without opening the window
    parse sentence "Technical Audit at 3pm on Friday" with add immediately
end tell
```

### Fantastical MCP 3.0 Connector
In June 2026, you can use the MCP connector to allow [Claude Code](../development_ops/claude-code.md) to manage your schedule:
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
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Patterns for autonomous scheduling.

## Licensing and cost
- **Open Source**: No
- **Cost**: Paid (Subscription required for Premium features), Free (Basic)
- **Self-hostable**: No

## Sources / References
- [Flexibits Fantastical Official Site](https://flexibits.com/fantastical)
- [Fantastical Release Notes (June 2026)](https://flexibits.com/fantastical/releasenotes)
- [Fantastical URL Scheme Documentation](https://flexibits.com/fantastical-ios/help/integration)

## Contribution Metadata
- Last reviewed: 2026-06-21
- Confidence: high
