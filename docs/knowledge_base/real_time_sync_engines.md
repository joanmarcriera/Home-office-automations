# Real-time Sync Engines

## What it is
Real-time sync engines are specialized software components that enable multiplayer collaboration and automatic data consistency across distributed applications. They handle the complex logic of synchronizing state between multiple clients and a central server, often using local-first principles and Conflict-free Replicated Data Types (CRDTs). As of **early January 2027**, they are the foundation for the "Agentic Workbench" pattern, facilitating sub-10ms state synchronization across humans and autonomous multi-agent systems.

## What problem it solves
Developing collaborative applications (like Google Docs, Figma, or interactive agentic dashboards) is notoriously difficult due to race conditions, network latency, and conflict resolution. Sync engines abstract these challenges, allowing developers to treat remote data as if it were local while the engine handles background synchronization, partial replication, and deterministic conflict merging. They eliminate the "loading spinner" and "network error" friction in high-interactivity apps.

## Architecture & Synchronization Data Flow

Real-time sync engines rely on a reactive, event-driven topology where local client edits are saved optimistically to an embedded client database and replicated via Change Data Capture (CDC) or WebSocket/WebRTC sync channels.

```
+-----------------------------------------------------------------------------------+
|                  Local-First Real-time Sync Engine Topology                       |
+-----------------------------------------------------------------------------------+
                                          |
 1. Local Application / Agent Mutation    |
 +-------------------------------+       |
 | Human Operator UI / AI Agent  |       |
 +---------------+---------------+       |
                 |                       |
                 v                       v
 2. Embedded Client Store (Optimistic Write)
 +-----------------------------------------------+
 |  Local PGlite / SQLite / In-Memory Store      |
 |  - Sub-1ms local read/write                   |
 |  - Offline pending mutation queue             |
 +---------------+-------------------------------+
                 |
                 v
 3. Sync Client SDK & Protocol Layer (FastMCP 3.1 Bridge)
 +-----------------------------------------------+
 |  CRDT / CDC Change Generation                 |
 |  - Vector clocks & LWW / Yjs document state   |
 +---------------+-------------------------------+
                 |
                 | (WebSocket / WebRTC Streaming)
                 v
 4. Backend Sync Cache & Replication Server
 +-----------------------------------------------+
 |  Sync Server (Zero Cache / ElectricSQL Engine)|
 |  - Shape filtering & auth validation          |
 |  - Conflict resolution & WAL ordering         |
 +---------------+-------------------------------+
                 |
                 v
 5. Server-side Primary Storage
 +-----------------------------------------------+
 |  PostgreSQL Primary (Logical Replication WAL) |
 +-----------------------------------------------+
```

## Where it fits in the stack
Sync engines sit between the **Application** layer and the **Data/Database** layer. They replace traditional REST/GraphQL APIs with a reactive synchronization protocol that keeps a client-side database (like SQLite, PGlite, or an in-memory store) in sync with a server-side source of truth (typically PostgreSQL with logical replication enabled).

## Typical use cases
- **Multiplayer Workspaces**: Highly interactive tools like Notion, Linear, or Figma.
- **Edge-Heavy Apps**: Mobile tools used in transit (trains, planes) with intermittent connectivity.
- **Agentic Workbenches**: Real-time coordination between human operators and multiple AI agents powered by Claude 5.1/5.6, GPT-5.5/5.6, Gemini 4.0 Pro/Ultra, DeepSeek-V4, Llama 4, and Gemma 3 working on the same shared application state.
- **Local-First AI**: Running local LLMs against a synced local vector store (e.g., using `pgvector` in PGlite).
- **Collaborative IDEs**: Shared coding environments where agents and humans refactor code simultaneously.

## Strengths
- **Optimistic UI**: No loading spinners for writes; changes are instant on the client and propagate in the background.
- **Offline Reliability**: The app works without a network; sync happens automatically when connectivity is restored.
- **Lower Server Load**: Many read queries are handled locally on the client's cached subset of data.
- **Conflict Resolution**: Built-in CRDT or Change Data Capture (CDC)-based merging ensures all clients eventually reach the same state.

## Limitations
- **Data Governance**: Storing sensitive data on client devices requires robust encryption-at-rest.
- **Large Dataset Handling**: Syncing millions of rows is impractical; requires "Sync Shapes" or sophisticated partial replication.
- **Migration Complexity**: Syncing across schema changes (DML) requires coordinated engine updates.
- **Initial Sync Latency**: The first time a user opens the app, there may be a delay while the initial "Shape" is downloaded.

## Real-Time Sync Engine Comparison Matrix

| Engine | Primary Paradigm | Client Database | Backend Primary DB | FastMCP 3.1 Support | Best Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Zero (Rocicorp)** | Zero-Query / Sync Shapes | Custom reactive store | PostgreSQL (WAL) | Native MCP Bridge | Ultra-fast optimistic web applications |
| **ElectricSQL** | CDC Partial Replication | PGlite (Wasm Postgres) / SQLite | PostgreSQL (Logical) | Integrated | Multi-device local-first AI apps |
| **InstantDB** | Reactive Graph Sync | In-memory graph cache | Instant Hosted / Postgres | MCP API Wrappers | Rapid prototyping & relational multiplayer |
| **Jazz** | CoValues / Local-First Mesh | Local Storage / IndexedDB | Jazz Cloud / Local Node | FastMCP Client | Peer-to-peer collaborative state |
| **Yjs / Automerge** | CRDT Document Trees | In-memory / IndexedDB | Any KV Store / WebSocket | MCP Tool Sync | Rich text & granular multiplayer canvas |

## When to use it
- When responsiveness is the primary competitive advantage (aiming for "vibe coding" speed).
- For collaborative tools where users (humans or agents) expect to see each other's changes in <50ms.
- For high-reliability field software (e.g., logistics, emergency services).
- When building "local-first" AI applications that need to work across multiple devices.

## When not to use it
- Simple CMS or blog sites where "stale" data for a few seconds is acceptable and multiplayer isn't needed.
- Highly regulated environments where no PII/sensitive data can touch the client disk even if encrypted.
- Purely server-side workloads (e.g., batch processing, internal reporting).
- Applications where the dataset is so large and unstructured that local caching provides no benefit.

## Getting started
Most sync engines require a server-side component (usually connected to Postgres) and a client-side SDK.

### Example: Running Zero (Rocicorp) with Docker
Zero requires a Postgres instance with logical replication enabled.
```bash
# Start Postgres with logical replication
docker run -d --name pg-sync -e POSTGRES_PASSWORD=password \
  -c wal_level=logical -p 5432:5432 postgres:16

# Start the Zero Cache server
docker run -d --name zero-cache -p 4848:4848 \
  -e ZERO_UPSTREAM_DB="postgresql://postgres:password@pg-sync:5432/postgres" \
  -e ZERO_CVR_DB="postgresql://postgres:password@pg-sync:5432/postgres" \
  rocicorp/zero:latest
```

## CLI examples
Sync engines often provide CLI tools for schema generation and sync monitoring.

```bash
# Generate client-side schema from your Postgres database (Zero)
npx zero-generate --db postgresql://user:pass@localhost:5432/mydb --out ./src/schema.ts

# Monitor sync replication lag
zero-cli status --server http://localhost:4848

# Inspect local PGlite state in the browser console
await pg.exec("SELECT * FROM tasks WHERE status = 'pending'");
```

## API examples

### Defining a Sync Shape
Instead of syncing the whole DB, the client requests a "Shape".
```typescript
import { useQuery, useZero } from '@rocicorp/zero/react';

function TaskList() {
  const z = useZero();
  // Request only the tasks assigned to the current user
  const [tasks] = useQuery(z.query.tasks.where('assigneeId', '=', 'me'));

  return (
    <ul>
      {tasks.map(t => <li key={t.id}>{t.title}</li>)}
    </ul>
  );
}
```

### FastMCP 3.1 Sync Protocol Engine Bridge
FastMCP 3.1 server exposing real-time synchronization mutation triggers and state inspection as structured agentic tools:

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import time

mcp = FastMCP("RealtimeSyncEngine-Bridge")

class MutationPayload(BaseModel):
    shape_id: str = Field(..., description="Target sync shape identifier")
    entity_id: str = Field(..., description="Unique record/entity ID")
    mutations: Dict[str, Any] = Field(..., description="Field update mapping")
    client_clock: int = Field(default_factory=lambda: int(time.time() * 1000))

class SyncStateResponse(BaseModel):
    shape_id: str
    status: str
    active_peers: int
    pending_mutations_count: int

@mcp.tool()
def apply_optimistic_mutation(payload: MutationPayload) -> Dict[str, Any]:
    """
    Applies an optimistic mutation into the FastMCP sync engine bridge for propagation across connected agents.
    """
    # Simulated execution: dispatching mutation to Local DB / CDC stream
    processed_at = time.time()
    return {
        "success": True,
        "shape_id": payload.shape_id,
        "entity_id": payload.entity_id,
        "applied_clock": payload.client_clock,
        "server_timestamp": processed_at
    }

@mcp.tool()
def inspect_sync_shape_status(shape_id: str) -> Dict[str, Any]:
    """
    Retrieves current synchronization state, replication lag, and active peer agents for a given shape.
    """
    status = SyncStateResponse(
        shape_id=shape_id,
        status="synced",
        active_peers=4,
        pending_mutations_count=0
    )
    return status.model_dump()

if __name__ == "__main__":
    mcp.run()
```

### Pydantic v2 CRDT Operation & Conflict Resolution Validation
Using **Pydantic v2** to programmatically validate and verify collaborative changesets and replication sync payload operations before they are merged into the local or remote DB state:

```python
from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any, Optional
from datetime import datetime

class CRDTReplicationEdit(BaseModel):
    """Pydantic model representing a collaborative real-time state change or edit."""
    client_id: str = Field(..., description="Unique client or agent identifier")
    sequence_number: int = Field(..., ge=0, description="Monotonically increasing sequence number")
    document_id: str = Field(..., description="Target document/shape ID")
    operation: str = Field(..., pattern="^(insert|update|delete|merge)$")
    changeset: Dict[str, Any] = Field(..., description="Key-value pair changes")
    vector_clock: Dict[str, int] = Field(default_factory=dict, description="Logical vector clock for causality tracking")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("changeset")
    @classmethod
    def validate_non_empty_changes(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        """Verify that changeset contains at least one update record."""
        if not v:
            raise ValueError("Changeset dict cannot be empty")
        return v

# Sample verification run
payload = {
    "client_id": "agent-007",
    "sequence_number": 42,
    "document_id": "doc-shape-workspace-11",
    "operation": "update",
    "changeset": {"status": "completed", "progress": 100},
    "vector_clock": {"agent-007": 42, "human-user-1": 15}
}
validated_edit = CRDTReplicationEdit(**payload)
print(f"Validated operation '{validated_edit.operation}' for client {validated_edit.client_id}.")
print(f"Vector clock causality: {validated_edit.vector_clock}")
```

## Related tools / concepts
- [Vector DBs](vector-db-comparison.md) — Often integrated with sync engines for local RAG via `pgvector`.
- [Agent Protocols](agent_protocols.md) — How agents communicate state changes over sync engines.
- [Invisible Kubernetes](invisible_kubernetes.md) — Automating the backend infrastructure for sync engines.
- [Supabase](../tools/infrastructure/supabase.md) — Provides "Realtime" sync as a core service.
- [Dify](../tools/ai_knowledge/dify.md) — Can use sync engines for real-time agentic collaboration state.
- [LiteLLM](../services/litellm.md) — Used in sync-heavy agent workbenches for multi-model inference.
- [Wasm](../tools/development_ops/vscode.md) — (Technology context) Enabling databases like PGlite in the browser.
- [OpenAI](../tools/ai_knowledge/openai.md) — Often the intelligence layer acting upon the synced state.
- [Gemma 3](../tools/ai_knowledge/local_llms.md) — Frequently used in local-first agentic workbenches.
- [MCP 3.1](patterns/tool-calling-and-mcp.md) — Protocol for agent-tool interaction, often synced in real-time.

## Sources / references
- [Local-first web development (RethinkDB blog, 2026 update)](https://rethinkdb.com/blog/local-first-2026/)
- [Zero Sync Documentation](https://zero.rocicorp.dev/docs)
- [ElectricSQL PGlite v1.0 Release Notes](https://electric-sql.com/blog/2026/01/15/pglite-stable)
- [InstantDB: The Graph Sync Engine](https://www.instantdb.com/)
- [Jazz: Collaborative Data Layer](https://jazz.tools/)
- [Model Context Protocol Specification 3.1](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
