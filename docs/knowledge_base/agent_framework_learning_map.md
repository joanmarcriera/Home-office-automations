# Agent Framework Learning Map

## What it is

The Agent Framework Learning Map is a structured, production-tested architectural guide designed to help software engineers, systems architects, and machine learning practitioners navigate the rapidly evolving ecosystem of artificial intelligence agent frameworks. It categorizes open-source and enterprise tools into stateful runtimes, lightweight SDKs, role-based orchestration platforms, autonomous coding harnesses, and specialized task agents to provide an uncompromised path from conceptual prototyping to hardened production deployment in late 2026 and early 2027.

```
+--------------------------------------------------------------------------------------------------+
|                            Enterprise Agent Orchestration Topology                              |
+--------------------------------------------------------------------------------------------------+
|                                    User & API Ingress Layer                                      |
|                [Frontier Clients] <----> [FastMCP 3.1 Reverse Proxy Gateway]                    |
+-------------------------------------------------+------------------------------------------------+
                                                  |
                                                  v
+--------------------------------------------------------------------------------------------------+
|                                 Orchestration & Decision Layer                                  |
|  +-----------------------------+  +-----------------------------+  +--------------------------+  |
|  | Stateful Graph Runtimes     |  | Role-Based Multi-Agent      |  | Lightweight Task SDKs    |  |
|  | (LangGraph Checkpointing)   |  | (CrewAI Team Coordination)  |  | (OpenAI Agents SDK)      |  |
|  +--------------+--------------+  +--------------+--------------+  +------------+-------------+  |
|                 |                                |                              |                |
|                 +--------------------------------+------------------------------+                |
|                                                  |                                               |
|                                                  v                                               |
|  +--------------------------------------------------------------------------------------------+  |
|  | Distributed Agent Bus (Redis Streams / Celery / Event Broker Pub-Sub)                      |  |
|  +-----------------------------------------------+--------------------------------------------+  |
+--------------------------------------------------|-----------------------------------------------+
                                                   |
                                                   v
+--------------------------------------------------------------------------------------------------+
|                                Autonomous Execution Workers & Harnesses                          |
|  +-------------------------------------+  +---------------------------------------------------+  |
|  | Code Sandboxes (OpenHands / Aider)  |  | Web Automation & Extraction (Browser Use / MultiOn)|  |
|  | [gVisor MicroVMs / Docker Rootless] |  | [Headless Chromium / FastMCP Browser Bridge]      |  |
|  +-------------------------------------+  +---------------------------------------------------+  |
+--------------------------------------------------|-----------------------------------------------+
                                                   |
                                                   v
+--------------------------------------------------------------------------------------------------+
|                                 Persistent State & Context Storage                               |
|        [PostgreSQL / pgvector] <---> [Redis Checkpoints] <---> [Letta Core & Archival Memory]    |
+--------------------------------------------------------------------------------------------------+
```

## What problem it solves

The explosion of agentic tooling has created an acute "choice overload" dilemma across engineering teams. Framework authors routinely position their projects as general-purpose, all-in-one platforms, masking fundamental trade-offs between execution durability, recovery ergonomics, state-machine determinism, and latency overhead.

This map systematically untangles that complexity. It delineates between tools built for open-ended creative exploration versus high-reliability enterprise production loops. It prevents "framework fatigue" and costly architectural rewrites by prescribing clear, criteria-driven selection pathways based on state durability requirements, sub-agent delegation topology, sandboxed runtime boundaries, and protocol standardization (such as FastMCP 3.1 and OpenAI Agents Protocol).

```mermaid
flowchart TD
    Start([Evaluate Agent Project Requirements]) --> Q1{Need Durable Checkpoints & Cycles?}
    Q1 -- Yes --> LangGraph[LangGraph / Stateful Graph Runtime]
    Q1 -- No --> Q2{Need Role-Based Multi-Agent Teams?}

    Q2 -- Yes --> CrewAI[CrewAI / Role-Based Teams]
    Q2 -- No --> Q3{Autonomous Coding & Repository Edits?}

    Q3 -- Yes --> Q3_1{Terminal & Sandboxed Filesystem?}
    Q3_1 -- Container Sandbox --> OpenHands[OpenHands / Docker Harness]
    Q3_1 -- Local Interactive CLI --> Aider[Aider Pair Programmer]
    Q3_1 -- Personal Daemon OS --> OpenClaw[OpenClaw Agent OS]

    Q3 -- No --> Q4{Browser Interaction or Deep Research?}
    Q4 -- Web UI Automation --> BrowserUse[Browser Use / Playwright Engine]
    Q4 -- Deep Research & Synthesis --> GPTResearch[GPT Researcher / DeerFlow]
    Q4 -- Minimalist Tool Handoffs --> OpenAISDK[OpenAI Agents SDK / Minimalist SDKs]
```

## Where it fits in the stack

**Category**: Knowledge Base / Learning Path & Architectural Meta-Framework. It operates in the **strategic architectural decision tier**, establishing the foundational topology upon which individual frameworks—such as [LangGraph](../tools/frameworks/langgraph.md), [CrewAI](../tools/frameworks/crewai.md), [OpenAI Agents SDK](../tools/frameworks/openai-agents-sdk.md), or [AutoGen](../tools/frameworks/autogen.md)—are selected, deployed, and interconnected with underlying foundation models and Model Context Protocol servers.

## Agent Execution State Lifecycle & Checkpoint Machine

Enterprise production agents require formal mathematical guarantees regarding state transitions, checkpoint commits, and human intervention points. The diagram below illustrates the state machine lifecycle enforced by production-grade engines:

```mermaid
stateDiagram-v2
    [*] --> Initialized: Ingest User Goal & System Payload
    Initialized --> Planning: Parse Context & Schema Validation
    Planning --> Evaluating: Generate Execution DAG

    state Evaluating {
        [*] --> ToolInspection
        ToolInspection --> GuardrailCheck: Verify Permissions & Parameters
        GuardrailCheck --> ExecutionPending: Passes Safety Policies
        GuardrailCheck --> Planning: Guardrail Violation (Self-Correction)
    }

    Evaluating --> Interrupted: Destructive Action Detected (HITL required)
    Interrupted --> Evaluating: Operator Approves Tool Payload
    Interrupted --> Aborted: Operator Rejects / Timeout

    Evaluating --> Dispatched: Tool Payload Executed via FastMCP 3.1
    Dispatched --> Checkpointing: Record Output State to Durable DB
    Checkpointing --> Evaluating: More Steps Required
    Checkpointing --> Completed: Terminal Condition Satisfied

    Completed --> [*]: Emit Structured JSON Response
    Aborted --> [*]: Emit Audit Log & Rollback
```

## Framework Taxonomy & Comprehensive Feature Matrix

The following matrix compares dominant agent frameworks across late 2026 / early 2027 technical capabilities, including execution guarantees, memory persistence backends, and FastMCP 3.1 compatibility:

| Framework | Primary Paradigm | State Durability Engine | Sub-Agent Delegation | FastMCP 3.1 Native | Human-in-the-Loop Mechanism | Production Readiness | Target Workload Profile |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- | :--- |
| [LangGraph](../tools/frameworks/langgraph.md) | Stateful Cyclic Graph | Postgres / SQLite / Redis Checkpoints | Native Hierarchical Subgraphs | Native | First-Class Interrupt & Resume Nodes | Tier 1 (Mission Critical) | Complex workflows, multi-turn circular logic, financial/legal pipelines |
| [OpenAI Agents SDK](../tools/frameworks/openai-agents-sdk.md) | Minimalist Orchestrator | Ephemeral Session / KV Memory | Token-based Agent Handoffs | Native | Function Call Interception & Callbacks | Tier 1 (Mission Critical) | High-speed routing, customer support triage, micro-services |
| [CrewAI](../tools/frameworks/crewai.md) | Role-Based Crew System | SQLite / Memory Threads / ChromaDB | Hierarchical & Sequential Routing | Native | Manager Agent Interruption Hooks | Tier 2 (Enterprise Ready) | Content generation, collaborative research, marketing workflows |
| [AutoGen](../tools/frameworks/autogen.md) | Conversational Agents | Ephemeral Memory & Chat Logs | Dynamic Group Chat Managers | Community | User Proxy Interactive Agent | Tier 2 (Enterprise Ready) | Multi-persona simulations, conversational brainstorming |
| [OpenHands](../tools/development_ops/openhands.md) | Autonomous Software Eng | Git Commits & Docker Snapshots | Sub-Agent Task Delegation | Native | Interactive Web Terminal & Diff Approval | Tier 2 (Enterprise Ready) | Headless bug fixing, repository refactoring, automated PR generation |
| [OpenClaw](../tools/development_ops/openclaw.md) | Personal Agent Operating Sys | SQLite Local DB & Event Logs | Skill Workers & Background Daemons | Native | Mobile Notifications & CLI Prompts | Tier 3 (Emerging / SOTA) | Homelab automation, local system administration, daily scheduling |
| [Browser Use](../tools/automation_orchestration/browser-use.md) | Web Automation & Scraping | Chromium Contexts & Storage State | Parallel Tab Dispatchers | Native | Live Visual Debugger & Action Pause | Tier 2 (Enterprise Ready) | E-commerce purchasing, complex data extraction, web QA testing |
| [GPT Researcher](../tools/agents/gpt-researcher.md) | Autonomous Web Research | File Markdown & Report Buffers | Parallel Scraping Sub-Agents | Native | Outline & Report Section Sign-Off | Tier 2 (Enterprise Ready) | Market intelligence, literature reviews, comprehensive whitepapers |
| [Letta](../tools/agents/letta.md) | Memory-Centric Architecture | Core, Recall & Archival Vector DB | Memory-Attached Workers | Native | Live Context Editing UI & Ingest Hooks | Tier 2 (Enterprise Ready) | Long-horizon assistants, perpetual virtual companions, persona retention |
| [DeerFlow](../tools/agents/deerflow.md) | Sandboxed Research Harness | Tenant Isolation Filesystems | Sub-Harness Spawning Loops | Native | Step-by-Step Approval Protocol | Tier 3 (Emerging / SOTA) | Code security scanning, multi-stage paper reproduction |

## Operational Service Level Agreements (SLAs) & Runtime Parameters

When deploying agent frameworks into mission-critical production environments, organizations must adhere to strict operational boundaries to prevent runaway latency, API token depletion, and infinite re-planning cycles:

| Operational Dimension | Lightweight Routing (OpenAI SDK) | Stateful Graph Workflows (LangGraph) | Multi-Agent Collaborative Teams (CrewAI) | Autonomous Coding Harnesses (OpenHands) |
| :--- | :--- | :--- | :--- | :--- |
| **Max Turn Latency (p95)** | < 1,200 ms | < 4,500 ms per step | < 18,000 ms per delegation round | < 60,000 ms per build & test loop |
| **Hard Recursion Limit** | 5 handoffs | 25 iterations | 15 task delegations | 30 tool execution steps |
| **State Persistence SLA** | Ephemeral / In-Memory | RPO: 0 (Synchronous Write-Ahead DB) | Session-bounded SQLite write | Git Commit Tree / Container Snapshot |
| **FastMCP Tool Timeout** | 3.0 seconds | 10.0 seconds | 15.0 seconds | 120.0 seconds (Test execution) |
| **Sandboxing Standard** | Process-level isolation | Container namespace isolation | Python `virtualenv` / Docker | Rootless Docker / gVisor MicroVM |
| **Human Sign-Off Rule** | Optional | Enforced on DB writes / external API | Enforced on final draft emission | Enforced prior to `git push` |

## Production Deployment Topology: Multi-Agent Docker Compose Stack

Below is a complete, containerized production deployment setup illustrating how to orchestrate a distributed agent runtime cluster consisting of a FastMCP 3.1 gateway, a persistent state store (PostgreSQL + pgvector), an event message broker (Redis), and isolated execution sandboxes:

```yaml
version: "3.9"

services:
  agent-gateway:
    image: python:3.11-slim
    container_name: agent-runtime-gateway
    restart: unless-stopped
    working_dir: /app
    volumes:
      - ./agents:/app/agents:ro
      - ./config:/app/config:ro
    environment:
      - DATABASE_URL=postgresql://agent_admin:SecretDBPass2027@postgres-db:5432/agent_state
      - REDIS_URL=redis://redis-broker:6379/0
      - MCP_SERVER_HOST=0.0.0.0
      - MCP_SERVER_PORT=8080
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    command: >
      bash -c "pip install --no-cache-dir fastmcp pydantic langgraph psycopg2-binary redis &&
               python /app/agents/server.py"
    ports:
      - "8080:8080"
    depends_on:
      postgres-db:
        condition: service_healthy
      redis-broker:
        condition: service_healthy
    networks:
      - agent-internal-net

  postgres-db:
    image: pgvector/pgvector:pg16
    container_name: agent-postgres-db
    restart: unless-stopped
    environment:
      - POSTGRES_USER=agent_admin
      - POSTGRES_PASSWORD=SecretDBPass2027
      - POSTGRES_DB=agent_state
    volumes:
      - agent-db-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U agent_admin -d agent_state"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - agent-internal-net

  redis-broker:
    image: redis:7-alpine
    container_name: agent-redis-broker
    restart: unless-stopped
    command: ["redis-server", "--appendonly", "yes", "--requirepass", "RedisSecureStream2027"]
    volumes:
      - agent-redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "RedisSecureStream2027", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
    networks:
      - agent-internal-net

volumes:
  agent-db-data:
  agent-redis-data:

networks:
  agent-internal-net:
    driver: bridge
```

## Production Systemd Service Unit: Agent Runtime Gateway

For bare-metal and enterprise virtual machines requiring unmanaged, high-performance background execution, deploy the agent orchestration runtime via systemd:

```ini
[Unit]
Description=Enterprise Agent Framework Gateway & FastMCP 3.1 Runtime
After=network.target network-online.target postgresql.service redis.service
Wants=network-online.target

[Service]
Type=simple
User=agentops
Group=agentops
WorkingDirectory=/opt/agent-gateway
Environment="PATH=/opt/agent-gateway/venv/bin:/usr/local/bin:/usr/bin"
Environment="PYTHONUNBUFFERED=1"
Environment="DATABASE_URL=postgresql://agent_admin:SecretDBPass2027@localhost:5432/agent_state"
Environment="REDIS_URL=redis://:RedisSecureStream2027@localhost:6379/0"
Environment="MCP_PORT=8080"
ExecStart=/opt/agent-gateway/venv/bin/python -m uvicorn gateway.app:app --host 0.0.0.0 --port 8080 --workers 4
Restart=always
RestartSec=5s

# Security Hardening & Isolation
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/agent-gateway/var /opt/agent-gateway/logs
NoNewPrivileges=true
PrivateTmp=true
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

## Typical use cases

- **Architectural Triage & Selection**: Deciding with analytical precision whether a project requires a deterministic cyclic graph ([LangGraph](../tools/frameworks/langgraph.md)) or a role-playing conversational multi-agent structure ([AutoGen](../tools/frameworks/autogen.md)).
- **Skill Upgrading & Engineering Curriculum**: Navigating a validated progression from single-turn zero-shot prompts to long-horizon, autonomous self-healing agents driven by Claude 5.6, GPT-5.6, or Gemini 4.0 Ultra.
- **Homelab System Administration**: Deploying lightweight local orchestrators ([OpenClaw](../tools/development_ops/openclaw.md)) paired with local routing infrastructure ([LiteLLM](../services/litellm.md)) for sovereign home automation.
- **Enterprise Multi-Agent Prototyping**: Rapidly assembling specialized departmental teams ([CrewAI](../tools/frameworks/crewai.md)) with automated manager-level synthesis to demonstrate ROI to leadership.

## Strengths

- **Outcome-Driven Methodology**: Prioritizes operational reliability, state resilience, and recovery ergonomics over marketing claims.
- **Taxonomic Rigor**: Distinguishes between foundational runtime libraries (SDKs), workflow coordination graphs, sandboxed coding engines, and autonomous background operating systems.
- **Privacy & Local-First Architectural Compatibility**: Champions topologies compatible with local inference stacks ([vLLM](../infrastructure/vllm.md), [Ollama](../../services/ollama.md)) alongside commercial frontier APIs.
- **Protocol Standardization**: Built around standard Model Context Protocol (FastMCP 3.1) primitives, eliminating vendor lock-in across tool registries and agent servers.

## Limitations

- **Ecosystem Velocity**: Agent frameworks evolve with unprecedented rapidity; feature parity and best practices require regular recalibration.
- **Abstract Architectural Scope**: Focuses on holistic architectural patterns and structural blueprints rather than granular, line-by-line API tutorials for every tool.
- **Infrastructure Overhead**: Implementing resilient, production-grade stateful multi-agent systems introduces database, queue, and isolation container complexities beyond simple LLM inference.

## When to use it

- When initiating an agent-driven software project and establishing core architecture.
- When existing prototype implementations suffer from memory degradation, runaway tool loops, or state serialization crashes.
- When establishing engineering standards for multi-agent delegation, human-in-the-loop oversight, and tool security.

## When not to use it

- If building a simple, stateless single-turn chatbot or direct RAG pipeline that requires neither persistent state nor dynamic tool selection.
- If your organization has strictly standardized on a single proprietary closed ecosystem that prohibits multi-agent frameworks.

## Getting started

To adopt agent frameworks systematically:

1. **The Hello World of Agents**: Start by reading the [OpenAI Agents SDK](../tools/frameworks/openai-agents-sdk.md) documentation. It provides the cleanest abstraction for tool calling, handoffs, and session boundaries.
2. **Master the State**: Move to [LangGraph](../tools/frameworks/langgraph.md). Construct a deterministic circular loop (e.g., an automated generator that submits code to a static analysis auditor for approval or revision).
3. **Explore Multi-Agent Dynamics**: Deploy a [CrewAI](../tools/frameworks/crewai.md) team of three agents (Researcher, Synthesizer, Editor) to examine how specialized prompts and delegated task handoffs impact output quality.
4. **Autonomous Sandboxed Execution**: Install [Aider](../tools/development_ops/aider.md) or launch an [OpenHands](../tools/development_ops/openhands.md) container to explore how autonomous agents execute shell operations against live code repositories.

### Recommended Learning Order (Late 2026 / Early 2027 Update)

#### Fundamentals & Stateful Runtimes
1. [LangGraph](../tools/frameworks/langgraph.md) (paired with Claude 5.6 or GPT-5.6 for complex reasoning loops)
2. [OpenAI Agents SDK](../tools/frameworks/openai-agents-sdk.md) (paired with GPT-5.6 or Gemini 4.0 Ultra for rapid microservices)
3. [CrewAI](../tools/frameworks/crewai.md) (role-playing multi-agent collaboration)
4. [AutoGen](../tools/frameworks/autogen.md) (conversational multi-persona dynamics)

#### Autonomous Coding Harnesses
1. [OpenHands](../tools/development_ops/openhands.md) (sandboxed software engineering harness)
2. [Aider](../tools/development_ops/aider.md) (terminal-native pair programming engine)
3. [OpenClaw](../tools/development_ops/openclaw.md) (persistent personal agent operating system)

#### Specialized Task & Research Modules
1. [Browser Use](../tools/automation_orchestration/browser-use.md) (dynamic Chromium DOM automation)
2. [GPT Researcher](../tools/agents/gpt-researcher.md) (autonomous web research synthesis)
3. [Letta](../tools/agents/letta.md) (perpetual tiered memory architectures)
4. [DeerFlow](../tools/agents/deerflow.md) (academic paper and complex algorithmic coding harness)

## CLI examples

### Initializing a LangGraph Production Template
```bash
# Clone the LangGraph production starter
git clone https://github.com/langchain-ai/langgraph-starter.git
cd langgraph-starter
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### Launching an Isolated OpenHands Sandboxed Session
```bash
# Launch OpenHands inside an isolated rootless container
docker run -it \
    -e SANDBOX_USER_ID=$(id -u) \
    -e WORKSPACE_BASE=$PWD/workspace \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v $PWD/workspace:/opt/workspace \
    -p 3000:3000 \
    ghcr.io/all-hands-ai/openhands:0.15
```

## API examples

### Production FastMCP 3.1 Agent Framework Dispatch Server
Standardized FastMCP 3.1 server exposing strict Pydantic v2 schemas (`extra="forbid"`, `frozen=True`) to route incoming agent goals to the appropriate runtime engine:

```python
from typing import Dict, Any, Literal
from pydantic import BaseModel, Field, ConfigDict, ValidationError
from fastmcp import FastMCP

# Initialize FastMCP 3.1 framework router
mcp = FastMCP("agent-framework-router", version="3.1.0")

class FrameworkSelectionCriteria(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    requires_persistence: bool = Field(..., description="Whether workflow requires persistent state across restarts")
    cyclic_graph_needed: bool = Field(..., description="Whether workflow contains cyclic correction or re-planning loops")
    execution_type: Literal["code_editing", "web_automation", "multi_role_collaboration", "micro_triage"] = Field(
        ..., description="Primary workload category"
    )
    max_budget_usd: float = Field(default=5.0, ge=0.1, le=100.0, description="Cost threshold per task invocation")

class FrameworkRecommendation(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    recommended_framework: str = Field(..., description="Optimal framework identifier")
    architectural_tier: str = Field(..., description="Architectural classification")
    runtime_notes: str = Field(..., description="Operational guidance and safety constraints")
    suggested_models: list[str] = Field(..., description="Compatible frontier models")

@mcp.tool(name="evaluate_framework_choice", description="Evaluates workload criteria and prescribes the optimal agent framework")
def evaluate_framework_choice(criteria: FrameworkSelectionCriteria) -> FrameworkRecommendation:
    """Prescribes an optimal agent framework based on state, cyclicity, and workload demands."""
    if criteria.execution_type == "code_editing":
        return FrameworkRecommendation(
            recommended_framework="OpenHands / Aider",
            architectural_tier="Autonomous Coding Harness",
            runtime_notes="Execute inside non-root Docker container with restricted network egress. Enforce git commit checkpoints.",
            suggested_models=["Claude-5.6-Sonnet", "DeepSeek-V4", "GPT-5.6-Codex"]
        )
    elif criteria.execution_type == "web_automation":
        return FrameworkRecommendation(
            recommended_framework="Browser Use",
            architectural_tier="Browser Automation Engine",
            runtime_notes="Run headless Chromium with cookie persistence and visual DOM action bounding.",
            suggested_models=["Claude-5.6-Sonnet", "Gemini-4.0-Ultra"]
        )
    elif criteria.requires_persistence or criteria.cyclic_graph_needed:
        return FrameworkRecommendation(
            recommended_framework="LangGraph",
            architectural_tier="Stateful Cyclic Graph Runtime",
            runtime_notes="Configure PostgreSQL checkpointer and enforce max recursion limit (<= 25). Set explicit interrupt nodes for destructive actions.",
            suggested_models=["Claude-5.6-Opus", "GPT-5.6"]
        )
    elif criteria.execution_type == "multi_role_collaboration":
        return FrameworkRecommendation(
            recommended_framework="CrewAI",
            architectural_tier="Role-Based Collaborative Team",
            runtime_notes="Define discrete personas and bind manager agent for delegation. Restrict maximum task depth.",
            suggested_models=["Claude-5.6-Sonnet", "GPT-5.6", "Llama-4"]
        )
    else:
        return FrameworkRecommendation(
            recommended_framework="OpenAI Agents SDK",
            architectural_tier="Minimalist Orchestrator",
            runtime_notes="Utilize lightweight function handoffs with session memory bounds for sub-second execution.",
            suggested_models=["GPT-5.6-Turbo", "Claude-5.6-Haiku"]
        )

if __name__ == "__main__":
    mcp.run()
```

## Production Guardrails & Operational Security Guidelines

1. **Sandboxed Code Execution & Isolation**:
   - Software engineering agents ([OpenHands](../tools/development_ops/openhands.md), [DeerFlow](../tools/agents/deerflow.md), [Aider](../tools/development_ops/aider.md)) must always run inside non-root Docker containers or gVisor microVMs with restricted network egress to avoid accidental code injection or credential leakage.

2. **Recursion & Step Limits**:
   - Enforce hard execution step limits (`max_steps=20` or `recursion_limit=25`) in stateful graph engines ([LangGraph](../tools/frameworks/langgraph.md)) to prevent runaway LLM loops during recursive tool calls.

3. **Human-in-the-Loop Interruption**:
   - Require explicit human confirmation (`interrupt_before=["tool_execution"]`) prior to issuing destructive actions like database writes, monetary transactions, or outbound email dispatches.

## Troubleshooting & Framework Diagnostic Guide

| Diagnostic Symptom | Probable Cause | Diagnostic Command / Tool | Remediation Action |
| :--- | :--- | :--- | :--- |
| **Infinite Re-planning Loop** | Sub-agent state not updating completion flag correctly | Checkpoint inspector (`langgraph.get_state()`) | Ensure state node returns explicit status state key updates and verify condition termination edges. |
| **Deadlocked Group Chat** | Speaker selection logic unable to resolve next speaker in AutoGen | `autogen.GroupChatManager.debug_log` | Set explicit `speaker_selection_method="round_robin"` or implement deterministic selector functions. |
| **Out-of-Context Memory Leak** | Agent appending full uncompressed scratchpads to every turn | FastMCP context window monitor | Integrate [Letta](../tools/agents/letta.md) core memory pruning or chunk summarization prior to prompt generation. |
| **Tool Calling Schema Error** | MCP schema format mismatch between agent and server | `python -m mcp.cli validate` | Re-generate tool definitions using FastMCP 3.1 Pydantic v2 models with `extra="forbid"`. |
| **Session State Deserialization Crash** | Schema drift between saved database state and code models | `pydantic.ValidationError` inspector | Implement database migration scripts and strict version tagging on checkpoint states. |
| **Silent Worker Disconnection** | Broker connection pool timeout on long tool runs | `redis-cli ping` / TCP keepalive monitor | Increase client socket keepalive intervals and configure heartbeats on background workers. |
| **Browser DOM Selector Freeze** | Dynamic JavaScript hydration blocking Playwright DOM tree | `browser_use.dom.inspect_tree()` | Inject explicit wait conditions (`wait_for_selector`) and enable visual fallback bounding boxes. |
| **Sandboxed Container OOM** | Autonomous coding test runner consuming excessive memory | `docker stats --no-stream` | Increase container memory limits (`--memory=4g`) and configure swap thresholds. |

## Related tools / concepts

- [AI Tooling Landscape](ai_tooling_landscape.md)
- [AI Builder Index](ai_builder_index.md)
- [Agent Protocols](agent_protocols.md)
- [Agentic Workflows](patterns/agentic-workflows.md)
- [OpenClaw Workflow Prompts](patterns/openclaw-workflow-prompts.md)
- [Data Copilot Text-to-SQL Architecture](../architecture/data-copilot-text-to-sql.md)
- [Multi-Agent KnowledgeOps](../architecture/multi_agent_knowledgeops.md)
- [Flows](../architecture/flows.md)
- [Infrastructure](../architecture/infrastructure.md)
- [LiteLLM](../services/litellm.md)

## Sources / References

- [LangGraph documentation](https://langchain-ai.github.io/langgraph/)
- [OpenAI Agents SDK documentation](https://openai.github.io/openai-agents-python/)
- [CrewAI documentation](https://docs.crewai.com/)
- [AutoGen documentation](https://microsoft.github.io/autogen/)
- [OpenHands documentation](https://docs.openhands.dev/)
- [OpenClaw documentation](https://docs.openclaw.ai/)
- [Browser Use documentation](https://docs.browser-use.ai/)
- [GPT Researcher GitHub](https://github.com/assafelovic/gpt-researcher)
- [Letta documentation](https://docs.letta.com/)
- [DeerFlow GitHub](https://github.com/bytedance/deer-flow)
- [Model Context Protocol Specification v3.1](https://modelcontextprotocol.org/spec)

## Contribution Metadata

- Last reviewed: 2027-01-07
- Confidence: high
