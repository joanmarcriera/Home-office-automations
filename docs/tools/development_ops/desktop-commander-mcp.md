# Desktop Commander MCP

## What it is
A privacy-first Model Context Protocol (MCP 3.0) server that provides AI assistants with terminal control, filesystem access, and surgical text editing capabilities. It is built to be the "local hands" for frontier models like **Claude 4.8 Opus** and **GPT-5.5**.

## What problem it solves
It enables AI assistants to interact directly with the local machine's development environment while strictly removing all telemetry, analytics, and external tracking typically found in similar tools. It solves the "trust gap" in agentic workflows by ensuring no data leaves the local environment except through explicitly defined MCP tool calls.

## Where it fits in the stack
**Development & Ops / Tool Layer**. It serves as a secure bridge between an LLM-based agent (running in an MCP-compliant host like Claude Desktop or Cursor 3.0) and the local OS.

## Typical use cases
- Reading and writing files in a local development environment.
- Executing terminal commands and managing local processes for **Llama 4 Maverick** fine-tuning.
- Searching code using `ripgrep` integrations for complex refactoring.
- Applying targeted search/replace operations (edit blocks) across multiple files.

## Strengths
- **Privacy-First**: No telemetry, analytics, or external connections; operates entirely on-device.
- **MCP 3.0 Native**: Full support for the latest Task Protocol and resource discovery.
- **Surgical Editing**: Includes the `edit_block` tool for precise, idempotent text replacements.
- **Configurable Security**: Allows blocking specific commands and restricting access to white-listed directories.

## Limitations
- **Permission Bound**: Operates with the permissions of the user running the server; lacks its own sandboxing.
- **Manual Config**: Requires manual configuration of allowed directories for security.
- **Local Only**: Not designed for remote or cloud-based execution without additional tunneling.

## When to use it
- When you want to give an agent access to your local dev environment but are concerned about privacy or data leakage.
- When you need a lightweight, reliable bridge for filesystem and terminal operations for `claude-4-8-opus-20260528`.
- In highly regulated environments where telemetry is strictly prohibited.

## When not to use it
- In untrusted environments where the agent could perform destructive actions (unless strictly configured).
- If you require cloud-native orchestration (consider [Superconductor](superconductor.md) instead).
- If you need native browser automation (use [Playwright](playwright.md) for those tasks).

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
Start a background process and manage its lifecycle using MCP 3.0 protocols.

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
- [Claude Code Container MCP](claude-code-container-mcp.md)
- [Aider](aider.md)
- [VS Code](vscode.md)
- [Zed](zed.md)
- [MCP Registry](../automation_orchestration/mcp-registry.md)
- [Agent Protocols](../../knowledge_base/agent_protocols.md)
- [Local LLMs](../ai_knowledge/local_llms.md)

## Sources / References
- [Desktop Commander MCP GitHub](https://github.com/democratize-technology/DesktopCommanderMCP)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-06-30
- Confidence: high
