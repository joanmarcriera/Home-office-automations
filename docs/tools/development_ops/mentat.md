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
Create a `.mentat_config.json` in your project root to manage model preferences, temperature, and context inclusion rules:

```json
{
  "model": "gpt-4o",
  "temperature": 0.1,
  "file_exclude": [
    "node_modules/",
    "dist/",
    "*.log",
    ".git/",
    "__pycache__/"
  ],
  "maximum_context": 32000
}
```

## CLI examples

### Context Management
Mentat allows granular control over what the AI can see. You can include files, directories, or use glob patterns:

```bash
# Include specific files and a directory, while excluding a sub-path
mentat src/main.py src/utils/ tests/ --exclude tests/legacy/

# Use glob patterns to include all python files in a directory
mentat "scripts/**/*.py"
```

### Interactive Refactoring Loop
Once inside the Mentat shell, the "edit-loop" begins. You can provide instructions and Mentat will propose changes:

```text
> Search the codebase for all occurrences of hardcoded API endpoints and move them to a new config.py file.
>
> Mentat: [Proposes changes to 4 files]
>
> [y/n/i/e] (y: apply, n: skip, i: individual, e: explain)
```

### Scripting and Automation
You can run Mentat in a non-interactive mode for automated tasks or CI integration:

```bash
# Run a specific command and exit
mentat --run "Refactor all imports to use absolute paths"

# Use a specific model for a single run
mentat --model claude-3-5-sonnet-20240620 src/
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
