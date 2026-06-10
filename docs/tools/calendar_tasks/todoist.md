# Todoist

## What it is
A popular task management application that helps individuals and teams organize, plan, and collaborate on projects. As of 2026, it features advanced AI capabilities through the **Ramble AI** voice engine and native Model Context Protocol (MCP) support.

## What problem it solves
Provides a simple yet powerful interface for capturing tasks, setting deadlines, and organizing work into projects and sub-tasks. It excels at natural language parsing, allowing users to schedule complex recurring tasks via text or voice.

## Where it fits in the stack
**Category**: Calendar & Tasks / Task Management

## Typical use cases
- **Daily task management**: Capture and organize personal work using the "Inbox" and "Today" views.
- **AI-assisted planning**: Use the **Ramble AI** voice-to-task feature for hands-free capture in 38+ languages.
- **Agentic workflows**: Connect Todoist to **Claude 4.7** or **GPT-5.5** via MCP to automate task sorting and breakdown.
- **Maintenance patterns**: Use recurring tasks for system health checks and routine admin.

## Strengths
- Clean, intuitive interface across all platforms (including Linux and wearables).
- Best-in-class natural language parsing for deadlines (e.g., "every second Thursday at 3pm").
- Two-way sync with Google Calendar and Reclaim.ai.
- **MCP Native**: Supports the Model Context Protocol for seamless integration with AI agents.

## Limitations
- Advanced features like reminders and filters require a Pro subscription.
- Lacks native Gantt charts or complex task dependencies (better for GTD, not heavy PM).

## When to use it
- For personal or small group task organization.
- When you need a fast, reliable way to capture and categorize tasks using natural language.
- If you want an AI agent to manage your todo list autonomously.

## When not to use it
- For complex software development projects with strict dependencies (prefer Jira or GitHub Issues).
- If you require a fully local-first or open-source solution (consider [Vikunja](../../services/vikunja.md)).

## Licensing and cost
- **Open Source**: No
- **Cost**: Freemium (Personal) / Paid (Pro/Business)
- **Self-hostable**: No

## Getting started
### Official Integration
Todoist offers native apps for all platforms. To integrate with AI tools:
1. Generate an API token in **Settings > Integrations > Developer**.
2. **Hello-world example**: Create a task via cURL:
   ```bash
   curl -X POST https://api.todoist.com/rest/v2/tasks \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"content": "Audit 2026 playbooks", "due_string": "tomorrow"}'
   ```

## CLI examples
> [!NOTE]
> While there is an official CLI, many users prefer the **Todoist MCP Server** for agentic use cases.

### Using the Official CLI
```bash
# Install (macOS/Linux)
brew install todoist-cli

# List tasks due today
todoist list --filter "today"

# Add a task
todoist add "Check server logs every morning" --date "every day"
```

## API examples
Todoist provides a stable REST API v2 for developers.

### Create a Task (Python)
```python
import requests

API_TOKEN = "YOUR_TODOIST_API_TOKEN" # Standardized naming
API_URL = "https://api.todoist.com/rest/v2/tasks"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "content": "Prepare project update",
    "due_string": "Friday at 5pm",
    "priority": 4
}

response = requests.post(API_URL, headers=headers, json=data)
print(response.json())
```

### Model Context Protocol (MCP) Integration
Integrate Todoist with agents like **Claude 4.7** or **Llama 4 Maverick** using an MCP server.

**Recommended Server**: `Doist/todoist-ai` (Official) or `shockedrope/todoist-mcp` (Community).

**Tools available**:
- `create_task`: Create tasks with full natural language support.
- `list_tasks`: Fetch tasks filtered by project, label, or date.
- `update_task`: Modify existing entries.
- `get_stats`: View productivity metrics and completed task counts.

## Related tools / concepts
- [Reclaim.ai](reclaim.md) — Automatically time-blocks Todoist tasks.
- [Akiflow](akiflow.md) — Aggregates tasks into a unified command center.
- [Vikunja](../../services/vikunja.md) — Self-hosted alternative.
- [n8n](../../services/n8n.md) — Used for advanced Todoist automations.
- [Google Calendar](google_calendar.md) — Two-way sync partner.

## Sources / References
- [Official Website](https://todoist.com/)
- [Todoist API v2 Documentation](https://developer.todoist.com/rest/v2/)
- [Todoist 2026 Changelog](https://www.todoist.com/help/articles/2026-changelog)
- [Todoist AI MCP Server](https://github.com/Doist/todoist-ai)

## Contribution Metadata
- Last reviewed: 2026-06-08
- Confidence: high
