# Microsoft To Do

## What it is
A cloud-based task management application developed by Microsoft, serving as the central hub for individual task tracking within the Microsoft 365 ecosystem. In June 2026, it features deep **Agentic Calendar Orchestration** via **GPT-5.5** and **Claude 4.8**.

## What problem it solves
Helps users stay organized and manage their day-to-day tasks with features like "My Day" and seamless, native synchronization with Outlook, Teams, and Microsoft Planner. It solves the fragmentation of enterprise tasks by centralizing them in a single, mobile-first interface.

## Where it fits in the stack
**Category**: Calendar & Tasks / Task Management. It acts as the personal task layer for the enterprise-grade Microsoft 365 stack, bridging the gap between communication (Teams/Outlook) and execution.

## Typical use cases
- **Personal Productivity**: Managing daily to-do lists via the "My Day" smart list.
- **Enterprise Integration**: Capturing tasks directly from flagged Outlook emails and Microsoft Teams chats.
- **Shared Collaboration**: Managing family shopping lists or small team project tasks with real-time sync.
- **Agentic Automation (June 2026)**: Using **Copilot 2.0** to autonomously prioritize, schedule, and execute tasks via natural language.

## Strengths
- **Ecosystem Synergy**: Deep integration with Outlook Tasks, Flagged Emails, and Microsoft Planner.
- **My Day Focus**: A unique feature that resets every morning, encouraging intentional daily planning.
- **Cross-Platform Accessibility**: Consistent experience across Web, Windows, macOS, iOS, and Android.
- **Agentic Scheduling**: Native support for **Agentic Calendar Orchestration**, allowing AI agents to move tasks between To Do and Outlook Calendar based on priority.

## Limitations
- **Power User Gaps**: Lacks complex features found in [Todoist](todoist.md) like robust natural language date parsing for all fields.
- **Project Complexity**: Not suitable for large-scale project management (use Microsoft Planner or Azure DevOps).
- **Privacy**: Tasks are stored within the Microsoft cloud, which may not meet "local-first" or strict privacy requirements.

## When to use it
- If you are already a heavy user of the Microsoft 365 ecosystem.
- When you want a simple, clean, and free task manager that "just works" with your work email.
- For users who prefer a daily "fresh start" approach to task management.

## When not to use it
- If you need advanced sub-tasking, complex custom filters, or markdown support.
- If you require a privacy-focused, encrypted, or self-hosted task manager (consider [Vikunja](../../services/vikunja.md)).
- For complex software development workflows (use [Gitea](../../services/gitea.md) issues or GitHub).

## Getting started
Microsoft To Do is primarily used via its web and mobile applications.

### Setup
1. **Sign In**: Use a personal Microsoft account or a Microsoft 365 work/school account.
2. **Setup 'My Day'**: Click the ☀️ icon to start your day and add tasks from your main list or suggestions.
3. **Enable Flagged Email**: Go to Settings > Connected Apps and toggle "Flagged Email" to auto-sync tasks from Outlook.

## CLI examples
While there is no first-party CLI, you can interact with Microsoft To Do using the **Microsoft Graph CLI**.

```bash
# Login to Microsoft Graph
mgc login

# List all your To Do task lists
mgc users todo lists list --user-id me

# Create a high-priority task in a specific list (June 2026 Syntax)
mgc users todo lists tasks create --user-id me --todo-task-list-id <list-id> \
  --body '{"title": "Verify Batch 120 Metadata", "importance": "high"}'
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
    "title": "Document June 2026 Graph API Patterns",
    "categories": ["Work", "Documentation"],
    "dueDateTime": {
        "dateTime": "2026-06-30T17:00:00",
        "timeZone": "UTC"
    }
}

response = requests.post(endpoint, headers=headers, json=task_data)
print(f"Task Created: {response.json()['id']}")
```

## Related tools / concepts
- [Todoist](todoist.md) — Feature-rich alternative.
- [TickTick](ticktick.md) — Alternative with integrated calendar and Pomodoro.
- [Fantastical](fantastical.md) — Premium client that supports Microsoft To Do tasks.
- [Vikunja](../../services/vikunja.md) — Self-hosted, privacy-first alternative.
- [Outlook](outlook.md) — The underlying mail and calendar provider.
- [n8n](../../services/n8n.md) — For automating task creation via AI workflows.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — The strategy behind Microsoft's Copilot orchestration.

## Licensing and cost
- **Open Source**: No
- **Cost**: Free (with Microsoft account); included with Microsoft 365 subscriptions.
- **Self-hostable**: No

## Sources / References
- [Microsoft To Do Official Site](https://todo.microsoft.com/)
- [Microsoft Graph API Documentation (Tasks)](https://learn.microsoft.com/en-us/graph/api/resources/todo-overview)
- [Power Automate June 2026 Feature Update](https://www.microsoft.com/en-us/power-platform/blog/2026/06/14/whats-new-in-power-platform-june-2026-feature-update/)

## Contribution Metadata
- Last reviewed: 2026-06-21
- Confidence: high
