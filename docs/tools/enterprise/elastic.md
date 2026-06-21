# Elastic (Elasticsearch)

## What it is
Elasticsearch is a distributed, RESTful search and analytics engine designed for horizontal scalability, real-time search, and advanced data analysis. As of June 2026, **Elasticsearch v9.4+** is the industry standard for production-grade Retrieval-Augmented Generation (RAG) and hybrid search, featuring the powerful **ES|QL** (Elasticsearch Query Language) and native vector database capabilities.
- **Licensing**: Elastic License 2.0 (Source-available) / SSPL / AGPL-3.0
- **Cost**: Free (Self-hosted) / Paid (Elastic Cloud managed service)
- **Self-hostable**: Yes

## What problem it solves
It solves the problem of finding "needles in haystacks" across massive datasets. Traditional databases struggle with fuzzy matching, relevance ranking, and multi-modal (text + vector) queries. Elasticsearch provides a unified infrastructure for logs, metrics, application search, and AI-driven retrieval, eliminating the need for separate keyword and vector stores.

## Where it fits in the stack
**Data & Storage Layer / Enterprise AI Search**. It acts as the primary "Context Layer" for agentic workflows, providing high-performance retrieval of both structured and unstructured data.

## Typical use cases
- **Production RAG**: Storing and retrieving chunks of data for LLM context using hybrid search (BM25 + kNN).
- **ES|QL Analytics**: Using the pipe-based query language to filter, transform, and aggregate data in a single command, now supporting **subqueries** in v9.4.
- **Observability**: Centralizing logs, metrics, and traces from a homelab or enterprise cluster for real-time monitoring and AI-driven root cause analysis.
- **Semantic Search**: Implementing natural language search that understands intent rather than just keywords, powered by native embedding models.

## Strengths
- **Hybrid Retrieval**: Native support for Reciprocal Rank Fusion (RRF) to combine keyword search (BM25) with dense vector search for maximum RAG accuracy.
- **ES|QL**: A modern, easy-to-learn query language that replaces complex JSON DSL; v9.4 adds subqueries and JSON function extraction.
- **Scalability**: Capable of handling petabytes of data across hundreds of nodes with automatic rebalancing and shard management.
- **Semantic Text**: Native `semantic_text` field type that handles chunking and embedding automatically within the database using internal inference.
- **Mature Ecosystem**: Seamless integration with Kibana (visualization) and LangChain/LlamaIndex/MCP (AI orchestration).

## Limitations
- **Operational Complexity**: Managing a multi-node cluster requires significant knowledge of heap tuning, sharding, and index lifecycle management (ILM).
- **Resource Intensive**: High RAM and CPU requirements, particularly for vector search and high-ingest observability workloads.
- **Cost**: Managed Elastic Cloud can become expensive; self-hosting requires robust infrastructure (at least 4GB+ RAM for a minimal dev node).

## When to use it
- When building production-ready RAG systems that require more than just a simple vector store.
- When you need to search across structured (SQL-like) and unstructured (text/vector) data simultaneously.
- When you require a centralized logging and monitoring solution (the "Search AI" platform).

## When not to use it
- For simple keyword search on small datasets where [SQLite FTS](../../services/navidrome.md) or a lighter tool would suffice.
- If you are constrained by low-memory hardware (e.g., a single Raspberry Pi with 2GB RAM).
- For primary relational data storage where strict multi-table ACID transactions are the primary requirement.

## Getting started

### Docker (Single Node for Development)
```bash
docker run -p 9200:9200 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  -e "ES_JAVA_OPTS=-Xms2g -Xmx2g" \
  docker.elastic.co/elasticsearch/elasticsearch:9.4.2
```

### Health Check (cURL)
```bash
curl -X GET "localhost:9200/_cluster/health?pretty"
```

## CLI examples
The Elastic stack provides several CLI tools, but most interaction happens via the REST API or the `elasticsearch-sql-cli`.

```bash
# Check cluster version and health
curl -u elastic:password -X GET "https://localhost:9200/" -k

# Use the ES|QL CLI to run a query (v9.4+)
./bin/elasticsearch-esql-cli --query "FROM logs-* | WHERE level == 'error' | LIMIT 5"

# Manage indices via the 'dev tools' in Kibana or curl
curl -X DELETE "localhost:9200/old-index"
```

## API examples
Elasticsearch v9.4 emphasizes **ES|QL** for both analytics and retrieval.

### 1. Hybrid Search (BM25 + kNN) via API
```json
POST /my-index/_search
{
  "retriever": {
    "rrf": {
      "retrievers": [
        {
          "standard": {
            "query": { "match": { "text": "how to scale k3s" } }
          }
        },
        {
          "knn": {
            "field": "vector_field",
            "query_vector_builder": {
              "text_embedding": {
                "model_id": "my-embedding-model",
                "model_text": "how to scale k3s"
              }
            }
          }
        }
      ]
    }
  }
}
```

### 2. ES|QL with Subquery (v9.4+)
```sql
FROM (
  FROM kibana_sample_data_ecommerce
  | WHERE taxful_total_price >= 1000
  | EVAL domain = "business"
  | KEEP order_date, domain, customer_full_name
), (
  FROM kibana_sample_data_logs
  | WHERE response >= "500"
  | EVAL domain = "operations"
  | KEEP @timestamp, domain, request
)
| SORT order_date DESC
| LIMIT 10
```

## Related tools / concepts
- [Kibana](https://www.elastic.co/kibana) — The visualization and management layer for Elastic.
- [Supabase](../infrastructure/supabase.md) — Vector search via pgvector (lighter alternative).
- [RAG Patterns](../../knowledge_base/patterns/rag.md) — For implementation strategies.
- [Qdrant](../../knowledge_base/vector-db-comparison.md) — Specialized high-performance vector database.
- [LiteLLM](../../services/litellm.md) — For integrating model providers with Elastic inference.
- [Coveo](coveo.md) — Enterprise-scale AI search alternative.
- [MCP Registry](../../architecture/multi_agent_knowledgeops.md) — For agentic context injection.

## Sources / References
- [Elasticsearch 9.4 Release Notes](https://www.elastic.co/guide/en/elasticsearch/reference/current/release-notes.html)
- [ES|QL Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql.html)
- [Elastic Search Labs: RAG Guide](https://www.elastic.co/search-labs/blog)
- [Elasticsearch End of Life Dates](https://endoflife.date/elasticsearch)

## Contribution Metadata
- Last reviewed: 2026-06-21
- Confidence: high
