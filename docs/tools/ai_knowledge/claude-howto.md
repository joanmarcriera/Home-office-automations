# Claude How-To

## What it is
`claude-howto` is a collection of guides and examples focused on mastering Claude and its associated ecosystem, including Claude Code, MCP (Model Context Protocol), and advanced agentic patterns. As of June 2026, it is a primary resource for developers transitioning from basic LLM usage to high-fidelity agentic engineering.

## What problem it solves
It bridges the gap between conversational AI and functional AI agents. It provides structured, hands-on instructions for configuring specialized environment files (like `CLAUDE.md`), implementing complex tool-calling patterns, and mastering the low-level interactions required to make frontier models like `claude-4-8-opus-20260528` operate autonomously and reliably.

## Where it fits in the stack
**AI Assistants & Knowledge / Educational Layer**. It serves as the operational manual for the **Development & Ops** layer, specifically for teams using the Claude suite of tools for automation and coding.

## Typical use cases
- **Developer Onboarding**: Quickly training a team on the specific idioms and commands of Claude Code.
- **Agent Environment Setup**: Implementing standardized `CLAUDE.md` and hook configurations across a repository.
- **MCP Mastery**: Learning how to build, deploy, and connect custom MCP servers to extend agent capabilities.
- **Workflow Optimization**: Using lesson modules to reduce token usage and improve reasoning performance in agent loops.

## Strengths
- **Structured Learning**: Organized into progressive modules that build from basic CLI usage to advanced multi-agent orchestration.
- **Practical Templates**: Includes battle-tested configurations for slash commands and operational guardrails.
- **Visual Learning**: Extensive use of diagrams to explain the internal logic of features like prompt caching and tool-use cycles.
- **Interactive Assessments**: Built-in `/self-assessment` and `/lesson-quiz` hooks for personalized learning paths.
- **Production-Ready**: Focuses on real-world scenarios, avoiding "toy" examples in favor of complex engineering tasks.

## Limitations
- **Platform Specificity**: Deeply specialized for the Anthropic ecosystem; many patterns do not translate directly to other CLI agents.
- **Intensity**: Requires a significant time commitment (11-13 hours) for full mastery of the curriculum.
- **Dependency Heavy**: Relies on specific versions of Claude Code and Python development tools (like `uv`) for the interactive components.

## When to use it
- When you are migrating from a general-purpose IDE to an agent-first development workflow using Claude Code.
- When you need to standardize how AI agents interact with your codebase via `CLAUDE.md`.
- When training engineers to build custom Model Context Protocol (MCP) servers.

## When not to use it
- If you primarily use Claude through the web-based chat interface or mobile application.
- If your primary development stack is exclusively built around Microsoft's GitHub Copilot or OpenAI's proprietary IDE integrations.
- If you require a high-level conceptual overview rather than a deep technical "how-to."

## Getting started
To begin with the `claude-howto` guide, clone the repository and set up the development environment:

```bash
git clone https://github.com/luongnv89/claude-howto.git
cd claude-howto

# Set up environment using uv
pip install uv
uv venv
source .venv/bin/activate
uv pip install -r scripts/requirements-dev.txt

# Run initial verification
pytest scripts/tests/
```

## CLI examples
The `claude-howto` repository includes several utility scripts for managing the learning experience.

### 1. Build the Offline Ebook
```bash
# Generate an EPUB version of the entire guide for offline study
uv run scripts/build_epub.py
```

### 2. Run Quality Audit
```bash
# Verify the integrity of the lesson files and scripts
ruff check scripts/
ruff format --check scripts/
```

### 3. Start Interactive Assessment
From within a Claude Code session:
```bash
# Launch the skills assessment module
/self-assessment
```

## API examples
While primarily a documentation repository, `claude-howto` provides internal Python helpers for guide automation.

### Programmatic Build Trigger
```python
import subprocess
import sys

def build_educational_assets():
    try:
        subprocess.run(
            ["uv", "run", "scripts/build_epub.py"],
            check=True,
            capture_output=True,
            text=True
        )
        print("Ebook generated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during build: {e.stderr}", file=sys.stderr)

if __name__ == "__main__":
    build_educational_assets()
```

## Related tools / concepts
- [Claude](../development_ops/claude-code.md) — The core AI model family.
- [Claude Code](../development_ops/claude-code.md) — The terminal-based agent for which this guide is built.
- [Everything Claude Code](everything-claude-code.md) — Performance optimization ecosystem for Claude.
- [Model Context Protocol (MCP)](../../knowledge_base/agent_protocols.md) — The standard for connecting tools.
- [Cline](../agents/cline.md) — An alternative agentic interface for VS Code.
- [Aider](../development_ops/aider.md) — A popular terminal-based AI coding assistant.
- [Prompt Caching](../../knowledge_base/patterns/prompt-caching.md) — A critical pattern for cost-efficient agent usage.
- [GPT-5.5](openai.md) — The industry baseline for comparison.
- [Llama 4](../ai_knowledge/llama.md) — The open-weights alternative for local agentic workflows.

## Sources / references
- [claude-howto GitHub Repository](https://github.com/luongnv89/claude-howto)
- [Anthropic Developer Documentation](https://docs.anthropic.com/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
