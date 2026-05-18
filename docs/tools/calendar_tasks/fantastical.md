# Fantastical

## What it is
A premium calendar and tasks app for macOS, iOS, and watchOS known for its natural language processing and elegant design.

## What problem it solves
Simplifies event creation through natural language input (e.g., "Lunch with John at 1pm tomorrow at Blue Bottle") and provides a beautiful, unified view of all calendars and tasks.

## Where it fits in the stack
**Category**: Calendar & Tasks / Personal Productivity

## Typical use cases
- Fast event creation via natural language
- Managing multiple calendar accounts (iCloud, Google, Exchange)
- View-focused daily planning

## Strengths
- Best-in-class natural language parsing
- Unified task management (reminders) within the calendar
- Beautiful widgets and Apple ecosystem integration

## Limitations
- Subscription-based model for many features
- Apple ecosystem exclusive (macOS, iOS, iPadOS)

## When to use it
- If you are a power user on Apple devices
- If you want a more intuitive way to add events than traditional forms

## When not to use it
- On Windows or Android
- If you prefer a free, basic calendar experience

## Licensing and cost
- **Open Source**: No
- **Cost**: Paid (Subscription), Free (Basic)
- **Self-hostable**: No

## Getting started
Fantastical is a client-side application. Install it via the Mac App Store or direct download from the Flexibits website.

**Installation:**
```bash
# On macOS via Homebrew Cask
brew install --cask fantastical
```

**Hello-world example:**
After installation, open Fantastical and use the natural language parser (Cmd+N) to create your first event:
`Meeting with Jules at 2pm tomorrow`

## CLI examples
While Fantastical does not provide a dedicated CLI binary, it can be controlled on macOS using the `open` command and its custom URL scheme:

```bash
# Create a new event using natural language
open "x-fantastical3://parse?sentence=Lunch%20with%20Alice%20at%201pm"

# Create a task (reminder)
open "x-fantastical3://parse?sentence=todo%20Buy%20milk%20at%205pm"

# Navigate to a specific date
open "x-fantastical3://show?date=2026-12-25"
```

## API examples
Fantastical offers deep integration on macOS via AppleScript and a robust URL scheme for cross-app automation.

**AppleScript (macOS):**
```applescript
tell application "Fantastical"
    parse sentence "Meeting with team at 10am tomorrow" with add immediately
end tell
```

**URL Scheme (Python Example):**
```python
import webbrowser
import urllib.parse

# Open Fantastical and start parsing an event
sentence = "Project Review at 2pm on Friday"
url = f"x-fantastical3://parse?sentence={urllib.parse.quote(sentence)}"
webbrowser.open(url)
```

## Related tools / concepts
- [Notion Calendar](notion-calendar.md)
- [Morgen](morgen.md)
- [Vimcal](vimcal.md)
- [Amie](amie.md)
- [Sunsama](sunsama.md)

## Sources / References
- [Flexibits Fantastical Official Site](https://flexibits.com/fantastical)
- [Fantastical URL Scheme Documentation](https://flexibits.com/fantastical-ios/help/integration)

## Contribution Metadata
- Last reviewed: 2026-05-02
- Confidence: high
