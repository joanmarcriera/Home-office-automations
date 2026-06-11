# Aider

## What it is
Aider is a command-line chat tool that allows you to code with LLMs directly in your local Git repository. As of June 2026, it is a leading AI pair programmer that supports **Claude 4.8 Opus** (`claude-4-8-opus-20260528`), **GPT-5.5**, and native **Model Context Protocol (MCP)** integration. It acts as an operator that can read your code, understand project structure via an advanced repository map, and apply edits with automated Git commits.

## What problem it solves
It bridges the gap between the LLM's reasoning and your local file system, eliminating the need for manual copy-pasting of code between a chat window and your editor. By managing context through a sophisticated, multi-level repository map, Aider allows models to reason about large, complex codebases without exceeding token limits or losing focus.

## Where it fits in the stack
**Development & Ops / AI Coding Assistant**. It acts as the "operator" that translates high-level instructions into file edits and git commands. It is often used in conjunction with high-performance editors like [Zed](zed.md) or [VS Code](vscode.md).

## Typical use cases
- **Feature Implementation**: "Add a login route to the Express app."
- **Refactoring**: "Convert all these functions to use async/await."
- **Bug Fixing**: "Fix the null pointer exception in the user controller."
- **Documentation**: "Write docstrings for all exported functions."
- **Test-Driven Development**: "Create unit tests and fix the code until they pass."
- **MCP Tool Use**: Using external MCP servers to query databases or cloud APIs during a coding session.

## Strengths
- **Git Integration**: Automatically commits changes with descriptive, high-quality, AI-written messages.
- **Context Management**: The advanced repository map is highly effective at providing relevant context for large projects.
- **Model Agnostic**: Supports a wide range of models via Anthropic, OpenAI, and [OpenRouter](../ai_knowledge/openrouter.md).
- **Native MCP Support**: First-class citizen for the Model Context Protocol, allowing seamless tool expansion.

## Limitations
- **CLI-Centric**: Requires comfort with the terminal and Git workflows.
- **Single-Agent Focus**: Primarily designed for a single pair-programming loop; less autonomous than multi-agent engines like [Plandex](plandex.md).

## When to use it
- For daily coding tasks where you want to remain in control but automate the typing and refactoring.
- When working in a Git-tracked repository.
- For quick fixes, refactors, and adding boilerplate or documentation.
- When you want to leverage [MCP](../automation_orchestration/mcp.md) servers directly in your terminal.

## When not to use it
- For massive, multi-step architectural changes that require a higher level of planning and execution (consider [Plandex](plandex.md)).
- When a graphical editor experience is the primary requirement (consider [Cursor](cursor.md)).

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
aider --model anthropic/claude-4-8-opus-20260528
```

## CLI examples

### Advanced Context and Model Control
Aider provides granular control over the coding environment:

```bash
# Use a specific model and enable MCP support
aider --model openai/gpt-5.5 --mcp

# Tune the repository map tokens for a large codebase
aider --map-tokens 4096

# Run a specific command and automatically fix errors
aider --message "Refactor the API" --lint-cmd "npm run lint" --test-cmd "npm test"
```

## API examples
Aider can be used as a Python library to build custom coding agents or automation scripts.

### Programmatic Pair Programming
```python
from aider.coders import Coder
from aider.models import Model

# Initialize a model and a coder session
model = Model("anthropic/claude-4-8-opus-20260528")
coder = Coder.create(main_model=model, fnames=["src/main.py"])

# Execute a coding task
coder.run("Add a robust error handler to the main function")

# Changes are automatically committed to Git
```

### Custom Repository Mapping
```python
from aider.repo_map import RepoMap

# Generate a map of the repository to provide context to an external LLM
repo_map = RepoMap(".")
map_content = repo_map.get_repo_map(["src/"], 1024)
print(map_content)
```

## Related tools / concepts
- [Claude Code](claude-code.md) — Anthropic's official agentic coding CLI.
- [Plandex](plandex.md) — AI coding engine for complex, multi-file tasks.
- [Mentat](mentat.md) — Terminal-native multi-file editor with MCP support.
- [OpenHands](openhands.md) — Autonomous AI agent for software engineering.
- [Zed](zed.md) — High-performance editor with native AI and MCP support.
- [Cursor](cursor.md) — AI-native IDE.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Standard for tool integration.

## Sources / References
- [Aider Official Website](https://aider.chat/)
- [Aider GitHub Repository](https://github.com/paul-gauthier/aider)
- [Aider Review 2026](https://aiagentslist.com/agents/aider)

## Contribution Metadata
- Last reviewed: 2026-06-10
- Confidence: high
