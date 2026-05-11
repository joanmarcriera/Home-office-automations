# Real-time Sync Engines

## What it is
Real-time sync engines are specialized software components that enable multiplayer collaboration and automatic data consistency across distributed applications. They handle the complex logic of synchronizing state between multiple clients and a central server, often using local-first principles.

## What problem it solves
Developing collaborative applications (like Google Docs or Trello) is notoriously difficult due to race conditions, network latency, and conflict resolution. Sync engines abstract these challenges, allowing developers to treat remote data as if it were local while the engine handles background synchronization and conflict merging.

## Where it fits in the stack
Sync engines sit between the **Application** layer and the **Data/Database** layer. They often replace traditional REST/GraphQL APIs with a reactive synchronization protocol that keeps a local client-side database (like SQLite or an in-memory store) in sync with a server-side source of truth (like Postgres).

## Key Sync Engine Technologies

### Zero (Rocicorp)
A sync engine that provides every client with a local SQLite database synchronized with a central PostgreSQL database:
- **Local-First Writes**: Mutations happen locally first for zero-latency UI updates.
- **Replay Mechanism**: Writes are replayed on the server; clients reconcile automatically if conflicts occur.
- **Mutator Model**: Allows fine-grained control over conflict resolution, especially for complex JSON values.
- **Granular Updates**: Ability to update specific fields (e.g., a single node's position) rather than replacing entire documents.

### ElectricSQL and PowerSync
Alternative sync engines for Postgres that focus on:
- **Bi-directional Sync**: Keeping local state and remote databases in harmony.
- **Relational Data**: Optimized for standard SQL rows rather than just document/text blobs.

### CRDT Libraries (Yjs, Automerge)
Conflict-free Replicated Data Types, ideal for:
- **Document Collaboration**: Rich text editors and drawing tools.
- **Decentralized Sync**: Scenarios where a central authoritative server may not be present.

## Typical use cases
- **Collaborative Editors**: Multi-user document or whiteboarding tools.
- **Local-First Apps**: Mobile or web apps that must work offline and sync perfectly when back online.
- **Real-time Dashboards**: Interactive displays that update instantly as underlying data changes across the network.

## Strengths
- **Zero Latency**: Local-first writes provide immediate UI feedback.
- **Offline Support**: Applications remain fully functional without a network connection.
- **Simplified Backend**: Reduces the need for complex API endpoints and state management logic.

## Limitations
- **Storage Constraints**: Large datasets may not fit in a client-side SQLite database.
- **Conflict Complexity**: While engines handle "merging," some business-logic conflicts still require custom mutator logic.
- **Initial Sync Overhead**: Downloading the initial state to a new client can be slow for data-heavy applications.

## When to use it
- When building "multiplayer" features where multiple users edit the same objects simultaneously.
- When application responsiveness is a top priority (aiming for <100ms latency).
- For field-service apps or mobile tools used in areas with poor connectivity.

## When not to use it
- For static content or simple "read-only" applications.
- When data privacy requirements forbid storing any sensitive data on the client device.
- For extremely large datasets that far exceed the storage capacity of typical mobile/web clients.

## Implementation Patterns

### Granular Mutators
Avoiding "clobbered drafts" by reading the current state, applying a specific change, and writing it back. This ensures that concurrent changes to different parts of the same object are preserved.

### Bulk Mutators
Used for operations that cannot be easily merged, such as "undo" to a specific snapshot, where the snapshot must win.

### Local State Management
Using lightweight stores like **Nanostores** to handle client-only state (e.g., undo history, UI toggles) that should not be synced across the network.

## Related tools / concepts
- [Nextcloud](../services/nextcloud.md): Uses file-based sync engines for document collaboration.
- [Vikunja](../services/vikunja.md): Could benefit from sync engines for offline task management.
- [Gitea](../services/gitea.md): Distributed version control is a form of asynchronous sync engine.
- [Tailscale](../services/tailscale.md): Uses a coordination server to sync network state across peers.
- [Authentik](../services/authentik.md): Syncs identity state across multiple providers and protocols.
- [Paperless-ngx](../services/paperless-ngx.md): Synchronizes document metadata and OCR results.
- [Immich](../services/immich.md): Synchronizes large media libraries between mobile devices and a central server.

## Sources / references
- [From clobbered drafts to real-time sync (The New Stack, 2026-04-14)](https://thenewstack.io/real-time-sync-engine/)
- [Zero Sync Engine](https://zero.rocicorp.dev/)
- [ElectricSQL](https://electric-sql.com/)

## Contribution Metadata
- Last reviewed: 2026-05-11
- Confidence: high
