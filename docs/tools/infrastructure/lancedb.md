# LanceDB

## What it is
LanceDB is an open-source, developer-friendly, serverless vector database built on top of the Lance columnar data format. Designed for embedded, disk-native vector search and AI applications, it supports zero-overhead persistent storage on local drives or S3/NFS without running background database daemon processes.

## What problem it solves
Traditional vector databases (like Milvus or Qdrant cluster setups) require dedicated server instances, memory reservation, and complex cluster management. LanceDB eliminates operational overhead for single-box home labs and edge devices by embedding directly into Python or Node.js applications while delivering millisecond-level vector similarity search directly from disk.

## Where it fits in the stack
**Infrastructure / Vector DB**. LanceDB serves as an embedded vector storage layer for local RAG, document search, and memory management across local home-lab agents and services.

## Typical use cases
- **Embedded Document RAG**: Storing and searching vector embeddings from Paperless-ngx or Obsidian notes locally.
- **Air-Gapped Single-Box AI**: Providing persistent vector storage on NVMe/S3 without running a Docker container daemon.
- **Multimodal Search**: Indexing combined image and text embeddings (CLIP/Whisper) for personal home video and photo archives.

## Strengths
- **Serverless & Embedded**: Runs in-process with zero client-server IPC overhead.
- **Disk-Native Columnar Performance**: Lance columnar format permits fast vector search on datasets larger than RAM.
- **Multi-Modal Support**: Native integration with PyArrow, pandas, and Polars.
- **Zero-Maintenance**: Persists directly to local directory paths or network shares.

## Limitations
- **Single-Host Primary**: Best suited for embedded/single-node deployment rather than massive multi-tenant distributed clusters.
- **Ecosystem Maturity**: Slightly newer ecosystem compared to PostgreSQL/pgvector or ChromaDB.

## When to use it
- When requiring zero-daemon embedded vector storage for local RAG applications.
- When querying datasets larger than RAM directly from disk using the Lance format.
- When deploying single-box or edge home-lab automation services.

## When not to use it
- When requiring distributed multi-tenant clustering with high-availability replication across multiple data centers.
- When already utilizing existing PostgreSQL/pgvector deployments for simple relational + vector storage.

## Getting started
Install LanceDB via `pip` or `uv`:

```bash
pip install lancedb
```

A minimal working hello-world example connecting to an embedded LanceDB storage directory, creating a table, and executing vector nearest-neighbor search:

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
```

## API examples

Minimal Python code snippet opening an existing LanceDB collection and executing similarity retrieval with limit parameters:

```python
import lancedb

db = lancedb.connect("./data/lancedb_store")
table = db.open_table("documents")

# Search nearest vectors and format matches
results = table.search([0.1, 0.2, 0.3]).limit(5).to_list()
for row in results:
    print(f"ID: {row['id']} | Text: {row['text']} | Score/Distance: {row.get('_distance', 0.0):.4f}")
```

## Related tools / concepts
- [ChromaDB](chroma.md) — Embedded vector database comparison.
- [Qdrant](qdrant.md) — Dedicated vector database.
- [Paperless-ngx](../../services/paperless-ngx.md) — Local document management and indexing service.
- [Local Embedding Models](local-embeddings.md) — Offline vector embedding generation.

## Sources / references
- [LanceDB Official Documentation](https://lancedb.github.io/lancedb/)
- [Lance Format Specification](https://github.com/lancedb/lance)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
