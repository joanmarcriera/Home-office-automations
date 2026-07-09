# Sunsama

Sunsama is a mindful daily planner designed to help professionals stay focused and realistic about their workload. As of June 2026, it has introduced **Sunny AI (v2.0)**, an agentic planning assistant that can autonomously triage backlogs and suggest optimal daily schedules based on energy levels and historical velocity.

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
- **MCP Support**: Allows for advanced technical context (e.g., GitHub repo details, Linear issue numbers) to be visible and actionable within the app.
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
Sunsama does not offer a public REST API for general development as of June 2026. Automation is handled through webhooks or the Sunny MCP:

### 1. Webhook-based Task Creation (Zapier/Make)
While there is no direct API, you can trigger task creation via the official Zapier connector or custom webhooks:

```python
import requests

# Example of a custom webhook trigger to create a task
webhook_url = "https://hooks.zapier.com/v1/event/..."
payload = {
    "title": "Analyze Ralph-loop Batch 196",
    "notes": "Automated task from KnowledgeOps agent.",
    "planned_date": "2026-07-21"
}

response = requests.post(webhook_url, json=payload)
print(f"Status: {response.status_code}")
```

### 2. Sunny MCP (Model Context Protocol)
For developers using [Claude Desktop](../development_ops/claude-code.md) or other MCP-compatible agents, Sunsama now exposes tools via Sunny:

```json
// Example: get_task_by_id call
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

## Sources / references
- [Official Website](https://sunsama.com/)
- [Product Changelog](https://roadmap.sunsama.com/changelog)
- [Sunny AI Guide](https://help.sunsama.com/docs/usage-guides/sunny/)
- [Sunsama Help Center](https://help.sunsama.com/)

## Contribution Metadata
- Last reviewed: 2026-06-21
- Confidence: high
