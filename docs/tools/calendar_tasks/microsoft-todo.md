# Microsoft To Do

## What it is
A cloud-based task management application developed by Microsoft, serving as the central hub for individual task tracking within the Microsoft 365 ecosystem.

## What problem it solves
Helps users stay organized and manage their day-to-day tasks with features like "My Day" and seamless, native synchronization with Outlook, Teams, and Microsoft Planner.

## Where it fits in the stack
**Category**: Calendar & Tasks / Task Management. It acts as the personal task layer for the enterprise-grade Microsoft 365 stack.

## Typical use cases
- **Personal Productivity**: Managing daily to-do lists via the "My Day" smart list.
- **Enterprise Integration**: Capturing tasks directly from flagged Outlook emails and Microsoft Teams chats.
- **Shared Collaboration**: Managing family shopping lists or small team project tasks with real-time sync.
- **Agentic Automation (2026)**: Using [Copilot for Microsoft 365](https://www.microsoft.com/en-us/microsoft-365/copilot) to summarize, prioritize, and create tasks via natural language.

## Strengths
- **Ecosystem Synergy**: Deep integration with Outlook Tasks, Flagged Emails, and Microsoft Planner.
- **My Day Focus**: A unique feature that resets every morning, encouraging intentional daily planning.
- **Cross-Platform Accessibility**: Consistent experience across Web, Windows, macOS, iOS, and Android.
- **No-Code Automation**: Extensive support via **Power Automate** (including natural language flow generation as of May 2026).

## Limitations
- **Power User Gaps**: Lacks complex features found in [Todoist](todoist.md) or [TickTick](ticktick.md) like robust natural language date parsing for all fields.
- **Project Complexity**: Not suitable for large-scale project management (use Microsoft Planner or Azure DevOps for these cases).
- **Privacy**: Tasks are stored within the Microsoft cloud, which may not meet "local-first" or strict privacy requirements.

## When to use it
- If you are already a heavy user of the Microsoft 365 ecosystem.
- When you want a simple, clean, and free task manager that "just works" with your work email.
- For users who prefer a daily "fresh start" approach to task management.

## When not to use it
- If you need advanced sub-tasking, complex custom filters, or markdown support.
- If you require a privacy-focused, encrypted, or self-hosted task manager (consider [Vikunja](../../services/vikunja.md)).
- For complex software development workflows (use [Gitea](../../services/gitea.md) issues or GitHub).

## Licensing and cost
- **Open Source**: No
- **Cost**: Free (with Microsoft account); included with Microsoft 365 subscriptions.
- **Self-hostable**: No

## Getting started
Microsoft To Do is primarily used via its web and mobile applications.

1. **Sign In**: Use a personal Microsoft account or a Microsoft 365 work/school account.
2. **Setup 'My Day'**: Click the ☀️ icon to start your day and add tasks from your main list or suggestions.
3. **Enable Flagged Email**: Go to Settings > Connected Apps and toggle "Flagged Email" to auto-sync tasks from Outlook.

## CLI examples
While there is no first-party CLI, you can interact with Microsoft To Do using the **Microsoft Graph CLI** or community tools.

### Microsoft Graph CLI
```bash
# Login to Microsoft Graph
mgc login

# List all your To Do task lists
mgc users todo lists list --user-id me

# Create a high-priority task in a specific list
mgc users todo lists tasks create --user-id me --todo-task-list-id <list-id> \
  --body '{"title": "Verify Batch 109 Metadata", "importance": "high"}'
```

## API examples
The **Microsoft Graph API (v1.0)** is the standard interface for programmatically managing tasks.

### Create a Task (Python)
This pattern is used by [n8n](../../services/n8n.md) or custom agents to sync tasks from external sources.
```python
import requests

# Access token should have 'Tasks.ReadWrite' scope
endpoint = "https://graph.microsoft.com/v1.0/me/todo/lists/<list-id>/tasks"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

task_data = {
    "title": "Document May 2026 Graph API Patterns",
    "categories": ["Work", "Documentation"],
    "dueDateTime": {
        "dateTime": "2026-05-30T17:00:00",
        "timeZone": "UTC"
    },
    "reminderDateTime": {
        "dateTime": "2026-05-30T09:00:00",
        "timeZone": "UTC"
    }
}

response = requests.post(endpoint, headers=headers, json=task_data)
if response.status_code == 201:
    print(f"Task Created: {response.json()['id']}")
```

### Power Automate Integration
In May 2026, you can use "Natural Language to Flow" to create complex triggers:
- **Prompt**: "When I receive a high-priority email from my boss about 'Project X', create a task in my 'Project X' list in To Do with a reminder for tomorrow morning."
- **Result**: Power Automate generates the logic and connects the Outlook and To Do connectors automatically.

## Related tools / concepts
- [Todoist](todoist.md) — Feature-rich alternative.
- [TickTick](ticktick.md) — Alternative with integrated calendar and Pomodoro.
- [Microsoft Planner](https://tasks.office.com/) — For team project management.
- [Outlook](outlook.md) — The underlying mail and calendar provider.

## Sources / References
- [Microsoft To Do Official Site](https://todo.microsoft.com/)
- [Microsoft Graph API Documentation (Tasks)](https://learn.microsoft.com/en-us/graph/api/resources/todo-overview)
- [Power Automate May 2026 Feature Update](https://www.microsoft.com/en-us/power-platform/blog/2026/05/14/whats-new-in-power-platform-may-2026-feature-update/)

## Contribution Metadata
- Last reviewed: 2026-05-30
- Confidence: high
