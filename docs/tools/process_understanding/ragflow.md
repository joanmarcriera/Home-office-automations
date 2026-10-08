# RAGFlow

## What it is
RAGFlow is a vision-native, open-source Retrieval-Augmented Generation (RAG) engine that prioritizes deep document understanding (DeepDoc) for complex, unstructured data. By early January 2027 (v0.16.x+), it has matured into an enterprise-grade Knowledge Engine for agentic workflows, featuring native multi-modal reasoning, native integration with frontier models (such as Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, Gemma 4, and Qwen 3.6), and a modular architecture for constructing production-grade RAG pipelines.

## Architecture & System Overview
RAGFlow utilizes a modular, microservice-based architecture to process raw unstructured files into high-fidelity knowledge graph structures and hybrid vector/sparse indices.

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             RAGFLOW ENGINE ARCHITECTURE                           │
└──────────────────────────────────────────────────────────────────────────────────┘

   Raw Sources             DeepDoc Vision Ingestion                Indexing & Storage
 ┌─────────────┐       ┌─────────────────────────────┐         ┌────────────────────────┐
 │ - PDF Files │──────>│ - Layout Recognition (YOLO) │────────>│ - Infinity / ES (Dense)│
 │ - 10-K / Qs │       │ - Table Parsing (TableTransformer)   │ - BM25 Sparse Index   │
 │ - Images    │       │ - OCR & Formula Extraction  │         │ - MinIO (Visual BBoxes)│
 └─────────────┘       └─────────────────────────────┘         └────────────────────────┘
                                      │                                    │
                                      ▼                                    ▼
                         ┌──────────────────────────┐           ┌──────────────────────┐
                         │ Chunking & Semantic Graphs│           │ Multi-Modal Retrieval│
                         │ - QA / Resume / Manual   │           │ - RRF Fusion         │
                         │ - Visual Citation BBoxes │           │ - Reranking (BGE-M3) │
                         └──────────────────────────┘           └──────────────────────┘
                                                                           │
                                                                           ▼
                                                               ┌───────────────────────┐
                                                               │  Agentic FastMCP 3.1  │
                                                               │ - MCP Client Context  │
                                                               └───────────────────────┘
```

## What problem it solves
It eliminates the "garbage in, garbage out" failure mode of traditional RAG systems by using layout-aware parsing (DeepDoc) instead of naive text chunking. It accurately extracts structured information from multi-column PDFs, nested tables, and embedded charts, ensuring that downstream LLM and agentic retrieval is grounded in high-fidelity evidence with precise, pixel-level visual citations.

## Where it fits in the stack
**Knowledge / Inference Layer**. RAGFlow serves as the specialized 'Cognitive Memory' in the agentic stack. It sits between raw data storage (S3, MinIO) and the orchestration layer (n8n, AG2, Flowise), providing a high-confidence context window for frontier models and local inference engines.

## Typical use cases
- **Complex Document Analysis**: Parsing financial statements (10-Ks, 10-Qs) and technical manuals where table structure and image context are critical.
- **Agentic RAG Pipelines**: Providing a high-fidelity knowledge source for agents built on Claude 5.6, Gemma 4, GPT-5.6, Gemini 4.0 Ultra, and DeepSeek-V4.
- **Multi-modal Knowledge Extraction**: Reasoning over diagrams, flowcharts, and handwritten notes in scanned documents using multi-modal LLMs (e.g., Qwen 3.6-VL, Gemma 4 Vision).
- **Enterprise-Grade Grounding**: Building self-hosted search systems with strict citation requirements, hybrid search (dense/sparse), and data sovereignty constraints.

## Comparison Matrix

| Feature | RAGFlow | Docling | Unstructured | LlamaParse |
| :--- | :--- | :--- | :--- | :--- |
| **Parsing Engine** | Vision-native DeepDoc | Docling Technical Layout | Multi-modal Partitioners | Cloud LLM Vision Parser |
| **Deployment Model** | Self-hosted Docker / K8s | Local Python / Rust CLI | Self-hosted API / Cloud | Managed SaaS API |
| **Visual Citations** | Pixel-level BBoxes | Segment-level BBoxes | Page-level Annotations | Page-level Citations |
| **Agentic Protocol** | FastMCP 3.1 Native | Custom Python Bindings | REST / LangChain Hook | LlamaIndex Native |
| **Hybrid Retrieval** | BM25 + Vector + RRF | External Vector DB needed| External Vector DB needed| Built-in Cloud Index |

## Strengths
- **Vision-Based Parsing (DeepDoc)**: Superior handling of complex layouts and tables compared to OCR-only or text-only extractors.
- **Template-Driven Chunking**: Intelligent segmentation based on document intent (e.g., Q&A, Paper, Manual, Book, Resume, Law).
- **Multi-modal Native**: Integrated support for VLM-based reasoning (e.g., Qwen 3.6-VL, Gemma 4 Vision) directly within the RAG pipeline.
- **Agentic Hooks**: Features native Model Context Protocol (MCP 3.1 / FastMCP 3.1) support for seamless integration with agentic tool-use protocols.
- **Hybrid Retrieval**: Standardized retrieval using BM25 and vector-based dense search combined with reciprocal rank fusion (RRF).

## Limitations
- **Resource Intensive**: Requires significant GPU/CPU resources (32GB+ RAM recommended for production DeepDoc parsing).
- **Initial Indexing Latency**: Vision-based parsing is slower than traditional text extraction methods due to neural network inference.
- **Configuration Depth**: The high degree of parsing control requires a learning curve to optimize for specific document types.

## When to use it
- When documents contain complex tables, multi-column layouts, or critical visual information.
- When you need a self-hosted, vision-native RAG solution that integrates with MCP 3.1 / FastMCP 3.1.
- When high-confidence citations and grounding are the primary system requirements.

## When not to use it
- For simple, structured text data (JSON, CSV) where a basic vector database or Postgres (pgvector) is sufficient.
- In low-latency scenarios where indexing speed is prioritized over parsing fidelity.
- On hardware with less than 16GB of RAM or no access to specialized inference engines.

## Getting started

### Installation (Docker Compose)
RAGFlow recommends a multi-container deployment for its cognitive services (Elasticsearch/Infinity, Redis, MySQL, MinIO).

```bash
# Clone the repository
git clone https://github.com/infiniflow/ragflow.git
cd ragflow/docker

# Increase system map count (required for Elasticsearch)
sudo sysctl -w vm.max_map_count=262144

# Start the cluster with GPU support
docker compose -f docker-compose.yml up -d
```

### Basic Workflow
1. Access the UI at `http://localhost:80`.
2. Configure your model providers (Claude 5.6 / GPT-5.6 / local Ollama running Gemma 4).
3. Create a 'Knowledge Base' and select the 'DeepDoc' parser template.
4. Upload documents and monitor the parsing queue in the 'Files' tab.

## CLI examples

### Health and Log Monitoring
```bash
# Check status of RAGFlow cognitive services
docker compose ps

# Follow parsing server logs
docker logs -f ragflow-server

# Verify Infinity/Elasticsearch connectivity
docker exec -it ragflow-server curl -X GET "http://ragflow-es:9200/_cluster/health?pretty"
```

### Image Management
```bash
# Pull the latest production image
docker pull infiniflow/ragflow:v0.16.0-cuda
```

## API examples

### Python SDK: Agentic Document Intake with Strict Pydantic v2 Validation
This example showcases document uploading, dataset state management, and visual citation extraction parsed under strict Pydantic v2 schema enforcement.

```python
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict

# 1. Define strict Pydantic v2 schemas for RAGFlow dataset and document configurations
class DatasetConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    dataset_name: str = Field(..., max_length=100, description="Unique name of the collection")
    parsing_template: str = Field("General", description="DeepDoc layout parser template (e.g., Law, Book, Manual)")
    top_k: int = Field(5, ge=1, le=100)
    similarity_threshold: float = Field(0.2, ge=0.0, le=1.0)
    vector_similarity_weight: float = Field(0.7, ge=0.0, le=1.0)

class VisualCitation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page_number: int = Field(..., ge=1)
    bbox: List[float] = Field(..., min_length=4, max_length=4, description="Bounding box [x0, y0, x1, y1]")
    confidence: float = Field(..., ge=0.0, le=1.0)

class IngestedDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")

    doc_id: str = Field(..., pattern=r"^doc_[a-f0-9]{32}$")
    filename: str
    status: str = Field("pending", pattern=r"^(pending|parsing|completed|failed)$")
    chunk_count: int = Field(0, ge=0)
    citations: Optional[List[VisualCitation]] = None

    @field_validator("citations")
    @classmethod
    def check_citations_presence_if_completed(cls, v: Optional[List[VisualCitation]], info) -> Optional[List[VisualCitation]]:
        status = info.data.get("status")
        if status == "completed" and (v is None or len(v) == 0):
            print("[Warning] Completed document lacks any bounding-box citations.")
        return v

# 2. Strict run simulation
def process_ragflow_document(raw_doc_response: dict) -> Optional[IngestedDocument]:
    try:
        doc = IngestedDocument.model_validate(raw_doc_response)
        return doc
    except Exception as e:
        print(f"RAGFlow schema validation error: {e}")
        return None

if __name__ == "__main__":
    sample_response = {
        "doc_id": "doc_a1b2c3d4e5f607182930313233343536",
        "filename": "quarterly_financial_report_q1_2027.pdf",
        "status": "completed",
        "chunk_count": 42,
        "citations": [
            {
                "page_number": 12,
                "bbox": [54.0, 120.5, 450.2, 380.1],
                "confidence": 0.985
            }
        ]
    }

    validated_doc = process_ragflow_document(sample_response)
    if validated_doc:
        print(f"Validated Document: {validated_doc.filename}")
        print(f"Extraction Status: {validated_doc.status.upper()}")
        print(f"Chunks Produced: {validated_doc.chunk_count}")
        print(f"Visual Grounding Citations: {len(validated_doc.citations or [])}")
```

### FastMCP 3.1 Integration Code Pattern
RAGFlow exposes knowledge bases via FastMCP 3.1, enabling agentic tool use and semantic search over indexed DeepDoc knowledge bases.

```python
import httpx
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "ragflow-search-server",
    instructions="Provides hybrid vector and layout-aware search capabilities via RAGFlow."
)

class RAGFlowQueryInput(BaseModel):
    dataset_ids: List[str] = Field(..., description="List of RAGFlow dataset IDs to search across.")
    query: str = Field(..., description="Natural language search query.")
    top_k: int = Field(5, ge=1, le=50, description="Number of relevant chunks to retrieve.")

@mcp.tool()
async def ragflow_hybrid_search(input_data: RAGFlowQueryInput) -> List[Dict[str, Any]]:
    """Executes a hybrid dense/sparse vector search using RAGFlow engine."""
    ragflow_url = "http://ragflow:9337/api/v1/retrieval"
    headers = {"Authorization": "Bearer rf-key-production-2027"}

    payload = {
        "dataset_ids": input_data.dataset_ids,
        "question": input_data.query,
        "top_k": input_data.top_k,
        "similarity_threshold": 0.2
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(ragflow_url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        results = []
        for chunk in data.get("data", {}).get("chunks", []):
            results.append({
                "content": chunk.get("content_with_weight"),
                "document_name": chunk.get("doc_name"),
                "similarity": chunk.get("similarity"),
                "page_number": chunk.get("page_number")
            })
        return results

if __name__ == "__main__":
    mcp.run()
```

## Operational Best Practices & Troubleshooting
- **Memory Allocation**: Always allocate a minimum of 32GB RAM to the Docker host when processing scanned high-DPI PDFs to prevent Out-Of-Memory (OOM) worker restarts.
- **DeepDoc Parsing Queue**: Set worker thread concurrency according to available VRAM. A single NVIDIA RTX 4090 or A10G can support 4 parallel DeepDoc layout recognition workers.
- **Vector DB Storage Tuning**: For datasets exceeding 1,000,000 document chunks, configure Infinity or Elasticsearch with dedicated SSD NVMe storage and set `vm.max_map_count=262144`.

## Related tools / concepts
- [Dify](../ai_knowledge/dify.md)
- [Docling](./docling.md)
- [OCRmyPDF](./ocrmypdf.md)
- [Unstructured](../intake_storage/unstructured.md)
- [LlamaParse](../intake_storage/llamaparse.md)
- [Firecrawl](./firecrawl.md)
- [AG2](../frameworks/ag2.md)
- [Flowise](../ai_knowledge/flowise.md)
- [Agentic RAG](../../knowledge_base/patterns/data-copilot-agentic-rag.md)
- [KnowledgeOps](../../architecture/multi_agent_knowledgeops.md)
- [Crawl4AI](./crawl4ai.md)
- [OvisOCR2](./ovisocr2.md)
- [Tesseract](./tesseract.md)
- [Ragas](./ragas.md)

## Sources / References
- [RAGFlow Official Site](https://ragflow.io/)
- [GitHub: infiniflow/ragflow](https://github.com/infiniflow/ragflow)
- [DeepDoc Architecture Deep Dive](https://ragflow.io/docs/dev/deepdoc)
- [RAGFlow Latest Release Notes](https://github.com/infiniflow/ragflow/releases)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
