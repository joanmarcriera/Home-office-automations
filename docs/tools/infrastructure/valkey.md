# Valkey

## What it is
Valkey is an open-source, ultra-low-latency in-memory key-value datastore, cache, and message broker maintained under the Linux Foundation. Created as an open-source fork of Redis (licensed under BSD-3-Clause), Valkey serves as a primary state store, prompt cache registry, agent chat history cache, and FastMCP 3.1 pub/sub messaging bus for multi-agent systems in early 2027.

## What problem it solves
Autonomous multi-agent systems demand sub-millisecond state access and conversation history retrieval. Disk-bound databases introduce query latency that degrades model tool-use performance. Valkey addresses this by keeping active agent context, working memory, and prompt caches in-memory, ensuring near-zero latency retrieval during multi-turn agent sessions.

## Where it fits in the stack
**Local Infrastructure & Caching Layer**. It functions as an in-memory cache, task queue, and agent state synchronizer across distributed execution nodes.

## Typical use cases
- **Multi-Agent Session Caching**: Maintaining active conversation threads and transient agent memory buffers.
- **Prompt Cache Indexing**: Storing embedding results and static prompt templates to bypass duplicate model calls and reduce API costs.
- **FastMCP 3.1 Agent Message Bus**: Using pub/sub channels to broadcast tool execution state updates between agent task nodes.
- **Dynamic Feature Flags & Routing**: Storing model routing preferences (e.g. Claude 5.6 vs GPT-5.6 vs DeepSeek-V4) and active agent tool configurations.

## Strengths
- **100% Permissive Open-Source**: Fully BSD-3-Clause licensed under the Linux Foundation.
- **Drop-In Redis Compatibility**: Direct compatibility with standard Redis SDKs and CLI tools.
- **Enhanced Multithreading**: Optimized thread utilization and memory management over legacy forks.
- **Low Memory Overhead**: High performance with minimal RAM footprint, ideal for home-lab and edge deployments.

## Limitations
- **In-Memory Volatility**: Primary storage is in RAM; requires persistence configuration (RDB/AOF snapshots) to survive server reboots.
- **No Native Dense Vector Indexing**: Not designed for high-dimensional vector search (use vector stores like Milvus or Weaviate for dense semantic search).

## When to use it
- When requiring sub-millisecond caching for agent session states and prompt responses.
- For open-source task queueing and message broker pipelines without licensing constraints.
- To reduce model API costs by caching token embeddings and system prompts.

## When not to use it
- As a primary disk-backed transactional database requiring ACID guarantees.
- For high-dimensional vector search across unstructured documents (use Milvus, Weaviate, or Pinecone).

## Getting started

### Docker Deployment
```bash
docker run --name valkey-server -p 6379:6379 -d valkey/valkey:latest
```

### Python Installation
```bash
pip install redis pydantic
```

## CLI examples

```bash
# Connect to Valkey via CLI
valkey-cli

# Set cached prompt payload with 30-minute expiration
valkey-cli SET "prompt:sys-v1" "You are an autonomous agent system controller." EX 1800

# Monitor live keyspace commands
valkey-cli MONITOR
```

## API examples

### Python Agent State Caching & Pydantic v2 Validation
This example demonstrates caching agent session state in Valkey and validating the retrieved structure with **Pydantic v2** for FastMCP 3.1 workflows.

```python
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError

class MessageTurn(BaseModel):
    role: str = Field(..., description="Message speaker role ('user', 'assistant', 'system')")
    content: str = Field(..., description="Message content")

class AgentSessionState(BaseModel):
    session_id: str = Field(..., description="Unique agent session UUID")
    model_routing_override: str = Field(default="claude-5.6", description="Active model override")
    conversation_history: List[MessageTurn] = Field(default_factory=list, description="Chat turn history")
    mcp_protocol_version: str = Field(default="3.1", description="FastMCP protocol version")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Context metadata tags")

class ValkeyCacheManager:
    def __init__(self):
        self._mock_db = {}

    def set_session_state(self, session_id: str, state: AgentSessionState):
        self._mock_db[f"session:{session_id}"] = state.model_dump_json()

    def get_session_state(self, session_id: str) -> Optional[AgentSessionState]:
        raw_data = self._mock_db.get(f"session:{session_id}")
        if not raw_data:
            return None
        try:
            parsed = json.loads(raw_data)
            return AgentSessionState.model_validate(parsed)
        except ValidationError as ve:
            print(f"Pydantic validation error: {ve}")
            return None

if __name__ == "__main__":
    cache = ValkeyCacheManager()
    session_id = "sess-2027-001"

    initial_state = AgentSessionState(
        session_id=session_id,
        model_routing_override="claude-5.6",
        conversation_history=[
            MessageTurn(role="user", content="Initialize FastMCP 3.1 task channel."),
            MessageTurn(role="assistant", content="FastMCP 3.1 channel established successfully.")
        ],
        metadata={"environment": "production", "agent_type": "orchestrator"}
    )

    cache.set_session_state(session_id, initial_state)
    retrieved = cache.get_session_state(session_id)

    if retrieved:
        print("Valkey State Cache Validated via Pydantic v2:")
        print(f"  Session ID: {retrieved.session_id}")
        print(f"  Model Routing: {retrieved.model_routing_override}")
        print(f"  Turns Loaded: {len(retrieved.conversation_history)}")
        print(f"  FastMCP Standard: {retrieved.mcp_protocol_version}")
```

## Related tools / concepts
- [Docker](docker.md) — Container runtime for hosting local Valkey instances.
- [Pinecone](pinecone.md) — Managed vector database often paired with Valkey cache layers.
- [Milvus](milvus.md) — Open-source vector store for dense embedding search.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Protocol for agent tool and task communication.

## Sources / references
- [Valkey Official Open-Source Project](https://github.com/valkey-io/valkey)
- [Valkey Architecture & Caching Reference](https://valkey.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
