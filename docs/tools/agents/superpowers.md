# Superpowers

## What it is
Superpowers is a comprehensive software development workflow and agentic skills framework designed for coding agents like [Claude Code](../development_ops/claude-code.md), [Cursor](../development_ops/cursor.md), and [Aider](../development_ops/aider.md). In June 2026, it enforces a rigorous engineering process through composable skills, optimized for frontier models including Claude 4.8 and GPT-5.5.

## What problem it solves
It addresses the lack of discipline and engineering rigor in standard AI coding interactions by providing a structured, skills-based workflow for design, planning, and implementation. This prevents failure modes like hallucinating file paths and circular refactoring, ensuring high performance on complex engineering tasks.

## Where it fits in the stack
**Agents / Workflow Framework**. It sits on top of coding agents to provide process-level guardrails and skills, now featuring **MCP 3.0 Task Protocol** support for robust, verifiable task management.

## Typical use cases
- **Engineering Discipline**: Enforcing Test-Driven Development (TDD) and design-first planning in autonomous agentic workflows.
- **Complex Refactoring**: Breaking down large-scale codebase changes into verifiable sub-tasks with automated review gates.
- **Long-Horizon Autonomy**: Managing multi-hour coding sessions where the agent must maintain state and verify progress against a plan.
- **Visual Verification**: Using Gemini 3.5's visual reasoning capabilities within Superpowers to verify UI/UX changes and layout consistency.

## Strengths
- **Engineering Standards**: Strictly enforces high-quality standards like TDD, YAGNI, and DRY through automated checks.
- **MCP 3.0 Integration**: Native support for the Model Context Protocol (MCP 3.0) for seamless skill discovery and task orchestration.
- **High Autonomy**: Increases agent reliability by requiring explicit verification steps for every task completion.
- **Composable Architecture**: Skills can be easily extended or specialized for project-specific logic using YAML definitions.
- **Visual Reasoning**: Integrates with vision-capable models (e.g., Gemini 3.5) for multi-modal verification of frontend changes.

## Limitations
- **Process Overhead**: The rigorous workflow can be slower for trivial, single-line edits.
- **Tooling Requirements**: Requires an agent environment that supports the skills framework or MCP (e.g., Claude Code).
- **Token Consumption**: Complex planning cycles can consume significant tokens, requiring efficient context management.
- **Configuration Complexity**: Defining custom skill YAMLs and project-specific guardrails has a learning curve.

## When to use it
- To enforce high-quality engineering standards in production-grade, agent-driven development.
- When you want agents to work autonomously for extended periods without deviating from a baseline design.
- For complex projects requiring a systematic approach to design, planning, and implementation.
- When multi-modal verification (e.g., visual layout checks) is required as part of the CI/CD pipeline.

## When not to use it
- For trivial code changes, simple documentation fixes, or ad-hoc questions.
- If you prefer a purely conversational, "quick and dirty" approach to coding.
- In environments where agents lack the necessary terminal or filesystem permissions to execute skills.

## Getting started

### 1. Installation
Superpowers is typically installed as a plugin within a supported agent runtime like Claude Code.

```bash
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

### 2. Initializing a Plan
Start a new engineering session by providing a high-level goal. Superpowers will guide the brainstorming and planning phase.

```bash
superpowers plan "Refactor authentication to use JWT middleware"
```

### 3. Configuring Guardrails
Create a `superpowers.json` in your project root to enforce specific engineering standards.

```json
{
  "enforce_tdd": true,
  "required_reviewers": 1,
  "max_subtasks": 5
}
```

## CLI examples

```bash
# List all active Superpowers skills and their status
superpowers list --active

# Execute verification steps for the current sub-task
superpowers verify --task-id 123

# View the current engineering plan and progress
superpowers status --verbose
```

## API examples

### Defining a Custom Skill (YAML)
Skills are defined in YAML to specify parameters and shell-based implementation.

```yaml
# verify_ui_layout.yaml
name: "verify_layout"
description: "Uses visual reasoning to check if the UI matches the design spec."
parameters:
  type: "object"
  properties:
    screenshot_path:
      type: "string"
    model:
      type: "string"
      default: "gemini-3-5-flash-202606"
implementation: |
  # Internal logic to dispatch visual reasoning task
  python3 scripts/vision_check.py {{screenshot_path}} --model {{model}}
```

## Related tools / concepts
- [Claude Code](../development_ops/claude-code.md) — The primary runtime environment.
- [Cursor](../development_ops/cursor.md) — AI-native IDE with deep indexing.
- [Aider](../development_ops/aider.md) — Multi-file pair programmer.
- [Mentat](../development_ops/mentat.md) — Context-aware coding assistant.
- [Plandex](../development_ops/plandex.md) — Long-horizon planning engine.
- [Model Context Protocol](../../knowledge_base/agent_protocols.md) — Standards for agentic tools.
- [Agency Agents](agency-agents.md) — Specialized personas for agentic teams.
- [SWE-bench](../benchmarking/swe-bench.md) — Benchmarking autonomous engineering.
- [FastMCP](../../knowledge_base/agent_protocols.md) — High-performance MCP implementation.

## Sources / references
- [Official GitHub Repository](https://github.com/obra/superpowers)
- [Superpowers for Claude Code (Blog Post)](https://blog.fsck.com/2025/10/09/superpowers/)
- [Anthropic Agent Skills Specification](https://agentskills.io/)
- [Awesome Skills Marketplace](https://awesome-skills.com/)

## Contribution Metadata
- Last reviewed: 2026-06-28
- Confidence: high
