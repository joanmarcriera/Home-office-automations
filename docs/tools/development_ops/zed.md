# Zed

## What it is
Zed is a high-performance, multiplayer code editor from the creators of Atom and Tree-sitter. Written in Rust, it is designed to leverage every core of your CPU and every pixel of your GPU to provide an exceptionally fast and responsive coding experience. By June 2026, it has matured into a leading AI-native IDE with first-class support for autonomous agents and complex tool-calling protocols.

## What problem it solves
It addresses the latency and resource consumption issues common in Electron-based editors (like VS Code). Furthermore, Zed integrates AI and real-time collaboration natively into the core of the editor, rather than treating them as secondary plugins, which allows for more seamless and high-performance AI interactions, especially when using frontier models like **Claude 4.8 Opus** and **GPT-5.5**.

## Where it fits in the stack
**Development & Ops / Editor**. It serves as a high-performance alternative to [VS Code](vscode.md) and [Cursor](cursor.md), particularly favored by developers working in performance-critical languages like Rust, C++, or Go, and those who require deep integration with the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md).

## Typical use cases
- **Low-Latency Coding**: Ideal for developers who are sensitive to input lag.
- **Native AI Pairing**: Using the built-in "Assistant" panel to chat with models like **Claude 4.8** or **GPT-5.5**.
- **Collaborative Coding**: Real-time "multiplayer" editing where multiple developers can see and edit the same file simultaneously with low latency.
- **MCP Tool Integration**: Connecting to local or remote [MCP](../automation_orchestration/mcp.md) servers to give the editor's AI assistant specialized capabilities (e.g., database access, API orchestration).
- **Local LLM Development**: Using [Ollama](../infrastructure/llama-cpp.md) or [vLLM](../infrastructure/vllm.md) to power code completions and chat with **Llama 4 Maverick**.

## Getting started

### Installation
On macOS, Linux, and Windows (GA as of early 2026), Zed can be installed via a simple script or by downloading the binary:

```bash
curl https://zed.dev/install.sh | sh
```

### Configuration
Zed uses a JSON-based configuration file. You can open it via `Cmd+,` (macOS/Windows) or `Ctrl+,` (Linux).

#### Configuring Native AI (Anthropic/OpenAI)
```json
// ~/.config/zed/settings.json
{
  "assistant": {
    "default_model": {
      "provider": "anthropic",
      "model": "claude-4-8-opus-20260528"
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

#### Configuring Context Servers (MCP)
Zed uses the `context_servers` key in `settings.json` to manage MCP integrations.

```json
{
  "context_servers": {
    "ionoscloud": {
      "source": "custom",
      "command": {
        "path": "/usr/local/bin/ionoscloud-mcp",
        "args": [],
        "env": {
          "IONOS_TOKEN": "YOUR_API_TOKEN"
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

# Open a file and wait for it to be closed (useful for git)
zed --wait README.md
```

## API examples
Zed's Extension API is primarily implemented in Rust and compiled to WebAssembly.

### extension.toml (Simplified)
```toml
id = "my-extension"
name = "My Zed Extension"
version = "0.1.0"
schema_version = 1
authors = ["Your Name <you@example.com>"]
description = "Adds specialized tools via MCP."
repository = "https://github.com/your/repo"

[lib]
kind = "rust"
```

## Strengths
- **Performance**: Extremely fast startup and zero-latency typing experience thanks to the GPUI framework.
- **Native AI Integration**: The Assistant feels integrated, not "bolted on", with support for streamed edits and inline refactoring.
- **Built-in MCP Support**: First-class citizen for the [Model Context Protocol](../automation_orchestration/mcp.md), allowing easy expansion of AI capabilities.
- **Resource Efficiency**: Significantly lower memory footprint compared to VS Code.
- **Multiplayer**: Superior real-time collaboration features (CRDT-based).

## Limitations
- **Ecosystem**: While growing, the extension library is still smaller than VS Code's decade-old ecosystem.
- **Rust-Centric Extensions**: Writing extensions requires Rust knowledge (Wasm-based), which can be a higher barrier than TypeScript for some.
- **Feature Depth**: Some deep IDE features for legacy enterprise stacks (e.g., complex Java/Enterprise .NET) are still maturing.

## When to use it
- When you want the fastest possible editor performance.
- When you frequently pair-program and need a low-latency collaborative environment.
- When you want to leverage [MCP](../automation_orchestration/mcp.md) servers natively with frontier models like **Claude 4.8**.
- When you prefer a minimalist, high-efficiency UI.

## When not to use it
- When you rely on specific, complex VS Code extensions that don't have Zed equivalents.
- When working in environments where Rust/Wasm extensions are restricted.
- When you need a "heavy" IDE with deep GUI-based management for legacy enterprise application servers.

## Related tools / concepts
- [VS Code](vscode.md) — The primary competitor and industry standard.
- [Cursor](cursor.md) — An AI-native editor based on VS Code.
- [Aider](aider.md) — Terminal-based AI coding that complements high-performance editors.
- [Claude Code](claude-code.md) — Anthropic's agentic coding CLI.
- [Model Context Protocol](../automation_orchestration/mcp.md) — The standard for connecting AI models to tools and data.
- [Claude](../ai_knowledge/claude.md) — Primary frontier model used in Zed's assistant.
- [Ollama](../infrastructure/llama-cpp.md) — For running local models like **Llama 4 Maverick** with Zed.
- [Codeium](codeium.md) — High-performance AI completion service.
- [GitHub Copilot](github_copilot.md) — Standard AI completion service supported by Zed.

## Sources / references
- [Official Website](https://zed.dev/)
- [Zed Documentation](https://zed.dev/docs)
- [Zed GitHub Repository](https://github.com/zed-industries/zed)
- [IONOS Cloud: Connecting Zed to MCP](https://docs.ionos.com/cloud/ai/mcp-server/connect-to-an-ai-client/zed)

## Contribution Metadata
- Last reviewed: 2026-06-10
- Confidence: high
