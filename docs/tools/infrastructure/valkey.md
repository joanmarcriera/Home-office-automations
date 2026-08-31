# Valkey

## What it is
Valkey is an open-source, high-performance, in-memory key-value datastore, cache, and message broker. Created as a fully open-source fork of Redis under the Linux Foundation, Valkey is highly optimized for low-latency operational workloads, real-time agent state storage, FastMCP 3.1 task protocol message queues, prompt-cache registries, and pub/sub messaging patterns across multi-agent systems.

## What problem it solves
Stateful AI applications and autonomous multi-agent systems need extremely fast access to transient system variables, chat history streams, session states, and large prompt cache indexes. Storing these parameters in disk-bound relational databases introduces significant latency, degrading the responsiveness of the AI. Valkey solves this speed constraint by storing and indexing data entirely in-memory with microsecond-level latency, preventing agents from lagging during context-retrieval steps.

## Where it fits in the stack
**Local Infrastructure & Caching Layer**. It acts as a blistering-fast local data store, caching agent states and acting as a messaging pipeline for distributed worker nodes.

## Typical use cases
- **AI Agent Session Caching**: Maintaining active, multi-turn chat logs and conversational memory schemas for instant retrieval.
- **Prompt Cache Indexing**: Caching static system prompts or embedding responses to prevent redundant model calls, substantially decreasing API costs.
- **Distributed Agent Pub/Sub**: Implementing a real-time message bus to coordinate operations and distribute execution payloads among multiple agents.
- **Dynamic Feature Flags Store**: Housing real-time configuration flags, model routing preferences, and tool schemas.

## Strengths
- **100% Permissively Open-Source**: Licensed under the highly permissive BSD-3-Clause license, supported by the Linux Foundation.
- **Complete Drop-In Compatibility**: Seamless compatibility with existing Redis clients, libraries, and integrations.
- **Highly Optimized Multithreading**: Offers enhanced parallel execution pipelines and memory reclamation algorithms over legacy forks.
- **Lightweight System Footprint**: Operates with minimal system memory overhead, ideal for space-constrained home-office servers.

## Limitations
- **No Native Vector Search**: Lacks built-in high-dimensional vector search indices, requiring integration with dedicated vector databases for RAG workflows.
- **In-Memory Volatility**: Data is primarily transient; requires deliberate configuration of snapshotting (RDB) or Append-Only Files (AOF) to ensure persistence across reboots.
- **Single-Core Threading for Commands**: Maintains a single execution thread for core commands, meaning heavy, slow commands can temporarily block queue execution.

## When to use it
- When you are deploying multi-agent swarms that require sub-millisecond coordination, message sharing, or shared session states.
- As a local caching gateway to store prompt responses and lower API billing costs for LLM endpoints.
- When you need a reliable, open-source caching engine without licensing restrictions or vendor lock-in.

## When not to use it
- For permanent, long-term archival data storage where transactional ACID compliance must be guaranteed at any cost.
- As a primary vector database for high-dimensional semantic search or dense vector embeddings retrieval (use dedicated vector stores instead).
- If your home-lab or hosting servers lack sufficient physical RAM to store active, rapidly growing datasets.

## Getting started
1. **Launch with Docker**: Quickly spin up a Valkey container on your system:
   ```bash
   docker run --name local-valkey -p 6379:6379 -d valkey/valkey:latest
   ```
2. **Install Python Client**: Install standard Redis/Valkey client drivers:
   ```bash
   pip install redis
   ```
3. **Execute Basic Connection**: Establish connection and write a key:
   ```python
   import redis

   client = redis.Redis(host="localhost", port=6379, decode_responses=True)
   client.set("agent_status", "ready")
   print(client.get("agent_status"))  # Outputs: ready
   ```

## CLI examples
The Valkey CLI (valkey-cli) supports interactive cache management, transaction debugging, and live telemetry streaming.

```bash
# Connect to the local Valkey instance using the CLI
valkey-cli

# Set a cached prompt payload with an automatic 30-minute expiration limit
valkey-cli SET "prompt:system-v1" "You are a helpful home automation assistant." EX 1800

# Stream live keyspace events and command executions for debugging
valkey-cli MONITOR

# Analyze database memory usage and identify massive cache keys
valkey-cli --bigkeys
```

## API examples

### Python State-Caching with Valkey & Pydantic v2 Validation
This API example demonstrates how to cache active agent session states in Valkey, retrieve keys, and validate payloads against strict **Pydantic v2** structures.

```python
import json
from typing import List, Dict, Any
from pydantic import BaseModel, Field

# Define schema for individual conversation turns
class MessageTurn(BaseModel):
    role: str = Field(..., description="The role of the speaker, e.g., 'user' or 'assistant'")
    content: str = Field(..., description="The textual content of the message")

# Define schema for the full agent session state
class AgentSessionState(BaseModel):
    session_id: str = Field(..., description="Unique identifier for the active agent session")
    model_routing_override: str = Field(default="gpt-5.5", description="Model selected for subsequent turns")
    conversation_history: List[MessageTurn] = Field(default_factory=list, description="List of previous conversation turns")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary execution context tags")

class ValkeyCacheManager:
    """Helper class to mock or wrap Valkey connection and validation."""
    def __init__(self):
        # In a real environment, you would instantiate the client:
        # self.client = redis.Redis(host="localhost", port=6379, decode_responses=True)
        self._mock_db = {}

    def set_session_state(self, session_id: str, state: AgentSessionState, ttl_seconds: int = 3600):
        # Serialize to JSON and store in cache
        json_payload = state.model_dump_json()
        # self.client.set(f"session:{session_id}", json_payload, ex=ttl_seconds)
        self._mock_db[f"session:{session_id}"] = json_payload

    def get_session_state(self, session_id: str) -> AgentSessionState:
        # Retrieve raw string from cache
        # raw_string = self.client.get(f"session:{session_id}")
        raw_string = self._mock_db.get(f"session:{session_id}")
        if not raw_string:
            raise KeyError(f"Session state for {session_id} not found in Valkey cache.")

        # Parse and validate using Pydantic v2
        parsed_data = json.loads(raw_string)
        return AgentSessionState(**parsed_data)

if __name__ == "__main__":
    cache = ValkeyCacheManager()

    # Define initial state
    session_id = "sess-89472"
    initial_state = AgentSessionState(
        session_id=session_id,
        model_routing_override="claude-5.1",
        conversation_history=[
            MessageTurn(role="user", content="Turn on the living room lights."),
            MessageTurn(role="assistant", content="Living room lights have been set to 100% brightness.")
        ],
        metadata={"home_zone": "living_room", "source": "voice_assistant"}
    )

    # Write to Valkey Cache
    cache.set_session_state(session_id, initial_state)

    # Read and Validate from Valkey Cache
    retrieved_state = cache.get_session_state(session_id)

    print("--- Valkey State Cache Management Verified ---")
    print(f"Session ID: {retrieved_state.session_id}")
    print(f"Routing Override: {retrieved_state.model_routing_override}")
    print(f"Total Conversation Turns Loaded: {len(retrieved_state.conversation_history)}")
    print(f"Home Zone Tag: {retrieved_state.metadata.get('home_zone')}")
```

## Related tools / concepts
- [Docker](../infrastructure/docker.md) — Standard container runtime used to deploy local Valkey services.
- [Pinecone](../infrastructure/pinecone.md) — External cloud-hosted vector database; often paired with Valkey cache.
- [Chroma](../infrastructure/chroma.md) — Open-source local vector database for fast multi-modal embeddings.
- [DuckDB](../infrastructure/duckdb.md) — High-performance local analytical database; integrates with caching pipelines.
- [BeeLlama.cpp](../infrastructure/beellama-cpp.md) — Optimized local inference engine that utilizes Valkey cache structures.
- [Llama.cpp](../infrastructure/llama-cpp.md) — Foundational local model runner serving cached prompt sessions.
- [Vikunja](../../services/vikunja.md) — Self-hosted task organizer that can utilize Valkey as its cache store.
- [Supabase](../infrastructure/supabase.md) — Self-hosted backend suite providing PostgreSQL and local storage adapters.

## Sources / references
- [Valkey: Architecture Patterns, In-Memory Storage, and Caching Core](https://www.infoq.com/presentations/valkey-architecture-patterns/)
- [Valkey Official Open-Source Project Governance and Repositories](https://github.com/valkey-io/valkey)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
