# OpenClaw Use-Case Catalog

The OpenClaw Use-Case Catalog is a categorized directory of recurring automation and assistant workflows optimized for the OpenClaw agent runtime.

## What it is

The OpenClaw Use-Case Catalog is a categorized directory of recurring automation and assistant workflows optimized for the [OpenClaw](../../tools/development_ops/openclaw.md) agent runtime. It distills real-world implementation notes from the community into a selection guide for users looking to deploy autonomous agents in their personal or professional environments. The July 2026 update includes deep integration with the [MCP 3.0 Task Protocol](../../architecture/multi_agent_knowledgeops.md) for standardized execution.

## What problem it solves

New users often find OpenClaw's flexibility overwhelming, leading to "blank canvas" syndrome. This catalog solves that by translating abstract agent capabilities into concrete workload shapes, providing the necessary guardrails and implementation notes to ensure workflows are reliable and safe. It standardizes the hand-off between users and agents for common household and development tasks.

## Where it fits in the stack

This catalog sits at the **Pattern & Selection Layer** of the agentic ecosystem. It helps users decide when OpenClaw is the appropriate runtime versus using a simpler script, an [n8n](../../services/n8n.md) flow, or a dedicated tool like [OpenHands](../../tools/development_ops/openhands.md). It leverages [FastMCP 3.0](../../architecture/multi_agent_knowledgeops.md) for low-latency tool discovery across these use cases.

## Typical use cases

- **Morning Briefing Assistant**: Aggregating weather, calendar events, and task lists into a single conversational summary using [Ralph's Family Context](../../reference-implementations/llm-prompts/family-context.md).
- **"Second Brain" Capture**: Processing bookmarks, notes, and links from various sources into a unified knowledge base via [SilverBullet](../../tools/intake_storage/silverbullet.md).
- **Nightly Research Digest**: Scheduled agents that search the web for specific topics and synthesize findings into a daily report.
- **Infrastructure Monitoring**: Performing periodic SSH-backed system checks and reporting anomalies to a chat channel like [Matrix](../../services/synapse.md).
- **Development Orchestration**: Coordinating multi-file changes and test runs via [Prompt Requests](prompt_requests.md) and [Gemma 3](../../tools/ai_knowledge/local_llms.md).

## Strengths

- **Practicality**: Based on long-running, real-world workflows rather than theoretical possibilities.
- **Safety-First**: Provides specific "Guardrails" for every use case to prevent unintended side effects.
- **Standardized Execution**: Uses MCP 3.0 Task Protocol to ensure skills work across different agent host environments.
- **Extensibility**: Skills are defined in YAML, making it easy to share and adapt catalog patterns for [Software Factories](software-factories.md).

## Limitations

- **User Bias**: Community examples often reflect the needs of "power users" and may be too complex for beginners.
- **Reliability Variance**: Not all documented workflows have the same level of production-grade stability.
- **Maintenance Overhead**: As the OpenClaw API and integrations evolve, these use cases require periodic refreshing.
- **Token Usage**: Complex recursive workflows in the catalog can quickly consume LLM token budgets.

## When to use it

- Use when designing a new agentic workflow and looking for established patterns and safety boundaries.
- Use to prioritize which agent capabilities to build first based on proven community success.
- Use when evaluating whether a complex automation task belongs in an autonomous agent or a traditional workflow tool like [n8n](../../services/n8n.md).

## When not to use it

- Don't use if the workflow is purely deterministic and better suited for a simple Python script or [n8n](../../services/n8n.md).
- Don't use for mission-critical industrial automation where human-in-the-loop (HITL) is not possible.
- Avoid when the primary requirement is absolute auditability with zero autonomous interpretation.

## Getting started

To begin using the patterns in this catalog:

1.  **Clone the Skill Repository**: Most catalog items reference skills available in the official OpenClaw skill library.
2.  **Select a Pattern**: Identify a use case (e.g., "Nightly Research Digest") from the table in the `Categorized use cases` section below.
3.  **Configure Environment**: Set the required API keys (e.g., Search, LLM) in your `.env` file.
4.  **Dry Run**: Run the skill with `dry_run: true` to inspect the proposed plan without executing actions.

## CLI examples

Interacting with catalog-inspired skills via the `openclaw` CLI:

```bash
# Execute the morning briefing skill
openclaw run morning_briefing --param city="London"

# List all available skills derived from the catalog
openclaw skills list

# Audit a skill for security guardrail compliance
openclaw audit skills/research_digest.yaml
```

## API examples

Programmatically invoking a use-case pattern via the OpenClaw Python SDK:

```python
from openclaw import OpenClawClient

client = OpenClawClient(api_key="your_key")

# Trigger a "Second Brain" capture workflow
response = client.execute_skill(
    skill_name="second_brain_capture",
    inputs={
        "url": "https://example.com/article",
        "tags": ["ai", "patterns"],
        "target": "obsidian"
    }
)

print(f"Workflow status: {response.status}")
```

## Categorized use cases

| Category | Use case | Why OpenClaw fits | Guardrail |
|---|---|---|---|
| Home-office | Morning briefing assistant | Good for collecting tasks, weather, reminders, and daily summaries across tools | Keep it read-only |
| Knowledge management | "Second brain" capture and recall | Works well when a conversational layer needs memory and retrieval over bookmarks, notes, and saved links | Make note-writing explicit |
| Research | Nightly research digest | Strong fit for scheduled search, summary, and digest workflows | Verify sources before external sharing |
| Content | Idea capture and content machine | Useful for capturing rough ideas, organizing them, and expanding into reusable drafts | Draft-only before publishing |
| Web work | URL summary and link processing | Efficient when a lightweight skill can summarize an article, PDF, or video from a link | Keep browsing isolated |
| Infrastructure | Server and service monitoring | Works well for SSH-backed checks plus human-readable reporting in chat | Require approval for fixes and restarts |
| Development | Coding remote PR prep | Helpful when conversational requests must turn into branch, commit, and PR actions | Never auto-merge without review |
| Communications | Email triage and draft replies | Good for classifying inbox traffic and drafting responses in the user's tone | Draft-only mode, never send directly |
| Operations | Daily life admin | Strong fit for errands, reminders, recurring personal tasks, and follow-up loops | Keep external side effects explicit |

## Related tools / concepts

- [OpenClaw](../../tools/development_ops/openclaw.md) — The primary runtime for these use cases.
- [n8n](../../services/n8n.md) — Visual workflow automation for deterministic paths.
- [OpenHands](../../tools/development_ops/openhands.md) — Specialized agent for coding-centric use cases.
- [Daily Briefing](../../reference-implementations/llm-prompts/daily-briefing.md) — Prompt template for the briefing use case.
- [Agentic Workflows](agentic-workflows.md) — Theoretical foundation for these patterns.
- [Prompt Requests](prompt_requests.md) — The preferred interface for development-centric use cases.
- [Software Factories](software-factories.md) — High-scale pattern for autonomous code generation.
- [MCP 3.0 Task Protocol](../../architecture/multi_agent_knowledgeops.md) — The standardized execution layer for catalog skills.
- [Gemma 3](../../tools/ai_knowledge/local_llms.md) — Recommended local reasoning engine for catalog use cases.

## Sources / References

- [OpenClaw automation examples and workflow notes](https://gist.github.com/ANcpLua/4ba21cd7f0bf08e0b483f3187dd93308)
- [OpenClaw after 50 days: all prompts for 20 real workflows](https://gist.github.com/velvet-shark/b4c6724c391f612c4de4e9a07b0a74b6)
- [awesome-openclaw-usecases](https://github.com/hesamsheikh/awesome-openclaw-usecases)

## Contribution Metadata

- Last reviewed: 2026-07-21
- Confidence: high
