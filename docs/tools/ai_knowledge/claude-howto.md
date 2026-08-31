# Claude How-To

## What it is
`claude-howto` is a curated collection of advanced technical guides and hands-on examples focused on mastering the Claude model family and its associated development ecosystem. As of early January 2027, it serves as the primary educational resource for software engineers transitioning from basic prompt engineering to high-fidelity agentic engineering with Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, Qwen 3.6 VL, and other frontier reasoning models.

## What problem it solves
It bridges the gap between conversational AI interfaces and functional, autonomous software development agents. The project provides structured, battle-tested guidelines for constructing specialised agent context files (such as `.claude/config.json` and `CLAUDE.md`), managing the FastMCP 3.1 Task Protocol, and optimizing token efficiency during iterative code modifications.

## Where it fits in the stack
**AI Assistants & Knowledge / Educational Layer**. It provides the operational playbook for developers utilizing the **Development & Ops** tooling layer, ensuring safe, consistent, and structured multi-agent interactions within active codebases.

## Typical use cases
- **Developer Workflow Standardization**: Setting up unified repo rules via `CLAUDE.md` to guide agents like Claude Code, Cursor, and Melty.
- **FastMCP 3.1 Server Deployment**: Guided building and deploying of custom FastMCP 3.1 servers to provide agents with local filesystem and testing tools.
- **Autonomous Multi-Agent Orchestration**: Coordinating autonomous subagents under Claude 5.6 for automated pull-request reviews and live regression sweeps.
- **Prompt Caching Audits**: Configuring system prompts to match exact boundaries, maximizing cost-savings through Anthropic prompt caching.

## Strengths
- **SOTA Alignment**: Updated for early January 2027, featuring native multi-agent delegation frameworks and deep reasoning controls across Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, and DeepSeek-V4.
- **Interactive Environment**: Supports interactive assessments using Anthropic's CLI agent and custom `/self-assessment` hooks.
- **Security-First Focus**: Outlines advanced procedures to isolate agent execution using sandboxed containers and permission scopes.
- **Detailed Token Management**: Demonstrates practical patterns for optimizing context limits through active token counting and prompt caching boundary alignment.

## Limitations
- **Platform Concentration**: Highly specialized for the Anthropic ecosystem; the unique syntax patterns (such as slash commands and CLAUDE.md styles) do not map directly to alternative LLM CLI setups.
- **High Complexity**: Demands a solid baseline in software engineering and Python/Node.js scripting to leverage custom FastMCP servers.
- **Rapid Ecosystem Drift**: Heavy dependencies on specific CLI releases of Claude Code require frequent configuration maintenance.

## When to use it
- When implementing a repository-wide standard for how autonomous coding assistants interact with your team's code.
- When creating custom tools for Claude via the FastMCP 3.1 Task Protocol specifications.
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
While predominantly a text-based learning resource, `claude-howto` supplies Python utilities utilizing strict **Pydantic v2** validation schemas to automate educational workflow deployments and configure FastMCP 3.1 environments.

### Automating Lesson Build and Assessment Configuration
```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime
import json

class LessonConfig(BaseModel):
    """
    Validates educational lesson build parameters.
    Fully compliant with strict Pydantic v2 standards.
    """
    lesson_id: str = Field(..., pattern=r"^lesson-\d{3}$")
    title: str = Field(..., min_length=5, max_length=100)
    difficulty: str = Field(..., pattern=r"^(beginner|intermediate|advanced)$")
    required_mcp_servers: List[str] = Field(default_factory=list)
    last_reviewed: datetime
    is_active: bool = True

    @field_validator("last_reviewed", mode="before")
    @classmethod
    def parse_review_date(cls, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Review date must follow YYYY-MM-DD format.")
        return value

def load_and_validate_config(config_json: str) -> LessonConfig:
    """
    Loads and parses lesson configurations, guaranteeing runtime correctness
    with Pydantic v2 schema-enforcement.
    """
    data = json.loads(config_json)
    config = LessonConfig.model_validate(data)
    print(f"Successfully loaded and validated lesson: {config.title} [{config.lesson_id}]")
    return config

if __name__ == "__main__":
    sample_json = """
    {
        "lesson_id": "lesson-101",
        "title": "Mastering FastMCP 3.1 Tool Injection",
        "difficulty": "advanced",
        "required_mcp_servers": ["mcp-server-git", "mcp-server-context"],
        "last_reviewed": "2027-01-07"
    }
    """
    validated = load_and_validate_config(sample_json)
    print(validated.model_dump_json(indent=2))
```

## Related tools / concepts
- [Claude](claude.md) — The core AI model family.
- [Claude Code](../development_ops/claude-code.md) — Terminal-native agent for which this guide is optimized.
- [Everything Claude Code](everything-claude-code.md) — Comprehensive performance and optimization system for Claude.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standardized open protocol for connecting AI models to tools.
- [Cline](../agents/cline.md) — VS Code-based autonomous agent support.
- [Aider](../development_ops/aider.md) — Highly popular command-line editing agent.
- [Prompt Caching](../../knowledge_base/patterns/agentic-workflows.md) — Critical pattern for cost-effective agent usage.
- [GPT-5.6](openai.md) — Frontier model standard for comparison.
- [Gemma 4](local_llms.md) — SOTA open-weights model for local workflows.
- [Claude Hooks](../development_ops/claude-hooks.md) — Specialized lifecycle management for terminal agents.

## Sources / references
- [claude-howto GitHub Repository](https://github.com/luongnv89/claude-howto)
- [Anthropic Developer Guides](https://docs.anthropic.com/)
- [Model Context Protocol (MCP) official site](https://modelcontextprotocol.io/)
- [Anthropic Prompt Caching Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
