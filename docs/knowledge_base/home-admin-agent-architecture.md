# Home Admin Agent Architecture

## What it is
The Home Admin Agent is a stateful, LangChain- and LangGraph-based autonomous coordination system designed to orchestrate complex homelab pipelines, manage family knowledge graphs, and control local smart home environments. As of early January 2027, it acts as the centralized intelligent operating system ("brain") for the home, capable of multi-step reasoning, persistent memory tracking, and dynamic tool invocation using the FastMCP 3.1 Task Protocol.

## What problem it solves
Managing a multi-service smart home or homelab environment typically requires navigating disconnected interfaces and protocols (e.g., Home Assistant, Paperless-ngx, Vikunja, and CalDAV). The Home Admin Agent architecture solves this fragmentation by offering an intelligent, natural-language interface capable of cross-service reasoning and complex long-horizon planning—such as coordinating between document uploads, task creation, and calendar scheduling without manual human coordination.

## Where it fits in the stack
**Category**: Knowledge Base / System Architecture. It sits as the master **Orchestration Layer** of the homelab, positioned directly above individual infrastructure **Services** (such as [Home Assistant](../services/home-assistant.md), [Paperless-ngx](../services/paperless-ngx.md), and [Vikunja](../services/vikunja.md)) and below user-facing clients (chat interfaces, voice assistants, and dashboard UIs).

## Typical use cases
- **Proactive Maintenance & Self-Healing**: Real-time parsing of system logs and system resource levels (e.g., TrueNAS or K3s) to automatically restart docker containers or schedule physical drive replacements.
- **Family Administrative Ingestion**: Reading and extracting dates, items, and tasks from scanned receipts or school documents uploaded to Paperless-ngx, then synchronizing them with CalDAV calendars and Vikunja.
- **Context-Aware Smart Home Control**: Formulating and executing complex automation routines (e.g., adjusting climate and lighting) based on the combined context of weather reports, active tasks, and family calendars.
- **Unified Knowledge Retrieval**: Querying multiple heterogenous sources (e.g., Obsidian vaults, personal databases, and historical logs) via a single unified semantic search interface.

## Strengths
- **Stateful Long-Horizon Planning**: Uses advanced LangGraph-based Plan-and-Execute loops to construct, monitor, and adapt multi-step completion strategies dynamically.
- **Durable Memory & Checkpointing**: Persists complete execution traces, message histories, and plan states across system restarts using robust SQLite backend storage.
- **Dynamic Tool Discovery (FastMCP 3.1 Task Protocol)**: Leverages FastMCP 3.1 Task Protocol interfaces to dynamically bind, inspect, and execute remote and local tool definitions.
- **Hybrid Inference Execution**: Seamlessly routes tasks between lightweight local models (e.g., Gemma 4, DeepSeek-V4, or Qwen 3.6 VL) for low-latency operations and frontier APIs (such as Claude 5.6, GPT-5.6, or Gemini 4.0 Ultra) for complex reasoning.

## Limitations
- **Processing Latency**: Sequential model execution and multi-agent planning overhead introduce noticeable delay (often 3–15 seconds) compared to traditional rule-based scripts.
- **Resource Intensity**: Running the orchestrator and local vision/reasoning models requires significant local hardware resources (e.g., dedicated GPUs or high-performance ARM64 nodes).
- **Access Management Overhead**: Demands a highly secure and meticulously configured credentials store to prevent LLM hallucination-driven actions from altering critical home services.

## When to use it
- When managing multiple self-hosted services that require unified, contextual, or cross-domain orchestration.
- When building intelligent homelab systems that need to maintain state, learn user preferences over time, and handle loosely structured natural-language requests.
- When creating automated agents that require a strict plan-verify-replan loop for highly critical tasks.

## When not to use it
- For immediate, millisecond-critical smart home automations (such as turning on a hallway light via motion sensor)—use native, low-latency [Home Assistant](../services/home-assistant.md) automation instead.
- If the homelab runs on low-powered edge devices (e.g., single Raspberry Pi nodes) with no external internet connection and insufficient RAM to execute local model pipelines.

## Getting started

### Core Architecture Concepts
The Home Admin Agent is built as a stateful cyclic graph using **LangGraph**:

1.  **Planner**: An LLM-driven graph node that takes a high-level goal and generates a structured, step-by-step list of sub-tasks.
2.  **Executor**: A node that executes the first unresolved step in the plan by selecting and running the appropriate tool from the registry.
3.  **Re-planner**: Evaluates the results returned by tool execution and determines whether to mark the step as completed, modify the remaining plan, or output the final response.
4.  **State Management**: Tracks variables such as conversation histories, active plans, results, and custom session contexts inside a schema-validated state class.

### Memory & State Persistence
Durable session state is preserved using a SQLite checkpointer wrapper, allowing the agent to resume interrupted tasks and maintain multi-session context.

## CLI examples

Interacting with the Home Admin Agent environment via the administrative CLI:

```bash
# Initialize the persistent SQLite database for conversation state and memory checkpointing
ralph-admin init-db --db-path ./data/agent_memory.db

# Launch the LangGraph orchestration server with active FastMCP 3.1 server registration
ralph-admin start --port 8080 --config ./config/agent_config.yaml --enable-mcp

# Test a specific tool in isolation to verify credentials and response schemas
ralph-admin tool-run --tool "paperless_search" --arguments '{"query": "january 2027 water bill"}'
```

## API examples

### Base Home Tool Schema (Python & Pydantic v2)
This example demonstrates a robust, type-safe validation layout for managing agent orchestration state, execution traces, and tool results using **Pydantic v2** (`BaseModel`, `Field`, `model_validate`, `ValidationError`).

```python
import sys
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError

# Pydantic v2 state schemas to validate agent planning trajectories
class StateMessage(BaseModel):
    role: str = Field(..., description="Role of the speaker: system, user, assistant, or tool")
    content: str = Field(..., description="The textual payload of the message")
    timestamp: float = Field(..., description="POSIX timestamp of message generation")

class SubTask(BaseModel):
    id: int = Field(..., description="Unique sub-task sequence ID")
    instruction: str = Field(..., description="Explicit sub-task instruction")
    assigned_model: str = Field(default="gemma4", description="Model routed for execution: e.g., gemma4, qwen3.6-vl, claude-5.6")
    status: str = Field(default="pending", pattern="^(pending|running|completed|failed)$")

class HomeAgentStateUpdate(BaseModel):
    thread_id: str = Field(..., description="Unique orchestration thread identifier")
    messages: List[StateMessage] = Field(default_factory=list)
    plan: List[SubTask] = Field(default_factory=list)
    session_context: Dict[str, Any] = Field(default_factory=dict)

def process_state_update(raw_payload: dict) -> Optional[HomeAgentStateUpdate]:
    """Parses and validates incoming LangGraph state updates using Pydantic v2."""
    try:
        # Strict validation with Pydantic v2 model_validate
        state = HomeAgentStateUpdate.model_validate(raw_payload)
        print(f"✅ Successfully validated thread: {state.thread_id}")
        print(f"  Messages: {len(state.messages)}")
        print(f"  Sub-tasks in active plan: {len(state.plan)}")
        return state
    except ValidationError as e:
        print(f"❌ State validation failed: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    # Mock runtime payload representing an updated agent loop
    mock_payload = {
        "thread_id": "homelab-sync-2027-01-07",
        "messages": [
            {
                "role": "user",
                "content": "Sync the latest receipt from Paperless to Vikunja as a task.",
                "timestamp": 1798628400.0
            },
            {
                "role": "assistant",
                "content": "I am planning the extraction and synchronization task.",
                "timestamp": 1798628402.0
            }
        ],
        "plan": [
            {
                "id": 1,
                "instruction": "Retrieve matching document metadata from Paperless-ngx",
                "assigned_model": "gemma4",
                "status": "completed"
            },
            {
                "id": 2,
                "instruction": "Create a high-priority synchronized todo item in Vikunja",
                "assigned_model": "qwen3.6-vl",
                "status": "pending"
            }
        ],
        "session_context": {
            "mcp_server": "FastMCP-3.1-Local",
            "active_user": "admin"
        }
    }

    validated_state = process_state_update(mock_payload)
    if validated_state:
        print("Trajectory verification:")
        for task in validated_state.plan:
            print(f"  Task {task.id}: '{task.instruction}' allocated to {task.assigned_model} [{task.status}]")
```

## Related tools / concepts
- [Agentic Workflows](patterns/agentic-workflows.md)
- [Home Assistant](../services/home-assistant.md)
- [Paperless-ngx](../services/paperless-ngx.md)
- [Vikunja](../services/vikunja.md)
- [LangGraph](../tools/frameworks/langgraph.md)
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md)
- [Pydantic](../tools/development_ops/pydantic.md)

## Sources / References
- [LangGraph Core State Documentation](https://langchain-ai.github.io/langgraph/)
- [SQLite Checkpointer Spec (LangGraph API)](https://langchain-ai.github.io/langgraph/reference/checkpoints/)
- [Model Context Protocol (MCP) FastMCP 3.1 Specification](https://modelcontextprotocol.io/)
- [Pydantic V2 Migration & Custom Types Guide](https://docs.pydantic.dev/latest/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
