# Semantic Caching

## What it is

Semantic Caching is an optimization pattern that stores LLM responses and retrieves them for future queries that are semantically similar, rather than just identical. Unlike traditional key-value caching (which requires an exact string match), semantic caching uses vector embeddings and similarity search to identify if a "new" question is essentially asking the same thing as a previously cached one.

## What problem it solves

*   **Cost Reduction**: Drastically reduces API costs by avoiding redundant calls to expensive frontier models for common or repetitive queries.
*   **Latency Improvement**: Returns cached responses in milliseconds, providing a near-instant user experience compared to the seconds required for LLM generation.
*   **Token Efficiency**: Preserves rate limits and monthly quotas by serving "recycled" tokens from a local or dedicated cache database.
*   **Consistency**: Ensures that identical or nearly identical questions receive the same verified answer, reducing variability in agent behavior.

## Where it fits in the stack

Semantic Caching is an **Orchestration / Performance** pattern (Layer 4-5). it typically resides in the middleware layer between the application and the LLM provider, often integrated into a proxy like [LiteLLM](../../services/litellm.md) or implemented as a custom wrapper around a vector database.

## Architecture

```text
 User Query
     |
     v
 [ Embedding Model ] ----> [ Query Vector ]
                                 |
                                 v
                         [ Vector Database ]
                                 |
                        (Similarity Search)
                                 |
               +-----------------+-----------------+
               |                                   |
         [ Match Found? ]                    [ No Match ]
         (Score > Threshold)                       |
               |                                   v
               v                           [ Generative LLM ]
       [ Return Cached ]                           |
          [ Response ]                             v
                                           [ Store Response ]
                                           [ in Vector DB ]
                                                   |
                                                   v
                                            [ Return LLM ]
                                             [ Response ]
```

## Typical use cases

*   **Frequent FAQs**: Handling common user questions about a product or service.
*   **RAG Pipelines**: Caching the results of expensive retrieval-plus-generation steps for popular topics.
*   **Development & Testing**: Reducing costs during the iterative development of agent prompts.
*   **Autonomous Agents**: Caching common reasoning steps or environment observations.

## Getting started

Implementation typically requires a vector store (e.g., Chroma, Qdrant) and an embedding model.

=== "Conceptual Python Example"

    ```python
    import numpy as np
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import OllamaEmbeddings

    # 1. Setup Cache
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    cache_db = Chroma(collection_name="llm_cache", embedding_function=embeddings)

    def get_semantic_response(query, threshold=0.95):
        # 2. Search for similar queries
        results = cache_db.similarity_search_with_relevance_scores(query, k=1)

        if results and results[0][1] > threshold:
            print("--- Semantic Cache Hit ---")
            return results[0][0].metadata["response"]

        # 3. Cache Miss - Call LLM (Pseudo-code)
        print("--- Cache Miss - Calling LLM ---")
        response = call_real_llm(query)

        # 4. Store for next time
        cache_db.add_texts(
            texts=[query],
            metadatas=[{"response": response}]
        )
        return response
    ```

## Key decisions

*   **Similarity Threshold**: Setting the "hit" boundary (e.g., 0.90 vs 0.98). Too low causes "false hits" where different questions get the same answer; too high reduces the hit rate.
*   **Eviction Policy**: Determining when to clear the cache (TTL, Least Recently Used, or manual clearing when the underlying knowledge base changes).
*   **Embedding Model**: The cache's accuracy depends entirely on the embedding model's ability to capture semantic meaning.
*   **Context Sensitivity**: Deciding if the cache should be global, user-specific, or session-specific.

## Strengths

*   **Instant ROI**: One of the fastest ways to reduce operational costs in LLM-heavy systems.
*   **Scalability**: Allows a system to handle spikes in traffic for popular topics without hitting provider rate limits.
*   **Privacy-Friendly**: Can be implemented entirely locally using tools like [Ollama](../../services/ollama.md) and a local vector DB.

## Limitations

*   **Semantic Drift**: Small nuances in a query (e.g., "How do I do X?" vs "Why shouldn't I do X?") might be missed if the threshold is too loose.
*   **Stale Data**: Cached responses may become incorrect if the underlying information source changes (e.g., pricing or API documentation).
*   **Overhead**: Calculating embeddings and searching the vector DB adds a small amount of latency to every query (though much less than an LLM call).

## When to use it

*   When you have a high volume of repetitive queries.
*   When using expensive models like GPT-4o or Claude 3.5 Sonnet.
*   When building production-grade RAG systems for static documentation.

## When not to use it

*   For highly dynamic or personalized content (e.g., "What is my current bank balance?").
*   When queries are extremely unique and unlikely to repeat.
*   When absolute real-time accuracy is required and the underlying data changes every minute.

## Related tools / concepts

*   **Proxies**: [LiteLLM](../../services/litellm.md) (supports semantic caching with Redis/Couchbase).
*   **Vector Stores**: [Chroma](../../tools/infrastructure/index.md), [Qdrant](../../tools/infrastructure/index.md), [pgvector](../../tools/infrastructure/index.md).
*   **Libraries**: GPTCache, LangChain Cache, LlamaIndex Cache.
*   **Pattern**: [LLM Routing and Optimization](llm-routing-and-optimization.md).

## Sources / references

*   [GPTCache: A Library for Creating Semantic Cache for LLM Queries](https://github.com/zilliztech/GPTCache)
*   [LiteLLM: Caching Documentation](https://docs.litellm.ai/)

## Contribution Metadata

- Last reviewed: 2026-03-08
- Confidence: high
