# Claude Desktop

## What it is
Claude Desktop is a native application for macOS and Windows that brings Anthropic's Claude AI models directly to the user's workspace. It serves as a powerful host for the Model Context Protocol (MCP), allowing Claude to interact with local files, data, and tools.

## What problem it solves
It overcomes the limitations of browser-based AI by providing a secure, local execution environment. Key problems solved include:
- **Local Context**: Direct access to local files and system resources through MCP.
- **Deep Integration**: Seamlessly integrates into desktop workflows without constant tab-switching.
- **Tool Use**: Serves as a standard host for MCP servers, enabling Claude to perform actions like searching local databases or interacting with desktop APIs.

## Where it fits in the stack
**AI Assistants & Knowledge**. It is a primary interface for interacting with [Anthropic (Claude)](../providers/anthropic.md) and acts as the "host" or "client" in the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) architecture.

## Typical use cases
- **Developer Workflows**: Indexing local codebases and running local tests through MCP servers like `filesystem` or `playwright`.
- **Data Analysis**: Querying local CSVs or SQLite databases.
- **Personal Productivity**: Connecting to local calendars or note-taking apps via desktop extensions.
- **Secure File Processing**: Processing sensitive documents without uploading them to a third-party web interface.

## Strengths
- **MCP Native**: The flagship implementation for MCP, supporting both local and remote MCP servers.
- **User Interface**: Provides a polished, native experience with keyboard shortcuts and desktop notifications.
- **Desktop Extensions**: Support for secure, installable packages that extend Claude's capabilities with local data.
- **Privacy**: Local MCP operations keep sensitive data on the machine rather than sending it all to the cloud.

## Limitations
- **OS Support**: Currently only available for macOS and Windows; no official Linux desktop app (CLI is recommended for Linux).
- **Subscription Required**: Many advanced desktop features, including some desktop extensions, require a Pro, Team, or Enterprise subscription.
- **Resource Usage**: Can be more resource-intensive than a browser tab due to its native nature and background MCP processes.

## When to use it
- When you need to give Claude access to your local filesystem or databases via MCP.
- For deep integration of AI into your daily macOS or Windows workflows.
- When you prefer a native desktop application experience over a web browser.
- For secure, local processing of sensitive documents using MCP tools.

## When not to use it
- If you are on a Linux-based operating system (use Claude CLI/Claude Code instead).
- If you have very limited system resources and prefer the lightweight nature of a browser tab.
- If your workflow is entirely cloud-based and does not require local system access.

## Getting started

1. **Download**: Visit [claude.ai/download](https://claude.ai/download) and select the version for your OS.
2. **Install**: Open the installer and follow the prompts.
3. **Sign In**: Log in with your Anthropic account.
4. **Configure MCP (Optional)**: To add local tools, edit your `claude_desktop_config.json` file.
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

## Technical Patterns

### MCP Configuration Example
Adding a local filesystem server to Claude Desktop:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/username/Documents"]
    }
  }
}
```

### Desktop Extensions
Claude Desktop supports "extensions" which are essentially pre-configured MCP servers or UI components. You can manage these in **Settings > Extensions**.

## Related tools / concepts
- [Anthropic (Claude)](../providers/anthropic.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Claude Code](../development_ops/claude-code.md)
- [Filesystem-as-Interface](../../knowledge_base/patterns/filesystem-context.md)
- [ServiceNow MCP Server](../automation_orchestration/servicenow-mcp.md)

## Sources / references
- [Official Download Page](https://claude.ai/download)
- [Claude Desktop Documentation](https://support.claude.com/en/articles/10065433-install-claude-desktop)
- [MCP Introduction](https://modelcontextprotocol.io/introduction)

## Contribution Metadata
- Last reviewed: 2026-06-06
- Confidence: high
