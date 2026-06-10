# Manual Assistant Troubleshooting Backend

Reference implementation for a RAG-based backend to search and answer questions from household manuals.

## What it is
A FastAPI-based backend that integrates with ChromaDB to perform hybrid (vector + metadata filtered) search across OCR'd manuals and provides an interface for LLM-based troubleshooting. As of June 2026, it supports native [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) for direct tool-calling by Claude 4.8.

## What problem it solves
It centralizes the "brain" for the [AI-Powered Warranty & Manual Assistant](../../roadmap.md), allowing users to ask natural language questions like "How do I clean the filter on my Bosch dishwasher?" and get answers directly from the scanned PDF. It solves the "lost physical manual" problem and provides immediate, context-aware troubleshooting advice.

## Where it fits in the stack
- **Upstream**: Paperless-ngx (source of PDFs), `scripts/process_manuals.py` (ingestion to ChromaDB).
- **This Layer**: API for searching and LLM orchestration.
- **Downstream**: Streamlit or Open WebUI (frontend for family use), and MCP-compatible agents.

## Typical use cases
- Troubleshooting appliance error codes (e.g., "What does E15 mean on a Bosch?").
- Finding maintenance schedules in manuals.
- Verifying warranty terms for specific products.
- Summarizing setup instructions for new devices.

## Comparison: ChromaDB vs. Simple Search
| Feature | Simple Search (grep) | ChromaDB (Vector) |
| :--- | :--- | :--- |
| **Search Method** | Exact keyword matching. | Semantic similarity. |
| **OCR Handling** | Fails on slight OCR errors. | Robust to minor misspellings. |
| **Context** | Returns isolated lines. | Returns semantic chunks. |
| **Metadata** | Limited or manual. | Rich, automated filtering. |

## Strengths
- **Metadata Filtering**: Quickly narrows search to the correct manufacturer/model.
- **Async Execution**: Built on FastAPI for high performance.
- **Decoupled**: Can be used by multiple frontends (web, mobile, voice).
- **Agentic**: Exposes manual search as a tool to Claude 4.8 via MCP.

## Limitations
- Requires pre-indexed manuals in ChromaDB.
- Accuracy depends heavily on OCR quality from Paperless-ngx.
- Limited by the quality of the original PDF documentation.

## When to use it
When you want to build a custom chat interface for your homelab that goes beyond simple keyword search in Paperless-ngx.

## When not to use it
If you only have a few manuals; simple full-text search in Paperless-ngx might be sufficient.

## Getting started
To set up the manual assistant troubleshooting backend:

1.  **Index Manuals**: Run `python3 scripts/process_manuals.py` to ingest your PDFs into ChromaDB.
2.  **Configure API**: Set your `CHROMA_DB_PATH` and `API_KEY` in `.env`.
3.  **Launch Backend**: Run the FastAPI server using `uvicorn`.

## CLI examples
> [!NOTE]
> The backend is typically accessed via API, but you can test it using `curl` or the [FastMCP](../../tools/automation_orchestration/mcp.md) CLI.

```bash
# Test the search endpoint via curl
curl -X GET "http://localhost:8000/search?query=clean+filter&manufacturer=Bosch"

# Inspect the status of the ChromaDB collection
python3 scripts/process_manuals.py --status

# Re-index a specific manual
python3 scripts/process_manuals.py --file "/path/to/manual.pdf"
```

## API examples
Example of using FastAPI and ChromaDB to search for a specific appliance model:

```python
from fastapi import FastAPI
import chromadb

app = FastAPI()
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="manuals")

@app.get("/search")
async def search_manual(query: str, manufacturer: str, model: str):
    results = collection.query(
        query_texts=[query],
        n_results=3,
        where={"$and": [{"manufacturer": manufacturer}, {"model": model}]}
    )
    return results
```

## Related tools / concepts
- [ChromaDB](../../docs/knowledge_base/vector-db-comparison.md)
- [scripts/process_manuals.py](../../scripts/process_manuals.py)
- [Paperless-ngx](../../services/paperless-ngx.md)
- [Ollama](../../services/ollama.md)
- [FastAPI](../../tools/development_ops/fastapi.md)
- [n8n](../../services/n8n.md)
- [Open WebUI](../../services/open-webui.md)
- [Manual Troubleshooting Research](../../knowledge_base/manual-troubleshooting-research.md)
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md)

## Sources / References
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [RAG Best Practices (June 2026 Update)](https://example.com/rag-2026)

## Contribution Metadata
- Last reviewed: 2026-06-10
- Confidence: high
