# Multi-Agent Systems

## What it is
Multi-Agent Systems (MAS) represent an architectural pattern and execution paradigm where multiple autonomous AI agents—each possessing distinct roles, tools, and context windows—collaborate, negotiate, and coordinate to solve complex, multi-step problems. As of early 2027, Multi-Agent Systems form the foundation of frontier autonomous software engineering, enterprise workflow automation, and distributed agentic task execution using protocols such as Model Context Protocol (MCP) and FastMCP 3.1.

## Architecture & Communication Topology

```
+-----------------------------------------------------------------------------------+
|                     Multi-Agent System (MAS) Orchestration Mesh                   |
|                                                                                   |
|   +--------------------------+       +----------------------------------------+   |
|   |  User Goal / Input       |       |  Isolated Worker Context Sandboxes     |   |
|   |  (GitHub PR / Spec)      |       |                                        |   |
|   +------------+-------------+       |   +--------------------------------+   |   |
|                |                     |   | Architect Agent                |   |   |
|                v                     |   | (Design / Spec Parser)         |   |   |
|   +--------------------------+       |   +---------------+----------------+   |   |
|   | Orchestrator / Planner   |<======|===================>                    |   |
|   | (Task Decomposition Engine)      |   +--------------------------------+   |   |
|   +------------+-------------+       |   | Developer Agent (Coder)        |   |   |
|                |                     |   | (FastMCP 3.1 Tools: FS/Git)    |   |   |
|                v                     |   +---------------+----------------+   |   |
|   +--------------------------+       |                   |                    |   |
|   | FastMCP 3.1 Event Bus /  |       |                   v                    |   |
|   | State Router             |       |   +--------------------------------+   |   |
|   +------------+-------------+       |   | Reviewer / Security QA Agent   |   |   |
|                |                     |   +--------------------------------+   |   |
|                v                     +----------------------------------------+   |
|   +---------------------------------------------------------------------------+   |
|   | Consolidated Output / Pull Request / Pydantic v2 Validated Artifact       |   |
|   +---------------------------------------------------------------------------+   |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Monolithic single-agent LLM executions suffer from severe constraints when confronted with enterprise-scale complexity:
- **Context Window Degeneration**: Monolithic prompts loaded with entire codebases, database schemas, and long interaction histories suffer from degraded instruction-following and attention saturation.
- **Role Pollution**: Expecting a single prompt to simultaneously act as a software architect, developer, security auditor, and QA tester leads to frequent hallucinations and missed edge cases.
- **Lack of Independent Verification**: Single agents cannot effectively evaluate their own outputs, leading to self-confirmation bias and unvalidated code generation.

Multi-Agent Systems solve these problems by enforcing strict role separation, isolated context spaces, and structured peer-review loops across specialized agent nodes.

## Topology & Collaboration Pattern Comparison

| Topology Pattern | Control Model | Latency Profile | Best Use Case | Risk / Drawbacks |
| :--- | :--- | :--- | :--- | :--- |
| **Hierarchical (Orchestrator-Worker)** | Centralized planner breaks down & routes tasks | Medium (2-4 turns) | Complex coding tasks, PR refactoring | Orchestrator single point of failure |
| **Peer-to-Peer Mesh (Swarm)** | Decentralized direct agent negotiation | High (Variable turns) | Autonomous red/blue security simulations | Infinite loop risk without turn limits |
| **Sequential Pipeline** | Deterministic output-to-input chain | Low-Medium (Fixed turns) | Data ingestion, transcription & extraction | Cascading errors if early step fails |

## Where it fits in the stack
**Category**: [Agents](../agents/index.md) / Architecture & Orchestration Pattern. Multi-Agent Systems sit between the high-level application orchestration layer and low-level LLM foundation models (such as Claude 5.1/5.6, GPT-5.5/5.6, and Gemini 4.0), organizing inter-agent message passing, task routing, and tool invocation.

## Typical use cases
- **Autonomous Software Development**: Teams of specialized agents (Architect, Coder, Tester, Reviewer) operating collaboratively on GitHub pull requests.
- **Complex Information Extraction & Synthesis**: Coordinating web scraping agents, document parsing agents, and schema validation agents for large-scale data ingestion pipelines.
- **Security & Vulnerability Auditing**: Red team attacker agents paired with blue team defender agents to automatically identify, exploit, and patch software vulnerabilities.
- **Enterprise Operations & Support**: Multi-department support agents routing queries across finance, IT, and legal domains with human-in-the-loop checkpoints.

## Strengths
- **Modular Design & Separation of Concerns**: Each agent operates with a focused prompt, specialized tools, and minimal necessary context.
- **Scalability**: New specialized agents can be integrated into the topology without refactoring the core reasoning logic of existing agents.
- **Built-in Quality Verification**: Multi-agent setups support automated peer review and validation before finalizing actions.

## Limitations
- **Increased Latency & Token Usage**: Multi-agent communication and intermediate feedback loops increase token costs and execution time.
- **Recursion & Infinite Loop Risks**: Unchecked agent interactions can result in circular reasoning or infinite tool invocation loops without strict execution limits.
- **Distributed State Synchronization**: Managing state, memory, and context coherence across multiple independent agents requires robust message routing.

## When to use it
- When tasks require distinct phases of planning, execution, and rigorous verification.
- When single-agent context windows become saturated or instruction-following deteriorates.
- When building enterprise autonomous coding or data analysis pipelines requiring specialized tool permissions.

## When not to use it
- For single-step or straightforward queries where a single prompt execution is faster and cheaper.
- For real-time, sub-second API endpoints where low latency is mandatory.

## Getting started

### 1. Conceptual Framework
A standard Multi-Agent System architecture consists of:
- **Orchestrator/Planner**: Breaks user input into atomic subtasks.
- **Worker Agents**: Specialized agents with specific tool access (e.g., File Editor, Terminal Executor).
- **Reviewer Agent**: Evaluates worker outputs against pre-defined quality criteria.

### 2. Multi-Agent Inter-Agent Communication
Agents exchange structured JSON payloads via standardization protocols like Model Context Protocol (MCP).

## CLI examples

### Inspect Multi-Agent Span Traces
```bash
# Query agent tracing spans for multi-agent workflows
openclaw trace list --workflow multi-agent-pipeline
```

### Execute Multi-Agent CLI Harness
```bash
# Run a multi-agent orchestration task using OpenSwarm
openswarm run --config agents.yaml --task "Refactor authentication module to Pydantic v2"
```

## API examples

### Pydantic v2 Task Delegation Engine
The following Python script utilizes **Pydantic v2** to define a structured multi-agent message routing and task delegation schema.

```python
from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Dict, Any
import json

class AgentTask(BaseModel):
    task_id: str = Field(..., description="Unique subtask identifier.")
    assigned_role: Literal["architect", "coder", "tester", "reviewer"] = Field(..., description="Target agent role.")
    instructions: str = Field(..., description="Specific instructions for the target agent.")
    context_payload: Dict[str, Any] = Field(default_factory=dict, description="Isolated context data.")

class AgentResponse(BaseModel):
    task_id: str = Field(..., description="Matching task identifier.")
    agent_role: str = Field(..., description="Role of the responding agent.")
    status: Literal["completed", "failed", "requires_review"] = Field(..., description="Execution status.")
    output: str = Field(..., description="Result or generated code/analysis.")
    next_action: Optional[AgentTask] = Field(None, description="Optional downstream task delegation.")

def dispatch_multi_agent_workflow(task: AgentTask) -> str:
    """Dispatches tasks across multi-agent topologies with validated schemas."""
    # Simulate worker execution
    response = AgentResponse(
        task_id=task.task_id,
        agent_role=task.assigned_role,
        status="completed",
        output=f"Executed task '{task.instructions}' successfully under role {task.assigned_role}.",
        next_action=AgentTask(
            task_id=f"{task.task_id}-review",
            assigned_role="reviewer",
            instructions="Verify generated implementation for compliance and correctness.",
            context_payload={"parent_task_id": task.task_id}
        )
    )
    return response.model_dump_json(indent=2)

if __name__ == "__main__":
    initial_task = AgentTask(
        task_id="task-101",
        assigned_role="coder",
        instructions="Implement JWT token validation function with FastMCP 3.1 support."
    )
    print(dispatch_multi_agent_workflow(initial_task))
```

### FastMCP 3.1 Multi-Agent Task Router Server
Expose a FastMCP 3.1 server to route task events and manage state pass-through across specialized agent nodes:

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

mcp = FastMCP("MultiAgentTaskRouter")

class DispatchRequest(BaseModel):
    workflow_id: str = Field(..., description="Unique workflow run ID")
    target_role: str = Field(..., description="Role of the target worker agent")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Context payload passed to worker")

class DispatchStatus(BaseModel):
    workflow_id: str = Field(..., description="Workflow ID")
    acknowledged: bool = Field(True, description="Receipt status")
    assigned_worker_id: str = Field(..., description="ID of worker container handling task")

@mcp.tool()
def route_agent_task(request: DispatchRequest) -> str:
    """Routes an agent task to a specialized worker node via FastMCP 3.1 task protocol."""
    status = DispatchStatus(
        workflow_id=request.workflow_id,
        acknowledged=True,
        assigned_worker_id=f"worker-{request.target_role}-01"
    )
    return status.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

## Operational Best Practices & Governance

1. **Strict Context Isolation**:
   - Never pass full conversation histories or full repository states between agents. Filter inputs to contain only the necessary sub-problem context.
2. **Infinite Loop & Recursion Guardrails**:
   - Set maximum recursion limits (`max_turns = 5`) on inter-agent communication channels to prevent looping agent-to-agent critique cycles.
3. **Audit Trails & Telemetry**:
   - Log all inter-agent messages and FastMCP tool invocations with trace correlation IDs to simplify debugging and security audits.

## Related tools / concepts
- [Agency Agents](agency-agents.md) — Multi-agent orchestrator for developer operations and task execution.
- [AutoGen](../frameworks/autogen.md) — Microsoft's multi-agent conversational framework.
- [LangGraph](../frameworks/langgraph.md) — State-machine graph framework for complex multi-agent workflows.
- [OpenSwarm](../development_ops/openswarm.md) — Multi-agent Claude CLI orchestrator.

## Sources / references
- [Multi-Agent System Architecture Standards](https://github.com/internal-ref/multi-agent-systems)
- [FastMCP 3.1 Protocol Specifications](https://modelcontextprotocol.io/)
- [TrueForge Claude Managed Agents Platform - The New Stack](https://thenewstack.io/truefoundry-trueforge-claude-managed-agents/)
- [Spline V2 MCP Agents - The New Stack](https://thenewstack.io/spline-v2-mcp-agents/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
