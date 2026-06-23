# Weaviate

## What it is
Weaviate is an open-source vector database that allows you to store data objects and vector embeddings from your favorite ML-models, and scale seamlessly into billions of data objects. As of June 2026, it is a primary infrastructure choice for AI-native applications requiring high-performance semantic search and native MCP 3.0 integration.

## What problem it solves
Managing and searching through massive amounts of unstructured data (text, images, audio) is challenging. Weaviate provides a scalable infrastructure for vector search, enabling semantic search, recommendation engines, and Retrieval-Augmented Generation (RAG) by converting unstructured data into searchable vectors. It bridges the gap between raw data and agentic reasoning.

## Where it fits in the stack
**Category**: [Infrastructure](index.md) / [Vector Database](../../knowledge_base/index.md). It serves as the "long-term memory" layer for agents, providing grounded context via vector retrieval.

## Typical use cases
- **Retrieval-Augmented Generation (RAG)**: Providing relevant context to LLMs for more accurate answers.
- **Semantic Search**: Finding information based on meaning rather than just keywords.
- **Recommendation Systems**: Suggesting products or content based on visual or textual similarity.
- **Image Search**: Building applications that can search for images using other images or text descriptions.
- **Agentic Memory**: Storing and retrieving past agent interactions and state via MCP 3.0.

## Strengths
- **Speed & Scalability**: Capable of sub-second search across billions of objects.
- **Modular Architecture**: Supports various vectorization modules (OpenAI, HuggingFace, Cohere, etc.).
- **Hybrid Search**: Combines vector search with traditional keyword search (BM25) for better results.
- **Multi-modal Support**: Natively handles text, image, and even audio embeddings.
- **Native MCP 3.0**: Enables seamless integration with agentic frameworks for automated tool use.

## Limitations
- **Memory Consumption**: Vector indices can be memory-intensive, especially for large datasets.
- **Learning Curve**: The GraphQL API and schema configuration might require some time to master compared to traditional SQL.
- **Resource Intensive**: High-performance deployments require significant RAM and CPU/GPU resources.

## When to use it
- When you need a production-grade vector database for RAG or semantic search.
- When you require a self-hostable solution with enterprise-grade features (sharding, replication).
- When you want to leverage hybrid search capabilities out of the box.
- For AI-native applications requiring multi-modal search (text + images).

## When not to use it
- For simple applications where a basic full-text search engine (like SQLite FTS) is sufficient.
- If you have extremely limited RAM and cannot afford the memory overhead of a vector database.
- For purely relational data tasks where SQL is more appropriate.

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
      ENABLE_MODULES: 'text2vec-openai,multi2vec-clip'
      CLUSTER_HOSTNAME: 'node1'
```

## CLI examples
Weaviate provides a dedicated CLI for administrative tasks and schema management.

```bash
# Install the Weaviate CLI
pip install weaviate-client

# Check the health of a local instance
weaviate health --url http://localhost:8080

# List all classes in the schema
weaviate schema list --url http://localhost:8080
```

## API examples

### Schema Creation (Python v4 SDK)
```python
import weaviate
import weaviate.classes as wvc

client = weaviate.connect_to_local()

try:
    client.collections.create(
        name="Document",
        vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),
        properties=[
            wvc.config.Property(name="content", data_type=wvc.config.DataType.TEXT),
        ]
    )
finally:
    client.close()
```

### Semantic Search (GraphQL)
```graphql
{
  Get {
    Document (
      nearText: {
        concepts: ["AI infrastructure June 2026"]
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
- [Qdrant](qdrant.md) — A Rust-based high-performance vector database.
- [Chroma](chroma.md) — An AI-native open-source embedding database.

## Sources / references
- [Weaviate Official Website](https://weaviate.io/)
- [GitHub Repository](https://github.com/weaviate/weaviate)
- [Weaviate Documentation](https://weaviate.io/developers/weaviate)
- [Weaviate v4 Python Client Release Notes](https://weaviate.io/blog/python-client-v4-release)

## Contribution Metadata
- Last reviewed: 2026-06-23
- Confidence: high
