# Claude Hooks

## What it is
Claude hooks are community patterns and scripts that run around Claude Code sessions to add policy checks, notifications, automation, and guardrails.

## What problem it solves
They let teams enforce workflow behavior outside the model prompt itself, which is often more reliable for guardrails and repetitive operational glue.

## Where it fits in the stack
**Development & Ops / Workflow Guardrails**. Hooks sit around the coding-agent loop rather than inside the generated output.

## Typical use cases
- Notifications on task completion or failures
- Policy and safety checks before execution
- Repo-specific workflow automation

## Strengths
- Better for deterministic enforcement than prompt-only instructions
- Useful for observability and local workflow automation

## Limitations
- Hook logic can become a hidden layer of behavior if poorly documented
- Bad hooks can be as disruptive as bad plugins

## When to use it
- When you need repeatable, deterministic guardrails around agent execution

## When not to use it
- When prompt instructions are sufficient and simplicity matters more

## Related tools / concepts
- [Claude Code](claude-code.md)
- [Claude Plugins](claude-plugins.md)
- [Playwright](playwright.md)

## Sources / References
- [Claude Hooks Repository](https://github.com/johnlindquist/claude-hooks)
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)

## Contribution Metadata
- Last reviewed: 2026-03-14
- Confidence: medium
