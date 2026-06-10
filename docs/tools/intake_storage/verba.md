# Verba

## What it is
Verba is an open-source Retrieval-Augmented Generation (RAG) application built on top of Weaviate. As of June 2026, Verba v2.0+ has evolved into an "Agentic RAG" platform, emphasizing modularity and native support for multi-modal data.

## What problem it solves
It provides a user-friendly interface for building RAG applications, handling data ingestion, chunking, and querying with LLMs out of the box. It bridges the gap between raw vector databases and end-user applications by providing a polished UI and pre-configured pipelines for models like Claude 4.8 and GPT-5.5.

## Where it fits in the stack
**Category**: Tool / Knowledge Management / RAG. It serves as the interaction layer for Weaviate-based knowledge bases.

## Typical use cases
- **Personal Knowledge Base**: Creating a searchable AI assistant for private notes and documents.
- **Enterprise Search Lite**: Rapidly prototyping Q&A systems for technical documentation.
- **Agentic Workflows**: Using Verba as a tool within larger agent frameworks via its MCP integration.

## Strengths
- **Native Weaviate Integration**: Leverages Weaviate 1.37+ features including high-performance vector search and HNSW indexing.
- **Agentic Capabilities**: Native support for tool-calling and autonomous retrieval patterns.
- **Multi-modal Support**: Processes text, images, and structured data through unified embedding pipelines.
- **Local-First**: Excellent support for local LLMs via Ollama and Llama 4 Maverick.

## Limitations
- **Ecosystem Lock-in**: Deeply integrated with Weaviate; transitioning to other vector DBs requires significant refactoring.
- **Performance at Scale**: While suitable for homelabs and small teams, massive datasets may require direct Weaviate tuning beyond the Verba UI.

## When to use it
- When you need a production-ready RAG interface with minimal configuration.
- If you are already invested in the Weaviate ecosystem.

## When not to use it
- If you require a vector database other than Weaviate (e.g., Pinecone or Milvus).
- For highly specialized retrieval logic that necessitates a custom LangChain or LlamaIndex implementation.

## Licensing and cost
- **Open Source**: Yes (BSD-3-Clause)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started
### Docker Deployment
The recommended deployment method for stability and performance.

```bash
git clone https://github.com/weaviate/Verba
cd Verba
# Configure .env with your WEAVIATE_URL and API keys
docker compose up -d
```

### PIP Installation
```bash
pip install goldenverba
verba start
```

## CLI examples
Verba provides a CLI for administrative tasks and quick indexing.

```bash
# Ingest a directory of documents
verba ingest --path ./my_docs/

# List configured data providers
verba providers list

# Run a quick query from the terminal
verba query "What are the latest updates to the MCP spec?"
```

## API examples
Verba v2.0+ exposes a REST API and a native MCP server for seamless integration.

### Query via Python
```python
import requests

API_URL = "http://localhost:8000/api/query"
API_TOKEN = "your-secret-token"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "query": "How do I configure the OIDC middleware for Traefik?",
    "conversation_id": "home-admin-01"
}

response = requests.post(API_URL, headers=headers, json=payload)
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
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Native protocol support for agentic tool-calling.
- [Claude Code](../development_ops/claude-code.md) — Can use Verba as a knowledge source via MCP.

## Sources / References
- [Official Website](https://verba.weaviate.io/)
- [GitHub Repository](https://github.com/weaviate/Verba)
- [Weaviate v1.37 Release Notes](https://weaviate.io/blog/weaviate-1-37-release)
- [Verba v2.0 Agentic RAG Announcement](https://weaviate.io/blog/verba-2-0-agentic-rag)

## Contribution Metadata
- Last reviewed: 2026-06-10
- Confidence: high
