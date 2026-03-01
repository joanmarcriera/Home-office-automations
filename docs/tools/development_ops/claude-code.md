# Claude Code

## What it is
Claude Code is a command-line interface (CLI) tool and AI agent from Anthropic that can directly interact with your local development environment. It can read and write files, run terminal commands, and perform complex coding tasks.

## What problem it solves
It reduces the friction of context-switching between an AI chat interface and a code editor. By operating directly in the terminal, it can autonomously navigate large codebases and execute the commands necessary to implement and verify changes.

## Where it fits in the stack
**Category**: Agent / Tool

## Typical use cases
- **Codebase Refactoring**: Identifying and applying patterns across multiple files.
- **Automated Debugging**: Running tests, analyzing error logs, and applying fixes in a loop.
- **Remote Environment Control**: Managing and interacting with remote servers or containers via its Remote Control feature.

## Strengths
- **Agentic Capabilities**: Can proactively run commands (e.g., `git`, `npm test`) to verify its work.
- **Remote Control**: Built-in support for managing remote dev environments.
- **Optimized Reasoning**: Leverages Claude 3.5 Sonnet for high-quality code generation and logic.

## Limitations
- **Proprietary**: Requires an Anthropic API key and is not open source.
- **CLI Only**: Lacks the visual multi-file diffing and GUI features found in IDEs like Cursor.

## When to use it
- Use when you need an autonomous agent to handle complex, multi-step development workflows.
- Use for tasks that require heavy terminal interaction alongside code editing.

## When not to use it
- Not necessary for simple coding questions or single-file edits.
- Not for users who prefer a fully visual GUI-based coding experience.

## Getting started

Install Claude Code globally via npm and authenticate with your Anthropic account:

```bash
# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Authenticate
claude auth login

# Start a session in your current directory
claude
```

## CLI examples

### claude-code init
Create a `CLAUDE.md` file to give Claude persistent context about your repository:
```bash
claude /init
```

### slash commands
Inside an active `claude` session, use these commands for quick actions:
- `/help`: Show available commands and skills.
- `/compact`: Summarize conversation history to save tokens.
- `/config`: Interactively configure settings (model, theme, etc.).
- `/review`: (If skill exists) Trigger a code review of staged changes.

### MCP setup
Configure Model Context Protocol servers to extend Claude's capabilities:
```bash
# List configured MCP servers
claude mcp list

# Add a new MCP server
claude mcp add my-server npx -y @modelcontextprotocol/server-everything
```

## Related tools / concepts
- [Aider](./aider.md)
- [Droid](./droid.md)
- [OpenHands](./openhands.md)
- [Claude Code Setup](./claude-code-setup.md)
- [Agent Client Protocol (ACP)](../../knowledge_base/agent_protocols.md)

## Sources / references
- [Claude Code Remote Control](https://code.claude.com/docs/en/remote-control)

## Contribution Metadata
- Last reviewed: 2026-03-01
- Confidence: medium
