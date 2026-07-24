# Claude Desktop

## What it is
Claude Desktop is a native application for macOS and Windows that brings Anthropic's Claude AI models directly to the user's workspace. It serves as the primary host for the Model Context Protocol (MCP), allowing Claude to interact with local files, data, and tools securely. As of late August 2026, it is the reference implementation for "Agentic Desktop" workflows, natively supporting **MCP 3.1** and frontier models like **Claude 5.1**.

## What problem it solves
It overcomes the limitations of browser-based AI by providing a secure, local execution environment. Key problems solved include:
- **Local Context**: Direct access to local files and system resources through MCP without uploading sensitive data to public cloud environments.
- **Deep Integration**: Seamlessly integrates into desktop workflows via keyboard shortcuts, system-level hooks, and direct file drag-and-drop operations.
- **Tool Orchestration**: Serves as a standard host for MCP servers, enabling Claude to perform complex actions like searching local databases, interacting with desktop APIs, or managing terminal sessions.
- **Multi-Agent Coordination**: With MCP 3.1 Task Protocol integrations, the desktop app acts as a local coordinator for sub-agents executing background micro-missions.

## Where it fits in the stack
**AI Assistants & Knowledge**. It is a primary interface for interacting with [Anthropic (Claude)](../providers/anthropic.md) and acts as the "host" in the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) architecture.

## Typical use cases
- **Developer Workflows**: Indexing local codebases and running local tests through MCP servers like `filesystem` or `playwright`.
- **Data Analysis**: Querying local CSVs, Excel files, or SQLite databases directly from the chat interface.
- **Personal Productivity**: Connecting to local calendars, email clients, and note-taking apps via MCP extensions.
- **Secure File Processing**: Summarizing and extracting data from sensitive local documents under strict enterprise privacy bounds.

## Strengths
- **MCP 3.1 Native**: The flagship implementation for MCP, supporting both local and remote MCP servers with dedicated configuration parameters and schema validations.
- **Stateful Task Support**: Supports the MCP 3.1 Task Protocol, enabling stateful, long-running agentic loops to run securely in the background.
- **High Performance**: Native performance with optimized resource usage for long-running agentic tasks on local CPU/GPU setups.
- **Enhanced Privacy**: Local MCP operations keep sensitive data on the machine; only necessary context slices are sent to the model.

## Limitations
- **OS Support**: Currently only available for macOS and Windows; no official Linux desktop app (though Claude Code/CLI is available).
- **Subscription Gates**: Advanced features like specific enterprise desktop extensions and higher model limits require Pro or Team subscriptions.
- **Configuration Complexity**: Setting up complex MCP configurations still requires manual JSON editing (though the UI is improving).

## When to use it
- When you need to give Claude access to your local filesystem or databases via MCP.
- For deep integration of AI into your daily macOS or Windows professional workflows.
- When you prefer a stable, native desktop application experience over a browser tab.
- For secure processing of sensitive documents that should stay local.

## When not to use it
- If you are on a Linux-based operating system (use [Claude Code](../development_ops/claude-code.md) or the CLI).
- If you have very limited system resources and prefer the lightweight nature of a browser tab.
- If your workflow is entirely cloud-based and does not require local system access.

## Getting started

1. **Download**: Visit the [Official Download Page](https://claude.ai/download) and select the version for your OS.
2. **Install**: Open the installer and follow the prompts.
3. **Sign In**: Log in with your Anthropic account.
4. **Configure MCP**: To add local tools, edit your `claude_desktop_config.json` file.
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

## CLI examples

### Managing the App via Terminal
While Claude Desktop is a GUI app, it can be interacted with via terminal for configuration:
```bash
# Open the MCP configuration file (macOS)
open ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Check if MCP servers are running (using standard process tools)
ps aux | grep mcp

# Verify the local configuration JSON using native python schema validator
python3 -c "import json, os; json.load(open(os.path.expanduser('~/Library/Application Support/Claude/claude_desktop_config.json')))"
```

## API examples

### MCP 3.1 Configuration JSON
Example of a `claude_desktop_config.json` adding a local filesystem and SQLite server with advanced MCP 3.1 properties:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/jules/Documents/project"],
      "env": {
        "MCP_PROTOCOL_VERSION": "3.1"
      }
    },
    "sqlite": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sqlite", "--db-path", "/Users/jules/data/home.db"],
      "env": {
        "MCP_PROTOCOL_VERSION": "3.1",
        "SQLITE_TIMEOUT_MS": "5000"
      }
    }
  }
}
```

## Related tools / concepts
- [Anthropic (Claude)](../providers/anthropic.md) — the provider for models used in the app.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — the core protocol for extensions.
- [Claude Code](../development_ops/claude-code.md) — the CLI-based counterpart for developers.
- [Filesystem-as-Interface](../../knowledge_base/patterns/filesystem-context.md) — the design pattern used by MCP.
- [ServiceNow MCP Server](../automation_orchestration/servicenow-mcp.md) — example of a remote MCP server.
- [Goose](../agents/goose.md) — alternative agentic CLI tool.
- [Aider](../development_ops/aider.md) — another terminal-based AI coding assistant.
- [OpenHands](../development_ops/openhands.md) — agentic platform that can interact with desktop environments.

## Sources / references
- [Official Download Page](https://claude.ai/download)
- [Claude Desktop Documentation](https://support.claude.com/en/articles/10065433-install-claude-desktop)
- [Model Context Protocol Website](https://modelcontextprotocol.io/introduction)
- [Claude Desktop Release Notes](https://anthropic.com/news/claude-desktop-updates)

## Contribution Metadata
- Last reviewed: 2026-08-03
- Confidence: high
