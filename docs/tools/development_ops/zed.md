# Zed

## What it is
Zed is a high-performance, multiplayer code editor from the creators of Atom and Tree-sitter. Written in Rust, it is designed to leverage every core of your CPU and every pixel of your GPU to provide an exceptionally fast and responsive coding experience.

## What problem it solves
It addresses the latency and resource consumption issues common in Electron-based editors (like VS Code). Furthermore, Zed integrates AI and real-time collaboration natively into the core of the editor, rather than treating them as secondary plugins, which allows for more seamless and high-performance AI interactions.

## Where it fits in the stack
**Development & Ops / Editor**. It serves as a high-performance alternative to [VS Code](vscode.md) and [Cursor](cursor.md), particularly favored by developers working in performance-critical languages like Rust, C++, or Go.

## Typical use cases
- **Low-Latency Coding**: Ideal for developers who are sensitive to input lag.
- **Native AI Pairing**: Using the built-in "Assistant" panel to chat with models like Claude 3.5 Sonnet or GPT-4o.
- **Collaborative Coding**: Real-time "multiplayer" editing where multiple developers can see and edit the same file simultaneously with low latency.
- **Rust Development**: Excellent support for the Rust ecosystem, given the editor's heritage.

## Getting started

### Installation
On macOS or Linux, Zed can be installed via a simple script or by downloading the binary:

```bash
curl https://zed.dev/install.sh | sh
```

### Configuration
Zed uses a JSON-based configuration file. You can open it via `Cmd+,` (macOS) or `Ctrl+,` (Linux).

## Technical examples

### Configuring Native AI (Anthropic/OpenAI)
Zed allows you to configure multiple AI providers natively.

```json
// ~/.config/zed/settings.json
{
  "assistant": {
    "default_model": {
      "provider": "anthropic",
      "model": "claude-3-5-sonnet-20240620"
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

### CLI Usage
The `zed` CLI (often aliased to `zedit`) allows you to interact with the editor from the terminal.

```bash
# Open a file or directory
zed .

# Open a specific file at a specific line
zed path/to/file.rs:42

# Use zed as your git editor
export GIT_EDITOR="zed --wait"
```

### Key Bindings for AI
Zed provides several shortcuts for its AI assistant:
- `Cmd+Shift+>`: Open/Close Assistant panel.
- `Cmd+Enter`: Send message to AI.
- `Cmd+Shift+I`: Inline AI transformation (refactor selected code).

## Strengths
- **Performance**: Extremely fast startup and zero-latency typing experience.
- **Native AI Integration**: The Assistant feels integrated, not "bolted on".
- **Multiplayer**: First-class support for real-time collaboration.
- **Resource Efficiency**: Significantly lower memory footprint compared to VS Code.

## Limitations
- **Ecosystem**: Much smaller extension library than VS Code.
- **Platform Support**: Windows support is still in development/beta compared to the mature macOS and Linux versions.
- **Feature Maturity**: Lacks some of the deep "quality of life" features found in older IDEs.

## When to use it
- When you want the fastest possible editor performance.
- When you frequently pair-program and need a low-latency collaborative environment.
- When you want native AI features without the overhead of heavy VS Code extensions.

## When not to use it
- When you rely on specific, complex VS Code extensions that don't have Zed equivalents.
- When you are working on a Windows machine (check current status of Windows support).
- When you need deep, specialized IDE features for enterprise Java or .NET development.

## Related tools / concepts
- [VS Code](vscode.md): The primary competitor and industry standard.
- [Cursor](cursor.md): An AI-native editor based on VS Code.
- [Aider](aider.md): Terminal-based AI coding that complements high-performance editors.
- [Claude Code](claude-code-setup.md): Anthropic's CLI assistant.
- [Tabnine](tabnine.md): Privacy-focused AI completions.
- [Codeium](codeium.md): High-performance AI extensions.
- [GitHub Copilot](github_copilot.md): Standard AI completion service.
- [Sourcegraph Cody](sourcegraph_cody.md): Context-aware AI assistant.

## Sources / references
- [Official Website](https://zed.dev/)
- [Zed Documentation](https://zed.dev/docs)
- [Zed GitHub Repository](https://github.com/zed-industries/zed)

## Contribution Metadata
- Last reviewed: 2026-05-15
- Confidence: high
