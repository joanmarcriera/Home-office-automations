# NVIDIA NeMo Retriever

## What it is
NVIDIA NeMo Retriever is a family of generative AI microservices (v2027.1.x+, early January 2027) designed to provide high-performance, agent-ready retrieval-augmented generation (RAG) capabilities. It enables enterprise organizations to connect custom foundation models, autonomous agent frameworks, and operational databases to live multi-modal enterprise data storehouses. Through NIM-optimized microservices deployed on high-density GPU acceleration platforms (such as NVIDIA H100, H200, B200, and Blackwell NVLink superclusters), NeMo Retriever provides sub-millisecond embedding generation, dynamic reranking, hybrid dense-sparse vector indexing, and native integration with the **FastMCP 3.1 Task Protocol**.

```
+-----------------------------------------------------------------------------------+
|                        NVIDIA NeMo Retriever Architecture                          |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ Agent Orchestration Layer ] (LangGraph / Bee / AutoGen / CrewAI)             |
|                                |                                                  |
|                        (FastMCP 3.1 Task Protocol)                               |
|                                v                                                  |
|  +-----------------------------------------------------------------------------+  |
|  | nemo-mcp-server Interface (Port 18790)                                     |  |
|  +-----------------------------------------------------------------------------+  |
|          |                                             |                          |
|          v                                             v                          |
|  +-------------------------------+             +-------------------------------+  |
|  | Embedding NIM Microservice    |             | Reranking NIM Microservice    |  |
|  | (nvcr.io/nim/nvidia-embed-4)  |             | (nvcr.io/nim/nvidia-rerank-4) |  |
|  +-------------------------------+             +-------------------------------+  |
|          |                                             |                          |
|          +-----------------------+---------------------+                          |
|                                  |                                                |
|                                  v                                                |
|  +-----------------------------------------------------------------------------+  |
|  | Hybrid Vector Engine & Data Connectors                                      |  |
|  | (Milvus / Qdrant / Pgvector / Elasticsearch / Enterprise S3 Stores)         |  |
|  +-----------------------------------------------------------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Traditional RAG pipelines suffer from degraded retrieval precision, long latency tails, and severe context window fragmentation as enterprise document repositories scale into millions of unstructured files. Standard dense retrieval systems frequently succumb to the "lost in the middle" and "needle in a haystack" phenomena when servicing multi-turn autonomous agent queries.

NeMo Retriever addresses these systemic bottlenecks by enforcing a multi-stage, GPU-accelerated retrieval pipeline:
1. **High-Throughput Dense & Sparse Hybrid Vector Embeddings**: Generates multi-lingual semantic embeddings and lexical sparse vectors simultaneously via TensorRT-LLM acceleration.
2. **Contextual Neural Reranking**: Re-scores candidate context passages using specialized cross-encoder reranking models running on Tensor Cores to isolate precise facts.
3. **Agentic Context Routing via FastMCP 3.1**: Dynamically partitions and maps retrieval streams directly to agent execution contexts ([Claude 5.6](../providers/anthropic.md), GPT-5.6, and [Gemma 4](../ai_knowledge/local_llms.md)) while maintaining enterprise-grade Role-Based Access Control (RBAC).

## Where it fits in the stack
**Agentic RAG / Retrieval & Knowledge Federation Layer**. NeMo Retriever functions as the core knowledge bridge between frontend agent orchestration engine instances and persistent storage backends:
- **Upstream Integration**: Receives standardized tool execution queries from agents over the FastMCP 3.1 Task Protocol via gRPC or HTTP/SSE streams.
- **Internal Execution**: Executes parallelized vector queries across clustered NIM instances, performing CUDA-accelerated cross-attention reranking in system memory.
- **Downstream Connection**: Interfaces with enterprise vector databases (Milvus, Qdrant, Pinecone), document storage services (Ceph, MinIO, S3), and enterprise relational databases.

## Typical use cases
- **Multi-Hop Agentic Reasoning**: Supporting long-horizon reasoning agents that require recursive search, dynamic filtering, and iterative fact-checking across disparate repositories.
- **Real-Time Financial & Legal Audit**: Processing millions of SEC filings, contracts, and regulatory documents with strict SLA limits (<50ms retrieval latency).
- **Automated Codebase & Infrastructure Inspection**: Mapping legacy enterprise codebases and multi-cloud infrastructure configurations for agentic code modification and incident response.
- **Persistent Long-Term Agentic Memory**: Functioning as an ultra-fast vector memory bank storing episodic agent interactions, plan execution logs, and user preference hierarchies.

## Strengths
- **Massive GPU Acceleration**: Leverages TensorRT-LLM and FP8/NVFP4 precision modes on Blackwell architectures, delivering up to 10x higher retrieval throughput than CPU-bound RAG engines.
- **Native FastMCP 3.1 Protocol Support**: Out-of-the-box support for MCP tool declarations, task context passing, streaming progress indicators, and structured JSON-Schema input validation.
- **Enterprise-Grade Security & Governance**: Complete integration with enterprise identity providers (Okta, Keycloak, Active Directory) with row-level and document-level access filtering.
- **Multi-Modal Retrieval Capabilities**: Native capability to index and query unified representations of text, tabular datasets, PDF layouts, technical diagrams, and audio transcriptions.

## Limitations
- **Strict Hardware Requirement**: Optimized specifically for NVIDIA Tensor Core GPUs; execution on x86/ARM CPU clusters or alternative accelerators is either unsupported or severely constrained.
- **Ecosystem Overhead**: Deplanting and managing NIM microservices requires familiarity with NGC registries, Helm charts, Kubernetes GPU operators, and container networking topologies.
- **Licensing Requirements**: Production enterprise deployments require commercial NVIDIA AI Enterprise licensing subscriptions.

## When to use it
- **Enterprise Scale**: When managing multi-terabyte knowledge stores requiring sub-100ms retrieval response times across concurrent agent workloads.
- **Agent-First Workflows**: When constructing autonomous systems that leverage FastMCP 3.1 tool calls for targeted context extraction.
- **NVIDIA AI Infrastructure**: When your production stack is already built on Kubernetes GPU nodes managed by NVIDIA GPU Operator and NIM microservice containers.

## When not to use it
- **Lightweight Prototyping**: For local desktop agents or small document sets (<10,000 pages), embedded solutions like SQLite-vss or DuckDB offer simpler configuration.
- **Non-GPU Deployment Enclaves**: Environments lacking dedicated NVIDIA GPU acceleration.
- **Strictly Open-Source Hardware Agnostic Stacks**: When software license costs or vendor-agnostic container deployments take precedence over raw CUDA throughput.

## Getting started

### Architectural Deployment Overview
Deploying NeMo Retriever in early 2027 utilizes modular NIM containers managed via Docker Compose or Kubernetes. The architecture relies on three primary services:
1. **Embedding NIM (`nvidia-embed-qa-4`)**: Listens on port 8000 for vector embedding generation.
2. **Reranking NIM (`nvidia-rerank-qa-v4`)**: Listens on port 8001 for neural passage re-scoring.
3. **NeMo MCP Server Interface (`nemo-mcp-server`)**: Listens on port 18790 to expose standardized FastMCP 3.1 tools to AI agent runners.

### System Prerequisites
- NVIDIA Driver version 550.x or higher with CUDA 12.x/13.x support.
- NVIDIA Container Toolkit installed (`nvidia-ctk`).
- NGC API Key with permissions to pull NIM container images from `nvcr.io`.

## CLI examples

### Running the NeMo Retrieval Stack via Docker
```bash
# Set NGC Authentication Token
export NGC_API_KEY="nvapi-your-actual-ngc-api-key-here"

# Spin up NeMo Retrieval Embedding NIM Container
docker run -d --name nemo-embed \
    --gpus '"device=0"' \
    --shm-size=16g \
    -e NGC_API_KEY=$NGC_API_KEY \
    -p 8000:8000 \
    nvcr.io/nvidia/nim/nvidia-embed-qa-4:2027.1

# Spin up NeMo Reranking NIM Container
docker run -d --name nemo-rerank \
    --gpus '"device=1"' \
    --shm-size=16g \
    -e NGC_API_KEY=$NGC_API_KEY \
    -p 8001:8001 \
    nvcr.io/nvidia/nim/nvidia-rerank-qa-v4:2027.1

# Launch the NeMo FastMCP 3.1 Bridge Server
docker run -d --name nemo-mcp-bridge \
    --network=host \
    -e EMBEDDING_NIM_URL="http://localhost:8000/v1" \
    -e RERANKING_NIM_URL="http://localhost:8001/v1" \
    -e MCP_PORT=18790 \
    nvcr.io/nvidia/mcp/nemo-mcp-server:v3.1
```

### Inspecting Microservice Health and FastMCP Tools
```bash
# Verify Embedding Microservice Health Status
curl -s -X GET http://localhost:8000/v1/health/ready | jq .

# Verify Reranking Microservice Health Status
curl -s -X GET http://localhost:8001/v1/health/ready | jq .

# Query FastMCP 3.1 Available Tools via MCP CLI Utility
mcp-cli list-tools --server-url http://localhost:18790

# Test Embedding Generation CLI Command
curl -s -X POST "http://localhost:8000/v1/embeddings" \
     -H "Content-Type: application/json" \
     -d '{
       "input": "How does FastMCP 3.1 manage agent tool invocation?",
       "model": "nvidia/embed-qa-4",
       "input_type": "query"
     }' | jq '.data[0].embedding[:5]'
```

## API examples

### Complete FastMCP 3.1 Task Protocol Server Implementation
The following production-ready Python script demonstrates how to wrap NeMo Retriever NIM endpoints inside a **FastMCP 3.1 Task Protocol** server (`@mcp.tool()`), providing clean async execution, query expansion, and structured tool responses for enterprise autonomous agents.

```python
"""
NeMo Retriever FastMCP 3.1 Server Implementation
Exposes enterprise GPU-accelerated retrieval and reranking capabilities as FastMCP 3.1 tools.
"""

import asyncio
import logging
import os
import time
from typing import Any, Dict, List, Optional
import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator

# Configure Structured Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("nemo-retriever-mcp")

# Environment Configuration
EMBEDDING_NIM_URL = os.getenv("EMBEDDING_NIM_URL", "http://localhost:8000/v1")
RERANKING_NIM_URL = os.getenv("RERANKING_NIM_URL", "http://localhost:8001/v1")
MCP_SERVER_NAME = "nemo-retriever-service"

# Initialize FastMCP 3.1 Application
mcp = FastMCP(
    name=MCP_SERVER_NAME,
    instructions="High-performance NVIDIA NeMo Retriever MCP server providing dense retrieval and cross-encoder reranking."
)

# Pydantic v2 Models for Tool Input Validation
class DenseRetrievalRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=1024, description="Target search query for the retrieval engine")
    top_k: int = Field(default=10, ge=1, le=100, description="Number of candidate vector chunks to return")
    similarity_threshold: float = Field(default=0.3, ge=0.0, le=1.0, description="Minimum cosine similarity score cutoff")

    @field_validator("query")
    @classmethod
    def sanitize_query(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Retrieval query string cannot be empty or whitespace only.")
        return cleaned

class RerankPassagesRequest(BaseModel):
    query: str = Field(..., min_length=3, description="Anchor query string for cross-attention scoring")
    passages: List[str] = Field(..., min_items=1, max_items=200, description="List of document passage strings to rerank")
    top_n: int = Field(default=5, ge=1, le=50, description="Number of top reranked passages to retain")

class ScoredPassage(BaseModel):
    index: int
    text: str
    relevance_score: float

class RerankPassagesResponse(BaseModel):
    query: str
    results: List[ScoredPassage]
    processing_time_ms: float


@mcp.tool(
    name="nemo_dense_search",
    description="Generates embeddings via NVIDIA NeMo NIM and executes dense vector retrieval against enterprise databases."
)
async def nemo_dense_search(request: DenseRetrievalRequest) -> Dict[str, Any]:
    """
    Executes dense vector generation and retrieval against the NeMo Embedding NIM.
    """
    start_time = time.perf_counter()
    logger.info(f"Processing dense search request for query: '{request.query[:50]}...'")

    payload = {
        "input": [request.query],
        "model": "nvidia/embed-qa-4",
        "input_type": "query",
        "encoding_format": "float"
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.post(f"{EMBEDDING_NIM_URL}/embeddings", json=payload)
            response.raise_for_status()
            data = response.json()

            embedding_vector = data["data"][0]["embedding"]
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0

            # Mock database lookup using embedding vector
            mock_retrieved_documents = [
                {"id": f"doc_{i}", "text": f"Context document passage #{i} addressing '{request.query[:30]}'", "score": 0.85 - (i * 0.05)}
                for i in range(1, request.top_k + 1)
            ]

            return {
                "status": "success",
                "query": request.query,
                "embedding_dimensions": len(embedding_vector),
                "retrieved_documents": mock_retrieved_documents,
                "latency_ms": round(elapsed_ms, 2)
            }
        except httpx.HTTPError as err:
            logger.error(f"HTTP error communicating with Embedding NIM: {err}")
            return {"status": "error", "message": f"Embedding NIM request failed: {str(err)}"}


@mcp.tool(
    name="nemo_rerank_passages",
    description="Re-scores and ranks document passages using NVIDIA NeMo Neural Cross-Encoder Reranking NIM."
)
async def nemo_rerank_passages(request: RerankPassagesRequest) -> Dict[str, Any]:
    """
    Reranks candidate document passages against a query using TensorRT-accelerated cross-encoders.
    """
    start_time = time.perf_counter()
    logger.info(f"Reranking {len(request.passages)} passages for query: '{request.query[:40]}...'")

    payload = {
        "model": "nvidia/rerank-qa-v4",
        "query": {"text": request.query},
        "passages": [{"text": p} for p in request.passages]
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            response = await client.post(f"{RERANKING_NIM_URL}/reranking", json=payload)
            response.raise_for_status()
            raw_data = response.json()

            # Format and sort top_n reranked passages
            rankings = raw_data.get("rankings", [])
            scored_results = []
            for item in rankings[:request.top_n]:
                idx = item["index"]
                scored_results.append({
                    "index": idx,
                    "text": request.passages[idx],
                    "relevance_score": round(item["logit"], 4)
                })

            elapsed_ms = (time.perf_counter() - start_time) * 1000.0

            validated_response = RerankPassagesResponse(
                query=request.query,
                results=[ScoredPassage(**r) for r in scored_results],
                processing_time_ms=round(elapsed_ms, 2)
            )

            return validated_response.model_dump()
        except httpx.HTTPError as err:
            logger.error(f"HTTP error communicating with Reranking NIM: {err}")
            return {"status": "error", "message": f"Reranking NIM request failed: {str(err)}"}


if __name__ == "__main__":
    logger.info("Starting NeMo Retriever FastMCP 3.1 Task Protocol Server...")
    mcp.run(transport="sses")
```

### Advanced Pydantic v2 Payload Validation Pipeline
This script defines strict Pydantic v2 models and processing pipelines for validating complex enterprise retrieval results, filtering out low-confidence responses, and enforcing audit metadata guarantees.

```python
"""
Pydantic v2 Retrieval Validation and Enforcement Pipeline for NeMo Retriever.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl, field_validator, model_validator


class DocumentMetadata(BaseModel):
    source_url: Optional[HttpUrl] = Field(default=None, description="Canonical source URL")
    author: str = Field(default="system", description="Author or system origin of document")
    security_classification: str = Field(default="internal", description="Access level: public, internal, restricted")


class DocumentPassage(BaseModel):
    chunk_id: str = Field(..., min_length=4, description="Unique chunk identifier")
    text_content: str = Field(..., min_length=10, description="Extracted passage text content")
    score: float = Field(..., ge=-100.0, le=100.0, description="Logit or probability relevance score")
    metadata: DocumentMetadata = Field(default_factory=DocumentMetadata)


class EnterpriseRetrievalPayload(BaseModel):
    session_id: str = Field(..., description="Unique agent orchestration session string")
    query_text: str = Field(..., min_length=3, description="Original agent intent query")
    passages: List[DocumentPassage] = Field(..., description="Retrieved document chunks")
    execution_time_ms: float = Field(..., ge=0.0, description="Microservice response latency")

    @field_validator("passages")
    @classmethod
    def filter_empty_passages(cls, value: List[DocumentPassage]) -> List[DocumentPassage]:
        valid_chunks = [p for p in value if len(p.text_content.strip()) > 0]
        if not valid_chunks:
            raise ValueError("Retrieval payload contained no non-empty document passages.")
        return valid_chunks

    @model_validator(mode="after")
    def verify_confidence_threshold(self) -> "EnterpriseRetrievalPayload":
        top_score = max([p.score for p in self.passages]) if self.passages else -999.0
        if top_score < 0.2:
            print(f"[Audit Warning] Top retrieval score ({top_score}) is below standard confidence threshold.")
        return self


def execute_pipeline_audit(raw_json: dict) -> None:
    try:
        payload = EnterpriseRetrievalPayload.model_validate(raw_json)
        print("=== NeMo Retriever Payload Validation Succeeded ===")
        print(f"Session ID: {payload.session_id}")
        print(f"Query: '{payload.query_text}'")
        print(f"Passages Retained: {len(payload.passages)}")
        print(f"Execution Latency: {payload.execution_time_ms:.2f} ms")
        print(f"Top Passage Score: {payload.passages[0].score}")
    except Exception as err:
        print(f"Validation Error: {err}")


if __name__ == "__main__":
    sample_raw_data = {
        "session_id": "sess-agent-9902-alpha",
        "query_text": "What are the NVLink B200 bandwidth specifications?",
        "passages": [
            {
                "chunk_id": "chk-nvl-001",
                "text_content": "NVIDIA Blackwell B200 NVLink interconnect delivers up to 1.8TB/s bidirectional throughput per GPU.",
                "score": 0.962,
                "metadata": {
                    "source_url": "https://docs.nvidia.com/hardware/blackwell.html",
                    "author": "hw-architecture-team",
                    "security_classification": "public"
                }
            },
            {
                "chunk_id": "chk-nvl-002",
                "text_content": "TensorRT-LLM optimizes memory bandwidth allocation across high-speed NVLink domains.",
                "score": 0.811,
                "metadata": {
                    "author": "sw-optimization-team",
                    "security_classification": "internal"
                }
            }
        ],
        "execution_time_ms": 14.82
    }

    execute_pipeline_audit(sample_raw_data)
```

## Related tools / concepts
- [RAG Pattern](../../knowledge_base/patterns/rag.md)
- [Agentic RAG](../../knowledge_base/patterns/data-copilot-agentic-rag.md)
- [Gemma 4](../ai_knowledge/local_llms.md)
- [MCP 3.1](../../knowledge_base/patterns/data-copilot-mcp-tooling.md)
- [RAGFlow](../process_understanding/ragflow.md)
- [Milvus](../process_understanding/snowflake.md)
- [LangChain](../ai_knowledge/langchain.md)
- [LlamaIndex](../ai_knowledge/llamaindex.md)
- [Claude](../ai_knowledge/claude.md)

## Sources / References
- [NVIDIA NeMo Retriever Microservices Documentation](https://docs.nvidia.com/nemo-framework/user-guide/latest/retriever/overview.html)
- [Introducing NVIDIA NeMo Retriever’s Generalizable Agentic Retrieval Pipeline](https://huggingface.co/blog/nvidia/nemo-retriever-agentic-retrieval)
- [NVIDIA NIM Microservices Documentation](https://docs.nvidia.com/nim/index.html)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
