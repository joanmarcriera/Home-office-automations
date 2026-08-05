# Letta

## What it is
Letta (v1.12.x+, late November 2026) is a framework for creating stateful AI agents with "infinite" memory. It manages memory as a tiered system (long-term, short-term) to overcome LLM context window limits by treating the context window as a "cache" for a larger, persistent memory store, now natively supporting the **MCP 3.1 Task Protocol** for tool and context orchestration.

## What problem it solves
Standard LLMs suffer from "forgetfulness" once their context window is exceeded. Letta enables long-lived agents that remember past interactions, user preferences, and project details over extended periods. It specifically solves the state management problem in autonomous, multi-session agentic workflows where context must persist across system restarts or model switches (e.g., transitioning from [Claude 5.1](../providers/anthropic.md) to GPT-5.5 or [Gemma 3](../ai_knowledge/local_llms.md)).

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
- **MCP 3.1 Support**: Native integration for the **MCP 3.1 Task Protocol**, enabling agents to use standardized tools and context sources.

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

### Example: Basic Letta Client Usage
```python
from letta import create_client

client = create_client()

# Create a stateful agent with persistent memory
agent = client.create_agent(
    name="DurableAssistant",
    memory_type="base_memory",
    embedding_config={"model": "text-embedding-3-small"}
)
```

### Example: Pydantic v2 Core Memory and State Validation
To guarantee structural integrity and type-safe state transitions within Letta's "Virtual Context" layer, developers utilize **Pydantic v2** models to marshal and parse agent memory block schemas programmatically.

```python
import sys
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, field_validator

# Define Pydantic v2 memory block structures
class MemoryBlock(BaseModel):
    block_type: str = Field(..., description="Memory classification, e.g., CORE, ARCHIVAL, RECENT")
    content: str = Field(..., min_length=1, description="Textual context content")
    updated_at: str = Field(..., description="Timestamp of the last modification (ISO format)")

class LettaAgentState(BaseModel):
    agent_id: str
    model_name: str
    memory: List[MemoryBlock]
    system_tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, str] = Field(default_factory=dict)

    @field_validator('memory')
    @classmethod
    def verify_core_block_exists(cls, memory_list: List[MemoryBlock]) -> List[MemoryBlock]:
        # Validate that at least one 'core' memory block exists for stateful reasoning
        has_core = any(b.block_type.upper() == 'CORE' for b in memory_list)
        if not has_core:
            raise ValueError("Letta agents must contain at least one CORE memory block to persist state.")
        return memory_list

def load_and_validate_letta_state(raw_json: str) -> Optional[LettaAgentState]:
    try:
        validated_state = LettaAgentState.model_validate_json(raw_json)
        print(f"Letta state successfully validated for Agent ID: {validated_state.agent_id}")
        print(f"Target model: {validated_state.model_name}")
        for block in validated_state.memory:
            print(f" - [{block.block_type}] -> {block.content[:40]}...")
        return validated_state
    except Exception as e:
        print(f"Letta agent state validation failed: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    print("Initializing Letta Virtual Context state validation (Pydantic v2)...")

    # Valid raw JSON state containing a core memory block
    valid_state_json = """
    {
        "agent_id": "letta-agent-99x",
        "model_name": "claude-5.1-sonnet",
        "memory": [
            {"block_type": "CORE", "content": "User prefers python over javascript, and uses Pydantic v2.", "updated_at": "2026-11-27T10:00:00Z"},
            {"block_type": "RECENT", "content": "Discussed FastMCP 3.1 configuration.", "updated_at": "2026-11-27T10:05:00Z"}
        ],
        "system_tags": ["developer", "strict-types"]
    }
    """

    load_and_validate_letta_state(valid_state_json)
```

## Related tools / concepts
- [Mem0](mem0.md)
- [Gemma 3](../ai_knowledge/local_llms.md)
- [Agno](agno.md)
- [Phidata](phidata.md)
- [LangGraph](../frameworks/langgraph.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [RAG Pattern](../../knowledge_base/patterns/rag.md)
- [MCP 3.1](../../knowledge_base/patterns/data-copilot-mcp-tooling.md)
- [DeepSeek R1](../ai_knowledge/deepseek-r1.md)

## Sources / references
- [Letta Official Site](https://www.letta.com/)
- [Letta GitHub](https://github.com/letta-ai/letta)
- [Official Documentation](https://docs.letta.com/)

## Contribution Metadata
- Last reviewed: 2026-11-27
- Confidence: high
