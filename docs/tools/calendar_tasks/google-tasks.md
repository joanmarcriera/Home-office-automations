# Google Tasks

## What it is
Google Tasks is a simple task management service developed by Google that allows users to create, manage, and edit tasks across Google Workspace. It is deeply integrated with Gmail, Google Calendar, and Google Drive.

## What problem it solves
It provides a lightweight, focused way to capture to-do items without the complexity of full-scale project management tools. It solves the fragmentation of tasks by allowing users to turn emails into tasks directly within the Gmail interface.

## Where it fits in the stack
**Category**: Calendar & Tasks / Task Management. It serves as a personal capture point within the Google ecosystem, often used as a source or destination for automation workflows.

## Typical use cases
- Creating to-do lists from emails in Gmail.
- Scheduling tasks with due dates that appear in [Google Calendar](google_calendar.md).
- Quick capture of personal errands via the mobile app.
- Programmatic task creation from automation tools like [n8n](../../services/n8n.md).

## Strengths
- **Seamless Integration**: Native to Google Workspace (Gmail, Calendar).
- **Simplicity**: Minimalist interface focused on speed.
- **Cross-Platform**: Synchronizes across web and mobile apps.
- **API Support**: Robust REST API for developers.

## Limitations
- **Lacks Advanced Features**: No subtasks (nested only one level), labels, or complex dependencies.
- **Minimal Collaboration**: Difficult to share task lists with others compared to [Todoist](todoist.md) or [Any.do](any-do.md).
- **Formatting**: Very limited support for rich text or Markdown in task notes.

## When to use it
- When you are already heavily invested in the Google Workspace ecosystem.
- For simple personal tasks that don't require complex project management features.
- When you want your tasks to be visible alongside your events in [Google Calendar](google_calendar.md).

## When not to use it
- For team project management (use [Gitea](../../services/gitea.md) or similar).
- If you need deep Markdown support (consider [Obsidian](../ai_knowledge/obsidian.md) or [Logseq](../ai_knowledge/logseq.md)).
- If you require advanced task organization like filters, tags, and priority levels.

## API and Automation
Google Tasks is a popular target for "Smart Task" patterns.

### 1. Python SDK Example
Creating a task using the `google-api-python-client`.

```python
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def add_task(title, notes=None, due=None):
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('tasks', 'v1', credentials=creds)

    task = {
        'title': title,
        'notes': notes,
        'due': due # ISO 8601 format: 2026-06-01T12:00:00Z
    }

    result = service.tasks().insert(tasklist='@default', body=task).execute()
    print(f"Task created: {result['title']} (ID: {result['id']})")
```

### 2. n8n Integration
The **Google Tasks** node in [n8n](../../services/n8n.md) allows for:
- **Trigger**: New task created or task completed.
- **Action**: Create, Update, or List tasks.
- **Workflow**: Automatically create a task when a high-priority email is received in Gmail.

## Getting started
1. Access Google Tasks via the sidebar in Gmail or Google Calendar.
2. Download the mobile app for iOS or Android.
3. For developers, enable the Tasks API in the [Google Cloud Console](https://console.cloud.google.com/).

## Related tools / concepts
- [Google Calendar](google_calendar.md)
- [Todoist](todoist.md)
- [Any.do](any-do.md)
- [Microsoft To Do](microsoft-todo.md)
- [TickTick](ticktick.md)
- [n8n](../../services/n8n.md)
- [Home Assistant](../../services/home-assistant.md)
- [Google Workspace CLI](../automation_orchestration/google-workspace-cli.md)
- [Chronos MCP](../automation_orchestration/chronos-mcp.md)

## Sources / references
- [Google Tasks Official Overview](https://support.google.com/tasks/answer/7675772)
- [Google Tasks API Documentation](https://developers.google.com/workspace/tasks)

## Contribution Metadata
- Last reviewed: 2026-06-05
- Confidence: high
