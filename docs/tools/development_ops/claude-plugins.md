# Claude Plugins

## What it is
Claude Plugins are modular, community-distributed extension packages designed to extend the capabilities of **Claude Code** and other agentic execution platforms. As of early 2027, the plugin architecture has matured into a standard extension ecosystem for frontier models including **Claude 5.1**, **GPT-5.5**, and **Gemini 4.0 Pro**. Claude Plugins package specialized CLI tools, workflow prompts, custom skills, and **FastMCP 3.1** server bindings into shareable, versioned bundles.

## What problem it solves
Configuring ad-hoc terminal scripts, copying prompt templates manually across repositories, or repeatedly wiring up external API integrations creates workflow fragmentation and maintenance overhead. Claude Plugins solve this by standardizing capability packaging. They enable developers to install pre-built integrations for web research, code reviews, automated testing, or database inspection with single CLI commands while maintaining governance and auditability.

## Where it fits in the stack
**Development & Ops / Extension Ecosystem**. Claude Plugins sit as an extension layer on top of [Claude Code](claude-code.md) and compatible terminal agents, connecting the base model with external developer tools, continuous integration systems, and local development environments.

## Typical use cases
- **Web Orchestration & Scraping**: Adding web research and automated DOM interactions via integrations like [Browser Use](../automation_orchestration/browser-use.md).
- **Automated PR Reviews**: Installing code review plugins that analyze diffs against repository standards before committing.
- **Test Generation & Repair**: Employing plugins that execute `pytest` or `jest` suites, capture tracebacks, and apply targeted bug fixes automatically.
- **FastMCP 3.1 Binding**: Connecting local or remote Model Context Protocol servers to expose enterprise APIs and data stores.
- **Skill Governance**: Standardizing enterprise developer workflows across engineering teams using [Superpowers](../agents/superpowers.md).

### Notable Plugins & Starters
| Plugin | Primary Job | Best Fit |
| :--- | :--- | :--- |
| `browser-use` | Live web research and multi-site orchestration | Automating web data extraction without native REST APIs |
| `chronos-mcp` | Advanced time-based scheduling and task management | Multi-calendar synchronization and cron task triggers |
| `connect-apps` | Connect Claude Code to GitHub, Slack, Notion, Jira | Cross-application project management and telemetry |
| `test-writer-fixer` | Generate and repair unit test suites (Pytest, Jest) | Legacy codebases with deficient test coverage |
| `mcp-builder` | Scaffold and iterate on [FastMCP](../automation_orchestration/mcp.md) servers | Engineering teams building internal tooling endpoints |

## Strengths
- **Rapid Ecosystem Reuse**: Instantly endows Claude Code with complex capabilities without writing custom boilerplate.
- **Package Standardization**: Versioned manifest specifications ensure predictable command interfaces and dependencies.
- **Native FastMCP 3.1 Support**: Direct bridging with Model Context Protocol servers for secure resource and tool access.
- **Developer Productivity**: Eliminates repetitive prompt setup and custom script wrapping across projects.

## Limitations
- **Security Audit Requirement**: Untrusted community plugins must be carefully audited to prevent unauthorized file access or credential leaks.
- **Overlapping Tool Definitions**: Installing multiple plugins with overlapping function signatures can cause model tool selection ambiguity.
- **Environment Drift**: Dependencies within plugins (e.g., node modules or python packages) require periodic updates.

## When to use it
- When equipping terminal coding agents with reusable, enterprise-approved workflows and external tools.
- When standardizing development practices, linter hooks, or code review protocols across software engineering teams.
- When connecting [Claude Code](claude-code.md) to internal infrastructure via FastMCP 3.1 endpoints.

## When not to use it
- In strictly locked-down production environments where installing dynamic third-party extensions is prohibited.
- For simple, one-off bash commands where standard system binaries suffice.

## Getting started

### Installing a Plugin
Install plugins directly via the Claude Code CLI plugin manager:

```bash
claude plugin add browser-use
```

### Listing Active Plugins
Inspect active plugins and their exposed capabilities:

```bash
claude plugin list
```

### Creating a Local Custom Skill
Expose a project-specific skill script that can be packaged into a plugin:

```python
# skills/doc_validator.py
import sys
from pydantic import BaseModel, Field

class AuditResult(BaseModel):
    filepath: str
    status: str = Field(default="compliant")

def validate_file(path: str) -> None:
    print(f"Auditing file: {path}")
    result = AuditResult(filepath=path)
    print(f"Audit output: {result.model_dump_json()}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        validate_file(sys.argv[1])
```

## CLI examples

### Executing Plugin Commands
Run a plugin-provided top-level command inside Claude Code:

```bash
claude browser-use "Search for the latest Claude 5.1 release notes and synthesize changes"
```

### Plugin Health Inspection
Verify plugin configuration, dependencies, and MCP server bindings:

```bash
claude plugin doctor
```

### Batch Plugin Update
Upgrade all installed plugins to their latest secure releases:

```bash
claude plugin update --all
```

## API examples

### JSON: Plugin Manifest Specification
An example manifest defining a custom KnowledgeOps helper plugin:

```json
{
  "name": "knowledge-ops-helper",
  "version": "1.5.0",
  "description": "Tools and MCP endpoints for maintaining KnowledgeOps standards",
  "commands": [
    {
      "name": "audit",
      "description": "Execute KnowledgeOps quality audit script",
      "exec": "python3 scripts/audit_docs_quality.py"
    }
  ],
  "mcp_servers": [
    "http://localhost:8000/mcp"
  ]
}
```

### Programmatic Python Plugin Manifest Validation (Pydantic v2)
Validate plugin manifest schemas programmatically before deployment:

```python
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional

class PluginCommand(BaseModel):
    name: str = Field(..., description="Unique command name")
    description: str = Field(..., description="Summary of tool purpose")
    exec: str = Field(..., description="Local system execution command")

class PluginManifest(BaseModel):
    name: str = Field(..., description="Package name")
    version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$", description="SemVer version")
    description: str = Field(..., description="Plugin description")
    commands: List[PluginCommand] = Field(default_factory=list)
    mcp_servers: Optional[List[str]] = Field(default=None)

# Sample manifest verification
manifest_payload = {
    "name": "knowledge-ops-helper",
    "version": "1.5.0",
    "description": "Tools and MCP endpoints for maintaining KnowledgeOps standards",
    "commands": [
        {
            "name": "audit",
            "description": "Execute KnowledgeOps quality audit script",
            "exec": "python3 scripts/audit_docs_quality.py"
        }
    ],
    "mcp_servers": ["http://localhost:8000/mcp"]
}

manifest = PluginManifest.model_validate(manifest_payload)
print(f"Validated Plugin: {manifest.name} (v{manifest.version}) with {len(manifest.commands)} commands.")
```

## Related tools / concepts
- [Claude Code](claude-code.md) — The primary terminal interface for executing plugins.
- [Claude Hooks](claude-hooks.md) — Event-driven middleware for agent session guardrails.
- [Browser Use](../automation_orchestration/browser-use.md) — Web automation library frequently packaged as a plugin.
- [Superpowers](../agents/superpowers.md) — Skill and identity management framework for agents.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Core protocol for tool and context interoperability.

## Sources / references
- [Official Claude Code Documentation](https://docs.anthropic.com/claude/docs/claude-code)
- [Awesome Claude Plugins Repository](https://github.com/ComposioHQ/awesome-claude-plugins)
- [FastMCP 3.1 Protocol Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
