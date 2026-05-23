# Motion

## What it is
An all-in-one productivity tool that uses AI to build a daily schedule based on your tasks, meetings, and project deadlines.

## What problem it solves
Eliminates the need for manual scheduling by automatically prioritizing tasks and fitting them into your calendar gaps.

## Where it fits in the stack
**Category**: Calendar & Tasks / AI Productivity

## Typical use cases
- Automated daily planning
- Project management integrated with calendar
- Team-wide automated scheduling

## Strengths
- "Intelligent Calendar" that moves tasks automatically when meetings are added
- Integrated task and project management
- Meeting booking links that respect task deadlines

## Limitations
- Higher cost compared to other scheduling tools
- Can feel restrictive if you prefer full manual control

## When to use it
- When you have a high volume of tasks and meetings and lack time to plan
- For teams that want to automate work distribution

## When not to use it
- If you have a simple schedule with few tasks
- If you are on a tight budget

## Getting started
Motion is a SaaS platform. Users typically interact with it via the web, desktop, or mobile apps. For automation, Motion provides a robust REST API for task and schedule management.

## Technical Examples

### Creating a Task (cURL)
Motion provides a public API that allows you to create tasks from external triggers (e.g., a "high priority" email or a new GitHub issue).

```bash
curl -X POST https://api.usemotion.com/v1/tasks \
  -H "X-API-Key: $MOTION_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Review Project Proposal",
    "dueDate": "2026-06-05T17:00:00Z",
    "duration": 60,
    "priority": "ASAP",
    "workspaceId": "YOUR_WORKSPACE_ID"
  }'
```

### Fetching Tasks (Python)
Retrieve a list of tasks for a specific workspace to use in your own automation dashboards.

```python
import requests
import os

MOTION_API_KEY = os.getenv("MOTION_API_KEY")

def get_motion_tasks(workspace_id):
    url = f"https://api.usemotion.com/v1/tasks?workspaceId={workspace_id}"
    headers = {"X-API-Key": MOTION_API_KEY}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Example: List task names
tasks = get_motion_tasks("YOUR_WORKSPACE_ID")
for task in tasks['tasks']:
    print(f"- {task['name']} ({task['status']})")
```

## Licensing and cost
- **Open Source**: No
- **Cost**: Paid (Subscription)
- **Self-hostable**: No

## Related tools / concepts
- [Reclaim.ai](reclaim.md) — smart scheduling and time blocking.
- [Akiflow](akiflow.md) — central command for tasks and calendar.
- [Google Calendar](google_calendar.md) — primary calendar backend for Motion.
- [Sunsama](sunsama.md) — manual daily planning and task ritual.
- [n8n](../../services/n8n.md) — automation platform for custom Motion triggers.
- [Todoist](todoist.md) — lightweight task management alternative.
- [Microsoft To Do](microsoft-todo.md) — enterprise task management.

## Sources / References
- [Motion Official Site](https://www.usemotion.com/)
- [Motion API Documentation](https://docs.usemotion.com/)

## Contribution Metadata
- Last reviewed: 2026-05-23
- Confidence: high
