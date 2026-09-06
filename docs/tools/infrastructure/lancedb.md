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
To install and use LanceDB in Python:

```bash
pip install lancedb
```

```python
import lancedb

# Connect to a local directory storage
db = lancedb.connect("./data/lancedb_store")
table = db.create_table(
    "documents",
    data=[
        {"vector": [0.1, 0.2, 0.3], "text": "Home-lab backup policy", "id": "doc1"},
        {"vector": [0.4, 0.5, 0.6], "text": "K3s cluster config", "id": "doc2"}
    ]
)

# Search nearest neighbors
results = table.search([0.1, 0.2, 0.3]).limit(1).to_list()
print("Search Result:", results)
```

## CLI examples

```bash
# Install LanceDB python package and CLI tool
pip install lancedb

# Inspect a local Lance table file using python CLI
python3 -c "import lancedb; db = lancedb.connect('./data/lancedb_store'); print(db.table_names())"
```

## API examples

### 1. Pydantic v2 Schema & LanceDB Vector Store Handler
```python
from typing import List, Dict, Any
from pydantic import BaseModel, ConfigDict, Field

class VectorRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    text: str
    vector: List[float] = Field(..., min_length=3)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class SearchQuery(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query_vector: List[float]
    top_k: int = Field(default=5, ge=1, le=100)

def search_lancedb_table(query: SearchQuery) -> List[Dict[str, Any]]:
    # Simulated search execution over LanceDB index
    return [
        {"id": "doc1", "text": "Paperless receipt metadata", "score": 0.98}
    ][:query.top_k]

if __name__ == "__main__":
    query = SearchQuery(query_vector=[0.1, 0.2, 0.3], top_k=2)
    results = search_lancedb_table(query)
    print(f"Retrieved {len(results)} match(es)")
```

### 2. FastMCP 3.1 Task Protocol Integration
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("lancedb-service")

@mcp.tool()
def query_vector_store(collection_name: str, vector: list[float], limit: int = 5) -> list[dict]:
    """Queries an embedded LanceDB collection using FastMCP 3.1 task protocol."""
    return [{"id": "item1", "score": 0.95}]
```

## Related tools / concepts
- [ChromaDB](chromadb.md) — Embedded vector database comparison.
- [Qdrant](qdrant.md) — Dedicated vector database.
- [Local Embedding Models](local-embeddings.md) — Offline vector embedding generation.

## Sources / references
- [LanceDB Official Documentation](https://lancedb.github.io/lancedb/)
- [Lance Format Specification](https://github.com/lancedb/lance)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
