# Manual Assistant Troubleshooting Backend

Reference implementation for a RAG-based backend to search and answer questions from household manuals.

## What it is
A FastAPI-based backend that integrates with ChromaDB v0.6+ to perform hybrid (vector + metadata filtered) search across OCR'd manuals and provides an interface for LLM-based troubleshooting. As of January 2027, it supports native **FastMCP 3.1** and **Model Context Protocol** for direct tool-calling by **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**, and **Llama 4**.

## What problem it solves
It centralizes the "brain" for the [AI-Powered Warranty & Manual Assistant](../../roadmap.md), allowing users to ask natural language questions like "How do I clean the filter on my Bosch dishwasher?" and get answers directly from the scanned PDF. It solves the "lost physical manual" problem and provides immediate, context-aware troubleshooting advice.

## Where it fits in the stack
**Orchestration Layer** — acts as the logic bridge between document storage and user interfaces.
- **Upstream**: Paperless-ngx (source of PDFs), `scripts/process_manuals.py` (ingestion to ChromaDB).
- **This Layer**: API for searching and LLM orchestration.
- **Downstream**: Streamlit or Open WebUI (frontend for family use), and FastMCP 3.1-compatible agents.

## Typical use cases
- Troubleshooting appliance error codes (e.g., "What does E15 mean on a Bosch?").
- Finding maintenance schedules in manuals.
- Verifying warranty terms for specific products.
- Summarizing setup instructions for new devices.
- Generating maintenance checklists from manual text.

## Strengths
- **Metadata Filtering**: Quickly narrows search to the correct manufacturer/model.
- **Async Execution**: Built on FastAPI for high performance.
- **Decoupled**: Can be used by multiple frontends (web, mobile, voice).
- **Agentic**: Exposes manual search as a FastMCP 3.1 tool to Claude 5.1 and GPT-5.5.
- **Robustness**: Uses semantic search to handle OCR noise from scanned documents.

## Limitations
- Requires pre-indexed manuals in ChromaDB.
- Accuracy depends heavily on OCR quality from Paperless-ngx.
- Limited by the quality of the original PDF documentation.
- Higher computational cost compared to basic keyword search.

## When to use it
- When you want to build a custom chat interface for your homelab that goes beyond simple keyword search in Paperless-ngx.
- For complex troubleshooting where understanding context (e.g., "filter location") is required.
- When integrating manual lookup into a broader Home Admin agent.

## When not to use it
- If you only have a few manuals; simple full-text search in Paperless-ngx might be sufficient.
- When low-latency is critical and you don't need semantic understanding.
- For extremely large corpora where a more enterprise-grade RAG solution (e.g., Pinecone, Weaviate) might be needed.

## Getting started
To set up the manual assistant troubleshooting backend:

1.  **Index Manuals**: Run `python3 scripts/process_manuals.py` to ingest your PDFs into ChromaDB.
2.  **Configure API**: Set your `CHROMA_DB_PATH` and `API_KEY` in `.env`.
3.  **Launch Backend**: Run the FastAPI server using `uvicorn`:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```

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

# Start the FastMCP server for the manual assistant
fastmcp run app/mcp_server.py --port 8000
```

## API examples
Example of using FastAPI and ChromaDB v0.6+ with strict Pydantic v2 schemas:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import chromadb
from typing import List, Optional

app = FastAPI(title="Manual Assistant RAG Service", version="2.0.0")
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="manuals")

class ManualSearchRequest(BaseModel):
    query: str = Field(..., description="Natural language search query")
    manufacturer: Optional[str] = Field(None, description="Filter by manufacturer")
    model: Optional[str] = Field(None, description="Filter by model number")
    top_k: int = Field(default=3, ge=1, le=10, description="Number of context snippets to return")

class ManualSearchResult(BaseModel):
    document: str = Field(..., description="Extracted paragraph text from manual")
    manufacturer: str = Field(..., description="Appliance manufacturer")
    model: str = Field(..., description="Appliance model designation")
    score: float = Field(..., description="Relevance score / distance")

class SearchResponse(BaseModel):
    results: List[ManualSearchResult] = Field(default_factory=list)

@app.post("/search", response_model=SearchResponse)
async def search_manual(request: ManualSearchRequest):
    where_clause = {}
    if request.manufacturer and request.model:
        where_clause = {"$and": [{"manufacturer": request.manufacturer}, {"model": request.model}]}
    elif request.manufacturer:
        where_clause = {"manufacturer": request.manufacturer}
    elif request.model:
        where_clause = {"model": request.model}

    results = collection.query(
        query_texts=[request.query],
        n_results=request.top_k,
        where=where_clause if where_clause else None
    )

    formatted = []
    if results.get("documents") and results["documents"][0]:
        docs = results["documents"][0]
        metas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(docs)
        distances = results["distances"][0] if results.get("distances") else [0.0] * len(docs)

        for doc, meta, dist in zip(docs, metas, distances):
            formatted.append(ManualSearchResult(
                document=doc,
                manufacturer=meta.get("manufacturer", "Unknown"),
                model=meta.get("model", "Unknown"),
                score=float(dist)
            ))

    return SearchResponse(results=formatted)
```

### FastMCP 3.1 Tool Call & Implementation
Example tool definition and validation block for Claude 5.1 and GPT-5.5:

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field
from openai import OpenAI

mcp = FastMCP("manual-assistant")

class ManualQueryInput(BaseModel):
    query: str = Field(..., description="The troubleshooting question or search query.")
    manufacturer: str = Field(..., description="Manufacturer name, e.g. Bosch.")
    model: str = Field(..., description="Model identifier, e.g. SHX878WD5N.")

@mcp.tool()
def lookup_manual(input_data: ManualQueryInput) -> str:
    """Search the household manual database for troubleshooting information."""
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_collection(name="manuals")

    results = collection.query(
        query_texts=[input_data.query],
        n_results=3,
        where={"$and": [{"manufacturer": input_data.manufacturer}, {"model": input_data.model}]}
    )

    documents = results.get("documents", [[]])[0]
    if not documents:
        return f"No relevant manual snippets found for {input_data.manufacturer} {input_data.model}."

    context = "\n---\n".join(documents)
    prompt = f"Answer the troubleshooting query using only the manual context.\n\nContext:\n{context}\n\nQuery: {input_data.query}"

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-5.5-preview",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    return response.choices[0].message.content
```

## Related tools / concepts
- [ChromaDB](../../knowledge_base/vector-db-comparison.md)
- [scripts/process_manuals.py](../../scripts/process_manuals.py)
- [Paperless-ngx](../../services/paperless-ngx.md)
- [Ollama](../../services/ollama.md)
- [FastAPI](../../tools/frameworks/fastapi.md)
- [n8n](../../services/n8n.md)
- [Open WebUI](../../services/open-webui.md)
- [Manual Troubleshooting Research](../../knowledge_base/manual-troubleshooting-research.md)
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md)

## Sources / references
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-06
- Confidence: high
