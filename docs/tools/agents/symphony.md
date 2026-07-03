# Symphony

## What it is
Symphony is an autonomous implementation framework by OpenAI (July 2026) that turns project work into isolated, autonomous implementation runs. It manages high-level work items (issues) by coordinating a fleet of coding agents that handle the end-to-end implementation lifecycle using the **MCP 3.0 Task Protocol**.

## What problem it solves
It solves the "supervision bottleneck" in agentic software engineering by shifting the human role from direct code-level supervision to high-level work item management. By utilizing the **MCP 3.0 Task Protocol** for standardized multi-agent coordination, Symphony enables a "software factory" model where agents operate with high autonomy and verifiable output.

## Where it fits in the stack
**Agents / Orchestration Framework**. It manages the lifecycle of implementation runs, interfacing between task trackers (e.g., Linear, Jira) and version control systems (GitHub, GitLab), while using [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) for tool and task standardization.

## Typical use cases
- **Multi-Agent Coordination**: Using the **MCP 3.0 Task Protocol** to distribute complex implementation tasks across specialized agents.
- **Issue-to-PR Automation**: Automating the transition from a descriptive issue to a verified Pull Request.
- **Fleet Management**: Managing dozens of agents working in parallel on isolated features, bug fixes, or documentation updates.
- **Continuous Implementation**: Integrating autonomous coding agents into the CI/CD pipeline to handle routine maintenance tasks.

## Strengths
- **MCP 3.0 Task Protocol**: Leverages standardized task representations for seamless coordination between diverse agent types.
- **Autonomous Implementation Runs**: Spawns agents to handle tasks from a work board without constant human prompting.
- **Proof of Work**: Enforces standardized verification (CI status, walkthrough videos, PR review feedback).
- **Safe Landing**: Built-in mechanisms for safely merging PRs once automated and manual checks pass.

## Limitations
- **Harness Dependency**: Requires robust testing environments and CI to ensure agentic changes don't introduce regressions.
- **Experimental State**: Many implementations are still in the reference stage (e.g., the Elixir-based reference implementation).
- **Context Management**: Can be token-intensive when processing large repositories or complex specifications.

## When to use it
- When you want to move from micro-managing coding agents (like [Aider](../development_ops/aider.md)) to managing high-level work items.
- In mature codebases that have already adopted [Software Factories](../../knowledge_base/patterns/software-factories.md) principles.
- When you need to scale engineering capacity using [GPT-5.5](../ai_knowledge/chatgpt.md) or [Claude 4.8](../ai_knowledge/claude.md) agents.

## When not to use it
- In small projects where manual agent supervision is not a bottleneck.
- In environments where comprehensive testing and CI are not yet established.
- When working on legacy systems that lack automated test suites.

## Getting started

### Requirements
- A codebase with established CI and testing harnesses.
- API access to a frontier model (Claude 4.8 Opus or GPT-5.5).
- An MCP 3.0 compatible environment for task coordination.

### Installation
Clone the official repository to explore the reference implementation:
```bash
git clone https://github.com/openai/symphony.git
cd symphony
```
For the Elixir reference implementation:
```bash
cd elixir
mix deps.get
mix compile
```

### Basic Implementation Run
```bash
# Configure the symphony environment
export SYMPHONY_MODEL=gpt-5.5-preview
export SYMPHONY_MCP_ENDPOINT=http://localhost:8000/task-protocol

# Start an implementation run for a specific issue
symphony run --issue BUG-404 --verify-with-ci
```

## CLI examples
```bash
# Start the symphony service with a specific workflow file
symphony start --workflow ./WORKFLOW.md

# Check the status of active implementation runs across the fleet
symphony status --detailed

# Manually trigger the MCP 3.0 Task Protocol handshake
symphony mcp handshake
```

## API examples
Symphony provides an HTTP API for monitoring and management (typically at `/api/v1/state`):

```json
{
  "state": "active",
  "mcp_version": "3.0",
  "active_runs": [
    {
      "issue_id": "FEAT-202",
      "agent_type": "claude-4-8-opus",
      "task_protocol_status": "in_progress",
      "ci_status": "passing"
    }
  ]
}
```

## Related tools / concepts
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Software Factories](../../knowledge_base/patterns/software-factories.md)
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
- [MCP 3.0 Task Protocol Documentation](https://modelcontextprotocol.io/spec/task-protocol)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
