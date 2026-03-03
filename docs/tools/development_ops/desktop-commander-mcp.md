# Desktop Commander MCP

## What it is
A privacy-first Model Context Protocol (MCP) server that provides AI assistants with terminal control, filesystem access, and surgical text editing capabilities.

## What problem it solves
It enables AI assistants (like Claude Desktop) to interact directly with the local machine's development environment while strictly removing all telemetry, analytics, and external tracking typically found in similar tools.

## Where it fits in the stack
**Tool / Agent**. It provides the "hands" for an agent to operate on a local machine.

## Typical use cases
- Reading and writing files in a local development environment.
- Executing terminal commands and managing local processes.
- Searching code using `ripgrep` integrations.
- Applying targeted search/replace operations (edit blocks).

## Strengths
- **Privacy-First**: No telemetry, analytics, or external connections.
- **Surgical Editing**: Includes a tool for precise text replacements.
- **Comprehensive Controls**: Covers filesystem, terminal, and system process management.
- **Configurable Security**: Allows blocking specific commands and restricting access to directories.

## Limitations
- Operates with the permissions of the user running the server.
- requires manual configuration of allowed directories for security.

## When to use it
- When you want to give an agent access to your local dev environment but are concerned about privacy or data leakage.
- When you need a lightweight, reliable bridge for filesystem and terminal operations.

## When not to use it
- In untrusted environments where the agent could perform destructive actions (unless strictly configured).
- If you require cloud-based orchestration or telemetry for team auditing.

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free
- **Self-hostable**: Yes (Local-only)

## Related tools / concepts
- [Claude Desktop](../development_ops/vscode.md)
- [Model Context Protocol](../../knowledge_base/agent_protocols.md)
- [ripgrep](https://github.com/BurntSushi/ripgrep)

## Sources / References
- [Desktop Commander MCP GitHub](https://github.com/democratize-technology/DesktopCommanderMCP)

## Contribution Metadata

- Last reviewed: 2026-03-02
- Confidence: high
