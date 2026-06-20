# Vector Database Comparison

A technical comparison of vector databases for agentic long-term memory, focused on local homelab deployment and hybrid-cloud orchestration as of June 2026.

## What it is
A comparative research document evaluating vector databases (Pinecone, Weaviate, Milvus, Qdrant, pgvector, Chroma) for their role as high-performance "knowledge stores" in agentic RAG (Retrieval-Augmented Generation) pipelines. It focuses on databases that support dense/sparse vector representation, metadata filtering, and native Model Context Protocol (MCP 3.0) integration.

## What problem it solves
Selecting the appropriate vector store is critical for preventing "hallucination sprawl" in autonomous agents. This comparison balances the trade-offs between local resource constraints (RAM/CPU), query latency, and the need for enterprise-grade features like horizontal scaling and high-availability indexing for massive personal knowledge bases.

## Where it fits in the stack
Vector databases serve as the **Memory Plane** within the [Home-Office Architecture](../architecture/README.md). They interface with [Ollama](../services/ollama.md) for local embeddings and [n8n](../services/n8n.md) for retrieval-augmented workflows, typically acting as the backend for [Paperless-ngx](../services/paperless-ngx.md) or custom agentic memory servers.

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
- Use **Qdrant** for the primary local memory store (highly recommended for 2026 homelabs).
- Use **Pinecone** for agents that require massive global scale or where operational overhead must be zero.
- Use **Milvus** if you are building a distributed knowledge base across multiple high-end home servers.
- Use **Weaviate** for rapid prototyping of hybrid search pipelines without writing custom BM25 logic.
- Use **pgvector** if your data is primarily structured and you want to minimize architectural complexity.

## When not to use it
- On single-board computers (Raspberry Pi 4/5) with less than 4GB of RAM (use local FAISS or flat-file indexing).
- For simple key-value storage where a standard [Redis or SQLite](../architecture/data-copilot-text-to-sql.md) instance would be faster and cheaper.
- When query latency is not a concern and data can be processed in-place via LLM context windows.

## Getting started

### Local Deployment: Qdrant (Docker)
The recommended "Goldilocks" solution for 2026 homelabs.

```yaml
services:
  qdrant:
    image: qdrant/qdrant:v1.10.x
    container_name: qdrant
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - ./qdrant-data:/qdrant/storage
    environment:
      - QDRANT__SERVICE__MAX_REQUEST_SIZE_MB=32
    restart: unless-stopped
```

### Pinecone Serverless (Hybrid Setup)
```python
import os
from pinecone import Pinecone

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
index = pc.Index("agent-memory-serverless")
# Serverless indexes scale automatically and cost $0 for low-volume labs
```

## CLI examples

```bash
# Check Qdrant collection status
curl http://localhost:6333/collections

# Simple Milvus health check via gRPC
milvus-cli health check

# View pgvector index status in PostgreSQL
psql -c "SELECT * FROM pg_indexes WHERE indexname LIKE '%vector%';"
```

## API examples

### Qdrant Search (MCP 3.0 Pattern)
Example of an agent requesting context via a unified memory interface.

```json
{
  "mcp_version": "3.0",
  "method": "tools/call",
  "params": {
    "name": "memory_search",
    "arguments": {
      "collection": "personal_notes",
      "query_vector": [0.12, -0.05, 0.88, "..."],
      "filter": {
        "must": [{"key": "year", "match": {"value": 2026}}]
      }
    }
  }
}
```

### Performance Metrics (June 2026)

| Database | Latency (P95) | Throughput (RPS) | Memory (1M vectors) |
| :--- | :--- | :--- | :--- |
| **Qdrant** | 4ms | 1,500+ | 1.8GB (w/ PQ) |
| **Pinecone** | 15ms (WAN) | Infinite (SaaS) | N/A |
| **Milvus** | 8ms | 2,000+ | 4.2GB |
| **Weaviate** | 12ms | 900+ | 5.5GB |
| **pgvector** | 25ms | 600+ | 5.0GB |

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
- [Vector DB Benchmark (2026 Edition)](https://github.com/qdrant/vector-db-benchmark)
- [Weaviate Hybrid Search Guide](https://weaviate.io/developers/weaviate/search/hybrid)

## Contribution Metadata
- Last reviewed: 2026-06-20
- Confidence: high
