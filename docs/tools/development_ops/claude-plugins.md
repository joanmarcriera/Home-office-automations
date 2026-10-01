# Claude Plugins

## What it is
Claude plugins are standardized, community-distributed extension packages that encapsulate extra commands, tools, workflow hooks, and FastMCP 3.1 server definitions around Claude Code and terminal agent environments. As of early 2027, they represent a mature ecosystem for extending the agentic capabilities of **Claude 5.1** and other model architectures (such as **GPT-5.5** and **Gemini 4.0 Pro**) directly within development environments.

By standardizing installation manifests, runtime lifecycle management, and sandboxed tool execution, Claude Plugins eliminate the need for engineers to manually paste prompt templates, copy ad-hoc Python scripts, or stitch together fragile terminal hooks across multiple repositories.

```
+-----------------------------------------------------------------------------------+
|                            DEVELOPER TERMINAL / ENVIRONMENT                       |
|                       (Claude Code CLI / Cursor / VS Code Agent)                  |
+------------------------------------------+----------------------------------------+
                                           |
                                 plugin add / invoke
                                           |
                                           v
+-----------------------------------------------------------------------------------+
|                             CLAUDE PLUGIN RUNTIME ENGINE                          |
|  +-----------------------+   +------------------------+   +--------------------+  |
|  | Plugin Manifest Parser|   | Hook Event Dispatcher  |   | Security & Scope   |  |
|  |    (manifest.json)    |   |  (Pre/Post Execution)  |   |   Audit Sandbox    |  |
|  +-----------+-----------+   +-----------+------------+   +---------+----------+  |
+-------------|---------------------------|---------------------------|-------------+
              |                           |                           |
              v                           v                           v
+-----------------------------------------------------------------------------------+
|                            FAST MCP 3.1 PROTOCOL LAYER                            |
|  +--------------------+  +--------------------+  +-----------------------------+  |
|  | Local File Tools   |  | Web Browser Agents |  | Issue Tracker & Git Tools   |  |
|  +--------------------+  +--------------------+  +-----------------------------+  |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Developing custom agent tooling without standard packaging creates significant engineering overhead:
- **Environment Drift**: Developers on the same team end up with differing prompt versions, uncommitted script patches, and incompatible tool bindings.
- **Integration Friction**: Connecting an AI agent to developer tooling (such as Jira, GitHub, Slack, Docker, or Postgres) requires custom glue code in every repo.
- **Security & Scope Risk**: Ad-hoc scripts executed by AI agents can perform destructive file operations or leak tokens if execution scope is not enforced.
- **Lack of Reusability**: Useful agent capabilities built by one team remain trapped in specific repositories rather than shared enterprise-wide.

Claude Plugins solve these problems by providing a manifest-driven specification that packages CLI commands, Model Context Protocol (MCP) servers, and event-driven lifecycle hooks into single-command installable bundles.

## Where it fits in the stack
Claude Plugins operate in the **Development & Ops / Extension Ecosystem** layer. They wrap around [Claude Code](claude-code.md) and related agent runtime environments, bridging agent decision-making with local shell tools and remote infrastructure APIs.

```
+-----------------------------------------------------------------------------------+
|                                  USER / CLAUDE CODE                               |
+------------------------------------------+----------------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------+
|                               CLAUDE PLUGIN REGISTRY                              |
|               (Local Manifests, Enterprise Registries, Community Hubs)            |
+------------------------------------------+----------------------------------------+
                                           |
                                  FastMCP 3.1 / JSON-RPC
                                           |
                                           v
+-----------------------------------------------------------------------------------+
|                         LOCAL ENVIRONMENT / TARGET APIS                           |
|       (Git Repositories, Database Clusters, Browser Puppeteers, CI Pipelines)     |
+-----------------------------------------------------------------------------------+
```

## Typical use cases

### 1. Web Orchestration & Browser Automation
Installing plugins like `browser-use` allows Claude Code to open headless web browsers, navigate JS-heavy single-page apps, fill forms, and extract live DOM state directly during debugging sessions.

### 2. Automated PR Review & Repository Auditing
Using plugins such as `code-review` and `agentlint` to automatically analyze Git diffs against organizational style guidelines, check KnowledgeOps compliance, and detect security vulnerabilities before code is merged.

### 3. Environment & Skill Standardization
Distributing team-wide developer skills using packages like [Superpowers](../agents/superpowers.md) to guarantee every developer's Claude environment shares identical project rules, testing workflows, and deployment commands.

### 4. Interactive Debugging & Bug Remediation
Plugins like `test-writer-fixer` and `debugger` monitor failing unit test suites (e.g., Pytest, Jest) and auto-apply code patches until all test assertions pass.

### Notable Plugins & Starters
| Plugin Name | Primary Function | Ideal Deployment Scenario |
| :--- | :--- | :--- |
| `browser-use` | Multi-step headless web research & DOM manipulation | Scraping sites without native REST APIs |
| `chronos-mcp` | FastMCP 3.1 temporal task scheduling & calendar sync | Complex multi-step release management |
| `connect-apps` | OAuth-bound connection to GitHub, Jira, Notion, Slack | Cross-platform developer workflows |
| `test-writer-fixer` | Unit test generation, execution, and patch repair | Codebases with regression debt |
| `mcp-builder` | Scaffolding new FastMCP 3.1 server plugins | Building internal corporate tool plugins |

## Strengths
- **Modular Packaging**: Bundles commands, dependencies, and MCP tool definitions into a single, easily distributed manifest.
- **FastMCP 3.1 Integration**: Plugins can dynamically expose high-performance FastMCP 3.1 tools with Pydantic v2 runtime validation.
- **Event-Driven Hooks**: Supports pre-command and post-command execution hooks to enforce guardrails and verify outputs automatically.
- **Enterprise Friendly**: Supports private plugin registries hosted on internal Git instances or S3 buckets.

## Limitations
- **Ecosystem Quality Variance**: Community-contributed plugins vary in security auditing, code quality, and active maintenance.
- **Permission Overhead**: Over-granting permissions to untrusted plugins can expose local environment variables or private file trees.
- **Tool Namespace Collision**: Installing multiple plugins that declare identically named tools (e.g., `search_code`) requires careful namespace configuration.

## When to use it
- When you want to package and distribute repeatable agent workflows across software development teams.
- When connecting Claude Code or terminal agents to specialized internal tools, staging environments, or proprietary databases.
- When enforcing standard code review, linting, or documentation practices across an enterprise organization.

## When not to use it
- In highly locked-down environments where third-party extension installation is explicitly blocked by corporate policy.
- For simple, one-off bash scripts where creating a structured plugin manifest adds unnecessary abstraction overhead.

## Getting started

### Installation
Plugins are managed directly via the `claude` CLI:

```bash
# Add an official or community plugin
claude plugin add browser-use

# Add a plugin from a specific GitHub repository or private Git endpoint
claude plugin add https://github.com/org/custom-mcp-plugin.git
```

### Listing & Managing Installed Plugins
Inspect installed plugins and their execution statuses:

```bash
# List all active plugins in current environment
claude plugin list

# Verify plugin health, permissions, and MCP server connections
claude plugin doctor
```

### Developing a Local Plugin Manifest
To create a plugin, add a `plugin.json` file in your repository root or plugin package directory:

```json
{
  "name": "knowledge-ops-auditor",
  "version": "2.1.0",
  "description": "Enforces KnowledgeOps doc standards and runs audit scripts",
  "author": "Engineering Ops",
  "commands": [
    {
      "name": "audit-docs",
      "description": "Audits markdown files for required headers and metadata",
      "exec": "python3 scripts/audit_docs_quality.py"
    }
  ],
  "mcp_servers": [
    {
      "name": "doc-server",
      "command": "python3",
      "args": ["-m", "mcp_server_docs"]
    }
  ]
}
```

## CLI examples

### 1. Invoking Plugin Commands
Execute a plugin command directly within your agentic shell:

```bash
# Run web research using the browser-use plugin
claude plugin exec browser-use -- "Extract API release notes from target docs"
```

### 2. Updating Installed Plugins
Update all active plugins to their latest compatible versions:

```bash
claude plugin update --all
```

### 3. Uninstalling a Plugin
Remove a plugin and cleanly unbind its associated MCP tools:

```bash
claude plugin remove knowledge-ops-auditor
```

## API examples

### Full FastMCP 3.1 Plugin Server Implementation
Below is a complete Python implementation of a FastMCP 3.1 server designed to be packaged inside a Claude Plugin:

```python
import sys
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP 3.1 plugin server instance
mcp = FastMCP(
    "Code Quality Plugin Server",
    version="3.1.0",
    description="FastMCP server providing repository auditing tools for Claude Code"
)

class DocAuditRequest(BaseModel):
    filepath: str = Field(..., description="Path to markdown file to audit")
    check_strict_headers: bool = Field(default=True, description="Enforce exact section heading matches")

    @field_validator("filepath")
    @classmethod
    def validate_md_extension(cls, v: str) -> str:
        if not v.endswith(".md"):
            raise ValueError("Filepath must target a Markdown file (.md)")
        return v

class DocAuditResponse(BaseModel):
    filepath: str
    is_compliant: bool
    missing_headers: List[str]
    character_count: int

@mcp.tool()
async def audit_markdown_file(req: DocAuditRequest) -> DocAuditResponse:
    """Audits a local markdown document for KnowledgeOps section compliance."""
    required = [
        "What it is", "What problem it solves", "Where it fits in the stack",
        "Typical use cases", "Strengths", "Limitations", "When to use it",
        "When not to use it", "Getting started", "CLI examples", "API examples",
        "Related tools / concepts", "Sources / references"
    ]

    try:
        with open(req.filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return DocAuditResponse(
            filepath=req.filepath,
            is_compliant=False,
            missing_headers=["FILE_NOT_FOUND"],
            character_count=0
        )

    missing = [h for h in required if f"## {h}" not in content]

    return DocAuditResponse(
        filepath=req.filepath,
        is_compliant=len(missing) == 0,
        missing_headers=missing,
        character_count=len(content)
    )

if __name__ == "__main__":
    mcp.run()
```

### Pydantic v2 Plugin Manifest Validator
Use Pydantic v2 to programmatically validate third-party plugin manifest configurations before execution:

```python
from pydantic import BaseModel, Field, HttpUrl, field_validator
from typing import List, Optional, Dict

class PluginCommandSpec(BaseModel):
    name: str = Field(..., description="CLI invocation sub-command")
    description: str = Field(..., description="Human readable command description")
    exec: str = Field(..., description="System binary or script path")

class MCPServerSpec(BaseModel):
    name: str = Field(..., description="Identifier for MCP service")
    command: str = Field(..., description="Executable e.g., python3 or node")
    args: List[str] = Field(default_factory=list, description="Command line arguments")
    env: Optional[Dict[str, str]] = Field(default=None, description="Environment variables")

class ClaudePluginManifest(BaseModel):
    name: str = Field(..., description="Unique slug for the plugin")
    version: str = Field(..., description="SemVer string e.g., 1.0.0")
    description: str = Field(..., description="Overview of plugin capabilities")
    author: Optional[str] = Field(None, description="Maintainer name or organization")
    repository: Optional[HttpUrl] = Field(None, description="Source code URL")
    commands: List[PluginCommandSpec] = Field(default_factory=list)
    mcp_servers: List[MCPServerSpec] = Field(default_factory=list)

    @field_validator("name")
    @classmethod
    def validate_plugin_name(cls, v: str) -> str:
        if not v.replace("-", "").replace("_", "").isalnum():
            raise ValueError("Plugin name must contain only alphanumeric characters, hyphens, or underscores.")
        return v.lower()

# Verification Example
manifest_data = {
    "name": "devops-helper",
    "version": "1.0.0",
    "description": "DevOps helper plugin for deployment checks",
    "commands": [
        {"name": "check-deploy", "description": "Verify cluster status", "exec": "kubectl get pods"}
    ],
    "mcp_servers": [
        {"name": "k8s-mcp", "command": "python3", "args": ["server.py"]}
    ]
}

manifest = ClaudePluginManifest.model_validate(manifest_data)
print(f"Manifest successfully validated: {manifest.name} (v{manifest.version})")
```

## Comparative Metrics & Ecosystem Benchmarks

| Feature Dimension | Native Claude Code Tools | Claude Plugin Ecosystem | Custom Shell Scripts |
| :--- | :--- | :--- | :--- |
| **Distribution Method** | Built-in | Manifest-driven (`plugin add`) | Manual file copy |
| **MCP 3.1 Support** | Static | Dynamic discovery & loading | None |
| **Sandboxing & Auditing** | High | Configurable / Audited | Low (raw shell access) |
| **Maintenance Overhead** | Minimal | Low (managed via registry) | High |
| **Multi-repo Portability** | Low | High | Medium |

## Lifecycle Hook & Configuration Reference

| Event Hook Name | Execution Timing | Typical Guardrail Purpose |
| :--- | :--- | :--- |
| `pre-tool-call` | Before an agent invokes a plugin tool | Sanitize arguments, enforce path constraints |
| `post-tool-call` | Immediately following tool response | Format output markdown, check for secrets |
| `on-plugin-load` | Upon plugin initialization in shell | Authenticate tokens, spin up background FastMCP server |
| `on-plugin-unload` | Upon exiting Claude shell | Gracefully shut down background MCP processes |

## Troubleshooting & Common Pitfalls

### 1. Unresponsive FastMCP Server Process
If a plugin's background FastMCP server fails to start, verify environment variables and dependencies:

```bash
# Debug plugin MCP server connection
claude plugin doctor --verbose --plugin knowledge-ops-auditor
```

### 2. Handling Tool Namespace Collisions
When two plugins export tools with identical names, alias them within your project-level `.clauderc` or `CLAUDE.md`:

```json
{
  "plugin_aliases": {
    "browser-use:search": "browser_search",
    "exa-plugin:search": "exa_search"
  }
}
```

## Related tools / concepts
- [Claude Code](claude-code.md) - Primary CLI pair programmer hosting plugins.
- [Claude Hooks](claude-hooks.md) - Event-driven hooks and lifecycle triggers.
- [Claude Skills Ecosystem](../agents/claude-skills-ecosystem.md) - Skill definitions and agent capability patterns.
- [Superpowers](../agents/superpowers.md) - Framework for agent persona and workflow modularity.
- [Browser Use](../automation_orchestration/browser-use.md) - Web browser automation library for agents.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) - Open standard for model-tool communication.
- [Aider](aider.md) - Git-integrated terminal pair programmer.

## Sources / references
- [Awesome Claude Plugins Repository](https://github.com/ComposioHQ/awesome-claude-plugins)
- [Awesome Claude AI Ecosystem](https://awesomeclaude.ai/)
- [Superpowers Framework Repository](https://github.com/obra/superpowers)
- [AI Templates Portal](https://www.aitmpl.com/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
