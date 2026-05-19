# OpenClaw Use-Case Catalog

## What it is
The OpenClaw Use-Case Catalog is a categorized directory of recurring automation and assistant workflows optimized for the [OpenClaw](../../tools/development_ops/openclaw.md) agent runtime. It distills real-world implementation notes from the community into a selection guide for users looking to deploy autonomous agents in their personal or professional environments.

## What problem it solves
New users often find OpenClaw's flexibility overwhelming, leading to "blank canvas" syndrome. This catalog solves that by translating abstract agent capabilities into concrete workload shapes, providing the necessary guardrails and implementation notes to ensure workflows are reliable and safe.

## Where it fits in the stack
This catalog sits at the **Pattern & Selection Layer** of the agentic ecosystem. It helps users decide when OpenClaw is the appropriate runtime versus using a simpler script, an [n8n](../../services/n8n.md) flow, or a dedicated tool like [OpenHands](../../tools/development_ops/openhands.md).

## Typical use cases
- **Morning Briefing Assistant**: Aggregating weather, calendar events, and task lists into a single conversational summary.
- **"Second Brain" Capture**: Processing bookmarks, notes, and links from various sources into a unified knowledge base.
- **Nightly Research Digest**: Scheduled agents that search the web for specific topics and synthesize findings into a daily report.
- **Email Triage**: Classifying incoming emails and drafting replies in the user's specific tone and style.
- **Infrastructure Monitoring**: Performing periodic SSH-backed system checks and reporting anomalies to a chat channel.

## Strengths
- **Practicality**: Based on long-running, real-world workflows rather than theoretical possibilities.
- **Safety-First**: Provides specific "Guardrails" for every use case to prevent unintended side effects.
- **Comparative Guidance**: Clearly defines when the agent is a "good fit" versus a "poor fit" for a task.

## Limitations
- **User Bias**: Community examples often reflect the needs of "power users" and may be too complex for beginners.
- **Reliability Variance**: Not all documented workflows have the same level of production-grade stability.
- **Maintenance Overhead**: As the OpenClaw API and integrations evolve, these use cases require periodic refreshing.

## Categorized use cases

| Category | Use case | Why OpenClaw fits | Guardrail |
|---|---|---|---|
| Home-office | Morning briefing assistant | Good for collecting tasks, weather, reminders, and daily summaries across tools | Keep it read-only |
| Knowledge management | "Second brain" capture and recall | Works well when a conversational layer needs memory and retrieval over bookmarks, notes, and saved links | Make note-writing explicit |
| Research | Nightly research digest | Strong fit for scheduled search, summary, and digest workflows | Verify sources before external sharing |
| Content | Idea capture and content machine | Useful for capturing rough ideas, organizing them, and expanding into reusable drafts | Draft-only before publishing |
| Web work | URL summary and link processing | Efficient when a lightweight skill can summarize an article, PDF, or video from a link | Keep browsing isolated |
| Infrastructure | Server and service monitoring | Works well for SSH-backed checks plus human-readable reporting in chat | Require approval for fixes and restarts |
| Development | Coding from phone / remote PR prep | Helpful when conversational requests must turn into branch, commit, and PR actions | Never auto-merge without review |
| Communications | Email triage and draft replies | Good for classifying inbox traffic and drafting responses in the user's tone | Draft-only mode, never send directly |
| Calendar and family | Scheduling and reminder coordination | Useful when the same assistant handles calendar checks, event creation, and reminders | Require confirmation for sensitive events |
| Operations | Daily life admin and recurring checklists | Strong fit for errands, reminders, recurring personal tasks, and follow-up loops | Keep external side effects explicit |
| Reporting | Scheduled reporting and anomaly detection | Good for pulling routine metrics and calling out patterns humans might miss | Separate reporting from action-taking |

## Implementation notes
- Use [LiteLLM](../../services/litellm.md) or a similar router to separate cheap routine jobs from expensive deep-thinking tasks.
- Keep destructive skills out of the default assistant loop.
- Put draft-first boundaries around email, publishing, and customer-facing actions.
- Use [n8n](../../services/n8n.md) or another workflow system when timing, retries, approvals, and auditability matter more than conversation.
- Start with one or two well-bounded skills before layering more channels or capabilities.

## Technical implementation example (YAML)
OpenClaw uses YAML-based skill definitions. Below is an example of a "Morning Briefing" skill that aggregates data from multiple sources:

```yaml
# skills/morning_briefing.yaml
name: morning_briefing
description: "Aggregates weather, calendar, and tasks for a daily summary."
trigger: "morning briefing"
parameters:
  location:
    type: string
    description: "The city for weather lookup"
    default: "San Francisco"
actions:
  - name: get_weather
    skill: weather_provider
    args:
      city: "{{location}}"
  - name: get_calendar
    skill: google_calendar
    args:
      view: "day"
  - name: get_tasks
    skill: todoist
    args:
      filter: "today"
prompt_template: |
  You are a helpful morning assistant. Based on the following data:
  Weather: {{actions.get_weather.output}}
  Calendar: {{actions.get_calendar.output}}
  Tasks: {{actions.get_tasks.output}}

  Provide a concise, motivating summary of the user's day.
```

## Security and Guardrails
When deploying these use cases, consider the following security patterns:
- **Credential Isolation**: Store API keys in environment variables or a secure vault, never in the YAML definitions.
- **Sandbox Execution**: For development use cases, ensure OpenClaw is running in a [Docker](../../tools/infrastructure/docker.md) container to isolate filesystem access.
- **Human-in-the-loop (HITL)**: For "Content" or "Communications" use cases, enforce a `draft_only: true` flag in the skill configuration.

## When to use it
- Use when designing a new agentic workflow and looking for established patterns and safety boundaries.
- Use to prioritize which agent capabilities to build first based on proven community success.
- Use when evaluating whether a complex automation task belongs in an autonomous agent or a traditional workflow tool.

## When not to use it
- Don't use if the workflow is purely deterministic and better suited for a simple Python script or [n8n](../../services/n8n.md).
- Don't use for mission-critical industrial automation where human-in-the-loop (HITL) is not possible.
- Avoid when the primary requirement is absolute auditability with zero autonomous interpretation.

## Related tools / concepts
- [OpenClaw](../../tools/development_ops/openclaw.md)
- [n8n](../../services/n8n.md)
- [OpenHands](../../tools/development_ops/openhands.md)
- [Daily Briefing](../../reference-implementations/llm-prompts/daily-briefing.md)
- [Agentic Workflows](agentic-workflows.md)
- [Agent Protocols](../agent_protocols.md)
- [Skills Best Practices](skills-best-practices.md)

## Sources / References
- [OpenClaw automation examples and workflow notes](https://gist.github.com/ANcpLua/4ba21cd7f0bf08e0b483f3187dd93308)
- [OpenClaw after 50 days: all prompts for 20 real workflows](https://gist.github.com/velvet-shark/b4c6724c391f612c4de4e9a07b0a74b6)
- [awesome-openclaw-usecases](https://github.com/hesamsheikh/awesome-openclaw-usecases)

## Contribution Metadata
- Last reviewed: 2026-03-29
- Confidence: high
