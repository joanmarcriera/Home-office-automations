# Matt Pocock Skills

## What it is
A repository of specialized skills for AI agents, including the "Grill-me" skill for rigorous plan verification.

## What problem it solves
Extends agent capabilities with domain-specific execution scaffolds and critical thinking tools.

## Where it fits in the stack
**Category**: AI & Knowledge / Agent Skills

## Typical use cases
- **Plan Verification**: Using `Grill-me` to ensure a proposed solution is robust before execution.
- **TDD Workflows**: Automating the Red-Green-Refactor loop with specialized skills.
- **Complex Bug Diagnosis**: Leveraging multi-step diagnostic patterns for elusive issues.

## Strengths
- **Action-Oriented**: Provides concrete execution scaffolds rather than just passive advice.
- **Critical Thinking**: Specifically designed to force agents to "think twice" before acting.
- **Standardized**: Uses the `skills.sh` pattern for easy installation and updates.

## Limitations
- **Setup Required**: Requires specific installation steps and sometimes tool configuration.
- **Learning Curve**: Agents may need specific instructions to effectively utilize some of the deeper skills.

## When to use it
- When you need a "staff engineer" level of rigor from your AI assistant.
- For complex projects that benefit from structured planning and TDD.

## When not to use it
- For quick, trivial scripts where the overhead of a "Grill-me" session is overkill.
- If you prefer a completely custom, non-standardized skill setup.

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free
- **Self-hostable**: Yes

## Key Skills
- **Grill-me**: A skill used to cross-examine and verify a proposed plan before execution. Getting the agent to ask detailed questions about what you are building to fix the communication gap between you and the agent.
- **Triage**: Uses labels to help triage tickets in your issue tracker.
- **TDD**: Implements a strict Red-Green-Refactor loop, refusing to write implementation code until a failing test exists.
- **Diagnose**: Runs a multi-point inspection of the environment and code to find the root cause of a failure.

## Getting started

### Installation
Matt Pocock's skills can be installed using the `skills.sh` installer:

```bash
npx skills@latest add mattpocock/skills
```

### Basic usage
After installation, run the setup skill in your agent:

```bash
/setup-matt-pocock-skills
```

This will guide you through configuring your issue tracker and document storage preferences.

## CLI examples
Use the skills directly within your AI agent's interactive session:

```bash
# Verify a plan before execution
# Agent will ask 3-5 challenging questions about your approach
/grill-me

# Use Test-Driven Development loop
# 1. Write failing test 2. Write code 3. Refactor
/tdd

# Diagnose a complex bug
# Agent runs logs, checks versions, and traces execution
/diagnose

# Setup skill
/setup-matt-pocock-skills
```

## Thinking Pattern: The "Grill-me" Session
Before starting a 2-hour refactor, the user triggers `/grill-me`.

**Agent Interaction:**
1. **User**: "I'm going to migrate the database to Prisma."
2. **Agent (/grill-me)**:
   - "How will you handle existing data migration?"
   - "What is the rollback plan if the Prisma schema generation fails in CI?"
   - "Have you considered the performance impact of Prisma's query engine on our edge functions?"
3. **User**: *Answers questions, refining the plan.*
4. **Agent**: "Plan verified. Proceeding with migration."

## Related tools / concepts

- [Andrej Karpathy Skills](karpathy-skills.md)
- [Claude Code](../development_ops/claude-code.md)
- [Claude Skills Ecosystem](../agents/claude-skills-ecosystem.md)
- [Superpowers](../agents/superpowers.md)

## Sources / references
- [Matt Pocock Skills (GitHub)](https://github.com/mattpocock/skills)
- [Total TypeScript - Professional AI Workflows](https://www.totaltypescript.com/)

## Contribution Metadata
- Last reviewed: 2026-05-11
- Confidence: high
