# Notion Calendar (Cron)

## What it is
A high-performance calendar app (formerly Cron) that integrates deeply with Notion for a unified workspace experience.

## What problem it solves
Bridges the gap between notes/tasks in Notion and time management in a calendar, providing a fast, keyboard-centric interface.

## Where it fits in the stack
**Category**: Calendar & Tasks / Productivity Interface

## Typical use cases
- Unified view of Notion tasks and Google Calendar events
- High-speed scheduling for power users
- Managing multiple time zones

## Strengths
- Deep Notion integration (linking pages to events)
- Fast, minimalist UI with excellent keyboard shortcuts
- Built-in scheduling links

## Limitations
- Only supports Google Calendar (limited support for other providers)
- Mobile app availability varies by platform (iOS first)

## When to use it
- If you are a heavy Notion user
- If you value speed and keyboard shortcuts in your calendar workflow

## When not to use it
- If you don't use Notion
- If you require support for Microsoft Exchange or iCloud

## Licensing and cost
- **Open Source**: No
- **Cost**: Free
- **Self-hostable**: No

## Getting started
To get started with the application:
1. Download the desktop app for macOS or Windows from the [official website](https://www.notion.so/product/calendar).
2. Sign in with your Google account.
3. **Hello-world example**: Use `Cmd+K` (macOS) or `Ctrl+K` (Windows) to open the Command Bar and type "New event" to create your first entry.
4. Integrate with Notion via the "Notion" tab in settings to link database entries to calendar events.

## CLI examples
> [!NOTE]
> Notion Calendar does not currently offer an official CLI.

## API examples
Notion Calendar supports a local URI scheme (`cron://`) to open the app to specific events or views from external tools.

**Open a specific event**:
```bash
# Example URI to open an event by its iCalUID
open "cron://[email protected]&iCalUID=[email protected]&startDate=2026-06-12T10:00:00Z&title=Meeting"
```

**Minimal API schema**:
```text
cron://[accountEmail]&[iCalUID]&startDate=[ISO8601]&endDate=[ISO8601]&title=[Title]
```

## Technical details
Notion Calendar leverages the Notion API to fetch and display database items as calendar events. It supports:
- **Bi-directional linking**: Opening a Notion page from a calendar event and vice versa.
- **Global shortcuts**: Quick-add events from anywhere on your OS.
- **Overlapping timezones**: View multiple timezone columns simultaneously for easy scheduling.

## Related tools / concepts
- [Google Calendar](google_calendar.md) — The underlying backend for Notion Calendar.
- [Fantastical](fantastical.md) — Another high-end calendar with NLP.
- [Morgen](morgen.md) — Multi-calendar aggregator with task management.
- [Amie](amie.md) — "Joyful" productivity app combining calendar and tasks.
- [Akiflow](akiflow.md) — Deep task consolidation with calendar sync.
- [Vimcal](vimcal.md) — Keyboard-focused speed-calendar.
- [Reclaim](reclaim.md) — Intelligent time blocking for Notion users.
- [Todoist](todoist.md) — Often integrated with Notion for task management.

## Sources / References
- [Official Website](https://www.notion.so/product/calendar)
- [Notion Calendar Help Center](https://www.notion.so/help/category/notion-calendar)
- [Notion Calendar API & Connections](https://www.notion.so/help/notion-calendar-connections)

## Contribution Metadata
- Last reviewed: 2026-05-13
- Confidence: high
