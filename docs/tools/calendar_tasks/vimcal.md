# Vimcal

## What it is
Vimcal is a high-speed calendar application designed for power users, featuring keyboard shortcuts, time zone coordination, and scheduling links. It aims to be the "fastest calendar in the world" through a command-palette-driven interface. It is a proprietary SaaS product with a paid subscription model and no free tier for advanced features.

## What problem it solves
It reduces the time spent on manual scheduling and coordination by streamlining event creation and availability sharing. It eliminates the friction of navigating traditional, mouse-heavy calendar interfaces, especially for users managing global teams across multiple time zones.

## Where it fits in the stack
**Calendar & Tasks**. It serves as the primary frontend for power users who manage complex schedules across [Google Calendar](google_calendar.md) and [Outlook](outlook.md).

## Typical use cases
- **Fast Event Creation**: Using natural language to book meetings in seconds.
- **Global Coordination**: Managing meetings across multiple time zones with a specialized horizontal view.
- **Availability Snippets**: Quickly sharing free slots with collaborators without sending a link.
- **Executive Scheduling**: Using the "Scheduling Assistant" to find mutual openings for large internal teams.
- **Agentic Scheduling**: Bridging Vimcal with AI assistants like **Claude 4.8** by using the [Google Calendar MCP Server](../automation_orchestration/mcp.md) to manage underlying data.

## Strengths
- **Keyboard-first navigation**: Inspired by Vim, allowing for extremely fast interaction.
- **Exceptional Time Zone Management**: Real-time conversion and visualization for global teams.
- **Natural Language Processing (NLP)**: High-accuracy event parsing for title, date, and location.
- **Distraction-Free UI**: Minimalist design focused on speed and efficiency.

## Limitations
- **Proprietary SaaS**: Closed-source model requiring a paid subscription.
- **No Public API**: As of June 2026, Vimcal remains a closed platform for direct developer integration.
- **Limited Task Integration**: Less focus on deep task management compared to specialized tools like [Akiflow](akiflow.md).

## When to use it
- If you spend a significant portion of your day in your calendar and want to minimize friction.
- If you frequently coordinate meetings across global time zones.
- If you prefer a keyboard-driven workflow for administrative tasks.

## When not to use it
- If you need a free or self-hosted calendar solution.
- If you require deep integration with local task databases or custom automation scripts.

## Getting started

### Installation
Vimcal is primarily a desktop and web application. Download the client from [Vimcal.com](https://www.vimcal.com/).

### Basic Setup
1. Sign up and connect your primary [Google Calendar](google_calendar.md) or [Outlook](outlook.md).
2. Use the command palette (`Cmd+K` on Mac, `Ctrl+K` on Windows) to start typing.
3. **Natural Language Example**: Type "Coffee with Max at 10am tomorrow at Starbucks" and press Enter. The NLP will automatically parse all details.

## CLI examples

### Raycast / Alfred Integration
While Vimcal does not have an official CLI, power users use launcher extensions:
```bash
# Raycast command example
raycast "Create Vimcal Event" --title "Review Q3 Roadmap" --time "2pm"
```

### Application Shortcuts
- `F`: Toggle "Free Slots" mode.
- `S`: Share availability snippets.
- `A`: Open the AI Scheduling Assistant.

## API examples

### Underlying Provider Automation (Google Calendar)
Since Vimcal lacks a public API, automation is performed via the provider:
```python
# Example using the Google Calendar API
from googleapiclient.discovery import build
service = build('calendar', 'v3', credentials=creds)

event = {
  'summary': 'Vimcal Sync',
  'start': {'dateTime': '2026-06-28T10:00:00Z'},
  'end': {'dateTime': '2026-06-28T11:00:00Z'}
}
service.events().insert(calendarId='primary', body=event).execute()
```

### MCP Integration
Use the [Google Calendar MCP Server](../automation_orchestration/mcp.md) to allow agents to interact with Vimcal data:
```bash
npx @modelcontextprotocol/server-google-calendar
```

## Related tools / concepts
- [Notion Calendar](notion-calendar.md) — High-speed, integrated calendar from Notion.
- [Amie](amie.md) — Personal and professional calendar-task hybrid.
- [Morgen](morgen.md) — Unified calendar and task manager.
- [Akiflow](akiflow.md) — For deep task and calendar consolidation.
- [Reclaim](reclaim.md) — AI-driven scheduling for teams.
- [Motion](motion.md) — AI calendar for automatic rescheduling.
- [Todoist](todoist.md) — Leading task management integration.
- [Google Calendar](google_calendar.md) — The underlying data provider.

## Sources / references
- [Vimcal Official Website](https://www.vimcal.com/)
- [Vimcal Scheduling Assistant Guide](https://docs.vimcal.com/vimcalea/scheduling-assistant)
- [Vimcal Keyboard Shortcuts](https://www.vimcal.com/shortcuts)
- [Llama 4 Maverick productivity benchmarks (June 2026)](https://www.vimcal.com/blog/2026/05/productivity-with-llama-4/)

## Contribution Metadata
- Last reviewed: 2026-06-28
- Confidence: high
