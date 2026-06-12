# Kimi Code CLI

## What it is
Kimi Code CLI (officially `kimi-cli`) is an open-source, terminal-native AI coding agent from Moonshot AI. It operates as an agentic loop directly in the terminal, capable of reading and editing code, executing shell commands, searching the web, and autonomously planning multi-step software development tasks.

## What problem it solves
It reduces context switching by bringing AI-powered software engineering capabilities into the developer's primary workspace: the terminal. Unlike standard chat interfaces, Kimi Code CLI has direct access to the local filesystem and shell, allowing it to perform actions like refactoring code, running tests, and fixing build errors autonomously.

## Where it fits in the stack
**Development & Ops / AI Coding Agent**. It is a CLI-native alternative to [Aider](../development_ops/aider.md) or [Claude Code](../development_ops/claude-code-setup.md), optimized for high-speed terminal interaction and agentic workflows.

## Typical use cases
- **Autonomous Feature Implementation**: Describing a new feature and letting the agent write the code and verify it.
- **Automated Bug Fixing**: Providing a stack trace and letting the agent find the root cause and apply a patch.
- **Codebase Exploration**: Asking questions about unfamiliar architectures or "finding where X is implemented."
- **Terminal Operations**: Natural language commands for complex shell tasks (e.g., "Find all large log files and compress them").

## Strengths
- **Agentic Loop**: Plans, executes, and adjusts actions based on terminal feedback.
- **Native Terminal Integration**: No need to leave the shell for AI assistance.
- **ACP Support**: Native support for the **Agent Client Protocol**, enabling integration with IDEs like Zed or JetBrains.
- **Web Access**: Can search and fetch live documentation to ground its coding suggestions.
- **Multi-Model Support**: Can be configured to use Moonshot's Kimi K2 models or any OpenAI-compatible API, including `claude-4-8-opus-20260528` and GPT-5.5 via local proxies.
- **Extensible**: Supports custom providers and headers via a TOML configuration.

## Limitations
- **Latency**: Agentic reasoning steps can take time, especially for complex planning.
- **Shell Compatibility**: Some built-in shell commands like `cd` are currently handled via a workaround rather than natively in all modes.
- **Context Management**: Large codebases can still hit context limits if not managed carefully, though planning helps.

## When to use it
- When you want an AI pair programmer that can actually *run* the code it writes.
- For rapid refactoring tasks across multiple files.
- When working in remote SSH environments where a browser-based AI is inaccessible.
- As a faster, terminal-native alternative to [Claude Code](../development_ops/claude-code-setup.md).

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

### Hello World Example
To verify Kimi is working correctly:

```bash
kimi "Write a 'hello world' script in Python and run it"
```

## CLI examples

```bash
# Refactor a specific module
kimi "Refactor the authentication logic in src/auth.py to use JWT instead of sessions"

# Find and fix errors
kimi "Run the test suite and fix any failing tests in the reports module"

# Explain code
kimi "Explain how the routing works in this project"
```

## API examples

### IDE Integration (Zed)
Kimi Code CLI supports the Agent Client Protocol (ACP). To use it as an agent server in Zed, add this to your `settings.json`:

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

### Manual Configuration (~/.kimi/config.toml)
For advanced users, providers can be configured manually:

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
- [Aider](../development_ops/aider.md)
- [Claude Code](../development_ops/claude-code-setup.md)
- [Mentat](../development_ops/mentat.md)
- [Plandex](../development_ops/plandex.md)
- [Agent Client Protocol (ACP)](../../knowledge_base/agent_protocols.md)
- [Moonshot AI](../providers/moonshot.md)
- [Terminal Benchmarking](../benchmarking/terminal-bench.md)

## Sources / References
- [Official Kimi Code CLI Repository](https://github.com/MoonshotAI/kimi-cli)
- [Kimi Code CLI Documentation](https://moonshotai.github.io/kimi-cli/en/guides/getting-started.html)
- [Sébastien Dubois: Kimi CLI Overview](https://www.dsebastien.net/kimi-cli/)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
