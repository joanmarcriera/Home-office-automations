# Andrej Karpathy Skills

## What it is
A curated collection of skills and patterns inspired by Andrej Karpathy's approach to AI and software engineering, designed to help agents avoid basic pitfalls. As of June 2026, these guidelines have been optimized for the extreme capabilities and potential over-engineering tendencies of **Claude 4.8**, **GPT-5.5**, and **Llama 4 Maverick**.

## What problem it solves
It codifies high-signal development habits and "instincts" into actionable patterns for AI agents. It specifically addresses the "hallucination of complexity" where advanced models attempt to solve simple problems with unnecessarily complex abstractions or massive library imports, ensuring code remains surgical and maintainable.

## Where it fits in the stack
**Category**: AI & Knowledge / Best Practices. These skills operate at the **Reasoning & Planning layer**, serving as a "sanity filter" for autonomous agents before they commit changes to the filesystem.

## Typical use cases
- **Agent Initialization**: Setting baseline "thinking" patterns in `CLAUDE.md` or system prompts for a new project.
- **Workflow Optimization**: Reducing agent hallucinations and "infinite loops" by enforcing clarifying questions.
- **Code Review Standard**: Using the "Surgical Changes" guideline as a checklist for automated or manual reviews.
- **MCP Constraint Enforcement**: Applying these patterns as system instructions for **Model Context Protocol 3.0** servers to ensure safe tool usage.

## Strengths
- **Low Overhead**: Simple Markdown-based guidelines that don't require complex infrastructure or external APIs.
- **High Signal**: Focuses on the most common and damaging mistakes (over-engineering, scope creep) made by frontier LLMs.
- **Developer-Centric**: Aligns AI behavior with senior-level software engineering best practices and the "Simplicity First" ethos.
- **Adaptive**: The guidelines become more valuable as models become more powerful and prone to speculative feature addition.

## Limitations
- **Opinionated**: Some patterns (like "minimal dependencies") might conflict with specific project styles that favor heavy framework usage.
- **Manual Enforcement**: Outside of specialized IDEs like Claude Code, requires manual inclusion in project context.
- **Nuance Dependent**: Requires the underlying model to have sufficient reasoning capability to identify when it is violating a principle.

## When to use it
- When you find your AI agent is making "obvious" mistakes or over-complicating simple bug fixes.
- At the start of a new project to establish a high bar for code quality and minimize technical debt.
- When configuring autonomous agents like [Jules](jules.md) for long-horizon, high-stakes tasks.

## When not to use it
- For highly experimental "creative" coding where standard engineering constraints might be too restrictive.
- In environments where a different, strict enterprise coding standard is already heavily enforced.

## Getting started
1. **CLAUDE.md**: The most effective way to apply these skills is by adding a `## Karpathy Instincts` section to your project's `CLAUDE.md`.
2. **Plugin Installation**: For users of Claude Code, install the community-maintained plugin:
   ```bash
   /plugin install andrej-karpathy-skills@latest
   ```
3. **Prompt Injection**: Include the "Zero-Draft" pattern in your initial agent task description to ensure small, verifiable steps.

## CLI examples
Management of Karpathy-inspired plugins via the agentic CLI.

```bash
# Verify the current project adheres to Karpathy simplicity standards
/plugin run karpathy-skills --audit

# Update the simplicity guidelines to the latest June 2026 version
/plugin update andrej-karpathy-skills

# List all active engineering constraints
/constraints list
```

## API examples
Agents can programmatically perform a "simplicity check" using a tool interface. Below is a Pydantic schema for a `SimplicityAuditTool`.

```python
from pydantic import BaseModel, Field

class SimplicityAuditArgs(BaseModel):
    code_snippet: str = Field(..., description="The code block to evaluate for complexity.")
    complexity_threshold: int = Field(default=5, description="Scale of 1-10; higher allows more abstraction.")
    language: str = Field("python", description="The programming language of the snippet.")

# The agent invokes the tool:
# simplicity_tool.run(code_snippet=new_function_code, complexity_threshold=3)
```

## Related tools / concepts
- [Matt Pocock Skills](matt-pocock-skills.md): Complementary skills focusing on TDD and plan verification.
- [Surgical Changes](https://peerlist.io/xiji2646/articles/the-978kstar-file-that-makes-claude-code-stop-overengineerin): The core philosophy behind these skills.
- [Claude Code](../development_ops/claude-code.md): The primary interface for Karpathy-style agentic development.
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md): The interface for enforcing these skills via tools.
- [Jules (Agent)](jules.md): A specialized agent optimized for these principles.
- [Superpowers](../agents/superpowers.md): Persona-based skill application.
- [TDD Pattern](../../knowledge_base/patterns/tdd.md): Enforced by the "Goal-Driven Execution" instinct.
- [Cline](../agents/cline.md): Supports custom engineering rulebooks.

## Sources / References
- [Andrej Karpathy Skills (GitHub)](https://github.com/forrestchang/andrej-karpathy-skills)
- [Andrej Karpathy's Recommendations for LLMs](https://karpathy.ai/llm.html)
- [The 'Simplicity First' Engineering Ethos](https://karpathy.ai/blog/simplicity.html)

## Contribution Metadata
- Last reviewed: 2026-06-28
- Confidence: high
