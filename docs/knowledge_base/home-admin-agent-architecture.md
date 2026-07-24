# Home Admin Agent Architecture

## What it is
The Home Admin Agent is a stateful, LangChain- and LangGraph-based autonomous coordination system designed to orchestrate complex homelab pipelines, manage family knowledge graphs, and control local smart home environments. It acts as the centralized intelligent operating system ("brain") for the home, capable of multi-step reasoning, persistent memory tracking, and dynamic tool invocation using the [Model Context Protocol (MCP 3.1)](../tools/automation_orchestration/mcp.md).

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
- **Dynamic Tool Discovery (MCP 3.1)**: Leverages Model Context Protocol (MCP 3.1) Task Protocol interfaces to dynamically bind, inspect, and execute remote and local tool definitions.
- **Hybrid Inference Execution**: Seamlessly routes tasks between lightweight local models (e.g., Gemma 3, Llama 4, or Qwen 3.6) for low-latency operations and frontier APIs (such as Claude 5.1 or GPT-5.5) for complex reasoning.

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

# Launch the LangGraph orchestration server with active MCP 3.1 server registration
ralph-admin start --port 8080 --config ./config/agent_config.yaml --enable-mcp

# Test a specific tool in isolation to verify credentials and response schemas
ralph-admin tool-run --tool "paperless_search" --arguments '{"query": "july 2026 water bill"}'
```

## API examples

### Graph State Definition (Python)
```python
from typing import Annotated, List, Dict, Any
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class HomeAgentState(TypedDict):
    """Represents the complete state of the LangGraph orchestration loop."""
    # List of conversational messages (automatically concatenated and updated)
    messages: Annotated[List[Any], add_messages]
    # Current active execution plan containing sequential sub-tasks
    plan: List[str]
    # History of executed step outputs and outcomes
    execution_results: List[Dict[str, Any]]
    # Dynamic runtime context shared across custom home tools
    session_context: Dict[str, Any]
```

### Stateful Memory Manager with SQLite checkpointer (Python)
```python
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

class AgentMemoryManager:
    """Manages the lifecycle of persistent state databases for the Home Admin Agent."""
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.saver = SqliteSaver(self.conn)

    def get_saver(self) -> SqliteSaver:
        return self.saver

    def get_thread_state(self, thread_id: str) -> Dict[str, Any]:
        config = {"configurable": {"thread_id": thread_id}}
        return self.saver.get(config)

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    manager = AgentMemoryManager("./data/agent_memory.db")
    print("Persistent SQLite state checkpointer initialized successfully.")
    manager.close()
```

### Base Home Tool Schema (Python & Pydantic v2)
```python
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import Type

class ToolMetadata(BaseModel):
    name: str = Field(..., description="Unique name of the tool registered in the agent registry")
    description: str = Field(..., description="Detailed explanation of the tool's usage, inputs, and side-effects")
    args_schema: Type[BaseModel] = Field(..., description="Pydantic schema defining the tool arguments")

class BaseHomeTool(ABC):
    """Abstract base class for all custom Python tools registered in the Home Admin Agent."""

    @classmethod
    @abstractmethod
    def get_metadata(cls) -> ToolMetadata:
        """Returns the structural metadata and validation schema for the tool."""
        pass

    @abstractmethod
    async def execute(self, **kwargs) -> str:
        """Executes the tool's core logic asynchronously with standard error boundaries."""
        pass
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
- [Model Context Protocol (MCP) v3.1 Technical Specification](https://modelcontextprotocol.io/)
- [Pydantic V2 Migration & Custom Types Guide](https://docs.pydantic.dev/latest/)

## Contribution Metadata
- Last reviewed: 2026-07-24
- Confidence: high
