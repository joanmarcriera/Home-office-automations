# Verba

## What it is
Verba is an open-source Retrieval-Augmented Generation (RAG) application built on top of Weaviate.

## What problem it solves
It provides a user-friendly interface for building RAG applications, handling data ingestion, chunking, and querying with LLMs out of the box.

## Where it fits in the stack
**Category**: Tool / Knowledge Management / RAG

## Typical use cases
- Creating a personal knowledge base with AI search.
- Question-answering over private document collections.
- Testing different chunking and retrieval strategies.
- Evaluating model performance (e.g., comparing Claude 4.7 vs GPT-5.5) on specific knowledge sets.

## Strengths
- Easy to set up with Docker.
- Built-in support for multiple data types (PDF, txt, etc.).
- Native integration with Weaviate's vector search capabilities.
- Support for latest frontier models like Llama 4 Maverick and Claude 4.7.

## Limitations
- Closely tied to the Weaviate ecosystem.
- May require configuration for optimal performance with specific datasets.

## When to use it
- When you want a production-ready RAG interface without building it from scratch.

## When not to use it
- If you need a highly customized retrieval pipeline that departs significantly from Verba's architecture.

## Licensing and cost
- **Open Source**: Yes (BSD-3-Clause)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started
### Docker Deployment
The most reliable way to run Verba is via Docker Compose, which packages the frontend, backend, and Weaviate database.

```bash
git clone https://github.com/weaviate/Verba
cd Verba
# Set your API keys in the .env file
docker compose up -d
```

### PIP Installation
```bash
pip install goldenverba
verba start
```

## CLI examples
Verba provides a CLI for managing the application and data.

```bash
# Start the Verba server
verba start

# Import data into Verba
verba import --path ./my_documents/

# Check the status of the Verba environment
verba status
```

## API examples
Verba exposes a backend API that can be used to programmatically ingest data or query the RAG pipeline.

### Query via Python
```python
import requests

url = "http://localhost:8000/api/query"
payload = {
    "query": "How do I configure the OIDC middleware for Traefik?",
    "conversation_id": "optional-id"
}

response = requests.post(url, json=payload)
print(response.json()["answer"])
```

## Related tools / concepts
- [Weaviate](../infrastructure/weaviate.md) — The vector database powering Verba.
- [Khoj](khoj.md) — Alternative RAG assistant for personal notes.
- [AnyType](anytype.md) — Local-first P2P knowledge base.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) — Underlying architectural concept.
- [Obsidian](../ai_knowledge/obsidian.md) — Can be used as a data source via Markdown export.
- [LangChain](../ai_knowledge/langchain.md) — Often used in conjunction with Weaviate for custom pipelines.
- [Ollama](../../services/ollama.md) — Supported as a local inference backend.
- [GPT-5.5](../ai_knowledge/openai.md) — Large language model often used with Verba.

## Sources / References
- [Official Website](https://verba.weaviate.io/)
- [GitHub Repository](https://github.com/weaviate/Verba)
- [Weaviate Documentation](https://weaviate.io/developers/verba)

## Contribution Metadata
- Last reviewed: 2026-06-08
- Confidence: high
