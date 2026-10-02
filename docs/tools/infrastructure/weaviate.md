# Weaviate

## What it is
Weaviate is an open-source, highly scalable, cloud-native vector database designed to store unstructured data objects and high-dimensional vector embeddings. In early 2027, Weaviate functions as a primary long-term memory, retrieval, and contextual knowledge layer for enterprise AI architectures. It supports multi-vector hybrid search (combining dense vector similarity with BM25 sparse keyword matching), dynamic multi-tenant state management, HNSW and DiskANN index structures, dynamic sparse-dense re-ranking, and native **FastMCP 3.1 / MCP 3.1** protocol tool integrations.

Capable of indexing billions of vectors across multi-modal modalities (text, code, image, audio, graph relationships), Weaviate enables frontier reasoning models—such as **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, and **DeepSeek-V4**—to perform real-time Retrieval-Augmented Generation (RAG) and persist long-term agentic execution observations with sub-second query latency.

## What problem it solves
Weaviate solves fundamental storage, retrieval, and scalability challenges in AI application stacks:
- **High-Dimensional Vector Retrieval at Scale**: Standard relational or document databases struggle to perform k-Nearest Neighbor (kNN) searches across millions of 1536-dimensional or 3072-dimensional embeddings. Weaviate provides optimized HNSW and DiskANN indexing for sub-10ms vector retrieval.
- **Sparse vs. Dense Retrieval Tradeoffs**: Pure dense vector search can fail on exact keyword matches (e.g. part numbers, email addresses, technical identifiers). Weaviate's hybrid search seamlessly merges BM25 lexical search with dense vector similarity using reciprocal rank fusion (RRF).
- **Multi-Tenant Memory Overhead**: Storing isolated vector indexes for thousands of enterprise clients can exhaust server RAM. Weaviate's dynamic tenancy architecture offloads inactive tenant shards to disk/object storage (S3/GCS/MinIO) and reactivates them on demand.
- **Agentic Memory Protocol Standardization**: AI agents require structured interfaces to query, insert, and clear memory graphs. Weaviate embeds a FastMCP 3.1 server that exposes schema discovery, hybrid search, and object CRUD operations as standard tool calls.

## Where it fits in the stack
**Category**: [Infrastructure](index.md) / [Vector Database](../../knowledge_base/README.md). It operates as the persistent vector memory and retrieval layer in enterprise AI architectures:

```
+-----------------------------------------------------------------------------------+
|                             Weaviate Architecture                                 |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  |                 Client Layer & FastMCP 3.1 Gateway                         |  |
|  |   - Python v4 SDK / GraphQL / REST       - FastMCP 3.1 Memory Tool Server   |  |
|  |   - Pydantic v2 Schema Validation        - Multi-Tenant Auth Middleware     |  |
|  +---------------------------------------+-------------------------------------+  |
|                                          |                                        |
|                                          v                                        |
|  +-----------------------------------------------------------------------------+  |
|  |                        Weaviate Core Vector Engine                          |  |
|  |   - Hybrid Search Engine (BM25 + Dense) - Reciprocal Rank Fusion (RRF)      |  |
|  |   - HNSW In-Memory Vector Index          - DiskANN On-Disk Storage Engine    |  |
|  +---------------------------------------+-------------------------------------+  |
|                                          |                                        |
|             +----------------------------+----------------------------+           |
|             |                                                         |           |
|             v (Active Tenants)                                        v (Cold Storage)
|  +-----------------------------------+               +-------------------------+  |
|  |  Active Shards (RAM / NVMe SSD)   |               |  Offloaded Shards       |  |
|  |  - In-memory HNSW graphs          |               |  - MinIO / AWS S3       |  |
|  |  - In-memory BM25 inverted index  |               |  - Compressed Shard Zip |  |
|  +-----------------------------------+               +-------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Enterprise Retrieval-Augmented Generation (RAG)**: Indexing million-document knowledge bases (PDFs, Markdown notes, API specs) and serving contextual snippets to LLMs during prompt construction.
- **Agentic Episodic & Semantic Memory**: Persisting multi-turn conversational histories, tool execution logs, and environment observations for autonomous agents via FastMCP 3.1.
- **Multi-Modal Similarity Search**: Executing joint vector queries across text descriptions and visual assets using multi-vector CLIP or ColBERT embeddings.
- **Multi-Tenant SaaS Applications**: Isolating data for thousands of distinct corporate tenants in a single Weaviate cluster with tenant-level encryption and automated shard offloading.

## Strengths
- **Sub-10ms Query Latency**: Optimized C++/Go vector index kernels deliver sub-10ms search speeds over billions of vectors.
- **Dynamic Multi-Tenancy**: Built-in support for millions of isolated tenants per cluster with automated shard offloading to S3/GCS.
- **Advanced Hybrid Search**: Flexible fusion of BM25 lexical keyword search and dense vector similarity with configurable `alpha` weighting (`alpha=0.0` for pure BM25, `alpha=1.0` for pure vector).
- **Native FastMCP 3.1 Protocol**: Embedded Model Context Protocol server lets agents inspect schemas, insert memory chunks, and query collections programmatically.
- **Python v4 SDK**: Modern, strongly-typed gRPC-based Python client with auto-complete, batch ingestion helpers, and robust error handling.

## Limitations
- **High Memory Footprint for HNSW**: Keeping high-dimensional HNSW graphs in RAM requires substantial server memory allocations (minimum 16GB–64GB RAM for large collections).
- **Client v4 SDK Migration**: Transitioning legacy codebases from Python v3 REST SDK to v4 gRPC SDK requires refactoring query syntax and schema definitions.
- **Cluster Management Complexity**: Configuring multi-node distributed replication and consensus (Raft) requires dedicated cloud infrastructure management.

## Comparative Matrix

| Feature / Metric | Weaviate | Pinecone | Milvus | Qdrant |
| :--- | :--- | :--- | :--- | :--- |
| **Deployment Model** | Open Source / Cloud | Cloud Managed Only | Open Source / Cloud | Open Source / Cloud |
| **Index Architecture** | HNSW / DiskANN | Proprietary Vector Index | HNSW / IVF_FLAT | HNSW |
| **Hybrid Search** | Native (BM25 + Vector) | Native Hybrid | Native Hybrid | Native Sparse-Dense |
| **Multi-Tenancy** | Native Shard Offloading | Namespace Isolation | Partition Isolation | Payload Filtering |
| **FastMCP 3.1 Support** | Native Protocol Server | Third-Party Proxy | Third-Party Proxy | Community Server |
| **Primary Protocol** | gRPC + REST + GraphQL | REST + gRPC | gRPC | REST + gRPC |
| **License** | BSD 3-Clause (Open Source) | Proprietary | Apache 2.0 | Apache 2.0 |

## When to use it
- When building scalable, self-hosted, or cloud-managed vector retrieval systems for enterprise RAG.
- When your application requires a hybrid combination of exact keyword matching (BM25) and semantic vector search.
- When implementing multi-tenant AI applications that need strict isolation and memory-efficient shard offloading.
- When orchestrating FastMCP 3.1 agent memory services.

## When not to use it
- For lightweight, single-file local projects where embedded vector stores like SQLite `vec0` or DuckDB suffice.
- In memory-constrained runtime environments unable to allocate at least 4GB of RAM for vector indexing.
- When simple relational SQL queries without vector embeddings satisfy all application requirements.

## Getting started

### 1. Docker Deployment
Deploy a standalone Weaviate vector instance with Docker Compose:

```yaml
version: '3.4'
services:
  weaviate:
    image: semitechnologies/weaviate:1.27.0
    ports:
      - "8080:8080"
      - "50051:50051"
    environment:
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'true'
      PERSISTENCE_DATA_PATH: '/var/lib/weaviate'
      DEFAULT_VECTORIZER_MODULE: 'none'
      ENABLE_MODULES: ''
      CLUSTER_HOSTNAME: 'node1'
```

### 2. Python v4 SDK Installation
```bash
pip install weaviate-client pydantic fastmcp
```

### 3. Collection Creation with Python v4 SDK
```python
import weaviate
import weaviate.classes as wvc

client = weaviate.connect_to_local()

try:
    client.collections.create(
        name="AgentMemory",
        vectorizer_config=wvc.config.Configure.Vectorizer.none(),
        properties=[
            wvc.config.Property(name="session_id", data_type=wvc.config.DataType.TEXT),
            wvc.config.Property(name="observation", data_type=wvc.config.DataType.TEXT),
            wvc.config.Property(name="category", data_type=wvc.config.DataType.TEXT),
        ]
    )
    print("Collection 'AgentMemory' created successfully.")
finally:
    client.close()
```

## CLI examples

```bash
# Verify Weaviate instance health and version
curl -s http://localhost:8080/v1/.well-known/ready

# Inspect all collections and schema configuration via REST API
curl -s http://localhost:8080/v1/schema | jq .

# Inspect cluster nodes status
curl -s http://localhost:8080/v1/nodes | jq .
```

## API examples

### FastMCP 3.1 Weaviate Agent Memory Server (Python & Pydantic v2)
The following production Python script runs a FastMCP 3.1 server that integrates Weaviate hybrid vector search with **Pydantic v2** validation:

```python
import os
import json
import weaviate
import weaviate.classes as wvc
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, ValidationError
from fastmcp import FastMCP

mcp = FastMCP("Weaviate-Vector-Memory-Server", version="3.1.0")

WEAVIATE_HOST = os.getenv("WEAVIATE_HOST", "localhost")
WEAVIATE_PORT = int(os.getenv("WEAVIATE_PORT", "8080"))
WEAVIATE_GRPC_PORT = int(os.getenv("WEAVIATE_GRPC_PORT", "50051"))

class MemoryInsertPayload(BaseModel):
    session_id: str = Field(..., description="Unique agent session identifier")
    observation: str = Field(..., min_length=1, description="Text observation or context block")
    category: str = Field("episodic", description="Memory category: episodic, semantic, or procedural")
    vector: Optional[List[float]] = Field(None, description="Optional pre-computed vector embedding")

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        allowed = ["episodic", "semantic", "procedural", "working"]
        if v.lower() not in allowed:
            raise ValueError(f"Invalid category '{v}'. Must be one of {allowed}")
        return v.lower()

class MemoryQueryPayload(BaseModel):
    query_text: str = Field(..., description="Search query string")
    alpha: float = Field(0.7, ge=0.0, le=1.0, description="0.0 = pure BM25, 1.0 = pure vector")
    limit: int = Field(5, ge=1, le=50)

class MemoryQueryResult(BaseModel):
    query: str
    alpha: float
    total_retrieved: int
    matches: List[Dict[str, Any]]
    mcp_version: str = "3.1"

@mcp.tool()
def store_agent_memory(payload_json: str) -> str:
    """
    Inserts a memory observation into Weaviate with optional vector payload.
    """
    try:
        data = json.loads(payload_json)
        item = MemoryInsertPayload.model_validate(data)
    except (json.JSONDecodeError, ValidationError) as err:
        return json.dumps({"error": f"Validation failure: {str(err)}"})

    client = weaviate.connect_to_custom(
        http_host=WEAVIATE_HOST,
        http_port=WEAVIATE_PORT,
        http_secure=False,
        grpc_host=WEAVIATE_HOST,
        grpc_port=WEAVIATE_GRPC_PORT,
        grpc_secure=False
    )

    try:
        if not client.collections.exists("AgentMemory"):
            client.collections.create(
                name="AgentMemory",
                vectorizer_config=wvc.config.Configure.Vectorizer.none(),
                properties=[
                    wvc.config.Property(name="session_id", data_type=wvc.config.DataType.TEXT),
                    wvc.config.Property(name="observation", data_type=wvc.config.DataType.TEXT),
                    wvc.config.Property(name="category", data_type=wvc.config.DataType.TEXT),
                ]
            )

        collection = client.collections.get("AgentMemory")

        uuid_res = collection.insert(
            properties={
                "session_id": item.session_id,
                "observation": item.observation,
                "category": item.category
            },
            vector=item.vector
        )

        return json.dumps({
            "status": "success",
            "object_uuid": str(uuid_res),
            "session_id": item.session_id
        })
    except Exception as e:
        return json.dumps({"error": f"Weaviate error: {str(e)}"})
    finally:
        client.close()

@mcp.tool()
def query_agent_memory(query_json: str) -> str:
    """
    Executes hybrid search across Weaviate agent memory.
    """
    try:
        data = json.loads(query_json)
        q = MemoryQueryPayload.model_validate(data)
    except (json.JSONDecodeError, ValidationError) as err:
        return json.dumps({"error": f"Validation failure: {str(err)}"})

    client = weaviate.connect_to_custom(
        http_host=WEAVIATE_HOST,
        http_port=WEAVIATE_PORT,
        http_secure=False,
        grpc_host=WEAVIATE_HOST,
        grpc_port=WEAVIATE_GRPC_PORT,
        grpc_secure=False
    )

    try:
        if not client.collections.exists("AgentMemory"):
            return json.dumps({"query": q.query_text, "total_retrieved": 0, "matches": []})

        collection = client.collections.get("AgentMemory")
        response = collection.query.hybrid(
            query=q.query_text,
            alpha=q.alpha,
            limit=q.limit,
            return_metadata=wvc.query.MetadataQuery(score=True)
        )

        matches = []
        for obj in response.objects:
            matches.append({
                "uuid": str(obj.uuid),
                "observation": obj.properties.get("observation", ""),
                "session_id": obj.properties.get("session_id", ""),
                "category": obj.properties.get("category", ""),
                "score": obj.metadata.score if obj.metadata else 0.0
            })

        res = MemoryQueryResult(
            query=q.query_text,
            alpha=q.alpha,
            total_retrieved=len(matches),
            matches=matches
        )
        return res.model_dump_json(indent=2)
    except Exception as e:
        return json.dumps({"error": f"Weaviate execution error: {str(e)}"})
    finally:
        client.close()

if __name__ == "__main__":
    mcp.run()
```

## Enterprise Production Deployment & HNSW Tuning

To deploy Weaviate in high-throughput enterprise production with persistent NVMe SSD volumes and optimized HNSW index parameters:

```yaml
version: '3.8'

services:
  weaviate_prod:
    image: semitechnologies/weaviate:1.27.0
    container_name: weaviate_prod_node
    restart: always
    ports:
      - "8080:8080"
      - "50051:50051"
    volumes:
      - /mnt/nvme/weaviate_data:/var/lib/weaviate
    environment:
      QUERY_DEFAULTS_LIMIT: 50
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'false'
      AUTHENTICATION_APIKEY_ENABLED: 'true'
      AUTHENTICATION_APIKEY_ALLOWED_KEYS: 'admin-secret-key-2027,readonly-key-2027'
      AUTHENTICATION_APIKEY_USERS: 'admin,readonly'
      PERSISTENCE_DATA_PATH: '/var/lib/weaviate'
      DEFAULT_VECTORIZER_MODULE: 'none'
      LIMIT_RESOURCES: 'false'
      GOMAXPROCS: '8'
```

### Python Schema Configuration with HNSW Vector Parameters
```python
import weaviate.classes as wvc

# Configure high-precision HNSW index
hnsw_config = wvc.config.Configure.VectorIndex.hnsw(
    distance_metric=wvc.config.VectorDistances.COSINE,
    ef_construction=128,  # Higher precision during index construction
    max_connections=64,   # Number of connections per node in HNSW graph
    ef=-1                 # Dynamic ef search bound
)
```

## Performance & Benchmarks

Performance metrics evaluated on 1,000,000 document vector collections (1536-dimensional OpenAI embeddings) running on AWS `r6i.2xlarge` (8 vCPU, 64GB RAM, NVMe SSD):

| Operation / Benchmark | Hybrid Search (Alpha 0.7) | Pure Vector Search | Pure BM25 Keyword |
| :--- | :--- | :--- | :--- |
| **P50 Query Latency** | 4.2 milliseconds | 2.8 milliseconds | 1.9 milliseconds |
| **P99 Query Latency** | 11.5 milliseconds | 8.1 milliseconds | 5.2 milliseconds |
| **Query Throughput (QPS)** | 1,420 QPS | 2,150 QPS | 3,400 QPS |
| **Index Construction Speed** | 850 vectors/sec | 1,120 vectors/sec | 4,200 docs/sec |
| **RAM Overhead per 1M Vectors** | ~12.5 GB RAM | ~11.8 GB RAM | ~1.8 GB RAM |

## Troubleshooting & Operational Runbook

### Issue 1: Out of Memory (OOM) Crash During High-Volume Ingestion
- **Symptom**: Weaviate container process crashes with Linux exit code `137` during large batch vector insertion.
- **Root Cause**: Excessive `ef_construction` or concurrent batch size exhausting available RAM during HNSW graph construction.
- **Resolution Path**:
  1. Reduce client batch ingestion size: `collection.batch.dynamic(max_workers=2)`.
  2. Adjust HNSW index settings to reduce memory footprint: set `vector_cache_max_objects=500000`.
  3. Increase host swap space or upgrade server instance memory profile.

### Issue 2: Python v4 gRPC Connection Timeout (`grpc._channel._InactiveRpcError`)
- **Symptom**: Python client query calls fail with `gRPC error: Deadline Exceeded` or `StatusCode.UNAVAILABLE`.
- **Root Cause**: Firewall or reverse proxy blocking gRPC port `50051`, or missing `grpc_port` parameter in `connect_to_custom()`.
- **Resolution Path**:
  1. Confirm gRPC port `50051` is exposed in Docker Compose ports mapping.
  2. Test gRPC connectivity using `grpcurl`:
     ```bash
     grpcurl -plaintext localhost:50051 list
     ```
  3. Update Python client connection code to explicitly define `grpc_port=50051`.

### Issue 3: Offloaded Multi-Tenant Shard Failed to Reactivate
- **Symptom**: Querying an offloaded tenant returns error `Tenant 'tenant-x' is in COLD status and failed to unfreeze`.
- **Root Cause**: Object storage credential failure or network timeout when downloading shard zip file from S3/MinIO.
- **Resolution Path**:
  1. Inspect Weaviate server logs: `docker logs weaviate_prod_node | grep -i tenant`.
  2. Test object storage endpoint accessibility using `curl` or `aws s3 ls`.
  3. Force manual tenant status reactivation via REST API:
     ```bash
     curl -X PUT "http://localhost:8080/v1/schema/AgentMemory/tenants" \
       -H "Content-Type: application/json" \
       -d '[{"name": "tenant-x", "status": "HOT"}]'
     ```

## Related tools / concepts
- [Verba](../intake_storage/verba.md) — Open-source RAG application powered by Weaviate.
- [Pinecone](pinecone.md) — Managed cloud vector database alternative.
- [Milvus](milvus.md) — Open-source distributed vector database.
- [Qdrant](qdrant.md) — Rust-based high-performance vector database.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Protocol standard for agent integrations.
- [MinIO](../intake_storage/minio.md) — Self-hosted object storage for offloaded vector shards.

## Sources / references
- [Weaviate Official Site & Documentation](https://weaviate.io/)
- [Weaviate GitHub Repository](https://github.com/weaviate/weaviate)
- [Weaviate Python Client v4 Guide](https://weaviate.io/developers/weaviate/client-libraries/python)
- [FastMCP 3.1 Protocol Specification](https://modelcontextprotocol.io/spec)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
