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
Install PrivateGPT via `uv` or package managers and launch the service:

```bash
uv tool install --python 3.11 \
  --find-links https://wheels.privategpt.dev/packages/ \
  "private-gpt[core]"
```

A minimal working example starting PrivateGPT connected to a local Ollama LLM endpoint:

```bash
OPENAI_API_BASE=http://localhost:11434/v1 \
OPENAI_EMBEDDING_API_BASE=http://localhost:11434/v1 \
private-gpt serve
```

## CLI examples

```bash
# 1. Install PrivateGPT with uv tool runner
uv tool install --python 3.11 "private-gpt[core]"

# 2. Launch the PrivateGPT server with Ollama local model server backend
PGPT_PROFILES=ollama private-gpt serve

# 3. Ingest local document directory into PrivateGPT RAG store
python scripts/ingest_folder.py --dir /data/documents
```

## API examples

Minimal Python snippet querying PrivateGPT's Claude/OpenAI-compatible `/v1/chat/completions` API:

```python
import urllib.request
import json

req = urllib.request.Request(
    "http://localhost:8080/v1/chat/completions",
    data=json.dumps({
        "messages": [{"role": "user", "content": "Summarize my ingested documents."}],
        "use_context": True
    }).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

with urllib.request.urlopen(req) as response:
    result = json.loads(response.read().decode())
    print(result["choices"][0]["message"]["content"])
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
