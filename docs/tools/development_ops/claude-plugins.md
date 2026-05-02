# Claude Plugins

## What it is
Claude plugins are community-distributed extensions that package extra commands, tools, or integrations around Claude Code workflows.

## What problem it solves
They make common add-ons easier to install and reuse instead of copying prompts, scripts, or workflow glue by hand across repos.

## Where it fits in the stack
**Development & Ops / Extension Ecosystem**. This is an ecosystem layer around Claude Code rather than a standalone product.

## Typical use cases
- Installing shared tool integrations such as browser automation
- Reusing workflow packs across multiple repos or teams
- Standardizing local coding-agent environments

## Strengths
- Faster reuse of community integrations
- Encourages distribution of packaged workflows instead of ad hoc snippets

## Limitations
- Quality and maintenance vary widely
- Plugins should be reviewed like code because they can shape tool access and execution behavior

## When to use it
- When you want fast installation of reviewed extensions

## When not to use it
- When you cannot audit community tooling or must minimize third-party trust

## Core Plugin Registry (Examples)

### Browser Use Plugin
- **What it is**: Connects Claude Code to the Playwright-based browser-use library.
- **Problem it solves**: Allows the agent to perform live web research and multi-site orchestration.
- **Typical Use Case**: Automating data extraction from websites without an API.

### Chronos MCP
- **What it is**: A plugin/server for advanced time-based scheduling and task management.
- **Problem it solves**: Adds native understanding of complex date-time logic and scheduling workflows.
- **Typical Use Case**: Managing multi-calendar synchronization and deadline reminders.

### Superpowers
- **What it is**: An extension framework for adding custom skills and identity management to Claude.
- **Problem it solves**: Standardizes how high-level skills (like documentation writing or code refinement) are discovered and executed.
- **Typical Use Case**: Enterprise-wide standardization of agent behaviors.

## Related tools / concepts
- [Claude Code](claude-code.md)
- [Claude Hooks](claude-hooks.md)
- [Claude Skills Ecosystem](../agents/claude-skills-ecosystem.md)
- [Browser Use](../automation_orchestration/browser-use.md)
- [Chronos MCP](../automation_orchestration/chronos-mcp.md)
- [Superpowers](../agents/superpowers.md)

## Sources / References
- [awesomeclaude.ai](https://awesomeclaude.ai/)
- [AI Templates](https://www.aitmpl.com/)
- [Superpowers](https://github.com/obra/superpowers)

## Contribution Metadata
- Last reviewed: 2026-05-11
- Confidence: high
