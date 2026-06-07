# Search Patterns

## What it is
Search patterns in AI represent the architectural strategies used to retrieve relevant information from large datasets to augment Large Language Model (LLM) responses. This includes traditional lexical search, semantic vector search, and advanced hybrid retrieval methods.

## What problem it solves
As the volume of unstructured data grows, simple keyword search often fails to capture the underlying meaning or intent of a user's query. Conversely, purely semantic search can miss exact matches for technical terms or product IDs. Search patterns provide a framework for combining these methods to ensure high-quality, accurate context for AI agents.

## Where it fits in the stack
**Category**: Knowledge Base / AI Patterns

## Typical use cases
- **Retrieval-Augmented Generation (RAG)**: Providing context to an LLM for answering questions about specific documents.
- **Enterprise Search**: Building intelligent search engines for corporate wikis or technical documentation.
- **Semantic Recommendation**: Suggesting similar products or articles based on user interest and intent.

## Strengths
- **Improved Relevance**: Combines multiple retrieval strategies to cover different types of queries.
- **Semantic Understanding**: Handles synonyms and complex natural language intent.
- **Scalability**: Can be applied across billions of documents using efficient vector databases.

## Limitations
- **Complexity**: Advanced patterns like hybrid search and re-ranking require more complex infrastructure and orchestration.
- **Latency**: Multiple retrieval and re-ranking stages can increase the overall response time of the AI system.

## When to use it
- When building production-grade RAG applications that require high retrieval accuracy.
- If your users interact with your data using complex, natural language questions.
- When your data contains both technical terms (requiring precision) and descriptive content (requiring semantic understanding).

## When not to use it
- For very small datasets where a simple keyword search or even a flat file read would suffice.
- If retrieval accuracy is not a critical factor in your application's performance.

## Core Search Modalities

### 1. Lexical (Keyword) Search
- **Mechanism**: Matches exact words or phrases using algorithms like BM25.
- **Strengths**: Excellent for exact matches (SKUs, names, technical terms) and very fast.
- **Weaknesses**: Cannot handle synonyms or semantic meaning.

### 2. Semantic (Vector) Search
- **Mechanism**: Converts data into high-dimensional vectors (embeddings) and finds the nearest neighbors using distance metrics (Cosine Similarity, Euclidean Distance).
- **Strengths**: Understands intent and relationships; finds semantically similar content.
- **Weaknesses**: Can miss exact matches if the embedding model is "fuzzy".

### 3. Graph-Based Search
- **Mechanism**: Traverses relationships in a Knowledge Graph to find connected entities.
- **Strengths**: Captures structural relationships (e.g., "Which drugs treat this specific enzyme?").

## Advanced Search Patterns

### Hybrid Search
Hybrid search combines Lexical and Semantic search into a single pipeline. Results from both are merged using a fusion algorithm like **Reciprocal Rank Fusion (RRF)**.

### Re-ranking (Two-Stage Retrieval)
1. **Retrieval (Stage 1)**: Use a fast but less precise method (like vector search) to pull candidate documents.
2. **Re-ranking (Stage 2)**: Use a more powerful model (a **Cross-Encoder**) to score the relevance of each candidate against the query and pick the top results.

### Query Expansion & Transformation
- **HyDE (Hypothetical Document Embeddings)**: The LLM generates a "fake" answer to the query, and that answer is used to search the vector DB.
- **Multi-Query**: The LLM generates variation of the user's question to capture different perspectives.

## Related tools / concepts
- [RAG Pattern](rag-pattern.md) — broader architecture for retrieval-augmented generation.
- [Vector DB Comparison](../vector-db-comparison.md) — choosing storage for these patterns.
- [Tool Calling & MCP](tool-calling-and-mcp.md) — how agents use search as a tool.
- [Pinecone](../../tools/infrastructure/pinecone.md) — managed vector database.
- [Milvus](../../tools/infrastructure/milvus.md) — high-performance open-source vector store.

## Sources / references
- [Hybrid Search and Reranking - Ubuntu](https://ubuntu.com/blog/hybrid-search-and-reranking-a-deeper-look-at-rag)
- [What is Hybrid Search? - FalkorDB](https://www.falkordb.com/blog/what-is-hybrid-search-in-ai/)
- [Cross-Encoders for Re-ranking - SBERT](https://www.sbert.net/examples/applications/retrieve_rerank/README.html)

## Contribution Metadata
- Last reviewed: 2026-06-06
- Confidence: high
