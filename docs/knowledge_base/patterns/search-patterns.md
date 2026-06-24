# Search Patterns

## What it is
Search patterns in AI represent the architectural strategies used to retrieve relevant information from large datasets to augment Large Language Model (LLM) responses. In June 2026, this has shifted from simple Retrieval-Augmented Generation (RAG) to **Agentic Search**, where autonomous agents iteratively refine queries and navigate knowledge graphs using the [Model Context Protocol (MCP 3.0)](../../tools/automation_orchestration/mcp.md).

## What problem it solves
As the volume of unstructured data grows, simple keyword search often fails to capture the underlying meaning or intent of a user's query. Conversely, purely semantic search can miss exact matches for technical terms or product IDs. Search patterns provide a framework for:
- **Retrieval Quality**: Combining lexical and semantic methods to ensure high-quality context.
- **Hallucination Mitigation**: Grounding model responses in verified facts rather than internal training data.
- **Multimodal Discovery**: Searching across text, images, and video using unified embedding spaces (e.g., [ColQwen](../../knowledge_base/patterns/data-copilot-agentic-rag.md)).
- **Real-Time Synthesis**: Synthesizing answers from rapidly changing web data via Agentic Search providers like [Exa AI](../../tools/providers/exa_ai.md).

## Where it fits in the stack
**Category**: Knowledge Base / AI Patterns. These patterns reside in the **Retrieval layer** of an application, sitting between the [Vector Database](../../tools/infrastructure/index.md) and the [Inference Engine](../../tools/infrastructure/index.md).

## Typical use cases
- **Agentic RAG**: Providing a multi-step retrieval loop for an agent to answer complex diagnostic questions.
- **Enterprise Semantic Search**: Building intelligent search engines for corporate wikis that understand domain-specific jargon.
- **Multimodal Product Discovery**: Finding products based on visual similarity or natural language descriptions.
- **Autonomous Research**: Using agents to scour the web and internal docs to generate comprehensive market reports.

## Strengths
- **Precision and Recall**: Hybrid methods capture both exact matches and semantic intent.
- **Scalability**: Can be applied across billions of documents using efficient vector stores like [Milvus](../../tools/infrastructure/milvus.md) or [Pinecone](../../tools/infrastructure/pinecone.md).
- **Interpretability**: Provides "citations" or "sources" for LLM outputs, increasing user trust.
- **Dynamism**: Can pull from live APIs and databases rather than static training sets.

## Limitations
- **Orchestration Complexity**: Advanced patterns like re-ranking and multi-query expansion add significant architectural overhead.
- **Latency**: Multiple retrieval stages (retrieval -> re-ranking -> synthesis) increase response time.
- **Embedding Mismatch**: Using an embedding model that wasn't trained on your specific domain can lead to poor semantic matches.
- **Cost**: High-frequency embedding generation and re-ranking can increase operational spend.

## When to use it
- When building production-grade RAG applications that require high retrieval accuracy.
- For AI agents that need to navigate complex, fragmented knowledge bases.
- When your data contains both technical terms (requiring lexical precision) and descriptive content (requiring semantic understanding).
- For implementing [Agentic Search](../../tools/providers/exa_ai.md) workflows.

## When not to use it
- For very small datasets (< 100 documents) where a simple keyword search or flat file read is faster.
- When the LLM's internal training data is sufficient for the task (e.g., general knowledge questions).
- In extremely low-latency applications where the overhead of a retrieval loop is unacceptable.

## Getting started
1. **Define the Data Source**: Identify whether you are searching internal docs ([MinIO](../../tools/intake_storage/minio.md)), structured databases, or the web.
2. **Select an Embedding Model**: Choose a model compatible with your domain (e.g., OpenAI `text-embedding-3-small` or a local BGE model).
3. **Initialize a Vector Store**: Deploy [Milvus](../../tools/infrastructure/milvus.md) or use a managed service like [Pinecone](../../tools/infrastructure/pinecone.md).
4. **Implement a Hybrid Pipeline**: Use a framework like [LlamaIndex](../../tools/frameworks/index.md) or [LangChain](../../tools/frameworks/index.md) to combine BM25 (lexical) and Vector (semantic) search.
5. **Add a Re-ranker**: Integrate a Cross-Encoder (e.g., Cohere Re-rank) to prune the final results for the LLM.

## CLI examples
Using the [Ollama](../../services/ollama.md) CLI to generate embeddings for a local document:

```bash
# Generate embeddings for a text snippet using a local model
curl http://localhost:11434/api/embeddings -d '{
  "model": "mxbai-embed-large",
  "prompt": "Llama 3 is a powerful open-source model."
}'
```

Querying an agentic search provider like [Exa AI](../../tools/providers/exa_ai.md) via CLI (conceptual):
```bash
# Search for recent papers on agentic search patterns
exa search "latest research on hybrid RAG patterns 2026" --use-autoprompt --num-results 5
```

## API examples
Implementation of a Hybrid Search query using [LlamaIndex TS](../../tools/frameworks/llamaindex-ts.md):

```typescript
import { VectorStoreIndex, QueryMode } from "llamaindex";

async function hybridSearch(query: string) {
  const index = await VectorStoreIndex.fromDocuments(documents);
  const retriever = index.asRetriever({
    similarityTopK: 5,
    mode: QueryMode.HYBRID, // Combines vector and keyword search
  });

  const results = await retriever.retrieve(query);
  return results;
}
```

## Related tools / concepts
- [RAG Pattern](rag-pattern.md) — The foundational pattern for retrieval-augmented generation.
- [Exa AI](../../tools/providers/exa_ai.md) — Neural search engine for AI agents.
- [Milvus](../../tools/infrastructure/milvus.md) — High-performance open-source vector store.
- [Pinecone](../../tools/infrastructure/pinecone.md) — Managed vector database with native hybrid search.
- [ColBERT / ColQwen](../../knowledge_base/patterns/data-copilot-agentic-rag.md) — Advanced late-interaction retrieval models.
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md) — Standard for agents to access search tools.
- [OpenRouter](../../tools/ai_knowledge/openrouter.md) — Used for routing search-related LLM calls.
- [MinIO](../../tools/intake_storage/minio.md) — Storage for raw documents before indexing.

## Sources / References
- [LlamaIndex: Hybrid Search Implementation Guide](https://docs.llamaindex.ai/en/stable/examples/vector_stores/HybridSearch/)
- [Exa AI Documentation: Agentic Search Patterns](https://docs.exa.ai/docs/agentic-search)
- [Pinecone: What is Hybrid Search?](https://www.pinecone.io/learn/hybrid-search/)
- [ColBERT v2: Effective and Efficient Late Interaction](https://arxiv.org/abs/2112.01488)

## Contribution Metadata
- Last reviewed: 2026-06-23
- Confidence: high
