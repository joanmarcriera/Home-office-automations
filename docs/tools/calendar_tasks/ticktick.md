# TickTick

TickTick is a powerful, all-in-one task management app that integrates a calendar, Pomodoro timer, habit tracker, and Markdown notes. As of early January 2027, it remains the most feature-dense choice for personal productivity, having added native AI transcription, summarization, and **Model Context Protocol (MCP 3.1 / FastMCP 3.1)** Task Protocol support for seamless AI agent integration with frontier models like Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, Gemma 4, DeepSeek-V4, and Qwen 3.6 VL.

## What it is
TickTick is a multi-platform productivity suite that consolidates essential tools into a single application. It is designed for individuals who want to manage their entire life—tasks, habits, focus, and schedule—without context switching between separate apps.

## What problem it solves
It reduces "app sprawl" and cognitive load by providing a unified interface for the Getting Things Done (GTD) methodology, Eisenhower Matrix prioritization, and time-blocking. It solves the fragmentation problem by keeping tasks and their associated calendar events and timers in one place, enabling seamless scheduling workflows.

## Where it fits in the stack
**Calendar & Tasks**. It serves as a unified human-facing interface for personal intelligence and task management. It sits between low-level calendar providers and the user, offering a rich set of capture and organization tools.

## Typical use cases
- **Unified GTD**: Capturing, clarifying, and organizing life and work tasks.
- **Time Blocking**: Dragging tasks onto the integrated calendar to schedule the day.
- **Habit Formation**: Tracking daily routines with the built-in Habit Tracker.
- **Deep Work**: Using the integrated Pomodoro timer with white noise and task-specific timers.
- **Agentic Task Management**: Using Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, Gemma 4, DeepSeek-V4, or Qwen 3.6 VL via FastMCP 3.1 Task Protocol to create tasks from meeting transcripts or code reviews.

## Strengths
- **Feature Density**: Includes calendar, timer, habits, and notes at a lower price point than most competitors.
- **AI Voice & Transcription**: Native ability to transcribe voice recordings into tasks and summarize meeting audio using frontier models.
- **Persistent Reminders**: "Nag" alerts that continue until a task is completed or snoozed.
- **Superior Calendar**: Full multi-project calendar view (Month, Week, Day) built directly into the task manager.
- **FastMCP 3.1 Integration**: Exposes task management tools to AI agents for automated planning, scheduling, and execution.

## Limitations
- **API Maturity**: The official public API remains less robust than competitors like Todoist, often requiring community wrappers for advanced automation.
- **Closed Ecosystem**: Proprietary and not self-hostable.
- **Privacy**: No local-only mode; all data is synced to TickTick's servers.

## When to use it
- If you want a single app to handle tasks, habits, and time-boxing.
- If you find Todoist too minimalist or find the cost of a multi-app stack prohibitive.
- If you need persistent, aggressive reminders for task completion.
- If you want an agent-ready task manager via MCP 3.1.

## When not to use it
- If you strictly require open-source or local-first data storage (see [Vikunja](../../services/vikunja.md)).
- If you need enterprise-level project management features with complex permission hierarchies.
- If you prefer a minimalist, text-only interface.

## Getting started

### Installation
TickTick is available on iOS, Android, macOS, Windows, Linux, and the Web.
- **Web**: [TickTick.com](https://ticktick.com/)
- **CLI (Python Library)**: `pip install ticktick-py pydantic`

### Basic Automation (Python)
```python
from ticktick.api import TickTickClient

# Initialize client
client = TickTickClient('your_email', 'your_password')

# Create a task
task = client.task.builder(
    title='Record meeting summary',
    content='Use TickTick AI to transcribe the audio',
    priority=3
)
client.task.create(task)
```

## CLI examples
While no official binary exists, you can use `curl` for automation via the Open API (V1).

```bash
# Get all projects
curl -X GET "https://api.ticktick.com/open/v1/project" \
  -H "Authorization: Bearer ${TICKTICK_ACCESS_TOKEN}"

# Create a task
curl -X POST "https://api.ticktick.com/open/v1/task" \
  -H "Authorization: Bearer ${TICKTICK_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Clean the house tomorrow at 10am",
    "content": "Focus on the kitchen first"
  }'
```

## API examples

### AI & Agent Integration (MCP)
TickTick can be used as a tool for AI agents (like Claude Desktop). This allows agents to:
- `create_task`: Create a new task with specific parameters.
- `list_all_tasks`: Retrieve open tasks for context-aware planning.

**Sample FastMCP 3.1 Config (Claude Desktop):**
```json
"mcpServers": {
  "ticktick": {
    "command": "npx",
    "args": ["-y", "@alexarevalo.ai/mcp-server-ticktick"],
    "env": {
      "TICKTICK_ACCESS_TOKEN": "your_token_here"
    }
  }
}
```

### Strict Task Input Validation (Python with Pydantic v2)
To ensure reliable structured integration between agents (e.g., Llama 4, Qwen 3.6, Gemini 4.0 Pro) and the TickTick API, developers use **Pydantic v2** models to validate schema payloads before submission.

```python
from pydantic import BaseModel, Field, ValidationError, model_validator
from typing import Optional, List
from datetime import datetime

class TickTickTaskSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="The title of the task")
    content: Optional[str] = Field(None, description="Detailed description or notes")
    priority: int = Field(0, ge=0, le=5, description="Priority (0 = None, 1 = Low, 3 = Medium, 5 = High)")
    tags: List[str] = Field(default_factory=list, description="Associated tags")
    due_date: Optional[datetime] = Field(None, alias="dueDate")

    @model_validator(mode='after')
    def check_non_empty_title(self) -> 'TickTickTaskSchema':
        if not self.title.strip():
            raise ValueError("Task title cannot be empty or whitespace-only")
        return self

# Example validation execution
payload = {
    "title": "Upgrade Agent Scheduling Stack",
    "content": "Incorporate FastMCP 3.1 into personal workflows",
    "priority": 5,
    "tags": ["AI", "productivity"],
    "dueDate": "2026-12-31T23:59:59Z"
}

try:
    # Validating task data via Pydantic v2
    validated_task = TickTickTaskSchema.model_validate(payload)
    print("Validation Successful!")
    print(validated_task.model_dump(by_alias=True))
except ValidationError as e:
    print("Schema Validation Failed:", e.json())
```

## Related tools / concepts
- [Todoist](todoist.md) — The primary minimalist competitor.
- [Any.do](any-do.md) — Mobile-first task management.
- [Akiflow](akiflow.md) — Consolidation-focused task and calendar management.
- [Amie](amie.md) — High-aesthetic "joyful" productivity suite.
- [Morgen](morgen.md) — Unified calendar and task integration for desktop.
- [Habitica](../../services/habitica.md) — Gamified task management.
- [Vikunja](../../services/vikunja.md) — Self-hosted open-source alternative.
- [Composio](../agents/composio.md) — For advanced agentic toolsets.
- [n8n](../../services/n8n.md) — For connecting TickTick to external workflows.
- [Make](../automation_orchestration/make.md) — Visual automation for task syncing.

## Sources / references
- [Official Website](https://ticktick.com/)
- [TickTick Developer Portal](https://developer.ticktick.com/)
- [AI Features Overview](https://help.ticktick.com/articles/7444685542580551680)
- [TickTick MCP Server (GitHub)](https://github.com/alexarevalo/mcp-server-ticktick)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
