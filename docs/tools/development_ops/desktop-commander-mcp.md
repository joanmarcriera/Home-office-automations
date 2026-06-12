# Desktop Commander MCP

## What it is
A privacy-first Model Context Protocol (MCP) server that provides AI assistants with terminal control, filesystem access, and surgical text editing capabilities.

## What problem it solves
It enables AI assistants (like Claude 4.8 Opus or GPT-5.5) to interact directly with the local machine's development environment while strictly removing all telemetry, analytics, and external tracking typically found in similar tools.

## Where it fits in the stack
**Tool / Agent**. It provides the "hands" for an agent to operate on a local machine, serving as a secure alternative to cloud-based execution environments.

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
- Requires manual configuration of allowed directories for security.

## When to use it
- When you want to give an agent access to your local dev environment but are concerned about privacy or data leakage.
- When you need a lightweight, reliable bridge for filesystem and terminal operations for `claude-4-8-opus-20260528`.

## When not to use it
- In untrusted environments where the agent could perform destructive actions (unless strictly configured).
- If you require cloud-based orchestration or telemetry for team auditing.

## Getting started

Desktop Commander MCP is designed for local-first, privacy-conscious AI workflows.

### 1. Installation
```bash
npm install -g @democratize-technology/desktop-commander-mcp
```

### 2. Configuration
Add the server to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "desktop-commander": {
      "command": "desktop-commander-mcp",
      "args": [],
      "env": {
        "ALLOWED_DIRECTORIES": "/home/user/projects"
      }
    }
  }
}
```

### 3. Verify Connection
Check the Claude Desktop logs or status bar to ensure the server is connected and the `edit_block` and `run_command` tools are available.

## CLI examples

### 1. Starting the server manually
Useful for debugging or using with custom MCP clients:
```bash
desktop-commander-mcp --port 3000
```

### 2. Listing allowed directories
Verify which paths the commander has access to:
```bash
desktop-commander-mcp --list-allowed
```

### 3. Running a specific tool via CLI (using mcp-cli)
```bash
mcp-cli call desktop-commander list_files --path "."
```

## API examples

### 1. Searching Code (search_code)
Search for specific patterns across the codebase with high performance using `ripgrep`.

```json
{
  "tool": "search_code",
  "arguments": {
    "query": "async function authenticate",
    "include": ["src/**/*.ts"],
    "exclude": ["node_modules/**"]
  }
}
```

### 2. Surgical Editing (edit_block)
Apply precise text replacements using SEARCH/REPLACE blocks.

```json
{
  "tool": "edit_block",
  "arguments": {
    "path": "src/auth.ts",
    "edit": "<<<<<<< SEARCH\n  return user.id;\n=======\n  return { id: user.id, role: user.role };\n>>>>>>> REPLACE"
  }
}
```

### 3. Terminal Control (start_process)
Start a background process and manage its lifecycle.

```json
{
  "tool": "start_process",
  "arguments": {
    "command": "npm run build",
    "cwd": "./project"
  }
}
```

## Related tools / concepts
- [Claude Code](claude-code-setup.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [ripgrep](ripgrep.md)
- [Claude Code Container MCP](claude-code-container-mcp.md)
- [Aider](aider.md)
- [VS Code](vscode.md)
- [Zed](zed.md)
- [MCP Registry](../automation_orchestration/mcp-registry.md)
- [Agent Protocols](../../knowledge_base/agent_protocols.md)

## Sources / References
- [Desktop Commander MCP GitHub](https://github.com/democratize-technology/DesktopCommanderMCP)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)

## Contribution Metadata

- Last reviewed: 2026-06-12
- Confidence: high
