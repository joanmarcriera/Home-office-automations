# Search Patterns

## What it is
Search patterns in AI represent the architectural strategies used to retrieve relevant information from large datasets to augment Large Language Model (LLM) responses. In late December 2026, this has shifted from simple Retrieval-Augmented Generation (RAG) to **Agentic Search** and **Autonomous Discovery Loops**, where frontier models (such as Claude 5.1, GPT-5.5, Llama 4, Gemma 3, and Qwen 3.6) iteratively refine queries, navigate dynamic knowledge graphs, and negotiate tool endpoints using the latest **Model Context Protocol (MCP 3.1)** / FastMCP 3.1. Late-Interaction embeddings (such as ColBERT and ColQwen) are widely used to maintain token-level alignment and superior retrieval accuracy.

## What problem it solves
As the volume of unstructured data grows, simple keyword search often fails to capture the underlying meaning or intent of a user's query. Conversely, purely semantic search can miss exact matches for technical terms or product IDs. Modern search patterns solve:
- **Retrieval Quality & Precision**: Combining lexical and semantic methods (hybrid search) with Cross-Encoder re-rankers to ensure high-quality context.
- **Token-Level Matching**: Using late-interaction mechanisms (e.g. ColQwen, ColBERT) to align query and document tokens, ensuring technical jargon is retrieved accurately.
- **Hallucination Mitigation**: Grounding model responses in verified facts rather than internal training parameters.
- **Multimodal Discovery**: Searching across text, images, and video using unified embedding spaces.
- **Real-Time Synthesis**: Synthesizing answers from rapidly changing web data via Agentic Search providers like [Exa AI](../../tools/providers/exa_ai.md).
- **Multi-Agent Coordination**: Routing and executing parallel search queries across federated data stores using MCP 3.1 / FastMCP 3.1 router architectures.

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
       "query": "latest research on hybrid RAG patterns in late December 2026",
       "useAutoprompt": true,
       "numResults": 5,
       "type": "neural"
     }'
```

## API examples
Implementation of a Hybrid Search and Re-ranking query using Python and the Cohere/Pinecone SDKs. The response is validated strictly using **Pydantic v2** models to ensure reliability in downstream multi-agent chains.

### Python: Hybrid Search and Re-ranking Pipeline with strict Pydantic v2 typing
```python
import os
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError
from pinecone import Pinecone
import cohere

# ---------------------------------------------------------------------------
# Strict Validation Schemas using Pydantic v2
# ---------------------------------------------------------------------------

class SearchQueryInput(BaseModel):
    query: str = Field(..., min_length=3, max_length=500, description="The natural language query string")
    index_name: str = Field(..., description="The target vector database index name")
    top_k: int = Field(default=5, ge=1, le=100, description="Number of re-ranked documents to return")

    @field_validator("query")
    @classmethod
    def clean_query_text(cls, v: str) -> str:
        # Strip trailing whitespaces and sanitize input text
        return v.strip()

class RankedDocument(BaseModel):
    id: str = Field(..., description="Unique document hash or identifier")
    text: str = Field(..., description="The raw document snippet text")
    score: float = Field(..., description="Relevance score computed by Cohere Re-rank v3")
    metadata: Optional[dict] = Field(default_factory=dict)

# ---------------------------------------------------------------------------
# Search Pipeline Function
# ---------------------------------------------------------------------------

# Initialize clients (ensure API keys are injected)
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY", "mock-key"))
co = cohere.ClientV2(api_key=os.environ.get("COHERE_API_KEY", "mock-key"))

def hybrid_search_and_rerank(raw_input: dict) -> List[dict]:
    """
    Executes a high-precision hybrid retrieval and Cohere Re-rank v3 pipeline,
    validated strictly with Pydantic v2 models.
    """
    try:
        # Validate inputs strictly using Pydantic v2
        validated_input = SearchQueryInput.model_validate(raw_input)
    except ValidationError as err:
        raise ValueError(f"Invalid search parameters: {err}")

    # 1. Generate Query Embeddings
    embedding_response = co.embed(
        texts=[validated_input.query],
        model="embed-english-v3.0",
        input_type="search_query"
    )
    query_vector = embedding_response.embeddings[0]

    # 2. Query Pinecone with Hybrid Search (Semantic + Sparse/Lexical)
    index = pc.Index(validated_input.index_name)
    results = index.query(
        vector=query_vector,
        top_k=validated_input.top_k * 2,
        include_metadata=True
    )

    # Extract text from matches
    documents = []
    for match in results.matches:
        doc_text = match.metadata.get("text", "") if match.metadata else ""
        documents.append({"id": match.id, "text": doc_text, "meta": match.metadata or {}})

    if not documents:
        return []

    # 3. Apply Cohere Re-rank v3 for high-precision ordering
    rerank_results = co.rerank(
        query=validated_input.query,
        documents=[doc["text"] for doc in documents],
        top_n=validated_input.top_k,
        model="rerank-english-v3.0"
    )

    # Reconstruct ranked documents and validate output schemas
    ranked_docs = []
    for result in rerank_results.results:
        original_doc = documents[result.index]
        try:
            doc_obj = RankedDocument(
                id=original_doc["id"],
                text=original_doc["text"],
                score=result.relevance_score,
                metadata=original_doc["meta"]
            )
            ranked_docs.append(doc_obj.model_dump())
        except ValidationError as err:
            # Log and skip single malformed record to keep retrieval fault-tolerant
            print(f"Skipping malformed retrieval record: {err}")
            continue

    return ranked_docs


if __name__ == "__main__":
    # Sample execution (late 2026 search parameters)
    raw_params = {
        "query": "  How does FastMCP 3.1 simplify tool-calling transport mechanisms?  ",
        "index_name": "homelab-docs-index",
        "top_k": 3
    }
    try:
        results = hybrid_search_and_rerank(raw_params)
        print(f"Retrieved and Re-ranked {len(results)} docs:")
        for doc in results:
            print(f"[{doc['score']:.4f}] Doc ID: {doc['id']} - Snippet: {doc['text'][:50]}...")
    except Exception as e:
        print(f"Search retrieval pipeline execution failed: {e}")
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
- Last reviewed: 2026-12-31
- Confidence: high
