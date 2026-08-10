# Search Patterns

## What it is
Search patterns in AI represent the architectural strategies used to retrieve relevant information from large datasets to augment Large Language Model (LLM) responses. In late November/December 2026, this has shifted from basic Retrieval-Augmented Generation (RAG) to **Agentic Search** and **Autonomous Discovery Loops**, where frontier models (such as Claude 5.1, GPT-5.5, Gemini 4.0 Pro, Llama 4, Gemma 3, and Qwen 3.6) iteratively refine queries, navigate dynamic knowledge graphs, and negotiate tool endpoints using the latest **Model Context Protocol (FastMCP 3.1)** features.

## What problem it solves
As the volume of unstructured data grows, simple keyword search often fails to capture the underlying meaning or intent of a user's query. Conversely, purely semantic search can miss exact matches for technical terms or product IDs. Modern search patterns solve:
- **Retrieval Quality & Precision**: Combining lexical and semantic methods (hybrid search) with Cross-Encoder re-rankers to ensure high-quality context.
- **Hallucination Mitigation**: Grounding model responses in verified facts rather than internal training parameters.
- **Multimodal Discovery**: Searching across text, images, and video using unified embedding spaces (e.g., [ColQwen](data-copilot-agentic-rag.md)).
- **Real-Time Synthesis**: Synthesizing answers from rapidly changing web data via Agentic Search providers like [Exa AI](../../tools/providers/exa_ai.md).
- **Multi-Agent Coordination**: Routing and executing parallel search queries across federated data stores using FastMCP 3.1 router architectures.

## Where it fits in the stack
**Category**: Knowledge Base / AI Patterns. These patterns reside in the **Retrieval and Context layer** of an application, sitting between the [Vector Database](../../tools/infrastructure/index.md) and the [Inference Engine](../../tools/infrastructure/index.md).

## Typical use cases
- **Agentic RAG**: Providing a multi-step retrieval loop for an agent to answer complex diagnostic questions.
- **Enterprise Semantic Search**: Building intelligent search engines for corporate wikis that understand domain-specific jargon.
- **Multimodal Product Discovery**: Finding products based on visual similarity or natural language descriptions.
- **Autonomous Research**: Using agents to scour the web and internal docs to generate comprehensive market reports.
- **Federated FastMCP 3.1 Search**: Dynamically selecting and querying local or cloud databases using MCP 3.1 tools.

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
       "query": "latest research on hybrid RAG patterns in late November 2026",
       "useAutoprompt": true,
       "numResults": 5,
       "type": "neural"
     }'
```

## API examples
The following Python example implements a validated neural search workflow using **Pydantic v2** (`BaseModel`, `Field`, `model_validate`, `ValidationError`) to strictly validate query parameters and search responses.

### Python: Validated Neural Search Pipeline (Pydantic v2)
```python
import os
from typing import List
from pydantic import BaseModel, Field, ValidationError, field_validator

# Pydantic v2 Schema for a robust Search Request
class NeuralSearchQuery(BaseModel):
    query: str = Field(..., min_length=2, max_length=500, description="The user or system search query")
    top_k: int = Field(default=5, ge=1, le=100, description="Number of results to retrieve")
    hybrid_ratio: float = Field(default=0.5, ge=0.0, le=1.0, description="Balance between keyword (0.0) and vector (1.0) search")

    @field_validator("query")
    @classmethod
    def strip_and_verify_query(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Search query cannot be empty or solely whitespace.")
        return cleaned

# Pydantic v2 Schema for a Search Result
class SearchResultDocument(BaseModel):
    document_id: str = Field(..., description="Unique ID of the matched document")
    content: str = Field(..., description="Text content chunk of the document")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Similarity score or normalized cross-encoder rank score")

class RankedSearchResponse(BaseModel):
    query: str
    results: List[SearchResultDocument]

def execute_validated_search(request_payload: dict) -> dict:
    """
    Validates query payload, executes a mock neural/hybrid search,
    and returns a strictly validated response payload.
    """
    try:
        # 1. Validate incoming search parameters with Pydantic v2
        search_params = NeuralSearchQuery.model_validate(request_payload)
    except ValidationError as ve:
        raise ValueError(f"Invalid search request arguments: {ve}")

    print(f"Executing SOTA search for '{search_params.query}' (top_k={search_params.top_k}, ratio={search_params.hybrid_ratio})")

    # 2. Simulate search execution (e.g. querying Pinecone + Cohere Re-rank)
    simulated_raw_results = [
        {
            "document_id": "doc-091",
            "content": "Claude 5.1 and GPT-5.5 offer outstanding native tooling capabilities for agent workflows in late 2026.",
            "relevance_score": 0.985
        },
        {
            "document_id": "doc-042",
            "content": "Model Context Protocol (FastMCP 3.1) simplifies client and server discovery across distributed nodes.",
            "relevance_score": 0.892
        }
    ]

    # Trim results to requested top_k
    trimmed_results = simulated_raw_results[:search_params.top_k]

    # 3. Formulate and validate output response schema
    response_payload = {
        "query": search_params.query,
        "results": trimmed_results
    }

    try:
        validated_response = RankedSearchResponse.model_validate(response_payload)
    except ValidationError as ve:
        raise ValueError(f"Search engine returned corrupted schemas: {ve}")

    return validated_response.model_dump()

if __name__ == "__main__":
    # Sample input query parameters
    payload = {
        "query": "  What are the SOTA agent standards in late November 2026? ",
        "top_k": 2,
        "hybrid_ratio": 0.75
    }

    try:
        result = execute_validated_search(payload)
        print("Search completed with full type safety:")
        for r in result["results"]:
            print(f"[{r['document_id']}] Score: {r['relevance_score']:.3f} | {r['content']}")
    except Exception as e:
        print(f"Error during search execution: {e}")
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

## Sources / references
- [LlamaIndex: Hybrid Search Implementation Guide](https://docs.llamaindex.ai/en/stable/examples/vector_stores/HybridSearch/)
- [Exa AI Documentation: Agentic Search Patterns](https://docs.exa.ai/docs/agentic-search)
- [Pinecone: What is Hybrid Search?](https://www.pinecone.io/learn/hybrid-search/)
- [ColBERT v2: Effective and Efficient Late Interaction](https://arxiv.org/abs/2112.01488)
- [Cohere ClientV2 Re-rank Guide](https://docs.cohere.com/docs/reranking)

## Contribution Metadata
- Last reviewed: 2026-12-31
- Confidence: high
