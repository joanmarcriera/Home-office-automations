# OpenAI Agents SDK

## What it is
The OpenAI Agents SDK is a framework designed to build and orchestrate AI agents. It introduces a separation between the "harness" (the control logic) and the "compute" (the LLM reasoning), allowing for more flexible and scalable agent architectures. By July 2026, it has become a standard for deploying high-autonomy agents, often compared against **Gemma 3** based agentic workflows for cross-platform versatility.

## What problem it solves
It simplifies the process of creating agents that can use tools, maintain state, and perform complex multi-step tasks. By separating the harness from the compute, it enables better resource management, sandboxed execution, and multi-tenant scaling, solving the security and reliability challenges of early autonomous agent implementations.

## Where it fits in the stack
**Category**: [Frameworks](./index.md) / [Agents](../agents/index.md). It acts as the orchestration layer for **GPT-5.5** and the **O4 reasoning series**, while supporting the **MCP 3.0 Task Protocol** for standardized tool execution.

## Typical use cases
- **Multi-step Reasoning**: Agents that need to perform a sequence of actions to reach a goal.
- **Tool-augmented Generation**: Integrating external APIs and tools into the agentic loop.
- **Sandboxed Execution**: Running agent code in isolated environments for security.
- **Heterogeneous Workflows**: Orchestrating different model sizes or providers within a single task harness.

## Strengths
- **Decoupled Architecture**: Separates agent logic (harness) from LLM execution (compute).
- **Native OpenAI Integration**: Designed to work seamlessly with the OpenAI platform and the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md).
- **Scalability**: Easier to manage multiple agents and concurrent tasks.
- **Security-First**: Built-in support for sandboxing and permission management.
- **Autonomous Excellence**: Optimized for high-autonomy tasks using the **O4 series**.

## Limitations
- **Platform Dependency**: Primarily optimized for OpenAI models, though Gemma 3 integrations are emerging via third-party bridges.
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
pip install openai-agents
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

### Harness vs. Compute Separation
```python
from openai_agents import Harness, Compute

compute = Compute(
    model="gpt-5.5-preview",
    temperature=0.1,
    max_tokens=2000
)

harness = Harness(
    agent=agent,
    compute=compute
)

result = harness.run("What's the weather in London?")
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
final_report = orchestrator.run("Research and write a report on MCP.")
```

## Related tools / concepts
- [Symphony (OpenAI)](../agents/symphony.md) — Multi-agent framework.
- [LangGraph](./langgraph.md) — Cyclic agent graphs.
- [CrewAI](./crewai.md) — Collaborative agent framework.
- [Agency Swarm](../agents/agency-swarm.md) — Collaborative agents.
- [Agentic Automation Canvas (AAC)](../agents/agentic-automation-canvas.md) — Design framework.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standardized tool-calling.
- [OpenHands](../development_ops/openhands.md) — Engineering agent.
- [AutoGen](./autogen.md) — Conversational agent framework.

## Sources / References
- [The next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk)
- [OpenAI’s Agents SDK separates the harness from the compute](https://thenewstack.io/openai-agents-sdk-sandboxes/)
- [Agents SDK Sandboxes](https://www.zdnet.com/article/openai-agents-sdk-sandboxes/)
- **Licensing**: Open-source SDK (MIT).

## Contribution Metadata
- Last reviewed: 2026-07-05
- Confidence: high
