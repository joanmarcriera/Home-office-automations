# Real-time Sync Engines

## What it is
Real-time sync engines are specialized software components that enable multiplayer collaboration and automatic data consistency across distributed applications. They handle the complex logic of synchronizing state between multiple clients and a central server, often using local-first principles and Conflict-free Replicated Data Types (CRDTs). As of June 2026, they are the foundation for the "Agentic Workbench" pattern.

## What problem it solves
Developing collaborative applications (like Google Docs or Trello) is notoriously difficult due to race conditions, network latency, and conflict resolution. Sync engines abstract these challenges, allowing developers to treat remote data as if it were local while the engine handles background synchronization, partial replication, and deterministic conflict merging. They eliminate the "loading spinner" and "network error" friction in high-interactivity apps.

## Where it fits in the stack
Sync engines sit between the **Application** layer and the **Data/Database** layer. They often replace traditional REST/GraphQL APIs with a reactive synchronization protocol that keeps a local client-side database (like SQLite, PGlite, or an in-memory store) in sync with a server-side source of truth (typically PostgreSQL).

## Typical use cases
- **Multiplayer Workspaces**: Tools like Notion, Linear, or Figma.
- **Edge-Heavy Apps**: Mobile tools used in transit (trains, planes) with intermittent connectivity.
- **Agentic Workbenches**: Real-time coordination between human operators and multiple AI agents working on the same state.
- **Local-First AI**: Running local LLMs against a synced local vector store (e.g., using `pgvector` in PGlite).
- **Collaborative IDEs**: Shared coding environments where agents and humans refactor code simultaneously.

## Strengths
- **Optimistic UI**: No loading spinners for writes; changes are instant on the client and propagate in the background.
- **Offline Reliability**: The app works without a network; sync happens automatically when connectivity is restored.
- **Lower Server Load**: Many read queries are handled locally on the client's cached subset of data.
- **Conflict Resolution**: Built-in CRDT or CDC-based merging ensures all clients eventually reach the same state.

## Limitations
- **Data Governance**: Storing sensitive data on client devices requires robust encryption-at-rest.
- **Large Dataset Handling**: Syncing millions of rows is impractical; requires "Sync Shapes" or sophisticated partial replication.
- **Migration Complexity**: Syncing across schema changes (DML) requires coordinated engine updates.
- **Initial Sync Latency**: The first time a user opens the app, there may be a delay while the initial "Shape" is downloaded.

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

## Getting started (including Docker/Local setup)
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

## API examples (TypeScript)
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

### Optimistic Mutation
```javascript
export const mutators = {
  toggleTodo: async (tx, { id, completed }) => {
    // This runs immediately on the client and eventually on the server
    await tx.set(`todo/${id}`, { completed, updatedAt: Date.now() });
  }
};
```

## Related tools / concepts
- [Vector DBs](vector-db-comparison.md) — Often integrated with sync engines for local RAG via `pgvector`.
- [Agent Protocols](agent_protocols.md) — How agents communicate state changes over sync engines.
- [Invisible Kubernetes](invisible_kubernetes.md) — Automating the backend infrastructure for sync engines.
- [Supabase](../tools/infrastructure/supabase.md) — Provides "Realtime" sync as a core service.
- [Dify](../tools/ai_knowledge/dify.md) — Can use sync engines for real-time agentic collaboration state.
- [LiteLLM](../../services/litellm.md) — Used in sync-heavy agent workbenches for multi-model inference.
- [Wasm](../tools/development_ops/vscode.md) — (Technology context) Enabling databases like PGlite in the browser.
- [OpenAI](../tools/ai_knowledge/openai.md) — Often the intelligence layer acting upon the synced state.

## Sources / References
- [Local-first web development (RethinkDB blog, 2026 update)](https://rethinkdb.com/blog/local-first-2026/)
- [Zero Sync Documentation](https://zero.rocicorp.dev/docs)
- [ElectricSQL PGlite v1.0 Release Notes](https://electric-sql.com/blog/2026/01/15/pglite-stable)
- [InstantDB: The Graph Sync Engine](https://www.instantdb.com/)
- [Jazz: Collaborative Data Layer](https://jazz.tools/)

## Contribution Metadata
- Last reviewed: 2026-06-20
- Confidence: high
