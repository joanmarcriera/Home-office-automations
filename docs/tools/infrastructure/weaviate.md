# Weaviate

## What it is
Weaviate is an open-source vector database that allows you to store data objects and vector embeddings from your favorite ML-models, and scale seamlessly into billions of data objects. It is designed for developers who want to build AI-native applications with high performance and reliability.

## What problem it solves
Managing and searching through massive amounts of unstructured data (text, images, audio) is challenging. Weaviate provides a scalable infrastructure for vector search, enabling semantic search, recommendation engines, and Retrieval-Augmented Generation (RAG) by converting unstructured data into searchable vectors.

## Where it fits in the stack
**Category**: Infrastructure / Vector Database

## Typical use cases
- **Retrieval-Augmented Generation (RAG)**: Providing relevant context to LLMs for more accurate answers.
- **Semantic Search**: Finding information based on meaning rather than just keywords.
- **Recommendation Systems**: Suggesting products or content based on visual or textual similarity.
- **Image Search**: Building applications that can search for images using other images or text descriptions.

## Strengths
- **Speed & Scalability**: Capable of sub-second search across billions of objects.
- **Modular Architecture**: Supports various vectorization modules (OpenAI, HuggingFace, Cohere, etc.).
- **Hybrid Search**: Combines vector search with traditional keyword search (BM25) for better results.
- **GraphQL API**: Offers a flexible and powerful API for querying data.

## Limitations
- **Memory Consumption**: Vector indices can be memory-intensive.
- **Learning Curve**: The GraphQL API and schema configuration might require some time to master for those used to traditional SQL.

## When to use it
- When you need a production-grade vector database for RAG or semantic search.
- When you require a self-hostable solution with enterprise-grade features.
- When you want to leverage hybrid search capabilities out of the box.

## When not to use it
- For simple applications where a basic full-text search engine (like SQLite FTS) is sufficient.
- If you have extremely limited RAM and cannot afford the memory overhead of a vector database.

## Licensing and cost
- **Open Source**: Yes (BSD 3-Clause)
- **Cost**: Free (Self-hosted) / Paid (Managed Cloud)
- **Self-hostable**: Yes

## Getting started

### Docker Deployment
```yaml
services:
  weaviate:
    command:
    - --host
    - 0.0.0.0
    - --port
    - '8080'
    - --scheme
    - http
    image: semitechnologies/weaviate:1.24.1
    ports:
    - 8080:8080
    restart: on-failure:0
    environment:
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'true'
      PERSISTENCE_DATA_PATH: '/var/lib/weaviate'
      DEFAULT_VECTORIZER_MODULE: 'none'
      ENABLE_MODULES: ''
      CLUSTER_HOSTNAME: 'node1'
```

## API examples

### Schema Creation (Python)
```python
import weaviate

client = weaviate.Client("http://localhost:8080")

class_obj = {
    "class": "Document",
    "vectorizer": "none",
    "properties": [
        {
            "name": "content",
            "dataType": ["text"],
        }
    ]
}

client.schema.create_class(class_obj)
```

### Semantic Search (GraphQL)
```graphql
{
  Get {
    Document (
      nearText: {
        concepts: ["AI infrastructure"]
      }
    ) {
      content
      _additional {
        distance
      }
    }
  }
}
```

## Related tools / concepts
- [Verba](../intake_storage/verba.md) — A RAG application built on top of Weaviate.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) — The architectural pattern Weaviate often enables.
- [LangChain](../ai_knowledge/langchain.md) — Frequently used to orchestrate flows involving Weaviate.
- [Ollama](../../services/ollama.md) — Can provide local embeddings for Weaviate.
- [Dify](../ai_knowledge/dify.md) — Integrates Weaviate for its RAG features.
- [Pinecone](pinecone.md) — A managed-only alternative to Weaviate.
- [Milvus](milvus.md) — Another open-source vector database alternative.

## Sources / references
- [Official Website](https://weaviate.io/)
- [GitHub Repository](https://github.com/weaviate/weaviate)
- [Weaviate Documentation](https://weaviate.io/developers/weaviate)

## Contribution Metadata
- Last reviewed: 2026-06-05
- Confidence: high
