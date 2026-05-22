# GitHub Copilot

## What it is
An AI pair programmer that provides autocomplete-style suggestions as you code. It is powered by OpenAI models and integrated into various IDEs. It can also be used via CLI.

## What problem it solves
Speeds up coding by generating inline code suggestions, reducing the time spent writing boilerplate and looking up API usage.

## Where it fits in the stack
**Development & Ops**. Provides AI-powered code completion as an IDE extension.

## Typical use cases
- Inline code completion while writing code
- Generating boilerplate and repetitive patterns
- CLI-based code generation

## Strengths
- Deep integration with GitHub ecosystem
- Supported in many popular IDEs
- Continuously improved with newer OpenAI models

## Limitations
- Requires a paid subscription
- Cloud-based; code snippets are sent to external servers for inference

## When to use it
- When you want a well-supported, mainstream AI code completion tool
- When working within the GitHub ecosystem

## When not to use it
- When strict local-only code processing is required
- When you prefer a free alternative (consider Codeium)

## Getting started

GitHub Copilot is available as an extension for VS Code, Visual Studio, JetBrains, and Neovim.

1. **Install**: Install the "GitHub Copilot" and "GitHub Copilot Chat" extensions.
2. **Auth**: Sign in to your GitHub account with an active Copilot subscription.
3. **Use**: Start typing to see inline suggestions, or press `Cmd+I` (Mac) / `Ctrl+I` (Windows) to open the chat.

## Usage examples

### Copilot Chat Commands
Use slash commands in the chat sidebar to perform specific tasks:
- `/explain`: Get an explanation of the selected code.
- `/fix`: Propose a fix for bugs in the selected code.
- `/tests`: Generate unit tests for the current file.

### GitHub Copilot CLI
The Copilot CLI brings AI assistance directly to your terminal for explaining commands or generating scripts.

```bash
# Install the GitHub CLI (if not already installed)
brew install gh

# Authenticate with GitHub
gh auth login

# Install the Copilot CLI extension
gh extension install github/gh-copilot

# Ask for a command explanation
gh copilot explain "git log --oneline --graph --all"

# Suggest a command for a task (interactive)
gh copilot suggest "find all large files over 100MB and delete them"

# Update the CLI extension
gh extension upgrade gh-copilot
```

### Workspace Agent
Use the `@workspace` participant to ask questions about your entire project with full context:
```text
@workspace How are the API routes structured in this project?
@workspace Where is the database connection initialized?
@workspace /explain How the authentication middleware works.
```

## Related tools / concepts

- [Codeium](codeium.md)
- [Tabnine](tabnine.md)
- [Claude Code — Project Setup Guide](claude-code-setup.md)
- [OpenCode (Oh My OpenCode Ecosystem)](opencode.md)
- [Sourcegraph Cody](sourcegraph_cody.md)
- [Aider](aider.md)
- [VS Code](vscode.md)
- [Zed](zed.md)

## Sources / references
- [Official Website](https://github.com/features/copilot)
- [Copilot CLI Documentation](https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-in-the-command-line)

## Contribution Metadata

- Last reviewed: 2026-05-15
- Confidence: high
