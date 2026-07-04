# Agency Swarm

## What it is
Agency Swarm is a multi-agent orchestration framework that simplifies the creation of collaborative agent teams. While originally built on the OpenAI Assistants API, by July 2026 it has evolved into a provider-agnostic system with first-class support for local deployments using **Gemma 3** and **Llama 4**. It utilizes the **FastMCP 3.0** protocol for high-performance tool communication and agent discovery.

## What problem it solves
It simplifies the creation of multi-agent systems by providing a structured way for agents to communicate via a "send_message" tool. It solves the complexity of manually managing conversation history, role-playing, and tool-calling loops between multiple specialized agents, while now enabling low-latency, privacy-preserving local swarms.

## Where it fits in the stack
[Layer 6: Agents & Orchestration](../../knowledge_base/ai_tooling_landscape.md#layer-6-agents-orchestration) — A high-level orchestration layer for multi-agent collaboration, supporting both managed cloud services and local-first execution.

## Typical use cases
- **Automated software development agencies**: Defining roles for requirement analysis, coding (Developer), and testing (QA).
- **Enterprise-grade content teams**: Orchestrating agents for research, drafting, and multi-platform distribution.
- **Local-first Research Swarms**: Deploying a team of [Gemma 3](../ai_knowledge/local_llms.md) agents on-premise to analyze sensitive data.
- **Complex business process automation**: Managing workflows that require coordination between multiple departmental agents.

## Strengths
- **Organizational Structure**: Designed around real-world agency roles, making it intuitive to design and visualize agent teams.
- **Local Execution**: Optimized for high-performance local swarms using [Gemma 3](../ai_knowledge/local_llms.md) and [FastMCP](../automation_orchestration/mcp.md).
- **Type-Safe Tools**: Built-in support for Pydantic-based tool definitions, ensuring robust data validation for tool calls.
- **FastMCP 3.0 Support**: Implements the latest Task Protocol for standardized tool hosting and agent discovery.

## Limitations
- **Orchestration Overhead**: The structured communication loop can introduce slight latency compared to raw prompt-based chaining.
- **Complexity**: Setting up a large agency with many agents requires careful design of communication paths to avoid "agent loops."
- **Local Hardware Requirements**: Running a full swarm of [Gemma 3](../ai_knowledge/local_llms.md) agents locally requires significant VRAM resources.

## When to use it
- When you want to build a "company" of agents with clear roles and communication paths.
- For projects requiring both cloud-based power ([GPT-5.5](../ai_knowledge/chatgpt.md)) and local-first privacy.
- If you need a framework that provides high-level abstractions for agent-to-agent messaging.

## When not to use it
- For very low-latency requirements where a single, simple agent loop is sufficient.
- When minimizing token overhead is the primary constraint and you prefer raw chat completions.
- For simple, stateless tasks that don't benefit from multi-agent collaboration.

## Getting started
### Installation
```bash
pip install agency-swarm
```

### Basic Usage (Local Gemma 3 Swarm)
```python
from agency_swarm import Agent, Agency, set_model

# 1. Configure for local Gemma 3 via FastMCP
set_model("gemma3-27b", provider="ollama")

# 2. Define specialized agents
ceo = Agent(name="CEO",
            description="Responsible for coordinating the agency.",
            instructions="Direct the developer to complete coding tasks.")

developer = Agent(name="Developer",
                 description="Responsible for writing and debugging code.",
                 instructions="Provide implementation for requested features.")

# 3. Create the agency (Communication: CEO <-> Developer)
agency = Agency([ceo, [ceo, developer]],
                shared_instructions="Collaborate to build high-quality software.")

# 4. Run a query
response = agency.get_completion("CEO, please ask the developer to implement a FastAPI endpoint.")
print(response)
```

## CLI examples
```bash
# Create a new agency project structure
agency-swarm create-space --name my_agency

# Run a specific agent within your agency (manual execution)
python -m my_agency.run_agent --agent_name CEO

# List all available FastMCP tools in your current agency space
python -m my_agency.list_tools --protocol fastmcp
```

## API examples
```python
from agency_swarm import Agent, BaseTool
from pydantic import Field

# Define a Pydantic-based tool for the agent
class GitHubIssueTool(BaseTool):
    """Create a new issue on GitHub."""
    title: str = Field(..., description="The title of the issue.")
    body: str = Field(..., description="The detailed description.")

    def run(self):
        # Implementation logic to call GitHub API
        return f"Issue '{self.title}' created successfully."

# Instantiate agent with tools
developer = Agent(
    name="Developer",
    tools=[GitHubIssueTool],
    instructions="Use the GitHubIssueTool to document bugs or features."
)
```

## Related tools / concepts
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [CrewAI](../frameworks/crewai.md)
- [LangGraph](../frameworks/langgraph.md)
- [Agno](./agno.md)
- [Phidata](./phidata.md)
- [Composio](./composio.md)
- [Gemma 3](../ai_knowledge/local_llms.md)
- [Claude](../ai_knowledge/claude.md)

## Sources / references
- [GitHub Repository](https://github.com/VRSEN/agency-swarm)
- [Official Website](https://agency-swarm.ai/)
- [Documentation](https://vrsen.github.io/agency-swarm/)
- [FastMCP Integration Guide](https://vrsen.github.io/agency-swarm/fastmcp)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
