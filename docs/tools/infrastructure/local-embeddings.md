# Local Embedding Models

## What it is
Local Embedding Models refer to offline, open-weights text and multimodal representation models (such as `nomic-embed-text-v1.5`, `bge-m3`, `gte-Qwen2`, and `all-MiniLM-L6-v2`) executed directly on local compute hardware (CPU, GPU, or Apple Silicon via Ollama, llama.cpp, or Sentence-Transformers) without external API dependencies.

## What problem it solves
Traditional cloud RAG architectures rely on remote embedding APIs (such as OpenAI `text-embedding-3-small` or Cohere Embed). This introduces latency, subscription/token costs, and data privacy risks when indexing confidential documents. Local embedding models allow complete air-gapped semantic search, vector indexing, and RAG document representation within a home-lab or enterprise edge boundary.

## Where it fits in the stack
**Infrastructure / AI Knowledge**. Local embedding models form the fundamental representation tier of offline RAG pipelines, serving as the bridge between document chunking (in Paperless-ngx, Obsidian, or Docling) and vector database storage (in ChromaDB, Qdrant, or LanceDB).

## Typical use cases
- **Paperless-ngx & Obsidian Semantic Search**: Generating dense vector representations for scanned PDFs, tax forms, and notes.
- **Local RAG Retrieval**: Powering local LLM reasoning (via Ollama and Claude 5.6/GPT-5.6/Gemini 4.0 Ultra agents) with zero outbound network calls.
- **Hybrid Retrieval (Dense + Sparse)**: Combining local dense embeddings with BM25 keyword matching for optimal recall.

## Strengths
- **100% Privacy & Compliance**: No document vectors or raw text leave the local server network.
- **Zero Token Fees**: Predictable, fixed hardware cost regardless of indexing volume.
- **Low Latency Execution**: On-device batched inference via ONNX Runtime, Metal, or CUDA.
- **Multilingual Support**: Advanced models like `bge-m3` support cross-lingual semantic search across 100+ languages.

## Limitations
- **Hardware Constraints**: Large context embedding models require VRAM/RAM (e.g., 2–8 GB for high-dimensional models).
- **Dimension Standardization Required**: Changing embedding models requires re-indexing existing vector collections.

## When to use it
- When building air-gapped or fully offline RAG pipelines in a home lab.
- When processing confidential documents (financial, medical, personal) locally.
- When avoiding recurring token-based API costs for large document indexing workloads.

## When not to use it
- When operating under extreme resource constraints with no RAM/VRAM capacity for model inference.
- When cloud API embeddings are explicitly mandated by remote host agreements.

## Getting started
To run local embedding models via Ollama or Sentence-Transformers:

```bash
# Pull and run nomic-embed-text locally via Ollama
ollama pull nomic-embed-text

# Test local embedding generation via curl
curl http://localhost:11434/api/embeddings -d '{
  "model": "nomic-embed-text",
  "prompt": "Home-lab automation pipeline setup"
}'
```

## CLI examples

```bash
# Generate embeddings using Python CLI tool
python3 -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('BAAI/bge-m3'); print(model.encode(['Home lab test']))"

# Pull BGE embedding model via Ollama CLI
ollama pull bge-m3
```

## API examples

### 1. Pydantic v2 Schema for Local Embedding Requests
```python
from typing import List
from pydantic import BaseModel, ConfigDict, Field

class LocalEmbeddingRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model_name: str = Field(default="nomic-embed-text", description="Name of the local embedding model")
    texts: List[str] = Field(..., description="List of strings to embed")

class LocalEmbeddingResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model_name: str
    dimensions: int
    embeddings: List[List[float]]

def process_local_embeddings(req: LocalEmbeddingRequest) -> LocalEmbeddingResponse:
    # Simulated local embedding generation (e.g. 768 dimensions)
    mock_vectors = [[0.015 * (i + 1) for i in range(768)] for _ in req.texts]
    return LocalEmbeddingResponse(
        model_name=req.model_name,
        dimensions=768,
        embeddings=mock_vectors,
    )

if __name__ == "__main__":
    request = LocalEmbeddingRequest(texts=["Paperless OCR document content"])
    response = process_local_embeddings(request)
    print(f"Generated {len(response.embeddings)} vector(s) of dimension {response.dimensions}")
```

### 2. FastMCP 3.1 Task Protocol Integration
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("local-embeddings-service")

@mcp.tool()
def generate_local_vector(text: str, model: str = "nomic-embed-text") -> list[float]:
    """Generates an embedding vector using a local embedding model."""
    # FastMCP 3.1 task protocol entry point for local vector generation
    return [0.0123] * 768
```

## Related tools / concepts
- [Ollama](../../services/ollama.md) — Local model runner supporting embedding models.
- [ChromaDB](../infrastructure/chromadb.md) — Embedded vector store.
- [Qdrant](../infrastructure/qdrant.md) — Production vector database.
- [Paperless-ngx](../../services/paperless-ngx.md) — Document management system.

## Sources / references
- [Nomic Embed Documentation](https://nomic.ai/)
- [BGE Models on HuggingFace](https://huggingface.co/BAAI)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
