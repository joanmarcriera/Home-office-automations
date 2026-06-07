# Pinecone

## What it is
Pinecone is a managed, cloud-native vector database designed for high-performance AI applications. It provides a simple API for storing, indexing, and querying high-dimensional vector embeddings, making it a popular choice for building Retrieval-Augmented Generation (RAG) systems and recommendation engines.

## What problem it solves
Managing vector databases at scale is operationally complex. Developers need to handle indexing algorithms (like HNSW), resource allocation, scaling, and high availability. Pinecone solves this by offering a "serverless" or managed experience where the underlying infrastructure is abstracted away, allowing developers to focus on building AI features rather than managing database clusters.

## Where it fits in the stack
**Category**: Infrastructure / Vector Databases

## Typical use cases
- **Retrieval-Augmented Generation (RAG)**: Providing relevant context to LLMs by searching through millions of document embeddings.
- **Semantic Search**: Finding similar text, images, or products based on meaning rather than exact keywords.
- **Recommendation Systems**: Using vector similarity to suggest content or products to users based on their behavior.
- **Anomaly Detection**: Identifying data points that are significantly different from the "normal" clusters in vector space.

## Strengths
- **Fully Managed**: Zero-ops experience with automated scaling and maintenance.
- **Low Latency**: Optimized for millisecond-level similarity search across billions of vectors.
- **Metadata Filtering**: Combines vector search with metadata-based filtering (e.g., "Find similar docs but only in the 'Legal' category").
- **Hybrid Search**: Supports blending dense vector search with sparse keyword search for better accuracy.

## Limitations
- **Cloud-Only**: No self-hosted or on-premises version; strictly a SaaS offering.
- **Cost**: Can become expensive as the number of vectors or dimensions increases, especially for high-throughput applications.
- **Closed Source**: Unlike alternatives like Milvus or Weaviate, the core engine is proprietary.

## When to use it
- When you want to get to production quickly without managing database infrastructure.
- For applications requiring high-speed similarity search with a relatively small operational team.
- When your application relies on cloud-native services and you are already using AWS, GCP, or Azure.

## When not to use it
- If you have strict data sovereignty requirements that mandate on-premises or air-gapped hosting.
- If you are building a simple, small-scale application where a local vector library (like FAISS) or a simple SQLite extension would suffice.
- If you require a fully open-source stack.

## Getting started

### Installation
```bash
pip install pinecone-client
```

### Basic Setup
1. Sign up at [Pinecone.io](https://www.pinecone.io/) and get an API key.
2. Initialize the client:
```python
from pinecone import Pinecone

pc = Pinecone(api_key="YOUR_API_KEY")
```

## Technical Examples

### 1. Creating a Serverless Index
```python
from pinecone import ServerlessSpec

pc.create_index(
    name="my-index",
    dimension=1536, # Dimension for OpenAI text-embedding-3-small
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)
```

### 2. Upserting Vectors with Metadata
```python
index = pc.Index("my-index")

index.upsert(
    vectors=[
        {
            "id": "doc1",
            "values": [0.1, 0.2, 0.3, ...],
            "metadata": {"category": "tech", "published": 2024}
        },
        {
            "id": "doc2",
            "values": [0.4, 0.5, 0.6, ...],
            "metadata": {"category": "finance", "published": 2023}
        }
    ]
)
```

### 3. Querying with Metadata Filters
```python
results = index.query(
    vector=[0.1, 0.2, 0.3, ...],
    top_k=2,
    include_metadata=True,
    filter={
        "category": {"$eq": "tech"}
    }
)

for match in results["matches"]:
    print(f"ID: {match['id']}, Score: {match['score']}, Metadata: {match['metadata']}")
```

## Related tools / concepts
- [Milvus](milvus.md) — open-source high-performance vector database.
- [Weaviate](weaviate.md) — open-source vector database with GraphQL support.
- [Vector DB Comparison](../../knowledge_base/vector-db-comparison.md) — choosing the right vector store.
- [RAG Pattern](../../knowledge_base/patterns/rag-pattern.md) — how vector databases fit into AI workflows.
- [Search Patterns](../../knowledge_base/patterns/search-patterns.md) — architecting retrieval systems.
- [LlamaIndex](../ai_knowledge/llamaindex.md) — data framework for LLM applications.
- [LangChain](../ai_knowledge/langchain.md) — building modular AI pipelines.
- [OpenAI](../ai_knowledge/openai.md) — providing embedding models often used with Pinecone.

## Sources / references
- [Pinecone Documentation](https://docs.pinecone.io/)
- [Pinecone Pricing](https://www.pinecone.io/pricing/)

## Contribution Metadata
- Last reviewed: 2026-06-06
- Confidence: high
