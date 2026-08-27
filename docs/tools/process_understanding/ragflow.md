# RAGFlow

## What it is
RAGFlow is a vision-native, open-source Retrieval-Augmented Generation (RAG) engine that prioritizes deep document understanding (DeepDoc) for complex, unstructured data. By early January 2027 (v0.16.x+), it has matured into an enterprise-grade Knowledge Engine for agentic workflows, featuring native multi-modal reasoning, native integration with frontier models (such as Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, Gemma 4, and Qwen 3.6), and a modular architecture for constructing production-grade RAG pipelines.

## What problem it solves
It eliminates the "garbage in, garbage out" failure mode of traditional RAG systems by using layout-aware parsing (DeepDoc) instead of naive text chunking. It accurately extracts structured information from multi-column PDFs, nested tables, and embedded charts, ensuring that downstream LLM and agentic retrieval is grounded in high-fidelity evidence with precise, pixel-level visual citations.

## Where it fits in the stack
**Knowledge / Inference Layer**. RAGFlow serves as the specialized 'Cognitive Memory' in the agentic stack. It sits between raw data storage (S3, MinIO) and the orchestration layer (n8n, AG2, Flowise), providing a high-confidence context window for frontier models and local inference engines.

## Typical use cases
- **Complex Document Analysis**: Parsing financial statements (10-Ks, 10-Qs) and technical manuals where table structure and image context are critical.
- **Agentic RAG Pipelines**: Providing a high-fidelity knowledge source for agents built on Claude 5.6, Gemma 4, GPT-5.6, Gemini 4.0 Ultra, and DeepSeek-V4.
- **Multi-modal Knowledge Extraction**: Reasoning over diagrams, flowcharts, and handwritten notes in scanned documents using multi-modal LLMs (e.g., Qwen 3.6-VL, Gemma 4 Vision).
- **Enterprise-Grade Grounding**: Building self-hosted search systems with strict citation requirements, hybrid search (dense/sparse), and data sovereignty constraints.

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
# Pull the latest early 2027 production image
docker pull infiniflow/ragflow:v0.16.0-cuda
```

## API examples

### Python SDK: Agentic Document Intake with Strict Pydantic v2 Validation
This example showcases document uploading, dataset state management, and visual citation extraction parsed under strict Pydantic v2 schema enforcement.

```python
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

# 1. Define strict Pydantic v2 schemas for RAGFlow dataset and document configurations
class DatasetConfig(BaseModel):
    dataset_name: str = Field(..., max_length=100, description="Unique name of the collection")
    parsing_template: str = Field("General", description="DeepDoc layout parser template (e.g., Law, Book, Manual)")
    top_k: int = Field(5, ge=1, le=100)

class VisualCitation(BaseModel):
    page_number: int = Field(..., ge=1)
    bbox: List[float] = Field(..., min_length=4, max_length=4, description="Bounding box [x0, y0, x1, y1]")
    confidence: float = Field(..., ge=0.0, le=1.0)

class IngestedDocument(BaseModel):
    doc_id: str = Field(..., pattern=r"^doc_[a-f0-9]{32}$")
    filename: str
    status: str = Field("pending", pattern=r"^(pending|parsing|completed|failed)$")
    citations: Optional[List[VisualCitation]] = None

    @field_validator("citations")
    @classmethod
    def check_citations_presence_if_completed(cls, v: Optional[List[VisualCitation]], info) -> Optional[List[VisualCitation]]:
        # Ensure completed state carries citations
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
        print(f"Visual Grounding Citations: {len(validated_doc.citations or [])}")
```

### FastMCP 3.1 Integration (Agentic Context)
RAGFlow exposes knowledge bases via Model Context Protocol (MCP 3.1 / FastMCP 3.1), allowing agents to query the document store directly. Configure your MCP host configuration as follows:
```json
{
  "mcpServers": {
    "ragflow": {
      "command": "npx",
      "args": ["@ragflow/mcp-server", "--base-url", "http://ragflow:9337", "--api-key", "rf-key"]
    }
  }
}
```

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
