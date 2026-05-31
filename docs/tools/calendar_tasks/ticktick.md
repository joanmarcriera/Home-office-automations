# TickTick

TickTick is a powerful, all-in-one task management app that integrates a calendar, Pomodoro timer, habit tracker, and Markdown notes. As of May 2026, it remains the most feature-dense choice for personal productivity, having added native AI transcription, summaries, and Model Context Protocol (MCP) support for AI agent integration.

## What it is
TickTick is a multi-platform productivity suite that consolidates essential tools into a single application. It is designed for individuals who want to manage their entire life—tasks, habits, focus, and schedule—without context switching between separate apps.

## What problem it solves
It reduces "app sprawl" and cognitive load by providing a unified interface for the Getting Things Done (GTD) methodology, Eisenhower Matrix prioritization, and time-blocking. It solves the fragmentation problem by keeping tasks and their associated calendar events and timers in one place.

## Where it fits in the stack
- **Category**: [Calendar & Tasks](../calendar_tasks/index.md) / Task Management
- **Layer**: Human-Facing Personal Intelligence

## Typical use cases
- **Unified GTD**: Capturing, clarifying, and organizing life and work tasks.
- **Time Blocking**: Dragging tasks onto the integrated calendar to schedule the day.
- **Habit Formation**: Tracking daily routines with the built-in Habit Tracker.
- **Deep Work**: Using the integrated Pomodoro timer with white noise and task-specific timers.
- **Eisenhower Matrix**: Visualizing task priority across four quadrants for better decision making.

## Strengths
- **Feature Density**: Includes calendar, timer, habits, and notes at a lower price point than competitors like Todoist + Fantastical.
- **AI Voice & Transcription**: Native ability to transcribe voice recordings into tasks and summarize meeting audio.
- **Persistent Reminders**: "Nag" alerts that continue until a task is completed or snoozed, excellent for high-priority items.
- **Superior Calendar**: Full multi-project calendar view (Month, Week, Day) built directly into the task manager.
- **MCP Integration**: Exposes task management tools to AI agents via the Model Context Protocol.

## Limitations
- **API Maturity**: The official public API remains less robust than Todoist's, often requiring community-maintained wrappers.
- **Closed Ecosystem**: Proprietary and not self-hostable.
- **Privacy**: No local-only mode; all data is synced to TickTick's servers.

## When to use it
- If you want a single app to handle tasks, habits, and time-boxing.
- If you find Todoist too minimalist or find the cost of a multi-app stack prohibitive.
- If you need persistent, aggressive reminders for task completion.

## When not to use it
- If you strictly require open-source or local-first data storage (see [Vikunja](../../services/vikunja.md)).
- If you need enterprise-level project management features with complex permission hierarchies.

## Licensing and cost
- **Open Source**: No
- **Cost**: Freemium. Pro subscription is ~$36/year (May 2026) and is required for calendar views and advanced filtering.
- **Self-hostable**: No

## Getting started

### Installation
TickTick is available on iOS, Android, macOS, Windows, Linux, and the Web. For automation, the `ticktick-py` library is the most popular community choice.

```bash
# Install the community Python client
pip install ticktick-py
```

### Hello World (Python)
```python
from ticktick.api import TickTickClient

# Initialize client (requires user credentials or OAuth)
client = TickTickClient('your_email', 'your_password')

# Create a task in the Inbox with a Pomodoro duration
task = client.task.builder(
    title='Record meeting summary',
    content='Use TickTick AI to transcribe the audio',
    priority=3 # High priority
)
client.task.create(task)
print(f"Task created: {task['title']}")
```

## CLI examples
While no official binary exists, you can use `curl` for automation via the Open API (V1).

```bash
# Get all projects
curl -X GET "https://api.ticktick.com/open/v1/project" \
  -H "Authorization: Bearer ${TICKTICK_ACCESS_TOKEN}"

# Create a task with natural language due date parsing (if supported by integration)
curl -X POST "https://api.ticktick.com/open/v1/task" \
  -H "Authorization: Bearer ${TICKTICK_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Clean the house tomorrow at 10am",
    "content": "Focus on the kitchen first"
  }'
```

## AI & Agent Integration

### AI Voice Add
Create tasks instantly by speaking. TickTick's AI will parse the due date, priority, and list automatically.

### TickTick MCP (Model Context Protocol)
TickTick can now be used as a tool for AI agents (like Claude Desktop). This allows agents to:
- `create_task`: Create a new task with specific parameters.
- `list_all_tasks`: Retrieve open tasks for context-aware planning.
- `get_project_by_id`: Fetch specific project data.

**Sample MCP Config (Claude Desktop):**
```json
"mcpServers": {
  "ticktick": {
    "command": "npx",
    "args": ["-y", "@alexarevalo.ai/mcp-server-ticktick"],
    "env": {
      "TICKTICK_ACCESS_TOKEN": "your_token_here"
    }
  }
}
```

## Related tools / concepts
- [Todoist](todoist.md) — The primary minimalist competitor.
- [Any.do](any-do.md) — Mobile-first task management.
- [Habitica](../../services/habitica.md) — Gamified task management.
- [Vikunja](../../services/vikunja.md) — Self-hosted open-source alternative.
- [Composio](https://composio.dev/toolkits/ticktick) — For advanced agentic toolsets.

## Links
- [Official Website](https://ticktick.com/)
- [TickTick Developer Portal](https://developer.ticktick.com/)
- [AI Features Overview](https://help.ticktick.com/articles/7444685542580551680)

## Backlog
- [x] Perform quarterly technical freshness audit (May 2026).

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-05-31

## Sources / References
- https://help.ticktick.com/articles/7444685542580551680
- https://2sync.com/blog/ticktick-vs-todoist
- https://composio.dev/toolkits/ticktick
- KnowledgeOps Triage (2026-05-31)
