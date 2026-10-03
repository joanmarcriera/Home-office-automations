# Claude How-To

## What it is
`claude-howto` is a curated, open-source technical reference repository and practical engineering framework focused on mastering the Claude model family and its associated developer tools ecosystem. As of early January 2027, it functions as the primary operational playbook for software engineers transitioning from simple chat interfaces and basic autocompletions to high-fidelity agentic software development with frontier reasoning models—including Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, and Qwen 3.6 VL.

The framework provides structured patterns, battle-tested agent configurations (e.g., `.claude/config.json`, `CLAUDE.md`), FastMCP 3.1 Task Protocol integrations, and exact prompt-caching boundary alignment practices that allow terminal agents like **Claude Code** to safely execute complex code modifications, run regression test suites, and orchestrate subagent swarms within production codebases.

## What problem it solves
- **Unstructured Agent Execution**: Without standardized project instruction contracts (such as `CLAUDE.md`), autonomous coding agents frequently introduce unwanted formatting churn, violate codebase architecture patterns, or modify build artifacts directly. `claude-howto` provides exact schema contracts for project rule enforcement.
- **Context Window Exhaustion & High Token Costs**: Naive agent loops quickly exhaust long context windows through repeated filesystem reads. `claude-howto` details exact prompt-caching boundary strategies and tool response compression techniques to reduce token expenditure by up to 80%.
- **Brittle Custom Tool Integrations**: Ad-hoc tool implementations often lack schema validation, causing agent tool calls to fail silently. `claude-howto` demonstrates strict Pydantic v2 schemas and FastMCP 3.1 server patterns for robust tool creation.
- **Uncontrolled Agent Mutations**: Unrestricted agent execution poses risks of unverified commits or unintended system state changes. `claude-howto` outlines multi-stage permission gates and containerized sandbox boundaries.

## Where it fits in the stack
**AI & Knowledge / Developer Operations Layer**. It sits at the intersection between **Agent Frameworks** ([Claude Code](../development_ops/claude-code.md), Cursor, Cline, Melty) and the **Execution Environment**, providing the configuration rules, MCP tool definitions, and prompt templates that govern agent behavior.

```
+-----------------------------------------------------------------------------------+
|                           Developer & Agent Interface                             |
|  +--------------------+   +-----------------------+   +------------------------+  |
|  |    Claude Code     |   |    Cursor / Cline     |   | Multi-Agent Orchestrator| |
|  | (Terminal Agent)   |   |   (IDE Integration)   |   | (Subagent Delegation)  |  |
|  +---------+----------+   +-----------+-----------+   +-----------+------------+  |
+------------|--------------------------|---------------------------|---------------+
             |                          |                           |
             +--------------------------+---------------------------+
                                        |
                                        v Reads Configuration & Protocols
                                        |  - CLAUDE.md (Project Rules Contract)
                                        |  - .claude/config.json (Permission Rules)
                                        |  - FastMCP 3.1 SSE / Stdio Connection
+---------------------------------------v-------------------------------------------+
|                          claude-howto Framework Core                              |
|  +-----------------------------------------------------------------------------+  |
|  |                     Context & Prompt Caching Manager                        |  |
|  |   +--------------------------+  +----------------------------------------+  |  |
|  |   | System Prompt Boundaries |  | Active Context Truncation Engine       |  |  |
|  |   +--------------------------+  +----------------------------------------+  |  |
|  +-----------------------------------------------------------------------------+  |
|  +-----------------------------------------------------------------------------+  |
|  |                       FastMCP 3.1 Tool Gateway                             |  |
|  |   +--------------------------+  +----------------------------------------+  |  |
|  |   | Pydantic v2 Validators   |  | Stdio / SSE Transport Adapter          |  |  |
|  |   +--------------------------+  +----------------------------------------+  |  |
|  +-----------------------------------------------------------------------------+  |
+---------------------------------------+-------------------------------------------+
                                        | Execution Calls
                                        v
+---------------------------------------+-------------------------------------------+
|                        Target Codebase & Tool Ecosystem                           |
|  +--------------------+   +-----------------------+   +------------------------+  |
|  | Local Git Repo /   |   |   Automated Tests     |   | Sovereign AI Stack     |  |
|  | File Tree Actions  |   |   (Pytest / Vitest)   |   | (Ollama / Nextcloud)   |  |
|  +--------------------+   +-----------------------+   +------------------------+  |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Repository Instruction Standardization (`CLAUDE.md`)**: Establishing standardized project rules, code style guidelines, build commands, and pre-commit verification steps that terminal agents read automatically upon invocation.
- **FastMCP 3.1 Custom Tool Server Setup**: Building custom Python or TypeScript FastMCP servers that grant agents safe read/write access to internal APIs, databases, or local home-lab services.
- **Subagent Multi-Task Delegation**: Configuring primary reasoner agents (Claude 5.6) to spawn parallel worker subagents (Claude 3.5 Haiku or local Gemma 4 instances) for widespread codebase refactoring and link checking.
- **Prompt Caching Boundary Alignment**: Structuring multi-thousand-token system instructions and static codebase maps behind fixed Anthropic prompt-caching boundaries to minimize input token billing.

## Architecture & Agent Execution Lifecycle

```
Developer / CI Workflow                  Claude Terminal Agent                  FastMCP 3.1 Tool Server
          |                                       |                                       |
          |  1. Invokes Agent (e.g., claude)      |                                       |
          |-------------------------------------->|                                       |
          |                                       |  2. Loads CLAUDE.md & .claude/config  |
          |                                       |  3. Connects to FastMCP Servers       |
          |                                       |-------------------------------------->|
          |                                       |  4. Returns Tool Capabilities List    |
          |                                       |<--------------------------------------|
          |                                       |                                       |
          |                                       |  5. Sends Prompt + System Context     |
          |                                       |     to Anthropic API (Prompt Cached)  |
          |                                       |                                       |
          |                                       |  6. Agent Decides Tool Invocation     |
          |                                       |     Calls Tool: `run_pytest`          |
          |                                       |-------------------------------------->|
          |                                       |  7. Returns Validated Tool Output     |
          |                                       |<--------------------------------------|
          |                                       |                                       |
          |  8. Receives Completed Code Mod &     |                                       |
          |     Passes Verification Gate          |                                       |
          |<--------------------------------------|                                       |
```

## Key Engineering Patterns

### 1. `CLAUDE.md` Structure
`claude-howto` defines a explicit structure for the root `CLAUDE.md` instruction contract:
- **Build & Test Commands**: Concise, copy-pasteable terminal commands for testing, linting, and building.
- **Code Style Guidelines**: Specific rules regarding typing, error handling, modularity, and file organization.
- **Repository Architecture**: High-level directory map outlining section ownership and key modules.
- **Pre-Commit Checklists**: Non-negotiable quality gates that agents must verify prior to calling git commit tools.

### 2. Prompt Caching Boundary Optimization
To leverage Anthropic's prompt caching:
- System prompts, repo architecture overviews, and static guidelines are positioned at the beginning of the context window.
- The `cache_control` header boundary (`{"type": "ephemeral"}`) is applied immediately after static system context.
- Dynamic tool outputs and conversation history follow the boundary, preventing cache invalidation across turn steps.

## Strengths
- **Battle-Tested Agentic Conventions**: Built on real-world engineering experiences with Claude Code, Cursor, and multi-agent systems.
- **Deep FastMCP 3.1 Integration**: Provides clear templates for writing typed, secure, and performant MCP servers in Python.
- **Token Efficiency Optimization**: Direct focus on cost reduction via prompt caching, context truncation, and compact tool responses.
- **Cross-Platform Compatibility**: Patterns apply to terminal agents (Claude Code, Aider), IDE extensions (Cline, Cursor), and web-based API wrappers.

## Limitations
- **Anthropic Ecosystem Centric**: Primary focus on Claude model family capabilities and Anthropic-specific features (such as `CLAUDE.md` auto-loading).
- **Requires CLI & Python Proficiency**: Maximum utility requires familiarity with terminal environments, virtual environments (`uv`), and Python/Pydantic scripting.
- **Fast Ecosystem Drift**: CLI tools and model context limits evolve quickly, requiring periodic updates to agent configuration specs.

## When to use it
- When setting up repository standards (`CLAUDE.md`) for autonomous coding agents operating on your codebase.
- When building custom tools via [FastMCP 3.1](../automation_orchestration/mcp.md) to integrate terminal agents with local infrastructure.
- When optimizing token usage and speed for iterative agent refactoring workflows.

## When not to use it
- If your development environment relies strictly on basic code completion without autonomous agent tool execution.
- If your stack relies purely on proprietary non-terminal web interfaces without codebase filesystem access.

## Getting started

```bash
# Clone the claude-howto educational repository
git clone https://github.com/luongnv89/claude-howto.git
cd claude-howto

# Setup virtual environment using uv
pip install uv
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Run linting and test validation suite
ruff check scripts/
pytest scripts/tests/
```

## CLI examples

### 1. Generate Project Instruction Contract (`CLAUDE.md`)
Use helper utilities to scaffold a repo-specific `CLAUDE.md` file:

```bash
uv run scripts/generate_claude_md.py --project-root . --tech-stack python-pydantic
```

### 2. Execute Prompt Caching Efficiency Audit
Audit context boundaries and estimate prompt caching efficiency:

```bash
uv run scripts/audit_cache_boundaries.py --config .claude/config.json
```

### 3. Interactive Agent Module Testing
Launch terminal self-assessment modules within Claude Code:

```bash
claude --prompt "Run /self-assessment module mcp-fastmcp-3.1"
```

## API examples

### Production FastMCP 3.1 Lesson & Tool Server

This production script demonstrates a FastMCP 3.1 tool server designed to manage lesson builds and validate developer configurations using **Pydantic v2**:

```python
import os
import json
from datetime import datetime
from typing import List, Optional, Dict, Any
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ValidationError

# Initialize FastMCP 3.1 Server
mcp = FastMCP("Claude-HowTo-Learning-Gateway")

# --- Pydantic v2 Validation Schemas ---

class LessonConfigInput(BaseModel):
    lesson_id: str = Field(..., pattern=r"^lesson-\d{3}$", description="Lesson identifier format (e.g. lesson-101)")
    title: str = Field(..., min_length=5, max_length=120, description="Title of the educational module")
    difficulty: str = Field(..., pattern=r"^(beginner|intermediate|advanced)$", description="Target difficulty tier")
    required_mcp_servers: List[str] = Field(default_factory=list, description="List of dependent MCP server IDs")
    review_date: str = Field(..., description="Date string in YYYY-MM-DD format")

    @field_validator("review_date")
    def validate_date_format(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("review_date must strictly match YYYY-MM-DD format")

class LessonValidationOutput(BaseModel):
    lesson_id: str
    title: str
    status: str
    is_ready_for_agent: bool
    summary_notes: str

# --- FastMCP 3.1 Tool Definitions ---

@mcp.tool(
    name="validate_educational_lesson",
    description="Validates a lesson configuration file against strict Pydantic v2 schemas for agentic training."
)
def validate_lesson(payload: LessonConfigInput) -> LessonValidationOutput:
    """Processes and validates lesson parameters, emitting agent-ready status."""
    mcp_count = len(payload.required_mcp_servers)
    ready = payload.difficulty in ["beginner", "intermediate"] or mcp_count > 0

    return LessonValidationOutput(
        lesson_id=payload.lesson_id,
        title=payload.title,
        status="VALIDATED",
        is_ready_for_agent=ready,
        summary_notes=f"Module '{payload.title}' validated successfully with {mcp_count} dependent MCP servers."
    )

@mcp.tool(
    name="generate_agent_rules_contract",
    description="Generates a standardized CLAUDE.md project instruction template based on tech stack inputs."
)
def generate_rules_contract(language: str, test_command: str) -> str:
    """Generates a structured CLAUDE.md template string."""
    return f"""# CLAUDE.md - Instructions Contract

## Language & Environment
- Primary Stack: {language}
- Verification Command: `{test_command}`

## Operational Rules
1. Always run `{test_command}` before completing tasks.
2. Maintain strict Pydantic v2 schemas for all API payloads.
3. Keep one canonical documentation page per tool/topic.
4. Do not commit build artifacts directly.
"""

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [Claude Code](../development_ops/claude-code.md): Terminal-native agent for which these patterns are designed.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md): Standard open protocol for connecting AI models to tools.
- [Everything Claude Code](everything-claude-code.md): Comprehensive system optimization guides for Claude.
- [Cline](../agents/cline.md): VS Code extension for autonomous agent execution.
- [Aider](../development_ops/aider.md): Terminal-based coding agent for local git repositories.
- [Claude Hooks](../development_ops/claude-hooks.md): Event lifecycle hooks for extending terminal agent workflows.

## Sources / references
- [claude-howto GitHub Repository](https://github.com/luongnv89/claude-howto)
- [Anthropic Official Developer Documentation](https://docs.anthropic.com/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [FastMCP 3.1 Task Protocol Specification](https://modelcontextprotocol.io/3.1/task-protocol)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
