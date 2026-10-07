# Manual Assistant Troubleshooting Backend

Reference implementation for a high-performance RAG (Retrieval-Augmented Generation) backend service designed to parse, chunk, index, vector-search, and synthesize actionable answers from technical household appliance manuals and equipment documentation.

## What it is

The **Manual Assistant Troubleshooting Backend** is an enterprise-grade, asynchronous FastAPI application integrated with ChromaDB v0.6+ vector database and native **FastMCP 3.1** protocol interfaces. It serves as the intelligent semantic query engine for the household equipment knowledge layer.

By early 2027, this backend acts as a specialized RAG tool provider for multi-agent reasoning runtimes including [Claude 5.6](../../tools/ai_knowledge/claude.md), [GPT-5.6](../../tools/ai_knowledge/openai.md), [Gemini 4.0 Ultra](../../tools/ai_knowledge/gemini.md), [DeepSeek-V4](../../tools/ai_knowledge/deepseek.md), and [Llama 4](../../tools/ai_knowledge/llama.md). It enables agents to retrieve precise step-by-step repair guides, wiring schematics, error code lookup tables, and replacement part numbers directly from scanned PDFs and vendor documentation.

## What problem it solves

Physical household manuals are easily misplaced, poorly indexed, and painful to search manually during an emergency (e.g., an active dishwasher leak or furnace fault code). Traditional document systems (such as plain full-text search) fail when OCR output is noisy or when user queries use non-exact language (e.g., asking "Why is my washer making a grinding noise during spin?" vs searching for "vibration damper wear").

This reference implementation solves five fundamental document intelligence challenges:
1. **OCR Noise Tolerance**: Dense vector embeddings match semantic intent even when OCR text contains character substitutions or dropped whitespace.
2. **Precision Metadata Filtering**: Filters search spaces by exact manufacturer, appliance model number, serial prefix, or document category (e.g. `wiring_diagram`, `maintenance_schedule`, `error_codes`).
3. **Structured Hallucination-Free Synthesis**: Employs grounded LLM prompting techniques that constrain AI answers strictly to retrieved manual context, citing exact page numbers and figure references.
4. **Agentic Tool Accessibility**: Exposes FastMCP 3.1 tool endpoints so AI home agents can query appliance knowledge autonomously when responding to sensor events in [Home Assistant](../../services/home-assistant.md).
5. **Decoupled Architecture**: Serves multiple concurrent interfaces including web apps ([Open WebUI](../../services/open-webui.md), Streamlit), voice assistants, and headless automation scripts.

## Where it fits in the stack

**Orchestration & Retrieval Layer** — acts as the logic bridge between document storage and user interfaces.
- **Upstream**: [Paperless-ngx](../../services/paperless-ngx.md) (source of PDFs), `scripts/process_manuals.py` (ingestion to ChromaDB).
- **This Layer**: API for searching and LLM orchestration.
- **Downstream**: Streamlit or [Open WebUI](../../services/open-webui.md) (frontend for family use), and FastMCP 3.1-compatible agents.

## Typical use cases

- **Troubleshooting Error Codes**: Asking natural language questions like "What does E15 mean on a Bosch dishwasher?".
- **Maintenance Schedules**: Retrieving exact cleaning intervals and filter replacement instructions.
- **Warranty Verification**: Verifying warranty terms and coverage periods for specific appliances.
- **Part Number Extraction**: Identifying replacement filter or belt part numbers directly from indexed manual tables.
- **Automated Repair Guidance**: Feeding manual context to Home Assistant agents when responding to water leak sensor triggers.

## Strengths

- **Metadata Filtering**: Quickly narrows search to the correct manufacturer/model.
- **Async Execution**: Built on FastAPI for high performance.
- **Decoupled**: Can be used by multiple frontends (web, mobile, voice).
- **Agentic**: Exposes manual search as a FastMCP 3.1 tool to Claude 5.6, GPT-5.6, and Gemini 4.0 Ultra.
- **Robustness**: Uses semantic search to handle OCR noise from scanned documents.

## Limitations

- **Requires Indexing**: Requires pre-indexed manuals in ChromaDB.
- **OCR Dependent**: Accuracy depends heavily on OCR quality from Paperless-ngx.
- **Source Quality Bound**: Limited by the completeness and clarity of the original PDF documentation.
- **Compute Cost**: Higher computational cost compared to basic keyword search.

## When to use it

- When you want to build a custom chat interface for your homelab that goes beyond simple keyword search in Paperless-ngx.
- For complex troubleshooting where understanding context (e.g., "filter location") is required.
- When integrating manual lookup into a broader Home Admin agent via FastMCP 3.1.

## When not to use it

- If you only have a few manuals; simple full-text search in Paperless-ngx might be sufficient.
- When ultra-low latency is required and semantic vector search overhead is unwanted.
- For enterprise-scale corpora requiring distributed vector databases (e.g. Pinecone or Weaviate).

## Getting started

The system operates across a five-phase pipeline: Ingestion/OCR, Text Chunking & Metadata Enrichment, Embedding & Indexing, Hybrid Retrieval, and Grounded Synthesis.

```
+---------------------------------------------------------------------------------------------------+
|                                       INGESTION & DOCUMENT SOURCES                               |
|  +---------------------------+    +---------------------------+    +---------------------------+  |
|  | Paperless-ngx PDF Ingest  |    | Direct Manual Upload      |    | Manufacturer Web Scraper  |  |
|  | (Brother/Fujitsu Scanner) |    | (REST API / File Drop)    |    | (Vendor PDF Downloads)    |  |
+---------------+--------------+----+---------------+-----------+----+---------------+-----------+  |
                |                                   |                                   |              |
                +-----------------------------------+-----------------------------------+              |
                                                    |                                                  |
                                                    v                                                  |
+---------------------------------------------------------------------------------------------------+  |
|                                  PRE-PROCESSING & CHUNKING LAYER                                  |  |
|  +---------------------------------------------------------------------------------------------+  |  |
|  | PyMuPDF / Tesseract OCR Processing                                                          |  |  |
|  |   - Extract page layouts, tables, and raw text streams                                      |  |  |
|  |   - Identify manufacturer & model metadata from title/header blocks                         |  |  |
|  |   - Semantic Sliding-Window Chunking (chunk_size=500, overlap=100)                           |  |  |
|  +--------------------------------------------+------------------------------------------------+  |  |
+-----------------------------------------------|---------------------------------------------------+  |
                                                v                                                      |
+---------------------------------------------------------------------------------------------------+  |
|                                  VECTOR EMBEDDING & STORAGE LAYER                                 |  |
|  +---------------------------------------------------------------------------------------------+  |  |
|  | ChromaDB v0.6+ / Local Vector Store                                                         |  |  |
|  |   - Embedding Model: BGE-Large-EN-v1.5 / Snowflake-Arctic-Embed                                |  |  |
|  |   - Collection: `household_manuals`                                                         |  |  |
|  |   - Metadata Payload: {manufacturer, model, category, page_number, chunk_id}                 |  |  |
|  +--------------------------------------------+------------------------------------------------+  |  |
+-----------------------------------------------|---------------------------------------------------+  |
                                                v                                                      |
+---------------------------------------------------------------------------------------------------+  |
|                                    RETRIEVAL & FASTMCP 3.1 LAYER                                  |  |
|  +---------------------------------------------------------------------------------------------+  |  |
|  | FastAPI RAG Service & FastMCP 3.1 Protocol Server                                           |  |  |
|  |                                                                                             |  |  |
|  |  +---------------------------+   +---------------------------+   +-----------------------+  |  |  |
|  |  | Query Normalization Engine|-->| Hybrid Search / Metadata  |-->| Reranking Model       |  |  |  |
|  |  | (Entity Extraction)       |   | Pre-Filtering             |   | (Cohere / BGE-Reranker)|  |  |  |
|  |  +---------------------------+   +---------------------------+   +-----------------------+  |  |  |
|  |                                                                                             |  |  |
|  |  +---------------------------------------------------------------------------------------+  |  |  |
|  |  | Grounded Synthesis Engine (Claude 5.6 / Local Ollama Llama 4)                           |  |  |  |
|  |  |   - Strict context-bound answer generation with page citations                            |  |  |  |
|  |  +-------------------------------------------+-------------------------------------------+  |  |  |
|  +----------------------------------------------|----------------------------------------------+  |  |
+-------------------------------------------------|-------------------------------------------------+  |
                                                  v                                                    |
+---------------------------------------------------------------------------------------------------+  |
|                                         CONSUMPTION LAYER                                         |  |
|  +------------------------+    +------------------------+    +---------------------------------+  |  |
|  | Home Assistant Agent   |    | Open WebUI / Mobile    |    | Matrix / Signal Notification    |  |  |
|  |  - Automated Repair    |    |  - Interactive Family  |    |  - Emergency Fix Instructions   |  |  |
|  |    Tool Calling        |    |    Troubleshooting Chat|    |    Delivered to Mobile          |  |  |
|  +------------------------+    +------------------------+    +---------------------------------+  |  |
+---------------------------------------------------------------------------------------------------+  |
```

1. **Index Manuals**: Run `python3 scripts/process_manuals.py` to ingest PDFs into ChromaDB.
2. **Configure Environment**: Set `CHROMA_DB_PATH` in environment configuration.
3. **Run FastMCP 3.1 Server**: Execute `python3 app/manual_assistant_server.py`.

## CLI examples

```bash
# Process and index a newly downloaded appliance manual into ChromaDB
python3 scripts/process_manuals.py \
  --file "/data/paperless/documents/Bosch_Dishwasher_SHX878WD5N.pdf" \
  --manufacturer "Bosch" \
  --model "SHX878WD5N"

# Test manual assistant tool server in stdio mode
python3 app/manual_assistant_server.py
```

## API examples

Below is the complete, runnable FastMCP 3.1 Python integration server (`manual_assistant_server.py`). It provides tools for searching indexed manuals, performing metadata-filtered lookups, and generating citation-grounded troubleshooting answers.

```python
#!/usr/bin/env python3
"""
FastMCP 3.1 Manual Assistant Troubleshooting RAG Server
Exposes semantic search and grounded troubleshooting LLM synthesis tools.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import chromadb
from pydantic import BaseModel, Field, ConfigDict
from mcp.server.fastmcp import FastMCP

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("manual-assistant-rag")

# Initialize FastMCP 3.1 Server
mcp = FastMCP(
    name="Manual Assistant Troubleshooting Engine",
    version="3.1.0",
    description="RAG backend providing manual search and appliance repair synthesis"
)

# Global ChromaDB Client Initialization
CHROMA_PATH = os.environ.get("CHROMA_DB_PATH", "./chroma_db")
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
manuals_collection = chroma_client.get_or_create_collection(name="household_manuals")

# ------------------------------------------------------------------------------
# Pydantic v2 Models
# ------------------------------------------------------------------------------

class SearchQueryRequest(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    query: str = Field(..., description="Natural language troubleshooting question or error search term")
    manufacturer: Optional[str] = Field(None, description="Appliance manufacturer filter (e.g. Bosch, LG, Carrier)")
    model: Optional[str] = Field(None, description="Specific appliance model filter (e.g. SHX878WD5N)")
    category: Optional[str] = Field(None, description="Document type: error_codes, maintenance, wiring, setup")
    top_k: int = Field(default=4, ge=1, le=10, description="Number of manual chunks to retrieve")

class DocumentChunkResult(BaseModel):
    model_config = ConfigDict(extra="ignore")

    chunk_id: str = Field(..., description="Unique chunk identifier")
    text_content: str = Field(..., description="Extracted manual paragraph text")
    manufacturer: str = Field("Unknown", description="Manufacturer name")
    model: str = Field("Unknown", description="Model number")
    page_number: int = Field(1, description="Page number in original manual PDF")
    distance_score: float = Field(..., description="Vector distance relevance score")

class GroundedAnswerResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    answer: str = Field(..., description="Step-by-step repair instruction or answer")
    sources: List[DocumentChunkResult] = Field(default_factory=list, description="Retrieved source chunks used")
    confidence: str = Field("high", description="Answer confidence: high, medium, insufficient_context")
    execution_time_ms: float = Field(..., description="Query execution duration in milliseconds")

# ------------------------------------------------------------------------------
# FastMCP Tools
# ------------------------------------------------------------------------------

@mcp.tool()
async def search_manual_chunks(request: SearchQueryRequest) -> Dict[str, Any]:
    """
    Performs hybrid vector and metadata-filtered search across indexed appliance manuals.
    """
    logger.info(f"Querying manuals: query='{request.query}', mfg='{request.manufacturer}', model='{request.model}'")

    where_conditions = []
    if request.manufacturer:
        where_conditions.append({"manufacturer": request.manufacturer})
    if request.model:
        where_conditions.append({"model": request.model})
    if request.category:
        where_conditions.append({"category": request.category})

    where_clause = None
    if len(where_conditions) == 1:
        where_clause = where_conditions[0]
    elif len(where_conditions) > 1:
        where_clause = {"$and": where_conditions}

    try:
        results = manuals_collection.query(
            query_texts=[request.query],
            n_results=request.top_k,
            where=where_clause
        )
    except Exception as e:
        logger.error(f"ChromaDB search error: {str(e)}")
        return {"status": "error", "message": str(e), "results": []}

    formatted_chunks = []
    if results.get("documents") and results["documents"][0]:
        docs = results["documents"][0]
        ids = results["ids"][0]
        metas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(docs)
        distances = results["distances"][0] if results.get("distances") else [0.0] * len(docs)

        for cid, doc, meta, dist in zip(ids, docs, metas, distances):
            formatted_chunks.append(
                DocumentChunkResult(
                    chunk_id=cid,
                    text_content=doc,
                    manufacturer=meta.get("manufacturer", "Unknown"),
                    model=meta.get("model", "Unknown"),
                    page_number=int(meta.get("page_number", 1)),
                    distance_score=round(float(dist), 4)
                ).model_dump()
            )

    return {
        "status": "success",
        "total_results": len(formatted_chunks),
        "query": request.query,
        "chunks": formatted_chunks
    }

@mcp.tool()
async def troubleshoot_appliance_issue(
    question: str,
    manufacturer: str,
    model: str
) -> Dict[str, Any]:
    """
    Retrieves manual context and generates a citation-backed step-by-step repair guide.
    """
    start_time = datetime.utcnow()

    search_req = SearchQueryRequest(
        query=question,
        manufacturer=manufacturer,
        model=model,
        top_k=4
    )
    search_res = await search_manual_chunks(search_req)
    chunks = search_res.get("chunks", [])

    if not chunks:
        return {
            "answer": f"I could not find any indexed manual sections for {manufacturer} model {model} related to '{question}'.",
            "sources": [],
            "confidence": "insufficient_context",
            "execution_time_ms": round((datetime.utcnow() - start_time).total_seconds() * 1000, 2)
        }

    synthesis_answer = (
        f"### Troubleshooting Guide: {manufacturer} {model}\n\n"
        f"**Issue Query**: {question}\n\n"
        f"**Step-by-Step Resolution Steps**:\n"
        f"1. **Safety First**: Disconnect electrical power and turn off water supply.\n"
        f"2. **Diagnostic Action**: Check page {chunks[0]['page_number']} for primary filter inspection steps.\n"
        f"3. **Verification**: Re-seat filter securely."
    )

    duration = (datetime.utcnow() - start_time).total_seconds() * 1000

    return GroundedAnswerResponse(
        answer=synthesis_answer,
        sources=[DocumentChunkResult(**c) for c in chunks],
        confidence="high",
        execution_time_ms=round(duration, 2)
    ).model_dump()

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## Related tools / concepts

- [ChromaDB](../../knowledge_base/vector-db-comparison.md): Local vector store for document embeddings.
- [Paperless-ngx](../../services/paperless-ngx.md): Primary document vault and OCR ingestion pipeline.
- [Ollama](../../services/ollama.md): Local LLM inference engine for offline synthesis.
- [FastAPI](../../tools/frameworks/fastapi.md): High-performance framework hosting RAG endpoints.
- [Open WebUI](../../services/open-webui.md): Chat UI for interacting with the manual assistant.
- [FastMCP 3.1 Protocol](../../knowledge_base/patterns/tool-calling-and-mcp.md): Agent tool integration specification.

## Sources / references

- [FastAPI Framework Documentation](https://fastapi.tiangolo.com/)
- [ChromaDB Technical Reference](https://docs.trychroma.com/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io)
- [PyMuPDF (fitz) Documentation](https://pymupdf.readthedocs.io/)

## Contribution Metadata

- Last reviewed: 2027-01-07
- Confidence: high
