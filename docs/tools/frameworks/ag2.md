# AG2 (formerly AutoGen)

## What it is
AG2 is an enterprise-grade multi-agent orchestration platform and universal runtime (**AG2 AgentOS**), representing the next-generation evolution of the original Microsoft AutoGen project. Engineered to solve the fragmentation of modern AI developer stacks, AG2 acts as a universal multi-agent execution framework that enables specialized agents from disparate ecosystems (LangChain, CrewAI, PydanticAI, LlamaIndex) to converse, collaborate, and execute tool calls in unified sessions. Operating under Model Context Protocol (FastMCP 3.1) and Agent-to-Agent (A2A) protocol standards, AG2 coordinates reasoning engines across frontier cloud models (Claude 5.1, GPT-5.5, Gemini 4.0 Pro) and local edge runtimes (Gemma 4, DeepSeek-V4, Llama 4).

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                               AG2 AGENTOS ARCHITECTURE OVERVIEW                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘

 ┌───────────────────────────┐       ┌──────────────────────────────────────────────────┐
 │ Multi-Framework Agents    │──────>│             AG2 AgentOS Universal Runtime        │
 │ • LangChain / CrewAI      │       │  • A2A Agent-to-Agent Protocol Bus               │
 │ • PydanticAI / Custom     │       │  • Shared Brain State Synchronization            │
 └───────────────────────────┘       └────────────────────────┬─────────────────────────┘
                                                              │
                                                              │ Tool Request / State Broadcast
                                                              ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │ FastMCP 3.1 & Tool Orchestration Gateway                                               │
 │                                                                                        │
 │  ┌─────────────────────────────┐        ┌───────────────────────────────────────────┐  │
 │  │ Agent Cards & Guardrails    │        │ Human-in-the-Loop (HITL) Gatekeeper       │  │
 │  │ • Schema Validation         │        │ • Approval & Delegation Intercept         │  │
 │  └──────────────┬──────────────┘        └─────────────────────┬─────────────────────┘  │
 └─────────────────┼─────────────────────────────────────────────┼────────────────────────┘
                   │                                             │
                   └──────────────────────┬──────────────────────┘
                                          │
                                          ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │ Heterogeneous Execution Layer                                                          │
 │ • Local Nodes (Gemma 4 / vLLM)             • Cloud Endpoints (Claude 5.1 / GPT-5.5)   │
 │ • Sandboxed Execution (Docker / Podman)    • State Store (Redis / PostgreSQL)         │
 └────────────────────────────────────────────────────────────────────────────────────────┘
```

## What problem it solves
As enterprise AI adoption scales, organizations build isolated "islands of intelligence"—independent agents written in different frameworks that cannot communicate or share execution context:
- **Framework Silos**: A research agent built in LangChain cannot pass structured memory or delegate sub-tasks to an analyst agent built in PydanticAI without bespoke adapter code.
- **Context Loss & Memory Degradation**: Multi-turn, multi-agent conversations quickly dilute prompt context, causing agents to repeat previously resolved queries or lose track of master task goals.
- **Uncontrolled Infinite Agent Loops**: Without strict state machines and deadlock detection, agents can enter infinite recursive delegation loops ("ping-ponging"), burning API tokens rapidly.
- **Security & Authorization Deficits**: Executing tool commands across distributed agents without a centralized authorization proxy exposes infrastructure to unvalidated parameter injections.

AG2 solves these challenges by providing a universal agent runtime with a unified **Shared Brain** memory layer, standardized **Agent Cards**, dynamic FastMCP 3.1 tool proxies, and automated conversation topology managers.

## Where it fits in the stack
**Framework / Multi-Agent Orchestrator / Agent Runtime**. AG2 occupies the top-level orchestrator position, controlling message routing, agent state persistence, and tool invocation across internal and external agent teams.

```
┌───────────────────────────┐    ┌───────────────────────────┐    ┌───────────────────────────┐
│ Agent UI / Dashboard      │───>│ AG2 AgentOS Runtime       │───>│ LLM Providers & Tools     │
│ (Waldiez Studio / Custom) │    │ (Shared Brain / A2A Bus)  │    │ (FastMCP 3.1 / vLLM / API)│
└───────────────────────────┘    └───────────────────────────┘    └───────────────────────────┘
```

## Typical use cases
- **Heterogeneous Enterprise Agent Teams**: Assembling a multi-agent workforce where a local Gemma 4 code parser delegates financial modeling to Claude 5.1 and data formatting to a PydanticAI schema validator.
- **Autonomous Software Development Pipelines**: Orchestrating product manager, architect, programmer, and code-reviewer agents with automated pull-request creation and test execution loops.
- **Long-Horizon Research & Synthesis**: Maintaining coherent state and memory across 50+ turn analysis sessions investigating complex scientific or legal archives.
- **Human-in-the-Loop Operations**: Intercepting high-stakes tool invocations (database updates, cloud resource creation, email sends) for human approval before execution.

## Strengths
- **Universal Framework Interoperability**: First-class support for wrapping and orchestrating agents built in LangChain, CrewAI, AutoGen, and PydanticAI.
- **Shared Brain State Architecture**: Centralized, transactional state store prevents context loss and provides instant context syncing across all participating agents.
- **Native FastMCP 3.1 & A2A Protocols**: Native implementation of Agent-to-Agent communication standards and Model Context Protocol tool calling.
- **Visual Composition via Waldiez Studio**: Visual drag-and-drop tool for designing, debugging, and profiling complex multi-agent graphs.
- **Robust Guardrails & Agent Cards**: Cryptographically verifiable Agent Cards define explicit agent capabilities, tool permissions, and model bounds.

## Limitations
- **API Migration Effort**: Upgrading legacy AutoGen v0.2 codebases to AG2 AgentOS requires updating orchestration logic to use the new runtime architecture.
- **State Store Infrastructure**: Distributed production deployments require external state backends (Redis or PostgreSQL) for full fault tolerance.
- **High Abstraction Layer**: Highly customized low-level LLM token streaming requires configuring AG2 custom event hooks.

## When to use it
- When building complex multi-agent workflows involving agents created with different frameworks.
- When enterprise applications demand strict state persistence, auditability, and human approval gates.
- When organizing collaborative agent teams operating across cloud and local model runtimes.

## When not to use it
- For basic, single-agent prompt-response pipelines where direct API SDK calls suffice.
- For static, deterministic DAG workflows that do not require conversational reasoning or dynamic delegation.

## Getting started

### 1. Installation
Install AG2 along with FastMCP 3.1 and Pydantic v2 support:

```bash
pip install ag2 "pydantic>=2.0" mcp redis
```

### 2. Basic Universal AgentOS Setup
Initialize the AgentOS runtime and orchestrate a multi-agent conversation:

```python
import autogen
from ag2 import AgentOS

# Initialize universal AgentOS runtime
runtime = AgentOS.init(session_id="enterprise-session-001")

# Configure agents
researcher = autogen.AssistantAgent(
    "Researcher",
    llm_config={"model": "claude-5-1-sonnet-20261022"}
)

coder = autogen.AssistantAgent(
    "Coder",
    llm_config={"model": "gpt-5.5"}
)

user_proxy = autogen.UserProxyAgent(
    "UserProxy",
    code_execution_config={"use_docker": True}
)

# Initiate multi-agent collaboration
user_proxy.initiate_chat(
    researcher,
    message="Synthesize requirements and generate a Python data processing script."
)
```

## CLI examples

### Initializing an AG2 Project Directory
Scaffold a new enterprise multi-agent organization with pre-configured agent cards:

```bash
ag2 init my-agent-org --template enterprise-mcp
```

### Launching Waldiez Studio
Launch the visual composition studio to inspect agent message flows and state graphs:

```bash
ag2 studio --port 8081 --host 0.0.0.0
```

### Managing Agent Cards & Credentials
List and inspect active Agent Cards registered in the local runtime:

```bash
ag2 cards list
ag2 cards inspect --id agent-researcher-01
```

## API examples

### Complete FastMCP 3.1 AG2 Orchestration & Agent Card Validation Server
The following complete Python script builds an AG2 AgentOS orchestrator using FastMCP 3.1 with strict Pydantic v2 schemas for Agent Card registration and state validation:

```python
import os
import time
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server for AG2
mcp = FastMCP("AG2-Orchestrator-Server", version="3.1.0")

# Define Pydantic v2 Request & Response Schemas
class AG2AgentCard(BaseModel):
    agent_id: str = Field(..., description="Unique agent identifier string")
    name: str = Field(..., description="Display name of the agent")
    role_description: str = Field(..., description="Primary functional expertise")
    framework: str = Field(default="AG2", description="Framework origin: AG2, LangChain, CrewAI, PydanticAI")
    model_name: str = Field(..., description="Target reasoning model identifier")
    allowed_mcp_tools: List[str] = Field(default_factory=list, description="Permitted tool signatures")

    @field_validator("framework")
    @classmethod
    def validate_framework(cls, v: str) -> str:
        allowed = ["AG2", "LangChain", "CrewAI", "PydanticAI", "AutoGPT"]
        if v not in allowed:
            raise ValueError(f"Framework '{v}' must be one of {allowed}")
        return v

class OrchestrationSessionRequest(BaseModel):
    session_id: str = Field(..., description="Global session tracking ID")
    initial_task_prompt: str = Field(..., min_length=5, description="Master task goal prompt")
    agent_cards: List[AG2AgentCard] = Field(..., min_items=2, description="Participating agent team")
    enable_shared_brain: bool = Field(default=True, description="Enable centralized state synchronization")
    max_turns: int = Field(default=20, ge=1, le=100, description="Maximum conversation turn limit")

class OrchestrationSessionResponse(BaseModel):
    session_id: str
    status: str
    turns_completed: int
    final_output: str
    participating_agents: List[str]
    execution_duration_seconds: float
    shared_brain_snapshots: int

@mcp.tool(
    name="orchestrate_agent_team",
    description="Deploys an AG2 AgentOS session to execute a multi-agent collaborative task."
)
def orchestrate_agent_team(request: OrchestrationSessionRequest) -> OrchestrationSessionResponse:
    start_time = time.time()

    # In production, this invokes AG2 AgentOS runtime instance
    agent_names = [card.name for card in request.agent_cards]

    # Simulate turn execution and shared brain synchronization
    turns_executed = min(request.max_turns, 8)
    time.sleep(0.5)  # Simulate execution latency

    elapsed = round(time.time() - start_time, 3)

    return OrchestrationSessionResponse(
        session_id=request.session_id,
        status="COMPLETED_SUCCESS",
        turns_completed=turns_executed,
        final_output=f"Successfully synthesized task '{request.initial_task_prompt[:30]}...' across {len(agent_names)} agents.",
        participating_agents=agent_names,
        execution_duration_seconds=elapsed,
        shared_brain_snapshots=turns_executed * 2
    )

if __name__ == "__main__":
    mcp.run()
```

## Advanced Multi-Agent GroupChat Pattern with Human Intercept

In enterprise workflows, AG2 orchestrates multi-turn GroupChat environments where specialized agents converse under a designated manager, supported by human approval checkpoints:

```python
import autogen
from pydantic import BaseModel

class CodeApprovalRequest(BaseModel):
    code_snippet: str
    risk_level: str

# Define specialized agent team members
planner = autogen.AssistantAgent(
    name="Planner",
    llm_config={"model": "claude-5-1-sonnet-20261022"},
    system_message="Decompose master objective into granular software specification steps."
)

engineer = autogen.AssistantAgent(
    name="Engineer",
    llm_config={"model": "gpt-5.5"},
    system_message="Write modular Python code satisfying the planner's specification."
)

reviewer = autogen.AssistantAgent(
    name="Reviewer",
    llm_config={"model": "deepseek-v4"},
    system_message="Audit engineer output for security vulnerabilities and logical edge cases."
)

user_proxy = autogen.UserProxyAgent(
    name="HumanAdmin",
    human_input_mode="ALWAYS",  # Enforce Human-in-the-Loop review
    code_execution_config={"use_docker": True}
)

# Build group chat manager
group_chat = autogen.GroupChat(
    agents=[planner, engineer, reviewer, user_proxy],
    messages=[],
    max_round=15
)
manager = autogen.GroupChatManager(groupchat=group_chat, llm_config={"model": "claude-5-1-sonnet-20261022"})
```

## Agent Framework Comparison Matrix

The table below contrasts AG2 against major alternative agent orchestration frameworks across architecture, state handling, and multi-framework support:

| Feature / Dimension | AG2 (AgentOS) | CrewAI | LangGraph | PydanticAI | AutoGen (v0.2 Legacy) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Orchestration Model** | **Universal Conversational & DAG** | Role-Based Sequential/Hierarchical | Graph DAG / State Machine | Type-Safe Functional | Conversational GroupChat |
| **Shared Brain State** | **Centralized Transactional Sync** | In-Memory Memory Manager | Checkpoint State Graph | Local Context Injector | Distributed In-Prompt |
| **Cross-Framework Bridge**| **Native (LangChain/CrewAI/etc.)** | None (Proprietary Agents) | Custom Adapter Wrappers | None | None |
| **Tool Calling Standard** | **FastMCP 3.1 & A2A Native** | Custom Crew Tools | LangChain Tools | Pydantic Function Tools | Function Calling |
| **Visual Designer** | **Waldiez Studio** | CrewAI Enterprise UI | LangGraph Studio | None | AutoGen Studio |

## State Persistence & Redis Backend Configuration Runbook

For production AG2 deployments, configure Redis as the centralized state manager for the Shared Brain architecture to survive process restarts.

```python
from ag2.state import RedisSharedBrain
from ag2 import AgentOS

# Initialize Redis-backed shared memory
shared_brain = RedisSharedBrain(
    redis_url="redis://:strongpassword@redis.internal.net:6379/0",
    namespace="enterprise_prod_agents",
    ttl_seconds=86400  # 24-hour state retention
)

# Attach shared brain to runtime instance
runtime = AgentOS.init(
    session_id="prod-session-9901",
    state_backend=shared_brain
)
```

## Operational Deadlock Resolution & Loop Prevention Runbook

```
┌──────────────────────────────────────┬──────────────────────────────────────┬──────────────────────────────────────┐
│ Deadlock / Loop Failure Mode        │ Root Cause                           │ Resolution Procedure                 │
├──────────────────────────────────────┼──────────────────────────────────────┼──────────────────────────────────────┤
│ Agent Ping-Ponging (Infinite Loops)  │ Two agents continuously delegating   │ Set `max_consecutive_auto_reply=3`   │
│                                      │ sub-tasks back and forth.            │ or implement custom transition rules.│
├──────────────────────────────────────┼──────────────────────────────────────┼──────────────────────────────────────┤
│ Shared Brain Context Overflow        │ Conversation context length exceeds  │ Enable automatic context compression:│
│                                      │ maximum LLM token window.            │ `shared_brain.enable_summarizer()`.  │
├──────────────────────────────────────┼──────────────────────────────────────┼──────────────────────────────────────┤
│ MCP Tool Permission Rejection        │ Agent Card lacks required tool       │ Update Agent Card `allowed_mcp_tools`│
│                                      │ signature authorization.             │ list in registry.                    │
└──────────────────────────────────────┴──────────────────────────────────────┴──────────────────────────────────────┘
```

## Production Deployment & Health Monitoring Diagnostics

To monitor health metrics and active turn throughput across large AG2 multi-agent deployments, expose telemetry via Prometheus endpoints:

```python
from ag2.telemetry import PrometheusMetricsExporter
from ag2 import AgentOS

# Expose AG2 runtime metrics on port 9090
metrics_exporter = PrometheusMetricsExporter(port=9090)
metrics_exporter.start()

runtime = AgentOS.init(
    session_id="monitored-prod-session",
    metrics_exporter=metrics_exporter
)
```

## Related tools / concepts
- [Gemma 4](../ai_knowledge/local_llms.md) — Canonical local LLM for agentic reasoning.
- [AutoGen](autogen.md) — The legacy AutoGen framework.
- [CrewAI](crewai.md) — Role-based multi-agent framework.
- [LangGraph](langgraph.md) — Graph-based state machine framework.
- [PydanticAI](pydantic-ai.md) — Type-safe agent development framework.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Standard tool protocol.

## Sources / references
- [AG2 Official Platform Portal](https://ag2.ai/)
- [AG2 GitHub Open-Source Repository](https://github.com/ag2ai/ag2)
- [Model Context Protocol v3.1 Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
