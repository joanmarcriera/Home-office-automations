# Chroma

## What it is
Chroma (also referred to as ChromaDB) is an open-source, lightweight, and AI-native embedding/vector database designed specifically to make it easy to build Retrieval-Augmented Generation (RAG) applications. Deployed either as an embeddable in-memory library inside Python/JavaScript applications or as a standalone distributed server, Chroma provides developer-friendly APIs to store, manage, query, and retrieve high-dimensional vector embeddings along with their associated metadata.

## What problem it solves
Setting up complex enterprise vector databases like Milvus or Qdrant can be highly time-consuming and resource-intensive for small-to-medium scale applications or developer prototyping. Chroma solves this by providing a "zero-configuration" database that can be fully integrated into a Python or Node.js runtime with a single import statement. It manages vector indexing, metadata filtering, and embedding model integration under a unified, easy-to-use interface.

## Where it fits in the stack
**Vector Database / Knowledge Store Layer**. It sits at the storage layer of RAG and agentic workflows, taking parsed document chunks and storing their embeddings to enable semantic retrieval and tool schemas by local or remote LLMs.

## Typical use cases
- **Desktop Agent Memory**: Providing long-term persistent memory for local coding assistants and tools like [Claude Code](../development_ops/claude-code.md).
- **Local Document RAG**: Indexing local PDFs, markdown files, or manuals to perform semantic context-injection for a Home Lab orchestrator (e.g., [Open WebUI](../../services/open-webui.md)).
- **Agentic Tool Filtering**: Storing and searching across thousands of tool definitions using semantic description matching to execute the exact required tool under the Model Context Protocol (MCP 3.1).

## Strengths
- **Pythonic & Native Simplicity**: Extremely simple to install and execute (`import chromadb` is all it takes).
- **Persistent Local Directory**: Easily saves database states locally on an NVMe SSD with persistent storage, avoiding the need for a separate database container during prototyping.
- **Built-in Embedding Functions**: Automatically handles text-to-vector embedding conversions using models from Hugging Face, OpenAI, or local Ollama instances.
- **Rich Metadata Filtering**: Supports standard filtering capabilities on document metadata tags to restrict search contexts.
- **Native MCP 3.1 Server Integration**: Includes direct integrations with the Model Context Protocol (MCP 3.1) enabling frontend and agent systems to query collections as standard tools.

## Limitations
- **Horizontal Scaling Limits**: Lacks native clustering or distributed sharding out-of-the-box, making it less suitable for massive multi-node enterprise database configurations.
- **Memory Consumption**: Relies heavily on in-memory storage during operation, which can lead to high RAM consumption on massive collections.
- **Language Lock-in**: Primary libraries and deep integrations are heavily focused on Python and JavaScript/TypeScript ecosystems.

## When to use it
- When you need a quick, reliable, and lightweight vector database for local prototyping or small-to-medium production deployments.
- When building a fully offline, air-gapped AI assistant that runs entirely on a single machine or home-lab server.
- When utilizing frameworks like LlamaIndex, LangChain, or Autogen, which offer native first-class integration for Chroma.

## When not to use it
- For enterprise-scale applications requiring distributed vector storage, high availability across regions, and complex horizontal partitioning (consider [Milvus](milvus.md), [Weaviate](weaviate.md), or [Pinecone](pinecone.md) instead).
- If your system has extremely strict memory limitations and cannot support in-memory vector storage.

## Getting started

To get started with Chroma, install the official Python library via pip:

```bash
pip install chromadb
```

### Initializing a Persistent Client
To configure a local persistent instance that writes to a local directory:

```python
import chromadb

# Initialize local database directory
client = chromadb.PersistentClient(path="./chroma_db")

# Create or get a collection
collection = client.get_or_create_collection(name="home_automation_manuals")
```

## CLI examples

Chroma can be served as an independent background container using Docker or the native CLI command.

### 1. Launching Standalone Chroma Server
```bash
# Start Chroma server on port 8000
chroma run --path ./chroma_db --port 8000
```

### 2. Standard Diagnostics with Docker
```bash
# Spin up an isolated official Chroma DB instance in the background
docker run -d -p 8000:8000 chromadb/chroma
```

## API examples

### Programmatic Python Integration with Pydantic v2 Schema Validation and Metadata Filtering
This example showcases how to ingest a document chunk, generate a query, filter results by metadata category (using Chroma `where` clauses), and strictly validate the structure of retrieved search results using **Pydantic v2** prior to exposing the context to LLM routing layers (such as Claude 5.1, GPT-5.5, or Gemini 4.0 Pro).

```python
import uuid
import chromadb
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError

# Define structured output validation schemas using Pydantic v2
class ChromaSearchResult(BaseModel):
    document_id: str = Field(..., description="Unique document hash or ID")
    text_content: str = Field(..., description="The matching document chunk text")
    distance: float = Field(..., description="The semantic distance score (lower is closer)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary metadata tags associated with the chunk")

class ValidationResponse(BaseModel):
    query: str
    filter_category: Optional[str] = None
    results: List[ChromaSearchResult]
    total_retrieved: int

def ingest_and_query_chroma_filtered(query_text: str, category_filter: Optional[str] = None) -> Optional[ValidationResponse]:
    # Initialize ephemeral/in-memory client for isolated testing
    client = chromadb.EphemeralClient()
    collection = client.get_or_create_collection(name="home_automation_collection")

    # Ingest mock documents
    doc_1 = "To reset the smart thermostat, hold the power button for 10 seconds."
    doc_2 = "Setting up a custom tailscale exit node requires administrator privileges."
    doc_3 = "Thermostat temperature limits can be set in the advanced settings menu."

    collection.add(
        documents=[doc_1, doc_2, doc_3],
        metadatas=[{"category": "hardware"}, {"category": "network"}, {"category": "hardware"}],
        ids=["doc_1", "doc_2", "doc_3"]
    )

    try:
        # Build metadata filter if specified
        where_filter = {"category": category_filter} if category_filter else None

        # Perform vector query with optional metadata filtering
        results = collection.query(
            query_texts=[query_text],
            n_results=2,
            where=where_filter
        )

        # Map to Pydantic structure
        search_results = []
        if results and results['ids'] and len(results['ids'][0]) > 0:
            for i in range(len(results['ids'][0])):
                search_results.append(ChromaSearchResult(
                    document_id=results['ids'][0][i],
                    text_content=results['documents'][0][i],
                    distance=results['distances'][0][i] if results['distances'] else 0.0,
                    metadata=results['metadatas'][0][i] if results['metadatas'] else {}
                ))

        payload = {
            "query": query_text,
            "filter_category": category_filter,
            "results": search_results,
            "total_retrieved": len(search_results)
        }

        # Validate structured payload
        return ValidationResponse.model_validate(payload)

    except ValidationError as ve:
        print(f"Validation failed on Chroma retrieved result: {ve}")
        return None
    except Exception as e:
        print(f"Error querying ChromaDB: {e}")
        return None

if __name__ == "__main__":
    print("Initiating local ChromaDB semantic search verification with metadata filtering...")
    # Query with a category filter restricting results to hardware manual entries
    resp = ingest_and_query_chroma_filtered("How to factory reset?", category_filter="hardware")
    if resp:
        print(f"Chroma Context Retrieval successfully verified via Pydantic v2:")
        print(f"  Query: '{resp.query}' (Filtered by category: '{resp.filter_category}')")
        for idx, item in enumerate(resp.results):
            print(f"  Result #{idx + 1}:")
            print(f"    Content: {item.text_content}")
            print(f"    Distance: {item.distance}")
            print(f"    Metadata: {item.metadata}")
```

### MCP 3.1 / FastMCP 3.1 Vector Tool Registration
Chroma can be served as a native tool server under the **MCP 3.1** specification. This allows client models like Claude 5.1 and GPT-5.5 to run semantic queries against a Chroma collection dynamically.

Example server tool schema definition mapping:
```json
{
  "name": "query_chroma_knowledge",
  "description": "Perform a semantic vector search on ChromaDB collections for home automation knowledge.",
  "input_schema": {
    "type": "object",
    "properties": {
      "query_text": {
        "type": "string",
        "description": "The search string or question to locate relevant documentation chunks."
      },
      "category_filter": {
        "type": "string",
        "description": "Optional category filter to isolate search (e.g., 'hardware', 'network')."
      }
    },
    "required": ["query_text"]
  }
}
```

## Related tools / concepts
- [Milvus](milvus.md) — Scalable, distributed enterprise vector database.
- [Weaviate](weaviate.md) — SOTA hybrid search-native vector database.
- [Pinecone](pinecone.md) — Fully managed cloud-native vector database.
- [LlamaIndex](../ai_knowledge/llamaindex.md) — Primary data framework integrated deeply with Chroma.
- [LangChain](../ai_knowledge/langchain.md) — AI orchestration library with native Chroma wrappers.
- [Open WebUI](../../services/open-webui.md) — Graphical chat dashboard with built-in Chroma support for local RAG.

## Sources / references
- [Chroma Official Website](https://www.trychroma.com/)
- [Chroma Official Documentation](https://docs.trychroma.com/)
- [Chroma GitHub Repository](https://github.com/chroma-core/chroma)
- [Reddit r/LocalLLaMA: Classic Vector RAG vs Google NotebookLM Benchmarks](https://www.reddit.com/r/LocalLLaMA/comments/1ve5r8y/i_benchmarked_classic_vector_rag_vs_googles_new/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
