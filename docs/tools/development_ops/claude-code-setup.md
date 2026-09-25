# Claude Code — Project Setup Guide

## What it is
A reproducible setup, environment blueprint, and workspace execution specification for the Anthropic Claude Code CLI environment in production engineering repos. It defines the workspace orchestration layer where **Claude 5.1** (`claude-5-1-20261101`) and hybrid multi-model agent systems operate. This includes global skill definitions, official and custom plugins, **FastMCP 3.1** Model Context Protocol server configurations, and repository lifecycle hooks (`.claude/settings.json`).

Rather than relying on uncommitted, workstation-specific setups, this guide specifies how to configure reproducible, containerized, or local developer workspaces where agentic execution is strictly governed by automated verification hooks, permission policies, and FastMCP tool boundaries.

## System Architecture

```mermaid
graph TD
    SubGraph_User[Developer Environment / Container Sandbox]
        CLI[Claude Code CLI Tool - `@anthropic/claude-code`]
        Config[Project Settings - `.claude/settings.json`]
        Auth[OAuth Token & API Key Store]
    end

    SubGraph_Hooks[Lifecycle Verification Hooks]
        PreHook[preToolUse Guardrail - Security & Syntax Audit]
        PostHook[postToolUse Guardrail - Contract & Quality Audit]
        Subshell[Subshell Bash Execution Sandbox]
    end

    SubGraph_Tools[Tool & Protocol Layer]
        FastMCP[FastMCP 3.1 Client Engine]
        Plugins[Claude Plugins - GitHub, Playwright, Security]
        FileSystem[Workspace Filesystem & Git Buffer]
    end

    SubGraph_Models[Cloud Reasoning Services]
        Claude5[Claude 5.1 Extended Reasoning Engine]
        Router[Claude Code Router - Hybird Multi-Model Dispatch]
    end

    CLI --> Config
    CLI --> Auth
    CLI --> FastMCP
    CLI --> PreHook
    PreHook --> Subshell
    CLI --> FileSystem
    FileSystem --> PostHook
    PostHook --> Subshell
    FastMCP --> Plugins
    CLI --> Router
    Router --> Claude5
```

## What problem it solves
Claude Code's autonomous file editing, shell command execution, and multi-step reasoning capabilities rely heavily on project-level configurations, custom tools, and strict execution guardrails:
1. **"Works on My Machine" Divergence**: Solves environment drift by storing project settings, hook scripts, and plugin lists directly inside Git version control (`.claude/settings.json`).
2. **Ungoverned Tool Execution**: Prevents accidental destructive commands or invalid code edits by intercepting tool calls using `preToolUse` and `postToolUse` lifecycle hooks.
3. **Context Isolation**: Bridges external documentation systems, local database schemas, and pull request management platforms into Claude Code sessions via **FastMCP 3.1** servers.
4. **Token & Permission Management**: Establishes transparent token budgeting (`/usage`) and explicit permission prompts for destructive system actions.

## Where it fits in the stack
**Development & Ops / Tooling Configuration & Execution Environment**. It acts as the local or containerized workbench for [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md), linking high-reasoning models (**Claude 5.1**) to shell commands, git operations, and local filesystems under strict security boundaries.

## Typical use cases
- **Developer Onboarding**: Bootstrapping new team workstations or ephemeral devcontainers with identical Claude Code skills, tools, and hooks in under 2 minutes.
- **Automated Quality Enforcement**: Executing real-time syntax checking (`check_docs_contract.py` or `pytest`) automatically whenever Claude Code writes or edits a file.
- **FastMCP 3.1 Context Extension**: Connecting local database replicas or documentation engines (Context7) to Claude Code's memory loop.
- **Agentic CI/CD Simulation**: Running headless non-interactive Claude Code tasks inside GitHub Actions or local bash scripts (`claude --prompt "..."`).

## Strengths
- **Fully Version-Controlled Workspaces**: Keeps workspace settings (`.claude/settings.json`) committed alongside application source code.
- **Real-Time Hook Execution**: Executes `preToolUse` and `postToolUse` hooks before and after tool calls, enforcing instant verification.
- **FastMCP 3.1 First-Class Integration**: Seamlessly discovers, mounts, and executes Model Context Protocol context servers.
- **Frontier extended thinking**: Leverages Claude 5.1's extended thinking and multi-step plan generation natively in the CLI shell.
- **Zero-Trust Permission Model**: Requires explicit user consent before executing destructive system calls or modifying sensitive files.

## Limitations
- **Interactive Initial Auth**: Initial authentication (`claude auth login`) requires interactive OAuth authentication via browser or web callback.
- **Host Binary Dependencies**: Relies on host system binaries (e.g., Node.js v20+, Python uv/pip, Git) being present in the user's `$PATH`.
- **Shell Cross-Compatibility**: Complex bash hook scripts must be carefully formatted to support both Linux (Bash) and macOS (Zsh/Bash) environments.

## When to use it
- When setting up new developer workstations, sandboxes, or containerized dev-environments for agentic coding.
- When committing project-level settings (`.claude/settings.json`) to standardize AI capabilities across engineering teams.
- When configuring **FastMCP 3.1** servers and safety guardrails for local development.

## When not to use it
- For general programmatic API calls inside backend services (use direct Anthropic SDKs or Pydantic AI instead).
- In strictly air-gapped embedded environments without local CLI or shell execution capabilities.

## Getting started

### Installation & Dependency Setup
Install the global `@anthropic/claude-code` CLI and verify system dependencies:

```bash
# Global npm installation
npm install -g @anthropic/claude-code

# Install Python environment manager (uv)
pip install uv

# Authenticate Claude Code CLI session
claude auth login
```

### Initial Workspace Verification
Verify the active installation, configuration, and model connectivity:

```bash
# Verify version
claude --version

# Run diagnostic check
claude /doctor

# Non-interactive sanity test prompt
claude --prompt "Verify local environment: list active project files and confirm Git repository state."
```

## CLI examples

### 1. Managing Official & Custom Plugins
Install plugins to grant Claude Code domain-specific tools:

```bash
# Install official plugins
claude plugin install github@claude-plugins-official
claude plugin install playwright@claude-plugins-official
claude plugin install security-guidance@claude-plugins-official

# List installed plugins and active versions
claude plugin list
```

### 2. Registering FastMCP 3.1 Context Servers
Mount Model Context Protocol tools into your workspace session:

```bash
# Add GitHub MCP server
claude mcp add github -- npx -y @anthropic-ai/mcp-server-github

# Add Context7 documentation search engine
claude mcp add context7 -- npx -y @upstash/context7-mcp

# Inspect active MCP server connections
claude mcp list
```

### 3. Usage & Token Budget Inspection
Inspect token usage, context limits, and cost estimates:

```bash
# View active session token cost and usage breakdown
claude /usage

# Export workspace status to JSON
claude status --json
```

## API examples

### FastMCP 3.1 Python Integration for Claude Code
Claude Code can interact directly with custom local FastMCP 3.1 servers. Below is a complete Python FastMCP server script (`scripts/claude_mcp_bridge.py`) that exposes project health checks and syntax auditing tools to Claude Code sessions:

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
import os
import subprocess

# Initialize FastMCP 3.1 Server for Claude Code Workspaces
mcp = FastMCP("ClaudeCodeWorkspaceBridge")

class AuditResponse(BaseModel):
    filepath: str = Field(description="Target file audited")
    passed: bool = Field(description="Whether the verification check passed")
    message: str = Field(description="Audit summary output")

@mcp.tool()
def run_project_docs_audit(filepath: str) -> str:
    """Executes the internal documentation contract auditor on a specific file."""
    if not os.path.exists(filepath):
        return f"Error: Target file '{filepath}' does not exist."

    try:
        result = subprocess.run(
            ["python3", "scripts/check_docs_contract.py", filepath],
            capture_output=True,
            text=True,
            timeout=15
        )
        passed = (result.returncode == 0)
        output = result.stdout or result.stderr
        res = AuditResponse(filepath=filepath, passed=passed, message=output.strip())
        return f"Audit {'PASSED' if res.passed else 'FAILED'} for {res.filepath}:\n{res.message}"
    except Exception as e:
        return f"Execution error during audit: {str(e)}"

@mcp.tool()
def get_git_status_summary(repo_path: str) -> str:
    """Returns a concise summary of modified and untracked files in the active Git repository."""
    if not os.path.exists(os.path.join(repo_path, ".git")):
        return f"Error: '{repo_path}' is not a valid Git repository root."

    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=10
        )
        changes = result.stdout.strip()
        if not changes:
            return "Git Status: Clean workspace (no uncommitted changes)."
        return f"Git Modified Files Summary:\n{changes}"
    except Exception as e:
        return f"Git query failed: {str(e)}"

if __name__ == "__main__":
    mcp.run()
```

### Validating Project Settings Schema with Pydantic v2
Ensure `.claude/settings.json` project configurations comply with strict Pydantic v2 validation models before committing changes:

```python
from pydantic import BaseModel, Field, field_validator
from typing import Dict, List, Optional
import json
import os

class HookConfig(BaseModel):
    edit: Optional[str] = Field(None, description="Shell command run before or after file edits")
    create: Optional[str] = Field(None, description="Shell command run before or after file creation")

class ClaudeProjectSettings(BaseModel):
    preferred_model: str = Field(default="claude-5-1-20261101", alias="preferredModel")
    hooks: Dict[str, HookConfig] = Field(default_factory=dict, description="Pre/Post tool hooks")
    mcp_servers: List[str] = Field(default_factory=list, alias="mcpServers")
    allowed_tools: List[str] = Field(default_factory=list, alias="allowedTools")

    @field_validator("preferred_model")
    @classmethod
    def validate_model_version(cls, v: str) -> str:
        if not v.startswith("claude-5"):
            raise ValueError(f"Project settings require Claude 5 series reasoning model, got '{v}'")
        return v

    class Config:
        populate_by_name = True

# Validate sample project configuration payload
raw_settings = {
    "preferredModel": "claude-5-1-20261101",
    "hooks": {
        "preToolUse": {
            "edit": "python3 scripts/security_audit.py {{file}}"
        },
        "postToolUse": {
            "edit": "python3 scripts/check_docs_contract.py {{file}}"
        }
    },
    "mcpServers": ["github", "context7"],
    "allowedTools": ["Bash", "Edit", "Write", "GlobTool"]
}

config = ClaudeProjectSettings.model_validate(raw_settings)
print(f"Validated Model: {config.preferred_model}")
print(f"Active Pre-Edit Hook: {config.hooks['preToolUse'].edit}")
```

### Complete Project Hook Configuration (`.claude/settings.json`)
Below is a production `.claude/settings.json` file configuring model selection, FastMCP server list, and automated verification hooks:

```json
{
  "preferredModel": "claude-5-1-20261101",
  "allowedTools": [
    "Bash",
    "Edit",
    "Write",
    "GlobTool",
    "LSTool"
  ],
  "hooks": {
    "preToolUse": {
      "edit": "python3 scripts/check_docs_contract.py {{file}}"
    },
    "postToolUse": {
      "edit": "python3 scripts/audit_docs_quality.py {{file}}"
    }
  },
  "mcpServers": [
    "github",
    "context7",
    "claude-mcp-bridge"
  ]
}
```

## Related tools / concepts
- [Claude Code Router](./claude-code-router.md) — Multi-model routing engine for Claude Code.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Standardized tool protocol framework.
- [Agent Protocols](../../knowledge_base/agent_protocols.md) — Specifications for agentic tool execution.
- [Standards & Conventions](../../standards.md) — Workspace coding guidelines.
- [Cursor](./cursor.md) — Alternative AI-native graphical IDE environment.

## Sources / references
- [Claude Code Official Documentation](https://docs.anthropic.com/claude-code)
- [Model Context Protocol Specification](https://modelcontextprotocol.io)
- [FastMCP 3.1 Python Framework](https://github.com/jlowin/fastmcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
