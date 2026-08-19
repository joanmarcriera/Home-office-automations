# Claude Code — Project Setup Guide

## What it is
A reproducible configuration and setup guide for the Claude Code CLI environment in software engineering workspaces. It defines the specific configuration layer where **Claude 5.1** (`claude-5-1-20261101`) and **GPT-5.5** operate, including plugins, global skills, **FastMCP 3.1** Model Context Protocol servers, and project-level lifecycle automation hooks (`.claude/settings.json`).

## What problem it solves
Claude Code's agentic capabilities within a repository rely heavily on repository-specific settings, custom hooks, and external context tools. This guide eliminates "works on my machine" inconsistencies by providing a standardized blueprint for bootstrapping identical engineering environments across workstations. It ensures that automated **Claude Hooks** (`preToolUse` / `postToolUse`) validate edits and commands in real time.

## Where it fits in the stack
**Development & Ops / Tooling Configuration Layer**. It acts as the local workspace execution environment for [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md), connecting high-reasoning models (**Claude 5.1**) to shell commands, git operations, and local filesystems under strict permission boundaries.

## Typical use cases
- Bootstrapping a fresh development machine or containerized sandbox for contributing to this codebase.
- Reproducing agentic tool behavior, permissions, and automated pre-commit hooks.
- Configuring **FastMCP 3.1** servers to provide filesystem, GitHub, or database context to the agent.
- Standardizing verification rules and pre-tool security inspection across team members.

## Strengths
- **Reproducible Agentic Environment**: Guarantees identical agent tool access and permission boundaries across developer environments.
- **Real-Time Hook Execution**: Supports `preToolUse` and `postToolUse` hooks to run security audits or linting scripts automatically before and after file edits.
- **FastMCP 3.1 Integration**: First-class support for expanding tool definitions via Model Context Protocol servers.
- **Tuned for Frontier Reasoning**: Optimized for the extended thinking and hook lifecycles of Claude 5.1 and GPT-5.5.

## Limitations
- **Manual Initial Auth**: Requires interactive browser-based authentication (`claude auth login`) upon initial setup.
- **Dependency Requirements**: Requires Node.js (v20+), Python (uv/pip), and git binaries to be pre-installed on the host system.
- **Platform Specificity**: Some hook shell scripts may require minor syntax adjustments between Linux (Ubuntu/Debian) and macOS environments.

## When to use it
- When setting up a new workstation or developer environment for agent-assisted coding.
- When updating or auditing the repository's `.claude/settings.json` configuration.
- When troubleshooting MCP server connections or permission denied errors in Claude Code.

## When not to use it
- For general LLM API calls inside Python application code (use direct Anthropic SDKs or Pydantic AI instead).
- In strictly isolated offline sandboxes without local CLI access.

## Getting started

### Installation
Install the core CLI, package manager, and authenticate:

```bash
npm install -g @anthropic/claude-code
pip install uv
claude auth login
```

### Hello-world (Verify Environment)
Verify CLI version and active context:

```bash
claude --version
claude --prompt "Run environment check: confirm active project context and MCP server connectivity."
```

## CLI examples

### 1. Plugin Management
Install official plugins for enhanced workspace operations:

```bash
claude plugin install github@claude-plugins-official playwright@claude-plugins-official security-guidance@claude-plugins-official
```

### 2. FastMCP 3.1 Server Management
Register MCP context providers for local development:

```bash
# Add GitHub context server via FastMCP
claude mcp add github -- npx @anthropic-ai/mcp-server-github

# Add Context7 documentation search server
claude mcp add context7 -- npx -y @upstash/context7-mcp
```

### 3. Usage & Diagnostic Commands
Inspect session token usage and troubleshoot settings:

```bash
claude /usage
claude /doctor
```

## API examples

### 1. Project Hook Configuration (`.claude/settings.json`)
Demonstrating real-time validation hooks that trigger Python verification scripts before and after file modifications:

```json
{
  "preferredModel": "claude-5-1-20261101",
  "hooks": {
    "preToolUse": {
      "edit": "python3 scripts/security_audit.py {{file}}"
    },
    "postToolUse": {
      "edit": "python3 scripts/audit_docs_quality.py {{file}}"
    }
  },
  "mcpServers": [
    "github",
    "context7"
  ]
}
```

### 2. Python Configuration Schema Validator (Pydantic v2)
Validate `.claude/settings.json` structure programmatically using strict Pydantic v2 schemas:

```python
import os
import json
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, ValidationError, ConfigDict

class HookDefinition(BaseModel):
    edit: Optional[str] = Field(None, description="Shell command executed during file editing")
    create: Optional[str] = Field(None, description="Shell command executed on file creation")

class ClaudeSettingsSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    preferred_model: str = Field(
        default="claude-5-1-20261101",
        alias="preferredModel",
        description="Target reasoning model"
    )
    hooks: Dict[str, HookDefinition] = Field(
        default_factory=dict,
        description="Lifecycle hook mappings"
    )
    mcp_servers: List[str] = Field(
        default_factory=list,
        alias="mcpServers",
        description="Active MCP server names"
    )

def validate_settings(filepath: str) -> Optional[ClaudeSettingsSchema]:
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        return ClaudeSettingsSchema.model_validate(data)
```

## Related tools / concepts
- [Claude Code Router](./claude-code-router.md) — Dynamic model routing layer.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Tool protocol standard.
- [Agent Protocols](../../knowledge_base/agent_protocols.md) — MCP and ACP architectural specifications.
- [Standards & Conventions](../../standards.md) — Repository development guidelines.
- [Cursor](./cursor.md) — Alternative agentic IDE interface.

## Sources / references
- [Claude Code Official Documentation](https://docs.anthropic.com/claude-code)
- [Model Context Protocol Specification](https://modelcontextprotocol.io)
- [FastMCP 3.1 Framework GitHub](https://github.com/jlowin/fastmcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
