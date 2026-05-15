# Aider

## What it is
Aider is a command-line chat tool that allows you to code with LLMs directly in your local Git repository. It acts as a pair programmer that can read your code, understand the project structure, and apply edits directly to your files, followed by automated Git commits.

## What problem it solves
It bridges the gap between the LLM's reasoning and your local file system, eliminating the need for manual copy-pasting of code between a chat window and your editor. By managing context through a sophisticated "repository map," Aider allows models to reason about large codebases without exceeding token limits.

## Where it fits in the stack
**Development & Ops / AI Coding Assistant**. It acts as the "operator" that takes high-level instructions and translates them into file edits and git commands. It is often used in conjunction with editors like [VS Code](vscode.md) or [Zed](zed.md).

## Typical use cases
- **Feature Implementation**: "Add a login route to the Express app."
- **Refactoring**: "Convert all these functions to use async/await."
- **Bug Fixing**: "Fix the null pointer exception in the user controller."
- **Documentation**: "Write docstrings for all exported functions."
- **Test Generation**: "Create unit tests for the newly added validation logic."

## Getting started

### Installation
Aider can be installed via pip:

```bash
pip install aider-chat
```

### Basic Usage
Set your API key and run it in your git repository:

```bash
export ANTHROPIC_API_KEY=your-key-here
aider
```

## Technical examples

### Repository Map Optimization
Aider uses a `repo map` to provide context to the LLM. You can tune how much context is sent using the `--map-tokens` flag.

```bash
# Provide more context for complex architectural changes
aider --map-tokens 2048

# Use a specific model optimized for coding
aider --model anthropic/claude-3-5-sonnet-20240620
```

### Batch Processing (Non-Interactive)
You can use Aider in scripts or CI/CD pipelines by passing messages directly.

```bash
# Add a comment to every file in a directory
aider --message "Add a license header to all files in src/" src/*.js --yes
```

### Using with Local Models (Ollama)
Aider supports local models via Ollama, providing a completely private coding experience.

```bash
# Run with a local Llama 3 model served via Ollama
aider --model ollama/llama3
```

## Advanced CLI Flags
- `--read <file>`: Add a file to the chat for reference without allowing Aider to edit it.
- `--lint-cmd <command>`: Provide a command to run after edits to check for errors; Aider will attempt to fix any errors found.
- `--test-cmd <command>`: Provide a test command; Aider will attempt to fix the code if tests fail.
- `--commit`: Automatically commit changes (default). Use `--no-commit` to review changes before committing manually.

## Strengths
- **Git Integration**: Automatically commits changes with descriptive, high-quality messages.
- **Context Management**: The repository map is highly effective at providing relevant context without hitting token limits.
- **Flexibility**: Supports almost any LLM (via OpenAI, Anthropic, or OpenRouter).
- **Speed**: Optimized for fast, iterative coding loops in the terminal.

## Limitations
- **Focus**: Primarily designed for file editing; limited support for long-running autonomous tasks or browser interaction compared to tools like [OpenHands](openhands.md).
- **CLI Learning Curve**: Requires familiarity with the terminal and Git.
- **Token Usage**: Can be heavy on token consumption if not managed carefully (especially the repo map).

## When to use it
- For daily coding tasks where you want to remain in control but automate the typing/refactoring.
- When working in a Git-tracked repository.
- For quick fixes, refactors, and adding boilerplate or documentation.

## When not to use it
- For massive, multi-step architectural changes that require a higher level of autonomy (consider [Plandex](plandex.md)).
- When you need the agent to browse the web or interact with non-file system tools.

## Related tools / concepts
- [OpenHands](openhands.md): An autonomous AI agent for software engineering.
- [Plandex](plandex.md): An AI coding engine designed for complex, multi-step tasks.
- [Claude Code](claude-code-setup.md): Anthropic's official terminal-based coding assistant.
- [VS Code](vscode.md) and [Zed](zed.md): Editors often used alongside Aider.
- [Mentat](mentat.md): A similar terminal-based AI pair programming tool.
- [Codeium](codeium.md) and [GitHub Copilot](github_copilot.md): IDE-integrated completion engines.

## Sources / References
- [Aider Official Website](https://aider.chat/)
- [Aider GitHub Repository](https://github.com/paul-gauthier/aider)
- [Aider Documentation](https://aider.chat/docs/)

## Contribution Metadata
- Last reviewed: 2026-05-15
- Confidence: high
