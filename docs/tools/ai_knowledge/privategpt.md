# PrivateGPT

## What it is
PrivateGPT is an open-source AI project that enables 100% private, local document processing and conversational search (RAG) over PDFs, Word documents, text files, and audio transcriptions without transmitting data to external third-party LLM providers.

## What problem it solves
Organizations and home lab administrators frequently handle confidential documents (financial records, medical history, proprietary code). Sending these documents to public cloud APIs violates privacy boundaries. PrivateGPT provides a turnkey, local RAG application that combines local LLMs (via Ollama/llama.cpp) and local vector embeddings to keep all document reasoning air-gapped.

## Where it fits in the stack
**AI Assistants & Knowledge**. PrivateGPT functions as a privacy-focused knowledge retrieval application and API, sitting above local vector stores (ChromaDB/Qdrant) and local inference runners.

## Typical use cases
- **Confidential Document Analysis**: Querying family tax records, medical charts, and contracts offline.
- **Air-Gapped Knowledge Base**: Providing local LLM search over local Obsidian vaults or exported Paperless documents.
- **REST API RAG Backend**: Serving structured RAG endpoints for home automation scripts or local chat interfaces.

## Strengths
- **100% Offline & Private**: Zero internet connection required after initial model downloads.
- **Turnkey Setup**: Includes pre-built FastAPI backend and Gradio web interface.
- **Modular Architecture**: Supports multiple LLM backends (Ollama, llama.cpp, OpenAI-compatible APIs) and vector DBs.

## Limitations
- **Hardware Dependent**: RAG response speed depends on local GPU/CPU compute performance.
- **Scalability**: Designed for single-tenant or team deployment rather than multi-tenant SaaS.

## When to use it
- When requiring an out-of-the-box local RAG web application and API for private document search.
- When querying sensitive documents offline without cloud LLM dependencies.
- When setting up an air-gapped knowledge assistant for local family or lab use.

## When not to use it
- When searching massive multi-terabyte public datasets requiring cloud-scale distributed search clusters.
- When simple static keyword search (like ripgrep) is sufficient for un-embedded text files.

## Getting started
To run PrivateGPT locally with Ollama support:

```bash
# Clone and install dependencies
git clone https://github.com/zylon-ai/private-gpt
cd private-gpt
poetry install --extras "ui vector-stores-qdrant llms-ollama embeddings-ollama"

# Set Ollama mode in settings.yaml and launch
PGPT_PROFILES=ollama make run
```

## CLI examples

```bash
# Launch PrivateGPT in Ollama mode using Makefile CLI
PGPT_PROFILES=ollama make run

# Ingest a document file into PrivateGPT via CLI
python scripts/ingest_folder.py --dir /data/documents
```

## API examples

### 1. Pydantic v2 Schema for PrivateGPT Ingestion Payload
```python
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

class IngestDocumentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    file_name: str = Field(..., description="Name of the file being ingested")
    content: str = Field(..., description="Extracted plain text or OCR content")
    tags: List[str] = Field(default_factory=list, description="Categorization tags")

class IngestDocumentResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    doc_id: str
    status: str
    chunks_indexed: int

def ingest_private_document(req: IngestDocumentRequest) -> IngestDocumentResponse:
    # Simulated local ingestion pipeline execution
    return IngestDocumentResponse(
        doc_id="doc_98765",
        status="indexed",
        chunks_indexed=len(req.content) // 500 + 1
    )

if __name__ == "__main__":
    req = IngestDocumentRequest(file_name="tax_2026.pdf", content="Confidential tax return details...", tags=["finance"])
    res = ingest_private_document(req)
    print(f"Ingested {req.file_name} -> ID: {res.doc_id}, Chunks: {res.chunks_indexed}")
```

### 2. FastMCP 3.1 Task Protocol Integration
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("privategpt-service")

@mcp.tool()
def query_private_documents(prompt: str, top_k: int = 3) -> dict:
    """Executes a private, local RAG query over PrivateGPT indexed documents."""
    return {"prompt": prompt, "answer": "Synthesized answer from local document context", "sources": ["tax_2026.pdf"]}
```

## Related tools / concepts
- [Ollama](../../services/ollama.md) — Local model inference engine.
- [ChromaDB](../infrastructure/chroma.md) — Local vector database.
- [Local Embedding Models](../infrastructure/local-embeddings.md) — Offline embeddings for RAG.

## Sources / references
- [PrivateGPT GitHub Repository](https://github.com/zylon-ai/private-gpt)
- [PrivateGPT Documentation](https://docs.privategpt.dev/)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
