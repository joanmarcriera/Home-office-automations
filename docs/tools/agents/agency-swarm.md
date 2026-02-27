# Agency Swarm

## What it is
Agency Swarm is a multi-agent orchestration framework built on top of the OpenAI Assistants API. It allows you to create "Agencies" where specialized agents (like a CEO, Developer, or Researcher) communicate and collaborate to solve complex tasks.

## What problem it solves
It simplifies the creation of multi-agent systems by providing a structured way for agents to communicate via a "send_message" tool and by leveraging OpenAI's managed infrastructure for threads and files.

## Where it fits in the stack
[Framework / Agent / Orchestration] - A high-level orchestration layer for multi-agent collaboration using the OpenAI ecosystem.

## Typical use cases
- Automated software development agencies
- Marketing and content creation teams
- Complex business process automation

## Strengths
- **Organizational Structure**: Designed around real-world agency roles, making it intuitive to design teams.
- **Managed State**: Leverages OpenAI Assistants API for thread management and persistence.
- **Type-Safe Tools**: Built-in support for Pydantic-based tool definitions.

## Limitations
- **Provider Lock-in**: Primarily tied to OpenAI's Assistants API.
- **Cost**: Depends on OpenAI Assistant pricing, which can be higher than raw chat completions for high-volume use.

## When to use it
- When you want to build a "company" of agents with clear roles and communication paths.
- If you prefer using OpenAI's managed infrastructure for assistant state.

## When not to use it
- If you need a provider-agnostic framework (consider CrewAI or LangGraph).
- For very low-latency requirements (Assistants API can have overhead).

## Getting started
### Installation
```bash
pip install agency-swarm
```

### Working Example
```python
from agency_swarm import Agent, Agency, set_openai_key

set_openai_key("YOUR_API_KEY")

# Define specialized agents
ceo = Agent(name="CEO",
            description="Responsible for coordinating the agency.",
            instructions="Direct the developer to complete tasks.")

developer = Agent(name="Developer",
                 description="Responsible for writing code.",
                 instructions="Write code based on CEO's instructions.")

# Create the agency
agency = Agency([ceo, [ceo, developer]],
                shared_instructions="Work together to build a hello world script.")

# Run a query
agency.get_completion("CEO, please ask the developer to write a Python hello world script.")
```

## Licensing and cost
- **Open Source**: Yes (MIT License)
- **Cost**: Free (Framework) / Paid (OpenAI API usage)
- **Self-hostable**: Yes (The framework itself)

## Related tools / concepts
- [OpenAI](../ai_knowledge/openai.md)
- [Agent Protocols](../../knowledge_base/agent_protocols.md)
- [CrewAI](../frameworks/crewai.md)

## Sources / References
- [GitHub Repository](https://github.com/VRSEN/agency-swarm)
- [Official Website](https://agency-swarm.ai/)

## Contribution Metadata
- Last reviewed: 2026-02-27
- Confidence: high
