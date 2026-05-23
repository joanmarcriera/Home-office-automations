# OpenAI Agents SDK

## What it is
The OpenAI Agents SDK is a framework designed to build and orchestrate AI agents. It introduces a separation between the "harness" (the control logic) and the "compute" (the LLM reasoning), allowing for more flexible and scalable agent architectures.

## What problem it solves
It simplifies the process of creating agents that can use tools, maintain state, and perform complex multi-step tasks. By separating the harness from the compute, it enables better resource management, sandboxed execution, and multi-tenant scaling.

## Where it fits in the stack
**Category**: [Frameworks](./index.md) / [Agents](../agents/index.md)

## Typical use cases
- **Multi-step Reasoning**: Agents that need to perform a sequence of actions to reach a goal.
- **Tool-augmented Generation**: Integrating external APIs and tools into the agentic loop.
- **Sandboxed Execution**: Running agent code in isolated environments for security.
- **Heterogeneous Workflows**: Orchestrating different model sizes or providers within a single task harness.

## Strengths
- **Decoupled Architecture**: Separates agent logic (harness) from LLM execution (compute).
- **Native OpenAI Integration**: Designed to work seamlessly with the OpenAI platform.
- **Scalability**: Easier to manage multiple agents and concurrent tasks.
- **Security-First**: Built-in support for sandboxing and permission management.

## Limitations
- **Platform Dependency**: Primarily optimized for OpenAI models.
- **Early Stage**: As a new evolution, ecosystem support and community tools are still maturing.

## When to use it
- Use when building complex agents on the OpenAI platform.
- Use when you need a clear separation between the agent's control logic and its reasoning engine.
- When multi-tenant isolation or sandboxed tool-use is a requirement.

## When not to use it
- Not necessary for simple, single-prompt chat interactions.
- If you are fully committed to a different framework like [LangGraph](./langgraph.md) or [CrewAI](./crewai.md).

## Getting started

### Installation
```bash
pip install openai-agents
```

### Basic Agent Configuration
Define an agent with a specific set of tools and a system prompt.

```python
from openai_agents import Agent, Tool

# Define a tool
def get_weather(location: str):
    return f"The weather in {location} is sunny."

weather_tool = Tool(
    name="get_weather",
    func=get_weather,
    description="Get the current weather for a location"
)

# Initialize the agent
agent = Agent(
    name="WeatherBot",
    model="gpt-4o",
    instructions="You are a weather assistant.",
    tools=[weather_tool]
)
```

## API: Harness vs. Compute Separation
The SDK allows you to define the "harness" (logic) separately from the "compute" (the actual LLM call), enabling more granular control over resource allocation.

```python
from openai_agents import Harness, Compute

# Define the compute configuration
compute = Compute(
    model="gpt-4o",
    temperature=0.1,
    max_tokens=500
)

# Define the harness
harness = Harness(
    agent=agent,
    compute=compute
)

# Execute a task
result = harness.run("What's the weather in London?")
print(result.output)
```

## API: Sandboxed Tool Execution
For security, the SDK supports running tool-calling logic in an isolated sandbox.

```python
from openai_agents import Sandbox

# Define a sandbox for tool execution
sandbox = Sandbox(
    image="python:3.11-slim",
    allow_network=True
)

# Register the agent with the sandbox
agent.register_sandbox(sandbox)

# When the agent calls a tool, it executes within the isolated environment
response = agent.run("Calculate the Fibonacci sequence up to 100.")
```

## Multi-Agent Orchestration
The SDK provides patterns for handovers between different specialized agents.

```python
from openai_agents import Orchestrator

# Define specialized agents
researcher = Agent(name="Researcher", ...)
writer = Agent(name="Writer", ...)

# Initialize orchestrator
orchestrator = Orchestrator(agents=[researcher, writer])

# The orchestrator manages handovers and context sharing
final_report = orchestrator.run("Research and write a report on MCP.")
```

## Licensing and cost
- **Open Source**: Yes (SDK)
- **Cost**: Free (SDK) / Usage-based (OpenAI API)
- **Self-hostable**: Yes (SDK logic)

## Related tools / concepts
- [Symphony (OpenAI)](../agents/symphony.md)
- [LangGraph](./langgraph.md)
- [Agency Swarm](../agents/agency-swarm.md)
- [Agentic Automation Canvas (AAC)](../agents/agentic-automation-canvas.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [OpenHands](../development_ops/openhands.md)
- [AutoGen](./autogen.md)

## Sources / References
- [The next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk)
- [OpenAI’s Agents SDK separates the harness from the compute](https://thenewstack.io/openai-agents-sdk-sandboxes/)
- [Agents SDK Sandboxes](https://www.zdnet.com/article/openai-agents-sdk-sandboxes/)

## Contribution Metadata
- Last reviewed: 2026-05-23
- Confidence: high
