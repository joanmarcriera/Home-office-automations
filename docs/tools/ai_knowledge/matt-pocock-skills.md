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
/grill-me

# Use Test-Driven Development loop
/tdd

# Diagnose a complex bug
/diagnose

# Setup skill
/setup-matt-pocock-skills
```

## Related tools / concepts

- [Andrej Karpathy Skills](karpathy-skills.md)
- [Claude Code](../development_ops/claude-code.md)
- [Claude Skills Ecosystem](../agents/claude-skills-ecosystem.md)
- [Superpowers](../agents/superpowers.md)

## Sources / references
- [Matt Pocock Skills (GitHub)](https://github.com/mattpocock/skills)

## Contribution Metadata
- Last reviewed: 2026-05-02
- Confidence: high
