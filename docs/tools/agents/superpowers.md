# Superpowers

## What it is
Superpowers is a comprehensive software development workflow and agentic skills framework designed for coding agents like [Claude Code](../development_ops/claude-code.md), [Cursor](../development_ops/cursor.md), and [Aider](../development_ops/aider.md). It builds on top of composable "skills" to enforce a rigorous engineering process.

## What problem it solves
It addresses the lack of discipline and engineering rigor in standard AI coding interactions by providing a structured, skills-based workflow for design, planning, and implementation. This prevents common failure modes like "hallucinating" file paths, circular refactoring, and code rot.

## Where it fits in the stack
**Agents / Workflow Framework**. It sits on top of coding agents to provide process-level guardrails and skills. It is often used in conjunction with the [Desktop Commander MCP](../development_ops/desktop-commander-mcp.md) for direct filesystem control.

## Typical use cases
- Enforcing TDD and plan-first development in agentic workflows
- Breaking down complex engineering tasks into verifiable sub-tasks
- Managing long-running autonomous coding sessions that span multiple files
- Maintaining code quality in large, complex repositories (e.g., those measured by [SWE-bench](../benchmarking/swe-bench.md))

## Strengths
- Enforces high-quality engineering standards (TDD, YAGNI, DRY)
- Increases agent autonomy and reliability through explicit verification steps
- Composable skills-based architecture that can be extended with project-specific logic
- Seamless integration with [Anthropic Agent Skills](anthropic-agent-skills.md)

## Limitations
- Higher process overhead for trivial tasks
- Requires an agent environment that supports the skills framework
- May require significant prompt tokens for complex planning cycles

## When to use it

- To enforce high-quality engineering standards (TDD, YAGNI, DRY) in agent-driven development.
- When you want agents to work autonomously for extended periods (hours) without deviating from a plan.
- For complex projects that require a systematic approach to design, planning, and implementation, as described in the [AI-Assisted Dev Workflow](../../playbooks/dev-workflow-ai-assisted.md).

## When not to use it

- For trivial code changes or simple questions.
- If you prefer an ad-hoc, conversational approach to coding without structured planning.

## Key Workflow Components

1.  **Brainstorming**: Socratic design refinement before writing code.
2.  **Isolated Workspaces**: Uses Git worktrees to ensure a clean baseline.
3.  **Bite-sized Planning**: Breaks work into 2-5 minute tasks with exact file paths and verification steps.
4.  **Subagent-Driven Development**: Dispatches fresh subagents per task with two-stage reviews.
5.  **Strict TDD**: Enforces RED-GREEN-REFACTOR cycle.
6.  **Formal Code Review**: Automated reviews against the plan before merging.

## Technical Implementation: Skill YAML Example

Superpowers skills are defined using a structured YAML format that specifies the tool's signature, implementation, and description for the LLM.

```yaml
# example_skill.yaml
name: "run_tests"
description: "Executes the test suite for the current project and returns results."
parameters:
  type: "object"
  properties:
    path:
      type: "string"
      description: "Path to the test directory or file."
    filter:
      type: "string"
      description: "Optional regex to filter tests."
implementation: |
  # The actual shell command or script to run
  pytest {{path}} -k {{filter}}
```

## Advanced Usage: Custom Task Verification

For complex refactors, you can define custom verification steps in your `superpowers.json` or `.claudestatus` files to ensure the agent doesn't just "complete" the task but actually fixes the underlying issue.

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

## Getting started

### Installation

Installation methods vary by platform:

#### Claude Code (via Plugin Marketplace)
```bash
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

#### Cursor
Install via the Cursor Agent plugin marketplace: `/plugin-add superpowers`.

#### Codex / OpenCode
Follow platform-specific instructions to fetch the skill files from the [official repository](https://github.com/obra/superpowers).

## Example company use cases
- **Product engineering**: enforce design-first planning and verification for every AI-generated pull request.
- **Agency delivery**: keep client repos consistent even when different agents or contractors are contributing.
- **Internal automation team**: standardize how agents propose, implement, verify, and hand off workflow changes.

## Example workflow
```text
Problem -> Brainstorming -> Written plan -> Implementation -> Verification -> Review -> Merge
```

## Ecosystem notes
- Superpowers sits inside the broader [Claude Skills Ecosystem](claude-skills-ecosystem.md) alongside Anthropic's reference [skills repository](https://github.com/anthropics/skills).
- It is often paired with other coding tools like [Mentat](../development_ops/mentat.md) or [Plandex](../development_ops/plandex.md) for specialized refactoring tasks.
- Community variants such as `ui-ux-pro-max-skill` are useful specialization examples, but they should be reviewed like code because they encode process, tools, and risk assumptions.

## Selection comments
- Superpowers is strongest when quality and repeatability matter more than raw speed.
- Use it by default for code that affects production systems, shared libraries, or client deliverables.
- Do not force it on trivial one-off edits where the process overhead outweighs the risk.

## Related tools / concepts
- [Claude Code](../development_ops/claude-code.md)
- [Anthropic Agent Skills](anthropic-agent-skills.md)
- [Claude Skills Ecosystem](claude-skills-ecosystem.md)
- [Desktop Commander MCP](../development_ops/desktop-commander-mcp.md)
- [Aider](../development_ops/aider.md)
- [Plandex](../development_ops/plandex.md)
- [SWE-bench](../benchmarking/swe-bench.md)

## Sources / References

- [Official GitHub Repository](https://github.com/obra/superpowers)
- [Superpowers for Claude Code (Blog Post)](https://blog.fsck.com/2025/10/09/superpowers/)
- [Anthropic Agent Skills Specification](https://agentskills.io/)
- [awesomeclaude.ai](https://awesomeclaude.ai/)
- [awesome-skills.com](https://awesome-skills.com/)
- [UI UX Pro Max Skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)

## Contribution Metadata
- Last reviewed: 2026-05-18
- Confidence: high
