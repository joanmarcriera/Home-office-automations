# Zed

## What it is
Zed is a high-performance, multiplayer code editor written in Rust, designed to leverage every core of the CPU and every pixel of the GPU. In June 2026, it has established itself as the leading alternative to Electron-based editors, offering native integration for **Claude 4.8** and **GPT-5.5** directly within its core "Assistant" framework.

## What problem it solves
It eliminates the input latency and heavy resource consumption typical of VS Code and other Electron editors. Zed's "native-first" approach to AI means that interactions with models like **Claude 4.8** are significantly faster, with deeper context awareness provided by the editor's high-performance indexing.

## Where it fits in the stack
**Development & Ops / Editor**. It is a core development environment favored by developers who prioritize speed, low latency, and integrated AI capabilities.

## Typical use cases
- **Performance-Critical Coding**: Ideal for Rust, C++, and Go development where responsive feedback is essential.
- **Native AI Pairing**: Using the built-in Assistant panel to chat with **Claude 4.8** or **GPT-5.5** for code generation and refactoring.
- **Low-Latency Collaboration**: Real-time "multiplayer" editing for remote pair programming with sub-10ms latency.
- **Local-First Development**: Using native indexing for fast project-wide search and navigation.

## Strengths
- **Rust-Powered Speed**: Near-instant startup and fluid typing experience on all platforms.
- **Native AI Integration**: Direct support for the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) for tool-using agents.
- **Cross-Platform Stability**: Fully stable support for Windows, Linux, and macOS (Apple Silicon optimized).
- **Multiplayer Editing**: Industry-leading real-time collaboration features.

## Limitations
- **Extension Library**: While growing, it remains smaller than the VS Code Marketplace.
- **Customization**: Offers a more opinionated experience with less UI flexibility than VS Code.
- **Feature Set**: Some legacy IDE features are still being ported to the high-performance Rust core.

## When to use it
- When you want the fastest, most responsive editor for modern software engineering.
- When you frequently use AI assistants and want them integrated natively into your workflow.
- For high-bandwidth collaborative sessions where low latency is critical.

## When not to use it
- When your workflow depends on highly specific, obscure VS Code extensions.
- When you require deep enterprise-level IDE features for specialized ecosystems (e.g., legacy .NET or Java).

## Getting started

### Installation
On all major platforms (macOS, Windows, Linux), Zed can be installed with a single command:

```bash
curl https://zed.dev/install.sh | sh
```

### AI Configuration
Set your primary model to **Claude 4.8** in your `settings.json`:

```json
{
  "assistant": {
    "default_model": {
      "provider": "anthropic",
      "model": "claude-4-8-opus-20260528"
    },
    "version": "2"
  }
}
```

## CLI examples

### 1. Opening Projects
Open a directory or file directly from the terminal:
```bash
zed .
zed src/main.rs:15
```

### 2. Git Integration
Set Zed as your default editor for Git operations:
```bash
export GIT_EDITOR="zed --wait"
```

### 3. CLI Assistant
Prompt the assistant directly from your terminal (via Zed's CLI tools):
```bash
zed ask "Explain the ownership model in this file"
```

## API examples

### Configuring Custom Models
Register a local or custom provider using the Zed configuration API:

```json
{
  "language_models": {
    "custom": {
      "name": "Local-Llama",
      "api_url": "http://localhost:11434/v1",
      "model": "llama-4-maverick"
    }
  }
}
```

### Using Inline AI
Trigger an inline refactor via shortcut (mapped to internal API call):
```bash
# internal command executed via Cmd+Shift+I
zed.ai_refactor(selection, "Convert this function to use async/await")
```

### MCP Tool Integration
Configure an MCP server for the Zed Assistant:

```json
{
  "mcp_servers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/path"]
    }
  }
}
```

## Related tools / concepts
- [VS Code](vscode.md) — The primary Electron-based alternative.
- [Cursor](cursor.md) — AI-native editor based on VS Code.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standard for connecting Zed to tools.
- [Claude Code](claude-code-setup.md) — Complementary terminal-based assistant.
- [Aider](aider.md) — Terminal-native AI coding tool.
- [Codeium](codeium.md) — AI extension compatible with Zed.
- [Tabnine](tabnine.md) — Privacy-first AI completions.
- [Claude 4.8](../ai_knowledge/index.md) — The target high-performance reasoning model.

## Sources / references
- [Official Website](https://zed.dev/)
- [Zed Documentation](https://zed.dev/docs)
- [Zed GitHub Repository](https://github.com/zed-industries/zed)
- [Zed Roadmap: June 2026 Update](https://zed.dev/blog/june-2026-update)

## Contribution Metadata
- Last reviewed: 2026-06-11
- Confidence: high
