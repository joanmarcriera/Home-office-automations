# Claude Plugins

## What it is
Claude plugins are community-distributed extensions that package extra commands, tools, or integrations around Claude Code workflows. As of June 2026, they represent a mature ecosystem for extending the capabilities of **Claude 4.7** and other agentic models within the terminal and development environments.

## What problem it solves
They make common add-ons easier to install and reuse instead of copying prompts, scripts, or workflow glue by hand across repos. They solve:
- **Capability Gaps**: Quickly adding specialized tools like browser automation or database access.
- **Workflow Standardization**: Enforcing consistent review or testing patterns across a team.
- **Integration Friction**: Simplifying the connection between Claude and external services like GitHub, Slack, or Jira.

## Where it fits in the stack
Claude Plugins sit in the **Development & Ops / Extension Ecosystem** layer. This is an ecosystem layer around [Claude Code](claude-code.md) rather than a standalone product.

## Typical use cases
- Installing shared tool integrations such as browser automation via [Browser Use](../automation_orchestration/browser-use.md).
- Reusing workflow packs across multiple repos or teams.
- Standardizing local coding-agent environments using [Superpowers](../agents/superpowers.md).
- Integrating with **Model Context Protocol (MCP)** servers to expose local data.

## Strengths
- Faster reuse of community integrations.
- Encourages distribution of packaged workflows instead of ad hoc snippets.
- Native integration with the Claude Code CLI.
- Large and active community registry.

## Limitations
- Quality and maintenance vary widely across community plugins.
- Plugins should be reviewed like code because they can shape tool access and execution behavior.
- Potential for overlapping tool definitions if multiple plugins are installed without care.

## When to use it
- When you want fast installation of reviewed extensions to boost agent productivity.
- When you need to bridge Claude Code with specific external tools or internal APIs.
- To maintain consistency in how agents interact with your codebase.

## When not to use it
- When you cannot audit community tooling or must minimize third-party trust.
- In highly restricted environments where external plugin execution is prohibited.

## Core Plugin Registry (Examples)

### Browser Use Plugin
- **What it is**: Connects Claude Code to the Playwright-based [Browser Use](../automation_orchestration/browser-use.md) library.
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
| `connect-apps` | Connect Claude Code to GitHub, Slack, Notion, Gmail, etc. | Cross-app project and operations workflows | Review OAuth scopes and workspace permissions. |
| `agentlint` | Check whether a repo is friendly to AI agents | Repos using `AGENTS.md`, `CLAUDE.md`, or structured docs | Run before adding more automation. |
| `code-review` | Run structured PR reviews before shipping | Teams that want a second-pass review from an agent | Treat as a reviewer aid, not a replacement. |
| `test-writer-fixer` | Generate and repair unit tests (Jest, Pytest, etc.) | Codebases with weak regression coverage | Pair with real test commands for verification. |
| `debugger` | Investigate complex bugs, logs, traces, and failing flows | Failures where the first stack trace is not enough | Give it exact reproduction commands. |
| `bug-fix` | Analyse stack traces and apply targeted fixes | Narrow failures with clear error output | Keep diffs small and verify after patching. |
| `mcp-builder` | Scaffold and iterate on [MCP](../automation_orchestration/mcp.md) servers | Teams exposing internal tools or services | Start with one small read-only tool. |
| `theme-factory` | Generate or adapt UI themes | Frontend projects needing consistent visual tokens | Review output against the app design system. |

## Getting started

### Installing a Plugin
Plugins are typically installed via the Claude Code CLI:
```bash
claude plugin add <plugin-name>
```

### Listing Installed Plugins
See what extensions are currently active in your environment:
```bash
claude plugin list
```

## CLI examples

### Running a Plugin Command
Many plugins expose new top-level commands to Claude:
```bash
claude browser-use "Search for the latest Claude 4.7 features"
```

### Checking Plugin Health
Verify that all installed plugins are correctly configured:
```bash
claude plugin doctor
```

### Updating Plugins
Keep your extensions up to date with the latest security and feature patches:
```bash
claude plugin update --all
```

## API examples

### Python: Creating a Custom Skill
While not a "plugin" in the distribution sense, creating a skill is the first step to building a plugin:

```python
# skills/documentation_audit.py
def audit_doc(filepath: str) -> str:
    """Audits a markdown file for KnowledgeOps compliance."""
    # Logic to check for Last reviewed date and headers
    return "Audit complete: Pass"

# Registering this skill in CLAUDE.md or via a plugin manifest
```

### JSON: Plugin Manifest (Example)
The structure of a community-distributed Claude plugin:

```json
{
  "name": "knowledge-ops-helper",
  "version": "1.2.0",
  "description": "Tools for maintaining KnowledgeOps standards",
  "commands": [
    {
      "name": "audit",
      "description": "Run the KnowledgeOps audit script",
      "exec": "python3 scripts/audit_docs_quality.py"
    }
  ],
  "mcp_servers": ["http://localhost:8000/mcp"]
}
```

## Related tools / concepts
- [Claude Code](claude-code.md) - The primary CLI for running these plugins.
- [Claude Hooks](claude-hooks.md) - Event-based automation within Claude Code.
- [Claude Skills Ecosystem](../agents/claude-skills-ecosystem.md) - The broader landscape of agent capabilities.
- [Browser Use](../automation_orchestration/browser-use.md) - High-level web automation library.
- [Chronos MCP](../automation_orchestration/chronos-mcp.md) - Time-based task orchestration.
- [Superpowers](../agents/superpowers.md) - Identity and skill management framework.
- [MCP (Model Context Protocol)](../automation_orchestration/mcp.md) - The underlying protocol for tool and resource exchange.

## Sources / References
- [awesomeclaude.ai](https://awesomeclaude.ai/)
- [AI Templates](https://www.aitmpl.com/)
- [Superpowers](https://github.com/obra/superpowers)
- [Awesome Claude Plugins](https://github.com/ComposioHQ/awesome-claude-plugins)
- [Issue #404 source discussion](https://github.com/joanmarcriera/Home-office-automations/issues/404)

## Contribution Metadata
- Last reviewed: 2026-06-08
- Confidence: high
