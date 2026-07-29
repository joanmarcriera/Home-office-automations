# Verba

## What it is
Verba is an open-source Retrieval-Augmented Generation (RAG) application built on top of Weaviate. It provides a "Golden RAG" experience, focusing on simplicity and high-quality retrieval out of the box.

## What problem it solves
It provides a user-friendly interface for building RAG applications, handling data ingestion, chunking, and querying with LLMs. It solves the complexity of setting up a complete RAG pipeline by providing a unified stack for experimentation and production use.

## Where it fits in the stack
**Category**: Tool / Knowledge Management / RAG. It serves as the application layer on top of a vector database (Weaviate) to enable conversational search over private documents.

## Typical use cases
- Creating a personal knowledge base with AI search.
- Question-answering over private document collections (PDF, Markdown, Text).
- Testing different chunking and retrieval strategies.
- Evaluating model performance (e.g., comparing **Claude 5.1** vs **GPT-5.5**) on specific knowledge sets.

## Strengths
- **Easy Setup**: Reliable Docker-based deployment.
- **Multimodal Support**: Built-in support for multiple data types (PDF, txt, etc.).
- **Native Weaviate Integration**: Leverages Weaviate's advanced vector search, including hybrid search and reranking.
- **Model Flexibility**: Supports latest frontier models like **Llama 4**, **Claude 5.1**, and **GPT-5.5**.

## Limitations
- **Ecosystem Lock-in**: Closely tied to the Weaviate ecosystem.
- **Configuration Overhead**: May require significant tuning for optimal performance with niche or extremely large datasets.
- **UI Constraints**: The built-in frontend is optimized for specific RAG workflows and may not be easily customizable for all enterprise needs.

## When to use it
- When you want a production-ready RAG interface without building it from scratch.
- For prototyping RAG workflows with Weaviate as the backend.
- When you need a local-first RAG solution that can scale to cloud.

## When not to use it
- If you need a highly customized retrieval pipeline that departs significantly from Verba's modular architecture.
- If you are already committed to a different vector database (e.g., Pinecone, Milvus) and do not wish to use Weaviate.

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

# Import data into Verba from a specific path
verba import --path ./my_documents/

# Check the status of the Verba environment and connected components
verba status
```

## API examples
Verba exposes a backend API that can be used to programmatically ingest data or query the RAG pipeline. Late 2026 pipelines must enforce strict request schema validation using **Pydantic v2**.

### Query validation and invocation (Python)
```python
import requests
from pydantic import BaseModel, Field
from typing import Optional

# Define Pydantic v2 validation schema for Verba query endpoint
class VerbaQueryPayload(BaseModel):
    query: str = Field(..., min_length=1, description="The query string for the RAG pipeline")
    conversation_id: Optional[str] = Field(default=None, description="Optional tracker for the conversation context")
    model: str = Field(default="claude-5-1-sonnet-20261022", description="Frontier model targeting the extraction")

# Validate the raw request payload
raw_query_data = {
    "query": "How do I configure the OIDC middleware for Traefik?",
    "model": "claude-5-1-sonnet-20261022"
}

try:
    # Model validation under Pydantic v2 guidelines
    validated_query = VerbaQueryPayload.model_validate(raw_query_data)
    print(f"Validated query string: '{validated_query.query}'")

    url = "http://localhost:8000/api/query"
    # We submit the validated payload dict using model_dump
    # response = requests.post(url, json=validated_query.model_dump(exclude_none=True))
    # print(response.json()["answer"])
except Exception as e:
    print(f"Payload validation failed: {e}")
```

## Related tools / concepts
- [Weaviate](../infrastructure/weaviate.md) — The vector database powering Verba.
- [Khoj](khoj.md) — Alternative RAG assistant for personal notes and desktop search.
- [AnyType](anytype.md) — Local-first P2P knowledge base.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) — Underlying architectural concept for retrieval augmentation.
- [Obsidian](../ai_knowledge/obsidian.md) — Can be used as a primary data source for Verba.
- [LangChain](../ai_knowledge/langchain.md) — Framework often used to extend Verba's capabilities.
- [Ollama](../../services/ollama.md) — Supported as a local inference backend for privacy-first RAG.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standard protocol for connecting Verba to external tools (Standard 3.1).

## Sources / references
- [Official Website](https://verba.weaviate.io/)
- [GitHub Repository](https://github.com/weaviate/Verba)
- [Weaviate Documentation](https://weaviate.io/developers/verba)

## Contribution Metadata
- Last reviewed: 2026-11-01
- Confidence: high
