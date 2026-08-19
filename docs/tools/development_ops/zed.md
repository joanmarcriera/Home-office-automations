# Zed

## What it is
Zed is a high-performance, multiplayer code editor from the creators of Atom and Tree-sitter. Written in Rust, it leverages multi-core CPU threading and GPU hardware acceleration via the GPUI framework to provide a responsive, low-latency editing experience. As of early 2027, it has matured into a leading AI-native IDE with first-class support for agentic workflows, streaming inline transformations, and the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) FastMCP 3.1 standard.

## What problem it solves
It resolves the input latency, startup overhead, and memory bloating associated with Electron-based editors (such as [VS Code](vscode.md)). Furthermore, Zed embeds AI pairing and real-time multiplayer collaboration directly into the editor kernel rather than offloading them to secondary extensions. This enables instant feedback loops when pairing with frontier models like **Claude 5.1**, **GPT-5.5**, and **Gemini 4.0 Pro**.

## Where it fits in the stack
**Development & Ops / Editor**. It serves as a high-performance, resource-efficient alternative to [VS Code](vscode.md) and [Cursor](cursor.md), particularly favored by software engineers working in Rust, Go, C++, or TypeScript monorepos who require native **FastMCP 3.1** server integrations.

## Typical use cases
- **Zero-Latency Editing**: Providing sub-millisecond input response and high-FPS canvas rendering on large codebases.
- **Native AI Pairing**: Utilizing the built-in Assistant panel to stream code generation, refactoring, and inline edits from **Claude 5.1** or **GPT-5.5**.
- **Real-Time Multiplayer**: Collaborative pair programming using CRDT-based shared buffers with instant cursor synchronization.
- **FastMCP 3.1 Tooling**: Direct discovery and execution of [MCP 3.1](../automation_orchestration/mcp.md) servers for database inspection, log streaming, and API testing.
- **Local Model Routing**: Connecting to local [Ollama](../../services/ollama.md) instances to power zero-cost inline completions with open models like **Llama 4**.

## Strengths
- **Unrivaled Performance**: Instant startup times and zero input lag achieved through native Rust compilation and GPU acceleration.
- **Embedded AI Workspaces**: Streamlined Assistant UI supporting context-aware inline refactoring without extension overhead.
- **FastMCP 3.1 Native**: Out-of-the-box discovery and connection management for Model Context Protocol context servers.
- **Minimal Resource Footprint**: Significantly reduced RAM and CPU consumption compared to Electron IDE alternatives.
- **Collaborative CRDT Engine**: Superior multiplayer editing architecture for low-latency team pair programming.

## Limitations
- **Ecosystem Scale**: While expanding rapidly, the extension catalog is still smaller than the decade-old VS Code ecosystem.
- **Wasm/Rust Extension Model**: Developing custom plugins requires Rust knowledge and WebAssembly compilation target setups.
- **Legacy Enterprise Tooling**: Specialized GUI-based extensions for legacy enterprise application servers are still maturing.

## When to use it
- When requiring maximum editor responsiveness, low memory overhead, and minimal battery consumption.
- When pairing on live codebases using real-time multiplayer editing capabilities.
- When integrating **FastMCP 3.1** tool servers natively alongside frontier models (**Claude 5.1**, **GPT-5.5**).
- For high-speed development in Rust, Go, C++, Python, or TypeScript.

## When not to use it
- When strictly dependent on proprietary VS Code extensions lacking Zed Wasm equivalents.
- In enterprise environments that block WebAssembly extension runtimes or local binary execution.
- When requiring complex visual designer tools for legacy enterprise GUI applications.

## Getting started

### Installation
On macOS, Linux, and Windows, Zed can be installed via terminal or binary package:

```bash
curl https://zed.dev/install.sh | sh
```

### Configuration
Zed is configured via a central JSON configuration file (`settings.json`).

#### Configuring Native AI Providers
```json
{
  "assistant": {
    "default_model": {
      "provider": "anthropic",
      "model": "claude-5-1"
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

#### Configuring FastMCP 3.1 Servers
Zed manages Model Context Protocol integrations directly in `settings.json`:

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

### AI Assistant Shortcuts
- `Cmd+Shift+>` / `Ctrl+Shift+>`: Toggle Assistant Panel.
- `Cmd+Enter` / `Ctrl+Enter`: Execute AI Prompt.
- `Cmd+Shift+I` / `Ctrl+Shift+I`: Inline AI Refactor.

## CLI examples
The `zed` CLI binary allows invoking workspace instances directly:

```bash
# Open current directory in Zed
zed .

# Open specific file at line number 42
zed path/to/file.rs:42

# Block terminal until editor buffer closes (ideal for Git commit messages)
zed --wait README.md
```

## API examples
Zed extensions are authored in Rust and target WebAssembly (`wasm32-wasip1`).

### extension.toml (Metadata)
```toml
id = "mcp-extension"
name = "MCP FastMCP Tooling"
version = "0.4.0"
schema_version = 1
authors = ["Home Admin <admin@homelab.local>"]
description = "Integrates FastMCP 3.1 tools directly into Zed Assistant."

[lib]
kind = "rust"
```

### Rust Extension Implementation
```rust
use zed_extension_api::{self as zed, Result};

struct FastMcpExtension;

impl zed::Extension for FastMcpExtension {
    fn new() -> Self {
        Self
    }
}

zed::register_extension!(FastMcpExtension);
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
- Last reviewed: 2027-01-07
- Confidence: high
