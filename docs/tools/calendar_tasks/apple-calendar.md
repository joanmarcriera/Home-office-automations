# Apple Calendar

## What it is
Apple's native calendar application, deeply integrated into macOS, iOS, iPadOS, and watchOS.

## What problem it solves
Provides a seamless, synchronized scheduling experience for users within the Apple ecosystem, supporting iCloud, Exchange, and Google Calendar.

## Where it fits in the stack
**Category**: Calendar & Tasks / Ecosystem Native

## Typical use cases
- Personal and family scheduling on Apple devices.
- Managing shared iCloud calendars for household coordination.
- Quick event entry via Siri or natural language parsing.

## Strengths
- **Native Integration**: Deeply embedded in Apple's operating systems and hardware.
- **Privacy-First**: Strong privacy controls and end-to-end encryption for iCloud data.
- **Siri Support**: Excellent voice-to-task/calendar integration on Apple devices.

## Limitations
- **Ecosystem Lock-in**: Limited functionality and poor UI on non-Apple platforms.
- **Feature Set**: Less powerful for complex business time blocking compared to tools like Akiflow or Morgen.

## When to use it
- If you are fully committed to the Apple hardware ecosystem.
- For simple personal and family calendar management.

## When not to use it
- If you require advanced cross-platform collaborative features.
- If you use Android or Windows as your primary devices.

## Licensing and cost
- **Open Source**: No
- **Cost**: Free (Included with Apple ID)
- **Self-hostable**: No

## Getting started

### Installation
Apple Calendar is pre-installed on all Apple devices. For command-line access, `icalBuddy` is the community standard.

```bash
# Install icalBuddy via Homebrew
brew install ical-buddy
```

### Hello World (AppleScript)
You can create events directly from the terminal using the built-in `osascript` (AppleScript) engine.

```bash
osascript -e 'tell application "Calendar" to make new event at end of events of calendar "Calendar" with properties {summary:"Hello from CLI", start date:(current date), end date:((current date) + 3600)}'
```

## CLI examples
Using `icalBuddy` to query the local calendar database:

```bash
# List all events for today
icalBuddy eventsToday

# List all uncompleted tasks/reminders
icalBuddy uncompletedTasks

# List all available calendars
icalBuddy calendars
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
```python
from EventKit import EKEventStore, EKEntityType

store = EKEventStore.alloc().init()
store.requestAccessToEntityType_completion_(EKEntityTypeEvent, lambda granted, error: None)

calendars = store.calendarsForEntityType_(EKEntityTypeEvent)
for calendar in calendars:
    print(f"Calendar: {calendar.title()}")
```

## Related tools / concepts
- [Google Calendar](google_calendar.md)
- [Outlook Calendar](outlook.md)
- [Proton Calendar](proton_calendar.md)
- [EventKit Framework](https://developer.apple.com/documentation/eventkit)

## Sources / References
- [Apple Calendar Support](https://support.apple.com/calendar)
- [icalBuddy Homepage](https://hasseg.org/icalBuddy/)
- [AppleScript Language Guide](https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/introduction/ASL_intro.html)

## Contribution Metadata
- Last reviewed: 2026-05-02
- Confidence: high
