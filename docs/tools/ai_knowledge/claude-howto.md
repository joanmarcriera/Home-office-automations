# Claude How-To

## What it is
`claude-howto` is a curated collection of advanced technical guides and hands-on examples focused on mastering the Claude model family and its associated development ecosystem. As of July 2026, it serves as the primary educational resource for software engineers transitioning from basic prompt engineering to high-fidelity agentic engineering with Claude 5.1 and other frontier models.

## What problem it solves
It bridges the gap between conversational AI interfaces and functional, autonomous software development agents. The project provides structured, battle-tested guidelines for constructing specialised agent context files (such as `.claude/config.json` and `CLAUDE.md`), managing the Model Context Protocol (MCP 3.1), and optimizing token efficiency during iterative code modifications.

## Where it fits in the stack
**AI Assistants & Knowledge / Educational Layer**. It provides the operational playbook for developers utilizing the **Development & Ops** tooling layer, ensuring safe, consistent, and structured multi-agent interactions within active codebases.

## Typical use cases
- **Developer Workflow Standardization**: Setting up unified repo rules via `CLAUDE.md` to guide agents like Claude Code, Cursor, and Melty.
- **MCP 3.1 Server Deployment**: Guided building and deploying of custom Model Context Protocol (MCP 3.1) servers to provide agents with local filesystem and testing tools.
- **Autonomous Multi-Agent Orchestration**: Coordinating autonomous subagents under Claude 5.1 for automated pull-request reviews.
- **Prompt Caching Audits**: Configuring system prompts to match exact boundaries, maximizing cost-savings through Anthropic prompt caching.

## Strengths
- **SOTA Alignment**: Updated for Claude 5.1, featuring native multi-agent delegation frameworks and deep reasoning controls.
- **Interactive Environment**: Supports interactive assessments using Anthropic's CLI agent and custom `/self-assessment` hooks.
- **Security-First Focus**: Outlines advanced procedures to isolate agent execution using sandboxed containers and permission scopes.
- **Detailed Token Management**: Demonstrates practical patterns for optimizing context limits through active token counting.

## Limitations
- **Platform Concentration**: Highly specialized for the Anthropic ecosystem; the unique syntax patterns (such as slash commands and CLAUDE.md styles) do not map directly to alternative LLM CLI setups.
- **High Complexity**: Demands a solid baseline in software engineering and Python/Node.js scripting to leverage custom MCP servers.
- **Rapid Ecosystem Drift**: Heavy dependencies on specific CLI releases of Claude Code require frequent configuration maintenance.

## When to use it
- When implementing a repository-wide standard for how autonomous coding assistants interact with your team's code.
- When creating custom tools for Claude via the Model Context Protocol (MCP 3.1) specifications.
- When training software engineering teams to transition from standard autocomplete extensions to fully agentic workflows.

## When not to use it
- If your development team exclusively utilizes web UI assistants rather than terminal or IDE integrated agents.
- If your workflow is strictly limited to proprietary Microsoft or OpenAI environments without room for custom CLI tool integrations.
- For high-level conceptual summaries of AI that do not require operational commands or scripts.

## Getting started
To initialize the `claude-howto` guide locally, set up the development environment using Python and the `uv` package manager:

```bash
# Clone the educational repository
git clone https://github.com/luongnv89/claude-howto.git
cd claude-howto

# Setup environment with uv
pip install uv
uv venv
source .venv/bin/activate
uv pip install -r scripts/requirements-dev.txt

# Execute validation suite
pytest scripts/tests/
```

## CLI examples
The `claude-howto` repository includes scripts to generate study materials and verify local setup integrity.

### 1. Render Local Ebook Assets
```bash
# Compile markdown educational guides into offline EPUB assets
uv run scripts/build_epub.py --output-dir ./dist/
```

### 2. Execute Codebase Linting Check
```bash
# Verify formatting of the helper scripts and lessons
ruff check scripts/
ruff format --check scripts/
```

### 3. Launch the Terminal Learning Environment
```bash
# Open interactive shell assessment inside the Claude Code agent
/self-assessment --interactive --module "mcp-routing"
```

## API examples
While predominantly a text-based learning resource, `claude-howto` supplies Python utilities to automate educational workflow deployments.

### Automating Lesson Build Pipelines
```python
import os
import subprocess
import sys

def compile_educational_assets(target_format: str = "epub") -> bool:
    """
    Automates the compilation of markdown lessons into offline formats.
    Optimized for Python 3.11+ and compatible with uv environments.
    """
    if target_format not in ["epub", "pdf"]:
        print(f"Unsupported format: {target_format}", file=sys.stderr)
        return False

    try:
        result = subprocess.run(
            ["uv", "run", "scripts/build_epub.py", "--format", target_format],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"Compilation output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Asset compilation failed: {e.stderr}", file=sys.stderr)
        return False

if __name__ == "__main__":
    compile_educational_assets("epub")
```

## Related tools / concepts
- [Claude](claude.md) — The core AI model family.
- [Claude Code](../development_ops/claude-code.md) — Terminal-native agent for which this guide is optimized.
- [Everything Claude Code](everything-claude-code.md) — Comprehensive performance and optimization system for Claude.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standardized open protocol for connecting AI models to tools.
- [Cline](../agents/cline.md) — VS Code-based autonomous agent support.
- [Aider](../development_ops/aider.md) — Highly popular command-line editing agent.
- [Prompt Caching](../../knowledge_base/patterns/agentic-workflows.md) — Critical pattern for cost-effective agent usage.
- [GPT-5.5](openai.md) — Frontier model standard for comparison.
- [Llama 4](local_llms.md) — SOTA open-weights model for local workflows.
- [Claude Hooks](../development_ops/claude-hooks.md) — Specialized lifecycle management for terminal agents.

## Sources / references
- [claude-howto GitHub Repository](https://github.com/luongnv89/claude-howto)
- [Anthropic Developer Guides](https://docs.anthropic.com/)
- [Model Context Protocol (MCP) official site](https://modelcontextprotocol.io/)
- [Anthropic Prompt Caching Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)

## Contribution Metadata
- Last reviewed: 2026-07-27
- Confidence: high
