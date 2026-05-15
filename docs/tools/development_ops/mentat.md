# Mentat

## What it is
Mentat is an AI tool that coordinates complex changes across multiple files directly from the terminal. It uses LLMs to understand the codebase and apply edits, focusing on developer productivity and precise control. Unlike many IDE-based assistants, Mentat is designed to handle large-scale refactors where the context spans dozens of files.

## What problem it solves
Enables developers to make coordinated, multi-file changes from the terminal with AI assistance, reducing the manual effort of large refactors and cross-cutting edits. It eliminates the need to manually copy-paste code into a chat interface by providing a direct terminal-based "edit-loop".

## Where it fits in the stack
**Development & Ops**. Functions as a terminal-based AI coding assistant for multi-file editing, typically used alongside a standard IDE or text editor.

## Typical use cases
- Coordinating complex changes across multiple files
- Codebase-wide refactoring from the terminal
- Applying precise, controlled edits with AI assistance
- Generating unit tests for existing codebases

## Strengths
- **Terminal-native workflow**: Ideal for developers who prefer the command line.
- **Precise control**: Allows users to include or exclude specific files from the context.
- **Multi-file coordination**: Handles dependencies and cross-file impacts effectively.

## Limitations
- **External LLM dependence**: Requires an API key for OpenAI, Anthropic, or other providers.
- **Learning curve**: Terminal commands and configuration may be less intuitive than GUI alternatives.

## When to use it
- When you need precise, multi-file edits from the terminal.
- When codebase standardization tasks require coordinated changes across several modules.

## When not to use it
- When a graphical editor experience (like [Cursor](cursor.md)) is preferred.
- When single-file completions are the primary need.

## Getting started

### Installation
Mentat can be installed via pip:

```bash
pip install mentat-ai
```

### Configuration
Create a `.mentat_config.json` in your project root to manage model preferences and excluded files:

```json
{
  "model": "gpt-4-turbo-preview",
  "temperature": 0.2,
  "file_exclude": ["node_modules/", "dist/", "*.log"]
}
```

## CLI examples

### Basic multi-file edit
Start Mentat with specific files included in the context:

```bash
mentat src/main.py src/utils.py tests/test_main.py
```

### Interactive Refactoring
Once inside the Mentat shell, you can issue natural language commands:

```text
> Add a new 'Logger' class to utils.py and update main.py to use it for all error handling.
```

### Including directories
You can also include entire directories to provide broader context:

```bash
mentat src/ --exclude src/legacy/
```

## Related tools / concepts
- [Aider](aider.md) — Another popular terminal-based AI pair programmer.
- [Plandex](plandex.md) — For terminal-native complex refactoring.
- [Codeium](codeium.md) — For IDE-native AI assistance.
- [Claude Code](./claude-code.md) — Anthropic's official CLI for agentic coding.
- [Cursor](cursor.md) — An AI-native IDE for a GUI-first approach.
- [Continue](./continue_dev.md) — An open-source IDE extension for AI assistance.
- [Sweep](./sweep_dev.md) — For automating GitHub issues into PRs.
- [Superconductor](./superconductor.md) — Parallel agent sessions for rapid development.

## Sources / references
- [Official Website](https://www.mentat.ai/)
- [GitHub Repository](https://github.com/AbanteAI/mentat)

## Contribution Metadata
- Last reviewed: 2026-05-15
- Confidence: high
