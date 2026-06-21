# Letta

## What it is
Letta (v1.5.x+, June 2026) is a framework for creating stateful AI agents with "infinite" memory. It manages memory as a tiered system (long-term, short-term) to overcome LLM context window limits by treating the context window as a "cache" for a larger, persistent memory store, now natively supporting MCP 3.0 for tool and context orchestration.

## What problem it solves
Standard LLMs suffer from "forgetfulness" once their context window is exceeded. Letta enables long-lived agents that remember past interactions, user preferences, and project details over extended periods. It specifically solves the state management problem in autonomous, multi-session agentic workflows where context must persist across system restarts or model switches (e.g., transitioning from Claude 4.8 to GPT-5.5).

## Where it fits in the stack
**Category**: Agent / Memory Layer. It sits as a stateful middleware between the Model (Inference) layer and the Application layer, providing persistent "Virtual Context" via a database backend (PostgreSQL/VectorDB).

## Typical use cases
- **Persistent Personal Assistants**: Agents that remember months of conversation history and deep user preferences.
- **Multi-session Coding Projects**: Agents that maintain state across different days of development, tracking open bugs and architectural decisions.
- **Durable Workflows**: Complex business processes that can be paused, resumed, and handed off between different agents without losing state.
- **Agentic CRM**: Maintaining long-term records of professional interactions and relationship history.

## Strengths
- **State Persistence**: State is stored in a database, allowing agents to survive process restarts and migrate between models.
- **Infinite Context**: Automatically manages what stays in the active LLM context and what goes to long-term storage using "Virtual Context".
- **Self-Editing Memory**: Agents can be given tools to "write" to and "edit" their own core memory.
- **MCP 3.0 Support**: Native integration for Model Context Protocol, enabling agents to use standardized tools and context sources.

## Limitations
- **Latency**: Tiered memory management and database lookups add overhead to each inference step.
- **Complexity**: Setting up the server and database (PostgreSQL + pgvector) is more involved than simple stateless agents.
- **Token Usage**: Managing the memory buffer and self-reasoning about memory requires additional tokens for internal system prompts.

## When to use it
- **Long-Lived Agents**: When you need an agent to maintain personality, memory, and state over weeks or months of interaction.
- **Context-Exceeding Tasks**: When the information needed for a task (e.g., a large codebase or complex user history) exceeds the LLM's raw context window.
- **Stateful Multi-Session Work**: For engineering or research tasks that span multiple sessions and require the agent to remember where it left off.
- **Cross-Model Workflows**: When you need to maintain state while switching between different frontier models for different sub-tasks.

## When not to use it
- **Stateless Transactions**: For simple, one-off API calls or basic chatbots, the memory management overhead is unnecessary.
- **Low-Latency Requirements**: If every millisecond counts, the overhead of memory retrieval might be prohibitive.
- **Serverless/Ephemeral Deployments**: Letta requires persistent infrastructure; it is not suited for purely ephemeral serverless functions without external state.

## Getting started

### Installation
```bash
pip install letta
```

### Server Setup
Start the Letta server with a PostgreSQL backend to enable persistent memory.
```bash
letta server --backend postgres
```

### Basic Agent Creation
```bash
letta create-agent --name "DurableCoder" --model "claude-3-5-sonnet-20240620"
```

## CLI examples
```bash
# Start the interactive Letta CLI to talk to your agent
letta run --agent DurableCoder

# List all persistent agents
letta list-agents

# Export agent state for migration
letta export --agent DurableCoder --output coder_state.json

# Run a query with a specific MCP tool source
letta run --agent DurableCoder --mcp-server http://localhost:18789
```

## API examples
```python
from letta import create_client

client = create_client()

# 1. Create a stateful agent with persistent memory
agent = client.create_agent(
    name="DurableAssistant",
    memory_type="base_memory",
    embedding_config={"model": "text-embedding-3-small"}
)

# 2. Send a message that updates agent state
response = client.user_message(
    agent_id=agent.id,
    message="I prefer using 'Alpine' base images for my Dockerfiles."
)

# 3. The agent will remember this in subsequent calls
print(f"Agent Response: {response[0].text}")

# 4. Access agent's core memory
core_memory = client.get_core_memory(agent_id=agent.id)
print(f"Current Memory: {core_memory}")
```

## Related tools / concepts
- [Mem0](mem0.md)
- [Agno](agno.md)
- [Phidata](phidata.md)
- [LangGraph](../frameworks/langgraph.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md)
- [MCP 3.0](../../knowledge_base/patterns/data-copilot-mcp-tooling.md)
- [DeepSeek R1](../ai_knowledge/deepseek-r1.md)

## Sources / references
- [Letta Official Site](https://www.letta.com/)
- [Letta GitHub](https://github.com/letta-ai/letta)
- [Official Documentation](https://docs.letta.com/)

## Contribution Metadata
- Last reviewed: 2026-06-20
- Confidence: high
