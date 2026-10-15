# Chroma

## What it is
Chroma (also known as ChromaDB) is an open-source, AI-native, lightweight embedding and vector database engineered specifically to simplify Retrieval-Augmented Generation (RAG), long-term agentic memory, and semantic search workflows. Deployed either as an embeddable in-memory library inside Python and Node.js runtimes or as a client-server distributed container, Chroma provides developer-friendly APIs to store, index, manage, and query high-dimensional vector embeddings alongside rich structured metadata.

In early 2027, Chroma serves as a core vector storage engine, offering native support for **Model Context Protocol (MCP 3.1 / FastMCP 3.1)** server tools, automatic embedding function integrations (Hugging Face, OpenAI, Ollama, sentence-transformers), HNSW vector indexing, and boolean metadata filter expressions for autonomous AI agents.

## What problem it solves
Deploying large enterprise-grade vector databases (e.g., Milvus, Qdrant) requires significant cluster orchestration, dedicated infrastructure, and complex configuration setups that create unnecessary overhead for developer prototyping, local agent assistants, and edge deployments. Conversely, naive in-memory array searches scale poorly ($O(N)$ brute-force distance calculations) and lack metadata filtering capabilities.

Chroma resolves this dilemma by delivering a zero-configuration, production-capable vector storage engine. It can be initialized in Python with a single line (`client = chromadb.PersistentClient(path="./chroma_db")`), handling vector embedding generation, HNSW graph indexing, persistence on NVMe SSD storage, and filtered metadata retrieval without external service dependencies.

## Where it fits in the stack
**Vector Storage & Knowledge Layer**. Positioned between document parsing/chunking pipelines ([Unstructured](../process_understanding/unstructured.md), [LlamaIndex](../ai_knowledge/llamaindex.md)) and LLM orchestrators ([Claude Code](../development_ops/claude-code.md), [Open WebUI](../../services/open-webui.md)), Chroma stores document chunk embeddings and metadata tags, allowing agents to execute fast hybrid semantic retrieval over local knowledge bases.

## Architecture Diagram

```
+---------------------------------------------------------------------------------------------------+
|                                   Chroma Vector Storage Engine                                    |
|                                                                                                   |
|  +---------------------------------------------------------------------------------------------+  |
|  | Application & Agent Interface                                                              |  |
|  | (Python Library, TypeScript SDK, FastMCP 3.1 Agent Server, REST API v1 Endpoint)              |  |
|  +---------------------------------------------------------------------------------------------+  |
|                                                ||                                                 |
|                                                \/                                                 |
|  +---------------------------------------------------------------------------------------------+  |
|  | Automatic Embedding Layer                                                                   |  |
|  | (Hugging Face, OpenAI, Ollama Local Models, SentenceTransformers, Custom Function Hooks)    |  |
|  +---------------------------------------------------------------------------------------------+  |
|                                                ||                                                 |
|                                                \/                                                 |
|  +---------------------------------------------------------------------------------------------+  |
|  | Indexing & Query Execution Engine                                                           |  |
|  | (HNSW Hierarchical Navigable Small World Graph, Cosine / L2 / Inner Product Metrics)        |  |
|  +---------------------------------------------------------------------------------------------+  |
|                                                ||                                                 |
|                                                \/                                                 |
|  +---------------------------------------------------------------------------------------------+  |
|  | Persistence & Metadata Filtering Layer                                                      |  |
|  | (SQLite Metadata Store, Parquet Vector Segments, NVMe SSD Storage, Boolean $and/$or Filters) |  |
|  +---------------------------------------------------------------------------------------------+  |
+---------------------------------------------------------------------------------------------------+
```

## Typical use cases
- **Long-Term Desktop Agent Memory**: Storing conversation histories, tool call results, and developer preferences for local AI coding assistants ([Claude Code](../development_ops/claude-code.md), [OpenClaw](../development_ops/openclaw.md)).
- **Local Document RAG**: Indexing local PDFs, markdown technical documentation, and home-lab manuals to enable offline semantic query capabilities in [Open WebUI](../../services/open-webui.md).
- **Agentic Tool Definition Filtering**: Storing thousands of OpenAPI and FastMCP 3.1 tool definition schemas in Chroma, dynamically retrieving only the top-$k$ relevant tools for a given user prompt.
- **Multimodal Vector Search**: Storing image and text embeddings generated by open-weight CLIP or SigLIP models for visual asset retrieval.

## Strengths
- **Instant Developer Onboarding**: Zero external dependencies required; runs embedded inside standard Python or Node.js applications.
- **Persistent Local Directory Engine**: Automatically writes collections to disk using SQLite metadata tables and Parquet vector segments.
- **Integrated Embedding Functions**: Seamlessly converts raw string documents into embeddings without requiring manual external embedding API code.
- **FastMCP 3.1 Native Protocol**: Direct FastMCP 3.1 server tools allow AI agents to ingest documents and query collections dynamically.
- **Rich Boolean Metadata Filters**: Supports complex `$and`, `$or`, `$eq`, `$in`, and `$gte` expressions on document metadata tags.

## Limitations
- **Horizontal Clustering Boundaries**: Lacks built-in multi-node sharding and distributed consensus (for massive petabyte-scale vector clusters, use [Milvus](milvus.md) or [Qdrant](../infrastructure/qdrant.md)).
- **RAM Footprint on Massive Collections**: HNSW graph indices reside in memory during active query execution, requiring sufficient system RAM for multi-million vector collections.
- **Ecosystem Focus**: Primary SDKs and deepest framework integrations are centered on Python and TypeScript ecosystems.

## When to use it
- When building lightweight, fast, local, or embedded RAG applications and agent memory systems.
- For fully offline, air-gapped AI applications running on edge hardware or home-lab servers.
- When using orchestration frameworks like LlamaIndex, LangChain, or Autogen.

## When not to use it
- For enterprise deployments requiring distributed cross-region horizontal sharding across hundreds of storage nodes (prefer [Milvus](milvus.md) or [Weaviate](weaviate.md)).
- If host memory is severely constrained (< 512 MB RAM) and cannot store active vector graphs.

## Getting started

### Installation
Install ChromaDB alongside embedding and FastMCP 3.1 dependencies:

```bash
pip install chromadb pydantic fastmcp
```

### Basic Persistent Client Example
Initialize a local persistent database directory and ingest documents:

```python
import chromadb

# Initialize local persistent storage on disk
client = chromadb.PersistentClient(path="./chroma_db")

# Create or retrieve collection with cosine distance metric
collection = client.get_or_create_collection(
    name="lab_documentation",
    metadata={"hnsw:space": "cosine"}
)

# Ingest documents with metadata tags
collection.add(
    documents=[
        "To reset the network router, hold the rear button for 10 seconds.",
        "Default SSH port is configured to 2222 in the security settings file.",
        "Thermostat temperature limits can be configured in the smart home dashboard."
    ],
    metadatas=[
        {"category": "hardware", "device": "router"},
        {"category": "network", "device": "server"},
        {"category": "hardware", "device": "thermostat"}
    ],
    ids=["doc_001", "doc_002", "doc_003"]
)

print(f"Collection initialized with {collection.count()} items.")
```

## CLI examples

### 1. Launching Standalone Chroma Server
```bash
# Start background HTTP Chroma server on port 8000
chroma run --path ./chroma_db --host 0.0.0.0 --port 8000
```

### 2. Docker Container Deployment
```bash
# Run isolated Chroma DB container with volume persistence
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/chroma_data:/chroma/chroma \
  -e IS_PERSISTENT=TRUE \
  chromadb/chroma:latest
```

## API examples

### Complete FastMCP 3.1 Server with Pydantic v2 Schema Validation and Filtering
The following script sets up a production-grade **FastMCP 3.1** server that exposes vector ingestion and semantic query tools with metadata filtering and strict **Pydantic v2** validation.

```python
import os
import chromadb
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator
from fastmcp import FastMCP

# Initialize FastMCP 3.1 Server
mcp = FastMCP(
    name="chroma-agent-vector-server",
    version="3.1"
)

# Initialize Chroma Persistent Client
chroma_client = chromadb.PersistentClient(path="./chroma_mcp_db")

# ---------------------------------------------------------------------------
# Pydantic v2 Validation Schemas
# ---------------------------------------------------------------------------

class DocumentIngestSchema(BaseModel):
    collection_name: str = Field("knowledge_base", min_length=2, max_length=64)
    documents: List[str] = Field(..., min_length=1)
    metadatas: List[Dict[str, Any]] = Field(..., min_length=1)
    document_ids: List[str] = Field(..., min_length=1)

    @field_validator("document_ids")
    @classmethod
    def validate_lengths_match(cls, v: List[str], info) -> List[str]:
        docs = info.data.get("documents")
        metas = info.data.get("metadatas")
        if docs and len(v) != len(docs):
            raise ValueError("document_ids length must match documents length")
        if metas and len(v) != len(metas):
            raise ValueError("document_ids length must match metadatas length")
        return v

class VectorQuerySchema(BaseModel):
    collection_name: str = Field("knowledge_base")
    query_text: str = Field(..., min_length=2, description="Semantic query text string")
    top_k: int = Field(3, ge=1, le=20, description="Number of nearest neighbor results to return")
    category_filter: Optional[str] = Field(None, description="Optional metadata category filter")

class RetrievedSearchResult(BaseModel):
    doc_id: str
    document_text: str
    distance: float = Field(..., ge=0.0)
    metadata: Dict[str, Any]

class QueryResponseSchema(BaseModel):
    query: str
    total_found: int
    results: List[RetrievedSearchResult]

# ---------------------------------------------------------------------------
# FastMCP 3.1 Tools
# ---------------------------------------------------------------------------

@mcp.tool(
    name="ingest_documents_to_chroma",
    description="Ingest text document chunks into a ChromaDB vector collection with metadata tags."
)
def ingest_documents_to_chroma(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Validate payload and ingest documents into ChromaDB."""
    try:
        data = DocumentIngestSchema.model_validate(payload)
        collection = chroma_client.get_or_create_collection(name=data.collection_name)

        collection.add(
            documents=data.documents,
            metadatas=data.metadatas,
            ids=data.document_ids
        )
        return {
            "success": True,
            "message": f"Successfully ingested {len(data.documents)} documents into '{data.collection_name}'."
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool(
    name="query_chroma_vector_store",
    description="Perform semantic vector search in ChromaDB with optional metadata filtering."
)
def query_chroma_vector_store(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Execute vector query and return Pydantic v2 validated search results."""
    try:
        query_data = VectorQuerySchema.model_validate(payload)
        collection = chroma_client.get_or_create_collection(name=query_data.collection_name)

        where_clause = {"category": query_data.category_filter} if query_data.category_filter else None

        raw_results = collection.query(
            query_texts=[query_data.query_text],
            n_results=query_data.top_k,
            where=where_clause
        )

        search_results = []
        if raw_results and raw_results.get("ids") and len(raw_results["ids"][0]) > 0:
            for i in range(len(raw_results["ids"][0])):
                search_results.append(RetrievedSearchResult(
                    doc_id=raw_results["ids"][0][i],
                    document_text=raw_results["documents"][0][i],
                    distance=raw_results["distances"][0][i] if raw_results.get("distances") else 0.0,
                    metadata=raw_results["metadatas"][0][i] if raw_results.get("metadatas") else {}
                ))

        response = QueryResponseSchema(
            query=query_data.query_text,
            total_found=len(search_results),
            results=search_results
        )
        return {"success": True, "data": response.model_dump(mode="json")}

    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    print("Starting FastMCP 3.1 Chroma Vector Server...")
    mcp.run()
```

## Troubleshooting & Common Operational Pitfalls

| Diagnostic Scenario | Potential Root Cause | Recommended Operational Resolution |
| :--- | :--- | :--- |
| **`ValueError: Embedding dimension mismatch`** | Query model dimension differs from collection model | Ensure same embedding model (e.g., `all-MiniLM-L6-v2`) is used for both ingestion and querying. |
| **`sqlite3.OperationalError: database is locked`** | Multiple processes writing concurrently to same SQLite file | Deploy Chroma in server mode (`chroma run`) and connect via `HttpClient`. |
| **High Query Latency on Disk** | Database stored on slow HDD storage | Store Chroma data directories on high-speed NVMe SSD drives. |
| **Empty Query Results with Metadata Filters** | Key name mismatch or strict case-sensitivity in `where` dict | Check metadata key casing and value types (`str` vs `int`). |

## Operational Guardrails & Best Practices
1. **Server Mode for Concurrency**: Use `chromadb.HttpClient(host="localhost", port=8000)` whenever multiple agent processes need simultaneous read/write access.
2. **Explicit Distance Metric Selection**: Always specify distance metric explicitly upon collection creation (`metadata={"hnsw:space": "cosine"}`).
3. **Chunk Idempotency**: Generate deterministic document IDs using content hashes (`hashlib.sha256(chunk_text.encode()).hexdigest()`) to prevent duplicate document insertion.

## Related tools / concepts
- [Milvus](milvus.md) — Scalable, distributed enterprise vector database.
- [Qdrant](../infrastructure/qdrant.md) — High-performance Rust vector database.
- [Weaviate](weaviate.md) — Hybrid search-native vector storage engine.
- [LlamaIndex](../ai_knowledge/llamaindex.md) — Data orchestration framework with native Chroma integrations.
- [Open WebUI](../../services/open-webui.md) — AI Web UI utilizing Chroma for local document RAG.

## Sources / references
- [Chroma Official Site](https://www.trychroma.com/)
- [Chroma Technical Documentation](https://docs.trychroma.com/)
- [Chroma GitHub Repository](https://github.com/chroma-core/chroma)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
