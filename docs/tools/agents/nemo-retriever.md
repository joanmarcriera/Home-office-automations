# NVIDIA NeMo Retriever

## What it is
NVIDIA NeMo Retriever is a family of generative AI microservices (v2026.11.x+) designed to provide high-performance, agent-ready retrieval-augmented generation (RAG) capabilities. It enables organizations to connect their custom models to live enterprise data and deliver highly accurate, context-aware responses through optimized inference microservices (NIM).

## What problem it solves
Traditional RAG pipelines often struggle with retrieval accuracy and latency as data scales. NeMo Retriever provides a generalized agentic retrieval pipeline that moves beyond simple semantic similarity to include more complex reasoning and multi-step retrieval strategies. It specifically addresses the "lost in the middle" and "needle in a haystack" problems for large context models like [Claude 5.1](../providers/anthropic.md), GPT-5.5, and [Gemma 3](../ai_knowledge/local_llms.md).

## Where it fits in the stack
**Agentic RAG / Retrieval Layer**. It sits between the agent orchestration layer (e.g., LangGraph, Bee) and the enterprise data sources, providing optimized embedding, reranking, and retrieval services via the **MCP 3.1 Task Protocol**.

## Typical use cases
- **Agentic Search**: Implementing complex multi-step search strategies for autonomous agents.
- **Enterprise RAG**: Connecting LLMs to massive corporate knowledge bases with high precision.
- **Real-time Data Access**: Providing agents with up-to-date information from structured and unstructured sources.
- **Agentic Memory**: Serving as a persistent, high-performance memory store for long-running agent sessions.

## Strengths
- **Agentic Retrieval**: Specifically designed for agent-based workflows with complex retrieval needs and **MCP 3.1 Task Protocol** support.
- **High Performance**: Optimized for NVIDIA H100/B200 and Blackwell-class GPUs to minimize RAG latency.
- **Enterprise Grade**: Designed for scale, security, and reliability in production environments with native RBAC.
- **Integration**: Native support for the `nemo-mcp-server` allowing seamless context delivery to frontier models.

## Limitations
- **Hardware Dependent**: Requires NVIDIA GPUs for optimal performance (NIM-optimized).
- **Setup Complexity**: Requires familiarity with the NVIDIA AI Enterprise stack and NGC container registry.
- **Cost**: Commercial licensing for NVIDIA AI Enterprise can be significant for smaller teams.

## When to use it
- **Enterprise-Scale RAG**: When you need to scale retrieval to millions of documents with sub-second latency.
- **Agentic Workflows**: If your agents require complex, multi-step retrieval strategies that go beyond simple vector search.
- **NVIDIA Ecosystem**: When you are already using NVIDIA GPUs and NIM for model serving.
- **MCP 3.1 Integration**: When you need a standardized protocol for connecting retrieval tools to agents via the **MCP 3.1 Task Protocol**.

## When not to use it
- **Small-Scale Projects**: For simple RAG with a few documents, a basic ChromaDB or SQLite setup is easier.
- **CPU-Only Environments**: It is heavily optimized for GPU; running it on CPU-only hardware is not efficient.
- **Budget Constrained**: If commercial licensing fees are a barrier, consider open-source alternatives like RAGFlow or Milvus.

## Getting started
NeMo Retriever is deployed via NVIDIA NIM. In late November 2026, the standard deployment involves the `nemo-mcp-server` for agentic integration.

### Minimal Concepts
1. **Embeddings**: Microservices for generating high-fidelity vector representations.
2. **Reranking**: Models that refine retrieval results based on relevance to the specific agentic intent.
3. **MCP Server**: The interface through which agents ([Claude 5.1](../providers/anthropic.md)/GPT-5.5/[Gemma 3](../ai_knowledge/local_llms.md)) request and receive context.

## CLI examples
```bash
# Pull and run the NeMo Retriever Embedding NIM
docker run --rm --runtime=nvidia -e NGC_API_KEY=$NGC_API_KEY \
    -p 8000:8000 \
    nvcr.io/nvidia/nim/nvidia-embed-qa-4:latest

# Check the health of the retriever service
curl -X 'GET' 'http://localhost:8000/v1/health' -H 'accept: application/json'

# List tools available via the NeMo MCP server
mcp-cli list-tools --server-url http://localhost:18790
```

## API examples

### Example: Calling the NeMo Retriever Reranking API
```python
import requests

# Example of calling the NeMo Retriever Reranking API
def rerank_results(query, documents, model="nvidia/rerank-qa-v4"):
    url = "http://localhost:8001/v1/reranking"
    payload = {
        "query": query,
        "documents": documents,
        "model": model
    }
    response = requests.post(url, json=payload)
    return response.json()
```

### Example: Pydantic v2 Schema for Query and Rerank Validation
This example provides a formal Python mechanism using **Pydantic v2** to validate inputs and response payloads for NeMo Retriever operations, ensuring data integrity across agent boundaries.

```python
import sys
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

# Define Pydantic v2 models for retriever orchestration
class NeMoRetrievalQuery(BaseModel):
    query: str = Field(..., min_length=3, description="Semantic search query from the agent")
    top_k: int = Field(default=5, ge=1, le=50, description="Number of documents to retrieve")
    min_score: float = Field(default=0.0, ge=-10.0, le=10.0, description="Minimum relevance score threshold")

class DocumentChunk(BaseModel):
    id: str = Field(..., description="Unique chunk identifier")
    text: str = Field(..., description="Textual context content")
    score: float = Field(..., description="Relevance score computed by the reranker")

class NeMoRetrievalResult(BaseModel):
    query: str
    documents: List[DocumentChunk]
    latency_ms: float = Field(..., description="Retrieval latency in milliseconds")

    @field_validator('documents')
    @classmethod
    def verify_results_exist(cls, v: List[DocumentChunk]) -> List[DocumentChunk]:
        # Log empty retrieval events
        if len(v) == 0:
            print("Warning: NeMo Retriever returned 0 documents for current query context.", file=sys.stderr)
        return v

def process_agent_retrieval(raw_response: dict) -> Optional[NeMoRetrievalResult]:
    try:
        validated_result = NeMoRetrievalResult.model_validate(raw_response)
        print(f"Validated retrieval results for query: '{validated_result.query}'")
        print(f"Top Document Score: {validated_result.documents[0].score if validated_result.documents else 'N/A'}")
        return validated_result
    except Exception as e:
        print(f"NeMo Retriever response parsing failed: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    print("Initializing NeMo Retriever payload validator...")
    # Mock data representing a typical response payload from the microservice
    mock_payload = {
        "query": "GPU cluster orchestration with FastMCP 3.1",
        "documents": [
            {"id": "doc_001", "text": "FastMCP 3.1 introduces optimized multi-threading...", "score": 0.945},
            {"id": "doc_002", "text": "NVIDIA Blackwell-class systems maximize RAG routing...", "score": 0.812}
        ],
        "latency_ms": 12.4
    }

    result = process_agent_retrieval(mock_payload)
    if result:
        print("Success: Retrieval session data parsed and validated using Pydantic v2.")
```

## Related tools / concepts
- [RAG Pattern](../../knowledge_base/patterns/rag.md)
- [Agentic RAG](../../knowledge_base/patterns/data-copilot-agentic-rag.md)
- [Gemma 3](../ai_knowledge/local_llms.md)
- [MCP 3.1](../../knowledge_base/patterns/data-copilot-mcp-tooling.md)
- [RAGFlow](../process_understanding/ragflow.md)
- [Milvus](../process_understanding/snowflake.md) (Integrated via NeMo)
- [LangChain](../ai_knowledge/langchain.md)
- [LlamaIndex](../ai_knowledge/llamaindex.md)
- [Claude](../ai_knowledge/claude.md)

## Sources / References
- [NVIDIA NeMo Retriever Documentation](https://docs.nvidia.com/nemo-framework/user-guide/latest/retriever/overview.html)
- [Introducing NVIDIA NeMo Retriever’s Generalizable Agentic Retrieval Pipeline](https://huggingface.co/blog/nvidia/nemo-retriever-agentic-retrieval)

## Contribution Metadata
- Last reviewed: 2026-11-27
- Confidence: high
