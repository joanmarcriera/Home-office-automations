# Todoist

## What it is
A popular task management application that helps individuals and teams organize, plan, and collaborate on projects.

## What problem it solves
Provides a simple yet powerful interface for capturing tasks, setting deadlines, and organizing work into projects and sub-tasks.

## Where it fits in the stack
**Category**: Calendar & Tasks / Task Management

## Typical use cases
- Daily personal task management
- Small team project collaboration
- Grocery lists and reminders

## Strengths
- Clean, intuitive interface across all platforms
- Excellent natural language parsing for deadlines
- Two-way sync with Google Calendar

## Limitations
- Advanced features like reminders and labels require a Pro subscription
- Not a full project management suite for complex enterprise needs

## When to use it
- For personal or small group task organization
- When you need a fast way to capture and categorize tasks

## When not to use it
- For complex software development projects (prefer Jira or GitHub Issues)
- If you need advanced resource allocation or Gantt charts

## Licensing and cost
- **Open Source**: No
- **Cost**: Freemium
- **Self-hostable**: No

## Getting started
### n8n Integration
Todoist has a native node in n8n. To create a task via n8n:
1. Add a **Todoist** node.
2. Connect your Todoist account via OAuth2.
3. Resource: `Task`, Operation: `Create`.
4. Fill in `Content` and `Project`.

## API examples
Todoist provides a powerful REST API for developers.

### Create a Task (Python)
```python
import requests

url = "https://api.todoist.com/rest/v2/tasks"
headers = {
    "Authorization": "Bearer YOUR_API_TOKEN",
    "Content-Type": "application/json"
}
data = {
    "content": "Buy milk",
    "due_string": "tomorrow at 12:00",
    "priority": 4
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

### Batch Operations and Filtering
You can fetch tasks filtered by project, section, or label.

```python
# Fetch all tasks in a specific project
project_id = "123456789"
response = requests.get(
    f"https://api.todoist.com/rest/v2/tasks?project_id={project_id}",
    headers=headers
)
tasks = response.json()
for task in tasks:
    print(f"- {task['content']} (Due: {task.get('due', {}).get('date', 'No date')})")
```

## Workflow Integration

### Recurring Task Patterns
Todoist's natural language engine is ideal for recurring "maintenance" tasks for agents.
- `every day at 9am`
- `every 1st Monday`
- `every weekday`

### Project-Based Organization
For complex agentic workflows, use **Sections** to manage task states:
1. **Inbox**: Raw task capture.
2. **Analysis**: Agent is processing the task.
3. **Action**: Ready for execution.
4. **Review**: Human-in-the-loop verification.

```python
# Move a task to a specific section
task_id = "..."
section_id = "..."
data = {"section_id": section_id}
requests.post(f"https://api.todoist.com/rest/v2/tasks/{task_id}", headers=headers, json=data)
```

## Related tools / concepts
- [Reclaim.ai](reclaim.md) — Syncs Todoist tasks into your Google Calendar.
- [Akiflow](akiflow.md) — Aggregates Todoist tasks into a unified command center.
- [TickTick](ticktick.md) — A direct competitor with built-in Pomodoro.
- [Microsoft To Do](microsoft-todo.md) — Microsoft's native task management tool.
- [Any.do](any-do.md) — Task manager with a focus on daily planning.
- [Vikunja](../../services/vikunja.md) — Self-hosted alternative to Todoist.
- [n8n](../../services/n8n.md) — Used for advanced Todoist automations.
- [Google Calendar](google_calendar.md) — Two-way sync partner.

## Sources / References
- [Official Website](https://todoist.com/)
- [Todoist Developer Documentation](https://developer.todoist.com/rest/v2/)
- [n8n Todoist Integration Guide](https://www.todoist.com/help/articles/use-n8n-with-todoist-w3BrOPja8)

## Contribution Metadata
- Last reviewed: 2026-05-13
- Confidence: high
