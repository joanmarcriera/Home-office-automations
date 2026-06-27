# Reclaim.ai

## What it is
An AI-powered scheduling automation tool that syncs with Google Calendar and Microsoft Outlook to find the best time for tasks, habits, and meetings. Following its acquisition by **Dropbox** in July 2024, it has expanded its enterprise capabilities while remaining a favorite for individual power users.

## What problem it solves
Solves "calendar tetris" by automatically blocking time for deep work and habits while staying flexible for incoming meetings. It dynamically adjusts your schedule in real-time as priorities shift.

## Where it fits in the stack
**Category**: Calendar & Tasks / Scheduling Automation

## Typical use cases
- **Automated time blocking**: Connect tools like Linear or Todoist to auto-schedule tasks.
- **Habit protection**: Ensure recurring priorities (exercise, lunch) move instead of being deleted when meetings conflict.
- **Multi-calendar syncing**: Protect personal time by blocking it on your work calendar without revealing private details.
- **Smart Focus Time**: Defend deep work slots using adaptive protection based on weekly busyness.

## Strengths
- Dynamic rescheduling based on calendar priority.
- Excellent multi-calendar sync to protect personal time.
- Integration with task managers like Todoist, Linear, and Asana.
- **MCP 3.0 Native**: Can be controlled via AI agents using the Model Context Protocol.

## Limitations
- Autopilot can feel overwhelming for users who prefer manual control.
- Tasks do not always follow manual changes easily once "locked" by the AI.
- No native mobile app (as of June 2026; primarily web and desktop-focused).

## When to use it
- When you have a busy schedule and struggle to find time for deep work.
- When you need to sync multiple calendars (personal/work) across Google and Outlook.
- If you use AI agents like **Claude 4.8 Opus** (`claude-4-8-opus-20260528`) or **GPT-5.5** and want them to manage your schedule.

## When not to use it
- If you prefer manual, fixed-time scheduling without AI interference.
- If you use iCloud as your primary calendar (limited support).

## Getting started
To begin using Reclaim.ai:
1. Sign up at [Reclaim.ai](https://reclaim.ai/).
2. Connect your Google or Outlook calendars during onboarding.
3. **Hello-world example**: Create your first "Habit" (e.g., "Daily Review") by selecting **Habits** in the sidebar. Reclaim will find the best slot in your schedule.
4. **Agent Setup**: Connect Reclaim to your AI agent using an MCP 3.0 server (see below).

## CLI examples
> [!NOTE]
> Reclaim.ai does not offer an official first-party CLI.

The primary ways to interact with Reclaim from the command line or desktop are:
- **Raycast Extension**: Use `Create Task` or `View Schedule` directly from the Raycast palette.
- **MCP Server**: Use `npx -y @jj3ny/reclaim-mcp-server` to give your AI agent access via MCP 3.0.

## API examples
Reclaim provides a REST API for managing tasks and schedules.

### List all tasks (Python)
```python
import requests

API_TOKEN = "YOUR_RECLAIM_API_KEY" # Standardized naming
API_URL = "https://api.app.reclaim.ai/api/tasks"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

response = requests.get(API_URL, headers=headers)
tasks = response.json()

for task in tasks:
    print(f"{task['title']} - {task['status']}")
```

### Model Context Protocol (MCP 3.0) Integration
You can use the community-maintained MCP server to manage tasks via agents like **Claude 4.8** or **Llama 4 Maverick**.

**Tools exposed**:
- `reclaim_list_tasks`: View your current queue.
- `reclaim_create_task`: Add a task with duration and deadline.
- `reclaim_add_time`: Add more time to an existing task.

## Licensing and cost
- **Open Source**: No
- **Cost**: Freemium (Personal/Starter) / Paid (Business/Enterprise)
- **Self-hostable**: No (Cloud-native)

## Related tools / concepts
- [Google Calendar](google_calendar.md)
- [Microsoft Outlook](outlook.md)
- [Motion](motion.md)
- [Akiflow](akiflow.md)
- [Todoist](todoist.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [n8n](../../services/n8n.md)
- [Chronos MCP](../automation_orchestration/mcp.md)

## Sources / references
- [Reclaim.ai Official Site](https://reclaim.ai/)
- [Dropbox Acquisition Announcement](https://reclaim.ai/blog/dropbox-acquisition)
- [Reclaim MCP Server (GitHub)](https://github.com/jj3ny/reclaim-mcp-server)

## Contribution Metadata
- Last reviewed: 2026-06-28
- Confidence: high
