# Aider

## What it is
Aider is a leading command-line AI pair programmer that allows developers to edit code across multiple files directly within their local Git repository. It utilizes a sophisticated "repository map" to provide LLMs with relevant context while managing the Git lifecycle, including automated commits with high-quality messages.

## What problem it solves
Aider eliminates the friction of copying and pasting code between a chat interface and an IDE. It solves the "context management" problem by automatically selecting the most relevant code snippets for a given task, enabling models like [Claude 4.8 Opus](../ai_knowledge/claude.md) and [GPT-5.5](../ai_knowledge/openai.md) to reason accurately about large, complex codebases without exceeding token limits.

## Where it fits in the stack
**Development & Ops / AI Coding Assistant**. It serves as a terminal-native operator that bridges high-level intent with local file system execution and Git version control.

## Typical use cases
- **Multi-file Refactoring**: Renaming symbols or updating API signatures across an entire project.
- **Test-Driven Development**: Generating tests and then iterating on code until the `--test-cmd` passes.
- **Legacy Code Onboarding**: Asking questions about a new repository and having Aider explain the flow.
- **Automated Documentation**: Generating JSDoc, Docstrings, or README updates based on the actual implementation.
- **Bug Fix Loops**: Providing a stack trace and letting Aider find and fix the root cause.

## Strengths
- **Native Git Integration**: Every successful edit is followed by a descriptive Git commit.
- **Language Agnostic**: Supports over 100 programming languages with optimized context gathering.
- **Advanced Context**: The repository map uses ctags to build a concise map of the entire project.
- **Frontier Model Support**: Day-zero support for [Claude 4.8](../ai_knowledge/claude.md), [GPT-5.5](../ai_knowledge/openai.md), and [Llama 4 Maverick](../ai_knowledge/qwen.md).
- **Interactive & Batch Modes**: Equally effective for real-time pair programming and automated scripts.

## Limitations
- **Terminal-Centric**: Users who prefer a GUI-first workflow may find the CLI-only interface restrictive compared to [Cursor](cursor.md).
- **State Management**: While excellent at editing, it lacks the deep autonomous "planning" stage found in [Plandex](plandex.md).
- **Connectivity**: Requires a stable internet connection for frontier model APIs (unless used with local providers like [Ollama](../../services/ollama.md)).

## When to use it
- When you want to remain in your terminal and maintain a tight Git-driven development loop.
- For tasks that require editing multiple files simultaneously with high precision.
- When working on large codebases where manual context gathering is prohibitive.

## When not to use it
- For high-level architectural planning that doesn't involve immediate code changes.
- If you require a full "agentic" experience that includes web browsing or cloud infrastructure management (use [Claude Code](claude-code.md) or [OpenHands](openhands.md)).

## Getting started

### Installation
Aider is best installed via `pip` or `pipx` for global availability:

```bash
pip install aider-chat
```

### Initial Setup
Set your provider API keys and launch Aider in your Git repo:

```bash
export ANTHROPIC_API_KEY=your_key
aider
```

## CLI examples

### Architect Mode with Claude 4.8
Use the architect mode for complex changes where reasoning is prioritized over immediate editing:

```bash
aider --model anthropic/claude-4-8-opus-20260528 --architect
```

### Automated Bug Fixing
Provide a test command and let Aider iterate until success:

```bash
aider --test-cmd "npm test" --message "Fix the failing tests in the auth module"
```

### Native MCP Integration (June 2026)
Attach an [MCP Server](../automation_orchestration/mcp.md) to give Aider additional capabilities like database access or web search:

```bash
aider --mcp npx -y @modelcontextprotocol/server-postgres --mcp-config database_url=...
```

## API examples

### Non-interactive Python Scripting
Aider can be invoked as a library or via subprocess for automated pipelines:

```python
import subprocess

def run_aider_task(prompt, files):
    cmd = ["aider", "--message", prompt, "--yes-always"] + files
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

# Usage
# run_aider_task("Add type hints to this module", ["lib/core.py"])
```

### Configuration via .aider.conf.yml
Standardize Aider behavior across a team using a YAML config:

```yaml
model: anthropic/claude-4-8-opus-20260528
edit-format: diff
map-tokens: 2048
commit: true
dark-mode: true
```

## Related tools / concepts
- [Claude Code](claude-code.md) — Anthropic's agentic coding CLI.
- [Plandex](plandex.md) — Plan-first engineering engine for complex tasks.
- [Cursor](cursor.md) — The leading AI-native IDE.
- [Mentat](mentat.md) — Terminal-native multi-file editor.
- [OpenHands](openhands.md) — Autonomous agentic engineering.
- [Model Context Protocol](../automation_orchestration/mcp.md) — For extending Aider's toolset.
- [LlamaIndex](../../tools/ai_knowledge/llamaindex.md) — Often used in the underlying RAG patterns.
- [Zed](zed.md) — High-performance editor with native Aider integration.

## Sources / references
- [Aider Official Site](https://aider.chat/)
- [Aider GitHub Repository](https://github.com/paul-gauthier/aider)
- [Unified Edit Format Benchmarks (2026)](https://aider.chat/docs/benchmarks.html)
- [Aider MCP Integration Guide](https://aider.chat/docs/mcp.html)

## Contribution Metadata
- Last reviewed: 2026-06-11
- Confidence: high
