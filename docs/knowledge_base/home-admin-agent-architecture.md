# Home Admin Agent Architecture

This document defines the architecture for the "Home Admin Agent," a LangChain-based assistant designed to orchestrate homelab tasks, manage family knowledge, and control home automation.

## Core Architecture

The agent follows a **Plan-and-Execute** pattern implemented using **LangGraph** for robust state management and multi-step reasoning.

### Workflow Components

1.  **Planner**: An LLM-driven node that breaks down the user's high-level request into a sequence of tool calls or sub-tasks.
2.  **Executor**: A node that executes the planned steps using the **Tool Registry**.
3.  **Re-planner**: Analyzes the results of tool executions and decides whether to continue, adjust the plan, or respond to the user.
4.  **State Management**: Uses `SqliteSaver` (via `MemoryManager`) to persist the conversation thread and the execution graph state.

## Tool Registry Schema

Tools must follow a standardized schema to ensure the agent can discover and invoke them correctly.

```python
from typing import Dict, Type, Any
from pydantic import BaseModel, Field

class ToolMetadata(BaseModel):
    name: str
    description: str
    args_schema: Type[BaseModel]
    category: str # e.g., 'knowledge', 'automation', 'tasks'

class ToolRegistry:
    """Registry for dynamic tool discovery."""
    def __init__(self):
        self._tools: Dict[str, Any] = {}

    def register(self, tool_class: Any):
        metadata = tool_class.get_metadata()
        self._tools[metadata.name] = tool_class

    def get_tool(self, name: str) -> Any:
        return self._tools.get(name)

    def list_tools(self) -> List[ToolMetadata]:
        return [t.get_metadata() for t in self._tools.values()]
```

## Base Tool Class

Every tool integrated into the Home Admin Agent must inherit from this base class.

```python
from abc import ABC, abstractmethod

class BaseHomeTool(ABC):
    @classmethod
    @abstractmethod
    def get_metadata(cls) -> ToolMetadata:
        pass

    @abstractmethod
    async def run(self, **kwargs) -> str:
        """Execute the tool's primary logic."""
        pass
```

## System Prompt Design

The "Family Context" system prompt is the agent's core personality and operational logic. It includes:

1.  **Identity**: "You are Ralph, the Home Admin Agent. You assist the family with schedule management, paperless document retrieval, and home automation."
2.  **Principles**: Priority on privacy, proactive but non-intrusive alerts, and clear communication.
3.  **Context Injection**: Dynamic injection of current date, family schedule (via Calendar Tool), and active task counts (via Vikunja Tool).

## Graph State Schema

```python
from typing import Annotated, List, TypedDict
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # Messages in the conversation
    messages: Annotated[List[Any], add_messages]
    # The current plan
    plan: List[str]
    # Results from executed steps
    results: List[str]
    # Shared context across tools
    context: Dict[str, Any]
```

- Last reviewed: 2025-05-15
- Confidence: high

## Sources / references
- [LangChain Plan-and-Execute](https://python.langchain.com/docs/modules/agents/agent_types/plan_and_execute)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Pydantic V2 Documentation](https://docs.pydantic.dev/latest/)
