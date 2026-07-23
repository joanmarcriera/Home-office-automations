# Search Patterns

## What it is
Search patterns in AI represent the architectural strategies used to retrieve relevant information from large datasets to augment Large Language Model (LLM) responses. In late July 2026, this has shifted from simple Retrieval-Augmented Generation (RAG) to **Agentic Search** and **Autonomous Discovery Loops**, where frontier models (such as Claude 5.1, GPT-5.5, Llama 4, Gemma 3, and Qwen 3.6) iteratively refine queries, navigate dynamic knowledge graphs, and negotiate tool endpoints using the latest **Model Context Protocol (MCP 3.1)**.

## What problem it solves
As the volume of unstructured data grows, simple keyword search often fails to capture the underlying meaning or intent of a user's query. Conversely, purely semantic search can miss exact matches for technical terms or product IDs. Modern search patterns solve:
- **Retrieval Quality & Precision**: Combining lexical and semantic methods (hybrid search) with Cross-Encoder re-rankers to ensure high-quality context.
- **Hallucination Mitigation**: Grounding model responses in verified facts rather than internal training parameters.
- **Multimodal Discovery**: Searching across text, images, and video using unified embedding spaces (e.g., [ColQwen](data-copilot-agentic-rag.md)).
- **Real-Time Synthesis**: Synthesizing answers from rapidly changing web data via Agentic Search providers like [Exa AI](../../tools/providers/exa_ai.md).
- **Multi-Agent Coordination**: Routing and executing parallel search queries across federated data stores using MCP 3.1 router architectures.

## Where it fits in the stack
**Category**: Knowledge Base / AI Patterns. These patterns reside in the **Retrieval and Context layer** of an application, sitting between the [Vector Database](../../tools/infrastructure/index.md) and the [Inference Engine](../../tools/infrastructure/index.md).

## Typical use cases
- **Agentic RAG**: Providing a multi-step retrieval loop for an agent to answer complex diagnostic questions.
- **Enterprise Semantic Search**: Building intelligent search engines for corporate wikis that understand domain-specific jargon.
- **Multimodal Product Discovery**: Finding products based on visual similarity or natural language descriptions.
- **Autonomous Research**: Using agents to scour the web and internal docs to generate comprehensive market reports.
- **Federated MCP 3.1 Search**: Dynamically selecting and querying local or cloud databases using MCP 3.1 tools.

## Strengths
- **High Precision and Recall**: Hybrid methods capture both exact matches (via BM25) and semantic intent.
- **Scalability**: Can be applied across billions of documents using efficient vector stores like [Milvus](../../tools/infrastructure/milvus.md) or [Pinecone](../../tools/infrastructure/pinecone.md).
- **Interpretability & Citation**: Provides "citations" or "sources" for LLM outputs, increasing user trust.
- **Dynamic Adaptability**: Pulls from live APIs and databases rather than relying on static training sets.

## Limitations
- **Orchestration Complexity**: Advanced patterns like re-ranking and multi-query expansion add significant architectural overhead.
- **Latency**: Multiple retrieval stages (retrieval -> re-ranking -> synthesis) increase response time.
- **Embedding Mismatch**: Using an embedding model that wasn't trained on your specific domain can lead to poor semantic matches.
- **Operational Cost**: High-frequency embedding generation and re-ranking can increase operational spend.

## When to use it
- When building production-grade RAG applications that require high retrieval accuracy.
- For AI agents that need to navigate complex, fragmented knowledge bases.
- When your data contains both technical terms (requiring lexical precision) and descriptive content (requiring semantic understanding).
- For implementing [Agentic Search](../../tools/providers/exa_ai.md) workflows with frontier models.

## When not to use it
- For very small datasets (< 100 documents) where a simple keyword search or flat file read is faster.
- When the LLM's internal training data is sufficient for the task (e.g., general knowledge questions).
- In extremely low-latency applications where the overhead of a retrieval loop is unacceptable.

## Getting started
1. **Define the Data Source**: Identify whether you are searching internal docs ([MinIO](../../tools/intake_storage/minio.md)), structured databases, or the web.
2. **Select an Embedding Model**: Choose a model compatible with your domain (e.g., OpenAI `text-embedding-3-small` or a local BGE/Ollama model).
3. **Initialize a Vector Store**: Deploy [Milvus](../../tools/infrastructure/milvus.md) or use a managed service like [Pinecone](../../tools/infrastructure/pinecone.md).
4. **Implement a Hybrid Pipeline**: Use a framework like [LlamaIndex](../../tools/frameworks/index.md) or [LangChain](../../tools/frameworks/index.md) to combine BM25 (lexical) and Vector (semantic) search.
5. **Add a Re-ranker**: Integrate a Cross-Encoder (e.g., Cohere Re-rank v3) to prune the final results for the LLM.

## CLI examples
Using the [Ollama](../../services/ollama.md) CLI to generate embeddings for a local document:

```bash
# Generate embeddings for a text snippet using a local model
curl http://localhost:11434/api/embeddings -d '{
  "model": "mxbai-embed-large",
  "prompt": "Llama 4 is a powerful open-source model."
}'
```

Querying an agentic search provider like [Exa AI](../../tools/providers/exa_ai.md) via CLI:
```bash
# Search for recent papers on agentic search patterns using Exa's auto-prompt and neural search
curl -s -X POST "https://api.exa.ai/search" \
     -H "x-api-key: $EXA_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "latest research on hybrid RAG patterns in late July 2026",
       "useAutoprompt": true,
       "numResults": 5,
       "type": "neural"
     }'
```

## API examples
Implementation of a Hybrid Search and Re-ranking query using Python and the Cohere/Pinecone SDKs:

```python
import os
from pinecone import Pinecone
import cohere

# Initialize SOTA July 2026 clients
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
co = cohere.ClientV2(api_key=os.environ["COHERE_API_KEY"])

def hybrid_search_and_rerank(query: str, index_name: str, top_k: int = 10) -> list:
    # 1. Generate Query Embeddings
    embedding_response = co.embed(
        texts=[query],
        model="embed-english-v3.0",
        input_type="search_query"
    )
    query_vector = embedding_response.embeddings[0]

    # 2. Query Pinecone with Hybrid Search (Semantic + Sparse/Lexical)
    index = pc.Index(index_name)
    results = index.query(
        vector=query_vector,
        top_k=top_k * 2,
        include_metadata=True
    )

    # Extract text from matches
    documents = [
        {"id": match.id, "text": match.metadata["text"]}
        for match in results.matches
    ]

    # 3. Apply Cohere Re-rank v3 for high-precision ordering
    rerank_results = co.rerank(
        query=query,
        documents=[doc["text"] for doc in documents],
        top_n=top_k,
        model="rerank-english-v3.0"
    )

    # Reconstruct ranked documents
    ranked_docs = []
    for result in rerank_results.results:
        original_doc = documents[result.index]
        ranked_docs.append({
            "id": original_doc["id"],
            "text": original_doc["text"],
            "score": result.relevance_score
        })

    return ranked_docs
```

## Related tools / concepts
- [RAG Pattern](rag-pattern.md) — The foundational pattern for retrieval-augmented generation.
- [Exa AI](../../tools/providers/exa_ai.md) — Neural search engine for AI agents.
- [Milvus](../../tools/infrastructure/milvus.md) — High-performance open-source vector store.
- [Pinecone](../../tools/infrastructure/pinecone.md) — Managed vector database with native hybrid search.
- [ColBERT / ColQwen](data-copilot-agentic-rag.md) — Advanced late-interaction retrieval models.
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md) — Standard for agents to access search tools.
- [OpenRouter](../../tools/ai_knowledge/openrouter.md) — Used for routing search-related LLM calls.
- [MinIO](../../tools/intake_storage/minio.md) — Storage for raw documents before indexing.

## Sources / References
- [LlamaIndex: Hybrid Search Implementation Guide](https://docs.llamaindex.ai/en/stable/examples/vector_stores/HybridSearch/)
- [Exa AI Documentation: Agentic Search Patterns](https://docs.exa.ai/docs/agentic-search)
- [Pinecone: What is Hybrid Search?](https://www.pinecone.io/learn/hybrid-search/)
- [ColBERT v2: Effective and Efficient Late Interaction](https://arxiv.org/abs/2112.01488)
- [Cohere ClientV2 Re-rank Guide](https://docs.cohere.com/docs/reranking)

## Contribution Metadata
- Last reviewed: 2026-07-25
- Confidence: high