# Zed

## What it is
Zed is a high-performance, multiplayer code editor from the creators of Atom and Tree-sitter. Written in Rust, it is designed to leverage every core of your CPU and every pixel of your GPU to provide an exceptionally fast and responsive coding experience. By late October and November 2026, it has matured into a leading AI-native IDE with first-class support for autonomous agents and the **Model Context Protocol (MCP 3.1)**.

## What problem it solves
It addresses the latency and resource consumption issues common in Electron-based editors (like [VS Code](vscode.md)). Furthermore, Zed integrates AI and real-time collaboration natively into the core of the editor, rather than treating them as secondary plugins. This allows for more seamless and high-performance AI interactions, especially when using frontier models like **Claude 5.1** and **GPT-5.5**, where instant feedback loops are critical for developer productivity.

## Where it fits in the stack
**Development & Ops / Editor**. It serves as a high-performance alternative to [VS Code](vscode.md) and [Cursor](cursor.md), particularly favored by developers working in performance-critical languages like Rust, C++, or Go, and those who require deep, native integration with **MCP 3.1** servers.

## Typical use cases
- **Low-Latency Coding**: Ideal for developers who are sensitive to input lag and want a "zero-latency" feel.
- **Native AI Pairing**: Using the built-in "Assistant" panel to chat with and apply code from models like **Claude 5.1** or **GPT-5.5**.
- **Collaborative Coding**: Real-time "multiplayer" editing where multiple developers can see and edit the same file simultaneously with extremely low latency.
- **MCP 3.1 Tool Integration**: Connecting to local or remote [MCP 3.1](../automation_orchestration/mcp.md) servers to give the editor's AI assistant specialized capabilities (e.g., database access, log analysis, API orchestration).
- **Local LLM Development**: Using local servers like Ollama to power code completions and chat with local open models like **Llama 4**.

## Strengths
- **Performance**: Extremely fast startup and zero-latency typing experience thanks to the GPUI framework and Rust-native core.
- **Native AI Integration**: The Assistant feels integrated into the UI/UX, supporting streamed edits and inline refactoring without the overhead of plugins.
- **Built-in MCP 3.1 Support**: First-class citizen for the **Model Context Protocol**, allowing easy expansion of AI capabilities via standard servers.
- **Resource Efficiency**: Significantly lower memory footprint compared to [VS Code](vscode.md), making it ideal for resource-constrained environments or massive monorepos.
- **Multiplayer**: Superior real-time collaboration features based on CRDTs, providing a seamless shared-editing experience.

## Limitations
- **Ecosystem**: While growing rapidly, the extension library is still smaller than the decade-old ecosystem of [VS Code](vscode.md).
- **Rust-Centric Extensions**: Writing custom extensions requires Rust knowledge (Wasm-based), which can be a higher barrier than TypeScript for some web developers.
- **Feature Depth**: Some deep IDE features for legacy enterprise stacks (e.g., complex Java/Enterprise .NET tooling) are still maturing compared to mature IDEs like IntelliJ.

## When to use it
- When you want the fastest possible editor performance and a minimalist, high-efficiency UI.
- When you frequently pair-program and need a robust, low-latency collaborative environment.
- When you want to leverage **MCP 3.1** servers natively with frontier models like **Claude 5.1** or **GPT-5.5**.
- When you are developing in Rust, Go, or other languages where Zed's performance advantages are most apparent.

## When not to use it
- When you rely on specific, complex [VS Code](vscode.md) extensions that do not yet have Zed equivalents.
- When working in corporate environments where Rust/Wasm extensions are restricted or unsupported.
- When you need a "heavy" IDE with deep, GUI-based management for legacy enterprise application servers.

## Getting started

### Installation
On macOS, Linux, and Windows (fully stable as of late 2026), Zed can be installed via a simple script or by downloading the binary:

```bash
curl https://zed.dev/install.sh | sh
```

### Configuration
Zed uses a JSON-based configuration file. You can open it via `Cmd+,` (macOS) or `Ctrl+,` (Linux/Windows).

#### Configuring Native AI (Anthropic/OpenAI)
```json
// ~/.config/zed/settings.json
{
  "assistant": {
    "default_model": {
      "provider": "anthropic",
      "model": "claude-5-1-sonnet-20261022"
    },
    "version": "2"
  },
  "language_models": {
    "anthropic": {
      "api_key": "YOUR_ANTHROPIC_API_KEY"
    },
    "openai": {
      "api_key": "YOUR_OPENAI_API_KEY"
    }
  }
}
```

#### Configuring Context Servers (MCP 3.1)
Zed uses the `context_servers` key in `settings.json` to manage MCP integrations.

```json
{
  "context_servers": {
    "home-admin-mcp": {
      "source": "custom",
      "command": {
        "path": "/usr/local/bin/home-admin-mcp",
        "args": ["--port", "8080"],
        "env": {
          "MCP_TOKEN": "YOUR_API_TOKEN"
        }
      }
    }
  }
}
```

### Key Bindings for AI
Zed provides several shortcuts for its AI assistant:
- `Cmd+Shift+>`: Open/Close Assistant panel.
- `Cmd+Enter`: Send message to AI.
- `Cmd+Shift+I`: Inline AI transformation (refactor selected code).

## CLI examples
The `zed` CLI (often aliased to `zedit`) allows you to interact with the editor from the terminal.

```bash
# Open a file or directory
zed .

# Open a specific file at a specific line
zed path/to/file.rs:42

# Open a file and wait for it to be closed (useful for git commits)
zed --wait README.md
```

## API examples
Zed's Extension API is primarily implemented in Rust and compiled to WebAssembly (Wasm).

### extension.toml (Metadata)
```toml
id = "mcp-extension"
name = "MCP Tool Integration"
version = "0.3.0"
schema_version = 1
authors = ["Home Admin <admin@homelab.local>"]
description = "Adds specialized tools via MCP 3.1."
repository = "https://github.com/homelab/zed-mcp"

[lib]
kind = "rust"
```

### Rust (Extension Logic - Snippet)
```rust
use zed_extension_api::{self as zed, Result};

struct MyExtension;

impl zed::Extension for MyExtension {
    fn new() -> Self {
        Self
    }
    // Extension implementation details...
}

zed::register_extension!(MyExtension);
```

## Related tools / concepts
- [VS Code](vscode.md) — The primary industry standard editor.
- [Cursor](cursor.md) — An AI-native editor fork of VS Code.
- [Aider](aider.md) — Terminal-based AI coding assistant that complements Zed.
- [Claude Code](claude-code.md) — Anthropic's agentic coding CLI for high-speed development.
- [Model Context Protocol](../automation_orchestration/mcp.md) — The standard for connecting AI to tools (MCP 3.1).
- [Codeium](codeium.md) — High-performance AI completion service with Zed support.
- [GitHub Copilot](github_copilot.md) — Standard AI completion service supported natively by Zed.

## Sources / references
- [Zed Official Website](https://zed.dev/)
- [Zed Documentation](https://zed.dev/docs)
- [Zed GitHub Repository](https://github.com/zed-industries/zed)
- [MCP 3.1 Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-11-01
- Confidence: high
