# Elastic (Elasticsearch)

Elasticsearch is a distributed, RESTful search and analytics engine designed for horizontal scalability, real-time search, and advanced data analysis. As of May 2026, **Elasticsearch v9.4+** is the industry standard for production-grade Retrieval-Augmented Generation (RAG) and hybrid search, featuring the powerful **ES|QL** (Elasticsearch Query Language) and native vector database capabilities.

## What it is
Elasticsearch is the core of the Elastic Stack (ELK). It is a schema-flexible, JSON-document-based database built on Apache Lucene. It excels at full-text search, structured search, and vector search, making it a "Swiss Army Knife" for data intelligence.

## What problem it solves
It solves the problem of finding "needles in haystacks" across massive datasets. Traditional databases struggle with fuzzy matching, relevance ranking, and multi-modal (text + vector) queries. Elasticsearch provides a unified infrastructure for logs, metrics, application search, and AI-driven retrieval.

## Where it fits in the stack
- **Category**: [Enterprise AI](../enterprise/index.md) / Search & Infrastructure
- **Layer**: [Data & Storage Layer](../../architecture/README.md)

## Typical use cases
- **Production RAG**: Storing and retrieving chunks of data for LLM context using hybrid search (BM25 + Vector).
- **ES|QL Analytics**: Using the pipe-based query language to filter, transform, and aggregate data in a single command.
- **Observability**: Centralizing logs and metrics from a homelab/enterprise cluster for real-time monitoring.
- **Application Search**: Implementing fast, type-ahead search with sophisticated relevance tuning.

## Strengths
- **Hybrid Retrieval**: Native support for combining keyword search (BM25) with dense vector search for maximum RAG accuracy.
- **ES|QL**: A modern, easy-to-learn query language that replaces complex JSON DSL for many use cases.
- **Scalability**: Capable of handling petabytes of data across hundreds of nodes with automatic rebalancing.
- **Semantic Text**: Native `semantic_text` field type that handles chunking and embedding automatically within the database.
- **Mature Ecosystem**: Seamless integration with Kibana (visualization) and LangChain/LlamaIndex (AI orchestration).

## Limitations
- **Operational Complexity**: Managing a multi-node cluster requires significant knowledge of heap tuning, sharding, and index lifecycle management (ILM).
- **Resource Intensive**: High RAM and CPU requirements, especially for vector search and high-ingest observability workloads.
- **Cost**: Managed Elastic Cloud can become expensive; self-hosting requires robust infrastructure.

## When to use it
- When building production-ready RAG systems that require more than just a simple vector store.
- When you need to search across structured and unstructured data simultaneously.
- When you require a centralized logging and monitoring solution (ELK stack).

## When not to use it
- For simple keyword search on small datasets where [SQLite FTS](../../services/navidrome.md) or a lighter tool would suffice.
- If you are constrained by low-memory hardware (e.g., a single Raspberry Pi with 2GB RAM).
- For primary relational data storage where ACID transactions across multiple tables are critical.

## Licensing and cost
- **Open Source**: Elastic License (Source-available).
- **Cost**: Free (Self-hosted) / Paid (Elastic Cloud managed service).
- **Self-hostable**: Yes.

## Getting started

### Docker (Single Node for Development)
```bash
docker run -p 9200:9200 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  -e "ES_JAVA_OPTS=-Xms1g -Xmx1g" \
  docker.elastic.co/elasticsearch/elasticsearch:9.4.2
```

### Health Check (cURL)
```bash
curl -X GET "localhost:9200/_cluster/health?pretty"
```

## ES|QL Examples
ES|QL is the modern way to query Elastic. It uses a pipe syntax similar to Unix shells.

```sql
# Search for logs, filter by error, and count by host
FROM logs-*
| WHERE level == "error"
| STATS count = COUNT(*) BY host
| SORT count DESC
| LIMIT 10
```

## RAG & Vector Search

### 1. Hybrid Search (BM25 + kNN)
Combining traditional text matching with vector similarity (Dense Vector).

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
            "query_vector": [0.1, -0.2, ...],
            "k": 10,
            "num_candidates": 100
          }
        }
      ]
    }
  }
}
```

### 2. Automatic Chunking & Embedding (Python)
Using the `semantic_text` field type available in v9.x.

```python
# Define mapping with native inference
mapping = {
    "properties": {
        "content": {
            "type": "semantic_text",
            "inference_id": "my-huggingface-model"
        }
    }
}
```

## Related tools / concepts
- [Coveo](coveo.md) — Enterprise-scale AI search.
- [Supabase](../infrastructure/supabase.md) — Vector search via pgvector.
- [RAG Patterns](../../knowledge_base/patterns/rag.md) — For implementation strategies.
- [Kibana](https://www.elastic.co/kibana) — The visualization layer for Elastic.
- [Qdrant](../../knowledge_base/vector-db-comparison.md) — Specialized vector database.

## Links
- [Official Website](https://www.elastic.co/)
- [ES|QL Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql.html)
- [Search Labs Blog](https://www.elastic.co/search-labs)

## Backlog
- [x] Perform quarterly technical freshness audit (May 2026).

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-05-31

## Sources / References
- https://www.elastic.co/guide/en/elasticsearch/reference/current/release-notes.html
- https://www.elastic.co/search-labs/blog/dense-vector-search-elasticsearch-query-language
- https://blog.devops.dev/building-production-ready-rag-with-elasticsearch-a-real-world-implementation-guide-c3ef353cc0d3
- KnowledgeOps Triage (2026-05-31)
