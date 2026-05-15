# Visual Studio Code (VS Code)

## What it is
Visual Studio Code is a lightweight but powerful source code editor which runs on your desktop and is available for Windows, macOS and Linux. It comes with built-in support for JavaScript, TypeScript and Node.js and has a rich ecosystem of extensions for other languages and runtimes.

## What problem it solves
It provides a highly extensible "middle ground" between a simple text editor and a heavy Integrated Development Environment (IDE). Its vast extension ecosystem makes it the primary platform for AI-powered development tools, allowing developers to mix and match different AI assistants and productivity tools.

## Where it fits in the stack
**Development & Ops / Editor**. It serves as the primary interface for coding and serves as the "host" for various AI extensions like GitHub Copilot, Continue, and Codeium.

## Typical use cases
- **General-Purpose Coding**: Supporting almost any language via extensions.
- **AI-Enhanced Development**: Running multiple AI assistants simultaneously.
- **Remote Development**: Connecting to remote servers, containers, or WSL via the Remote Development extension pack.
- **Cloud-Native Dev**: Integrating with Kubernetes, Docker, and various cloud providers (AWS, Azure, GCP).

## Getting started

### Installation
Download and install for your platform from the [official website](https://code.visualstudio.com/).

### Key Extensions for AI
- **GitHub Copilot**: The standard AI completion engine.
- **Continue**: Open-source autopilot that allows using any LLM.
- **Codeium**: Fast, free (for individuals) AI autocomplete and chat.
- **Tabnine**: Privacy-focused AI assistant.

## Technical examples

### Optimizing `settings.json` for AI Performance
To ensure AI extensions don't interfere with standard IDE features or each other, use specific configuration patterns.

```json
{
  "editor.inlineSuggest.enabled": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll": "explicit"
  },
  // Continue extension configuration (example)
  "continue.continueServerUrl": "http://localhost:65432",
  "continue.models": [
    {
      "title": "Claude 3.5 Sonnet",
      "provider": "anthropic",
      "model": "claude-3-5-sonnet-20240620",
      "apiKey": "${env:ANTHROPIC_API_KEY}"
    }
  ],
  // Disabling built-in completions to favor AI if needed
  "editor.suggest.showSnippets": false
}
```

### CLI Usage
VS Code provides a powerful CLI (`code`) for managing the editor and extensions.

```bash
# Open current directory in VS Code
code .

# Install an extension from the terminal
code --install-extension github.copilot

# Open a diff between two files
code --diff file1.txt file2.txt

# Run VS Code with a clean environment for debugging extensions
code --disable-extensions
```

## Strengths
- **Extensibility**: Unmatched library of plugins and themes.
- **Performance**: Faster than traditional IDEs while being more capable than basic editors.
- **Remote Capabilities**: Best-in-class support for remote development.
- **Ecosystem**: Most AI tools target VS Code as their first integration platform.

## Limitations
- **Resource Intensity**: Can consume significant memory with many active extensions.
- **Configuration Overhead**: Complex setups (especially with multiple AI tools) can require significant `settings.json` tweaking.
- **Built-in AI**: Unlike [Cursor](cursor.md) or [Zed](zed.md), AI features are secondary additions via extensions rather than natively integrated.

## When to use it
- When you need a versatile, battle-tested editor with the widest possible support for languages and tools.
- When you want to experiment with multiple different AI assistants (e.g., using Aider in the terminal and Copilot in the editor).
- When performing remote development on servers or in Docker containers.

## When not to use it
- When you want an editor that is "AI-native" where the AI has deep access to the editor's internals (consider [Cursor](cursor.md)).
- When you need maximum startup speed and minimal memory footprint (consider [Zed](zed.md)).

## Related tools / concepts
- [Zed](zed.md): A high-performance, Rust-based alternative.
- [Cursor](cursor.md): A fork of VS Code with deep AI integration.
- [Aider](aider.md): Terminal-based AI coding assistant often used alongside VS Code.
- [Claude Code](claude-code-setup.md): Anthropic's CLI-based coding tool.
- [Codeium](codeium.md): A popular extension for VS Code.
- [Tabnine](tabnine.md): A privacy-focused extension for VS Code.
- [GitHub Copilot](github_copilot.md): The flagship AI extension for VS Code.
- [Sourcegraph Cody](sourcegraph_cody.md): Another powerful AI extension focusing on context.

## Sources / references
- [Official Website](https://code.visualstudio.com/)
- [VS Code Documentation](https://code.visualstudio.com/docs)
- [Remote Development in VS Code](https://code.visualstudio.com/docs/remote/remote-overview)

## Contribution Metadata
- Last reviewed: 2026-05-15
- Confidence: high
