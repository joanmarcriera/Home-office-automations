# Notion Calendar

## What it is
A high-performance calendar app (formerly Cron) that serves as the unified time-management layer for Notion. As of 2026, it is the primary interface for **Notion Agents** and **Skills**, allowing for automated scheduling and database-driven time blocking. It is a closed-source product integrated into the Notion ecosystem.

## What problem it solves
Bridges the gap between notes/tasks in Notion and time management in a calendar. It provides a fast, keyboard-centric interface that synchronizes Google Calendar events with Notion database items in real-time.

## Where it fits in the stack
**Category**: Calendar & Tasks / Productivity Interface

## Typical use cases
- **Unified workspace view**: See Notion database entries (tasks, project milestones) alongside Google Calendar events.
- **High-speed scheduling**: Use keyboard shortcuts and scheduling links to manage a busy calendar.
- **Agentic time-blocking**: Use **Notion Agents** (powered by **Claude 4.8 Opus** or **GPT-5.5**) to automatically find slots for Notion tasks.
- **Cross-timezone coordination**: Manage global teams with integrated timezone columns.

## Strengths
- Deep Notion integration (linking pages to events, database sync).
- Fast, minimalist UI with excellent keyboard shortcuts (`Cmd+K` / `Ctrl+K`).
- Built-in scheduling links and "Share availability" features.
- **Worker-powered sync**: Leverages **Notion Workers** for reliable, server-side data synchronization.

## Limitations
- Primary backend is Google Calendar (limited support for other providers like iCloud).
- Deepest features require a Notion workspace.

## When to use it
- If you are a heavy Notion user who manages tasks within databases.
- If you value speed, keyboard shortcuts, and a minimalist design.
- If you want an integrated AI agent to help manage your time and Notion content.

## When not to use it
- If you don't use Notion (prefer [Reclaim.ai](reclaim.md) or [Fantastical](fantastical.md)).
- If you require native support for Microsoft Exchange (prefer [Outlook](outlook.md)).

## Getting started
1. Download the app from the [Notion website](https://www.notion.so/product/calendar).
2. Sign in with Google and connect your Notion workspace.
3. **Hello-world example**: Press `Cmd+K` and type "New event" to create a task.
4. **Agent Integration**: Enable "Notion Agent" in your workspace settings to allow AI-assisted scheduling.

## CLI examples
> [!NOTE]
> Notion Calendar does not offer an official CLI.

However, it supports a robust local **URI scheme** (`cron://`) for automation:
```bash
# Open a specific Notion page as a calendar event
open "cron://[email protected]&iCalUID=EVENT_ID&startDate=2026-06-12T10:00:00Z&title=Deep+Work"
```

## API examples
Notion Calendar's data is primarily managed via the **Notion API** and **Notion Workers**.

### Querying Notion Events (Python)
```python
import requests

API_TOKEN = "YOUR_NOTION_TOKEN" # Standardized naming
DATABASE_ID = "YOUR_DATABASE_ID"
API_URL = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Notion-Version": "2026-03-11",
    "Content-Type": "application/json"
}

# Fetch tasks with a 'Date' property
filter_data = {
    "filter": {
        "property": "Date",
        "date": { "is_not_empty": True }
    }
}

response = requests.post(API_URL, headers=headers, json=filter_data)
print(response.json())
```

## Model Context Protocol (MCP 3.0) Integration
Notion provides an official **Notion MCP Server** (`@suekou/mcp-notion-server` or official `Doist/todoist-ai` equivalent) that agents use to interact with the calendar via MCP 3.0.

**Agent Capabilities (via MCP):**
- `notion_find`: Search for pages and calendar entries.
- `notion_read_page`: Extract context from a specific event's linked Notion page.
- `notion_update_item`: Reschedule or modify Notion database entries.

## Related tools / concepts
- [Google Calendar](google_calendar.md) — The underlying backend.
- [Reclaim.ai](reclaim.md) — Intelligent time blocking for Notion users.
- [Vimcal](vimcal.md) — Keyboard-focused speed-calendar competitor.
- [n8n](../../services/n8n.md) — For complex database-to-calendar automation.
- [Chronos MCP](../automation_orchestration/chronos-mcp.md)
- [Akiflow](akiflow.md)
- [Todoist](todoist.md)

## Sources / references
- [Official Website](https://www.notion.so/product/calendar)
- [Notion 3.5 Developer Platform Release](https://www.notion.com/releases/2026-05-13)
- [Notion MCP Server (GitHub)](https://github.com/suekou/mcp-notion-server)

## Contribution Metadata
- Last reviewed: 2026-06-28
- Confidence: high
