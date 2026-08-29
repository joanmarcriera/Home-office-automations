# Microsoft To Do

## What it is
A cloud-based task management application developed by Microsoft, serving as the central hub for individual task tracking within the Microsoft 365 ecosystem. As of early January 2027, it features advanced **Agentic Calendar Orchestration** via **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, **Qwen 3.6 VL**, and [Gemma 4](../ai_knowledge/local_llms.md), utilizing **MCP 3.1** and **FastMCP 3.1** Task Protocols for cross-service tool routing.

## What problem it solves
Helps users stay organized and manage their day-to-day tasks with features like "My Day" and seamless, native synchronization with Outlook, Teams, and Microsoft Planner. It solves the fragmentation of enterprise tasks by centralizing them in a single, mobile-first interface with AI-native prioritization and multi-agent intent resolution.

## Where it fits in the stack
**Category**: Calendar & Tasks / Task Management. It acts as the personal task layer for the enterprise-grade Microsoft 365 stack, bridging the gap between communication (Teams/Outlook) and execution.

## Typical use cases
- **Personal Productivity**: Managing daily to-do lists via the "My Day" smart list.
- **Enterprise Integration**: Capturing tasks directly from flagged Outlook emails and Microsoft Teams chats.
- **Shared Collaboration**: Managing family shopping lists or small team project tasks with real-time sync.
- **Agentic Automation**: Using [Gemma 4](../ai_knowledge/local_llms.md), DeepSeek-V4, and Qwen 3.6 VL via **FastMCP 3.1** to autonomously prioritize, schedule, and execute tasks via natural language.

## Strengths
- **Ecosystem Synergy**: Deep integration with Outlook Tasks, Flagged Emails, and Microsoft Planner.
- **My Day Focus**: A unique feature that resets every morning, encouraging intentional daily planning.
- **Cross-Platform Accessibility**: Consistent experience across Web, Windows, macOS, iOS, and Android.
- **Agentic Scheduling**: Native support for **Agentic Calendar Orchestration**, allowing AI agents like Claude 5.6, GPT-5.6, and Gemini 4.0 Ultra to move tasks between To Do and Outlook Calendar based on priority and urgency.

## Limitations
- **Power User Gaps**: Lacks complex features found in [Todoist](todoist.md) like robust natural language date parsing for all custom fields.
- **Project Complexity**: Not suitable for large-scale project management (use Microsoft Planner or Azure DevOps).
- **Privacy**: Tasks are stored within the Microsoft cloud, which may not meet "local-first" or strict privacy requirements.

## When to use it
- If you are already a heavy user of the Microsoft 365 ecosystem.
- When you want a simple, clean, and free task manager that "just works" with your work email.
- For users who prefer a daily "fresh start" approach to task management.

## When not to use it
- If you need advanced sub-tasking, complex custom filters, or markdown support.
- If you require a privacy-focused, encrypted, or self-hosted task manager (consider [Vikunja](../../services/vikunja.md)).
- For complex software development workflows (use [Gitea](../../services/gitea.md) issues or GitHub).

## Getting started
Microsoft To Do is primarily used via its web and mobile applications.

### Setup
1. **Sign In**: Use a personal Microsoft account or a Microsoft 365 work/school account.
2. **Setup 'My Day'**: Click the ☀️ icon to start your day and add tasks from your main list or suggestions.
3. **Enable Flagged Email**: Go to Settings > Connected Apps and toggle "Flagged Email" to auto-sync tasks from Outlook.

## CLI examples
While there is no first-party CLI, you can interact with Microsoft To Do using the **Microsoft Graph CLI**.

```bash
# Login to Microsoft Graph
mgc login

# List all your To Do task lists
mgc users todo lists list --user-id me

# Create a high-priority task in a specific list (Early January 2027 Syntax)
mgc users todo lists tasks create --user-id me --todo-task-list-id <list-id> \
  --body '{"title": "Verify FastMCP 3.1 Task Protocol Integration", "importance": "high"}'
```

## API examples
The **Microsoft Graph API (v1.0)** is the standard interface for programmatically managing tasks. The following script shows how to structure and validate a task creation request using **Pydantic v2** prior to transmission.

### Create a Task (Python)
This pattern is used by [n8n](../../services/n8n.md) or custom agents to sync tasks from external sources.
```python
import os
import requests
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, ValidationError

class DateTimeZone(BaseModel):
    dateTime: str = Field(..., description="ISO 8601 formatted date-time string.")
    timeZone: str = Field(default="UTC", description="The time zone (e.g., UTC).")

class MicrosoftToDoTask(BaseModel):
    title: str = Field(..., min_length=1, max_length=250, description="Task title.")
    importance: Literal["low", "normal", "high"] = Field("normal", description="Priority level.")
    categories: List[str] = Field(default_factory=list, description="Array of task categories.")
    dueDateTime: Optional[DateTimeZone] = Field(None, description="Due date and time of the task.")

def create_microsoft_todo_task(access_token: str, list_id: str, raw_task_data: dict):
    """
    Validates task payload using Pydantic v2 before posting to Microsoft Graph API.
    """
    endpoint = f"https://graph.microsoft.com/v1.0/me/todo/lists/{list_id}/tasks"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        # Strict programmatic validation
        validated_task = MicrosoftToDoTask.model_validate(raw_task_data)
        payload = validated_task.model_dump(exclude_none=True)

        # In actual deployment:
        # response = requests.post(endpoint, headers=headers, json=payload)
        # response.raise_for_status()
        # return response.json()

        print("Pydantic v2 Validation Succeeded. Payload matches Microsoft Graph API expectations.")
        return payload
    except ValidationError as e:
        print("Schema validation failed for Microsoft To Do Task payload:")
        raise e

# Example execution by Claude 5.6, GPT-5.6, or Gemini 4.0 Ultra agent
token_placeholder = "token-xyz"
list_placeholder = "list-abc"
raw_input = {
    "title": "Document Early January 2027 FastMCP Graph API Patterns",
    "importance": "high",
    "categories": ["Work", "Documentation"],
    "dueDateTime": {
        "dateTime": "2027-01-31T17:00:00",
        "timeZone": "UTC"
    }
}

create_microsoft_todo_task(token_placeholder, list_placeholder, raw_input)
```

## Related tools / concepts
- [Todoist](todoist.md) — Feature-rich alternative.
- [TickTick](ticktick.md) — Alternative with integrated calendar and Pomodoro.
- [Fantastical](fantastical.md) — Premium client that supports Microsoft To Do tasks.
- [Vikunja](../../services/vikunja.md) — Self-hosted, privacy-first alternative.
- [Outlook](outlook.md) — The underlying mail and calendar provider.
- [n8n](../../services/n8n.md) — For automating task creation via AI workflows.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — The strategy behind Microsoft's Copilot orchestration.
- **Licensing**: Free for personal use; included with Microsoft 365 business and enterprise plans.

## Sources / References
- [Microsoft To Do Official Site](https://todo.microsoft.com/)
- [Microsoft Graph API Documentation (Tasks)](https://learn.microsoft.com/en-us/graph/api/resources/todo-overview)
- [Microsoft 365 Roadmap](https://www.microsoft.com/en-us/microsoft-365/roadmap)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
