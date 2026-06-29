# Claude Code — Project Setup Guide

## What it is
A reproducible configuration guide for the Claude Code CLI setup used in this repository. It defines the specific environment where Claude 4.8 Opus (`claude-4-8-opus-20260528`) and GPT-5.5 operate, including plugins, global skills, MCP servers, and project-level automation hooks. As of June 2026, it supports the **MCP 3.0** standard for agentic tool discovery and resource connection.

## What problem it solves
Claude Code's power in this repo comes from project-specific hooks, agents, and skills. This guide solves the "it works on my machine" problem for AI agents by providing a standardized blueprint for reproducing the full engineering environment from scratch. It ensures that the specialized **Claude Hooks** (Pre/PostToolUse) are correctly configured for real-time validation.

## Where it fits in the stack
**Category**: Development & Ops / Tooling Configuration. It acts as the "bootstrap" layer for the [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) used to maintain this repository, integrating the Reasoning Layer with local execution capabilities.

## Typical use cases
- Setting up a local environment for contributing to this repository.
- Reproducing project-specific agent behaviors and automated verification loops.
- Standardizing the developer experience for both human and AI contributors.
- Debugging MCP 3.0 connectivity or plugin conflicts in the local workspace.

## Strengths
- **Reproducible Engineering**: Guaranteed consistency across different workstations.
- **Deep Automation**: Leverages project-level hooks for real-time validation (e.g., `mkdocs.yml` syntax).
- **Extensible Architecture**: Easily integrates new MCP 3.0 servers and global skills.
- **Optimized for Claude 4.8**: Specifically tuned for the high-reasoning capabilities and hook lifecycles of the June 2026 model generation.

## Limitations
- **Manual Bootstrapping**: Requires initial manual steps for global skill installation.
- **Environment Dependencies**: High reliance on Node.js, Python (uv), and specific API configurations.
- **Platform Specificity**: Some hook behaviors may vary between macOS (M4/M5) and Linux (TrueNAS/Ubuntu) environments.

## When to use it
- When initializing a new development environment for this repository.
- When the repository's `.claude/` configuration changes and needs to be re-synchronized.
- When onboarding new team members (human or AI).

## When not to use it
- For general Claude Code usage outside of this specific repository context.
- In environments where persistent local storage or internet access is prohibited.

## Getting started

### 1. Installation
Install the core CLI and prerequisites:
```bash
npm install -g @anthropic/claude-code
pip install uv
claude auth login
```

### 2. Hello World (Verify Setup)
Verify the installation by checking the version and active project context:
```bash
claude --version
claude --prompt "Status check: are project-level hooks and MCP 3.0 active?"
```

## CLI examples

### 1. Plugin Management
Install the mandatory plugin suite for this repository:
```bash
claude plugin install github@claude-plugins-official playwright@claude-plugins-official security-guidance@claude-plugins-official
```

### 2. MCP Server Configuration
Add the required context layers for documentation and automation (MCP 3.0):
```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp
claude mcp add github -- npx @anthropic-ai/mcp-server-github
```

### 3. Usage & Diagnostics
Monitor token consumption and troubleshoot environment issues:
```bash
claude /usage
claude /doctor
```

## API examples

### 1. Project-Level Hook (`.claude/settings.json`)
A snippet demonstrating how **Claude Hooks** (`PreToolUse` and `PostToolUse`) are enforced for real-time validation:
```json
{
  "hooks": {
    "preToolUse": {
      "edit": "python3 scripts/security_audit.py {{file}}"
    },
    "postToolUse": {
      "edit": "python3 scripts/sql_validator.py {{file}}"
    }
  }
}
```

### 2. Subagent Definition (`.claude/agents/reviewer.md`)
Standardized system prompt for the playbook reviewer:
```markdown
# Playbook Reviewer
You are a specialist agent. Verify:
1. All 13 mandatory sections are present.
2. Internal links resolve to real files in /docs.
3. Reference models include Claude 4.8 and GPT-5.5.
```

## Related tools / concepts
- [Claude Code](./claude-code.md)
- [Claude Code Router](./claude-code-router.md)
- [Agent Protocols (MCP & ACP)](../../knowledge_base/agent_protocols.md)
- [Standards & Conventions](../../standards.md)
- [Aider](./aider.md)
- [Mentat](./mentat.md)
- [Cursor](./cursor.md)
- [Zed](./zed.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)

## Sources / references
- [Claude Code Official Documentation](https://docs.anthropic.com/claude-code)
- [MCP Specification and Servers](https://modelcontextprotocol.io)
- [FastMCP 3.0 Release Notes](https://github.com/jlowin/fastmcp)
- [Project-Specific Claude Config (GitHub Repo)](https://github.com/shanraisshan/claude-code-best-practice)

## Contribution Metadata
- Last reviewed: 2026-06-29
- Confidence: high
