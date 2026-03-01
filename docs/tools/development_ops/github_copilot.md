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

### copilot chat commands
Use slash commands in the chat sidebar to perform specific tasks:
- `/explain`: Get an explanation of the selected code.
- `/fix`: Propose a fix for bugs in the selected code.
- `/tests`: Generate unit tests for the current file.

### workspace agent
Use the `@workspace` participant to ask questions about your entire project:
```text
@workspace How are the API routes structured in this project?
@workspace Where is the database connection initialized?
```

## Related tools / concepts
- [Codeium](codeium.md)
- [Tabnine](tabnine.md)

## Sources / references
- [Official Website](https://github.com/features/copilot)

## Contribution Metadata

- Last reviewed: 2026-02-28
- Confidence: medium
