# Vector Database Comparison (Local Homelab)

## What it is
A comparison of vector databases suitable for self-hosted environments, focusing on those that can be run on consumer hardware or home servers (e.g., TrueNAS, Docker).

## What problem it solves
Selecting a vector database for local RAG (Retrieval-Augmented Generation) requires balancing resource usage (RAM/CPU), persistence, and ease of integration with tools like n8n, LangChain, and LlamaIndex.

## Where it fits in the stack
It serves as the long-term memory for local AI agents, storing embeddings for scanned manuals, family journals, and historical documents.

## Typical use cases
- Semantic search across OCR'd PDFs in Paperless-ngx.
- Context retrieval for a local "Home Admin Agent."
- Indexing personal notes from Obsidian for natural language queries.

## Strengths
- **Chroma**: Extremely easy to set up, "it just works" philosophy, great for prototyping.
- **Milvus**: High performance, scalable, features a rich ecosystem and management UI (Attu).
- **Qdrant**: Rust-based, very efficient, native support for many distance metrics, and a clean API.

## Limitations
- **Chroma**: Can be harder to manage in a multi-container production environment compared to dedicated servers.
- **Milvus**: Higher resource overhead; better suited for larger datasets or dedicated hardware.
- **Qdrant**: Slightly steeper learning curve for advanced filtering compared to Chroma.

## When to use it
- Use **Chroma** for quick projects or when running on very limited hardware.
- Use **Milvus** if you plan to index millions of vectors and need horizontal scaling.
- Use **Qdrant** for a balanced "goldilocks" solution that is both fast and robust.

## When not to use it
- Do not use a dedicated vector DB if your dataset is small enough to fit in a simple flat file or `FAISS` index.
- Avoid Milvus if you are running on a machine with less than 4GB of RAM dedicated to the database.

## Related tools / concepts
- [RAG Patterns](../patterns/rag.md)
- [Ollama](../../services/ollama.md)
- [n8n](../../services/n8n.md)

## Sources / references
- [Chroma Documentation](https://docs.trychroma.com/)
- [Milvus Documentation](https://milvus.io/docs)
- [Qdrant Documentation](https://qdrant.tech/documentation/)

## Contribution Metadata
- Last reviewed: 2026-04-18
- Confidence: high
