# Microsoft To Do

## What it is
A cloud-based task management application developed by Microsoft, which allows users to manage their tasks from a smartphone, tablet, and computer.

## What problem it solves
Helps users stay organized and manage their day-to-day tasks with features like "My Day" and seamless integration with the Microsoft 365 ecosystem.

## Where it fits in the stack
**Category**: Calendar & Tasks / Task Management

## Typical use cases
- Managing daily personal and professional to-do lists.
- Capturing tasks from Outlook and Microsoft Teams.
- Shared list collaboration for projects or shopping.

## Strengths
- **Microsoft 365 Integration**: Seamlessly syncs with Outlook Tasks and flagged emails.
- **Cross-Platform**: Available on web, Windows, macOS, iOS, and Android.
- **My Day**: A unique focus feature that encourages daily planning from a clean slate.

## Limitations
- **Advanced Features**: Lacks complex project management features found in Todoist or TickTick (e.g., natural language dates are less robust).
- **Automation**: Third-party automation can be less intuitive compared to Todoist.

## When to use it
- If you are already a heavy user of Microsoft 365 (Outlook, Teams).
- If you want a simple, clean, and free task manager for daily use.

## When not to use it
- If you need advanced sub-tasking, complex filters, or deep TDD integration.
- If you prefer a platform-agnostic tool with more robust third-party integrations.

## Licensing and cost
- **Open Source**: No
- **Cost**: Free (with Microsoft account)
- **Self-hostable**: No

## Getting started

Microsoft To Do is primarily used via its web and mobile applications, but it can be accessed programmatically via the Microsoft Graph API.

1. **Account**: Sign in with a personal Microsoft account or a Microsoft 365 work/school account.
2. **Setup**: Create your first list and try the "My Day" feature to plan your tasks.
3. **Integration**: Enable "Flagged Email" in Settings to automatically create tasks from emails you flag in Outlook.

## CLI examples

While there is no official first-party CLI specifically for Microsoft To Do, you can interact with it using the **Microsoft Graph CLI** or unofficial community tools.

### Using Microsoft Graph CLI
```bash
# Login to Microsoft Graph
mgc login

# List your task lists
mgc users todo lists list --user-id me

# Create a new task in the default 'Tasks' list
mgc users todo lists tasks create --user-id me --todo-task-list-id <list-id> --body '{"title": "Complete documentation", "importance": "high"}'
```

### Unofficial Community CLI (todoist-style)
Tools like `microsoft-todo-cli` (Node.js based) provide a more streamlined experience.
```bash
# Install (community tool)
npm install -g microsoft-todo-cli

# Add a task
todo add "Review project proposal"
```

## API examples

The **Microsoft Graph API** is the primary way to programmatically manage To Do tasks.

### Create a Task (Python via msal)
```python
import requests

# Assuming you have an access token from MSAL
endpoint = "https://graph.microsoft.com/v1.0/me/todo/lists/<list-id>/tasks"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}
task_data = {
    "title": "Send weekly report",
    "categories": ["Work"],
    "dueDateTime": {
        "dateTime": "2024-05-25T12:00:00",
        "timeZone": "UTC"
    }
}

# response = requests.post(endpoint, headers=headers, json=task_data)
# print(response.json())
```

## Related tools / concepts
- [Todoist](todoist.md)
- [Outlook Calendar](outlook.md)
- [Google Calendar](google_calendar.md)

## Sources / References
- [Microsoft To Do Official Site](https://todo.microsoft.com/)

## Contribution Metadata
- Last reviewed: 2026-05-02
- Confidence: high
