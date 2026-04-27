# Cline

## What it is
Cline (formerly Claude Dev) is an open-source, autonomous AI coding agent that runs directly inside VS Code and JetBrains IDEs. It has full access to the project files, terminal, and browser, allowing it to perform complex software development tasks.

## What problem it solves
It eliminates the "copy-paste" loop between an IDE and an AI chat interface. Instead of just suggesting code snippets, Cline can read the entire codebase, create or edit files, execute terminal commands (e.g., running tests, installing dependencies), and automate browser-based tasks.

## Where it fits in the stack
**Agent / IDE Extension / Developer Experience (DX)**.

## Typical use cases
- **Feature Implementation**: Implementing new features from a high-level description across multiple files.
- **Bug Fixing**: Running tests, identifying the cause of failures, and applying fixes autonomously.
- **Refactoring**: Performing large-scale refactors with human-in-the-loop approval.
- **Research & Browsing**: Using its built-in browser to research documentation or debug UI issues.

## Strengths
- **Fully Open Source**: Transparent and inspectable (Apache 2.0 license).
- **Human-in-the-Loop**: Asks for permission before executing commands or saving file changes.
- **Provider Agnostic**: Supports Anthropic, OpenAI, Google, AWS Bedrock, OpenRouter, and local models (via Ollama/LM Studio).
- **Tool Use**: Capable of using the filesystem, terminal, and browser.
- **IDE Native**: Works as a sidebar in VS Code, preserving your existing themes, keybindings, and extensions.

## Limitations
- **Latency**: Complex tasks using large context windows can be slow.
- **Token Cost**: Extensive "Act Mode" sessions can consume significant tokens.
- **Context Management**: While good, extremely large repositories can still challenge its attention.

## When to use it
- When you want an autonomous agent that stays inside your existing VS Code environment.
- For tasks that require iterating over terminal outputs (e.g., fixing test failures).
- When you prefer an open-source alternative to proprietary AI IDEs like Cursor.

## When not to use it
- For very small, single-file edits where a simple chat prompt is faster.
- In highly restricted environments where terminal access cannot be granted to an extension.

## Getting started

### Installation
1. Install the **Cline** extension from the VS Code Marketplace.
2. Configure your API provider (e.g., OpenRouter or Anthropic) in the extension settings.
3. Open the Cline sidebar and start a task.

## Licensing and cost
- **Open Source**: Yes (Apache 2.0).
- **Cost**: Free (Extension) + LLM API costs.
- **Self-hostable**: Yes (local models supported).

## Related tools / concepts
- [Roo Code](roo-code.md) (Popular fork/alternative)
- [Aider](../development_ops/aider.md) (Terminal-based agent)
- [Cursor](https://cursor.com/) (AI-native IDE)
- [Windsurf](../development_ops/windsurf.md) (Agentic IDE)

## Sources / References
- [Official GitHub](https://github.com/cline/cline)
- [Cline Wiki](https://github.com/cline/cline/wiki)
- [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev)

## Contribution Metadata
- Last reviewed: 2026-04-28
- Confidence: high
