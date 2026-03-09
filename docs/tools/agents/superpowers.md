# Superpowers

Superpowers is a comprehensive software development workflow and agentic skills framework designed for coding agents like Claude Code, Cursor, and Codex. It builds on top of composable "skills" to enforce a rigorous engineering process.

## When to use it

- To enforce high-quality engineering standards (TDD, YAGNI, DRY) in agent-driven development.
- When you want agents to work autonomously for extended periods (hours) without deviating from a plan.
- For complex projects that require a systematic approach to design, planning, and implementation.

## When not to use it

- For trivial code changes or simple questions.
- If you prefer an ad-hoc, conversational approach to coding without structured planning.

## Key Workflow Components

1.  **Brainstorming**: Socratic design refinement before writing code.
2.  **Isolated Workspaces**: Uses Git worktrees to ensure a clean baseline.
3.  **Bite-sized Planning**: Breaks work into 2-5 minute tasks with exact file paths and verification steps.
4.  **Subagent-Driven Development**: Dispatches fresh subagents per task with two-stage reviews.
5.  **Strict TDD**: Enforces RED-GREEN-REFACTOR cycle.
6.  **Formal Code Review**: Automated reviews against the plan before merging.

## Getting started

### Installation

Installation methods vary by platform:

#### Claude Code (via Plugin Marketplace)
```bash
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

#### Cursor
Install via the Cursor Agent plugin marketplace: `/plugin-add superpowers`.

#### Codex / OpenCode
Follow platform-specific instructions to fetch the skill files from the [official repository](https://github.com/obra/superpowers).

## Related tools / concepts
- [Claude Code](../development_ops/claude-code.md)
- [Anthropic Agent Skills](anthropic-agent-skills.md)

## Sources / References

- [Official GitHub Repository](https://github.com/obra/superpowers)
- [Superpowers for Claude Code (Blog Post)](https://blog.fsck.com/2025/10/09/superpowers/)
- [Anthropic Agent Skills Specification](https://agentskills.io/)

## Contribution Metadata
- Last reviewed: 2026-03-09
- Confidence: high
