# Sunsama

Sunsama is a "guided daily planner" designed for professionals who prioritize intentionality, sustainable productivity, and work-life balance. As of May 2026, it has integrated advanced AI capabilities via "Sunny" (its native AI assistant) and the Model Context Protocol (MCP) to deepen its integration with external task and code management tools.

## What it is
Sunsama is a unified daily planning tool that aggregates tasks from various platforms (Email, Slack, GitHub, Linear, Jira, etc.) into a single, time-boxed schedule. It emphasizes a "ritualized" approach to planning and ending the day.

## What problem it solves
It combats burnout, over-commitment, and digital fragmentation. By encouraging users to manually plan their day and set realistic workloads, it prevents the "infinite to-do list" problem and helps users maintain focus on their most important work.

## Where it fits in the stack
- **Category**: [Calendar & Tasks](../calendar_tasks/index.md) / Unified Productivity
- **Layer**: Human-Facing Planning Layer

## Typical use cases
- **Guided Daily Planning**: Following a step-by-step ritual every morning to decide what to work on.
- **Task Consolidation**: Pulling tasks from GitHub issues, Linear tickets, and Gmail threads into one view.
- **Time Boxing**: Dragging tasks onto a calendar to allocate specific hours for deep work.
- **Weekly Reflection**: Using the automated weekly recap to review accomplishments and plan the next cycle.

## Strengths
- **Mindful Workflow**: Forces you to be realistic about what you can actually achieve in a day.
- **Deep Integrations**: Best-in-class support for pulling tasks from external tools while maintaining back-links.
- **Native AI (Sunny)**: A powerful assistant that can plan your day, estimate tasks, and interact with your backlog.
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

## When not to use it
- If you are highly budget-conscious.
- If you prefer a completely automated, algorithm-driven scheduler.
- If you need to build custom, low-level API integrations with your task list.

## Licensing and cost
- **Open Source**: No
- **Cost**: Paid (Subscription).
- **Self-hostable**: No

## Getting started
Sunsama is available as a web app, desktop app (macOS, Windows, Linux), and mobile app.

### Installation (macOS)
```bash
brew install --cask sunsama
```

### Sunny the AI Assistant
Enable Sunny in **Settings > Integrations > AI Assistant**. Once enabled, you can use the sparkle (✦) button or `Cmd + K` to:
- "Plan my day based on my calendar and backlog."
- "What did I accomplish last Tuesday?"
- "Braindump these tasks into my project folder: [list]"

## CLI examples
Sunsama does not have an official CLI. However, it supports global keyboard shortcuts in the desktop app for fast capture:
- `A`: Add task to today.
- `B`: Open backlog.
- `P`: Start daily planning.
- `F`: Enter Focus Mode on the selected task.

## API examples
Sunsama does not offer a public REST API for general development as of May 2026. Automation is handled through:

### 1. Zapier / Make.com
Use the official Sunsama connector to create tasks from external triggers.
- **Action**: Create Task
- **Data**: Title, Note, Planned Date, Channel.

### 2. Sunny MCP (Model Context Protocol)
For developers using [Claude Desktop](../../tools/development_ops/claude-code.md) or other MCP-compatible agents, Sunsama now exposes tools via Sunny:
- `get_task_by_id`: Fetch full details of a specific task.
- `list_today_tasks`: Get the current day's plan for context-aware coding assistance.

## Related tools / concepts
- [Akiflow](akiflow.md) — For faster, keyboard-driven triage.
- [Morgen](morgen.md) — For AI-assisted scheduling with more manual control.
- [Motion](motion.md) — For fully automated, algorithmic scheduling.
- [Todoist](todoist.md) — Common source integration.
- [n8n](../../services/n8n.md) — Can be used via Zapier-bridge or email-ingestion.

## Links
- [Official Website](https://sunsama.com/)
- [Product Changelog](https://roadmap.sunsama.com/changelog)
- [Sunny AI Guide](https://help.sunsama.com/docs/usage-guides/sunny/)

## Backlog
- [x] Perform quarterly technical freshness audit (May 2026).

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-05-31

## Sources / References
- https://roadmap.sunsama.com/changelog
- https://help.sunsama.com/docs/usage-guides/sunny/
- https://www.morgen.so/blog-posts/sunsama-vs-akiflow
- KnowledgeOps Triage (2026-05-31)
