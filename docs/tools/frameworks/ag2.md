# AG2 (formerly AutoGen)

## What it is
AG2 is the next-generation evolution of the AutoGen framework. It is an open-source framework for building multi-agent AI applications that can converse with each other and interact with tools and environments. As of June 2026, it serves as a universal runtime (AG2 AgentOS) for orchestrating specialized agents from various frameworks including Google ADK, OpenAI, and LangChain.

## What problem it solves
It simplifies the development of complex AI systems where multiple agents need to collaborate, reason, and act. AG2 addresses "islands of intelligence" by providing a universal runtime for framework interoperability, unified state management ("shared brain"), and standardized protocols (A2A and MCP) for secure agent-to-agent and agent-to-tool communication.

## Where it fits in the stack
**Framework / Multi-Agent Orchestrator / Agent Runtime**.

## Typical use cases
- **Multi-Framework Orchestration**: Connecting agents built in different frameworks (e.g., a LangChain researcher and an OpenAI analyst) into a single cohesive team.
- **Cross-Platform Coordination**: Assembling dynamic teams of specialized personas that can operate across local and cloud environments.
- **Unified State Management**: Maintaining consistent context and task state across long-running agentic workflows.
- **Visual Team Composition**: Using **Waldiez** (the community-led visual companion) to design and debug multi-agent group chats.

## Strengths
- **Protocol-First Interoperability**: Built-in support for **A2A (Agent-to-Agent)** and **MCP (Model Context Protocol)**.
- **Flexible Conversational Design**: Native support for group chats, hierarchical orchestration, and custom state-based transitions.
- **Enterprise-Ready Security**: Features like Agent Cards and secure tool-calling guards for production deployments.
- **Shared Brain Architecture**: Advanced state management that prevents context loss in complex multi-step tasks.

## Limitations
- **Transition Complexity**: Migrating from the legacy Microsoft AutoGen (v0.2) to the AG2 AgentOS architecture requires significant refactoring of orchestration logic.
- **Orchestration Overhead**: The high level of abstraction can make fine-grained control over individual LLM parameters more complex than using low-level SDKs.

## When to use it
- When you need to build sophisticated multi-agent systems involving agents from multiple different providers or frameworks.
- When you require a proven, enterprise-grade foundation for collaborative AI workflows.
- When building AI-native organizations where specialized agents must discover and delegate to each other dynamically.

## When not to use it
- For simple, single-agent tasks where a direct SDK call is sufficient.
- If you prefer a rigid DAG-based workflow without conversational flexibility.

## Getting started

### Installation
```bash
pip install ag2
```

### Basic Multi-Agent Setup
AG2 maintains compatibility with the `autogen` package name:
```python
import autogen
from ag2 import AgentOS

# Initialize the universal runtime
runtime = AgentOS.init()

# Define agents
assistant = autogen.AssistantAgent("helper", llm_config={"model": "gpt-4o"})
user_proxy = autogen.UserProxyAgent("user", code_execution_config={"use_docker": False})

# Orchestrate
user_proxy.initiate_chat(assistant, message="Analyze our cross-framework dependencies.")
```

## CLI examples

### Initializing a Project
```bash
ag2 init my-agent-org
```

### Running in Studio Mode
```bash
ag2 studio --port 8081
```

## API examples

### Cross-Framework Delegation (A2A)
```python
from ag2.protocols import A2A

# Delegate a task to an external Google ADK agent
result = await A2A.delegate(
    target_agent_id="google-adk-analyst",
    task="Perform financial sentiment analysis",
    context=shared_brain.get_context()
)
```

### Unified State Access
```python
# Access the 'shared brain' across the team
state = runtime.get_state("workflow-id-123")
print(state.history)
```

## Related tools / concepts
- [AutoGen](autogen.md) — The original legacy framework.
- [CrewAI](crewai.md) — Role-based multi-agent framework.
- [LangGraph](langgraph.md) — Graph-based agent orchestration.
- [Mastra](mastra.md) — TypeScript-native agent framework.
- [Rivet](rivet.md) — Visual AI programming environment.
- [MCP](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Standardized tool-calling protocol supported by AG2.
- [PydanticAI](pydantic-ai.md) — Type-safe agent framework.
- [Semantic Kernel](semantic-kernel.md) — Microsoft's agentic framework.

## Sources / References
- [Official Website](https://ag2.ai/)
- [GitHub Repository](https://github.com/ag2ai/ag2)
- [AG2 vs AutoGen Comparison](https://www.ag2.ai/compare/autogen)

## Backlog
- [x] Perform quarterly technical freshness audit. (Completed: 2026-06-21)

## Contribution Metadata
- Last reviewed: 2026-06-21
- Confidence: high
