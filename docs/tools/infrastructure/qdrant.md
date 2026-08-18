# Qdrant

## What it is

- **Rust-Engineered Vector Storage**: Custom-built in Rust for memory safety, concurrency, and high-throughput vector similarity matching (Cosine, Dot Product, Euclidean, Manhattan distance metrics).
- **HNSW Graph Indexing with Payload Filtering**: Advanced Hierarchical Navigable Small World (HNSW) graph indexing coupled with real-time JSON metadata payload filtering during vector traversal.
- **Hybrid & Multi-Vector Support**: Support for multiple named dense vectors per point, sparse vectors for lexical keyword matching, multi-vector representations (such as ColBERT late-interaction models), and Reciprocal Rank Fusion (RRF).
- **Advanced Vector Quantization**: Built-in Scalar Quantization (SQ), Product Quantization (PQ), and Binary Quantization (BQ), reducing RAM footprint by up to 95% with minimal impact on search recall.
- **Distributed Cloud-Native Scaling**: Raft-consensus cluster orchestration, dynamic collection sharding, zero-downtime rolling updates, and disk-backed payload/vector storage options.


## What problem it solves
- Solves high memory footprint and slow vector search retrieval times in large-scale Retrieval-Augmented Generation (RAG) and agent memory systems.
- Eliminates post-filtering latency overhead by applying payload metadata constraints during graph traversal.

## Where it fits in the stack
- Sits in the **Vector Infrastructure & Storage** layer.
- Serves as the high-performance memory store for multi-agent swarms, LLM retrieval pipelines, and semantic search tools.

## Typical use cases

- **Agentic Long-Term Memory**: Persistent vector indexing of conversation history, user preferences, tool call logs, and execution traces for multi-agent swarms.
- **Enterprise Hybrid RAG**: Combining dense semantic embedding retrieval with sparse BM25/splade keyword filtering across millions of corporate documents.
- **Multi-Modal Similarity Search**: Indexing image embeddings (CLIP/SigLIP), audio vectors, and code representations for multi-modal agent workflows.
- **Real-Time Recommendation Engines**: High-throughput vector retrieval with dynamic payload constraints (e.g., availability, user location, access control tags).


## Strengths

- **Resource Efficiency**: Rust runtime zero-cost abstractions paired with binary/scalar quantization deliver extreme memory efficiency compared to JVM-based or Python-based vector databases.
- **Precise Metadata Filtering**: Unlike two-pass filtering vector stores, Qdrant integrates payload filtering directly into the HNSW graph traversal.
- **Rich Client Ecosystem**: Official SDKs for Python, Rust, Go, TypeScript/Node.js, and Java, accompanied by FastMCP 3.1 tools.


## Limitations

- **HNSW Index Building Overhead**: Initial index construction and heavy quantization on massive datasets (100M+ vectors) require temporary high CPU/RAM resources.
- **Complex Hyperparameter Tuning**: Tuning HNSW graph parameters (`m`, `ef_construct`, `ef`) requires benchmarking to balance indexing speed versus recall accuracy.


## When to use it

- When building production-grade agentic memory systems requiring strict payload filtering, multi-vector schemas, and low-latency retrieval.
- When memory footprint and infrastructure costs are paramount, making Rust performance and vector quantization essential.
- When deploying vector search across hybrid cloud or on-premises Kubernetes environments via open-source or managed Qdrant Cloud.


## When not to use it
- When managing strictly relational SQL workloads or lightweight key-value stores without vector embeddings.
- When an embedded in-memory database like SQLite or DuckDB is sufficient for single-user offline scripts.

## Getting started

```
+-------------------------------------------------------------------+
|                        Qdrant Core Engine                         |
|                                                                   |
|   +-------------------+    +----------------+    +------------+   |
|   | gRPC / REST API   |===>| Query Planner  |===>| HNSW Vector|   |
|   | / FastMCP 3.1     |    | & Payload Filter|   | Graph Index|   |
|   +-------------------+    +----------------+    +------------+   |
|                                                          ||       |
|                                                          \/       |
|                            +----------------------------------+   |
|                            | Quantized Storage & NVMe Payload |   |
|                            +----------------------------------+   |
+-------------------------------------------------------------------+
           ^                                         ||
           | Ingest & Query                          \/
+-----------------------+                    +---------------+
| Multi-Agent Swarms &  |                    | FastMCP 3.1   |
| RAG Retrieval Engines |                    | Search Engine |
+-----------------------+                    +---------------+
```


## CLI examples



## API examples

The following Python example demonstrates initializing a Qdrant client, validating payload structures using strict **Pydantic v2** schemas, upserting dense vector points with metadata, and executing hybrid payload-filtered vector similarity search.

```python
import uuid
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue

# ---------------------------------------------------------------------------
# Pydantic v2 Payload & Query Schemas
# ---------------------------------------------------------------------------
class VectorPayloadSchema(BaseModel):
    document_id: str = Field(..., description="Source document identifier")
    author: str = Field(..., description="Document author or agent name")
    category: str = Field(..., description="Document domain category")
    content_chunk: str = Field(..., description="Raw text snippet corresponding to vector")
    access_level: str = Field(..., description="Security access control level")

    @field_validator("access_level")
    @classmethod
    def validate_access_level(cls, v: str) -> str:
        allowed = {"public", "internal", "confidential"}
        if v.lower() not in allowed:
            raise ValueError(f"access_level must be one of {allowed}")
        return v.lower()

class VectorQuerySchema(BaseModel):
    query_vector: List[float] = Field(..., min_items=4, description="Dense embedding vector")
    top_k: int = Field(default=5, ge=1, le=100, description="Number of nearest neighbors")
    filter_category: Optional[str] = Field(None, description="Category metadata filter constraint")

# ---------------------------------------------------------------------------
# Qdrant Vector Search Pipeline
# ---------------------------------------------------------------------------
class QdrantVectorService:
    def __init__(self, collection_name: str = "agentic_knowledge", vector_size: int = 1536):
        # In-memory instance for testing/demonstration
        self.client = QdrantClient(":memory:")
        self.collection_name = collection_name
        self._init_collection(vector_size)

    def _init_collection(self, vector_size: int) -> None:
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

    def upsert_point(self, vector: List[float], payload_data: Dict[str, Any]) -> str:
        validated_payload = VectorPayloadSchema.model_validate(payload_data)
        point_id = str(uuid.uuid4())

        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=validated_payload.model_dump()
                )
            ]
        )
        return point_id

    def search_similar(self, query_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        query = VectorQuerySchema.model_validate(query_data)

        query_filter = None
        if query.filter_category:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="category",
                        match=MatchValue(value=query.filter_category)
                    )
                ]
            )

        hits = self.client.search(
            collection_name=self.collection_name,
            query_vector=query.query_vector,
            query_filter=query_filter,
            limit=query.top_k
        )

        return [
            {"id": str(hit.id), "score": hit.score, "payload": hit.payload}
            for hit in hits
        ]

if __name__ == "__main__":
    service = QdrantVectorService(vector_size=4)
    sample_vector = [0.1, 0.3, 0.8, 0.4]
    sample_payload = {
        "document_id": "doc-991",
        "author": "agent-researcher",
        "category": "architecture",
        "content_chunk": "Qdrant uses Rust-native HNSW graphs for fast search.",
        "access_level": "internal"
    }

    pid = service.upsert_point(sample_vector, sample_payload)
    print(f"Upserted point ID: {pid}")

    results = service.search_similar({
        "query_vector": [0.12, 0.28, 0.81, 0.39],
        "top_k": 2,
        "filter_category": "architecture"
    })
    print(f"Search results count: {len(results)}")
    if results:
        print(f"Top match score: {results[0]['score']}")
```


## Related tools / concepts

- **[Weaviate](weaviate.md)**: Complementary cloud-native vector database offering GraphQL vector search.
- **[Chroma](chroma.md)**: Embedded vector database popular for local prototype developer workflows.
- **[FastMCP 3.1 Framework](../agents/multi-agent-systems.md)**: High-performance vector memory provider for multi-agent orchestration.


## Sources / references

- [Qdrant Official Documentation](https://qdrant.tech/documentation/)
- [Qdrant Vector Database GitHub Repository](https://github.com/qdrant/qdrant)
- [Qdrant FastMCP 3.1 Vector Search Tool Integration](https://qdrant.tech/documentation/frameworks/mcp/)
- [Vector Quantization Benchmarks in Qdrant](https://qdrant.tech/articles/quantization/)



## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
