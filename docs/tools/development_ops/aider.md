# Aider

## What it is
Aider is a command-line chat tool that allows you to code with LLMs directly in your local Git repository.

## What problem it solves
It bridges the gap between the LLM's reasoning and your local file system, allowing the model to read, edit, and commit code autonomously with your supervision.

## Where it fits in the stack
**Agent / Orchestration**. It acts as the "operator" that takes high-level instructions and translates them into file edits and git commands.

## Architecture overview
CLI tool that runs locally. It manages the context by selecting relevant files to send to the LLM (using a repo map) and applies the LLM's suggested changes back to the disk.

## Typical workflows
- **Feature Implementation**: "Add a login route to the Express app."
- **Refactoring**: "Convert all these functions to use async/await."
- **Bug Fixing**: "Fix the null pointer exception in the user controller."
- **Documentation**: "Write docstrings for all exported functions."

## Strengths
- **Git integration**: Automatically commits changes with descriptive messages.
- **Efficiency**: Only sends necessary code snippets to the LLM (repo map).
- **Flexibility**: Supports almost any LLM (via OpenAI, Anthropic, or OpenRouter).
- **Speed**: Optimized for fast, iterative coding loops.

## Limitations
- **Focus**: Primarily designed for file editing; limited support for long-running autonomous tasks or browser interaction.
- **Local only**: Usually runs where the code is; requires manual setup for remote execution unless running over SSH yourself.

## When to use it
- For daily coding tasks where you want to remain in control but automate the typing/refactoring.
- When working in a Git-tracked repository.
- For quick fixes and smaller features.

## When not to use it
- For massive, multi-step architectural changes that require a higher level of autonomy.
- When you need the agent to browse the web or interact with non-file system tools.

## Getting started

Install Aider via pip and run it in your git repository:

```bash
# Install Aider
pip install aider-chat

# Set your API key (optional if using local models)
export ANTHROPIC_API_KEY=your-key-here

# Start Aider in your project
aider
```

## CLI examples

### Hello World
Ask Aider to create a new file with a simple script:
```bash
aider hello-world.py
# In the chat: "Create a hello world script in python"
```

### Using Local Models (Ollama)
Aider supports local models via Ollama or LiteLLM:
```bash
# Run with a local Llama 3 model
aider --model ollama/llama3
```

### Commit Workflow
Aider automatically commits changes with descriptive messages:
```bash
# Start aider and it will track your session
aider

# After making changes via chat, aider will:
# 1. Show you the diff
# 2. Ask for confirmation (or auto-commit if configured)
# 3. Create a git commit: "feat: add login route to express app"
```

## Security considerations
- **File Access**: Aider has the same permissions as the user running it.
- **Commit History**: Review automated commits to ensure no secrets were accidentally added.

## Links to related pages
- [OpenHands](openhands.md)
- [OpenAI](../ai_knowledge/openai.md)
- [Anthropic](../providers/anthropic.md)

## Sources / References

- [Reference](https://aider.chat/)

## Contribution Metadata

- Last reviewed: 2026-02-27
- Confidence: medium
