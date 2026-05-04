# Letta

## What it is
Letta (formerly MemGPT) is a framework for creating stateful AI agents with "infinite" memory. It manages memory as a tiered system (long-term, short-term) to overcome LLM context window limits by treating the context window as a "cache" for a larger, persistent memory store.

## What problem it solves
Standard LLMs suffer from "forgetfulness" once their context window is exceeded. Letta enables long-lived agents that remember past interactions, user preferences, and project details over extended periods, making them suitable for personal assistants and complex, multi-session software engineering.

## Where it fits in the stack
**Category**: Agent / Memory Layer

## Typical use cases
- **Persistent Personal Assistants**: Agents that remember months of conversation history and preferences.
- **Multi-session Coding Projects**: Agents that maintain state across different days of development.
- **Interactive Role-playing**: Characters that maintain consistent long-term story arcs.
- **Durable Workflows**: Agents that can be paused and resumed without losing task context.

## Virtual Context Management
Letta implements a "Virtual Context" architecture inspired by operating systems:
- **Core Memory**: Fixed-size, high-priority context (e.g., current task, user bio).
- **Archival Memory**: Infinite long-term storage (vector DB) for facts and past logs.
- **Recall Memory**: Searchable history of all past interactions.
- **Memory Tiering**: The agent can explicitly move information between these tiers using tool calls.

## Strengths
- **State Persistence**: State is stored in a database (PostgreSQL by default), allowing agents to survive process restarts.
- **Infinite Context**: Automatically manages what stays in the active LLM context and what goes to long-term storage.
- **Self-Editing Memory**: Agents can be given tools to "write" to their own memory.

## Limitations
- **Latency**: Tiered memory management adds overhead to each inference step.
- **Complexity**: Setting up the server and database infrastructure is more involved than simple stateless agents.
- **Token Usage**: Managing the memory buffer requires additional tokens for system prompts and internal reasoning.

## Getting started

### Installation
```bash
pip install letta
```

### Basic usage (Local Server)
```bash
# Start the Letta server
letta server
```

### Python SDK Example
```python
from letta import create_client

client = create_client()

# Create a new agent with persistent memory
agent = client.create_agent(
    name="MemoryAgent",
    memory_type="base_memory"
)

# Send a message
response = client.user_message(
    agent_id=agent.id,
    message="Remember that my favorite color is indigo."
)

print(f"Agent Response: {response[0].text}")

# In a separate session, the agent will still remember!
```

## Related tools / concepts

- [Mem0](mem0.md)
- [Agno](agno.md)
- [Agency Swarm](agency-swarm.md)
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)

## Sources / references
- [Letta Official Site](https://www.letta.com/)
- [Letta GitHub](https://github.com/letta-ai/letta)
- [Virtual Context Management Research](https://arxiv.org/abs/2310.08560)

## Contribution Metadata
- Last reviewed: 2026-05-16
- Confidence: high
