# Vector Database Comparison (Local Homelab)

## What it is
A comparison of vector databases suitable for self-hosted environments, focusing on those that can be run on consumer hardware or home servers (e.g., TrueNAS, Docker, K3s). It evaluates their suitability for long-term memory in AI agent workflows as of May 2026.

## What problem it solves
Selecting a vector database for local RAG (Retrieval-Augmented Generation) requires balancing resource usage (RAM/CPU), persistence, and ease of integration with tools like n8n, LangChain, and LlamaIndex. This guide prevents "over-engineering" by matching database capabilities to homelab constraints.

## Where it fits in the stack
It serves as the **long-term memory layer** for local AI agents, storing embeddings for scanned manuals, family journals, and historical documents. It sits between the [Inference Layer](../architecture/README.md) and the [Application Layer](../architecture/README.md).

## Typical use cases
- Semantic search across OCR'd PDFs in [Paperless-ngx](../services/paperless-ngx.md).
- Context retrieval for a local [Home Admin Agent](./home-admin-agent-architecture.md).
- Indexing personal notes from [Obsidian](../tools/ai_knowledge/obsidian.md) for natural language queries.
- Storing audit trails for LLM decisions in [Data Copilot](../architecture/data-copilot-text-to-sql.md).
- **Hybrid Search**: Combining keyword search (BM25) with vector similarity for precise technical term retrieval.
- **Multi-modal Memory**: Storing image and audio embeddings for whole-home event analysis.

## Strengths
- **Chroma**: Extremely easy to set up, "it just works" philosophy, great for prototyping and single-user labs. Now supports basic multi-tenancy and improved persistence in v0.6+.
- **Milvus**: High performance, horizontally scalable, features a rich ecosystem and management UI (Attu). Best for massive datasets (billions of vectors).
- **Qdrant**: Rust-based, very efficient, native support for many distance metrics, and a clean REST/gRPC API. Excellent performance-per-watt and advanced **Scalar/Product Quantization** for memory saving.
- **Weaviate**: Feature-rich with built-in modules for vectorization (text2vec) and hybrid search (BM25 + vector) out of the box. Excellent for "all-in-one" implementations.
- **pgvector**: Minimal overhead if you already run PostgreSQL. Standard SQL interface and ACID compliance.

## Limitations
- **Chroma**: Can be harder to manage in a multi-container production environment; lacks advanced hybrid search compared to Qdrant or Weaviate.
- **Milvus**: Higher resource overhead (requires MinIO, etcd); better suited for larger datasets or dedicated hardware (16GB+ RAM baseline).
- **Qdrant**: Slightly steeper learning curve for advanced filtering and payload indexing compared to Chroma's simple collection API.
- **Weaviate**: Memory consumption can be high for large HNSW indexes; complex configuration for multi-node clusters.
- **pgvector**: Indexing (HNSW/IVFFlat) is slower than dedicated vector DBs; limited specialized vector operations.

## Performance Metrics (2026 Baseline)

| Database | Latency (ms) | Throughput (RPS) | Memory per 1M (1536-dim) |
| :--- | :--- | :--- | :--- |
| **Qdrant (Rust)** | 5-10ms | 1,200+ | ~2GB (with Quantization) |
| **Weaviate (Go)** | 12-25ms | 800+ | ~6GB |
| **Chroma (Python)** | 30-50ms | 300+ | ~8GB |
| **pgvector (C)** | 20-40ms | 500+ | ~6GB |

## When to use it
- Use **Chroma** for quick projects, individual research logs, or when running on very limited hardware (e.g., 8GB RAM total).
- Use **Milvus** if you plan to index millions of vectors, require distributed search, and have 32GB+ of RAM to spare.
- Use **Qdrant** for a balanced "goldilocks" solution that is both fast, robust, and native to the n8n ecosystem. Recommended for most 2026 homelabs.
- Use **Weaviate** if you want built-in hybrid search and modular embedding pipelines without external scripts.
- Use **pgvector** if you are already using PostgreSQL for your application data and want to avoid adding another service.

## When not to use it
- Do not use a dedicated vector DB if your dataset is small enough (under 1,000 items) to fit in a simple flat file or `FAISS` index stored in memory.
- Avoid Milvus on resource-constrained ARM nodes (Raspberry Pi) due to its multi-component overhead.
- Don't use a vector DB for structured data queries that are better handled by [PostgreSQL or SQLite](../architecture/data-copilot-text-to-sql.md).

## Comparison Matrix

| Feature | Chroma | Qdrant | Milvus | Weaviate | pgvector |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Implementation** | Python / JS | Rust | Go / Python / C++ | Go | C (Postgres) |
| **Deployment** | Docker / Embedded | Docker / K8s | Distributed / Docker | Docker / K8s | Postgres Ext |
| **Hybrid Search** | Limited | Yes (Sparse+Dense) | Yes | Yes (BM25) | Yes (via FTS) |
| **Quantization** | No | Yes (SQ/PQ) | Yes | Yes (PQ) | No |
| **n8n Support** | Native Node | Native Node | Webhook / Python | Native Node | Postgres Node |

## Deployment Patterns

### Pattern 1: The "Minimalist" (pgvector)
Run as an extension in your existing Postgres instance.
```sql
CREATE EXTENSION vector;
CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(1536));
```

### Pattern 2: The "Performance Lab" (Qdrant)
Dedicated Rust-based engine for high-speed agentic memory.

```yaml
services:
  qdrant:
    image: qdrant/qdrant:latest
    container_name: qdrant
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - ./qdrant-data:/qdrant/storage
    restart: unless-stopped
```

## CLI examples

```bash
# Check Qdrant collection status via REST API
curl http://localhost:6333/collections

# Simple health check
curl http://localhost:6333/healthz

# Inspect Chroma version
curl http://localhost:8000/api/v1/version
```

## API examples (Python)
Using the `qdrant-client` library with metadata filtering:

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, Filter, FieldCondition, MatchValue

client = QdrantClient("localhost", port=6333)

# Create a collection with HNSW configuration
client.recreate_collection(
    collection_name="manuals",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)

# Search with metadata filtering (e.g., only search within 'service_manuals')
results = client.search(
    collection_name="manuals",
    query_vector=[0.1] * 1536,
    query_filter=Filter(
        must=[FieldCondition(key="category", match=MatchValue(value="service_manuals"))]
    ),
    limit=5
)
print(results)
```

## Related tools / concepts
- [RAG Patterns](./patterns/rag.md)
- [Ollama](../services/ollama.md)
- [n8n](../services/n8n.md)
- [Paperless-ngx](../services/paperless-ngx.md)
- [Obsidian](../tools/ai_knowledge/obsidian.md)
- [Data Copilot](../architecture/data-copilot-text-to-sql.md)
- [Architecture](../architecture/README.md)
- [Home Admin Agent Architecture](./home-admin-agent-architecture.md)
- [Tool Calling and MCP](./patterns/tool-calling-and-mcp.md)

## Sources / references
- [Chroma Documentation](https://docs.trychroma.com/)
- [Milvus Documentation](https://milvus.io/docs)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Weaviate Documentation](https://weaviate.io/developers/weaviate)
- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [Vector Database Benchmarks (2026)](https://github.com/qdrant/vector-db-benchmark)

## Contribution Metadata
- Last reviewed: 2026-05-28
- Confidence: high
