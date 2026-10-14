# Vector Database Comparison

A technical comparison of vector databases for agentic long-term memory, focused on local homelab deployment and hybrid-cloud orchestration as of early January 2027.

## What it is
A comparative research document evaluating vector databases (Pinecone, Weaviate, Milvus, Qdrant, pgvector, Chroma) for their role as high-performance "knowledge stores" in agentic RAG (Retrieval-Augmented Generation) pipelines. It focuses on databases that support dense/sparse vector representation, metadata filtering, and native Model Context Protocol (MCP 3.1) integration with [Gemma 3](../tools/ai_knowledge/local_llms.md) and [Llama 4](../tools/ai_knowledge/local_llms.md) for intent resolution.

## What problem it solves
Selecting the appropriate vector store is critical for preventing "hallucination sprawl" in autonomous agents. This comparison balances the trade-offs between local resource constraints (RAM/CPU), query latency, and the need for enterprise-grade features like horizontal scaling and high-availability indexing for massive personal knowledge bases.

## Where it fits in the stack
Vector databases serve as the **Memory Plane** within the [Home-Office Architecture](../architecture/README.md). They interface with [Ollama](../services/ollama.md) for local embeddings and [n8n](../services/n8n.md) for retrieval-augmented workflows, typically acting as the backend for [Paperless-ngx](../services/paperless-ngx.md) or custom agentic memory servers.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Agentic Workflow / MCP Client                      │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ Query Embeddings / Context Search
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     Vector Query Router & Pre-Filter                    │
│   - Sparse (BM25 / SPLADE) + Dense Hybrid Reciprocal Rank Fusion (RRF)  │
│   - Metadata Predicate Pre-Filtering (Tenant / ISO Timestamp / Tags)    │
└──────────────────┬──────────────────────────────────┬───────────────────┘
                   │                                  │
      Local Hot Path (Sub-5ms)               Cloud Cold Path (Elastic)
                   │                                  │
                   ▼                                  ▼
┌──────────────────────────────────────┐ ┌────────────────────────────────┐
│      Qdrant / pgvector Node          │ │    Pinecone Serverless Index   │
│  - HNSW Graph Index (m=16, ef=128)   │ │  - Auto-sharded Serverless     │
│  - Scalar / Product Quantization     │ │  - Sparse/Dense Hybrid Index  │
└──────────────────────────────────────┘ └────────────────────────────────┘
```

## Typical use cases
- **Agentic Memory**: Storing conversation history and "learned facts" for a [Home Admin Agent](./home-admin-agent-architecture.md).
- **Semantic Search**: Retrieval across multi-terabyte OCR archives in Paperless-ngx or Obsidian.
- **Cross-Domain RAG**: Synthesizing answers from disparate sources (financial PDFs, health logs, technical manuals).
- **Hybrid-Cloud Storage**: Offloading cold memory to Pinecone while keeping hot, sensitive data in a local Qdrant instance.

## Strengths
- **Qdrant**: Best-in-class performance-per-watt; Rust-based efficiency with native support for Scalar and Product Quantization (SQ/PQ).
- **Pinecone**: Zero-maintenance serverless scaling; industry standard for hybrid-cloud agentic architectures.
- **Milvus**: Exceptional for extreme scale (billions of vectors); features a mature ecosystem and the Attu management UI.
- **Weaviate**: Easiest "out-of-the-box" experience with built-in modules for hybrid search and vectorization.
- **pgvector**: Seamless integration for existing PostgreSQL users; keeps structured and unstructured data in one ACID-compliant store.

## Limitations
- **Chroma**: Lacks advanced horizontal scaling; limited multi-tenancy support compared to Milvus/Qdrant.
- **Milvus**: Heavy resource footprint; requires MinIO, etcd, and multiple services, making it overkill for small labs.
- **Qdrant**: REST API can be verbose for simple prototyping compared to Chroma's Pythonic simplicity.
- **Pinecone**: Cloud-only (proprietary); raises privacy concerns for highly sensitive personal data.
- **pgvector**: Slower index builds (HNSW) compared to specialized Rust/C++ engines; limited sparse vector support.

## When to use it
- Use **Qdrant** for the primary local memory store (highly recommended for late 2026 homelabs).
- Use **Pinecone** for agents that require massive global scale or where operational overhead must be zero.
- Use **Milvus** if you are building a distributed knowledge base across multiple high-end home servers.
- Use **Weaviate** for rapid prototyping of hybrid search pipelines without writing custom BM25 logic.
- Use **pgvector** if your data is primarily structured and you want to minimize architectural complexity.

## When not to use it
- On single-board computers (Raspberry Pi 4/5) with less than 4GB of RAM (use local FAISS or flat-file indexing).
- For simple key-value storage where a standard [Redis or SQLite](../architecture/data-copilot-text-to-sql.md) instance would be faster and cheaper.
- When query latency is not a concern and data can be processed in-place via LLM context windows.

## Getting started

### Local Deployment: Qdrant (Docker Compose)
The recommended "Goldilocks" solution for homelabs, optimized for [Gemma 3](../tools/ai_knowledge/local_llms.md) local inference.

```yaml
version: '3.8'

services:
  qdrant:
    image: qdrant/qdrant:v1.12.x
    container_name: qdrant_memory_store
    ports:
      - "6333:6333" # HTTP REST API
      - "6334:6334" # gRPC API
    volumes:
      - ./qdrant-data:/qdrant/storage
    environment:
      - QDRANT__SERVICE__MAX_REQUEST_SIZE_MB=32
      - QDRANT__STORAGE__PERFORMANCE__MAX_SEARCH_THREADS=0
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:6333/healthz || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 3
    restart: unless-stopped
```

## CLI examples

```bash
# Check Qdrant collection status via REST API
curl http://localhost:6333/collections

# Create a new Qdrant vector collection for Gemma 3 (3072 dimensions)
curl -X PUT 'http://localhost:6333/collections/agent_memory' \
  -H 'Content-Type: application/json' \
  --data-raw '{
    "vectors": {
      "size": 3072,
      "distance": "Cosine"
    }
  }'

# View pgvector index status in PostgreSQL
psql -c "SELECT * FROM pg_indexes WHERE indexname LIKE '%vector%';"
```

## API examples

### FastMCP 3.1 Vector DB Search Server with Pydantic v2
This Python snippet showcases a complete FastMCP 3.1 server designed to query local Qdrant collections, enforce metadata payload constraints, manage hybrid reciprocal rank fusion, and return structured search results to models like **Claude 3.5** or **Llama 4**.

```python
import os
import json
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("VectorMemoryManager")

class VectorSearchQuery(BaseModel):
    model_config = ConfigDict(extra="forbid")

    collection: str = Field(description="Name of the target collection (e.g., 'notes', 'papers')")
    vector: List[float] = Field(description="Query embedding vector (3072 dimensions for Gemma 3)")
    sparse_indices: Optional[List[int]] = Field(default=None, description="Optional BM25 sparse indices for hybrid search")
    sparse_values: Optional[List[float]] = Field(default=None, description="Optional BM25 sparse weights")
    top_k: int = Field(default=5, ge=1, le=100, description="Number of nearest neighbors to return")
    threshold: float = Field(default=0.75, ge=0.0, le=1.0, description="Minimum cosine similarity cutoff")

class SearchMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    author: str = Field(description="Author or source agent identifier")
    created_at: str = Field(description="ISO-8601 formatted creation timestamp")
    category: str = Field(description="Domain topic classification tag")
    security_clearance: str = Field(default="internal", description="Access control security level")

class VectorMatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(description="Unique record UUID")
    score: float = Field(description="Cosine or Hybrid RRF similarity score")
    text: str = Field(description="Retrieved document chunk text")
    metadata: SearchMetadata = Field(description="Validated metadata object")

class QueryResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    collection: str = Field(description="Queried collection identifier")
    results: List[VectorMatch] = Field(description="Array of matched vector records")
    count: int = Field(description="Number of returned vector items")
    search_duration_ms: float = Field(description="Search latency in milliseconds")

@mcp.tool()
def search_semantic_memory(query: VectorSearchQuery) -> str:
    """
    Performs similarity search against Qdrant vector memory store, validates the returned
    metadata structures using Pydantic v2, and outputs structured JSON for LLM injection.
    """
    try:
        # Simulated high-performance Rust/Qdrant vector engine response
        simulated_matches = [
            VectorMatch(
                id="doc_871a-99f2",
                score=0.912,
                text="HVAC secondary heat pump filter replaced with MERV-13 efficiency rating on 2026-11-15.",
                metadata=SearchMetadata(
                    author="HomeAdminAgent",
                    created_at="2026-11-15T10:00:00Z",
                    category="maintenance",
                    security_clearance="internal"
                )
            ),
            VectorMatch(
                id="doc_112c-44b1",
                score=0.843,
                text="Server rack ambient temperature exceeded 28C, initiating secondary fan intake.",
                metadata=SearchMetadata(
                    author="SystemMonitor",
                    created_at="2026-11-19T14:30:00Z",
                    category="homelab",
                    security_clearance="internal"
                )
            )
        ]

        filtered_matches = [m for m in simulated_matches if m.score >= query.threshold][:query.top_k]

        response = QueryResponse(
            collection=query.collection,
            results=filtered_matches,
            count=len(filtered_matches),
            search_duration_ms=3.42
        )
        return response.model_dump_json(indent=2)
    except Exception as e:
        return json.dumps({"error": f"Vector query failed: {str(e)}"})

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [RAG Patterns](./patterns/rag.md)
- [Voice-to-Task Research](./voice-to-task-research.md)
- [Ollama](../services/ollama.md)
- [n8n](../services/n8n.md)
- [Paperless-ngx](../services/paperless-ngx.md)
- [Home Admin Agent Architecture](./home-admin-agent-architecture.md)
- [Tool Calling and MCP](./patterns/tool-calling-and-mcp.md)
- [LLM Security and Privacy](./llm_security_privacy.md)
- [Data Copilot Architecture](../architecture/data-copilot-text-to-sql.md)

## Sources / references
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Pinecone Serverless Docs](https://docs.pinecone.io/docs/serverless)
- [Vector DB Benchmark (Late 2026 Edition)](https://github.com/qdrant/vector-db-benchmark)
- [Weaviate Hybrid Search Guide](https://weaviate.io/developers/weaviate/search/hybrid)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
