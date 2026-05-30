# Real-time Sync Engines

## What it is
Real-time sync engines are specialized software components that enable multiplayer collaboration and automatic data consistency across distributed applications. They handle the complex logic of synchronizing state between multiple clients and a central server, often using local-first principles and Conflict-free Replicated Data Types (CRDTs).

## What problem it solves
Developing collaborative applications (like Google Docs or Trello) is notoriously difficult due to race conditions, network latency, and conflict resolution. Sync engines abstract these challenges, allowing developers to treat remote data as if it were local while the engine handles background synchronization, partial replication, and deterministic conflict merging.

## Where it fits in the stack
Sync engines sit between the **Application** layer and the **Data/Database** layer. They often replace traditional REST/GraphQL APIs with a reactive synchronization protocol that keeps a local client-side database (like SQLite, PGlite, or an in-memory store) in sync with a server-side source of truth (typically PostgreSQL).

## Key Sync Engine Technologies (2026 Baseline)

### Zero (Rocicorp)
A sync engine that providing zero-latency UI by syncing a filtered subset of a Postgres database to a local SQLite instance:
- **Partial Replication**: Syncs only what the user needs (e.g., "my tasks" vs "all tasks").
- **Zero Latency Writes**: Mutations are applied locally and optimistically immediately.
- **Permissioned Sync**: Integrated auth logic determines what rows/columns a client can see.

### InstantDB
A graph-based sync engine that treats the database like a client-side state manager:
- **No-Schema Prototyping**: Relational data without the traditional SQL migrations.
- **Relay-inspired Queries**: Declarative data fetching that automatically updates the UI on change.

### PGlite (ElectricSQL v2)
The evolution of ElectricSQL into a lightweight, Wasm-based Postgres that runs entirely in the browser:
- **Native Postgres in Browser**: Support for extensions like `pgvector` locally.
- **Logical Replication**: Uses standard Postgres replication protocols for sync.

### Triplit
A full-stack database designed for local-first apps:
- **Datalog Queries**: Powerful relational queries on both client and server.
- **Built-in Storage**: No need for a separate SQLite or IndexedDB setup.

### CRDT Frameworks (Automerge, Yjs)
The foundational libraries for shared state:
- **Binary Protocols**: Optimized for low-bandwidth sync.
- **Rich Text Support**: Specialized types for collaborative editing (e.g., `Y.Text`).

## Typical use cases
- **Multiplayer Workspaces**: Tools like Notion, Linear, or Figma.
- **Edge-Heavy Apps**: Mobile tools used in transit (trains, planes) with intermittent connectivity.
- **Agentic Workbenches**: Real-time coordination between human operators and multiple AI agents.
- **Local-First AI**: Running local LLMs against a synced local vector store (e.g., using `pgvector` in PGlite).

## Strengths
- **Optimistic UI**: No loading spinners for writes; changes are instant.
- **Offline Reliability**: The app works without a network; sync happens in the background.
- **Lower Server Load**: Many queries are handled locally, reducing API hits.

## Limitations
- **Data Governance**: Storing sensitive data on client devices requires robust encryption-at-rest.
- **Large Dataset Handling**: Syncing millions of rows is impractical; requires "Sync Shapes" or partial replication.
- **Migration Complexity**: Syncing across schema changes (DML) requires coordinated engine updates.

## When to use it
- When responsiveness is the primary competitive advantage (aiming for "vibe coding" speed).
- For collaborative tools where users expect to see each other's presence and changes in <50ms.
- For high-reliability field software (e.g., logistics, emergency services).

## When not to use it
- Simple CMS or blog sites where "stale" data for a few seconds is acceptable.
- Highly regulated environments where no PII/sensitive data can touch the client disk.
- Purely server-side workloads (e.g., batch processing).

## Implementation Patterns

### Sync Shapes (Partial Replication)
Instead of syncing the whole DB, the client requests a "Shape" (a set of tables and filters).
```typescript
// Example: Requesting a Shape for a specific project
const shape = db.projects.sync({
  where: { id: 'proj_123' },
  include: { tasks: true, comments: true }
});
```

### Optimistic Mutators
Mutators must be deterministic so the client and server reach the same state.
```javascript
export const mutators = {
  toggleTodo: async (tx, { id, completed }) => {
    await tx.set(`todo/${id}`, { completed, updatedAt: Date.now() });
  }
};
```

### Local Vector Search
Using PGlite with `pgvector` to perform RAG entirely on the client.
```javascript
const pg = new PGlite();
await pg.exec("CREATE EXTENSION IF NOT EXISTS vector");
// Vector search runs locally on the synced subset of data
```

## Technical Protocol Comparison

| Feature | Zero | InstantDB | PGlite | Jazz |
| :--- | :--- | :--- | :--- | :--- |
| **Data Model** | Relational (SQL) | Graph | Relational (SQL) | Collaborative Objects |
| **Local Store** | SQLite (Wasm) | IndexedDB | Postgres (Wasm) | CRDT Cache |
| **Sync Method** | Filtered CDC | WebSockets | Logical Replication | P2P / Mesh |
| **Primary Goal** | Postgres Sync | Developer Speed | Pure Postgres | Shared Objects |

## Related tools / concepts
- [Vector DBs](vector-db-comparison.md): Often integrated with sync engines for local RAG.
- [Agent Protocols](agent_protocols.md): How agents communicate state changes over sync engines.
- [Invisible Kubernetes](invisible_kubernetes.md): Automating the backend infrastructure for sync engines.
- [PostgreSQL](../tools/infrastructure/postgresql.md): The canonical source of truth for most engines.
- [Wasm](../tools/development_ops/wasm.md): The technology enabling full databases in the browser.

## Sources / references
- [Local-first web development (RethinkDB blog, 2026 update)](https://rethinkdb.com/blog/local-first-2026/)
- [Zero Sync Documentation](https://zero.rocicorp.dev/docs)
- [ElectricSQL PGlite v1.0 Release Notes](https://electric-sql.com/blog/2026/01/15/pglite-stable)
- [InstantDB: The Graph Sync Engine](https://www.instantdb.com/)

## Contribution Metadata
- Last reviewed: 2026-05-30
- Confidence: high
