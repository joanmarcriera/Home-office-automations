# Symphony

## What it is
Symphony is an enterprise-grade autonomous implementation framework open-sourced by OpenAI (updated early January 2027) designed to transform structured project requirements into fully isolated, self-verifying autonomous implementation runs. It automates high-level work items (such as Jira or Linear issues) by orchestrating a dynamic fleet of specialized coding agents executing under the standardized **FastMCP 3.1 Task Protocol**.

## What problem it solves
It solves the "supervision bottleneck" in agentic software engineering. Instead of humans micro-prompting coding models line-by-line, Symphony shifts the developer's role to high-level system specification and code-review approval. By combining the **FastMCP 3.1 Task Protocol** for standardized multi-agent coordination with rigorous validation loops, Symphony guarantees that agent-generated PRs are structurally sound, well-tested, and safe to land.

## Where it fits in the stack
[Layer 6: Agents & Orchestration](../../knowledge_base/ai_tooling_landscape.md#layer-6-agents-orchestration) — An autonomous, multi-agent lifecycle coordinator sitting between issue-tracking platforms (Linear, Jira) and version control hosts (GitHub, GitLab), standardizing execution via the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) ecosystem.

## Typical use cases
- **Multi-Agent Task Distribution**: Utilizing the **FastMCP 3.1 Task Protocol** to parcel out code-base refactoring, unit test generation, and documentation tasks across targeted agents.
- **Auto-Healing Bug Resolution**: Ingesting failing telemetry logs, auto-reproducing bugs in isolated sandboxes, and producing verified, CI-passing fixes.
- **Continuous Implementation Pipelines**: Injecting autonomous agents directly into CI/CD pipelines to handle routine technical debt, dependency updates, and boilerplate generation.
- **Compliance & PR Auditing**: Running automated validation audits on candidate pull requests against strict enterprise standards.

## Strengths
- **FastMCP 3.1 Task Protocol Alignment**: Native compatibility with early 2027 Task Protocol standards for seamless handshake, lifecycle state, and token routing across agent fleets.
- **Isolated Run Architectures**: Spawns isolated, self-contained runtimes (Docker, WASM, or micro-VMs) for agents to safely build and execute code.
- **Proof-of-Work Constraints**: Enforces mandatory verification steps (compilation gates, test coverage thresholds, lint checks) before submitting pull requests.
- **Multi-Model Support**: Dynamically routes specific tasks to specialized model variants (e.g., GPT-5.6 for architecture, Claude 5.6 for surgical code refinement, Gemini 4.0 Ultra for multimodal auditing).

## Limitations
- **Harness & CI Dependency**: Extremely dependent on pre-existing unit test suites and comprehensive coverage to prevent regressions.
- **Token Consuming**: Deep-research and multi-agent synthesis loops can become highly token-intensive.
- **Evolving Standard**: The FastMCP 3.1 Task Protocol and associated server-side libraries are iterating rapidly, requiring frequent runtime updates.

## When to use it
- When implementing a fully automated [Software Factories](../../knowledge_base/patterns/software-factories.md) model within mature codebases.
- For managing and orchestrating parallel task executions using high-capability models like [GPT-5.6](../ai_knowledge/chatgpt.md) or [Claude 5.6](../providers/anthropic.md).
- When a codebase already has rigorous automated test suites and robust containerized staging environments.

## When not to use it
- In early-stage, fast-moving prototypes lacking comprehensive unit testing or automated CI.
- For simple interactive tasks where single-agent CLI assistants (such as [Aider](../development_ops/aider.md)) are faster and easier to deploy.

## Getting started

### Requirements
- Containerized or isolated execution environment (Docker or WASM sandbox).
- High-coverage CI test runner.
- Valid API keys for GPT-5.6, Claude 5.6, or Gemini 4.0 Ultra.
- A FastMCP 3.1-compliant environment for agent-to-tool handshakes.

### Installation
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
Configure your environment to point to a FastMCP 3.1 Task Protocol endpoint and trigger an autonomous implementation run:
```bash
export SYMPHONY_MODEL=gpt-5.6
export SYMPHONY_MCP_ENDPOINT=http://localhost:8000/v1/task-protocol

# Start an implementation run for a designated issue
symphony run --issue BUG-904 --verify-with-ci
```

## CLI examples
```bash
# Initialize a workspace with standard workflow specifications
symphony start --workflow ./WORKFLOW.md

# List and audit running implementation sessions across the fleet
symphony status --detailed

# Trigger a manual handshake to inspect FastMCP 3.1 Task Protocol capability matrices
symphony mcp handshake --endpoint http://localhost:8080
```

## API examples

### Verifying a Symphony Implementation Run State using Pydantic v2
This Python script demonstrates how to interact with the Symphony REST API, deserialize the payload, and strictly validate the lifecycle and task states using Pydantic v2.

```python
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, conlist, field_validator
import requests

# 1. Define strict Pydantic v2 schemas for verification
class TaskMetric(BaseModel):
    mcp_protocol_version: str = Field("3.1", pattern=r"^3\.\d+$")
    agent_id: str = Field(..., min_length=3)
    tokens_consumed: int = Field(..., ge=0)
    execution_time_ms: float = Field(..., gt=0.0)

class RunStatus(BaseModel):
    issue_id: str = Field(..., pattern=r"^[A-Z]+-\d+$")
    status: Literal["pending", "in_progress", "verifying", "completed", "failed"]
    ci_passed: bool
    metrics: TaskMetric
    active_steps: List[str] = Field(default_factory=list)

    @field_validator("status")
    @classmethod
    def validate_ci_on_completion(cls, v: str, info) -> str:
        # Custom validation: if status is completed, CI must have passed
        if v == "completed" and not info.data.get("ci_passed", False):
            raise ValueError("Run cannot be marked completed if CI is failing.")
        return v

# 2. Query the Symphony local controller API and validate state
def audit_active_runs(endpoint: str) -> List[RunStatus]:
    try:
        response = requests.get(f"{endpoint}/api/v1/runs", timeout=10)
        response.raise_for_status()
        raw_runs = response.json()

        # Parse and validate list of active runs
        validated_runs = [RunStatus.model_validate(run) for run in raw_runs]
        return validated_runs
    except Exception as e:
        print(f"Audit verification failed: {e}")
        return []

if __name__ == "__main__":
    runs = audit_active_runs("http://localhost:2026")
    for run in runs:
        print(f"Verified Run {run.issue_id}: State={run.status}, CI={run.ci_passed}")
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
- [Symphony Specifications](https://github.com/openai/symphony/blob/main/SPEC.md)
- [OpenAI GitHub Repository](https://github.com/openai/symphony)
- [FastMCP 3.1 Task Protocol Specification](https://modelcontextprotocol.io/spec/task-protocol)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
