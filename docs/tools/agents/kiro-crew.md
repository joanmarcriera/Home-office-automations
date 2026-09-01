# Kiro Crew

## What it is
**Kiro Crew** is an enterprise agent workforce orchestration platform and multi-agent development environment designed to coordinate teams of specialized AI agents across complex software engineering and operational workflows. As of early January 2027, Kiro Crew native runtimes fully implement the **FastMCP 3.1 Task Protocol** and support high-throughput model routing across frontier reasoning models including **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Gemma 4**, **DeepSeek-V4**, and **Qwen 3.6 VL**. It provides a structured framework for defining agent personas, role-based tool capabilities, shared contextual memory, and deterministic task delegation pipelines.

## What problem it solves
Managing multiple autonomous agents on complex codebases often leads to context drift, race conditions in workspace modifications, duplicate effort, and uncoordinated pull requests. Kiro Crew solves these challenges by providing a centralized agent coordinator and execution sandbox that enforces task boundaries, synchronized state management, automated code reviews between agent personas, and strict resource isolation.

## Where it fits in the stack
**Agent Orchestration and Execution Layer**. Kiro Crew operates above individual LLM foundation models and MCP tool servers, serving as the multi-agent control plane that schedules, monitors, and evaluates multi-agent task execution.

## Typical use cases
- **Autonomous Feature Delivery**: Orchestrating a crew consisting of a Product Manager Agent (specs), Software Architecture Agent (design), Coding Agent (implementation), and QA Agent (test generation & verification).
- **Large-Scale Repository Refactoring**: Dividing large monolith refactoring projects into discrete, non-overlapping tasks assigned to concurrent agent workers.
- **Continuous Documentation & Compliance Sync**: Deploying background agents that monitor code commits and automatically update documentation, OpenAPI specs, and security audit logs.
- **Incident Mitigation**: Running automated triage crews that collect telemetry, analyze log streams, run diagnostic commands, and propose hotfixes.

## Strengths
- **FastMCP 3.1 Task Protocol Support**: Native support for task decomposition, progress reporting, and tool execution across distributed MCP servers.
- **Git Workspace Isolation**: Automated worktree branch isolation prevents concurrent agents from overwriting uncommitted code modifications.
- **Flexible Model Routing**: Assigns different foundation models to different crew roles (e.g., DeepSeek-V4 for code synthesis, Claude 5.6 for architecture and planning).
- **Role-Based Tool Authorization**: Enforces strict permission boundaries on which tools and capabilities each agent persona can invoke.

## Limitations
- **Orchestration Overhead**: Managing multi-agent messaging and state synchronization adds slight latency compared to single-agent execution loops.
- **Configuration Complexity**: Defining multi-agent interactions, handoff triggers, and validation protocols requires careful upfront design.
- **Cluster Deployment Cost**: Running enterprise Kiro Crew execution workers requires Kubernetes or container orchestration infrastructure for full isolation.

## When to use it
- When software development tasks require distinct specialized roles (e.g., design, implementation, code review, test verification).
- When operating on large codebases where single-agent context windows are insufficient or prone to hallucination.
- When enterprise auditability and human-in-the-loop approvals are required prior to applying changes.

## When not to use it
- For simple, single-turn code generation or single-file edits (use [Claude Code](../development_ops/claude-code.md) or [Cline](cline.md) instead).
- When minimal execution latency is the critical metric and agent collaboration is unneeded.

## Getting started

### Installation
Install the Kiro Crew CLI and orchestration SDK:

```bash
pip install kiro-crew
```

### Initializing a Crew Workspace
Initialize a new Kiro Crew project configuration:

```bash
kiro-crew init my-dev-crew
cd my-dev-crew
```

## CLI examples

```bash
# Validate crew definition and agent tool permissions
kiro-crew validate --config crew.yaml

# Run a multi-agent coding task across the repository
kiro-crew run --task "Implement OAuth2 PKCE login flow with unit tests" --config crew.yaml

# Inspect real-time execution status and agent telemetry
kiro-crew status --active
```

## API examples

### Multi-Agent Crew Definition with FastMCP 3.1 & Pydantic v2 Verification
This example demonstrates defining a multi-agent crew with FastMCP 3.1 protocol compliance and validating agent task output using strict **Pydantic v2** models:

```python
from typing import List, Dict, Any
from pydantic import BaseModel, Field, ValidationError

# Define FastMCP 3.1 Task Schema
class CrewTask(BaseModel):
    task_id: str = Field(..., description="Unique task identifier")
    role: str = Field(..., description="Assigned agent role (e.g., Architect, Developer, Reviewer)")
    instructions: str = Field(..., description="Detailed instructions for the agent")
    assigned_model: str = Field(default="claude-5.6", description="Target LLM for this task")
    dependencies: List[str] = Field(default_factory=list, description="IDs of tasks that must complete first")

class CrewExecutionSummary(BaseModel):
    crew_id: str = Field(..., description="Identifier for the executed crew")
    status: str = Field(..., description="Overall execution status")
    completed_tasks: int = Field(..., ge=0)
    total_tokens_used: int = Field(..., ge=0)
    artifacts: List[str] = Field(default_factory=list)

def execute_kiro_crew(crew_id: str, tasks: List[CrewTask]) -> CrewExecutionSummary:
    # Simulated execution engine interacting with FastMCP 3.1 Task Protocol
    summary_data = {
        "crew_id": crew_id,
        "status": "completed",
        "completed_tasks": len(tasks),
        "total_tokens_used": 18450,
        "artifacts": ["src/auth/pkce.py", "tests/test_pkce.py"]
    }

    # Strict Pydantic v2 verification
    return CrewExecutionSummary.model_validate(summary_data)

if __name__ == "__main__":
    task1 = CrewTask(
        task_id="task-001",
        role="Architect",
        instructions="Design OpenAPI schema for OAuth2 PKCE endpoints",
        assigned_model="claude-5.6"
    )
    task2 = CrewTask(
        task_id="task-002",
        role="Developer",
        instructions="Implement PKCE code challenge verification in Python",
        assigned_model="deepseek-v4",
        dependencies=["task-001"]
    )

    try:
        result = execute_kiro_crew("crew-auth-dev", [task1, task2])
        print(f"Crew Execution Successful: {result.crew_id} - Status: {result.status}")
        print(f"Artifacts Generated: {', '.join(result.artifacts)}")
    except ValidationError as e:
        print(f"Validation error in crew execution response: {e}")
```

## Related tools / concepts
- [Agency Swarm](agency-swarm.md) — Collaborative multi-agent framework built on OpenAI Assistants API.
- [LangGraph](../frameworks/langgraph.md) — Stateful multi-agent graph orchestration framework.
- [AWS Dogwood](aws-dogwood.md) — Policy management and safety framework for agent tool calls.
- [Claude Code](../development_ops/claude-code.md) — Autonomous CLI coding agent.
- [Cline](cline.md) — Autonomous IDE coding assistant with MCP support.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Protocol for agent-tool connectivity.

## Sources / references
- [InfoQ: Kiro Crew Coding Agents Announcement](https://www.infoq.com/news/2026/08/kiro-crew-coding-agents/)
- [Kiro Crew GitHub Organization](https://github.com/kiro-crew)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
