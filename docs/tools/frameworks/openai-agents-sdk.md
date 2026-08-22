# OpenAI Agents SDK

## What it is
The OpenAI Agents SDK is a framework designed to build and orchestrate AI agents. It introduces a separation between the "harness" (the control logic) and the "compute" (the LLM reasoning), allowing for more flexible and scalable agent architectures. In early 2027, it serves as a primary standard for deploying high-autonomy agents, often compared against **Gemma 3** and **DeepSeek-V4** based agentic workflows for cross-platform versatility and multi-model routing.

## What problem it solves
It simplifies the process of creating agents that can use tools, maintain state, and perform complex multi-step tasks. By separating the harness from the compute, it enables better resource management, sandboxed execution, and multi-tenant scaling, solving the security and reliability challenges of early autonomous agent implementations.

## Where it fits in the stack
**Category**: [Frameworks](./index.md) / [Agents](../agents/index.md). It acts as the orchestration layer for **GPT-5.5 / 5.6** and the **O5/O6 reasoning series**, while fully supporting the **MCP 3.1 Task Protocol** and **FastMCP 3.1** for standardized tool execution.

## Typical use cases
- **Multi-step Reasoning**: Agents that need to perform a sequence of actions to reach a goal.
- **Tool-augmented Generation**: Integrating external APIs and FastMCP 3.1 tools into the agentic loop.
- **Sandboxed Execution**: Running agent code in isolated environments for security.
- **Heterogeneous Workflows**: Orchestrating different model sizes or providers within a single task harness.

## Strengths
- **Decoupled Architecture**: Separates agent logic (harness) from LLM execution (compute).
- **Native OpenAI Integration**: Designed to work seamlessly with the OpenAI platform and the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) (MCP 3.1 specifications).
- **Scalability**: Easier to manage multiple agents and concurrent tasks.
- **Security-First**: Built-in support for sandboxing and permission management.
- **Autonomous Excellence**: Optimized for high-autonomy tasks using the **O5 / O6 series**.

## Limitations
- **Platform Dependency**: Primarily optimized for OpenAI models, though Gemma 3 and DeepSeek-V4 integrations are emerging via third-party bridges.
- **Complexity**: The harness/compute separation adds a layer of abstraction that may be unnecessary for simple tasks.
- **Ecosystem Maturity**: While standard, it requires deep integration with specific OpenAI API features.

## When to use it
- Use when building complex agents on the OpenAI platform.
- Use when you need a clear separation between the agent's control logic and its reasoning engine.
- When multi-tenant isolation or sandboxed tool-use is a requirement.

## When not to use it
- Not necessary for simple, single-prompt chat interactions.
- If you are fully committed to a different framework like [LangGraph](./langgraph.md) or [CrewAI](./crewai.md).

## Getting started
Install the SDK and configure a basic agent with tools.

```bash
pip install openai-agents "pydantic>=2.0.0"
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
    model="gpt-5.6",
    instructions="You are a weather assistant.",
    tools=[weather_tool]
)
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
    model: str = Field("gpt-5.6", description="Target OpenAI model, e.g., gpt-5.6 or o6-mini")
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

# Validating a GPT-5.6 high autonomy agent configuration
config_payload = """
{
    "agentName": "ResearchHarnessAgent",
    "computeConfig": {
        "model": "gpt-5.6",
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
