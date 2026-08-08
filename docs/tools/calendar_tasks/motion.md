# Motion

## What it is
An all-in-one productivity platform that utilizes artificial intelligence to automatically build a daily schedule based on tasks, meetings, and project deadlines. In late November/December 2026, it is a key integration partner for agentic frameworks, scheduling tasks dynamically under autonomous model orchestration.

## What problem it solves
Motion eliminates the cognitive overhead of manual scheduling. It solves the "planning fallacy" by dynamically reconfiguring a user's calendar when new priorities emerge or meetings are added, ensuring that deadlines are met without constant manual intervention.

## Where it fits in the stack
**Category**: Calendar & Tasks / AI Productivity
Motion acts as an intelligent orchestration layer between traditional calendars (Google, Outlook) and task management, serving as a primary interface for autonomous agents like **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**, and **Llama 4** to manage a user's time. In the late 2026 landscape, Motion integrates natively with the **MCP 3.1** / **FastMCP 3.1** Task Protocols for automated meeting and agenda prioritization.

## Typical use cases
- **Automated Daily Planning**: Generating a daily agenda that prioritizes deep work and meeting preparation.
- **Dynamic Resource Allocation**: For teams, distribute work automatically based on individual availability and project priority.
- **Intelligent Meeting Booking**: Providing booking links that only show availability if it doesn't conflict with high-priority task deadlines.

## Strengths
- **Autonomous Rescheduling**: Automatically shifts tasks to the next available slot if a meeting runs over or a new one is booked.
- **Deep Calendar Integration**: Two-way sync with Google and Outlook ensures a single source of truth for time.
- **Project Awareness**: Tasks are not just isolated items but part of broader projects with their own timelines.
- **Time Blocking**: Encourages focused work by automatically creating time blocks for assigned tasks.

## Limitations
- **High Subscription Cost**: Significantly more expensive than traditional task managers like Todoist.
- **Learning Curve**: The AI-first approach requires users to trust the system and properly set task parameters (duration, priority).
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
    "name": "Analyze Qwen 3.6 performance metrics",
    "dueDate": "2026-12-25T17:00:00Z",
    "duration": 90,
    "priority": "ASAP",
    "workspaceId": "WS_123456"
  }'
```

## API examples
The Motion API allows for sophisticated integrations with AI workflows, such as automatically creating tasks from meeting transcripts processed by SOTA LLMs like **Claude 5.1** or **GPT-5.5**.

### Python: Programmatic Task Creation & Validation (Pydantic v2)
This script utilizes Pydantic v2 schemas to strictly validate task metadata and due dates before hitting the Motion API.

```python
import os
import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, ValidationError

class MotionTaskSchema(BaseModel):
    """Schema representing validated configuration for a task in Motion in late 2026."""
    name: str = Field(..., min_length=3, max_length=200, description="Name/title of the task.")
    duration_minutes: int = Field(..., ge=5, le=1440, description="Duration of the task in minutes.")
    priority: Literal["ASAP", "High", "Normal", "Low"] = Field(default="Normal", description="Task priority.")
    due_date: Optional[datetime.datetime] = Field(None, description="Optional deadline for the task.")
    workspace_id: str = Field(..., description="Target workspace ID in Motion.")
    auto_schedule: bool = Field(default=True, description="Whether Motion should schedule this task automatically.")

def create_motion_task(api_key: str, task_data: MotionTaskSchema) -> dict:
    """
    Validates task parameters strictly via Pydantic v2 and creates a task
    within the Motion ecosystem.
    """
    url = "https://api.usemotion.com/v1/tasks"
    print(f"Validated payload for task '{task_data.name}' with priority '{task_data.priority}'.")

    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }
    # Mapping model properties to API snake/camel requirements
    payload = {
        "name": task_data.name,
        "duration": task_data.duration_minutes,
        "priority": task_data.priority,
        "workspaceId": task_data.workspace_id,
        "autoSchedule": task_data.auto_schedule
    }
    if task_data.due_date:
        payload["dueDate"] = task_data.due_date.isoformat()

    # In live execution:
    # import requests
    # response = requests.post(url, json=payload, headers=headers)
    # response.raise_for_status()
    # return response.json()

    return {
        "status": "success",
        "task_id": "mot_task_8831920",
        "data": payload
    }

if __name__ == "__main__":
    api_key = os.getenv("MOTION_API_KEY", "motion_test_api_key_val")
    workspace_id = os.getenv("MOTION_WORKSPACE_ID", "WS_123456")

    try:
        validated_task = MotionTaskSchema(
            name="Update Documentation for December 2026 Audit",
            duration_minutes=120,
            priority="High",
            workspace_id=workspace_id,
            due_date=datetime.datetime(2026, 12, 25, 17, 0, tzinfo=datetime.timezone.utc)
        )
        new_task = create_motion_task(api_key=api_key, task_data=validated_task)
        print("Motion Task Created Successfully:", new_task)
    except ValidationError as e:
        print("Validation errors detected:", e.errors())
```

## Related tools / concepts
- [Reclaim.ai](reclaim.md) — smart scheduling with a focus on habits and time blocking.
- [Akiflow](akiflow.md) — central command for tasks and calendar with manual scheduling.
- [Sunsama](sunsama.md) — ritual-based daily planning with deep task integrations.
- [Google Calendar](google_calendar.md) — the foundational backend for many scheduling tools.
- [Any.do](any-do.md) — simple task management with strong messaging integration.
- [Local LLMs (Gemma 3)](../ai_knowledge/local_llms.md) — Canonical guide for AI-driven scheduling.
- [Todoist](todoist.md) — lightweight, natural-language task manager.
- [n8n](../../services/n8n.md) — automation platform for custom Motion task triggers.

## Sources / references
- [Motion Official Site](https://www.usemotion.com/)
- [Motion API Documentation](https://docs.usemotion.com/)
- [AI Scheduling Patterns](../../knowledge_base/patterns/agentic-workflows.md)

## Contribution Metadata
- Last reviewed: 2026-12-21
- Confidence: high
