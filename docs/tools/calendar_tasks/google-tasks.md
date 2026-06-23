# Google Tasks

## What it is
Google Tasks is a lightweight task management service integrated into Google Workspace. As of June 2026, it serves as a primary "Surface" for agentic task execution via the [Model Context Protocol (MCP 3.0)](../../knowledge_base/mcp.md) and the Google Graph API, enabling autonomous agents to manage to-do items across Gmail, Calendar, and mobile devices.

## What problem it solves
It provides a minimalist, centralized capture point for tasks within the Google ecosystem. It solves task fragmentation by allowing [Autonomous Agents](../agents/README.md) and users to convert emails or calendar events into actionable items that synchronize across all Google surfaces.

## Where it fits in the stack
**Category**: Calendar & Tasks / Task Management. It acts as the "Durable Task Layer" for Google-native agentic workflows, sitting between the [Inference Layer](../ai_knowledge/README.md) and the user's daily productivity interface.

## Typical use cases
- **Agentic Orchestration**: An agent like [Gemini Spark](../ai_knowledge/gemini.md) identifying a task in an email and creating it in Google Tasks.
- **Workflow Automation**: Using [n8n](../../services/n8n.md) to sync [GitHub Issues](../development_ops/github.md) to a personal Google Tasks list.
- **Contextual Capture**: Turning [Google Calendar](google_calendar.md) event follow-ups into tasks automatically.
- **Smart Reminders**: Programmatic creation of time-sensitive reminders via the [Google Workspace CLI](../automation_orchestration/google-workspace-cli.md).

## Strengths
- **Ecosystem Integration**: Native, deep integration with Gmail, Calendar, and Drive.
- **MCP 3.0 Support**: Fully compatible with the Google MCP server for direct tool-calling by LLMs.
- **Low Friction**: Minimalist interface optimized for rapid capture and completion.
- **Reliability**: Highly available service with robust synchronization across web and mobile.

## Limitations
- **Feature Set**: Lacks advanced project management features like subtask nesting (limited to one level), complex dependencies, or custom labels.
- **Collaboration**: Sharing task lists is limited compared to enterprise tools like [Todoist](todoist.md) or [TickTick](ticktick.md).
- **Formatting**: Limited support for rich text or Markdown in task notes.

## When to use it
- When you are deeply integrated into the Google Workspace ecosystem.
- For simple, personal to-do lists that require visibility in [Google Calendar](google_calendar.md).
- When building agents that need a low-latency, reliable task storage backend.

## When not to use it
- For complex team project management (use [Gitea](../../services/gitea.md) or [Linear](../enterprise/linear.md)).
- If you require advanced organization like tags, filters, or Kanban views.
- If your workflow is primarily Markdown-based (consider [Obsidian](../ai_knowledge/obsidian.md) or [Logseq](../ai_knowledge/logseq.md)).

## Getting started
1. **Access**: Open Google Tasks in the Gmail or Calendar sidebar.
2. **Setup API**: Enable the Google Tasks API in the [Google Cloud Console](https://console.cloud.google.com/).
3. **Agentic Use**: Configure the Google MCP server to allow your agent to read/write tasks.

## CLI examples

### Using Google Workspace CLI
```bash
# List all tasks in the default list
gworkspace tasks list

# Create a new task
gworkspace tasks create --title "Review architectural diagrams" --notes "Focus on MCP 3.0 implementation" --due "2026-07-01T10:00:00Z"
```

### Using MCP 3.0 (within an agent prompt)
```text
/call google_tasks.create_task(title="Renew home-office domain", notes="Check Google Domains status")
```

## API examples

### Python (Google API Client)
```python
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def create_google_task(title, notes=None):
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('tasks', 'v1', credentials=creds)

    task = {
        'title': title,
        'notes': notes
    }

    result = service.tasks().insert(tasklist='@default', body=task).execute()
    print(f"Task created: {result['title']} (ID: {result['id']})")
```

### Node.js (MCP Tool Definition)
```javascript
export const createTaskTool = {
  name: "google_tasks_create",
  description: "Create a new task in Google Tasks",
  parameters: {
    type: "object",
    properties: {
      title: { type: "string" },
      notes: { type: "string" }
    },
    required: ["title"]
  }
};
```

## Related tools / concepts
- [Google Calendar](google_calendar.md)
- [Todoist](todoist.md)
- [TickTick](ticktick.md)
- [n8n](../../services/n8n.md)
- [Google Workspace CLI](../automation_orchestration/google-workspace-cli.md)
- [Chronos MCP](../automation_orchestration/chronos-mcp.md)
- [Gemini](../ai_knowledge/gemini.md)
- [MCP 3.0](../../knowledge_base/mcp.md)
- [Microsoft To Do](microsoft-todo.md)

## Sources / References
- [Google Tasks Official Support](https://support.google.com/tasks/answer/7675772)
- [Google Tasks API Reference](https://developers.google.com/workspace/tasks)
- [Google Cloud Console](https://console.cloud.google.com/)

## Contribution Metadata
- Last reviewed: 2026-06-23
- Confidence: high
