# Home Admin Agent Architecture

## What it is
The Home Admin Agent is a LangChain and LangGraph-based autonomous system designed to orchestrate homelab tasks, manage family knowledge, and control home automation. It acts as a central "brain" for a self-hosted smart home, capable of multi-step reasoning and tool interaction.

## What problem it solves
Managing a complex homelab and smart home often requires multiple disparate interfaces (Home Assistant, Paperless-ngx, Vikunja, etc.). This architecture provides a unified, natural language interface that can reason across these services—for example, "Remind me to pay the bill I just uploaded to Paperless."

## Where it fits in the stack
It is the **Orchestration Layer** of the home AI ecosystem. It sits above individual **Services** (like Home Assistant) and below the **User Interface** (like a mobile app or chat client), translating high-level intent into technical execution.

## Typical use cases
- **Proactive Maintenance**: Monitoring server logs and notifying the user of potential disk failures.
- **Family Administration**: Automatically extracting due dates from scanned school forms and adding them to the family calendar.
- **Context-Aware Automation**: Adjusting home lighting or climate based on the user's current schedule and location.

## Strengths
- **Autonomous Reasoning**: Uses a Plan-and-Execute pattern to handle complex, multi-service requests.
- **Modular Extensibility**: The standardized Tool Registry allows for easy integration of new services.
- **Stateful Persistence**: Remembers conversation context and execution history across restarts.

## Limitations
- **High Latency**: Multi-step reasoning through LLM calls is slower than traditional, rule-based automation.
- **Hardware Dependency**: Requires significant local compute or reliable API access to frontier models (like Claude 3.5 Sonnet).
- **Security Complexity**: Requires careful management of API tokens and permissions for the various home services it controls.

## When to use it
- When you have a complex set of self-hosted services that you want to control via a single, intelligent interface.
- When you need "cross-service" reasoning that simple automations cannot provide.

## When not to use it
- For simple, time-critical automations (e.g., turning on a light when a motion sensor is triggered)—use Home Assistant's native automations instead.
- If you have strict privacy requirements that prevent sending data to external LLM providers (unless using a fully local LLM like Llama 3).

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

## Related tools / concepts
- [Agentic Workflows](patterns/agentic-workflows.md)
- [Multi-Agent KnowledgeOps](../architecture/multi_agent_knowledgeops.md)
- [Home Assistant](../services/home-assistant.md)
- [Paperless-ngx](../services/paperless-ngx.md)
- [Vikunja](../services/vikunja.md)
- [LangGraph](../tools/frameworks/langgraph.md)
- [LangChain](../tools/frameworks/langchain.md)
- [Pydantic](../tools/development_ops/pydantic.md)

## Sources / References
- [LangChain Plan-and-Execute](https://python.langchain.com/docs/modules/agents/agent_types/plan_and_execute)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Pydantic V2 Documentation](https://docs.pydantic.dev/latest/)

## Contribution Metadata
- Last reviewed: 2026-05-10
- Confidence: high
