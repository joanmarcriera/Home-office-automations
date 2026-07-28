# Superpowers

## What it is
Superpowers is a comprehensive software development workflow and agentic skills framework designed for next-generation coding agents like [Claude Code](../development_ops/claude-code.md), [Cursor](../development_ops/cursor.md), and [Aider](../development_ops/aider.md). It builds on top of composable "skills" to enforce a rigorous engineering process, optimized for frontier models like [Claude 5.1](../providers/anthropic.md) and [GPT-5.5](../ai_knowledge/openai.md) while utilizing **Gemini 3.5/3.6 visual reasoning** for complex UI tasks and front-end verification.

## What problem it solves
It addresses the lack of discipline and engineering rigor in standard AI coding interactions by providing a structured, skills-based workflow for design, planning, and implementation. This prevents common failure modes like "hallucinating" file paths, circular refactoring, and code rot, ensuring high performance on benchmarks like [SWE-bench](../benchmarking/swe-bench.md).

## Where it fits in the stack
**Agents / Workflow Framework**. It sits on top of coding agents to provide process-level guardrails and skills. It is often used in conjunction with the [Desktop Commander MCP](../development_ops/desktop-commander-mcp.md) for direct filesystem and terminal control.

## Typical use cases
- Enforcing Test-Driven Development (TDD) and plan-first development in agentic workflows.
- Breaking down complex engineering tasks into verifiable sub-tasks.
- Managing long-running autonomous coding sessions that span multiple files.
- Maintaining code quality in large, complex repositories.
- Standardizing agent behavior across a distributed engineering team.

## Strengths
- **MCP 3.1 Task Protocol**: Native implementation of the standardized task protocol for multi-agent handoffs, state serialization, and verifiable progress.
- **Visual Reasoning**: Integration with **Gemini 3.5/3.6** for automated UI/UX verification and visual regression testing.
- **Process Rigor**: Enforces high-quality engineering standards (TDD, YAGNI, DRY).
- **Agent Autonomy**: Increases reliability through explicit verification steps and self-correction loops.
- **Context Handling**: Optimized for [Claude 5.1](../providers/anthropic.md)'s expanded token context window.

## Limitations
- Higher process overhead for trivial tasks.
- Requires an agent environment that supports the skills framework or MCP.
- May require significant prompt tokens for complex planning cycles (addressed by [Everything Claude Code](../ai_knowledge/everything-claude-code.md) optimizations).
- Learning curve for developers to define custom skill YAMLs.

## When to use it
- To enforce high-quality engineering standards (TDD, YAGNI, DRY) in agent-driven development.
- When you want agents to work autonomously for extended periods (hours) without deviating from a plan.
- For complex projects that require a systematic approach to design, planning, and implementation, as described in the [AI-Assisted Dev Workflow](../../playbooks/dev-workflow-ai-assisted.md).

## When not to use it
- For trivial code changes or simple questions.
- If you prefer an ad-hoc, conversational approach to coding without structured planning.
- In environments where agents lack terminal or filesystem access (though remote MCP can bridge this).

## Getting started

### Installation (Claude Code Plugin)
Superpowers is typically installed as a plugin or set of skills using the MCP 3.1 protocol:

```bash
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

### Enabling Visual Reasoning
To enable visual verification with Gemini 3.5:
```bash
superpowers config set vision_provider gemini-3.5-pro
```

### Creating custom skills
Create a simple `hello_world.yaml` skill file:

```yaml
name: "hello_world"
description: "Prints a greeting to the console."
implementation: |
  echo "Hello from Superpowers!"
```

### Configuring Task Guardrails
Add a `superpowers.json` to your project root to enforce verification:

```json
{
  "enforce_tdd": true,
  "required_reviewers": 1,
  "max_subtasks": 5
}
```

## CLI examples

```bash
# List all active Superpowers skills
superpowers list --active

# Initialize a new engineering plan for a task
superpowers plan "Refactor authentication logic to use JWT"

# Execute verification steps for a specific sub-task
superpowers verify --task-id 123 --file tests/auth_test.py
```

## API examples

### Defining a Verification Skill (YAML)
Skills are defined in YAML and consumed by the agent's tool-calling logic.

```yaml
# verify_test_coverage.yaml
name: "verify_coverage"
description: "Ensures test coverage is above a certain threshold."
parameters:
  type: "object"
  properties:
    threshold:
      type: "integer"
      default: 80
implementation: |
  coverage run -m pytest && coverage report --fail-under={{threshold}}
```

### Custom Task Verification (JSON)
For complex refactors, you can define custom verification steps in your `superpowers.json` file to ensure the agent performs regression tests before proposing a merge.

```json
{
  "tasks": [
    {
      "id": "refactor-auth-logic",
      "description": "Move auth logic to middleware",
      "files": ["src/middleware/auth.js", "src/routes/user.js"],
      "verification": "npm test src/tests/auth.test.js && curl -I http://localhost:3000/api/user"
    }
  ]
}
```

## Related tools / concepts
- [Agency-Agents](agency-agents.md)
- [Claude Code](../development_ops/claude-code.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Desktop Commander MCP](../development_ops/desktop-commander-mcp.md)
- [Aider](../development_ops/aider.md)
- [Plandex](../development_ops/plandex.md)
- [Mentat](../development_ops/mentat.md)
- [SWE-bench](../benchmarking/swe-bench.md)

## Sources / references
- [Official GitHub Repository](https://github.com/obra/superpowers)
- [Superpowers for Claude Code (Blog Post)](https://blog.fsck.com/2025/10/09/superpowers/)
- [Anthropic Agent Skills Specification](https://agentskills.io/)
- [awesome-skills.com](https://awesome-skills.com/)

## Contribution Metadata
- Last reviewed: 2026-10-01
- Confidence: high
