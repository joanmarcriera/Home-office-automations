# Search Patterns

## What it is
Search patterns in AI represent the architectural strategies used to retrieve relevant information from large datasets to augment Large Language Model (LLM) responses. In 2026, this has evolved into **Agentic Search**, where agents dynamically refine queries, traverse knowledge graphs, and use multi-step retrieval loops to find high-fidelity information. These patterns encompass traditional lexical search, semantic vector search, and advanced hybrid retrieval methods.

## What problem it solves
As the volume of unstructured data grows, simple keyword search often fails to capture the underlying meaning or intent of a user's query. Conversely, purely semantic search can miss exact matches for technical terms or product IDs. Search patterns provide a framework for:
- **Capturing Intent**: Moving beyond keywords to understand what the user is actually looking for.
- **Precision at Scale**: Finding specific "needles in haystacks" within billions of documents.
- **Contextual Grounding**: Providing the most relevant "facts" to an LLM to prevent hallucinations.
- **Relational Discovery**: Using knowledge graphs to find connected information that is not explicitly mentioned in the query.

## Where it fits in the stack
Search patterns reside in the **Retrieval Layer** of an AI application. They act as the bridge between the **Orchestration Layer** (where the agent lives) and the **Data Layer** (where vector databases, graph databases, and search engines reside).

## Typical use cases
- **Retrieval-Augmented Generation (RAG)**: Providing grounding context for agents answering complex domain-specific questions.
- **Enterprise Knowledge Discovery**: Building "agentic wikis" that can synthesize information across multiple internal platforms.
- **Agentic Web Research**: Enabling autonomous agents to use [Exa AI](../../tools/providers/exa_ai.md) or [Tavily](../../tools/providers/tavily.md) to perform deep-dive research.
- **Multimodal Retrieval**: Searching for images, videos, or audio snippets using natural language descriptions (e.g., via [ColQwen](../../tools/ai_knowledge/colqwen.md)).

## Strengths
- **Improved Relevance**: Combines multiple retrieval strategies (Hybrid Search) to cover different types of queries.
- **Semantic Understanding**: Handles synonyms, paraphrasing, and complex natural language intent.
- **Scalability**: Efficiently retrieves from billions of documents using Approximate Nearest Neighbor (ANN) algorithms.
- **Dynamic Refinement**: Agents can iteratively improve their search queries based on initial results.

## Limitations
- **Complexity**: Advanced patterns like hybrid search, re-ranking, and graph traversal require complex infrastructure.
- **Latency**: Multiple retrieval stages (e.g., vector search -> cross-encoder re-ranking) add to the overall response time.
- **Context Window Constraints**: Even the best search pattern must ultimately fit the retrieved results into the LLM's context window.

## When to use it
- When building production-grade RAG applications that require high retrieval accuracy.
- If your users interact with your data using complex, natural language questions.
- When your data contains both technical terms (requiring precision) and descriptive content (requiring semantic understanding).
- When information is spread across multiple disconnected sources that need to be synthesized.

## When not to use it
- For very small datasets where a simple keyword search or even a flat file read would suffice.
- If retrieval accuracy is not a critical factor in your application's performance.
- When the data is highly structured and can be perfectly queried using SQL or a direct API.

## Getting started
To implement modern search patterns:
1. **Choose your Embeddings**: Select a model like `text-embedding-3-large` or a local BGE model for vectorization.
2. **Select a Vector Store**: Deploy [Pinecone](../../tools/infrastructure/pinecone.md), [Milvus](../../tools/infrastructure/milvus.md), or [Weaviate](../../tools/infrastructure/weaviate.md).
3. **Implement Hybrid Search**: Configure your database to use both BM25 (lexical) and vector (semantic) search.
4. **Add a Re-ranker**: Use a Cross-Encoder (e.g., from Cohere or Jina) to sort the top 20-50 results for the highest precision.
5. **Set up Agentic Loops**: Enable your agent to use tools like [Exa AI](../../tools/providers/exa_ai.md) for iterative query refinement.

## CLI examples
Using the [Exa AI CLI](../../tools/providers/exa_ai.md) for agentic search:

```bash
# Search for recent research on Agentic Search patterns
exa search "latest advancements in agentic RAG and search patterns June 2026" --num-results 5 --use-autoprompt
```

Using `curl` to query a [Pinecone](../../tools/infrastructure/pinecone.md) index with a vector:

```bash
curl -X POST "https://your-index-id.svc.us-west1-gcp.pinecone.io/query" \
  -H "Api-Key: $PINECONE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "vector": [0.1, 0.2, 0.3, ...],
    "topK": 10,
    "includeMetadata": true
  }'
```

## API examples
Example of Hybrid Search with [Weaviate](../../tools/infrastructure/weaviate.md) v4 Python SDK:

```python
import weaviate
import weaviate.classes as wvc

client = weaviate.connect_to_local()

collection = client.collections.get("Documentation")
response = collection.query.hybrid(
    query="How to implement MCP 3.0?",
    alpha=0.5, # 0.5 balances keyword and vector search
    limit=5
)

for obj in response.objects:
    print(obj.properties["content"])

client.close()
```

Implementing a re-ranking loop in Python:

```python
from sentence_transformers import CrossEncoder

# 1. Initial Retrieval (e.g., from Vector DB)
candidates = ["Doc A content...", "Doc B content...", "Doc C content..."]
query = "What is agentic search?"

# 2. Re-ranking
model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
scores = model.predict([(query, doc) for doc in candidates])

# 3. Sort by score
ranked_results = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
```

## Related tools / concepts
- [RAG Pattern](rag.md) — The broader architecture for retrieval-augmented generation.
- [Tool Calling & MCP](tool-calling-and-mcp.md) — How agents use search as a tool via the Model Context Protocol.
- [Exa AI](../../tools/providers/exa_ai.md) — Neural search engine designed specifically for AI agents.
- [Tavily](../../tools/providers/tavily.md) — Search API optimized for LLMs and RAG.
- [Pinecone](../../tools/infrastructure/pinecone.md) — Managed vector database for high-performance search.
- [Milvus](../../tools/infrastructure/milvus.md) — Open-source vector database for large-scale retrieval.
- [Weaviate](../../tools/infrastructure/weaviate.md) — Vector database with native hybrid search and re-ranking.
- [ColQwen](../../tools/ai_knowledge/colqwen.md) — Multimodal retrieval using late interaction.

## Sources / References
- [Hybrid Search and Reranking - Ubuntu](https://ubuntu.com/blog/hybrid-search-and-reranking-a-deeper-look-at-rag)
- [What is Hybrid Search? - FalkorDB](https://www.falkordb.com/blog/what-is-hybrid-search-in-ai/)
- [Cross-Encoders for Re-ranking - SBERT](https://www.sbert.net/examples/applications/retrieve_rerank/README.html)
- [Agentic Search: Query Refinement Patterns](https://example.com/agentic-search-research)

## Contribution Metadata
- Last reviewed: 2026-06-24
- Confidence: high
