# Apple Calendar

## What it is
Apple's native calendar application, deeply integrated into macOS, iOS, iPadOS, and watchOS.

## What problem it solves
Provides a seamless, synchronized scheduling experience for users within the Apple ecosystem, supporting iCloud, Microsoft Exchange, Google Calendar, and CalDAV.

## Where it fits in the stack
**Category**: Calendar & Tasks / Ecosystem Native. It acts as the default system-level scheduler for all Apple hardware.

## Typical use cases
- **Personal & Family Scheduling**: Managing shared iCloud calendars for household coordination.
- **Cross-Platform Sync**: Synchronizing work (Exchange) and personal (iCloud/Google) calendars in a single view.
- **AI-Enhanced Entry (2026)**: Using 'Apple Intelligence' to automatically extract event details from Mail or Messages and suggest calendar additions.
- **Voice-First Productivity**: Creating and querying events hands-free via Siri (Agentic mode).

## Strengths
- **Native Integration**: Deeply embedded in Apple's operating systems and hardware (widgets, lock screen, Focus modes).
- **Privacy-First**: Strong privacy controls and end-to-end encryption for iCloud data; processing for 'Apple Intelligence' remains on-device or on Private Cloud Compute.
- **System-Wide Access**: Available to any app via the EventKit framework.
- **Zero Cost**: Included with every Apple ID without subscription fees.

## Limitations
- **Ecosystem Lock-in**: Limited functionality and poor UI on non-Apple platforms (web version is basic).
- **Power User Gaps**: Lacks native time-blocking features found in [Akiflow](akiflow.md) or [Morgen](morgen.md).
- **Limited Automation**: Advanced automation requires [AppleScript](#hello-world-applescript) or third-party CLI tools.

## When to use it
- If you are fully committed to the Apple hardware ecosystem.
- For simple personal and family calendar management.
- When on-device privacy is a primary requirement.

## When not to use it
- If you require advanced cross-platform collaborative features (use [Google Calendar](google_calendar.md) or [Outlook](outlook.md)).
- If you use Android or Windows as your primary devices.
- For complex project-based time tracking (consider [TickTick](ticktick.md) or [Todoist](todoist.md)).

## Licensing and cost
- **Open Source**: No
- **Cost**: Free (Included with Apple ID)
- **Self-hostable**: No (iCloud backend only)

## Getting started

### Installation
Apple Calendar is pre-installed on all Apple devices. For command-line access, `icalBuddy` is the community standard for reading data.

```bash
# Install icalBuddy via Homebrew (macOS)
brew install ical-buddy
```

### Hello World (AppleScript)
You can create events directly from the terminal using the built-in `osascript` (AppleScript) engine. This is useful for integration with [n8n](../../services/n8n.md) or local shell scripts.

```bash
osascript -e 'tell application "Calendar" to make new event at end of events of calendar "Home" with properties {summary:"Review Batch 109", start date:(current date), end date:((current date) + 3600)}'
```

## CLI examples
Using `icalBuddy` to query the local calendar database:

```bash
# List all events for today, separated by section
icalBuddy -sd -sc eventsToday

# List all uncompleted tasks/reminders (synced from Apple Reminders)
icalBuddy uncompletedTasks

# List events for the next 7 days from a specific calendar
icalBuddy -includeCals "Work" eventsFrom:(current date) to:((current date) + 7*86400)

# Filter events and output as a simple list for agentic consumption
icalBuddy -n -ea -ec eventsToday | grep -v "^$"
```

## API examples
The official way to interact with Apple Calendar programmatically is via the **EventKit** framework (Swift/Objective-C) or **AppleScript**.

### List Calendars (AppleScript)
```applescript
tell application "Calendar"
    set calendarList to name of every calendar
    return calendarList
end tell
```

### Accessing EventKit (Python via PyObjC)
This pattern is used by local agents like [Claude Code](claude-code.md) to read calendar data without a GUI.
```python
import objc
from EventKit import EKEventStore, EKEntityType

# Initialize Event Store
store = EKEventStore.alloc().init()

# Request access (requires TCC permission in macOS Settings)
store.requestAccessToEntityType_completion_(EKEntityTypeEvent, lambda granted, error: print(f"Granted: {granted}"))

# List available calendars
calendars = store.calendarsForEntityType_(EKEntityTypeEvent)
for calendar in calendars:
    print(f"Calendar: {calendar.title()} (Type: {calendar.type()})")
```

## Advanced Automation: Siri & Shortcuts
- **Siri Agent**: In May 2026, Siri can perform "Personal Context" lookups, e.g., "Siri, when is my next appointment with Dr. Smith?" using the local EventKit index.
- **Shortcuts.app**: Native integration for "Find Calendar Events" and "Add New Event" actions, which can be triggered via [Raycast](https://www.raycast.com/) or [Alfred](https://www.alfredapp.com/).

## Related tools / concepts
- [Google Calendar](google_calendar.md) — Cross-platform alternative.
- [Outlook Calendar](outlook.md) — Enterprise alternative.
- [Fantastical](fantastical.md) — Premium third-party client for Apple Calendar.
- [Amie](amie.md) — Social-first calendar integration.
- [EventKit Framework](https://developer.apple.com/documentation/eventkit) — Official developer API.

## Sources / References
- [Apple Calendar Support](https://support.apple.com/calendar)
- [Apple Intelligence Overview (2026)](https://www.apple.com/apple-intelligence/)
- [icalBuddy Homepage](https://hasseg.org/icalBuddy/)
- [AppleScript Language Guide](https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/introduction/ASL_intro.html)

## Contribution Metadata
- Last reviewed: 2026-05-30
- Confidence: high
