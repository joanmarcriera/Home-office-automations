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

## Recommended Claude Code Plugin Starters

Start with plugins that match the workflow already in use. Do not install every community plugin at once; overlapping repo instructions, hooks, and tool permissions can make agent behaviour harder to reason about.

| Plugin | Primary job | Best fit | Adoption note |
| :--- | :--- | :--- | :--- |
| `connect-apps` | Connect Claude Code to GitHub, Slack, Notion, Gmail, and other work apps | Cross-app project and operations workflows | Review OAuth scopes and workspace permissions before enabling broad access. |
| `agentlint` | Check whether a repo is friendly to AI agents | Repos using `AGENTS.md`, `CLAUDE.md`, tool manifests, or structured docs | Run before adding more automation so missing context is fixed at the repo level. |
| `code-review` | Run structured PR reviews before shipping | Teams that want a second-pass review from an agent | Treat as a reviewer aid, not a replacement for required human review on risky changes. |
| `test-writer-fixer` | Generate and repair unit tests across Jest, Vitest, Pytest, and similar frameworks | Codebases with weak regression coverage | Pair with the real test command so generated tests prove behaviour rather than only compile. |
| `debugger` | Investigate complex bugs, logs, traces, and failing flows | Failures where the first stack trace is not enough | Give it exact reproduction commands and current logs. |
| `bug-fix` | Analyse stack traces and apply targeted fixes | Narrow failures with clear error output | Keep diffs small and require verification after patching. |
| `mcp-builder` | Scaffold and iterate on Model Context Protocol servers | Teams exposing internal tools or services to agents | Start with one small read-only tool before granting write capabilities. |
| `theme-factory` | Generate or adapt UI themes | Frontend projects that need consistent visual tokens | Review output against the app design system before accepting generated styles. |

## Suggested adoption order

1. `agentlint` to improve repository readiness.
2. `code-review` and `test-writer-fixer` for quality gates.
3. `debugger` and `bug-fix` for repair loops.
4. `connect-apps` only after permissions and audit expectations are clear.
5. `mcp-builder` when the team has a real internal tool to expose.
6. `theme-factory` when a frontend project needs repeatable theme work.

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
- [Awesome Claude Plugins](https://github.com/ComposioHQ/awesome-claude-plugins)
- [Issue #404 source discussion](https://github.com/joanmarcriera/Home-office-automations/issues/404)

## Contribution Metadata
- Last reviewed: 2026-05-11
- Confidence: high
