# Fantastical

## What it is
A premium calendar and tasks application for macOS, iOS, iPadOS, and watchOS, widely recognized for its best-in-class natural language processing and elegant design.

## What problem it solves
Simplifies event and task creation through natural language input (e.g., "Lunch with John at 1pm tomorrow at Blue Bottle") and provides a beautiful, unified interface for multiple calendar and task accounts.

## Where it fits in the stack
**Category**: Calendar & Tasks / Personal Productivity. It acts as the primary user interface (GUI) for the [Apple Calendar](apple-calendar.md) ecosystem and beyond.

## Typical use cases
- **Rapid Scheduling**: Creating complex events with alerts and locations using simple sentences.
- **Unified Management**: Managing iCloud, Google, Microsoft 365 (Graph), and Exchange accounts in one view.
- **Calendar Sets**: Automatically switching visible calendars based on location or Focus mode (e.g., hiding work calendars when at home).
- **Agentic Scheduling (2026)**: Using the **Fantastical MCP Connector** for [Claude Code](../development_ops/claude-code.md) to manage events via chat.

## Strengths
- **Superior Natural Language Parsing**: Handles complex recurring rules and attendee invites via text.
- **Flexibits Premium**: A single subscription that includes both Fantastical and Cardhop (contacts).
- **Ecosystem Integration**: Deep support for Apple-specific features like widgets, Menubar icon, and Handoff.
- **Advanced Features (v4.x)**: Support for combining events from [Reclaim.ai](https://reclaim.ai/) on Microsoft 365 accounts and native proposal management.

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
- If you require a local-first, open-source calendar client.

## Licensing and cost
- **Open Source**: No
- **Cost**: Paid (Subscription required for Premium features), Free (Basic)
- **Self-hostable**: No

## Getting started

### Installation
Fantastical is a client-side application. Install it via the Mac App Store or direct download from the Flexibits website.

```bash
# On macOS via Homebrew Cask
brew install --cask fantastical
```

### Hello-world example
After installation, open Fantastical and use the natural language parser (**Cmd+N**) to create your first event:
`Meeting with Jules at 2pm tomorrow /Work` (The `/Work` suffix automatically assigns it to the "Work" calendar).

## CLI examples
While Fantastical does not provide a dedicated CLI binary, it can be controlled on macOS using the `open` command and its custom URL scheme. This is ideal for integration with [n8n](../../services/n8n.md) or local automation scripts.

```bash
# Create a new event using natural language
open "x-fantastical3://parse?sentence=Lunch%20with%20Alice%20at%201pm"

# Create a task (reminder)
open "x-fantastical3://parse?sentence=todo%20Buy%20milk%20at%205pm"

# Navigate to a specific date in the calendar
open "x-fantastical3://show?date=2026-12-25"

# Search for a specific event
open "x-fantastical3://search?query=Batch%20109"
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

### Fantastical MCP Connector (Claude Code)
In May 2026, you can use the MCP connector to allow [Claude Code](../development_ops/claude-code.md) to manage your schedule:
```bash
# Example agent command
/ask "Claude, what does my Friday afternoon look like in Fantastical?"
```

## Related tools / concepts
- [Apple Calendar](apple-calendar.md) — The underlying system database.
- [Notion Calendar](notion-calendar.md) — Cross-platform alternative.
- [Morgen](morgen.md) — Privacy-focused alternative with task integration.
- [Cardhop](https://flexibits.com/cardhop) — Included contacts app for managing attendees.

## Sources / References
- [Flexibits Fantastical Official Site](https://flexibits.com/fantastical)
- [Fantastical Release Notes (v4.0.13)](https://flexibits.com/fantastical/releasenotes)
- [Fantastical URL Scheme Documentation](https://flexibits.com/fantastical-ios/help/integration)

## Contribution Metadata
- Last reviewed: 2026-05-30
- Confidence: high
