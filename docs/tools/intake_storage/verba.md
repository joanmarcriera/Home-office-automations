# Verba

## What it is
Verba is an open-source Retrieval-Augmented Generation (RAG) application built on top of Weaviate. As of June 2026, it is a flagship demonstration of "Modular RAG," allowing users to swap out embedding models, chunking strategies, and LLM backends (including **Claude 4.8** and **GPT-5.5**) through a polished web interface.

## What problem it solves
It provides a user-friendly, production-ready interface for building RAG applications. It solves the complexity of manual data ingestion, vectorization, and retrieval-chain management by handling the entire pipeline out of the box with Weaviate's hybrid search (vector + keyword) capabilities.

## Where it fits in the stack
**Category**: Tool / Knowledge Management / RAG. It serves as the application layer that sits between your data (PDFs, docs) and your inference provider (Ollama, Anthropic, OpenAI).

## Typical use cases
- **Personal Knowledge Base**: Create an AI search engine for your private document collection.
- **Enterprise Q&A**: Deploy a secure internal bot for answering questions based on company wikis.
- **RAG Benchmarking**: Use Verba's modular architecture to compare the performance of different models (e.g., **Claude 4.8 Sonnet** vs **Llama 4 70B**) on specific knowledge sets.
- **Academic Research**: Rapidly ingest and query hundreds of research papers.

## Strengths
- **Modular Design**: Swap components (Readers, Chunkers, Embedders) without changing code.
- **Hybrid Search**: Combines BM25 and vector search for high-precision retrieval.
- **Production-Ready**: Comes with a clean React-based frontend and FastAPI backend.
- **Open Source**: BSD-3-Clause license allows for broad reuse and customization.
- **Multi-Model**: Native support for **Claude 4.8**, **GPT-5.5**, and local models via Ollama.

## Limitations
- **Ecosystem Lock-in**: Closely tied to Weaviate as the primary vector store.
- **Resource Intensive**: Running Weaviate and frontier LLMs locally requires significant RAM (32GB+ recommended).
- **Complexity**: While easy to start, fine-tuning retrieval parameters for complex datasets requires a deep understanding of RAG.

## When to use it
- When you want a professional-grade RAG interface without building the frontend or ingestion logic from scratch.
- When you need to compare different RAG strategies (chunking, embedding) visually.
- If you are already utilizing Weaviate in your infrastructure.

## When not to use it
- If you require a vectorless RAG approach (use [PageIndex](pageindex.md)).
- For extremely simple use cases where a single-file agent (like **Claude Code**) can handle the context.
- If you prefer a P2P, local-first database like [AnyType](anytype.md).

## Getting started
### Docker Deployment (Recommended)
The most reliable way to run Verba is via Docker Compose, which packages the frontend, backend, and Weaviate database.

```bash
git clone https://github.com/weaviate/Verba
cd Verba
# Edit the .env file with your API keys (Anthropic, OpenAI, etc.)
docker compose up -d
```

### PIP Installation
```bash
# Recommended to use a virtual environment
pip install goldenverba
verba start
```

## CLI examples
Verba provides a CLI for environment management and data ingestion.

### Environment Management
```bash
# Check the status of your Verba/Weaviate environment
verba status

# Start the application on a custom port
verba start --port 8080
```

### Data Ingestion
```bash
# Ingest all documents from a specific directory
verba import --path ./knowledge_base/markdown/
```

## API examples
Verba exposes a REST API for programmatic ingestion and querying.

### Querying the RAG Pipeline (Python)
```python
import requests

API_URL = "http://localhost:8000/api/query"
headers = {"Content-Type": "application/json"}

payload = {
    "query": "What are the latest updates for EKS Auto Mode in June 2026?",
    "conversation_id": "session-123",
    "model": "claude-4-8-sonnet"
}

response = requests.post(API_URL, headers=headers, json=payload)
print(response.json()["answer"])
```

### Health Check (Bash)
```bash
curl -X GET http://localhost:8000/api/health
```

## Related tools / concepts
- [Weaviate](../infrastructure/weaviate.md) — The vector database powering Verba.
- [Khoj](khoj.md) — Alternative RAG assistant for personal notes and Emacs/Obsidian.
- [LlamaParse](llamaparse.md) — Used for high-fidelity PDF parsing before Verba ingestion.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) — Underlying architectural concept.
- [Obsidian](../ai_knowledge/obsidian.md) — Commonly used as a primary source for Verba docs.
- [Ollama](../../services/ollama.md) — Supported as a local inference backend for privacy.
- [Claude](../ai_knowledge/claude.md) — Recommended frontier model for Verba reasoning.
- [Unstructured](unstructured.md) — Alternative library for complex document partitioning.

## Sources / references
- [Verba Official Site](https://verba.weaviate.io/)
- [Verba GitHub Repository](https://github.com/weaviate/Verba)
- [Weaviate Documentation](https://weaviate.io/developers/verba)

## Contribution Metadata
- Last reviewed: 2026-06-27
- Confidence: high
