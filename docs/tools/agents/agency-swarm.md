# Agency Swarm

## What it is
Agency Swarm (v1.4+, early January 2027) is an open-source, multi-agent orchestration framework that simplifies the creation of collaborative agent teams organized like a professional company or department. While originally built on top of the OpenAI Assistants API, it has evolved into a robust, provider-agnostic system optimized for local first-class execution on local models like [Gemma 4](../ai_knowledge/local_llms.md), [Llama 4](../ai_knowledge/local_llms.md), and [Qwen 3.6](../ai_knowledge/local_llms.md), alongside frontier cloud models such as [Claude 5.6](../providers/anthropic.md), [GPT-5.6](../ai_knowledge/openai.md), and [Gemini 4.0 Ultra](../providers/google-ai-studio.md). It features full compatibility with the [Model Context Protocol (MCP) 3.1](../../knowledge_base/agent_protocols.md) and FastMCP 3.1 Task Protocol.

## What problem it solves
Managing coordination loops, conversation histories, prompt sequencing, and tool execution in large multi-agent systems is highly complex. Without structure, agents frequently experience "agentic loops," redundant executions, or state fragmentation. Agency Swarm solves this by implementing an organizational hierarchy where agents communicate dynamically through standardized "send_message" mechanisms. This design establishes clean communication boundaries and maintains execution state, allowing complex multi-turn tasks to execute autonomously.

## Where it fits in the stack
[Layer 6: Agents & Orchestration](../../knowledge_base/ai_tooling_landscape.md#layer-6-agents-orchestration) — A structured multi-agent collaboration framework that handles high-level team workflows.

## Typical use cases
- **Software Development Agency**: Structuring specialized roles (CEO, Developer, Product Owner, QA Engineer) working in sequence to implement and test features.
- **Enterprise Marketing Pipelines**: Deploying creative and research swarms that collaborate on target audience profiling, copy drafts, and channel distribution schedules.
- **Privacy-First Local Analysis**: Running specialized local [Gemma 4](../ai_knowledge/local_llms.md) agents on-premise to securely analyze financial statements.
- **Support Ticket Escalation**: Directing user requests through triaging agents that automatically route complex technical issues to dedicated API integration agents.

## Strengths
- **Intuitive Organization**: Formulating agent groups via a company hierarchy is straightforward and easy to conceptualize.
- **Native FastMCP 3.1**: Standardized tool discovery and low-latency local hosting for high-frequency tool calls.
- **Local Optimization**: Tailored to run efficiently on local inference engines (e.g., [Ollama](../../services/ollama.md)) with minimal token overhead.
- **Strict Data Validation**: Utilizes robust type-safe Pydantic tool structures for clean data passing.

## Limitations
- **Communication Overhead**: The structured message-passing pattern can add small execution latencies relative to raw parallel prompt chains.
- **VRAM Heavy**: Running a multi-agent swarm locally with multiple concurrent model contexts requires substantial hardware/GPU capacity.
- **Configuration Fine-Tuning**: Designing stable, loop-free communications for large swarms with more than 5 agents requires meticulous instruction tuning.

## When to use it
- When you need to build collaborative agent teams with clearly defined boundaries, tasks, and interaction rules.
- For mixed execution topologies where cloud intelligence ([GPT-5.6](../ai_knowledge/chatgpt.md)) co-orchestrates with local security ([Gemma 4](../ai_knowledge/local_llms.md)).
- If you require out-of-the-box support for hierarchical tool sharing and session management.

## When not to use it
- For basic, single-step tasks that do not benefit from multi-agent role-playing.
- In latency-critical applications where direct prompt chaining or simple routing suffices.
- If you prefer graph-based state machines (consider [LangGraph](../frameworks/langgraph.md)).

## Getting started
### Installation
```bash
pip install agency-swarm pydantic
```

### Basic Usage
Initialize an agency swarm using specialized local and cloud agents with FastMCP 3.1:
```python
from agency_swarm import Agent, Agency, set_model

# Configure the system to run local Gemma 4
set_model("gemma4:31b", provider="ollama")

# Define our collaborative agents
ceo = Agent(
    name="CEO",
    description="Corporate leader managing project directions.",
    instructions="Review project requests and dispatch coding tasks to the Developer."
)

developer = Agent(
    name="Developer",
    description="Software engineer building solutions.",
    instructions="Implement requested code features and report back to the CEO."
)

# Establish the agency with permitted communication paths (CEO <-> Developer)
agency = Agency(
    [ceo, [ceo, developer]],
    shared_instructions="Collaborate professionally to implement reliable features."
)

# Run the agency
result = agency.get_completion("CEO, please ask the developer to create a simple FastAPI server.")
print(result)
```

## CLI examples
```bash
# Create a new boilerplated agency workspace structure
agency-swarm create-space --name dev_agency

# Execute a specific agent stand-alone in the console
python -m dev_agency.run_agent --agent_name CEO

# Verify and list all FastMCP 3.1 tools registered within your local space
python -m dev_agency.list_tools --protocol fastmcp3.1
```

## API examples
### Multi-Agent Communication Trace Validation (Pydantic v2)
In enterprise scenarios, validating communication traces and execution states generated by Agency Swarm is key to preventing system failures. The following script validates a message-passing log using Pydantic v2:

```python
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class AgentMessage(BaseModel):
    sender: str = Field(..., description="The name of the sending agent")
    recipient: str = Field(..., description="The name of the receiving agent")
    message_body: str = Field(..., description="The content of the message")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class AgencyState(BaseModel):
    agency_id: str = Field(..., description="Unique Agency execution session ID")
    active_model: str = Field(..., description="The underlying LLM coordinating the swarm")
    agents: List[str] = Field(default_factory=list, description="Active agents in the agency")
    communication_history: List[AgentMessage] = Field(default_factory=list)
    status: Literal["idle", "processing", "escalated", "completed"] = Field("idle")

    @field_validator("agents")
    @classmethod
    def validate_agent_swarm(cls, agents: List[str]) -> List[str]:
        if len(agents) < 2:
            raise ValueError("An agency swarm must contain at least 2 cooperating agents")
        return agents

# Sample telemetry data from a completed run
swarm_telemetry = {
    "agency_id": "agency-session-2027-0484",
    "active_model": "gemma4-31b",
    "agents": ["CEO", "Developer"],
    "communication_history": [
        {
            "sender": "CEO",
            "recipient": "Developer",
            "message_body": "Developer, please expose a FastMCP 3.1 tool for document searching.",
            "timestamp": "2027-01-07T09:15:00Z"
        },
        {
            "sender": "Developer",
            "recipient": "CEO",
            "message_body": "CEO, the FastMCP 3.1 Task Protocol tool is running on port 18790.",
            "timestamp": "2027-01-07T09:16:30Z"
        }
    ],
    "status": "completed"
}

# Strict validation
validated_state = AgencyState(**swarm_telemetry)
print(f"Validated Agency: {validated_state.agency_id} with Status: {validated_state.status}")
print(f"Communicated agents count: {len(validated_state.agents)}")
```

## Related tools / concepts
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [CrewAI](../frameworks/crewai.md)
- [LangGraph](../frameworks/langgraph.md)
- [Agno](./agno.md)
- [Bee Agent Framework](./bee-agent-framework.md)
- [Composio](./composio.md)
- [Gemma 3](../ai_knowledge/local_llms.md)

## Sources / references
- [GitHub Repository](https://github.com/VRSEN/agency-swarm)
- [Official Website](https://agency-swarm.ai/)
- [Agency Swarm Documentation](https://vrsen.github.io/agency-swarm/)
- [FastMCP 3.1 Integration Guide](https://vrsen.github.io/agency-swarm/fastmcp3.1)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
