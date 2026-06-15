# Symphony

## What it is
Symphony is an autonomous implementation framework by OpenAI (June 2026) that turns project work into isolated, autonomous implementation runs. It allows engineering teams to manage high-level work items (issues) while coding agents handle the end-to-end implementation lifecycle.

## What problem it solves
It solves the "supervision bottleneck" in agentic software engineering by shifting the human role from direct code-level supervision to high-level work item management. By relying on "harness engineering" for verification, Symphony enables a "software factory" model where agents operate with high autonomy.

## Where it fits in the stack
**Agents / Orchestration Framework**. It manages the lifecycle of implementation runs, interfacing between task trackers (e.g., Linear, Jira) and version control systems (GitHub, GitLab).

## Typical use cases
- **Issue-to-PR Automation**: Automating the transition from a descriptive issue to a verified Pull Request.
- **Fleet Management**: Managing dozens of agents working in parallel on isolated features, bug fixes, or documentation updates.
- **Continuous Implementation**: Integrating autonomous coding agents into the CI/CD pipeline to handle routine maintenance tasks.

## Strengths
- **Autonomous Implementation Runs**: Spawns agents to handle tasks from a work board without constant human prompting.
- **Proof of Work**: Enforces standardized verification (CI status, walkthrough videos, PR review feedback).
- **Language-Agnostic Specification**: The [Symphony Spec](https://github.com/openai/symphony/blob/main/SPEC.md) allows for implementations in any language (Elixir, Python, TypeScript).
- **Safe Landing**: Built-in mechanisms for safely merging PRs once automated and manual checks pass.

## Limitations
- **Harness Dependency**: Requires robust "harness engineering" (comprehensive tests and CI) to ensure agentic changes don't introduce regressions.
- **Experimental State**: Many implementations are still in the reference stage (e.g., the Elixir-based reference implementation).
- **Context Management**: Can be token-intensive when processing large repositories or complex specifications.

## When to use it
- When you want to move from micro-managing coding agents (like [Aider](../development_ops/aider.md)) to managing high-level work items.
- In mature codebases that have already adopted rigorous testing and CI/CD practices.
- When you need to scale engineering capacity without linear hiring by utilizing [GPT-5.5](../ai_knowledge/chatgpt.md) or [Claude 4.8 Opus](../ai_knowledge/claude.md) agents.

## When not to use it
- In small projects where manual agent supervision is not a bottleneck.
- In environments where "harness engineering" (comprehensive testing and CI) is not yet established.
- When working on legacy systems that lack automated test suites.

## Getting started

### Requirements
- A codebase with established CI and testing harnesses.
- An environment capable of running the Symphony service (e.g., Elixir for the reference implementation).
- API access to a frontier model (Claude 4.8 Opus or GPT-5.5).

### Installation
Clone the official repository to explore the reference implementation:
```bash
git clone https://github.com/openai/symphony.git
cd symphony
```
For the Elixir implementation:
```bash
cd elixir
mix deps.get
mix compile
```

### Usage
Configure your `WORKFLOW.md` according to the Symphony specification and start the service to begin processing tasks.

## CLI examples
```bash
# Start the symphony service with a specific workflow file
symphony start --workflow ./WORKFLOW.md

# Run a one-off implementation run for a specific issue
symphony run --issue PROJ-101 --model gpt-5.5-preview

# Check the status of active implementation runs across the fleet
symphony status --detailed
```

## API examples
Symphony provides an HTTP API for monitoring and management (typically at `/api/v1/state`):

```json
{
  "state": "active",
  "counts": {
    "running": 5,
    "completed": 12,
    "retrying": 1
  },
  "active_runs": [
    {
      "issue_id": "FEAT-202",
      "agent_type": "claude-4-8-opus",
      "session_id": "run-8829",
      "ci_status": "passing"
    }
  ]
}
```

## Related tools / concepts
- [Harness Engineering](../../knowledge_base/patterns/harness-engineering.md)
- [LangGraph](../frameworks/langgraph.md)
- [Bee Agent Framework](bee-agent-framework.md)
- [Claude Skills Ecosystem](claude-skills-ecosystem.md)
- [Superpowers](superpowers.md)
- [OpenHands](../development_ops/openhands.md)
- [Devin](../development_ops/devin.md)
- [Cline](cline.md)

## Sources / references
- [Official GitHub Repository](https://github.com/openai/symphony)
- [Symphony Specification (SPEC.md)](https://github.com/openai/symphony/blob/main/SPEC.md)
- [Harness Engineering (OpenAI Blog)](https://openai.com/index/harness-engineering/)

## Contribution Metadata
- Last reviewed: 2026-06-15
- Confidence: high
