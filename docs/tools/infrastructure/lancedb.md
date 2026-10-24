# LanceDB

## What it is
LanceDB is an open-source, developer-friendly, serverless vector database built on top of the Lance columnar data format. Designed for embedded, disk-native vector search and AI applications, it supports zero-overhead persistent storage on local drives, network-attached storage (NFS/SMB), or S3-compatible object stores without running background database daemon processes. By storing vector indices alongside structured columnar attributes in unified `.lance` files, LanceDB delivers low-latency hybrid search and high-throughput analytical queries for local retrieval-augmented generation (RAG) and multi-agent memory systems.

## What problem it solves
Traditional vector databases (such as Milvus or multi-node Qdrant cluster deployments) require dedicated background server processes, complex network configuration, memory allocation tuning, and continuous daemon maintenance. For edge nodes, local development environments, and single-box home labs, this infrastructure overhead introduces failure points and consumes valuable CPU/RAM resources.

LanceDB eliminates operational complexity by embedding directly into Python, Node.js, Rust, or C++ applications. Its disk-native Lance layout utilizes zero-copy random access via memory-mapped IO (`mmap`), allowing applications to query multi-million vector datasets that exceed available system RAM while operating entirely in-process without client-server IPC latency.

## Where it fits in the stack
**Infrastructure / Vector DB**. LanceDB serves as an embedded, zero-daemon vector and structured document storage engine for local RAG pipelines, long-term agent memory context stores, and multimodal media retrieval systems across local home labs, edge gateways, and edge AI workloads.

```mermaid
graph TD
    SubGraph1[AI Agent Framework / FastMCP Server] -->|In-Process Python/Node SDK| LanceDB[LanceDB Embedded Engine]
    LanceDB -->|Zero-Copy MMAP / PyArrow| Storage[Disk Storage / S3 / NFS]

    subgraph Storage Layout
        Storage --> Table1[documents.lance]
        Storage --> Table2[embeddings.lance]
        Table1 --> Index[IVF-PQ Vector Index]
        Table1 --> Columnar[Columnar Metadata Files]
    end

    Inference[Local Embedding Model / Ollama] -->|Vectors| SubGraph1
```

## Typical use cases
- **Embedded Document RAG**: Storing and searching vector embeddings generated from Paperless-ngx documents, Obsidian vaults, or local PDF collections.
- **Air-Gapped Single-Box AI**: Providing high-performance vector storage on local NVMe or NFS shares without managing Docker container daemons or systemd database services.
- **Multimodal Media Search**: Indexing combined image and text embeddings (such as CLIP or Whisper transcripts) for personal photo/video archives with hybrid metadata filtering.
- **FastMCP Agent Memory**: Serving as an embedded, persistent semantic memory store for FastMCP tool servers that save conversation turns and user preferences.

## Systemd Compactor & Maintenance Timer Configuration

For persistent local installations, run `lancedb-compactor.service` and `lancedb-compactor.timer` to execute background table compaction and snapshot pruning:

```ini
# /etc/systemd/system/lancedb-compactor.service
[Unit]
Description=LanceDB Embedded Table Compactor & Snapshot Cleaner
After=network.target

[Service]
Type=oneshot
User=lancedb
Group=lancedb
WorkingDirectory=/var/lib/lancedb
ExecStart=/usr/local/bin/python3 -c "import lancedb; db=lancedb.connect('/var/lib/lancedb'); [db.open_table(t).compact_files() for t in db.table_names()]"

# /etc/systemd/system/lancedb-compactor.timer
[Unit]
Description=Daily LanceDB Table Compaction Timer

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

## Diagnostic & Troubleshooting Guide

| Issue / Symptom | Root Cause | Verification Command | Resolution & Workaround Strategy |
| :--- | :--- | :--- | :--- |
| **`Commit Conflict Error` on multi-process writes** | Concurrent write processes attempting simultaneous table append operations | `journalctl -u lancedb-compactor` | Implement file-lock synchronization or designate a single write worker process queue. |
| **Slow query speeds on multi-million row tables** | Search running unindexed flat brute-force scan (`Flat` index) | `python3 -c "print(tbl.index_stats())"` | Create an IVF-PQ index (`table.create_index(metric='cosine', num_partitions=256)`) to build clustered vector centroids. |
| **High disk bloat after frequent row updates** | LanceDB retaining historical version snapshots | `du -sh /var/lib/lancedb/*.lance` | Run `table.cleanup_old_versions(older_than=timedelta(days=1))` to purge obsolete data files. |
| **`PyArrow.ArrowInvalid: Schema mismatch`** | Appending record dicts with missing or mismatched field types | `python3 -c "print(tbl.schema)"` | Validate incoming document objects using Pydantic v2 schemas before appending to LanceDB tables. |
| **Memory spike during IVF-PQ index creation** | Insufficient VRAM/RAM available for multi-subvector training | `free -h` & `dmesg \| grep -i oom` | Reduce `num_partitions` or set `max_train_samples` parameter during `create_index()` execution. |

## Strengths
- **Serverless & Embedded**: Runs in-process with zero client-server network overhead, eliminating background daemon management and socket connection pools.
- **Disk-Native Columnar Performance**: Built on the Lance format, enabling random-access vector similarity queries over datasets larger than system RAM with millisecond latency.
- **Hybrid Search Capabilities**: Integrates full-text search (FTS) and SQL filtering directly alongside vector distance metrics (Cosine, L2, Dot Product).
- **Zero-Copy Arrow Integration**: Direct interoperability with Apache Arrow, PyArrow, pandas, and Polars for high-throughput data processing and zero-copy transformations.
- **Flexible Storage Backends**: Persists seamlessly to local disk directories, AWS S3, Cloudflare R2, MinIO, or NFS mounts.

## Limitations
- **Single-Writer Constraint**: While multiple readers can access the same LanceDB dataset simultaneously via shared storage, concurrent writes require serialized execution or single-writer coordination.
- **Distributed Cluster Abstraction**: Optimized primarily for embedded or single-node deployments; scaling across massive multi-tenant distributed clusters requires manual partition management or cloud abstractions.
- **Ecosystem Age**: While rapidly growing, its third-party plugin ecosystem is newer compared to legacy relational or traditional standalone vector daemons.

## When to use it
- When requiring zero-daemon embedded vector storage for local Python or Node.js RAG applications.
- When querying datasets larger than RAM directly from local NVMe or SSD storage using the Lance format.
- When deploying single-box or edge home-lab automation services where resource footprint must be minimized.
- When building FastMCP servers that need persistent semantic vector search without introducing container dependencies.

## When not to use it
- When requiring distributed multi-tenant clustering with active-active high-availability write replication across multiple geographical locations.
- When existing PostgreSQL/pgvector or SQLite setups already meet low-concurrency relational and vector storage needs without dedicated vector format optimizations.

## Getting started

### Installation
Install LanceDB via `pip` or `uv`:

```bash
pip install lancedb pyarrow pydantic
```

### Quickstart Example
A minimal working example connecting to an embedded LanceDB storage directory, creating a table, and executing vector nearest-neighbor search:

```python
import lancedb

# Connect to local embedded database path
db = lancedb.connect("./data/lancedb_store")

# Create table with vector embeddings and metadata
table = db.create_table(
    "documents",
    data=[
        {"vector": [0.1, 0.2, 0.3], "text": "Home-lab backup policy", "id": "doc1"},
        {"vector": [0.4, 0.5, 0.6], "text": "K3s cluster config", "id": "doc2"}
    ],
    mode="overwrite"
)

# Execute vector search query
results = table.search([0.1, 0.2, 0.3]).limit(1).to_list()
print("Search Result:", results)
```

## CLI examples

```bash
# 1. Install LanceDB Python SDK package
pip install lancedb

# 2. Inspect local database table names via Python CLI invocation
python3 -c "import lancedb; db = lancedb.connect('./data/lancedb_store'); print(db.table_names())"

# 3. Query row count over an embedded LanceDB table via Python CLI
python3 -c "import lancedb; db = lancedb.connect('./data/lancedb_store'); print(db.open_table('documents').count_rows())"

# 4. Perform direct vector search and output results from CLI
python3 -c "import lancedb; db = lancedb.connect('./data/lancedb_store'); print(db.open_table('documents').search([0.1, 0.2, 0.3]).limit(2).to_list())"
```

## API examples

### 1. Advanced Vector Query with Metadata Filtering
```python
import lancedb

db = lancedb.connect("./data/lancedb_store")
table = db.open_table("documents")

# Search nearest vectors with SQL metadata filter and limit parameters
results = (
    table.search([0.12, 0.21, 0.31])
    .where("id = 'doc1'")
    .limit(5)
    .to_list()
)

for row in results:
    print(f"ID: {row['id']} | Text: {row['text']} | Score/Distance: {row.get('_distance', 0.0):.4f}")
```

### 2. FastMCP 3.1 Embedded Memory Server Integration
```python
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict
from mcp.server.fastmcp import FastMCP
import lancedb
import pyarrow as pa

mcp = FastMCP("lancedb-memory-server", version="3.1.0")
DB_PATH = "./data/mcp_lancedb_memory"

class DocumentRecord(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: str = Field(..., description="Unique document identifier")
    text: str = Field(..., description="Text content or excerpt")
    category: str = Field(default="default", description="Classification category for metadata filtering")
    vector: List[float] = Field(..., description="Dense float vector embedding")
    source_url: Optional[str] = Field(None, description="Optional canonical URL or document file path")

class QueryRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    vector: List[float] = Field(..., description="Query vector embedding")
    top_k: int = Field(default=5, ge=1, le=100, description="Number of nearest neighbors to retrieve")
    filter_sql: Optional[str] = Field(None, description="Optional SQL filter clause")

def get_db():
    return lancedb.connect(DB_PATH)

@mcp.tool()
def store_memory(record: DocumentRecord) -> str:
    """Stores a semantic vector memory entry in embedded LanceDB."""
    db = get_db()
    table_name = "agent_memories"

    data = [record.model_dump()]

    if table_name in db.table_names():
        table = db.open_table(table_name)
        table.add(data)
    else:
        table = db.create_table(table_name, data=data)

    return f"Successfully stored memory ID '{record.id}' in LanceDB."

@mcp.tool()
def search_memories(req: QueryRequest) -> List[Dict[str, Any]]:
    """Retrieves top-k relevant agent memories from LanceDB based on vector similarity."""
    db = get_db()
    if "agent_memories" not in db.table_names():
        return []

    table = db.open_table("agent_memories")
    query = table.search(req.vector).limit(req.top_k)

    if req.filter_sql:
        query = query.where(req.filter_sql)

    return query.to_list()

@mcp.tool()
def compact_memory_tables() -> Dict[str, Any]:
    """Triggers file compaction and old version cleanup on embedded LanceDB tables."""
    db = get_db()
    compacted = []
    for t_name in db.table_names():
        tbl = db.open_table(t_name)
        tbl.compact_files()
        compacted.append(t_name)
    return {"status": "completed", "compacted_tables": compacted}

if __name__ == "__main__":
    mcp.run()
```

## Architectural Comparison & Vector Database Matrix

| Vector Store | Primary Architecture | Daemon Required | Memory Footprint | Full-Text Search (FTS) | Best Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **LanceDB** | Serverless Embedded (`.lance` columnar files) | No (Embedded Python/Node/Rust) | Disk-native MMAP (Zero-RAM bloat) | Native BM25 + Vector Hybrid | Embedded local RAG, single-box agent memory, NVMe vector stores |
| **Qdrant** | Standalone Service / Cluster | Yes (`qdrant` daemon) | High (In-Memory HNSW graphs) | Payload text indexing | Enterprise multi-tenant cloud vector search & microservices |
| **ChromaDB** | Embedded SQLite + HNSW / Server | Optional | Medium (In-memory index) | Basic metadata filter | Simple prototype RAG & Python experiment scripts |
| **Milvus** | Distributed Kubernetes Cluster | Yes (Multi-container etcd/MinIO) | Heavy | Supported via plugins | High-throughput distributed enterprise vector search at billion scale |

## Related tools / concepts
- [ChromaDB](chroma.md) — Embedded vector database comparison.
- [Qdrant](qdrant.md) — Dedicated standalone vector database engine.
- [Paperless-ngx](../../services/paperless-ngx.md) — Local document management and indexing service.
- [Local Embedding Models](local-embeddings.md) — Offline vector embedding generation runtimes.

## Sources / references
- [LanceDB Official Documentation](https://lancedb.github.io/lancedb/)
- [Lance Format Specification](https://github.com/lancedb/lance)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
