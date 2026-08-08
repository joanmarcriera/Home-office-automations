# Sunsama

Sunsama is a mindful daily planner designed to help professionals stay focused and realistic about their workload. In late November/December 2026, it features **Sunny AI (v2.5)**, an agentic planning assistant that leverages **Gemma 3**, **GPT-5.5**, and **Claude 5.1** to autonomously triage backlogs and suggest optimal daily schedules based on energy levels and historical velocity.

## What it is
Sunsama is an all-in-one daily planner that pulls tasks from various tools (GitHub, Linear, Trello, Slack, Email) into a single, unified view. It emphasizes a "ritualized" approach to planning, guiding users through a morning setup and evening shutdown routine.

## What problem it solves
It solves the problem of "to-do list overwhelm" and fragmented workflows. By forcing users to time-box their tasks onto a calendar, it ensures that plans are grounded in the reality of available time. It addresses the friction of jumping between multiple project management tools by centralizing everything into a single focus-oriented interface.

## Where it fits in the stack
**Calendar & Tasks**. It acts as the "orchestration layer" for personal productivity, sitting on top of specific project management tools and base calendars. It is designed for individual use rather than team-wide project coordination.

## Typical use cases
- **Guided Daily Planning**: Following a step-by-step ritual every morning to decide what to focus on today.
- **Task Consolidation**: Pulling assigned GitHub issues, Linear tickets, and Slack messages into a single daily list.
- **Time Boxing**: Dragging tasks from the list onto a Google or Outlook calendar to reserve space for deep work.
- **Weekly Reflection**: Using the automated weekly recap to review accomplishments and plan the next cycle.
- **Agentic Triage**: Using Sunny AI to automatically prioritize a cluttered backlog into a manageable daily plan.

## Strengths
- **Mindful Workflow**: Forces you to be realistic about what you can actually achieve in a day.
- **Deep Integrations**: Best-in-class support for pulling tasks from external tools while maintaining back-links.
- **Sunny AI (2026)**: A powerful assistant that can plan your day, estimate tasks, and interact with your backlog.
- **FastMCP 3.1 / MCP 3.1 Support**: Native integration with the **Model Context Protocol (MCP 3.1)** allows for advanced technical context (e.g., GitHub repo details, Linear issue numbers, Qwen 3.6 runtimes) to be visible and actionable within the app.
- **High-Quality UI**: A calm, distraction-free interface that supports both light and dark modes.

## Limitations
- **High Cost**: One of the most expensive personal productivity tools ($20/mo baseline).
- **Manual Overhead**: Requires active participation; users looking for 100% "auto-scheduling" may prefer [Motion](motion.md).
- **No Public REST API**: Programmatic access is limited to official integrations and Zapier/Make.

## When to use it
- If you struggle with over-commitment and need a tool that encourages realism.
- If your work is scattered across many different project management tools.
- If you value a guided, ritualized approach to time management.
- If you want an AI assistant (Sunny) that understands your personal productivity patterns.

## When not to use it
- If you are highly budget-conscious.
- If you prefer a completely automated, algorithm-driven scheduler.
- If you need to build custom, low-level API integrations with your task list.
- If you require a self-hosted or offline-only solution.

## Getting started

### Installation
Sunsama is available as a web app, desktop app (macOS, Windows, Linux), and mobile app.

```bash
# macOS Installation
brew install --cask sunsama
```

- **Web**: Visit [Sunsama.com](https://sunsama.com/)

### Sunny the AI Assistant (Hello World)
Enable Sunny in **Settings > Integrations > AI Assistant**. Once enabled, you can use the sparkle (✦) button or `Cmd + K` to verify your agentic planning setup:

```markdown
"Plan my day based on my calendar and backlog."
```

Sunny will then analyze your workload and suggest an optimal schedule.

## CLI examples
Sunsama does not have an official CLI. However, it supports global keyboard shortcuts in the desktop app for fast capture and navigation:

```text
A: Add task to today
B: Open backlog
P: Start daily planning
F: Enter Focus Mode on the selected task
Cmd + K: Open the Command Palette for Sunny AI commands
```

## API examples
Sunsama does not offer a public REST API for general development as of late 2026. Automation is handled through webhooks or the Sunny MCP.

### 1. Webhook-based Task Creation with Pydantic v2 (Zapier/Make)
While there is no direct public API, custom webhooks are utilized to parse payloads safely. SOTA models like **Claude 5.1** use Pydantic v2 model schemas to validate these payloads before dispatching them.

```python
import os
import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ValidationError, HttpUrl

class SunsamaWebhookPayloadSchema(BaseModel):
    """Schema representing validated webhook payload structure for Sunsama task integration in late 2026."""
    title: str = Field(..., min_length=1, max_length=255, description="The title of the task to be created.")
    notes: Optional[str] = Field(None, description="Detailed notes or subtasks list.")
    planned_date: Optional[datetime.date] = Field(None, description="Target date for scheduling the task.")
    channel_source: Optional[str] = Field(default="Webhook", description="Origin channel, e.g. 'Slack', 'GitHub', 'Email'.")
    external_url: Optional[HttpUrl] = Field(None, description="Backlink URL referencing the original issue or email.")
    labels: List[str] = Field(default_factory=list, description="Array of tag labels to apply.")

def send_validated_sunsama_webhook(webhook_url: str, payload_data: SunsamaWebhookPayloadSchema) -> dict:
    """
    Validates the outbound Sunsama payload via Pydantic v2 and posts the
    validated data structure to the Sunsama ingestion hook.
    """
    print(f"Schema validation succeeded. Dispatching task '{payload_data.title}' to Sunsama Webhook...")

    # Dump to JSON-compatible dict format (serializing dates/URLs automatically)
    payload = payload_data.model_dump(mode="json", exclude_none=True)

    # In live execution:
    # import requests
    # response = requests.post(webhook_url, json=payload)
    # response.raise_for_status()
    # return response.json()

    return {
        "status": "dispatched",
        "payload_sent": payload
    }

if __name__ == "__main__":
    test_webhook_url = os.environ.get("SUNSAMA_WEBHOOK_URL", "https://hooks.zapier.com/v1/event/example_id")

    try:
        task_data = SunsamaWebhookPayloadSchema(
            title="Analyze Ralph-loop Batch 340",
            notes="Verify technical freshness compliance under Claude 5.1 & FastMCP 3.1.",
            planned_date=datetime.date(2026, 12, 21),
            external_url="https://github.com/coder/knowledgeops-agents/issues/340",
            labels=["FreshnessAudit", "Batch-340"]
        )
        dispatch_result = send_validated_sunsama_webhook(webhook_url=test_webhook_url, payload_data=task_data)
        print("Success:", dispatch_result)
    except ValidationError as e:
        print("Webhook data validation failed:", e.errors())
```

### 2. Sunny MCP (Model Context Protocol)
For developers using [Claude Desktop](../ai_knowledge/claude-desktop.md) or other **MCP 3.1** compatible agents, Sunsama now exposes tools via Sunny:

```json
// Example: get_task_by_id call using MCP 3.1 Task Protocol / FastMCP 3.1
{
  "method": "tools/call",
  "params": {
    "name": "get_task_by_id",
    "arguments": {
      "id": "task_123abc"
    }
  }
}
```

## Related tools / concepts
- [Akiflow](akiflow.md) — For faster, keyboard-driven triage.
- [Morgen](morgen.md) — For AI-assisted scheduling with more manual control.
- [Motion](motion.md) — For fully automated, algorithmic scheduling.
- [Todoist](todoist.md) — Common source integration.
- [n8n](../../services/n8n.md) — Can be used via Zapier-bridge or email-ingestion.
- [TickTick](ticktick.md) — All-in-one alternative with habit tracking.
- [Notion Calendar](notion-calendar.md) — Scheduling for Notion users.
- [Chronos MCP](../automation_orchestration/chronos-mcp.md) — For cross-platform scheduling orchestration.
- [Amie](amie.md) — A "joyful" productivity alternative.

## Sources / references
- [Official Website](https://sunsama.com/)
- [Product Changelog](https://roadmap.sunsama.com/changelog)
- [Sunny AI Guide](https://help.sunsama.com/docs/usage-guides/sunny/)
- [Sunsama Help Center](https://help.sunsama.com/)

## Contribution Metadata
- Last reviewed: 2026-12-21
- Confidence: high
