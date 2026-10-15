# Elastic (Elasticsearch)

## What it is
Elasticsearch is a distributed, RESTful search and analytics engine designed for horizontal scalability, real-time search, and advanced data analysis. As of early 2027, **Elasticsearch v9.6+** is the industry standard for production-grade Retrieval-Augmented Generation (RAG) and hybrid search, featuring the powerful **ES|QL** (Elasticsearch Query Language) and native vector database capabilities.
- **Licensing**: Elastic License 2.0 (Source-available) / SSPL / AGPL-3.0
- **Cost**: Free (Self-hosted) / Paid (Elastic Cloud managed service)
- **Self-hostable**: Yes

## What problem it solves
It solves the problem of finding "needles in haystacks" across massive datasets. Traditional databases struggle with fuzzy matching, relevance ranking, and multi-modal (text + vector) queries. Elasticsearch provides a unified infrastructure for logs, metrics, application search, and AI-driven retrieval, eliminating the need for separate keyword and vector stores.

## Where it fits in the stack
**Data & Storage Layer / Enterprise AI Search**. It acts as the primary "Context Layer" for agentic workflows, providing high-performance retrieval of both structured and unstructured data. In early 2027, it serves as a central hub for context management across multiple SOTA models (including Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, Gemma 4, DeepSeek-V4, and Qwen 3.6 VL), integrating smoothly via standard FastMCP 3.1 Task Protocol APIs.

## Architecture & Enterprise Hybrid Search Flow

```
                                ELASTICSEARCH 9.6+ HYBRID AI SEARCH ARCHITECTURE

  ┌────────────────────────┐    ┌────────────────────────┐    ┌────────────────────────┐
  │  Claude 5.6 / Agents   │    │ FastMCP 3.1 Tools API  │    │  Log Ingestion Pipeline│
  └───────────┬────────────┘    └───────────┬────────────┘    └───────────┬────────────┘
              │                             │                             │
              └──────────────────────┬──────┴─────────────────────────────┘
                                     │
                                     ▼
                      ┌──────────────────────────────┐
                      │ Elasticsearch Query Frontend │
                      │  - ES|QL Pipe Parser         │
                      │  - Semantic Text Inference   │
                      └──────────────┬───────────────┘
                                     │
            ┌────────────────────────┴────────────────────────┐
            ▼                                                 ▼
  ┌────────────────────────┐                        ┌────────────────────────┐
  │ BM25 Lexical Engine    │                        │ Dense Vector Engine    │
  │ - Inverted Index       │                        │ - HNSW Vector Index    │
  │ - BM25 Scoring         │                        │ - kNN Vector Retriever │
  └───────────┬────────────┘                        └───────────┬────────────┘
              │                                                 │
              └──────────────────────┬──────────────────────────┘
                                     │
                                     ▼
                      ┌──────────────────────────────┐
                      │  Reciprocal Rank Fusion (RRF)│
                      │  - Rank Window: 100          │
                      │  - Rank Constant: 60         │
                      └──────────────┬───────────────┘
                                     │
                                     ▼
                      ┌──────────────────────────────┐
                      │   Pydantic v2 Result Stream  │
                      │   - Strictly Validated RAG   │
                      └──────────────────────────────┘
```

## SOTA Vector & Search Platform Comparison

| Platform / Database | Vector Index Type | Hybrid RRF Support | Query Language | Built-in Inference | Self-Hosting Footprint |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Elasticsearch 9.6+** | HNSW + Quantization | Native (Reciprocal Rank Fusion) | ES|QL + JSON DSL | Native (`semantic_text`) | Medium/High (4GB+ RAM) |
| **Qdrant** | HNSW / Quantized | Manual payload combining | REST / gRPC Filter DSL | External via Proxy | Low/Medium (512MB+ RAM) |
| **Milvus** | HNSW / IVF_FLAT | Hybrid Search API | SQL-like filtering | External models | High (Multi-node microservices) |
| **Pinecone** | Proprietary Cloud | Hybrid sparse-dense | Proprietary API | External Embeddings | Cloud-only (Managed) |
| **pgvector (Supabase)** | HNSW / IVFFlat | Custom SQL RRF ranking | Standard PostgreSQL | External / PL/Python | Low/Medium (Depends on Postgres) |

## Typical use cases
- **Production RAG**: Storing and retrieving chunks of data for LLM context using hybrid search (BM25 + kNN).
- **ES|QL Analytics**: Using the pipe-based query language to filter, transform, and aggregate data in a single command, now supporting **subqueries** and JSON object expansions.
- **Observability**: Centralizing logs, metrics, and traces from a homelab or enterprise cluster for real-time monitoring and AI-driven root cause analysis.
- **Semantic Search**: Implementing natural language search that understands intent rather than just keywords, powered by native embedding models.
- **Agentic Search**: Providing a robust data retrieval backbone for autonomous agents orchestrating workflows through modern **FastMCP 3.1** standards.

## Strengths
- **Hybrid Retrieval**: Native support for Reciprocal Rank Fusion (RRF) to combine keyword search (BM25) with dense vector search for maximum RAG accuracy.
- **ES|QL**: A modern, easy-to-learn query language that replaces complex JSON DSL; v9.6+ adds robust subqueries and JSON function extraction.
- **Scalability**: Capable of handling petabytes of data across hundreds of nodes with automatic rebalancing and shard management.
- **Semantic Text**: Native `semantic_text` field type that handles chunking and embedding automatically within the database using internal inference.
- **FastMCP 3.1 Support**: Native FastMCP 3.1 compatibility allows agents (e.g., Claude 5.6, Gemma 4) to execute context-aware semantic searches directly via standardized tool interfaces.

## Limitations
- **Operational Complexity**: Managing a multi-node cluster requires significant knowledge of heap tuning, sharding, and index lifecycle management (ILM).
- **Resource Intensive**: High RAM and CPU requirements, particularly for vector search and high-ingest workloads.
- **Cost**: Managed Elastic Cloud can become expensive; self-hosting requires robust infrastructure (at least 4GB+ RAM for a minimal dev node).

## When to use it
- When building production-ready RAG systems that require more than just a simple vector store.
- When you need to search across structured (SQL-like) and unstructured (text/vector) data simultaneously.
- When you require a centralized logging and monitoring solution (the "Search AI" platform).
- When enabling autonomous AI search workflows that leverage FastMCP 3.1 and frontier models like Claude 5.6 and Gemma 4.

## When not to use it
- For simple keyword search on small datasets where a lighter tool would suffice.
- If you are constrained by low-memory hardware (e.g., a single Raspberry Pi with 2GB RAM).
- For primary relational data storage where strict multi-table ACID transactions are the primary requirement.

## Getting started

### Docker (Single Node for Development)
```bash
docker run -d --name elasticsearch -p 9200:9200 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  -e "ES_JAVA_OPTS=-Xms2g -Xmx2g" \
  docker.elastic.co/elasticsearch/elasticsearch:9.6.0
```

### Health Check (cURL)
```bash
curl -X GET "http://localhost:9200/_cluster/health?pretty"
```

### Registering the FastMCP 3.1 Server
To connect Elasticsearch to your agentic workflows (like Claude Desktop or other client engines), register the Elasticsearch MCP server:
```bash
# Add the Elasticsearch server to your MCP configuration
npx -y @modelcontextprotocol/server-elasticsearch --url http://localhost:9200
```

## CLI examples
The Elastic stack provides several CLI tools, but most interaction happens via the REST API, dev tools, or the `elasticsearch-sql-cli`.

```bash
# Check cluster version and health
curl -X GET "http://localhost:9200/"

# Use the ES|QL CLI to run a query (v9.6+)
./bin/elasticsearch-esql-cli --query "FROM logs-* | WHERE level == 'error' | LIMIT 5"

# Manage indices via curl
curl -X DELETE "http://localhost:9200/old-index"

# Register the Elasticsearch FastMCP 3.1 server in the local MCP CLI tool
mcp register --command "npx" --args "-y @modelcontextprotocol/server-elasticsearch --url http://localhost:9200"
```

## FastMCP 3.1 Elasticsearch Server Implementation

The snippet below demonstrates a production-grade **FastMCP 3.1** server that exposes Elasticsearch v9.6+ hybrid search and ES|QL analytical querying tools to autonomous AI agents.

```python
from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, Field, ValidationError
from typing import Dict, Any, List, Optional
import httpx

# Initialize FastMCP 3.1 Elasticsearch server
mcp = FastMCP(
    "elasticsearch-mcp-server",
    instructions="FastMCP 3.1 server for querying Elasticsearch 9.6+ indices using hybrid RRF search and ES|QL."
)

ELASTICSEARCH_URL = "http://localhost:9200"

class EsqlQueryRequest(BaseModel):
    query: str = Field(..., description="ES|QL query string (e.g. 'FROM logs-* | WHERE level == \"error\" | LIMIT 10')")
    format: str = Field(default="json", description="Response format (json, csv, txt)")

class HybridSearchRequest(BaseModel):
    index: str = Field(..., description="Target Elasticsearch index name")
    query_text: str = Field(..., description="Text query to search semantically and lexically")
    vector_field: str = Field(default="vector_field", description="Field name storing dense vectors")
    top_k: int = Field(default=10, ge=1, le=100, description="Number of results to return")

@mcp.tool()
async def execute_esql_query(request: EsqlQueryRequest, ctx: Context) -> Dict[str, Any]:
    """Execute a pipe-based ES|QL query against Elasticsearch 9.6+."""
    await ctx.info(f"Executing ES|QL query: {request.query}")
    endpoint = f"{ELASTICSEARCH_URL}/_query"
    payload = {"query": request.query}

    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(endpoint, json=payload, headers={"Content-Type": "application/json"}, timeout=10.0)
            if res.status_code != 200:
                return {"error": f"Elasticsearch HTTP {res.status_code}", "details": res.text}
            return res.json()
        except Exception as err:
            return {"error": "Failed to connect to Elasticsearch", "details": str(err)}

@mcp.tool()
async def execute_hybrid_rrf_search(request: HybridSearchRequest, ctx: Context) -> Dict[str, Any]:
    """Perform a Reciprocal Rank Fusion (RRF) hybrid search combining BM25 keyword matching and dense kNN vector retrieval."""
    await ctx.info(f"Executing Hybrid RRF search on index '{request.index}' for query: {request.query_text}")
    endpoint = f"{ELASTICSEARCH_URL}/{request.index}/_search"

    rrf_payload = {
        "size": request.top_k,
        "retriever": {
            "rrf": {
                "retrievers": [
                    {
                        "standard": {
                            "query": { "match": { "text": request.query_text } }
                        }
                    },
                    {
                        "knn": {
                            "field": request.vector_field,
                            "query_vector_builder": {
                                "text_embedding": {
                                    "model_id": "my-embedding-model",
                                    "model_text": request.query_text
                                }
                            }
                        }
                    }
                ],
                "rank_window_size": 100,
                "rank_constant": 60
            }
        }
    }

    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(endpoint, json=rrf_payload, headers={"Content-Type": "application/json"}, timeout=10.0)
            if res.status_code != 200:
                return {"error": f"Elasticsearch HTTP {res.status_code}", "details": res.text}
            return res.json()
        except Exception as err:
            return {"error": "Failed to connect to Elasticsearch", "details": str(err)}

if __name__ == "__main__":
    mcp.run()
```

## API examples
Elasticsearch v9.6+ emphasizes ES|QL for analytics and native vector integration for hybrid RAG.

### 1. Hybrid Search (BM25 + kNN) via Python API
Below is a modern Python snippet executing hybrid search with Reciprocal Rank Fusion (RRF) using the v9.6+ client.

```python
from elasticsearch import Elasticsearch

# Initialize the Elasticsearch client
es = Elasticsearch("http://localhost:9200")

# Perform a hybrid search combining keyword and vector queries
response = es.search(
    index="my-rag-index",
    retriever={
        "rrf": {
            "retrievers": [
                {
                    "standard": {
                        "query": { "match": { "text": "how to scale k3s clusters" } }
                    }
                },
                {
                    "knn": {
                        "field": "vector_field",
                        "query_vector_builder": {
                            "text_embedding": {
                                "model_id": "my-embedding-model",
                                "model_text": "how to scale k3s clusters"
                            }
                        }
                    }
                }
            ],
            "rank_window_size": 100,
            "rank_constant": 60
        }
    }
)

for hit in response['hits']['hits']:
    print(f"ID: {hit['_id']} | Score: {hit['_score']} | Content: {hit['_source']['text']}")
```

### 2. Elastic Payload Validation with Strict Pydantic v2 Schema
The following robust Python example uses **Pydantic v2** to programmatically validate the search payload configurations before submitting them to Elasticsearch, guaranteeing robust typing and preventing schema mismatch errors.

```python
import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ValidationError, model_validator

# 1. Define Elasticsearch Search Configuration schema
class ElasticSearchConfig(BaseModel):
    query_string: str = Field(..., min_length=2, max_length=200)
    target_index: str = Field(..., pattern="^[a-z0-9-_]+$")
    model_preference: str = Field("claude-5.6", pattern="^(claude-5.6|gpt-5.6|gemma-4|deepseek-v4)$")
    vector_search_enabled: bool = Field(default=True)
    num_results: int = Field(default=10, ge=1, le=100)

    @model_validator(mode="after")
    def restrict_vector_query(self) -> "ElasticSearchConfig":
        if self.target_index.startswith("legacy-") and self.vector_search_enabled:
            raise ValueError("Legacy indices do not support vector search operations.")
        return self

# 2. Example representation of raw input parameters
raw_input = {
    "query_string": "How to scale K3s cluster architectures",
    "target_index": "production-rag-index",
    "model_preference": "claude-5.6",
    "vector_search_enabled": True,
    "num_results": 15
}

# 3. Validate search configurations using Pydantic v2
try:
    validated_config = ElasticSearchConfig.model_validate(raw_input)
    print("Elasticsearch search query configuration is valid!")
    print(f"Index to Search: {validated_config.target_index}")
    print(f"Embedding/RAG Model: {validated_config.model_preference}")
except ValidationError as e:
    print(f"Elasticsearch Search Validation failed with errors: {e.json()}")
```

## Operational Guardrails & Troubleshooting

| Operational Issue | Root Cause | Impact | Resolution Strategy |
| :--- | :--- | :--- | :--- |
| **CircuitBreakerException (Data Too Large)** | JVM Heap exhaustion caused by large vector memory requirements | Cluster fails queries and drops nodes | Adjust ES_JAVA_OPTS to set heap size to 50% of system RAM (max 32GB) and enable byte quantization for vector fields. |
| **High Vector Indexing Latency** | HNSW graph construction under heavy concurrent write loads | Slow ingestion and drop in indexing throughput | Increase `index.translog.flush_threshold_size` and defer HNSW indexing during bulk loading using deferred vector indices. |
| **RRF Ranking Inconsistency** | Mismatched field mappings across shards or unnormalized BM25 scores | Sub-optimal ranking in hybrid search results | Set explicit `rank_window_size` (e.g. 100) and ensure uniform mappings across all index shards. |
| **Elasticsearch Out of Memory (OOM) Kill** | Docker container memory limit hit due to unmapped off-heap memory | Process killed by OS kernel | Set Docker memory limit higher than ES JVM heap (e.g., 8GB container limit for a 4GB JVM heap). |
| **ES|QL Query Syntax Errors** | Using deprecated JSON DSL syntax inside `_query` endpoints | Query returns 400 Bad Request | Ensure ES|QL queries follow pipe format (`FROM index | WHERE ... | LIMIT x`). |

## Related tools / concepts
- [Coveo](coveo.md) — Enterprise-scale AI search alternative.
- [Glean](glean.md) — Unified workplace search and enterprise-ready assistant.
- [Hebbia](hebbia.md) — Advanced document search and synthesis platform.
- [Curiosity](curiosity.md) — Local search and workspace organizer.
- [Supabase](../infrastructure/supabase.md) — Open-source Postgres database with pgvector vector search capabilities.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standardized communication protocol for connecting LLMs to data stores.
- [Claude](../ai_knowledge/claude.md) — Frontier LLM utilized for orchestrating advanced enterprise search workflows.
- [Gemma 4](../ai_knowledge/gemini-macos.md) — Lightweight model capable of running local vector and semantic searches.
- [RAG Patterns](../../knowledge_base/patterns/rag.md) — Architectural pattern for Retrieval-Augmented Generation context retrieval.
- [Vector DB Comparison](../../knowledge_base/vector-db-comparison.md) — Technical comparison of dedicated vector databases (Qdrant, Milvus, Pinecone).
- [LiteLLM](../../services/litellm.md) — Multi-provider LLM proxy for unified model orchestration.
- [Multi-Agent KnowledgeOps](../../architecture/multi_agent_knowledgeops.md) — Core repository-wide multi-agent interaction standard.

## Sources / references
- [Elasticsearch v9.6 Release Notes](https://www.elastic.co/guide/en/elasticsearch/reference/current/release-notes.html)
- [ES|QL Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql.html)
- [Elastic Search Labs: RAG and Semantic Search Guide](https://www.elastic.co/search-labs/blog)
- [Model Context Protocol GitHub Registry](https://github.com/modelcontextprotocol/servers)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
