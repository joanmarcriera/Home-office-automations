# Claude Context Mode

## What it is
Claude Context Mode refers to community and workflow patterns for giving Claude Code richer, better-structured operating context, often through MCP servers, repository memory files, and scoped task documents. It is the practice of "context engineering" specifically for agentic coding workflows.

## What problem it solves
It reduces prompt sprawl and makes agent behavior more repeatable than pasting large amounts of context into every session. It solves the "context window amnesia" problem by ensuring the agent has access to a durable, versioned source of truth about the project's architecture, standards, and progress.

## Where it fits in the stack
**Development & Ops / Context Engineering Pattern**. It is a practical operating pattern around Claude Code, MCP, and AI-native IDEs (like Cursor or VS Code with Continue).

## Typical use cases
- **Repository Onboarding**: Giving an agent a high-level map of a new codebase.
- **Architectural Guardrails**: Ensuring the agent follows specific design patterns (e.g., "always use FastAPI dependency injection").
- **Task Persistence**: Resuming a complex, multi-day coding task across different chat sessions.

## Strengths
- **Consistency**: Agent behavior becomes more predictable across sessions.
- **Efficiency**: Reduces the amount of manual context pasting required.
- **Versionable**: Context files (like `MEMORY.md` or `AGENTS.md`) live in the repo and evolve with the code.

## Limitations
- **Maintenance Overhead**: Requires human (or agent) discipline to keep context files up to date.
- **Noise**: Poorly designed context layers can still overwhelm the model and cause "distraction" from the immediate task.

## When to use it
- When working on complex, long-running projects where architectural consistency is critical.
- When collaborating with multiple agents or human-agent teams.
- When you need to provide the agent with external tool context via MCP.

## When not to use it
- For trivial, one-off scripts where the overhead of creating context files exceeds the task effort.
- When the task is simple enough for the agent to infer everything from local file context alone.

## Implementation Pattern: The Repository Memory

A common pattern is maintaining a `MEMORY.md` or `AGENTS.md` at the root of the repository.

### Example `AGENTS.md` Structure
```markdown
# Agent Instructions

## Project Overview
This is a Next.js application using Tailwind CSS and Prisma.

## Coding Standards
- Use functional components.
- All API routes must be in `src/app/api`.
- Use Zod for schema validation.

## Current Sprint
- [x] Implement User Auth
- [x] Refactor Task Dashboard
- [x] Add Email Notifications

### Example Skill: Email Notification Wrapper
You can define a "skill" for the agent to use when specific conditions are met, ensuring it follows the repository's notification standards.

```markdown
# Skill: send_deployment_email

## Summary
Send a standardized email notification after a successful production deployment.

## Triggers
- When the `deploy_prod` workflow completes successfully.

## Instructions
1. Retrieve the list of changes from `CHANGELOG.md`.
2. Format the email using the template in `templates/email/deployment_alert.html`.
3. Send to `dev-alerts@example.com` via the SMTP MCP server.
```

### Implementing Email Notifications
To implement the "Email Notifications" task from the memory file, the agent uses the configured SMTP MCP server and follows the `templates/` directory structure.

```bash
# Example command for the agent to send the notification
mcp use smtp-server send_email \
  --to "dev-alerts@example.com" \
  --subject "Production Deployment Successful" \
  --body "New features: $(cat CHANGELOG.md | head -n 10)"
```

## Context Mapping
- Documentation: `/docs`
- Schemas: `/src/lib/schemas`
```

## Technical Integration: Claude Config

You can automate the loading of this context by using environment variables or wrapper scripts when starting Claude Code sessions.

```bash
# Example wrapper to inject repo memory
alias claude-pro='claude --prompt "Project context: $(cat AGENTS.md)"'
```

## Practical Tips
- Use **Checkpoints**: At the end of a session, ask the agent to update the `MEMORY.md` file with its progress.
- **Modularize Context**: Keep architectural standards separate from task-specific progress.
- **MCP for Dynamic Context**: Use MCP servers to fetch real-time data (like Jira tickets or GitHub PRs) into the context mode.

## Related tools / concepts
- [Claude Code](claude-code.md)
- [Tool Calling and MCP](../../knowledge_base/patterns/tool-calling-and-mcp.md)
- [Claude Hooks](claude-hooks.md)
- [OpenClaw Workflow Prompts](../../knowledge_base/patterns/openclaw-workflow-prompts.md)
- [Standards and Conventions](../../standards-and-conventions.md)
- [Architecture Index](../../ARCHITECTURE.md)

## Sources / References
- [awesomeclaude.ai](https://awesomeclaude.ai/)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Claude Desktop Documentation](https://docs.anthropic.com/claude/docs/claude-desktop-overviews)

## Contribution Metadata
- Last reviewed: 2026-05-15
- Confidence: high
