# TickTick

## What it is
A powerful, all-in-one task management app that features a calendar, Pomodoro timer, habit tracker, and Markdown notes.

## What problem it solves
Consolidates personal productivity tools into a single app, reducing context switching between task lists, calendars, and timers.

## Where it fits in the stack
**Category**: Calendar & Tasks / Task Management

## Typical use cases
- Personal task management and GTD (Getting Things Done).
- Habit tracking and time-boxing with the integrated Pomodoro timer.
- Managing shared family lists and simple team projects.

## Strengths
- **Feature Rich**: Includes many features (calendar, timer, habits) that usually require separate apps.
- **Natural Language Parsing**: Excellent at recognizing dates and times in task names.
- **Multi-Platform**: Robust apps for almost every operating system and device.

## Limitations
- **Calendar Power**: The integrated calendar is good but not as powerful as specialized tools like Fantastical.
- **Free Tier Constraints**: Several core features (like full calendar view) are locked behind the Pro subscription.

## When to use it
- If you want a single app to handle tasks, habits, and time-boxing.
- If you find Todoist too minimalist or expensive for its feature set.

## When not to use it
- If you need enterprise-level project management features.
- If you prefer a modular approach with specialized apps for each function.

## Licensing and cost
- **Open Source**: No
- **Cost**: Freemium (Basic features free; Pro subscription for full features)
- **Self-hostable**: No

## Getting started

### Installation
TickTick provides a limited official API (V1) and a more powerful unofficial one (V2). The `ticktick-py` library is the most popular community client.

```bash
# Install the community Python client
pip install ticktick-py
```

### Hello World (Python)
Authenticate and create a simple task:

```python
from ticktick.api import TickTickClient

client = TickTickClient('your_email', 'your_password')
task = client.task.builder('Hello from Python')
client.task.create(task)
```

## CLI examples
There is no official CLI, but you can use `curl` to interact with the Open API (V1) once you have an OAuth token.

```bash
# Get all projects
curl -X GET "https://api.ticktick.com/open/v1/project" \
  -H "Authorization: Bearer ${TICKTICK_ACCESS_TOKEN}"

# Create a task in the Inbox
curl -X POST "https://api.ticktick.com/open/v1/task" \
  -H "Authorization: Bearer ${TICKTICK_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy Milk", "content": "Organic if possible"}'

# Get uncompleted tasks for a specific project
curl -X GET "https://api.ticktick.com/open/v1/project/{projectId}/data" \
  -H "Authorization: Bearer ${TICKTICK_ACCESS_TOKEN}"
```

## API examples

### Batch Task Operations (Python)
Using the unofficial `ticktick-py` for advanced features like batch creation.

```python
from ticktick.api import TickTickClient

client = TickTickClient('user@example.com', 'password')

# Batch create tasks
tasks = [
    client.task.builder('Task 1', priority=3),
    client.task.builder('Task 2', priority=1)
]
client.task.create(tasks)

# Get all uncompleted tasks from the state
uncompleted = client.state['tasks']
for task in uncompleted:
    print(f"[{task['title']}] - ID: {task['id']}")
```

### Webhook Support
TickTick does not provide official outgoing webhooks. Automation usually requires polling the API or using a middleman like Zapier/Make.

## Related tools / concepts
- [Todoist](todoist.md)
- [Any.do](any-do.md)
- [Habitica](../../services/habitica.md)
- [TickTick Open API (V1)](https://developer.ticktick.com/docs)

## Sources / References
- [TickTick Official Site](https://ticktick.com/)
- [TickTick Developer Portal](https://developer.ticktick.com/)
- [ticktick-py Documentation](https://pypi.org/project/ticktick-py/)

## Contribution Metadata
- Last reviewed: 2026-05-02
- Confidence: high
