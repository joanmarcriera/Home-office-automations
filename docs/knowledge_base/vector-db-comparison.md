# Vector Database Comparison (Local Homelab)

## What it is
A comparison of vector databases suitable for self-hosted environments, focusing on those that can be run on consumer hardware or home servers (e.g., TrueNAS, Docker, K3s). It evaluates their suitability for long-term memory in AI agent workflows as of June 2026, incorporating benchmarks for Pinecone, Weaviate, and Milvus in agentic RAG pipelines.

## What problem it solves
Selecting a vector database for local RAG (Retrieval-Augmented Generation) requires balancing resource usage (RAM/CPU), persistence, and ease of integration with tools like n8n, LangChain, and LlamaIndex. This guide prevents "over-engineering" by matching database capabilities to homelab constraints.

## Where it fits in the stack
It serves as the **long-term memory layer** for local AI agents, storing embeddings for scanned manuals, family journals, and historical documents. It sits between the [Inference Layer](../architecture/README.md) and the [Application Layer](../architecture/README.md).

## Typical use cases
- **Semantic Search**: Searching across OCR'd PDFs in [Paperless-ngx](../services/paperless-ngx.md).
- **Agentic Memory**: Providing context for a [Home Admin Agent](./home-admin-agent-architecture.md).
- **Hybrid Search**: Combining keyword search (BM25) with vector similarity for precise technical term retrieval.
- **Multi-modal Memory**: Storing image (CLIP) and audio embeddings for whole-home event analysis.
- **Knowledge Synthesis**: Indexing personal notes from [Obsidian](../tools/ai_knowledge/obsidian.md) for natural language queries.

## Strengths
- **Qdrant**: Rust-based, extremely efficient, native support for many distance metrics, and a clean REST/gRPC API. Excellent performance-per-watt and advanced **Scalar/Product Quantization**.
- **Milvus (Zilliz)**: High performance, horizontally scalable, best for massive datasets (billions of vectors). Includes native support for **Multi-vector** search and partition keys.
- **Weaviate**: Feature-rich with built-in modules for vectorization (text2vec) and hybrid search (BM25 + vector). Excellent for "all-in-one" implementations.
- **pgvector**: Minimal overhead if you already run PostgreSQL. Standard SQL interface and ACID compliance.
- **Chroma**: Extremely easy to set up, "it just works" philosophy, great for prototyping.

## Limitations
- **Milvus**: Higher resource overhead (requires MinIO, etcd); better suited for larger datasets or dedicated hardware (16GB+ RAM baseline).
- **Weaviate**: Memory consumption can be high for large HNSW indexes; complex configuration for multi-node clusters.
- **pgvector**: Indexing (HNSW/IVFFlat) is slower than dedicated vector DBs; limited specialized multi-modal operations.
- **Pinecone**: Cloud-only; unsuitable for 100% private, zero-egress homelabs, though often used as a baseline for performance.

## Performance Metrics (June 2026 Baseline)

| Database | Latency (ms) | Throughput (RPS) | Memory per 1M (1536-dim) | Homelab Rating |
| :--- | :--- | :--- | :--- | :--- |
| **Qdrant (Rust)** | 5-10ms | 1,200+ | ~2GB (with Quantization) | ⭐⭐⭐⭐⭐ |
| **Weaviate (Go)** | 12-25ms | 800+ | ~6GB | ⭐⭐⭐⭐ |
| **Milvus (Go/C++)**| 8-15ms | 1,100+ | ~5GB (v2.5+) | ⭐⭐⭐ |
| **pgvector (C)** | 20-40ms | 500+ | ~6GB | ⭐⭐⭐⭐ |
| **Pinecone (Cloud)**| 20-50ms | N/A | N/A | ⭐ |

## When to use it
- Use **Qdrant** for a balanced "goldilocks" solution that is both fast, robust, and native to the n8n ecosystem. Recommended for most 2026 homelabs.
- Use **Milvus** if you plan to index millions of vectors, require distributed search, and have 32GB+ of RAM to spare.
- Use **Weaviate** if you want built-in hybrid search and modular embedding pipelines without external scripts.
- Use **pgvector** if you are already using PostgreSQL for your application data and want to avoid adding another service.

## When not to use it
- Do not use a dedicated vector DB if your dataset is small enough (under 1,000 items) to fit in a simple flat file or `FAISS` index.
- Avoid Milvus on resource-constrained ARM nodes (Raspberry Pi) due to its multi-component overhead.
- Don't use a vector DB for structured data queries that are better handled by [PostgreSQL or SQLite](../architecture/data-copilot-text-to-sql.md).

## Getting started

### Qdrant (Docker)
The recommended choice for 2026 homelabs.

```yaml
services:
  qdrant:
    image: qdrant/qdrant:latest
    container_name: qdrant
    ports:
      - "6333:6333"
    volumes:
      - ./qdrant-data:/qdrant/storage
    restart: unless-stopped
```

## CLI examples

### Health Check (Qdrant)
```bash
curl http://localhost:6333/healthz
```

### Inspect Collections (Milvus)
```bash
# Using the Milvus CLI
milvus-cli list collections
```

## API examples

### Python: Hybrid Search with Qdrant
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

client = QdrantClient("localhost", port=6333)

results = client.search(
    collection_name="homelab_docs",
    query_vector=[0.1] * 1536,
    query_filter=Filter(
        must=[FieldCondition(key="category", match=MatchValue(value="manuals"))]
    ),
    limit=5
)
```

## Related tools / concepts
- [RAG Patterns](./patterns/rag.md) - The primary use case for vector DBs.
- [Ollama](../services/ollama.md) - For generating embeddings locally.
- [n8n](../services/n8n.md) - For orchestrating ingestion pipelines.
- [Paperless-ngx](../services/paperless-ngx.md) - Document management system.
- [Obsidian](../tools/ai_knowledge/obsidian.md) - Personal knowledge base.
- [Data Copilot](../architecture/data-copilot-text-to-sql.md) - For structured vs unstructured data.
- [Architecture](../architecture/README.md) - High-level placement.
- [Home Admin Agent Architecture](./home-admin-agent-architecture.md) - The reasoning layer.
- [Tool Calling and MCP](./patterns/tool-calling-and-mcp.md) - Agentic tool execution.
- [Ragas](../tools/process_understanding/ragas.md) - Evaluation framework for RAG.

## Sources / references
- [Vector Database Benchmark (2026)](https://github.com/qdrant/vector-db-benchmark)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Milvus Documentation](https://milvus.io/docs)
- [Weaviate Documentation](https://weaviate.io/developers/weaviate)
- [pgvector GitHub](https://github.com/pgvector/pgvector)

## Contribution Metadata
- Last reviewed: 2026-06-20
- Confidence: high
