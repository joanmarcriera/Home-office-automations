# Vector Database Comparison (Local Homelab)

## What it is
A comparison of vector databases suitable for self-hosted environments, focusing on those that can be run on consumer hardware or home servers (e.g., TrueNAS, Docker, K3s). It evaluates their suitability for long-term memory in AI agent workflows.

## What problem it solves
Selecting a vector database for local RAG (Retrieval-Augmented Generation) requires balancing resource usage (RAM/CPU), persistence, and ease of integration with tools like n8n, LangChain, and LlamaIndex. This guide prevents "over-engineering" by matching database capabilities to homelab constraints.

## Where it fits in the stack
It serves as the **long-term memory layer** for local AI agents, storing embeddings for scanned manuals, family journals, and historical documents. It sits between the [Inference Layer](../architecture/README.md) and the [Application Layer](../architecture/README.md).

## Typical use cases
- Semantic search across OCR'd PDFs in [Paperless-ngx](../services/paperless-ngx.md).
- Context retrieval for a local [Home Admin Agent](./home-admin-agent-architecture.md).
- Indexing personal notes from [Obsidian](../tools/ai_knowledge/obsidian.md) for natural language queries.
- Storing audit trails for LLM decisions in [Data Copilot](../architecture/data-copilot-text-to-sql.md).

## Strengths
- **Chroma**: Extremely easy to set up, "it just works" philosophy, great for prototyping and single-user labs.
- **Milvus**: High performance, horizontally scalable, features a rich ecosystem and management UI (Attu). Best for massive datasets.
- **Qdrant**: Rust-based, very efficient, native support for many distance metrics, and a clean REST/gRPC API. Excellent performance-per-watt.

## Limitations
- **Chroma**: Can be harder to manage in a multi-container production environment; persistent storage handling in K3s requires specific volume configurations.
- **Milvus**: Higher resource overhead (requires MinIO, etcd); better suited for larger datasets or dedicated hardware.
- **Qdrant**: Slightly steeper learning curve for advanced filtering and payload indexing compared to Chroma's simple collection API.

## When to use it
- Use **Chroma** for quick projects, individual research logs, or when running on very limited hardware (e.g., 8GB RAM total).
- Use **Milvus** if you plan to index millions of vectors, require distributed search, and have 16GB+ of RAM to spare.
- Use **Qdrant** for a balanced "goldilocks" solution that is both fast, robust, and native to the n8n ecosystem via community nodes.

## When not to use it
- Do not use a dedicated vector DB if your dataset is small enough (under 1,000 items) to fit in a simple flat file or `FAISS` index stored in memory.
- Avoid Milvus on resource-constrained ARM nodes (Raspberry Pi) due to its multi-component overhead.
- Don't use a vector DB for structured data queries that are better handled by [PostgreSQL or SQLite](../architecture/data-copilot-text-to-sql.md).

## Comparison Matrix

| Feature | Chroma | Qdrant | Milvus |
| :--- | :--- | :--- | :--- |
| **Primary Language** | Python / JS | Rust | Go / Python / C++ |
| **Deployment** | Docker / Embedded | Docker / K8s | Distributed / Docker |
| **Filtering** | Basic (Metadata) | Advanced (Payload) | Advanced (Expression) |
| **Resource Usage** | Low | Medium-Low | High |
| **n8n Support** | Native Node | Native Node | Webhook / Python |

## Getting started

### Docker Compose for Qdrant (Recommended)
Qdrant is the recommended starting point for most homelabs due to its efficiency and dashboard.

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
```

## API examples (Python)
Using the `qdrant-client` library for a simple insertion and search:

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient("localhost", port=6333)

# Create a collection
client.recreate_collection(
    collection_name="family_history",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)

# Search with a dummy vector
results = client.search(
    collection_name="family_history",
    query_vector=[0.1] * 1536,
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

## Sources / references
- [Chroma Documentation](https://docs.trychroma.com/)
- [Milvus Documentation](https://milvus.io/docs)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Vector Database Benchmarks](https://github.com/qdrant/vector-db-benchmark)

## Contribution Metadata
- Last reviewed: 2026-05-28
- Confidence: high
