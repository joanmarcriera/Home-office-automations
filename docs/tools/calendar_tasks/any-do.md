# Any.do

## What it is
A comprehensive task management and calendar platform designed for individuals and teams, known for its deep integration with messaging services and cross-platform accessibility.

## What problem it solves
Simplifies personal and professional organization by unifying tasks, calendars, and reminders into a single interface. It specifically addresses the "input friction" problem with its WhatsApp and Telegram integrations, allowing users to capture tasks directly from their primary communication channels.

## Where it fits in the stack
**Category**: Calendar & Tasks / Task Management
It serves as the execution layer for personal and small-team workflows, often integrated with AI agents like Claude 4.8 Opus for automated task ingestion and prioritization.

## Typical use cases
- **Personal Daily Planning**: Organizing household chores, shopping lists, and personal appointments.
- **Small Team Collaboration**: Managing shared projects, assigning tasks, and tracking progress in a unified workspace.
- **Omnichannel Task Capture**: Using the WhatsApp bot to turn fleeting thoughts or requests into actionable tasks without leaving the chat app.

## Strengths
- **Native Messaging Integration**: The "Any.do for WhatsApp" feature remains a market leader for chat-to-task conversion.
- **Visual Clarity**: Highly intuitive UI/UX that reduces cognitive load during planning.
- **Reliable Sync**: Near-instantaneous synchronization across mobile, web, and desktop clients.
- **Freemium Model**: Robust free tier suitable for many individual users.

## Limitations
- **Scaling Complexity**: While great for small teams, it lacks the advanced resource management found in enterprise tools like Jira.
- **API Rate Limits**: Standard tiers have constraints that may affect high-frequency agentic integrations.
- **Markdown Support**: Still trails behind tools like Obsidian or SilverBullet in terms of deep document formatting within tasks.

## When to use it
- If your primary workflow revolves around mobile messaging (WhatsApp/Telegram).
- When you need a "set it and forget it" task manager with minimal learning curve.
- For family or small team coordination where visual simplicity is prioritized over complex reporting.

## When not to use it
- For managing high-concurrency engineering sprints (use Linear or GitHub Projects).
- If you require a fully local, E2EE, or self-hosted solution (use Vikunja or AnyType).
- When deep hierarchical task structures and complex dependencies are mandatory.

## Getting started
Any.do is accessible via web browsers, mobile apps (iOS/Android), and desktop applications. For developers and AI agents, it provides a REST API and pre-built integrations with Zapier, Make, and the Model Context Protocol (MCP) for Claude 4.8 Opus and GPT-5.5.

## CLI examples
While Any.do does not have an official CLI, it can be interacted with via `curl` for quick task creation from the terminal.

```bash
# Create a task with a high priority using the Any.do API
curl -X POST https://api.any.do/v1/tasks \
  -H "Authorization: Bearer $ANYDO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Finalize Q3 roadmap with GPT-5.5",
    "priority": "High",
    "dueDate": "2026-06-20T09:00:00Z"
  }'
```

## API examples
The Any.do API allows for advanced automation, such as using Claude 4.8 Opus to parse unstructured notes into structured tasks.

```python
import requests
import os

# Configuration for the Any.do API
ANYDO_TOKEN = os.getenv("ANYDO_TOKEN")

def create_structured_task(parsed_content):
    """
    Creates a task in Any.do using data typically parsed by a reasoning model like Claude 4.8.
    """
    url = "https://api.any.do/v1/tasks"
    headers = {
        "Authorization": f"Bearer {ANYDO_TOKEN}",
        "Content-Type": "application/json"
    }

    # Payload structured from AI extraction
    payload = {
        "title": parsed_content.get("title"),
        "status": "UNCHECKED",
        "notes": parsed_content.get("description"),
        "priority": parsed_content.get("priority", "Normal")
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# Example: Task data extracted from a Claude 4.8 Opus session
task_data = {
    "title": "Review AI Audit results",
    "description": "Examine the 13-section compliance for the latest documentation batch.",
    "priority": "High"
}

create_structured_task(task_data)
```

## Related tools / concepts
- [TickTick](ticktick.md) — advanced task management with built-in Pomo timer.
- [Todoist](todoist.md) — natural language input for fast task entry.
- [Microsoft To Do](microsoft-todo.md) — integrated task management for Microsoft 365.
- [Google Tasks](google-tasks.md) — lightweight task list within the Google ecosystem.
- [Motion](motion.md) — AI-driven scheduling that automatically places tasks on the calendar.
- [Reclaim.ai](reclaim.md) — smart time blocking and habit tracking.
- [Vikunja](../../services/vikunja.md) — open-source, self-hosted task management alternative.

## Sources / references
- [Any.do Official Website](https://www.any.do/)
- [Any.do API Reference](https://api.any.do/)
- [WhatsApp Integration Overview](https://www.any.do/whatsapp/)

## Contribution Metadata
- Last reviewed: 2026-06-16
- Confidence: high
