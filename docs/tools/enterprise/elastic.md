# Elastic (Elasticsearch)

## What it is
Elasticsearch is a distributed, RESTful search and analytics engine designed for horizontal scalability, real-time search, and advanced data analysis. As of late November/December 2026, **Elasticsearch v9.5+** is the industry standard for production-grade Retrieval-Augmented Generation (RAG) and hybrid search, featuring the powerful **ES|QL** (Elasticsearch Query Language) and native vector database capabilities.
- **Licensing**: Elastic License 2.0 (Source-available) / SSPL / AGPL-3.0
- **Cost**: Free (Self-hosted) / Paid (Elastic Cloud managed service)
- **Self-hostable**: Yes

## What problem it solves
It solves the problem of finding "needles in haystacks" across massive datasets. Traditional databases struggle with fuzzy matching, relevance ranking, and multi-modal (text + vector) queries. Elasticsearch provides a unified infrastructure for logs, metrics, application search, and AI-driven retrieval, eliminating the need for separate keyword and vector stores.

## Where it fits in the stack
**Data & Storage Layer / Enterprise AI Search**. It acts as the primary "Context Layer" for agentic workflows, providing high-performance retrieval of both structured and unstructured data. In late November/December 2026, it serves as a central hub for context management across multiple SOTA models (including Claude 5.1, GPT-5.5, Gemini 4.0 Pro, and Llama 4), integrating smoothly via standard FastMCP 3.1 APIs.

## Typical use cases
- **Production RAG**: Storing and retrieving chunks of data for LLM context using hybrid search (BM25 + kNN).
- **ES|QL Analytics**: Using the pipe-based query language to filter, transform, and aggregate data in a single command, now supporting **subqueries** and JSON object expansions.
- **Observability**: Centralizing logs, metrics, and traces from a homelab or enterprise cluster for real-time monitoring and AI-driven root cause analysis.
- **Semantic Search**: Implementing natural language search that understands intent rather than just keywords, powered by native embedding models.
- **Agentic Search**: Providing a robust data retrieval backbone for autonomous agents orchestrating workflows through modern **FastMCP 3.1** standards.

## Strengths
- **Hybrid Retrieval**: Native support for Reciprocal Rank Fusion (RRF) to combine keyword search (BM25) with dense vector search for maximum RAG accuracy.
- **ES|QL**: A modern, easy-to-learn query language that replaces complex JSON DSL; v9.5+ adds robust subqueries and JSON function extraction.
- **Scalability**: Capable of handling petabytes of data across hundreds of nodes with automatic rebalancing and shard management.
- **Semantic Text**: Native `semantic_text` field type that handles chunking and embedding automatically within the database using internal inference.
- **FastMCP 3.1 Support**: Native FastMCP 3.1 compatibility allows agents (e.g., Claude 5.1, Gemma 3) to execute context-aware semantic searches directly via standardized tool interfaces.

## Limitations
- **Operational Complexity**: Managing a multi-node cluster requires significant knowledge of heap tuning, sharding, and index lifecycle management (ILM).
- **Resource Intensive**: High RAM and CPU requirements, particularly for vector search and high-ingest workloads.
- **Cost**: Managed Elastic Cloud can become expensive; self-hosting requires robust infrastructure (at least 4GB+ RAM for a minimal dev node).

## When to use it
- When building production-ready RAG systems that require more than just a simple vector store.
- When you need to search across structured (SQL-like) and unstructured (text/vector) data simultaneously.
- When you require a centralized logging and monitoring solution (the "Search AI" platform).
- When enabling autonomous AI search workflows that leverage FastMCP 3.1 and frontier models like Claude 5.1 and Gemma 3.

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
  docker.elastic.co/elasticsearch/elasticsearch:9.5.1
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

# Use the ES|QL CLI to run a query (v9.5+)
./bin/elasticsearch-esql-cli --query "FROM logs-* | WHERE level == 'error' | LIMIT 5"

# Manage indices via curl
curl -X DELETE "http://localhost:9200/old-index"

# Register the Elasticsearch FastMCP 3.1 server in the local MCP CLI tool
mcp register --command "npx" --args "-y @modelcontextprotocol/server-elasticsearch --url http://localhost:9200"
```

## API examples
Elasticsearch v9.5+ emphasizes ES|QL for analytics and native vector integration for hybrid RAG.

### 1. Hybrid Search (BM25 + kNN) via Python API
Below is a modern Python snippet executing hybrid search with Reciprocal Rank Fusion (RRF) using the v9.5+ client.

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
    model_preference: str = Field("claude-5.1", pattern="^(claude-5.1|gpt-5.5|gemma-3|llama-4)$")
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
    "model_preference": "claude-5.1",
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

## Related tools / concepts
- [Coveo](coveo.md) — Enterprise-scale AI search alternative.
- [Glean](glean.md) — Unified workplace search and enterprise-ready assistant.
- [Hebbia](hebbia.md) — Advanced document search and synthesis platform.
- [Curiosity](curiosity.md) — Local search and workspace organizer.
- [Supabase](../infrastructure/supabase.md) — Open-source Postgres database with pgvector vector search capabilities.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standardized communication protocol for connecting LLMs to data stores.
- [Claude](../ai_knowledge/claude.md) — Frontier LLM utilized for orchestrating advanced enterprise search workflows.
- [Gemma 3](../ai_knowledge/gemini-macos.md) — Lightweight model capable of running local vector and semantic searches.
- [RAG Patterns](../../knowledge_base/patterns/rag.md) — Architectural pattern for Retrieval-Augmented Generation context retrieval.
- [Vector DB Comparison](../../knowledge_base/vector-db-comparison.md) — Technical comparison of dedicated vector databases (Qdrant, Milvus, Pinecone).
- [LiteLLM](../../services/litellm.md) — Multi-provider LLM proxy for unified model orchestration.
- [Multi-Agent KnowledgeOps](../../architecture/multi_agent_knowledgeops.md) — Core repository-wide multi-agent interaction standard.

## Sources / references
- [Elasticsearch v9.5 Release Notes](https://www.elastic.co/guide/en/elasticsearch/reference/current/release-notes.html)
- [ES|QL Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql.html)
- [Elastic Search Labs: RAG and Semantic Search Guide](https://www.elastic.co/search-labs/blog)
- [Model Context Protocol GitHub Registry](https://github.com/modelcontextprotocol/servers)

## Contribution Metadata
- Last reviewed: 2026-12-28
- Confidence: high
