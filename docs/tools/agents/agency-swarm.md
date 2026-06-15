# Agency Swarm

## What it is
Agency Swarm is a multi-agent orchestration framework built on top of the OpenAI Assistants API. It allows you to create "Agencies" where specialized agents (like a CEO, Developer, or Researcher) communicate and collaborate to solve complex tasks. In June 2026, it remains the primary choice for developers heavily invested in the OpenAI ecosystem for building structured multi-agent systems.

## What problem it solves
It simplifies the creation of multi-agent systems by providing a structured way for agents to communicate via a "send_message" tool and by leveraging OpenAI's managed infrastructure for threads, files, and state management. It solves the complexity of manually managing conversation history and tool-calling loops between multiple specialized agents.

## Where it fits in the stack
[Layer 6: Agents & Orchestration](../../knowledge_base/ai_tooling_landscape.md#layer-6-agents-orchestration) — A high-level orchestration layer for multi-agent collaboration using the OpenAI Assistants API.

## Typical use cases
- **Automated software development agencies**: Defining roles for requirement analysis, coding (Developer), and testing (QA).
- **Enterprise-grade content teams**: Orchestrating agents for research, drafting, and multi-platform distribution.
- **Complex business process automation**: Managing workflows that require coordination between multiple departmental agents (e.g., Sales <-> Legal <-> Finance).

## Strengths
- **Organizational Structure**: Designed around real-world agency roles, making it intuitive to design and visualize agent teams.
- **Managed State**: Leverages OpenAI Assistants API for thread management, persistence, and vector store integration.
- **Type-Safe Tools**: Built-in support for Pydantic-based tool definitions, ensuring robust data validation for tool calls.
- **Simplified Communication**: Provides a high-level API for agent-to-agent messaging without manual prompt engineering.

## Limitations
- **Provider Lock-in**: Primarily tied to OpenAI's Assistants API, making it difficult to switch to other providers like Anthropic.
- **Cost**: Depends on OpenAI Assistant pricing (including token costs and storage fees), which can be higher than raw chat completions for high-volume use.
- **Latency**: The overhead of the Assistants API and the "send_message" tool-call loop can result in higher latency compared to lightweight alternatives.

## When to use it
- When you want to build a "company" of agents with clear roles and communication paths.
- If you prefer using OpenAI's managed infrastructure for assistant state and vector storage.
- For projects where the structure and ease of development outweigh the need for provider agnosticism.

## When not to use it
- If you need a provider-agnostic framework (consider [CrewAI](../frameworks/crewai.md) or [LangGraph](../frameworks/langgraph.md)).
- For very low-latency requirements or applications where minimizing token overhead is the primary constraint.

## Getting started
### Installation
```bash
pip install agency-swarm
```

### Basic Usage
```python
from agency_swarm import Agent, Agency, set_openai_key

set_openai_key("YOUR_API_KEY")

# 1. Define specialized agents
ceo = Agent(name="CEO",
            description="Responsible for coordinating the agency.",
            instructions="Direct the developer to complete coding tasks.")

developer = Agent(name="Developer",
                 description="Responsible for writing and debugging code.",
                 instructions="Provide implementation for requested features.")

# 2. Create the agency (Communication: CEO <-> Developer)
agency = Agency([ceo, [ceo, developer]],
                shared_instructions="Collaborate to build high-quality software.")

# 3. Run a query
response = agency.get_completion("CEO, please ask the developer to implement a FastAPI endpoint.")
print(response)
```

## CLI examples
```bash
# Create a new agency project structure
agency-swarm create-space --name my_agency

# Run a specific agent within your agency (manual execution)
python -m my_agency.run_agent --agent_name CEO

# List all available tools in your current agency space
python -m my_agency.list_tools
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
- [OpenAI Assistants](../ai_knowledge/openai.md)
- [Agent Protocols (MCP)](../../knowledge_base/agent_protocols.md)
- [CrewAI](../frameworks/crewai.md)
- [LangGraph](../frameworks/langgraph.md)
- [Agno](agno.md)
- [Phidata](phidata.md)
- [Composio](composio.md)

## Sources / references
- [GitHub Repository](https://github.com/VRSEN/agency-swarm)
- [Official Website](https://agency-swarm.ai/)
- [Documentation](https://vrsen.github.io/agency-swarm/)

## Contribution Metadata
- Last reviewed: 2026-06-15
- Confidence: high
