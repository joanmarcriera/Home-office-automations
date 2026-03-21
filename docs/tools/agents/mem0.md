# mem0

## What it is
mem0 is a memory layer for AI agents and AI applications that stores and retrieves durable user, task, and workflow context over time.

## What problem it solves
It prevents every agent interaction from starting from zero. Instead of cramming long-term context into prompts, mem0 externalizes memory into a system that can be updated and retrieved as needed.

## Where it fits in the stack
**Agents / Memory Layer**. It sits between the model and application logic as persistent memory infrastructure for agents.

## Typical use cases
- Remembering user preferences across sessions
- Persisting account, project, or process context for agents
- Tracking multi-step work across long-running company workflows

## Strengths
- Clear fit for agent memory and personalization
- Useful for cross-session continuity
- Strong complement to workflow and browser agents

## Limitations
- Adds complexity if the workflow does not truly need persistence
- Poor memory design can create noisy or low-value recall

## When to use it
- When the same users, accounts, or projects recur over time
- When agents need to remember preferences, history, or prior decisions

## When not to use it
- When each task is isolated and stateless
- When a simple database table or CRM field is enough

## Example company use cases
- **Sales assistant**: remember preferred outreach angles, prior objections, and account stage per lead.
- **Ops assistant**: remember vendor-specific quirks, invoice routing rules, and approval boundaries.
- **Content team**: remember channel voice, past winning hooks, and audience-specific formatting preferences.

## Selection comments
- Use **mem0** when you need long-lived memory that should survive across sessions.
- Use **Supabase** when you need general app state and relational data but not specialized memory behavior.
- Use **n8n** when you need process execution and scheduling, not memory by itself.

## Related tools / concepts

- [Browser Use](../automation_orchestration/browser-use.md)
- [n8n](../../services/n8n.md)
- [Supabase](../infrastructure/supabase.md)

## Sources / References
- [GitHub Repository](https://github.com/mem0ai/mem0)

## Contribution Metadata
- Last reviewed: 2026-03-14
- Confidence: medium
