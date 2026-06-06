# Any.do

## What it is
A comprehensive task management and calendar app designed for individuals and teams, featuring a unique "WhatsApp" integration.

## What problem it solves
Simplifies life and work organization with a clean interface and the ability to turn chats into tasks directly from messaging apps.

## Where it fits in the stack
**Category**: Calendar & Tasks / Task Management

## Typical use cases
- Managing personal daily routines and household tasks.
- Team project management for small businesses.
- Turning WhatsApp messages into actionable tasks via their bot.

## Getting started
Any.do is available on all major platforms. For technical users, Any.do offers a public API and an official Zapier/Make integration for connecting with external services.

## Technical Examples

### Creating a Task (cURL)
Use the Any.do API to programmatically create tasks.

```bash
curl -X POST https://api.any.do/v1/tasks \
  -H "Authorization: Bearer $ANYDO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "priority": "High",
    "dueDate": "2026-06-01T12:00:00Z"
  }'
```

### Turning a Message into a Task (Python)
Simulating a simple hook that could be used with a messaging bot.

```python
import requests
import os

ANYDO_TOKEN = os.getenv("ANYDO_TOKEN")

def message_to_anydo_task(message_text):
    url = "https://api.any.do/v1/tasks"
    headers = {
        "Authorization": f"Bearer {ANYDO_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "title": f"From Chat: {message_text}",
        "status": "UNCHECKED"
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# Example usage
message_to_anydo_task("Don't forget to review the contract")
```

## Strengths
- **WhatsApp Integration**: Unique capability to manage tasks through WhatsApp.
- **Cross-App Sync**: Strong sync between tasks and calendar events.
- **Design**: One of the most visually appealing and intuitive task managers.

## Limitations
- **Complexity at Scale**: Can feel a bit cluttered as the volume of tasks grows.
- **Pricing**: Some advanced features require a relatively high monthly subscription.

## When to use it
- If you use WhatsApp as a primary communication channel for work or family.
- If you want a task manager that feels "approachable" rather than clinical.

## When not to use it
- For complex, multi-year engineering projects (consider Jira or Linear).
- If you need deep Markdown support in your tasks.

## Licensing and cost
- **Open Source**: No
- **Cost**: Freemium (Free for personal use; paid tiers for power users and teams)
- **Self-hostable**: No

## Related tools / concepts
- [TickTick](ticktick.md) — feature-rich task manager with built-in Pomo timer.
- [Todoist](todoist.md) — flexible task management with natural language input.
- [Microsoft To Do](microsoft-todo.md) — lightweight personal task manager from Microsoft.
- [Google Tasks](google-tasks.md) — simple task manager integrated with Google Workspace.
- [Habitica](../../services/habitica.md) — gamified task management.
- [Vikunja](../../services/vikunja.md) — open-source self-hosted task manager.
- [n8n](../../services/n8n.md) — automation for syncing tasks across platforms.

## Sources / References
- [Any.do Official Site](https://www.any.do/)

## Contribution Metadata
- Last reviewed: 2026-05-23
- Confidence: high
