# Search Patterns

## What it is
Search patterns in AI represent the architectural strategies used to retrieve relevant information from large datasets to augment Large Language Model (LLM) responses. In early January 2027, this has shifted from simple Retrieval-Augmented Generation (RAG) to **Agentic Search** and **Autonomous Discovery Loops**, where frontier models (such as Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, Gemma 4, DeepSeek-V4, and Qwen 3.6 VL) iteratively refine queries, navigate dynamic knowledge graphs, and negotiate tool endpoints using the **FastMCP 3.1 Task Protocol**. Late-Interaction embeddings (such as ColBERT and ColQwen) are widely used to maintain token-level alignment and superior retrieval accuracy.

## What problem it solves
As the volume of unstructured data grows, simple keyword search often fails to capture the underlying meaning or intent of a user's query. Conversely, purely semantic search can miss exact matches for technical terms or product IDs. Modern search patterns solve:
- **Retrieval Quality & Precision**: Combining lexical and semantic methods (hybrid search) with Cross-Encoder re-rankers to ensure high-quality context.
- **Token-Level Matching**: Using late-interaction mechanisms (e.g. ColQwen, ColBERT) to align query and document tokens, ensuring technical jargon is retrieved accurately.
- **Hallucination Mitigation**: Grounding model responses in verified facts rather than internal training parameters.
- **Multimodal Discovery**: Searching across text, images, and video using unified embedding spaces.
- **Real-Time Synthesis**: Synthesizing answers from rapidly changing web data via Agentic Search providers like [Exa AI](../../tools/providers/exa_ai.md).
- **Multi-Agent Coordination**: Routing and executing parallel search queries across federated data stores using MCP 3.1 / FastMCP 3.1 router architectures.

## System Architecture

```
                                      Hybrid Search & Re-ranking Flow

  +-----------------------+        +------------------------+        +--------------------------+
  |  Natural Language     | ---->  |  Hybrid Search Router  | ---->  | Dense Vector Search      |
  |  Query Input          |        |  (Lexical + Semantic)  |        | (Milvus / Pinecone HNSW) |
  +-----------------------+        +------------------------+        +--------------------------+
                                               |                                  |
                                               v                                  v
  +-----------------------+        +------------------------+        +--------------------------+
  | LLM Context Window    | <----  | Cohere / Cross-Encoder | <----  | Sparse Lexical Search    |
  | (Prompt Augmentation) |        | Re-ranking Engine      |        | (BM25 / SPLADE Index)    |
  +-----------------------+        +------------------------+        +--------------------------+
```

## Search Pattern Architectural Matrix

| Search Strategy | Retrieval Precision | Query Latency | Implementation Complexity | Primary Ideal Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Naive Dense Vector** | Moderate | Very Low (<20ms) | Low | Broad semantic clustering & topic search |
| **Hybrid (BM25 + Vector)**| High | Low (<50ms) | Moderate | Enterprise document search with technical jargon |
| **Late Interaction (ColBERT)**| Extremely High | Low-Moderate (<80ms)| High | Token-level exact match across dense corpora |
| **Agentic Loop Search** | Highest | High (>500ms) | Very High | Autonomous research & multi-step web discovery |

## Diagnostic Troubleshooting Matrix

| Issue Symptom | Root Cause | Diagnostic Check Command | Resolution Path |
| :--- | :--- | :--- | :--- |
| **Low Retrieval Precision** | Unbalanced dense vs lexical weighting in RRF | Inspect intermediate top_k BM25 vs vector recall scores | Adjust Reciprocal Rank Fusion (RRF) `k` parameter (standard `k=60`) or re-tune dense alpha weights. |
| **Re-ranking Latency Spike** | Passing too many candidate documents to Cross-Encoder | Measure Cohere/Cross-Encoder API round-trip latency | Prune initial retrieval candidate set from top_k=100 down to top_k=20 before invoking cross-encoder re-ranking. |
| **Out-Of-Memory (OOM) Vector DB**| Excessive HNSW M/efConstruction index parameters | Inspect memory limits: `docker stats milvus-standalone` | Tune vector index parameters (`M=16, efConstruction=64`) or switch to IVF-PQ/SCaNN vector quantization formats. |
| **FastMCP Search Tool Timeout** | Concurrent query lock or database connection starvation | Check vector DB connection pool logs and active socket handles | Increase async connection pool limit (`pool_size=32`) and enforce tool query timeout guardrails (15s). |
| **Missing Technical Part Numbers**| Pure semantic embedding model smoothing out alphanumeric tokens | Test BM25 keyword search directly on raw indexed fields | Enforce hybrid search mode with exact match filters for SKU/part numbers using BM25 tokenizers. |
| **Pydantic ValidationError on Tool Call**| Extra schema parameters passed during LLM tool invocation | Check FastMCP stderr for `extra_forbidden` validation errors | Clean parameter schema or verify client agent respects strict `ConfigDict(extra="forbid")`. |
| **Etcd Cluster Compaction Lag**| Etcd revisions growing unboundedly in high-churn ingestion | Inspect etcd storage metrics: `etcdctl endpoint status -w table` | Configure automatic compaction (`ETCD_AUTO_COMPACTION_MODE=revision`) and compact etcd revisions. |
| **Stale Query Results in Cache**| Ingestion events not triggering Redis cache invalidation keys | Monitor Redis invalidation events: `redis-cli monitor | grep -i search` | Implement write-through cache eviction or configure TTL expiration window (e.g., 300s). |
| **ColBERT Max Token Truncation**| Long query string exceeds Late-Interaction 128-token query mask | Check query token lengths with tokenizer inspect utility | Split multi-sentence query into discrete sub-queries or expand query token limit to 256. |
| **MinIO Connection Refused on Milvus Boot**| MinIO container took longer to pass ready state than Milvus init | Inspect Milvus logs: `docker logs milvus-standalone | grep -i minio` | Ensure Docker Compose `depends_on` utilizes `condition: service_healthy` on MinIO. |

## Where it fits in the stack
**Category**: Knowledge Base / AI Patterns. These patterns reside in the **Retrieval and Context layer** of an application, sitting between the [Vector Database](../../tools/infrastructure/index.md) and the [Inference Engine](../../tools/infrastructure/index.md).

## Typical use cases
- **Agentic RAG**: Providing a multi-step retrieval loop for an agent to answer complex diagnostic questions.
- **Enterprise Semantic Search**: Building intelligent search engines for corporate wikis that understand domain-specific jargon.
- **Multimodal Product Discovery**: Finding products based on visual similarity or natural language descriptions.
- **Autonomous Research**: Using agents to scour the web and internal docs to generate comprehensive market reports.
- **Federated MCP 3.1 Search**: Dynamically selecting and querying local or cloud databases using MCP 3.1 tools.

## Strengths
- **High Precision and Recall**: Hybrid methods capture both exact matches (via BM25) and semantic intent.
- **Scalability**: Can be applied across billions of documents using efficient vector stores like [Milvus](../../tools/infrastructure/milvus.md) or [Pinecone](../../tools/infrastructure/pinecone.md).
- **Interpretability & Citation**: Provides "citations" or "sources" for LLM outputs, increasing user trust.
- **Dynamic Adaptability**: Pulls from live APIs and databases rather than relying on static training sets.

## Limitations
- **Orchestration Complexity**: Advanced patterns like re-ranking and multi-query expansion add significant architectural overhead.
- **Latency**: Multiple retrieval stages (retrieval -> re-ranking -> synthesis) increase response time.
- **Embedding Mismatch**: Using an embedding model that wasn't trained on your specific domain can lead to poor semantic matches.
- **Operational Cost**: High-frequency embedding generation and re-ranking can increase operational spend.

## When to use it
- When building production-grade RAG applications that require high retrieval accuracy.
- For AI agents that need to navigate complex, fragmented knowledge bases.
- When your data contains both technical terms (requiring lexical precision) and descriptive content (requiring semantic understanding).
- For implementing [Agentic Search](../../tools/providers/exa_ai.md) workflows with frontier models.

## When not to use it
- For very small datasets (< 100 documents) where a simple keyword search or flat file read is faster.
- When the LLM's internal training data is sufficient for the task (e.g., general knowledge questions).
- In extremely low-latency applications where the overhead of a retrieval loop is unacceptable.

## Getting started
1. **Define the Data Source**: Identify whether you are searching internal docs ([MinIO](../../tools/intake_storage/minio.md)), structured databases, or the web.
2. **Select an Embedding Model**: Choose a model compatible with your domain (e.g., OpenAI `text-embedding-3-small` or a local BGE/Ollama model).
3. **Initialize a Vector Store**: Deploy [Milvus](../../tools/infrastructure/milvus.md) or use a managed service like [Pinecone](../../tools/infrastructure/pinecone.md).
4. **Implement a Hybrid Pipeline**: Use a framework like [LlamaIndex](../../tools/frameworks/index.md) or [LangChain](../../tools/frameworks/index.md) to combine BM25 (lexical) and Vector (semantic) search.
5. **Add a Re-ranker**: Integrate a Cross-Encoder (e.g., Cohere Re-rank v3) to prune the final results for the LLM.

## Systemd Service Unit Configuration

To run the Hybrid Search & Re-ranking Router Service on a Linux host, create `/etc/systemd/system/search-mcp-router.service`:

```ini
[Unit]
Description=FastMCP 3.1 Hybrid Search and Re-ranking Router Service
After=network.target milvus.service

[Service]
Type=simple
User=searchrouter
Group=searchrouter
WorkingDirectory=/opt/search-mcp-router
Environment="PATH=/opt/search-mcp-router/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin"
Environment="MILVUS_URI=http://localhost:19530"
Environment="COHERE_API_KEY=your-cohere-api-key"
ExecStart=/opt/search-mcp-router/venv/bin/fastmcp run /opt/search-mcp-router/server.py --port 8085
Restart=always
RestartSec=5s
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now search-mcp-router.service
sudo systemctl status search-mcp-router.service
```

## Production Multi-Container Docker Cluster (`compose.yaml`)

Deploy an enterprise hybrid search topology with Milvus vector database, MinIO object store, Etcd coordination cluster, Redis query cache, and FastMCP 3.1 hybrid retrieval gateway:

```yaml
version: '3.8'

services:
  etcd:
    container_name: milvus-etcd
    image: quay.io/coreos/etcd:v3.5.14
    environment:
      - ETCD_AUTO_COMPACTION_MODE=revision
      - ETCD_AUTO_COMPACTION_RETENTION=1000
      - ETCD_QUOTA_BACKEND_BYTES=4294967296
      - ETCD_SNAPSHOT_COUNT=50000
    volumes:
      - etcd-data:/etcd
    command: etcd -advertise-client-urls=http://127.0.0.1:2379 -listen-client-urls http://0.0.0.0:2379 --data-dir=/etcd
    healthcheck:
      test: ["CMD", "etcdctl", "endpoint", "health"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - search-cluster-net

  minio:
    container_name: milvus-minio
    image: minio/minio:RELEASE.2025-01-20T14-49-07Z
    environment:
      MINIO_ACCESS_KEY: minioadmin
      MINIO_SECRET_KEY: minioadmin
    volumes:
      - minio-data:/minio_data
    command: minio server /minio_data --console-address ":9001"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - search-cluster-net

  milvus-standalone:
    container_name: milvus-standalone
    image: milvusdb/milvus:v2.5.2
    command: ["milvus", "run", "standalone"]
    security_opt:
      - seccomp:unconfined
    environment:
      ETCD_ENDPOINTS: etcd:2379
      MINIO_ADDRESS: minio:9000
    volumes:
      - milvus-data:/var/lib/milvus
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9091/healthz"]
      interval: 15s
      timeout: 10s
      retries: 5
    ports:
      - "19530:19530"
      - "9091:9091"
    depends_on:
      etcd:
        condition: service_healthy
      minio:
        condition: service_healthy
    networks:
      - search-cluster-net

  redis-search-cache:
    container_name: redis-search-cache
    image: redis:7.2-alpine
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 1gb --maxmemory-policy allkeys-lru
    ports:
      - "6381:6379"
    volumes:
      - redis-search-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
    networks:
      - search-cluster-net

  search-mcp-router:
    container_name: search-mcp-router
    image: python:3.11-slim
    restart: unless-stopped
    ports:
      - "8085:8085"
    environment:
      - MILVUS_URI=http://milvus-standalone:19530
      - REDIS_URL=redis://redis-search-cache:6379/0
      - COHERE_API_KEY=${COHERE_API_KEY}
      - PINECONE_API_KEY=${PINECONE_API_KEY}
      - MCP_PORT=8085
    volumes:
      - ./router:/opt/search-mcp-router:ro
    working_dir: /opt/search-mcp-router
    command: python3 server.py
    depends_on:
      milvus-standalone:
        condition: service_healthy
      redis-search-cache:
        condition: service_healthy
    networks:
      - search-cluster-net
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2048M

networks:
  search-cluster-net:
    driver: bridge

volumes:
  etcd-data:
  minio-data:
  milvus-data:
  redis-search-data:
```

## CLI examples
Using the [Ollama](../../services/ollama.md) CLI to generate embeddings for a local document:

```bash
# Generate embeddings for a text snippet using a local model
curl http://localhost:11434/api/embeddings -d '{
  "model": "mxbai-embed-large",
  "prompt": "Llama 4 is a powerful open-source model."
}'
```

Querying an agentic search provider like [Exa AI](../../tools/providers/exa_ai.md) via CLI:
```bash
# Search for recent papers on agentic search patterns using Exa's auto-prompt and neural search
curl -s -X POST "https://api.exa.ai/search" \
     -H "x-api-key: $EXA_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "latest research on hybrid RAG patterns in late December 2026",
       "useAutoprompt": true,
       "numResults": 5,
       "type": "neural"
     }'
```

## API examples
Implementation of a Hybrid Search and Re-ranking query using Python and the Cohere/Pinecone SDKs. The response is validated strictly using **Pydantic v2** models and exposed as a **FastMCP 3.1** tool.

### Python: FastMCP 3.1 Hybrid Search Tool with strict Pydantic v2 typing
```python
import os
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, ValidationError, ConfigDict
from pinecone import Pinecone
import cohere
from fastmcp import FastMCP

# Initialize FastMCP 3.1 Server
mcp = FastMCP("Search-Patterns-Router", version="3.1.0")

class SearchQueryInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    query: str = Field(..., min_length=3, max_length=500, description="The natural language query string")
    index_name: str = Field(..., description="The target vector database index name")
    top_k: int = Field(default=5, ge=1, le=100, description="Number of re-ranked documents to return")

    @field_validator("query")
    @classmethod
    def clean_query_text(cls, v: str) -> str:
        return v.strip()

class RankedDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(..., description="Unique document hash or identifier")
    text: str = Field(..., description="The raw document snippet text")
    score: float = Field(..., description="Relevance score computed by Cohere Re-rank v3")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

# Initialize clients (ensure API keys are injected)
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY", "mock-key"))
co = cohere.ClientV2(api_key=os.environ.get("COHERE_API_KEY", "mock-key"))

class DocumentIndexPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(..., description="Document identifier")
    text: str = Field(..., min_length=10, description="Raw document text to embed and index")
    index_name: str = Field(..., description="Destination index name")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata tags")

class IndexOperationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: str = Field(..., description="Operation outcome (e.g. success, error)")
    document_id: str = Field(..., description="ID of indexed record")
    indexed_tokens: int = Field(..., description="Token count of indexed body")

@mcp.tool(name="hybrid_search_and_rerank", description="Executes hybrid vector + lexical search with Cohere Re-rank v3.")
def hybrid_search_and_rerank(raw_input: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Executes a high-precision hybrid retrieval and Cohere Re-rank v3 pipeline,
    validated strictly with Pydantic v2 models.
    """
    try:
        validated_input = SearchQueryInput.model_validate(raw_input)
    except ValidationError as err:
        raise ValueError(f"Invalid search parameters: {err}")

    # 1. Generate Query Embeddings
    embedding_response = co.embed(
        texts=[validated_input.query],
        model="embed-english-v3.0",
        input_type="search_query"
    )
    query_vector = embedding_response.embeddings[0]

    # 2. Query Pinecone with Hybrid Search (Semantic + Sparse/Lexical)
    index = pc.Index(validated_input.index_name)
    results = index.query(
        vector=query_vector,
        top_k=validated_input.top_k * 2,
        include_metadata=True
    )

    documents = []
    for match in results.matches:
        doc_text = match.metadata.get("text", "") if match.metadata else ""
        documents.append({"id": match.id, "text": doc_text, "meta": match.metadata or {}})

    if not documents:
        return []

    # 3. Apply Cohere Re-rank v3 for high-precision ordering
    rerank_results = co.rerank(
        query=validated_input.query,
        documents=[doc["text"] for doc in documents],
        top_n=validated_input.top_k,
        model="rerank-english-v3.0"
    )

    ranked_docs = []
    for result in rerank_results.results:
        original_doc = documents[result.index]
        try:
            doc_obj = RankedDocument(
                id=original_doc["id"],
                text=original_doc["text"],
                score=result.relevance_score,
                metadata=original_doc["meta"]
            )
            ranked_docs.append(doc_obj.model_dump())
        except ValidationError as err:
            print(f"Skipping malformed retrieval record: {err}")
            continue

    return ranked_docs

@mcp.tool(name="index_document_snippet", description="Indexes a document passage into vector store with dense embeddings.")
def index_document_snippet(raw_input: Dict[str, Any]) -> Dict[str, Any]:
    """Inserts and embeds a new document record into the target search collection."""
    try:
        payload = DocumentIndexPayload.model_validate(raw_input)
    except ValidationError as err:
        raise ValueError(f"Payload validation failed: {err}")

    # Generate document embeddings
    emb = co.embed(texts=[payload.text], model="embed-english-v3.0", input_type="search_document")
    doc_vector = emb.embeddings[0]

    # Store in index
    idx = pc.Index(payload.index_name)
    meta = payload.metadata.copy()
    meta["text"] = payload.text
    idx.upsert(vectors=[(payload.id, doc_vector, meta)])

    return IndexOperationResult(
        status="success",
        document_id=payload.id,
        indexed_tokens=len(payload.text.split())
    ).model_dump()

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [RAG Pattern](rag-pattern.md) — The foundational pattern for retrieval-augmented generation.
- [Exa AI](../../tools/providers/exa_ai.md) — Neural search engine for AI agents.
- [Milvus](../../tools/infrastructure/milvus.md) — High-performance open-source vector store.
- [Pinecone](../../tools/infrastructure/pinecone.md) — Managed vector database with native hybrid search.
- [ColBERT / ColQwen](data-copilot-agentic-rag.md) — Advanced late-interaction retrieval models.
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md) — Standard for agents to access search tools.
- [OpenRouter](../../tools/ai_knowledge/openrouter.md) — Used for routing search-related LLM calls.
- [MinIO](../../tools/intake_storage/minio.md) — Storage for raw documents before indexing.

## Sources / References
- [LlamaIndex: Hybrid Search Implementation Guide](https://docs.llamaindex.ai/en/stable/examples/vector_stores/HybridSearch/)
- [Exa AI Documentation: Agentic Search Patterns](https://docs.exa.ai/docs/agentic-search)
- [Pinecone: What is Hybrid Search?](https://www.pinecone.io/learn/hybrid-search/)
- [ColBERT v2: Effective and Efficient Late Interaction](https://arxiv.org/abs/2112.01488)
- [Cohere ClientV2 Re-rank Guide](https://docs.cohere.com/docs/reranking)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
