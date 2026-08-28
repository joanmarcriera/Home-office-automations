# AG2 (formerly AutoGen)

## What it is
AG2 is the next-generation evolution of the AutoGen framework. It is an open-source framework for building multi-agent AI applications that can converse with each other and interact with tools and environments. In early January 2027, it serves as a universal runtime (**AG2 AgentOS**) for orchestrating specialized agents from various frameworks, fully integrated with SOTA models like Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, and [Gemma 4](../ai_knowledge/local_llms.md) for local reasoning and the **Model Context Protocol (MCP 3.1)** and **FastMCP 3.1** task execution standards.

## What problem it solves
It simplifies the development of complex AI systems where multiple agents need to collaborate, reason, and act. AG2 addresses "islands of intelligence" by providing a universal runtime for framework interoperability, unified state management ("shared brain"), and standardized protocols (A2A and FastMCP 3.1) for secure agent-to-agent and agent-to-tool communication. It specifically solves the orchestration and latency bottleneck in large-scale multi-agent deployments.

## Where it fits in the stack
**Framework / Multi-Agent Orchestrator / Agent Runtime**. AG2 AgentOS sits at the orchestrator layer, organizing and coordinating individual agents and routing messages.

## Typical use cases
- **Multi-Framework Orchestration**: Connecting agents built in different frameworks (e.g., a LangChain researcher and a PydanticAI analyst) into a single cohesive team.
- **Cross-Platform Coordination**: Assembling dynamic teams of specialized personas that can operate across local (Gemma 4) and cloud (Claude 5.6/GPT-5.6/Gemini 4.0 Ultra) environments.
- **Unified State Management**: Maintaining consistent context and task state across long-running, multi-step agentic workflows.
- **Visual Team Composition**: Using **Waldiez** (the community-led visual companion) to design, validate, and debug multi-agent group chats.

## Strengths
- **Protocol-First Interoperability**: Native support for **A2A (Agent-to-Agent)** and **MCP 3.1 / FastMCP 3.1** Task Protocols.
- **Flexible Conversational Design**: Support for group chats, hierarchical orchestration, and custom state-based transitions.
- **Enterprise-Ready Security**: Features like Agent Cards, guardrails, and secure tool-calling authorization for production environments.
- **Shared Brain Architecture**: Advanced state management that prevents context loss or dilution in complex multi-step tasks.

## Limitations
- **Transition Complexity**: Migrating from legacy AutoGen (v0.2) to the AG2 AgentOS architecture requires refactoring of orchestration logic.
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
pip install ag2 pydantic>=2.0
```

### Basic Multi-Agent Setup
AG2 maintains compatibility with the `autogen` package name:
```python
import autogen
from ag2 import AgentOS

# Initialize the universal runtime
runtime = AgentOS.init()

# Define agents
assistant = autogen.AssistantAgent("helper", llm_config={"model": "gpt-5.6"})
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

### Managing Agent Cards
```bash
ag2 cards list
```

## API examples

### Python (Universal AgentOS Config & FastMCP 3.1 Card Validation)
AG2 relies on Agent Cards and Runtime Configurations to coordinate multi-agent teams. The following example validates an AG2 runtime and agent cards setup using **Pydantic v2**:

```python
import os
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator

# 1. Define robust Pydantic v2 schemas for AG2 Agent Cards & AgentOS Configurations
class AG2AgentCard(BaseModel):
    agent_id: str = Field(..., serialization_alias="agentId", validation_alias="agentId")
    name: str = Field(..., description="Name of the agent.")
    role: str = Field(..., description="The expertise or primary function of this agent.")
    model_name: str = Field(..., serialization_alias="modelName", validation_alias="modelName")
    mcp_tools: List[str] = Field(default_factory=list, serialization_alias="mcpTools", validation_alias="mcpTools")

    @field_validator("model_name")
    @classmethod
    def validate_model(cls, v: str) -> str:
        allowed = ["Claude 5.6", "GPT-5.6", "Gemini 4.0 Ultra", "DeepSeek-V4", "Gemma 4"]
        if not any(m in v for m in allowed):
            raise ValueError(f"Model {v} must be an early 2027 SOTA model: {allowed}")
        return v

class AG2RuntimeConfig(BaseModel):
    session_id: str = Field(..., serialization_alias="sessionId", validation_alias="sessionId")
    agents: List[AG2AgentCard] = Field(...)
    enable_shared_brain: bool = Field(default=True, serialization_alias="enableSharedBrain", validation_alias="enableSharedBrain")
    max_turns: int = Field(default=20, ge=1, le=100, serialization_alias="maxTurns", validation_alias="maxTurns")

# 2. Setup configuration payload for a collaborative analyst-researcher team
runtime_payload = {
    "sessionId": "session-ag2-9904",
    "enableSharedBrain": True,
    "maxTurns": 30,
    "agents": [
        {
            "agentId": "agent-researcher-1",
            "name": "Local Researcher",
            "role": "Retrieves local documentation data",
            "modelName": "Gemma 4",
            "mcpTools": ["fetch_file", "search_directory"]
        },
        {
            "agentId": "agent-analyst-1",
            "name": "Lead Analyst",
            "role": "Synthesizes final reports",
            "modelName": "Claude 5.6",
            "mcpTools": ["generate_chart"]
        }
    ]
}

# 3. Validate AG2 configuration payload
try:
    config = AG2RuntimeConfig(**runtime_payload)
    print("AG2 AgentOS runtime configuration verified successfully!")
    print(f"Session ID: {config.session_id}")
    print(f"Shared Brain Enabled: {config.enable_shared_brain}")
    print(f"Total Configured Agents: {len(config.agents)}")
    for agent in config.agents:
        print(f" - Agent: {agent.name} backed by {agent.model_name}")
except Exception as e:
    print(f"Configuration validation failed: {e}")
```

## Related tools / concepts
- [Gemma 4](../ai_knowledge/local_llms.md) — Canonical local LLM for agentic reasoning.
- [AutoGen](autogen.md) — The original legacy framework.
- [CrewAI](crewai.md) — Role-based multi-agent framework.
- [LangGraph](langgraph.md) — Graph-based agent orchestration.
- [Mastra](mastra.md) — TypeScript-native agent framework.
- [Rivet](rivet.md) — Visual AI programming environment.
- [MCP](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Standardized tool-calling protocol.
- [PydanticAI](pydantic-ai.md) — Type-safe agent framework.
- [Semantic Kernel](semantic-kernel.md) — Microsoft's agentic framework.

## Sources / references
- [Official Website](https://ag2.ai/)
- [GitHub Repository](https://github.com/ag2ai/ag2)
- [AG2 vs AutoGen Comparison](https://www.ag2.ai/compare/autogen)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
