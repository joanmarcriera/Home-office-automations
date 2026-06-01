# Reclaim.ai

## What it is
An AI-powered scheduling automation tool that syncs with Google Calendar to find the best time for tasks, habits, and meetings.

## What problem it solves
Solves "calendar tetris" by automatically blocking time for deep work and habits while staying flexible for incoming meetings.

## Where it fits in the stack
**Category**: Calendar & Tasks / Scheduling Automation

## Typical use cases
- Automated time blocking for tasks
- Multi-calendar syncing (personal/work)
- Habit tracking within the calendar

## Strengths
- Dynamic rescheduling based on calendar priority
- Excellent multi-calendar sync to protect personal time
- Integration with task managers like Todoist, Linear, and Asana

## Limitations
- Only supports Google Calendar (as of mid-2024; Outlook support in progress)
- Requires full calendar access permissions

## When to use it
- When you have a busy schedule and struggle to find time for deep work
- When you need to sync multiple calendars without revealing private details

## When not to use it
- If you use Outlook or iCloud as your primary calendar
- If you prefer manual, fixed-time scheduling

## Getting started
To begin using Reclaim.ai:
1. Sign up for a free account at [Reclaim.ai](https://reclaim.ai/).
2. Connect your primary Google or Outlook calendar during onboarding.
3. **Hello-world example**: Create your first "Habit" (e.g., "Lunch") by selecting **Habits** in the sidebar and choosing a time window. Reclaim will automatically find the best slot in your schedule.
4. To use the API, go to **Settings > Integrations > API** and click **Generate API Key**.

## CLI examples
> [!NOTE]
> Reclaim.ai does not currently offer an official first-party command-line interface.

The primary way to interact with Reclaim from the desktop is via the **Raycast extension**:
- **Create Task**: Quickly add a task to your smart queue with a due date and duration.
- **Share Scheduling Link**: Copy your availability links directly to the clipboard.
- **View Schedule**: See your daily agenda and join meetings from the Raycast command palette.

## API examples
Reclaim provides a REST API for managing tasks and schedules.

### List all tasks (Python)
```python
import requests

API_KEY = "YOUR_RECLAIM_API_KEY"
url = "https://api.app.reclaim.ai/api/tasks"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
tasks = response.json()

for task in tasks:
    print(f"{task['title']} - {task['status']}")
```

### Create a task (cURL)
```bash
curl -X POST https://api.app.reclaim.ai/api/tasks \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Finish Documentation",
       "eventCategory": "WORK",
       "timeChunksRequired": 4,
       "minChunkSize": 2,
       "maxChunkSize": 4,
       "priority": "HIGH"
     }'
```

## Licensing and cost
- **Open Source**: No
- **Cost**: Freemium
- **Self-hostable**: No

## Related tools / concepts
- [Google Calendar](google_calendar.md)
- [Motion](motion.md)
- [Akiflow](akiflow.md)
- [Todoist](todoist.md)
- [n8n](../../services/n8n.md)

## Sources / References
- [Reclaim.ai Official Site](https://reclaim.ai/)
- [Reclaim API Documentation](https://github.com/reclaim-ai/reclaim-api)

## Contribution Metadata
- Last reviewed: 2026-05-13
- Confidence: high
