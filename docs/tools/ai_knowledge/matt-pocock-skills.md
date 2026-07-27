# Matt Pocock Skills

## What it is
A repository of specialized, execution-ready skill definitions and scaffolds designed for autonomous AI agents. Originally famous for the "Grill-me" planning and validation workflow, this collection serves as a premier library of behavioral scripts, test-driven development (TDD) loops, and interactive system diagnostics. As of September 2026, these skills have been upgraded to harness the native reasoning, planning, and tool-use capabilities of frontier models like **Claude 5.1**, **GPT-5.5**, **Llama 4**, and **Gemini 3.5 series**.

## What problem it solves
Raw LLMs often suffer from a "hallucination of competence" when attempting complex, multi-file software engineering tasks or system migrations. Matt Pocock Skills provide structured execution scaffolding, planning verification gates, and TDD guardrails. By forcing agents to systematically "think twice," write failing tests first, and aggressively cross-examine their proposed plans before editing files, this framework significantly reduces code regressions and bad implementations.

## Where it fits in the stack
**AI Assistants & Knowledge / Agent Skills**. These skills act as procedural plugins at the **Logic & Execution Layer**, integrating natively with agent execution setups (like [Jules](jules.md)), IDEs, and terminal environments via the **Model Context Protocol (MCP 3.1)** and the **Agent Client Protocol (ACP)**.

## Typical use cases
- **Plan Verification (Grill-me)**: Requiring the agent to submit its execution plan to a self-critique loop before modifying files.
- **Automated TDD Loops**: Enforcing a strict red-green-refactor workflow during complex Python or TypeScript feature additions.
- **Multi-File Diagnostic Audits**: Scanning workspace logs, lockfiles, and environment structures to resolve tricky dependency or version conflicts.
- **Terminal Agent Augmentation**: Feeding highly focused system commands to terminal-native coding tools like [Claude Code](../development_ops/claude-code.md) or [Kimi Code CLI](kimi-cli.md).

## Strengths
- **Strict Rigor**: Enforces robust pre-execution verification rather than relying on reactive bug fixing.
- **TDD Integration**: Promotes high code quality by automating the creation of failing test cases.
- **Model-Agnostic Design**: Works exceptionally well across all 2026 flagship reasoning models.
- **MCP 3.1 & ACP Ready**: Seamlessly hooks into IDEs like Cursor, Cline, or Zed via standardized agent transport protocols.

## Limitations
- **Token Context Overhead**: Interactive dialogue options (like large plan-grilling loops) can increase input context sizes.
- **Setup Requirements**: Requires proper workspace environment configurations and node/python runner setups for local verification tools.
- **Over-Caution**: Can occasionally introduce slight planning delays for simple, trivial adjustments.

## When to use it
- When an AI agent has write permissions to a local codebase and is executing complex, multi-layered features or migrations.
- For high-stakes, mission-critical infrastructure adjustments where a regression would cause immediate downtime.
- In team environments utilizing custom MCP-capable tools like [Cline](../agents/cline.md) or [Claude Code](../development_ops/claude-code.md).

## When not to use it
- For quick, single-line configuration file changes or spelling corrections.
- If the development team does not use agentic workflows and prefers standard autocomplete suggestions.

## Getting started

### 1. Global Installation
Install the skills CLI directly to your local development workspace via npm or yarn:

```bash
# Install the core Matt Pocock Skills tool suite
npx skills@latest add mattpocock/skills
```

### 2. Configure Your Agent
Configure your agent's system prompt or `CLAUDE.md` to load the skills suite. Add the following command to your agent's environment startup routine:

```bash
skills init --profile=knowledge-ops
```

### 3. Verify Interactive Mode
Test that the interactive "Grill-me" pattern is active:

```bash
# Trigger an interactive plan-grilling session
/grill-me
```

## CLI examples

Matt Pocock Skills can be invoked directly inside any active shell or within agent-run bash processes.

### 1. Run the Plan Validator (Grill-me)
Before making file changes, submit the current markdown plan to the agent-grilling engine.

```bash
# Grill a proposed plan located in plan.md, requesting 4 tough questions
skills grill --plan="./docs/reports/draft-plan.md" --questions=4 --strict
```

### 2. Execute Automated TDD Loop
Enforce a test-driven development loop on a target module.

```bash
# Runs the tdd skill, watching the auth file and running pytest on save
skills tdd --target="./src/auth.py" --test-runner="pytest"
```

### 3. Diagnose Workspace Environment Status
Verify dependency alignment and search for configuration drift.

```bash
# Run a comprehensive environment diagnostic check
skills diagnose --format=json > workspace_health.json
```

## API examples

The skills suite is exposed programmatically via JSON-RPC over the Model Context Protocol (MCP 3.1) or directly as callable Python modules in orchestration frameworks.

### Schema Definition for Grill-me Skill (MCP 3.1)
The following Python schema demonstrates how an agentic orchestrator represents and executes the `grill_me` skill.

```python
from pydantic import BaseModel, Field
from typing import Optional, List

class GrillMeSkillSchema(BaseModel):
    """
    Schema for the Grill-Me planning verification skill.
    Forces the agent to submit its plan for severe cross-examination.
    """
    proposed_plan: str = Field(
        ...,
        description="The full Markdown text of the proposed steps to resolve the issue."
    )
    question_count: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Number of critical edge cases or failure modes to challenge."
    )
    critical_dependencies: Optional[List[str]] = Field(
        default=None,
        description="List of modules or systems affected by this change."
    )

# Direct tool execution within an agent framework
# response = mcp_client.call_tool("mattpocock-skills", "grill_me", args={
#     "proposed_plan": "1. Replace MD5 with SHA-256 in user password hashing...",
#     "question_count": 5
# })
```

## Related tools / concepts
- [Andrej Karpathy Skills](karpathy-skills.md): Surgical code edits and lightweight change patterns.
- [Claude Code](../development_ops/claude-code.md): The primary IDE interface optimized for executing high-level skills.
- [Cline](../agents/cline.md): Open-source agentic IDE supporting custom toolsets.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md): The transport protocol for skills.
- [Agent Client Protocol (ACP)](../../knowledge_base/agent_protocols.md): Protocol for agent-to-IDE communication.
- [Jules (Agent)](jules.md): A specialized agent executing tasks on this workspace.
- [TDD Pattern](../../knowledge_base/patterns/tdd.md): Enforcing red-green-refactor loops.

## Sources / references
- [Matt Pocock Skills (GitHub)](https://github.com/mattpocock/skills)
- [Total TypeScript - Professional AI Workflows](https://www.totaltypescript.com/)
- [The Grill-me Pattern for Agents](https://twitter.com/mattpocockuk)
- [Model Context Protocol (MCP) 3.1 Specs](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2026-09-04
- Confidence: high
