# Matt Pocock Skills

## What it is
A repository of specialized skills and execution scaffolds designed for AI agents, including the flagship "Grill-me" skill for rigorous plan verification. As of early 2027, these skills have been updated to leverage the advanced reasoning capabilities of frontier models including **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**, and **Llama 4 Maverick**.

## What problem it solves
It extends agent capabilities with domain-specific execution scaffolds and critical thinking tools. It bridges the gap between raw LLM intelligence and professional software engineering rigor by enforcing structured workflows, preventing the "hallucination of competence" in complex system migrations and architectural changes.

## Where it fits in the stack
**AI Assistants & Knowledge / Agent Skills**. These skills act as the "reasoning plugins" for autonomous agents like [Jules](jules.md), operating at the logic and execution layer of the agentic stack.

## Typical use cases
- **Plan Verification**: Using `Grill-me` to ensure a proposed solution is robust and handles edge cases before execution.
- **TDD Workflows**: Automating the Red-Green-Refactor loop with specialized skills for TypeScript, Rust, and Python.
- **Complex Bug Diagnosis**: Leveraging multi-step diagnostic patterns to isolate and fix elusive production memory leaks or race conditions.
- **Agentic IDE Integration**: Enhancing [Claude Code](../development_ops/claude-code.md) or [Cline](../agents/cline.md) with custom skill sets via FastMCP 3.1 servers.

## Strengths
- **Action-Oriented**: Provides concrete execution scaffolds rather than just passive advice.
- **Critical Thinking**: Specifically designed to force agents to "think twice" and self-correct before acting.
- **Standardized**: Uses the `skills.sh` pattern for easy installation and updates across diverse target environments.
- **Model-Agnostic**: Works across all frontier models, though optimized for those with high reasoning scores (e.g., GPT-5.5, Claude 5.1, Gemini 4.0 Pro).

## Limitations
- **Setup Required**: Requires specific installation steps and sometimes tool configuration for local execution.
- **Learning Curve**: Agents may need explicit guidance in their system prompt to effectively utilize deeper skills like `tdd`.
- **Context Usage**: Complex skills can consume significant token context if not managed properly during long, iterative reasoning loops.

## When to use it
- When you need a "staff engineer" level of rigor from your AI assistant for critical infrastructure or database migrations.
- For complex software projects that benefit from structured planning and strict TDD enforcement.
- When working with autonomous agents that have full filesystem access and require high-confidence verification.

## When not to use it
- For quick, trivial scripts where the overhead of a "Grill-me" session is overkill for the task.
- If you prefer a completely custom, non-standardized skill setup without external dependencies.

## Getting started
1. **Install the CLI**: Use the official installer to add the skills to your local environment (requires Node.js 22+).
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

### Programmatic Grill-Me Integration (FastMCP 3.1 with Pydantic v2)
The following Python script illustrates how an agent orchestrates the "Grill-me" skill programmatically using Pydantic v2 validation, feeding it into a structured JSON-RPC payload for a FastMCP 3.1 task handler.

```python
import json
import urllib.request
from pydantic import BaseModel, Field, field_validator
from typing import List

class GrillMePlan(BaseModel):
    plan_text: str = Field(..., description="The proposed technical plan text.")
    context_files: List[str] = Field(default_factory=list, description="Relevant file paths.")
    question_count: int = Field(default=3, description="Number of challenging questions to prompt.")

    @field_validator('question_count')
    @classmethod
    def validate_count(cls, v: int) -> int:
        if not (1 <= v <= 10):
            raise ValueError("question_count must be between 1 and 10")
        return v

def submit_grill_me_task(plan: GrillMePlan) -> dict:
    url = "http://localhost:8000/tasks/v1/grill"
    payload = {
        "jsonrpc": "2.0",
        "method": "grill_plan",
        "params": plan.model_dump(),
        "id": "pocock-skills-grill-001"
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))

# Example usage:
# proposal = GrillMePlan(plan_text="Migrate SQLite to Dolt database", question_count=5)
# print(submit_grill_me_task(proposal))
```

## Related tools / concepts
- [Andrej Karpathy Skills](karpathy-skills.md): Complementary guidelines for simplicity and surgical changes.
- [Claude Code](../development_ops/claude-code.md): The primary IDE interface for these skills.
- [Claude Skills Ecosystem](../agents/claude-skills-ecosystem.md): The broader framework for agent capabilities.
- [Superpowers](../agents/superpowers.md): Pre-configured agent personas.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Jules (Agent)](jules.md): A specialized agent that frequently utilizes these skills.
- [Cline](../agents/cline.md): An open-source agentic IDE that supports custom skill loading.
- [Skills Best Practices](../../knowledge_base/patterns/skills-best-practices.md): Underlying guidelines and methodology for writing clean, reusable agent tools.

## Sources / references
- [Matt Pocock Skills (GitHub)](https://github.com/mattpocock/skills)
- [Total TypeScript - Professional AI Workflows](https://www.totaltypescript.com/)
- [The Grill-me Pattern for Agents](https://twitter.com/mattpocockuk)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
