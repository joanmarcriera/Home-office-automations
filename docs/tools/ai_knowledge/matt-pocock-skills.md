# Matt Pocock Skills

## What it is
A repository of specialized skills for AI agents, including the "Grill-me" skill for rigorous plan verification. As of June 2026, these skills have been updated to leverage the advanced reasoning capabilities of **Claude 4.8**, **GPT-5.5**, and **Llama 4 Maverick**.

## What problem it solves
Extends agent capabilities with domain-specific execution scaffolds and critical thinking tools. It bridges the gap between raw LLM intelligence and professional software engineering rigor by enforcing structured workflows, preventing the "hallucination of competence" in complex system migrations.

## Where it fits in the stack
**Category**: AI & Knowledge / Agent Skills. These skills act as the "reasoning plugins" for autonomous agents like [Jules](jules.md), operating at the **Logic & Execution layer**.

## Typical use cases
- **Plan Verification**: Using `Grill-me` to ensure a proposed solution is robust before execution.
- **TDD Workflows**: Automating the Red-Green-Refactor loop with specialized skills for TypeScript and Python.
- **Complex Bug Diagnosis**: Leveraging multi-step diagnostic patterns for elusive production issues.
- **Agentic IDE Integration**: Enhancing [Claude Code](../development_ops/claude-code.md) or [Cline](../agents/cline.md) with custom skill sets via MCP.

## Strengths
- **Action-Oriented**: Provides concrete execution scaffolds rather than just passive advice.
- **Critical Thinking**: Specifically designed to force agents to "think twice" before acting.
- **Standardized**: Uses the `skills.sh` pattern for easy installation and updates across different environments.
- **Model-Agnostic**: Works across all frontier models, though optimized for those with high reasoning scores (e.g., GPT-5.5).

## Limitations
- **Setup Required**: Requires specific installation steps and sometimes tool configuration for local execution.
- **Learning Curve**: Agents may need specific instructions to effectively utilize some of the deeper skills like `tdd`.
- **Context Usage**: Complex skills can consume significant token context if not managed properly during long reasoning loops.

## When to use it
- When you need a "staff engineer" level of rigor from your AI assistant for critical infrastructure changes.
- For complex projects that benefit from structured planning and strict TDD enforcement.
- When working with autonomous agents that have full filesystem access and require high-confidence verification.

## When not to use it
- For quick, trivial scripts where the overhead of a "Grill-me" session is overkill for the task.
- If you prefer a completely custom, non-standardized skill setup without external dependencies.

## Getting started
1. **Install the CLI**: Use the official installer to add the skills to your local environment.
   ```bash
   npx skills@latest add mattpocock/skills
   ```
2. **Configure the Agent**: Add the setup command to your agent's system prompt or `CLAUDE.md`.
3. **Initialize**: Run `/setup-matt-pocock-skills` to configure integrations with your issue tracker and storage.

## CLI examples
Use the skills directly within your AI agent's interactive session or via standard shell commands.

```bash
# Verify a plan before execution (interactive)
/grill-me

# Use Test-Driven Development loop for the current file
/tdd

# Diagnose environment issues and version conflicts
/diagnose

# List all available Pocock skills
/skills list
```

## API examples
Agents can programmatically call these skills via a tool interface. Below is a Pydantic schema for the `GrillMeTool`.

```python
from pydantic import BaseModel, Field

class GrillMeArgs(BaseModel):
    plan: str = Field(..., description="The full text of the proposed execution plan.")
    question_count: int = Field(default=3, description="Number of challenging questions to ask.")
    context: str = Field(None, description="Additional technical context (e.g., repo architecture).")

# The agent invokes the tool:
# grill_me_tool.run(plan=current_plan, question_count=5)
```

## Related tools / concepts
- [Andrej Karpathy Skills](karpathy-skills.md): Complementary guidelines for simplicity and surgical changes.
- [Claude Code](../development_ops/claude-code.md): The primary IDE interface for these skills.
- [Claude Skills Ecosystem](../agents/claude-skills-ecosystem.md): The broader framework for agent capabilities.
- [Superpowers](../agents/superpowers.md): Pre-configured agent personas.
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md): The transport layer for skills.
- [Jules (Agent)](jules.md): A specialized agent that frequently utilizes these skills.
- [Cline](../agents/cline.md): An open-source agentic IDE that supports custom skill loading.
- [TDD Pattern](../../knowledge_base/patterns/tdd.md): The underlying methodology for the `/tdd` skill.

## Sources / references
- [Matt Pocock Skills (GitHub)](https://github.com/mattpocock/skills)
- [Total TypeScript - Professional AI Workflows](https://www.totaltypescript.com/)
- [The Grill-me Pattern for Agents](https://twitter.com/mattpocockuk)

## Contribution Metadata
- Last reviewed: 2026-06-28
- Confidence: high
