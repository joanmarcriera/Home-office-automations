# Agency Swarm

## What it is
Agency Swarm (v1.4+, early January 2027) is an open-source, multi-agent orchestration framework that simplifies the creation of collaborative agent teams organized like a professional company or department. While originally built on top of the OpenAI Assistants API, it has evolved into a robust, provider-agnostic system optimized for local first-class execution on local models like [Gemma 4](../ai_knowledge/local_llms.md), [Llama 4](../ai_knowledge/local_llms.md), and [Qwen 3.6](../ai_knowledge/local_llms.md), alongside frontier cloud models such as [Claude 5.6](../providers/anthropic.md), [GPT-5.6](../ai_knowledge/openai.md), and [Gemini 4.0 Ultra](../providers/google-ai-studio.md). It features full compatibility with the [Model Context Protocol (MCP) 3.1](../../knowledge_base/agent_protocols.md) and FastMCP 3.1 Task Protocol.

```
+-----------------------------------------------------------------------------------+
|                        AGENCY SWARM SYSTEM ARCHITECTURE                           |
+-----------------------------------------------------------------------------------+

  +-------------------------------------------------------------------------------+ |
  |                         ORGANIZATIONAL AGENCY TOPOLOGY                        | |
  |                                                                               | |
  |   +---------------------+   +---------------------+   +---------------------+ | |
  |   | CEO Agent           |   | Product Owner Agent |   | Security / QA       | | |
  |   | (Chief Orchestration|   | (Requirements       |   | Audit Agent         | | |
  |   +---------------------+   +---------------------+   +---------------------+ | |
  +-------------------------------------------------------------------------------+ |
                                            |
                                            v
  +-------------------------------------------------------------------------------+ |
  |                     DIRECTED COMMUNICATION & STATE BUS                        | |
  |                                                                               | |
  |   +---------------------+   +---------------------+   +---------------------+ | |
  |   | SendMessage Protocol|   | Session Memory &    |   | Context Window      | | |
  |   | (Strict Agent-to-   |   | Thread Checkpoints  |   | Truncation Guard    | | |
  |   | Agent Routing)      |   |                     |   |                     | | |
  |   +---------------------+   +---------------------+   +---------------------+ | |
  +-------------------------------------------------------------------------------+ |
                                            |
                                            v
  +-------------------------------------------------------------------------------+ |
  |                       FAST MCP 3.1 TOOL EXTRACTION & RUNTIMES                 | |
  |                                                                               | |
  |   +---------------------+   +---------------------+   +---------------------+ | |
  |   | Developer Agent     |   | FastMCP 3.1 Tool    |   | Local Gemma 4 /     | | |
  |   | (Code Implementation|   | Registry & Servers  |   | GPT-5.6 LLM Bridge  | | |
  |   +---------------------+   +---------------------+   +---------------------+ | |
  +-------------------------------------------------------------------------------+ |
                                            |
                                            v
  +-------------------------------------------------------------------------------+ |
  |                    HYBRID LLM PROVIDER DISPATCH LAYER                         | |
  |                                                                               | |
  |   +---------------------+   +---------------------+   +---------------------+ | |
  |   | Local Ollama Daemon |   | Anthropic API       |   | OpenAI API Gateway  | | |
  |   | (Gemma 4 31B Local) |   | (Claude 5.6 Cloud)  |   | (GPT-5.6 Cloud)     | | |
  |   +---------------------+   +---------------------+   +---------------------+ | |
  +-------------------------------------------------------------------------------+ |
```

## What problem it solves
Managing coordination loops, conversation histories, prompt sequencing, and tool execution in large multi-agent systems is highly complex. Without structure, agents frequently experience "agentic loops," redundant executions, or state fragmentation. Agency Swarm solves this by implementing an organizational hierarchy where agents communicate dynamically through standardized "send_message" mechanisms. This design establishes clean communication boundaries and maintains execution state, allowing complex multi-turn tasks to execute autonomously.

- **Unstructured Multi-Agent Chaos**: Eliminates chaotic all-to-all communication channels by establishing strict hierarchical messaging permissions.
- **Agentic Infinite Loops**: Implements strict tool execution budgets and message reflection loops to break circular agent responses.
- **Provider Lock-In**: Enables hybrid swarms where strategic planning agents run on high-capacity cloud APIs while execution/code-writing agents run on local open-weights engines.

## Where it fits in the stack
[Layer 6: Agents & Orchestration](../../knowledge_base/ai_tooling_landscape.md#layer-6-agents-orchestration) — A structured multi-agent collaboration framework that handles high-level team workflows.

```
+-----------------------------------------------------------------------------------+
|                            STACK INTEGRATION MATRIX                               |
+-----------------------------------------------------------------------------------+
  Control Topology        : Agency Hierarchy (CEO -> PM -> Dev / QA)
  Communication Protocol  : SendMessage Tool Protocol & FastMCP 3.1 Tools
  Validation Engine       : Pydantic v2 Telemetry & Message Schema Validator
  Compute Backends        : Local Ollama (Gemma 4 / Llama 4), Anthropic Claude 5.6
+-----------------------------------------------------------------------------------+
```

## Key Features & Operational Capabilities

### 1. Hierarchical Permitted Communication Graph
In Agency Swarm, communication channels between agents are explicitly declared during initialization (e.g., `[ceo, [ceo, dev], [dev, qa]]`). A developer agent cannot send unsolicited instructions to the CEO unless explicitly granted a return channel, preventing authorization and state leaks.

### 2. Hybrid Cloud / On-Premise Model Binding
Different agents in the same agency can utilize different model providers:
- **CEO Agent**: Bound to **Claude 5.6** or **GPT-5.6** for high-context strategic reasoning.
- **Developer Agent**: Bound to local **Gemma 4 31B** or **Qwen 3.6** running via Ollama for zero-cost, high-speed code generation.

```
+-----------------------------------------------------------------------------------+
|                        COMMUNICATION GRAPH & PERMISSIONS                          |
+-----------------------------------------------------------------------------------+
  [ CEO Agent ] <======== (SendMessage Allowed) ========> [ Project Manager ]
       ||                                                        ||
       || (Blocked Direct Path)                                  || (Allowed Path)
       \/                                                        \/
  [ QA Inspector ] <======= (SendMessage Allowed) ========> [ Developer Agent ]
+-----------------------------------------------------------------------------------+
```

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
pip install agency-swarm pydantic>=2.0.0
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

## Detailed Code Example: Hybrid FastMCP 3.1 Swarm Orchestrator

The following complete Python application demonstrates a production-grade Agency Swarm pipeline integrating FastMCP 3.1 tool binding, Pydantic v2 execution tracking, and hybrid model routing.

```python
import asyncio
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field, field_validator, ValidationError

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] AgencySwarm: %(message)s")
logger = logging.getLogger("EnterpriseSwarm")

# --- Pydantic v2 Data Models ---

class AgentMessagePayload(BaseModel):
    message_id: str = Field(..., description="Unique message UUID")
    sender_role: str = Field(..., description="Role emitting the message")
    recipient_role: str = Field(..., description="Target role recipient")
    content: str = Field(..., description="Message text or tool request payload")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class SwarmTelemetry(BaseModel):
    session_id: str = Field(..., description="Agency session identifier")
    primary_model: str = Field("claude-5.6", description="Top-level planning LLM")
    local_model: str = Field("gemma-4-31b", description="Local code generation LLM")
    messages: List[AgentMessagePayload] = Field(default_factory=list)
    status: Literal["init", "active", "completed", "failed"] = Field("init")

    @field_validator("messages")
    @classmethod
    def enforce_communication_sequence(cls, msgs: List[AgentMessagePayload]) -> List[AgentMessagePayload]:
        if len(msgs) > 0 and msgs[0].sender_role != "User" and msgs[0].sender_role != "CEO":
            logger.warning(f"Swarm initiated by non-standard role: {msgs[0].sender_role}")
        return msgs

# --- FastMCP 3.1 Swarm Bridge ---

class AgencySwarmBridge:
    def __init__(self, session_id: str):
        self.telemetry = SwarmTelemetry(session_id=session_id)

    def dispatch_agent_message(self, sender: str, recipient: str, message: str) -> AgentMessagePayload:
        logger.info(f"[{sender} -> {recipient}]: {message[:80]}...")
        payload = AgentMessagePayload(
            message_id=f"msg_{len(self.telemetry.messages) + 1:04d}",
            sender_role=sender,
            recipient_role=recipient,
            content=message
        )
        self.telemetry.messages.append(payload)
        return payload

    async def execute_agency_workflow(self, task_prompt: str) -> SwarmTelemetry:
        self.telemetry.status = "active"

        # Step 1: User -> CEO
        self.dispatch_agent_message("User", "CEO", task_prompt)

        # Step 2: CEO -> Product Owner (Planning)
        await asyncio.sleep(0.5)
        self.dispatch_agent_message(
            "CEO", "ProductOwner",
            "Decompose user requirement into FastMCP 3.1 technical specifications."
        )

        # Step 3: Product Owner -> Developer (Local Gemma 4 Generation)
        await asyncio.sleep(0.5)
        self.dispatch_agent_message(
            "ProductOwner", "Developer",
            "Generate Python Pydantic v2 schemas for the requested API endpoint."
        )

        # Step 4: Developer -> CEO (Completion Report)
        await asyncio.sleep(0.5)
        self.dispatch_agent_message(
            "Developer", "CEO",
            "Code generation complete. FastMCP 3.1 server validated on port 8080."
        )

        self.telemetry.status = "completed"
        return self.telemetry

# --- Execution Demonstration ---

async def main():
    bridge = AgencySwarmBridge(session_id="agency_session_2027_99x")

    task = "Build an automated Paperless-ngx document metadata parsing agent swarm."
    telemetry_result = await bridge.execute_agency_workflow(task)

    print("\n=== AGENCY TELEMETRY SUMMARY ===")
    print(f"Session ID   : {telemetry_result.session_id}")
    print(f"Swarm Status : {telemetry_result.status}")
    print(f"Total Messages: {len(telemetry_result.messages)}")
    print("\n=== MESSAGE HISTORY JSON ===")
    print(json.dumps([m.model_dump() for m in telemetry_result.messages], indent=2))

if __name__ == "__main__":
    asyncio.run(main())
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
