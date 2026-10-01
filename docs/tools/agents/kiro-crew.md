# Kiro Crew

## What it is
**Kiro Crew** is an enterprise agent workforce orchestration platform and multi-agent development environment designed to coordinate teams of specialized AI agents across complex software engineering and operational workflows. As of early January 2027, Kiro Crew native runtimes fully implement the **FastMCP 3.1 Task Protocol** and support high-throughput model routing across frontier reasoning models including **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Gemma 4**, **DeepSeek-V4**, and **Qwen 3.6 VL**. It provides a structured framework for defining agent personas, role-based tool capabilities, shared contextual memory, and deterministic task delegation pipelines.

### Kiro Crew Multi-Agent Architecture
Kiro Crew uses a hierarchical supervisor-worker topology with isolated workspace worktrees, event-driven agent messaging, and integrated FastMCP 3.1 tool execution endpoints.

```
+-----------------------------------------------------------------------------------+
|                            KIRO CREW CONTROL PLANE                                |
|   +-------------------+    +--------------------+    +------------------------+   |
|   | Supervisor Agent  |    | Workspace Sync     |    | FastMCP 3.1 Server     |   |
|   | (Planning Engine) |    | (Git Worktrees)    |    | (Tool & State Proxy)   |   |
|   +---------+---------+    +---------+----------+    +-----------+------------+   |
+-------------|------------------------|---------------------------|----------------+
              | Delegated Tasks        | Workspace Locking         | Tool Calls
              v                        v                           v
+-----------------------------------------------------------------------------------+
|                            SPECIALIZED AGENT WORKERS                              |
|   +------------------+     +-------------------+     +------------------------+   |
|   | Architect Agent  |     | Developer Agent   |     | QA & Compliance Agent  |   |
|   | (Claude 5.6)     |     | (DeepSeek-V4)     |     | (Qwen 3.6 VL)          |   |
|   +--------+---------+     +---------+---------+     +-----------+------------+   |
+------------|-------------------------|---------------------------|----------------+
             | Code Design             | Implementation            | Verification
             +-------------------------+---------------------------+
                                       |
                                       v
                       +-------------------------------+
                       | Verified Git PR & Code Patch  |
                       +-------------------------------+
```

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
pip install kiro-crew fastmcp pydantic
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

# Export execution logs and telemetry trace
kiro-crew telemetry export --crew-id crew-8841 --format json > crew_trace.json
```

## API examples

### FastMCP 3.1 Crew Tool Server & Orchestration Engine
Below is a full Python integration demonstrating a **FastMCP 3.1** server providing multi-agent crew execution, status monitoring, and role-based tool delegation.

```python
import os
import json
from typing import List, Dict, Any, Optional
from fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator

# Initialize FastMCP Server
mcp = FastMCP("Kiro Crew Orchestrator", dependencies=["pydantic", "fastmcp"])

class AgentPersona(BaseModel):
    name: str = Field(..., description="Agent role name, e.g. Architect, Developer, Reviewer")
    model: str = Field("claude-5.6", description="Target model ID for agent persona")
    allowed_tools: List[str] = Field(default_factory=list, description="Permitted MCP tool IDs")

class CrewTaskConfig(BaseModel):
    task_id: str = Field(..., description="Unique task identifier")
    description: str = Field(..., min_length=10, description="Task goal description")
    assigned_role: str = Field(..., description="Target agent persona role")
    dependencies: List[str] = Field(default_factory=list, description="IDs of prerequisite tasks")

class CrewDefinition(BaseModel):
    crew_id: str = Field(..., description="Unique crew workspace identifier")
    agents: List[AgentPersona] = Field(..., min_items=1)
    tasks: List[CrewTaskConfig] = Field(..., min_items=1)

@mcp.tool()
def deploy_kiro_crew(crew_config: CrewDefinition) -> dict:
    """Deploys a multi-agent crew in isolated Git worktree sandboxes."""
    # Process crew startup logic
    return {
        "status": "deployed",
        "crew_id": crew_config.crew_id,
        "agents_active": len(crew_config.agents),
        "total_tasks": len(crew_config.tasks),
        "sandbox_path": f"/tmp/kiro_sandboxes/{crew_config.crew_id}"
    }

@mcp.tool()
def fetch_crew_telemetry(crew_id: str) -> dict:
    """Fetch real-time agent token usage and task completion metrics."""
    return {
        "crew_id": crew_id,
        "active_status": "running",
        "completed_tasks": 2,
        "pending_tasks": 1,
        "total_token_count": 42100,
        "cost_estimate_usd": 0.126
    }

if __name__ == "__main__":
    mcp.run()
```

### Multi-Agent Verification Schemas (Pydantic v2)
To guarantee payload safety across agentic workflows, complex crew outputs are verified using Pydantic v2:

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional
from datetime import datetime

class CodeReviewFeedback(BaseModel):
    reviewer_agent: str = Field(..., description="Name of QA or Reviewer agent")
    file_path: str = Field(..., description="Path to reviewed file")
    severity: str = Field(..., pattern=r"^(info|warning|critical)$")
    comment: str = Field(..., min_length=5)
    line_number: Optional[int] = Field(None, ge=1)

class AgentExecutionResult(BaseModel):
    task_id: str = Field(..., description="Task UUID")
    agent_name: str = Field(..., description="Executing agent role")
    status: str = Field(..., pattern=r"^(completed|failed|halted)$")
    artifacts_created: List[str] = Field(default_factory=list)
    review_comments: List[CodeReviewFeedback] = Field(default_factory=list)
    execution_time_seconds: float = Field(..., ge=0.0)

    @model_validator(mode="after")
    def check_failure_artifacts(self) -> "AgentExecutionResult":
        if self.status == "failed" and self.artifacts_created:
            raise ValueError("Failed agent execution cannot return valid artifacts.")
        return self

# Example execution validation
sample_result = {
    "task_id": "task-402",
    "agent_name": "Developer Agent",
    "status": "completed",
    "artifacts_created": ["src/auth/jwt.py", "tests/test_jwt.py"],
    "review_comments": [
        {
            "reviewer_agent": "Security QA Agent",
            "file_path": "src/auth/jwt.py",
            "severity": "warning",
            "comment": "Ensure secret key expiration is configured via environment variable.",
            "line_number": 24
        }
    ],
    "execution_time_seconds": 12.4
}

validated_output = AgentExecutionResult.model_validate(sample_result)
print("Validated Agent Result:", validated_output.model_dump_json(indent=2))
```

## Performance & Feature Benchmark Matrix

| Feature / Metric | Kiro Crew | CrewAI | Agency Swarm | LangGraph |
| :--- | :--- | :--- | :--- | :--- |
| **Topology** | Hierarchical / Supervisor | Sequential & Hierarchical | Swarm / Directed Graph | Arbitrary Stateful Graph |
| **FastMCP 3.1 Support** | Native First-Class | Extension Adapter | Custom Wrapper | MCP Agent Nodes |
| **Workspace Isolation**| Native Git Worktrees | Directory Sandboxing | None | Virtual File System |
| **Model Heterogeneity**| Multi-Model Dynamic Routing | Multi-Model Support | OpenAI Focused | Any LLM Model |
| **State Persistence** | SQLite / Redis Sync | In-Memory / ChromaDB | Local JSON File | Postgres / Redis Checkpointer |
| **Target Scale** | Enterprise Codebases | Lightweight Agent Teams | Conversational Swarms | Production Workflows |

## Operational & Troubleshooting Guide

### 1. Concurrent Git Worktree Lock Conflicts
- **Symptom**: Agent worker throws `Git Worktree Locked` exception during task initialization.
- **Cause**: A previously crashed agent process left a stale index lock file `.git/worktrees/<agent>/index.lock`.
- **Resolution**:
  Execute lock cleanup command before launching the crew:
  ```bash
  kiro-crew workspace unlock --crew-id crew-auth-dev --force
  ```

### 2. Context Window Exhaustion in Long Multi-Turn Handoffs
- **Symptom**: Developer Agent truncates code patches or loses track of initial architectural requirements.
- **Cause**: Shared context buffer accumulated raw chat messages without summarization across multiple agent handoffs.
- **Resolution**: Enable state compression in `crew.yaml`:
  ```yaml
  context_management:
    compression_strategy: "summarize_on_handoff"
    max_context_tokens: 32000
  ```

### 3. FastMCP 3.1 Tool Timeout During Integration Tests
- **Symptom**: QA Agent times out when triggering automated test runner tools.
- **Cause**: Test suite execution exceeded default FastMCP response timeout (30s).
- **Resolution**: Adjust `mcp_tool_timeout` setting in agent tool configuration:
  ```python
  mcp_config = {
      "timeout_seconds": 120,
      "retry_attempts": 3
  }
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
- [FastMCP 3.1 Specification](https://github.com/jina-ai/fastmcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
