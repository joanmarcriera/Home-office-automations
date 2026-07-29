# Claude Plugins

## What it is
Claude plugins are community-distributed extensions that package extra commands, tools, or integrations around Claude Code workflows. As of late 2026, they represent a mature ecosystem for extending the capabilities of **Claude 5.1** and other agentic frontier models (such as **GPT-5.5** and **Gemini 4.0**) within terminal environments and development workflows.

## What problem it solves
They make common add-ons easier to install and reuse instead of copying prompts, scripts, or workflow glue by hand across repos. They solve:
- **Capability Gaps**: Quickly adding specialized tools like browser automation or database access.
- **Workflow Standardization**: Enforcing consistent review or testing patterns across a team.
- **Integration Friction**: Simplifying the connection between Claude and external services like GitHub, Slack, or Jira.

## Where it fits in the stack
Claude Plugins sit in the **Development & Ops / Extension Ecosystem** layer. This is an ecosystem layer around [Claude Code](claude-code.md) rather than a standalone product.

## Typical use cases
- **Web Orchestration**: Installing shared tool integrations such as browser automation via [Browser Use](../automation_orchestration/browser-use.md).
- **Environment Standardization**: Reusing workflow packs across multiple repos or teams.
- **Skill Discovery**: Standardizing local coding-agent environments using [Superpowers](../agents/superpowers.md).
- **Data Access**: Integrating with **Model Context Protocol (MCP 3.1)** servers to expose local data.
- **Automated Quality**: Running [Agentlint](../agents/agentlint.md) to check whether a repo is friendly to AI agents.
- **PR Review**: Using `code-review` plugins to run structured PR reviews before shipping.
- **Bug Remediation**: Utilizing `debugger` and `bug-fix` plugins to investigate complex failures and apply targeted patches.

### Notable Plugins & Starters
| Plugin | Primary job | Best fit |
| :--- | :--- | :--- |
| `browser-use` | Live web research and multi-site orchestration | Automating data extraction from websites without an API |
| `chronos-mcp` | Advanced time-based scheduling and task management | Managing multi-calendar synchronization |
| `connect-apps` | Connect Claude Code to GitHub, Slack, Notion, Gmail | Cross-app project and operations workflows |
| `test-writer-fixer` | Generate and repair unit tests (Jest, Pytest, etc.) | Codebases with weak regression coverage |
| `mcp-builder` | Scaffold and iterate on [MCP](../automation_orchestration/mcp.md) servers | Teams exposing internal tools or services |

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

### Creating a Custom Skill
While not a "plugin" in the distribution sense, creating a skill is the first step to building a plugin:

```python
# skills/documentation_audit.py
def audit_doc(filepath: str) -> str:
    """Audits a markdown file for KnowledgeOps compliance."""
    # Logic to check for Last reviewed date and headers
    return "Audit complete: Pass"

# Registering this skill in CLAUDE.md or via a plugin manifest
```

## CLI examples

### Running a Plugin Command
Many plugins expose new top-level commands to Claude:
```bash
claude browser-use "Search for the latest Claude 5.1 features"
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

### Programmatic Python Plugin Config Validator (Pydantic v2)
Ensure community plugins conform to schema specifications:

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class Command(BaseModel):
    name: str = Field(..., description="The command name")
    description: str = Field(..., description="Short explanation of command capability")
    exec: str = Field(..., description="Local command to run")

class PluginManifest(BaseModel):
    name: str = Field(..., description="Package name of the Claude plugin")
    version: str = Field(..., description="SemVer string")
    description: str = Field(..., description="Usage info")
    commands: List[Command] = Field(default_factory=list, description="Exposed CLI tools")
    mcp_servers: Optional[List[str]] = Field(default=None, description="Associated MCP endpoint URLs")

# Example validation
manifest_data = {
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

manifest = PluginManifest.model_validate(manifest_data)
print(f"Validated plugin: {manifest.name} v{manifest.version}")
```

## Related tools / concepts
- [Claude Code](claude-code.md) - The primary CLI for running these plugins.
- [Claude Hooks](claude-hooks.md) - Event-based automation within Claude Code.
- [Claude Skills Ecosystem](../agents/claude-skills-ecosystem.md) - The broader landscape of agent capabilities.
- [Browser Use](../automation_orchestration/browser-use.md) - High-level web automation library.
- [Chronos MCP](../automation_orchestration/chronos-mcp.md) - Time-based task orchestration.
- [Superpowers](../agents/superpowers.md) - Identity and skill management framework.
- [MCP (Model Context Protocol)](../automation_orchestration/mcp.md) - The underlying protocol for tool and resource exchange.
- [Aider](aider.md) - Terminal-native pair programmer.
- [Plandex](plandex.md) - Plan-first engineering engine.

## Sources / references
- [awesomeclaude.ai](https://awesomeclaude.ai/)
- [AI Templates](https://www.aitmpl.com/)
- [Superpowers](https://github.com/obra/superpowers)
- [Awesome Claude Plugins](https://github.com/ComposioHQ/awesome-claude-plugins)
- [Issue #404 source discussion](https://github.com/joanmarcriera/Home-office-automations/issues/404)

## Contribution Metadata
- Last reviewed: 2026-11-01
- Confidence: high
