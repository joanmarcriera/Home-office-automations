# Motion

## What it is
An all-in-one productivity platform that utilizes artificial intelligence to automatically build a daily schedule based on tasks, meetings, and project deadlines.

## What problem it solves
Motion eliminates the cognitive overhead of manual scheduling. It solves the "planning fallacy" by dynamically reconfiguring a user's calendar when new priorities emerge or meetings are added, ensuring that deadlines are met without constant manual intervention.

## Where it fits in the stack
**Category**: Calendar & Tasks / AI Productivity
Motion acts as an intelligent orchestration layer between traditional calendars (Google, Outlook) and task management, often serving as the primary interface for autonomous agents like Claude 4.8 Opus to manage a user's time.

## Typical use cases
- **Automated Daily Planning**: Generating a daily agenda that prioritizes deep work and meeting preparation.
- **Dynamic Resource Allocation**: For teams, automatically distributing work based on individual availability and project priority.
- **Intelligent Meeting Booking**: Providing booking links that only show availability if it doesn't conflict with high-priority task deadlines.

## Strengths
- **Autonomous Rescheduling**: Automatically shifts tasks to the next available slot if a meeting runs over or a new one is booked.
- **Deep Calendar Integration**: Two-way sync with Google and Outlook ensures a single source of truth for time.
- **Project Awareness**: Tasks are not just isolated items but part of broader projects with their own timelines.
- **Time Blocking**: Encourages focused work by automatically creating time blocks for assigned tasks.

## Limitations
- **High Subscription Cost**: Significantly more expensive than traditional task managers like Todoist.
- **Learning Curve**: The "AI-first" approach requires users to trust the system and properly set task parameters (duration, priority).
- **Manual Control**: Users who prefer absolute manual control over every minute of their day may find the automation restrictive.

## When to use it
- For professionals with high-velocity schedules and frequent meeting interruptions.
- When you have more tasks than time and need help prioritizing what to work on next.
- For teams that want to reduce the administrative burden of work coordination.

## When not to use it
- If your schedule is relatively static and predictable.
- When operating on a tight budget where a free or lower-cost tool would suffice.
- If you require a local-only or privacy-focused offline task manager.

## Getting started
Motion is a SaaS platform accessible via web, macOS, Windows, iOS, and Android. It integrates deeply with Google Workspace and Microsoft 365. Developers and agents can use the Motion API to programmatically inject tasks and manage schedules.

## CLI examples
While there is no official CLI, the Motion API is highly accessible via standard terminal tools like `curl`.

```bash
# Create a new high-priority task in a specific workspace
curl -X POST https://api.usemotion.com/v1/tasks \
  -H "X-API-Key: $MOTION_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Analyze GPT-5.5 performance metrics",
    "dueDate": "2026-06-25T17:00:00Z",
    "duration": 90,
    "priority": "ASAP",
    "workspaceId": "WS_123456"
  }'
```

## API examples
The Motion API allows for sophisticated integrations with AI workflows, such as automatically creating tasks from meeting transcripts processed by Claude 4.8 Opus.

```python
import requests
import os

MOTION_API_KEY = os.getenv("MOTION_API_KEY")

def create_motion_task(name, duration_mins, priority="Normal"):
    """
    Creates a task in Motion, often triggered by an AI agent's reasoning.
    """
    url = "https://api.usemotion.com/v1/tasks"
    headers = {
        "X-API-Key": MOTION_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "name": name,
        "duration": duration_mins,
        "priority": priority,
        "workspaceId": os.getenv("MOTION_WORKSPACE_ID"),
        "autoSchedule": True
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# Example: Task generated from a project review session
new_task = create_motion_task(
    name="Update Documentation for June 2026 Audit",
    duration_mins=120,
    priority="High"
)
print(f"Task created: {new_task['id']}")
```

## Related tools / concepts
- [Reclaim.ai](reclaim.md) — smart scheduling with a focus on habits and time blocking.
- [Akiflow](akiflow.md) — central command for tasks and calendar with manual scheduling.
- [Sunsama](sunsama.md) — ritual-based daily planning with deep task integrations.
- [Google Calendar](google_calendar.md) — the foundational backend for many scheduling tools.
- [Any.do](any-do.md) — simple task management with strong messaging integration.
- [Todoist](todoist.md) — lightweight, natural-language task manager.
- [n8n](../../services/n8n.md) — automation platform for custom Motion task triggers.

## Sources / references
- [Motion Official Site](https://www.usemotion.com/)
- [Motion API Documentation](https://docs.usemotion.com/)
- [AI Scheduling Patterns](../../knowledge_base/patterns/agentic-workflows.md)

## Contribution Metadata
- Last reviewed: 2026-06-16
- Confidence: high
