# OpenAI Agents SDK

## What it is
The OpenAI Agents SDK is an enterprise-grade framework designed to build, orchestrate, and govern AI agents. It introduces a clear separation between the "harness" (the control logic and governance loop) and the "compute" (the LLM reasoning layer), allowing for high-scalability multi-agent architectures. In early 2027, it serves as a primary standard for deploying high-autonomy agents powered by **GPT-5.5 / GPT-5.6**, **O5 reasoning series**, and interoperable multi-model fallback routines for models like **Claude 5.1** and **Gemma 3**.

```
+-----------------------------------------------------------------------------------+
|                     OPENAI AGENTS SDK SYSTEM ARCHITECTURE                         |
+-----------------------------------------------------------------------------------+

  +-------------------------------------------------------------------------------+ |
  |                         AGENT HARNESS CONTROL LAYER                           | |
  |                                                                               | |
  |   +---------------------+   +---------------------+   +---------------------+ | |
  |   | State & Checkpoint  |   | Guardrails & Safety |   | Handoff & Router    | | |
  |   | Management          |   | Perimeter           |   | Orchestration       | | |
  |   +---------------------+   +---------------------+   +---------------------+ | |
  +-------------------------------------------------------------------------------+ |
                                            |
                                            v
  +-------------------------------------------------------------------------------+ |
  |                        FAST MCP 3.1 PROTOCOL & SANDBOX                        | |
  |                                                                               | |
  |   +---------------------+   +---------------------+   +---------------------+ | |
  |   | FastMCP 3.1 Tool    |   | Containerized Code  |   | Multi-Tenant Token  | | |
  |   | Integration         |   | Sandbox Runtime     |   | Metering & Auth     | | |
  |   +---------------------+   +---------------------+   +---------------------+ | |
  +-------------------------------------------------------------------------------+ |
                                            |
                                            v
  +-------------------------------------------------------------------------------+ |
  |                       DECOUPLED LLM COMPUTE PROVIDERS                         | |
  |                                                                               | |
  |   +---------------------+   +---------------------+   +---------------------+ | |
  |   | GPT-5.5 / GPT-5.6   |   | O5 Reasoning Series |   | Claude 5.1 / Gemma  | | |
  |   | High-Context Engine |   | Chain-of-Thought    |   | External Fallbacks  | | |
  |   +---------------------+   +---------------------+   +---------------------+ | |
  +-------------------------------------------------------------------------------+ |
```

## What problem it solves
It simplifies the creation of multi-agent systems that execute multi-step tools, manage distributed state, and adhere to strict safety perimeters. By separating the harness control layer from the underlying model compute, it enables fine-grained sandbox isolation, multi-tenant token billing, and secure tool execution, eliminating the security and reliability bottlenecks of monolithic agent loops.

- **Monolithic Control Failure**: Traditional agent loops bundle model inference directly with state management, making context truncation or provider failover hazardous to persistent tasks.
- **Unbounded Code Execution Risks**: Prevents runaway local code execution by forcing all dynamically generated scripts into sandboxed isolated runtimes.
- **Protocol Fragmentations**: Standardizes tool invocations using the **FastMCP 3.1 Protocol**, eliminating custom JSON wrapper boilerplate across enterprise agent networks.

## Where it fits in the stack
**Category**: [Frameworks](./index.md) / [Agents](../agents/index.md). It acts as the orchestration layer for **GPT-5.5 / 5.6** and the **O5 reasoning series**, while natively supporting the **FastMCP 3.1 Protocol** for standardized, ultra-low latency tool execution.

```
+-----------------------------------------------------------------------------------+
|                            STACK INTEGRATION MATRIX                               |
+-----------------------------------------------------------------------------------+
  Control Layer           : OpenAI Agents SDK Harness (Python / TypeScript)
  Tool Protocol           : FastMCP 3.1 Server Bridges & Standardized MCP Specs
  Runtime Container       : gVisor / Docker Sandboxes with Network Isolation
  Compute Backends        : GPT-5.6, O5-Max, Claude 5.1 Fallback Connectors
+-----------------------------------------------------------------------------------+
```

## Key Features & Operational Capabilities

### 1. Harness vs. Compute Decoupling
The framework's core architectural principle strictly separates execution state from model inference:
- **Harness**: Manages memory, execution graph routing, tool dispatching, human-in-the-loop approvals, and quota limits.
- **Compute**: Stateless call interface targeting LLMs. If GPT-5.6 experiences rate limits, the harness can redirect compute requests to alternative backends without dropping execution context.

### 2. Native Multi-Agent Handoff
Allows agents to transfer responsibility dynamically. When a primary agent encounters a sub-problem requiring deep mathematical reasoning or sandboxed data processing, it yields execution to a specialized sub-agent with its own prompt instructions and restricted tool subset.

```
+-----------------------------------------------------------------------------------+
|                        MULTI-AGENT HANDOFF FLOW CHART                             |
+-----------------------------------------------------------------------------------+
  User Input --> Primary Orchestration Agent (GPT-5.6)
                       |
                       +---> Complex Code Requirement? ---> Sandboxed Python Agent
                       |                                          |
                       +---> Web Research Needed?      ---> FastMCP Search Agent
                       |                                          |
                       v                                          v
  Final Aggregated Output <-- Yield & Handoff Summary <-----------+
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Multi-step Reasoning & Task Decomposition**: High-autonomy agents utilizing O5 chain-of-thought to solve complex tasks.
- **Tool-augmented Generation**: Integrating external REST APIs and FastMCP 3.1 tools into the agentic loop.
- **Sandboxed Execution**: Running agent-generated Python or bash code in secure, isolated runtime containers.
- **Heterogeneous Workflows**: Orchestrating task handoffs across O5 reasoning models, GPT-5.5, and external Claude 5.1 bridges within a unified harness.

## Strengths
- **Decoupled Architecture**: Strictly decouples control harness logic from underlying LLM execution.
- **Native OpenAI & FastMCP 3.1 Integration**: Seamless integration with OpenAI platform features and the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) (FastMCP 3.1 specifications).
- **Scalability & State Persistence**: Native session checkpointing for long-running workflows and multi-agent coordination.
- **Security & Sandboxing**: Enterprise-grade permission management and containerized code execution.
- **Reasoning Optimization**: Specialized bindings for the **O5 reasoning series** and high-context window GPT-5.5/5.6 models.

## Limitations
- **Platform Alignment**: Deeply optimized for OpenAI models, requiring adapter layers or third-party bridges for non-OpenAI LLM provider backends.
- **Abstraction Overhead**: Harness/compute separation adds structural complexity for single-prompt script applications.
- **Ecosystem Rate Limits**: Highly autonomous O5 loops can consume large reasoning token budgets quickly if unbounded.

## When to use it
- When building production-grade agents on the OpenAI platform requiring O5 reasoning capabilities.
- When your architecture requires strict separation between agent control flow and inference compute.
- When multi-tenant isolation, sandboxed code execution, or FastMCP 3.1 protocol tool management is required.

## When not to use it
- For simple, single-prompt chat interactions or basic retrieval pipelines.
- If you are fully committed to an alternative graph-based framework like [LangGraph](./langgraph.md) or Microsoft [Semantic Kernel](./semantic-kernel.md).

## Getting started
Install the SDK and configure a basic agent with FastMCP 3.1 tools.

```bash
pip install openai-agents pydantic>=2.0.0
```

### Basic Agent Configuration
```python
from openai_agents import Agent, Tool

def get_weather(location: str):
    return f"The weather in {location} is sunny."

weather_tool = Tool(
    name="get_weather",
    func=get_weather,
    description="Get the current weather for a location"
)

agent = Agent(
    name="WeatherBot",
    model="gpt-5.5",
    instructions="You are a weather assistant utilizing FastMCP 3.1 tools.",
    tools=[weather_tool]
)
```

## Detailed Code Example: Complete Enterprise Production Harness

The following Python example demonstrates a complete enterprise-grade implementation of the OpenAI Agents SDK incorporating FastMCP 3.1 tool integration, Pydantic v2 strict configuration validation, containerized sandboxing, and multi-agent handoffs.

```python
import json
import logging
import asyncio
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("OpenAIAgentsHarness")

# --- Pydantic v2 Schema Definitions ---

class ToolParameterSchema(BaseModel):
    type: str = Field("object")
    properties: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    required: List[str] = Field(default_factory=list)

class FastMCPToolSpec(BaseModel):
    name: str = Field(..., description="Unique tool identifier")
    description: str = Field(..., description="Semantic purpose of tool")
    parameters: ToolParameterSchema = Field(default_factory=ToolParameterSchema)

class AgentComputeConfig(BaseModel):
    primary_model: str = Field("gpt-5.6", description="Primary model compute engine")
    fallback_model: str = Field("claude-5.1", description="Fallback compute engine")
    temperature: float = Field(0.0, ge=0.0, le=2.0)
    max_reasoning_tokens: int = Field(8192, gt=0)

    @field_validator("primary_model")
    @classmethod
    def validate_primary_model(cls, v: str) -> str:
        allowed = {"gpt-5.5", "gpt-5.6", "o5", "o5-max", "o5-mini"}
        if v not in allowed:
            logger.warning(f"Model '{v}' not in standard primary list. Proceeding with caution.")
        return v

class HarnessAgentConfig(BaseModel):
    agent_id: str = Field(..., description="Unique ID for agent instance")
    instructions: str = Field(..., description="System instructions")
    compute: AgentComputeConfig = Field(default_factory=AgentComputeConfig)
    mcp_tools: List[FastMCPToolSpec] = Field(default_factory=list)
    enable_sandbox: bool = Field(True, description="Enforce sandboxed execution")

# --- FastMCP 3.1 & Agent Harness Implementation ---

class MockFastMCPServer:
    """Simulates an external FastMCP 3.1 protocol tool provider."""
    @staticmethod
    async def call_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"[FastMCP 3.1] Executing tool '{tool_name}' with args: {arguments}")
        if tool_name == "sql_query_executor":
            return {"status": "success", "rows_returned": 42, "data": [{"id": 1, "status": "active"}]}
        elif tool_name == "code_sandbox_run":
            return {"status": "success", "stdout": "Execution completed in 12ms", "exit_code": 0}
        return {"status": "error", "message": f"Unknown tool: {tool_name}"}

class OpenAIHarnessRuntime:
    def __init__(self, config: HarnessAgentConfig):
        self.config = config
        self.mcp_client = MockFastMCPServer()
        self.session_state: Dict[str, Any] = {}

    async def initialize(self):
        logger.info(f"Initializing Harness for Agent '{self.config.agent_id}'")
        logger.info(f"Compute Engine: {self.config.compute.primary_model} (Fallback: {self.config.compute.fallback_model})")
        logger.info(f"Loaded FastMCP Tools: {[t.name for t in self.config.mcp_tools]}")
        if self.config.enable_sandbox:
            logger.info(" gVisor Code Sandbox Runtime initialized & attached.")

    async def run_step(self, user_prompt: str) -> Dict[str, Any]:
        logger.info(f"Executing step for prompt: '{user_prompt}'")

        # Simulate agent reasoning and decision to call FastMCP tool
        if "sql" in user_prompt.lower():
            mcp_res = await self.mcp_client.call_tool(
                "sql_query_executor",
                {"query": "SELECT * FROM users WHERE status='active'"}
            )
            self.session_state["last_tool_output"] = mcp_res
            return {
                "agent_id": self.config.agent_id,
                "status": "completed",
                "response": f"Query returned {mcp_res['rows_returned']} records.",
                "state": self.session_state
            }

        return {
            "agent_id": self.config.agent_id,
            "status": "completed",
            "response": "Processed request without tool invocation.",
            "state": self.session_state
        }

# --- Demonstration Execution ---

async def main():
    raw_config_json = """
    {
        "agent_id": "EnterpriseDataAnalyst_01",
        "instructions": "You are an autonomous data analysis agent.",
        "compute": {
            "primary_model": "gpt-5.6",
            "fallback_model": "claude-5.1",
            "temperature": 0.1,
            "max_reasoning_tokens": 16384
        },
        "mcp_tools": [
            {
                "name": "sql_query_executor",
                "description": "Execute validated SQL read queries against enterprise database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"}
                    },
                    "required": ["query"]
                }
            }
        ],
        "enable_sandbox": true
    }
    """

    try:
        validated_config = HarnessAgentConfig.model_validate_json(raw_config_json)
        harness = OpenAIHarnessRuntime(validated_config)
        await harness.initialize()

        output = await harness.run_step("Execute SQL analysis on user retention")
        print("\n--- Final Step Output ---")
        print(json.dumps(output, indent=2))

    except ValidationError as e:
        logger.error(f"Configuration validation failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## CLI examples
The SDK includes a CLI for managing and testing agent deployments.

```bash
# Initialize a new agent project
openai-agents init my-agent

# Run an agent in interactive mode
openai-agents run --agent WeatherBot

# List active agent harnesses
openai-agents harness list

# Check SDK version and health
openai-agents --version
```

## API examples
The SDK provides advanced patterns for resource separation, sandboxing, and orchestration.

### Harness vs. Compute Validation with Pydantic v2
This example demonstrates configuring and validating compute configurations and tool interfaces prior to starting the OpenAI Agents harness loop.

```python
import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ValidationError

# Define Pydantic v2 models for validation
class ToolDefinitionSchema(BaseModel):
    name: str = Field(..., description="Unique tool identifier")
    description: str = Field(..., description="Semantic explanation of tool function")
    parameters_schema: Dict[str, Any] = Field(..., alias="parametersSchema", description="Zod or JSON schema of tool parameters")

class ComputeConfigSchema(BaseModel):
    model: str = Field("gpt-5.5", description="Target OpenAI model, e.g., gpt-5.5, gpt-5.6, or o5-mini")
    temperature: float = Field(0.1, ge=0.0, le=2.0)
    max_tokens: int = Field(2000, gt=0)

class AgentHarnessSchema(BaseModel):
    agent_name: str = Field(..., alias="agentName")
    compute_config: ComputeConfigSchema = Field(..., alias="computeConfig")
    tools: List[ToolDefinitionSchema] = Field(default_factory=list)

def validate_and_launch_harness(raw_json: str) -> Optional[AgentHarnessSchema]:
    try:
        # Validate JSON config using Pydantic v2 model_validate_json
        validated_harness = AgentHarnessSchema.model_validate_json(raw_json)
        print(f"Harness validation successful for: {validated_harness.agent_name}")
        print(f"Launching model: {validated_harness.compute_config.model}")
        return validated_harness
    except ValidationError as e:
        print(f"Harness configuration is invalid: {e.errors()}")
        return None

# Validating a GPT-5.5 high autonomy agent configuration
config_payload = """
{
    "agentName": "ResearchHarnessAgent",
    "computeConfig": {
        "model": "gpt-5.5",
        "temperature": 0.0,
        "max_tokens": 4096
    },
    "tools": [
        {
            "name": "fetch_mcp_docs",
            "description": "Fetch FastMCP 3.1 specifications",
            "parametersSchema": {
                "type": "object",
                "properties": {
                    "section": {"type": "string"}
                },
                "required": ["section"]
            }
        }
    ]
}
"""

validated_config = validate_and_launch_harness(config_payload)
```

### Sandboxed Tool Execution
```python
from openai_agents import Sandbox

sandbox = Sandbox(
    image="python:3.12-slim",
    allow_network=True
)

agent.register_sandbox(sandbox)
response = agent.run("Calculate the Fibonacci sequence up to 100.")
```

### Multi-Agent Orchestration
```python
from openai_agents import Orchestrator

researcher = Agent(name="Researcher", ...)
writer = Agent(name="Writer", ...)

orchestrator = Orchestrator(agents=[researcher, writer])
final_report = orchestrator.run("Research and write a report on FastMCP 3.1 specifications.")
```

## Related tools / concepts
- [Symphony (OpenAI)](../agents/symphony.md) — Multi-agent framework.
- [LangGraph](./langgraph.md) — Cyclic agent graphs.
- [CrewAI](./crewai.md) — Collaborative agent framework.
- [Agency Swarm](../agents/agency-swarm.md) — Collaborative agents.
- [Agentic Automation Canvas (AAC)](../agents/agentic-automation-canvas.md) — Design framework.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standardized tool-calling (FastMCP 3.1 support).
- [OpenHands](../development_ops/openhands.md) — Engineering agent.
- [AutoGen](./autogen.md) — Conversational agent framework.

## Sources / References
- [The next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk)
- [OpenAI’s Agents SDK separates the harness from the compute](https://thenewstack.io/openai-agents-sdk-sandboxes/)
- [Agents SDK Sandboxes](https://www.zdnet.com/article/openai-agents-sdk-sandboxes/)
- **Licensing**: Open-source SDK (MIT).

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
