# Sunsama

## What it is
A "guided daily planner" that helps professionals build a sustainable daily routine by pulling tasks from various tools into a unified, time-boxed schedule.

## What problem it solves
Combats burnout and fragmentation by encouraging intentional daily planning and limiting the number of tasks you commit to each day.

## Where it fits in the stack
**Category**: Calendar & Tasks / Unified Productivity

## Typical use cases
- Daily planning and time-blocking for deep work.
- Aggregating tasks from Jira, Trello, GitHub, and Email.
- Reflecting on daily accomplishments via a guided shutdown ritual.

## Strengths
- **Integrations**: High-quality integrations with major work platforms.
- **Workflow Focus**: Not just a list; it's a workflow for planning your day.
- **Clean UI**: Beautiful, distraction-free interface.

## Limitations
- **High Cost**: One of the most expensive personal productivity tools.
- **Manual Work**: Requires a few minutes of active planning every morning (intentional by design).

## When to use it
- If you struggle with over-commitment and need a tool that forces you to be realistic.
- If you want a "premium" planning experience.

## When not to use it
- If you are budget-conscious.
- If you prefer a completely automated, "set-it-and-forget-it" scheduler.

## Licensing and cost
- **Open Source**: No
- **Cost**: Paid (Subscription)
- **Self-hostable**: No

## Getting started
Sunsama is available as a web app, desktop app (macOS, Windows, Linux), and mobile app.

**Installation:**
```bash
# On macOS via Homebrew Cask
brew install --cask sunsama
```

**Hello-world example:**
After installation, use the `A` shortcut to add your first task to your daily plan:
`Review the KnowledgeOps handbook`

Note: Sunsama has no official public CLI documentation. CLI sections are skipped.

## API examples
Sunsama does not currently offer a public REST API for general development. Programmatic task creation is primarily handled via their official **Zapier integration**.

**Creating a task via Zapier (Conceptual):**
Users can generate a **Zapier Token** in their Sunsama settings to allow external automation tools to create tasks.

1. Generate token in `Settings > Zapier`.
2. In Zapier, select **Sunsama** as the Action App.
3. Use the "Create Task" event to map data from other services to Sunsama.

## Related tools / concepts
- [Akiflow](akiflow.md)
- [Morgen](morgen.md)
- [Motion](motion.md)

## Sources / References
- [Sunsama Official Site](https://sunsama.com/)
- [Sunsama Help Center: Zapier Integration](https://help.sunsama.com/docs/integrations/zapier/)

## Contribution Metadata
- Last reviewed: 2026-05-02
- Confidence: high
