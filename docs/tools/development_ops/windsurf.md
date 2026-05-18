# Windsurf

## What it is
Windsurf is an agentic IDE from Codeium that features a deeply integrated AI assistant capable of understanding and acting upon the entire codebase.

## What problem it solves
It moves beyond simple "chat-in-sidebar" interfaces by allowing the AI to navigate files, run commands, and perform complex refactors with full awareness of the project's context.

## Where it fits in the stack
**Category**: Tool / Development & Ops / AI Assistant

## Typical use cases
- Large-scale refactoring of legacy code.
- Implementing new features across multiple files.
- Debugging complex issues by allowing the AI to trace execution paths.

## Strengths
- "Flow" state integration: AI actions are fast and low-friction.
- Deep context: Uses Codeium's proprietary indexing for high-precision retrieval.
- Multi-file editing and command execution capabilities.

## Limitations
- Proprietary IDE (based on VS Code but managed by Codeium).
- Requires an internet connection for advanced agentic features.

## When to use it
- When you need an AI that can "do" rather than just "suggest."
- If you are already in the Codeium ecosystem or looking for a more "agentic" alternative to Cursor.

## When not to use it
- If you have strict requirements against using proprietary, cloud-connected IDEs.

## Licensing and cost
- **Open Source**: No
- **Cost**: Freemium / Paid Subscription
- **Self-hostable**: No

## Getting started
Windsurf can be installed on macOS, Windows, and Linux. It allows for a fresh setup or importing configurations from VS Code or Cursor.

**Installation:**
1. Download the installer from the [official website](https://codeium.com/windsurf).
2. Run the installer and follow the onboarding flow.
3. (Optional) Install the `windsurf` command in your PATH during onboarding to enable CLI access.

**Hello-world example:**
After installation, open a folder and activate **Cascade** (Cmd+L) to start a new project. Try asking:
`Generate a simple React counter application.`

```bash
# Launch Windsurf from the terminal (if added to PATH)
windsurf .
```

## CLI examples
The `windsurf` CLI is primarily used for launching the IDE and opening specific files or folders.

```bash
# Open the current directory in Windsurf
windsurf .

# Open a specific file
windsurf path/to/file.py

# Open a specific file at a specific line
windsurf -g path/to/file.py:42

# Compare two files
windsurf --diff file1.py file2.py
```

## API examples
Windsurf extends the VS Code ecosystem, meaning it is compatible with most VS Code extensions and APIs. Additionally, it supports the **Model Context Protocol (MCP)** for extending its agentic capabilities.

**Example MCP Configuration (`windsurf_mcp_config.json`):**
Windsurf can connect to external MCP servers to provide the AI agent (Cascade) with additional tools.

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_token_here"
      }
    }
  }
}
```

## Related tools / concepts
- [Cursor](cursor.md)
- [Aider](aider.md)
- [Claude Code](claude-code.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)

## Sources / References
- [Windsurf Official Documentation](https://docs.windsurf.com/windsurf/getting-started)
- [Windsurf MCP Guide](https://docs.windsurf.com/windsurf/cascade/mcp)
- [Codeium Blog](https://codeium.com/blog)

## Contribution Metadata
- Last reviewed: 2026-04-27
- Confidence: high
