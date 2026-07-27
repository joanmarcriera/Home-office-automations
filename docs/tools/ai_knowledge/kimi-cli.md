# Kimi Code CLI

## What it is
Kimi Code CLI (officially `kimi-cli`) is an open-source, terminal-native AI coding agent developed by Moonshot AI. Running as an interactive, agentic planning and execution loop inside the developer's command shell, it can read and edit files, run shell commands, perform real-time web searches, and autonomously troubleshoot errors. As of September 2026, it is a flagship tool for high-performance agentic engineering, natively integrated with **Moonshot Kimi K3**, Claude 5.1, and GPT-5.5.

## What problem it solves
Traditional chat-based AI interfaces require extensive copy-pasting, causing friction and context-switching overhead. Kimi Code CLI solves this by executing natively inside the terminal. Having direct, secure file-system access and shell execution capabilities, the agent can diagnose build failures, refactor sprawling multi-module files, and run tests independently, dramatically accelerating development cycles.

## Where it fits in the stack
**Development & Ops / AI Coding Agent**. Operating as a terminal-native pairing agent alongside tools like [Aider](../development_ops/aider.md) or [Claude Code](../development_ops/claude-code.md), it acts as a **Logic & Execution Agent** and integrates with local or remote services via the **Model Context Protocol (MCP 3.1)** and the **Agent Client Protocol (ACP)**.

## Typical use cases
- **Multi-File Structural Refactoring**: Asking the agent to restructure routing modules or migrate database frameworks across multiple files.
- **Autonomous Troubleshooting & Repair**: Feeding Kimi Code CLI a failing compiler error or test suite traceback and allowing it to iteratively locate and patch the bug.
- **Environment & Dependency Diagnostics**: Inspecting local directories, lockfiles, and virtual environments to rectify version mismatches and setup errors.
- **Workspace Navigation & Auditing**: Asking high-level architectural questions about unfamiliar code structures or performing repository-wide code reviews.

## Strengths
- **Native Shell Integration**: Operates directly inside standard terminal environments (bash, zsh) with complete tool and command execution loops.
- **Model Context Protocol (MCP 3.1)**: Full support for the MCP 3.1 protocol, enabling Kimi to command external servers, search tools, and APIs.
- **Real-Time Web Grounding**: Performs live semantic searches to verify the latest library documentation, APIs, and resolved issues online.
- **Rubin GPU Optimization**: Can be configured to route queries through local NVIDIA NIM (Inference Microservices) for near-instantaneous responses powered by local **NVIDIA Rubin** hardware.
- **Multi-Model Flexibility**: Native, first-class support for Kimi K3, Claude 5.1, and GPT-5.5.

## Limitations
- **Planning Latency**: As an agent running multi-turn loops, complex planning sequences can introduce processing latency before final files are modified.
- **Context Allocation**: Very large, flat folders can quickly expand the context window if local `.gitignore` files are not properly parsed.
- **Command Workarounds**: Standard interactive commands (like text editors or ssh requests) must be handled via virtual terminals to prevent shell blocking.

## When to use it
- When you want an autonomous pair programmer that can not only generate code but directly test and compile its own changes.
- For rapid workspace modifications, environment debugging, and complex refactoring tasks on remote SSH connections or dev containers.
- If you prefer keeping your hands on the keyboard and avoiding visual IDE GUI interfaces like Cursor.

## When not to use it
- For quick, throwaway snippets or queries that require no codebase or system execution context.
- In highly restricted enterprise terminals where shell process execution is locked down by strict security profiles.

## Getting started

### 1. Installation
Install Kimi Code CLI globally using the official installer script (requires Python 3.12+):

```bash
# Download and install via curl
curl -LsSf https://code.kimi.com/install.sh | bash

# Verify that the installation succeeded
kimi --version
```

### 2. Configure Your Environment
Run the login wizard to input your Moonshot or custom provider credentials:

```bash
# Initialize login and authorize terminal access
kimi /login
```

### 3. Verify Basic Execution
Run a simple, self-contained terminal test to ensure agentic execution is functioning:

```bash
kimi "Write a quick prime number generator in Python, save it as prime.py, and run it"
```

## CLI examples

You can call `kimi` directly from your command prompt with descriptive instruction prompts.

### 1. Initiate Multi-File Refactoring
Provide high-level architectural instructions for codebase modifications.

```bash
# Execute a comprehensive refactoring of the user model class
kimi "Refactor ./models/user.py to use Pydantic v2 validation instead of v1, and adjust all imports"
```

### 2. Run and Fix a Test Suite
Allow Kimi Code CLI to iteratively run tests, examine error traces, and apply patches until all pass.

```bash
# Feed test execution output directly to the agent loop
kimi "Run pytest on the auth suite. If any tests fail, locate the bug, fix it, and re-run until 100% green"
```

### 3. Explain and Document Complex Files
Generate structured documentation for unfamiliar parts of your repository.

```bash
# Request an architectural review and save the output
kimi "Explain the websocket connection lifecycle in our router and write a markdown summary to docs/"
```

## API examples

Kimi Code CLI supports advanced, programmatic configurations, allowing you to fine-tune system rules and local inference setups.

### 1. Manual Configuration File (~/.kimi/config.toml)
Configure local NVIDIA NIM and remote provider paths to switch between Kimi K3 and local GPU nodes.

```toml
# Configuration file for Kimi Code CLI - September 2026 SOTA

[default]
model = "kimi-k3-coding"
temperature = 0.1
max_turns = 15

[providers.moonshot]
type = "kimi"
base_url = "https://api.kimi.com/coding/v1"
api_key = "sk-moonshot-xxxxxxxxxxxxxxxxxxxxx"

[providers.nvidia-rubin]
type = "openai_legacy"
base_url = "http://localhost:8000/v1"
api_key = "local-nim-rubin"
model_mapping = "nvidia/kimi-k3-nim"
```

### 2. Zed IDE Integration (settings.json)
Natively run Kimi Code CLI inside the Zed editor using the standardized Agent Client Protocol (ACP).

```json
{
  "agent_servers": {
    "Kimi Code CLI": {
      "type": "custom",
      "command": "kimi",
      "args": ["acp", "--profile", "development"]
    }
  }
}
```

## Related tools / concepts
- [Aider](../development_ops/aider.md)
- [Claude Code](../development_ops/claude-code.md)
- [Mentat](../development_ops/mentat.md)
- [Plandex](../development_ops/plandex.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Agent Client Protocol (ACP)](../../knowledge_base/agent_protocols.md)
- [Moonshot AI](../providers/moonshot.md)
- [Terminal Benchmarking](../benchmarking/terminal-bench.md)
- [NVIDIA NIM](../providers/nvidia.md)

## Sources / references
- [Official Kimi Code CLI Repository](https://github.com/MoonshotAI/kimi-cli)
- [Kimi Code CLI Documentation](https://moonshotai.github.io/kimi-cli/en/guides/getting-started.html)
- [NVIDIA NIM for Kimi Models on Rubin Architecture](https://www.nvidia.com/en-us/ai-data-science/generative-ai/nim/)
- [Sébastien Dubois: Developer Review of Kimi CLI](https://www.dsebaisen.net/kimi-cli-guide)

## Contribution Metadata
- Last reviewed: 2026-09-04
- Confidence: high
