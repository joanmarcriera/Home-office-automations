# Kimi Code CLI

## What it is
Kimi Code CLI (officially `kimi-cli`) is an open-source, terminal-native AI coding agent from Moonshot AI. It operates as an agentic loop directly in the terminal, capable of reading and editing code, executing shell commands, searching the web, and autonomously planning multi-step software development tasks.

## What problem it solves
It reduces context switching by bringing AI-powered software engineering capabilities into the developer's primary workspace: the terminal. Unlike standard chat interfaces, Kimi Code CLI has direct access to the local filesystem and shell, allowing it to perform actions like refactoring code, running tests, and fixing build errors autonomously.

## Where it fits in the stack
**Development & Ops / AI Coding Agent**. It is a CLI-native alternative to [Aider](../development_ops/aider.md) or [Claude Code](../development_ops/claude-code-setup.md), optimized for high-speed terminal interaction and agentic workflows in June 2026.

## Typical use cases
- **Autonomous Feature Implementation**: Describing a new feature and letting the agent write the code and verify it.
- **Automated Bug Fixing**: Providing a stack trace and letting the agent find the root cause and apply a patch.
- **Codebase Exploration**: Asking questions about unfamiliar architectures or "finding where X is implemented."
- **Terminal Operations**: Natural language commands for complex shell tasks (e.g., "Find all large log files and compress them").

## Key Features
- **Agentic Loop**: Plans, executes, and adjusts actions based on terminal feedback.
- **Shell Mode**: Press `Ctrl-X` to switch between chatting with the agent and running direct shell commands.
- **ACP Support**: Native support for the **Agent Client Protocol**, enabling integration with IDEs like [Zed](../development_ops/zed.md) or JetBrains.
- **Web Access**: Can search and fetch live documentation to ground its coding suggestions.

## Strengths
- **Native Terminal Integration**: No need to leave the shell for AI assistance.
- **Multi-Model Support**: Can be configured to use Moonshot's Kimi K2 models or any OpenAI-compatible API.
- **Extensible**: Supports custom providers and headers via a TOML configuration.

## Limitations
- **Latency**: Agentic reasoning steps can take time, especially for complex planning.
- **Shell Compatibility**: Some built-in shell commands like `cd` are currently handled via a workaround in specific modes.
- **Model specific**: Optimized for Kimi K2; performance may vary with third-party model providers.

## When to use it
- When you want an AI pair programmer that can actually *run* the code it writes.
- For rapid refactoring tasks across multiple files.
- When working in remote SSH environments where a browser-based AI is inaccessible.

## When not to use it
- For simple snippets that don't require file or shell context (use a standard chat).
- If you prefer a GUI-first experience (use [Cursor](../development_ops/cursor.md)).

## Getting started

### Installation
Install using the official script (requires Python 3.12+):

```bash
# Linux / macOS
curl -LsSf https://code.kimi.com/install.sh | bash

# Verify installation
kimi --version
```

### Initial Setup
Run the setup wizard to configure your API provider:

```bash
kimi /login
```

## CLI examples

### Refactor a module
Start an agentic session with a specific goal:
```bash
kimi "Refactor the authentication logic in src/auth.py to use JWT instead of sessions"
```

### Automated Bug Fixing
Provide a test command and let Kimi iterate until success:
```bash
kimi "Run the test suite and fix any failing tests in the reports module"
```

### Direct Agent Query
Ask Kimi to explain part of the codebase:
```bash
kimi "Where is the database connection pooling logic implemented?"
```

## API examples

### Agent Client Protocol (ACP) Configuration
Kimi Code CLI supports the Agent Client Protocol. To use it as an agent server in [Zed](../development_ops/zed.md), add this to your `settings.json`:

```json
{
  "agent_servers": {
    "Kimi Code CLI": {
      "type": "custom",
      "command": "kimi",
      "args": ["acp"]
    }
  }
}
```

### Manual Provider Config (~/.kimi/config.toml)
For advanced users, providers can be configured manually using TOML:

```toml
[providers.kimi-for-coding]
type = "kimi"
base_url = "https://api.kimi.com/coding/v1"
api_key = "sk-xxxxxxxxxxxx"

[providers.openai-local]
type = "openai_legacy"
base_url = "http://localhost:11434/v1"
api_key = "ollama"
```

## Related tools / concepts
- [Aider](../development_ops/aider.md) — Multi-file AI pair programmer.
- [Claude Code](../development_ops/claude-code-setup.md) — Anthropic's agentic CLI.
- [Mentat](../development_ops/mentat.md) — Terminal-native coding assistant.
- [Plandex](../development_ops/plandex.md) — Complex task planning engine.
- [Agent Client Protocol (ACP)](../../knowledge_base/agent_protocols.md) — Standardized agent-IDE communication.
- [Moonshot AI](../providers/moonshot.md) — The provider of Kimi models.
- [Terminal Benchmarking](../benchmarking/terminal-bench.md) — Evaluating terminal-based agents.

## Sources / References
- [Official Kimi Code CLI Repository](https://github.com/MoonshotAI/kimi-cli)
- [Kimi Code CLI Documentation](https://moonshotai.github.io/kimi-cli/en/guides/getting-started.html)
- [Sébastien Dubois: Kimi CLI Overview](https://www.dsebastien.net/kimi-cli/)

## Contribution Metadata
- Last reviewed: 2026-06-24
- Confidence: high
