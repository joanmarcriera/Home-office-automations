# Claude Code

## What it is
Claude Code is a high-performance command-line interface (CLI) tool and autonomous AI agent from Anthropic. It operates directly within your local development environment, capable of reading/writing files, running terminal commands, and orchestrating complex engineering workflows.

## What problem it solves
It eliminates the friction of manual context-switching. Instead of copy-pasting code into a chat, Claude Code lives where your code lives, allowing it to autonomously navigate repositories, execute tests, debug runtime errors, and verify its own implementations.

## Where it fits in the stack
**Category**: Agent / [Development & Ops](index.md). It serves as the primary agentic interface for "AI-Native Software Engineering."

## Typical use cases
- **Autonomous Feature Implementation**: Describing a feature and letting the agent handle the file creation, logic, and testing.
- **Deep Debugging**: Analyzing stack traces, searching for root causes across modules, and applying surgical fixes.
- **Continuous Documentation**: Maintaining `CLAUDE.md` and `AGENTS.md` to ensure the repository remains "Agent-Friendly."
- **Overnight Routines**: Delegating long-running refactors or audits to run autonomously, providing a verified summary in the morning.

## Key Features (May 2026 Update)
- **Dynamic Workflows**: Claude can now dynamically adjust its execution plan based on real-time feedback from terminal commands and test results.
- **Universal MCP Tunnels**: Native support for secure tunnels to self-hosted [Model Context Protocol](../../knowledge_base/patterns/tool-calling-and-mcp.md) servers, even behind NAT/Firewalls.
- **Subagent Orchestration**: Ability to spin up specialized "Subagents" in isolated contexts to handle high-compute reasoning without polluting the main conversation history.
- **Usage Breakdown**: The `/usage` command now provides detailed cost/limit breakdowns by category (Skills, Subagents, Plugins, and MCP Servers).
- **Persistent Containers**: Integration with Anthropic's managed sandboxes for safe, stateful execution of bash sessions and file operations that span multiple turns.

## Strengths
- **Frontier Performance**: Consistently tops coding benchmarks (e.g., 87.6% on SWE-bench as of May 2026).
- **Tool-Calling Excellence**: Highly reliable execution of terminal commands, file edits, and MCP tool calls.
- **Transparency**: Native support for viewing "Thinking Blocks," allowing developers to inspect the agent's reasoning before it acts.
- **Multi-Environment**: Seamlessly switches between local, remote (SSH), and containerized development.

## Limitations
- **Token Intensity**: Autonomous loops can quickly consume large amounts of context and API tokens.
- **technical Setup**: Requires technical configuration of MCP servers and environment variables for maximum effectiveness.

## When to use it
- For "Agentic Engineering" where you want to delegate entire tasks rather than just get code suggestions.
- When working on large, complex codebases where manual context gathering is time-consuming.
- When you need to integrate with external tools (GitHub, Slack, Jira) via MCP.

## When not to use it
- For simple, one-off logic questions (use the [Claude web interface](https://claude.ai)).
- In environments where outbound network access or local file access is strictly prohibited for AI tools.

## Getting started

### Installation
Install Claude Code via the official bootstrap script:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

### Initial Setup
Run the authentication and configuration wizard:

```bash
claude auth login
claude init
```

## CLI & Slash Commands
Claude Code features a robust set of built-in commands:

```text
/usage    # Show detailed token and cost breakdown
/compact  # Summarize history to free up context window
/review   # Perform a professional-grade audit of staged changes
/doctor   # Diagnose environment and MCP connectivity issues
/rewind   # Undo the last turn to remove failed reasoning or code
```

## Advanced Patterns

### 1. The Verification Loop
Always instruct Claude to verify its work. A common pattern is:
*"Implement feature X, then run the relevant tests. If they fail, fix the code. Repeat until tests pass."*

### 2. CLAUDE.md Optimization
Keep a `CLAUDE.md` file in the root of your repo. Use it to define:
- Build/Test commands.
- Coding style rules.
- Important architecture constraints.
Claude reads this file at the start of every session.

### 3. MCP Server Management
Extend Claude's "senses" by adding MCP servers:
```bash
# Add a server for live web search
claude mcp add web-search npx -y @modelcontextprotocol/server-fetch
```

## Related tools / concepts
- [Aider](aider.md): A popular open-source alternative for CLI-based AI coding.
- [big-AGI](../ai_knowledge/big-agi.md): The recommended multi-model GUI for professional AI workspaces.
- [Documentation Writer](../agents/documentation-writer.md): A specialized skill for repository maintenance.
- [Roo Code](../agents/roo-code.md): An open-source VS Code extension with similar agentic powers.

## Sources / references
- [Claude Code Official Documentation](https://code.claude.com/)
- [Anthropic Changelog](https://code.claude.com/docs/en/changelog)
- [Introducing Dynamic Workflows (May 2026)](https://releasebot.io/updates/anthropic/claude)
- [Claude Code Best Practices](https://github.com/shanraisshan/claude-code-best-practice)

## Contribution Metadata
- Last reviewed: 2026-05-30
- Confidence: high
