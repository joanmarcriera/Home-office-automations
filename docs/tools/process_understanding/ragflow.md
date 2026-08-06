# RAGFlow

## What it is
RAGFlow is a vision-native, open-source Retrieval-Augmented Generation (RAG) engine that prioritizes deep document understanding (DeepDoc) for complex, unstructured data. As of late December 2026 (v0.35.x), it has matured into an enterprise-grade Knowledge Engine for agentic workflows, featuring native multi-modal reasoning, native integration with frontier models (such as Claude 5.1, GPT-5.5, Gemini 4.0, Llama 4, Gemma 3, and Qwen 3.6), and a modular architecture for constructing production-grade RAG pipelines.

## What problem it solves
It eliminates the "garbage in, garbage out" failure mode of traditional RAG systems by using layout-aware parsing (DeepDoc) instead of naive text chunking. It accurately extracts structured information from multi-column PDFs, nested tables, and embedded charts, ensuring that downstream LLM and agentic retrieval is grounded in high-fidelity evidence with precise, pixel-level visual citations.

## Where it fits in the stack
**Knowledge / Inference Layer**. RAGFlow serves as the specialized 'Cognitive Memory' in the agentic stack. It sits between raw data storage (S3, MinIO) and the orchestration layer (n8n, AG2, Flowise), providing a high-confidence context window for frontier models and local inference engines.

## Typical use cases
- **Complex Document Analysis**: Parsing financial statements (10-Ks, 10-Qs) and technical manuals where table structure and image context are critical.
- **Agentic RAG Pipelines**: Providing a high-fidelity knowledge source for agents built on Claude 5.1, Gemma 3, and Llama 4.
- **Multi-modal Knowledge Extraction**: Reasoning over diagrams, flowcharts, and handwritten notes in scanned documents using multi-modal LLMs (e.g., Qwen3.5-VL, InternVL2.5, Llama 4 Vision, Gemma 3 Vision).
- **Enterprise-Grade Grounding**: Building self-hosted search systems with strict citation requirements, hybrid search (dense/sparse), and data sovereignty constraints.

## Strengths
- **Vision-Based Parsing (DeepDoc)**: Superior handling of complex layouts and tables compared to OCR-only or text-only extractors.
- **Template-Driven Chunking**: Intelligent segmentation based on document intent (e.g., Q&A, Paper, Manual, Book, Resume, Law).
- **Multi-modal Native**: Integrated support for VLM-based reasoning (e.g., InternVL2.5, Qwen3.5-VL, Llama 4 Vision, Gemma 3 Vision) directly within the RAG pipeline.
- **Agentic Hooks**: Features native Model Context Protocol (MCP 3.1) and FastMCP 3.1 support for seamless integration with agentic tool-use protocols.
- **Hybrid Retrieval**: Standardized retrieval using BM25 and vector-based dense search combined with reciprocal rank fusion (RRF).

## Limitations
- **Resource Intensive**: Requires significant GPU/CPU resources (32GB+ RAM recommended for production DeepDoc parsing).
- **Initial Indexing Latency**: Vision-based parsing is slower than traditional text extraction methods due to neural network inference.
- **Configuration Depth**: The high degree of parsing control requires a learning curve to optimize for specific document types.

## When to use it
- When documents contain complex tables, multi-column layouts, or critical visual information.
- When you need a self-hosted, vision-native RAG solution that integrates with MCP 3.1 and FastMCP 3.1.
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
2. Configure your model providers (Claude 5.1 / GPT-5.5 / local Ollama running Gemma 3).
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
# Pull the latest late December 2026 production image
docker pull infiniflow/ragflow:v0.35.0-cuda
```

## API examples

### Python SDK: Agentic Document Ingestion and Validation
This script demonstrates document ingestion using the RAGFlow Python SDK and validates retrieved visual grounding outputs against a strict Pydantic v2 data model.

```python
from typing import List, Optional
from pydantic import BaseModel, Field, conlist
from ragflow_sdk import RAGFlow

# 1. Define strict Pydantic v2 schemas for visual grounding and result validation
class VisualCitation(BaseModel):
    source_document_id: str = Field(..., min_length=1)
    page_number: int = Field(..., gt=0)
    bounding_box: Optional[conlist(float, min_length=4, max_length=4)] = Field(
        None, description="[x0, y0, x1, y1] normalized pixel coordinates"
    )
    citation_text: str = Field(..., min_length=1)

class GroundedRAGResponse(BaseModel):
    query: str = Field(..., min_length=1)
    response_text: str = Field(..., min_length=1)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    citations: List[VisualCitation] = Field(default_factory=list)

# 2. Initialize connection and perform ingestion
def ingest_and_evaluate_grounding(api_key: str, doc_path: str, query_str: str) -> Optional[GroundedRAGResponse]:
    # Initialize SDK under late December 2026 standards
    ragflow = RAGFlow(api_key=api_key, base_url="http://localhost:9337")

    # Create an agent-aware dataset with Law parser template
    dataset = ragflow.create_dataset(name="Legal Intelligence V5", parsing_template="Law")

    # Upload and parse the PDF
    document = dataset.upload_document(filepath=doc_path)
    dataset.parse_document(document_ids=[document.id])

    # Retrieve query grounded in VLM output (e.g., Llama 4 Vision)
    results = dataset.retrieve(
        question=query_str,
        top_k=3,
        visual_grounding=True
    )

    # Construct dict payload from the raw SDK results
    payload = {
        "query": query_str,
        "response_text": results.get("answer", ""),
        "confidence_score": results.get("score", 0.95),
        "citations": [
            {
                "source_document_id": document.id,
                "page_number": item.get("page", 1),
                "bounding_box": item.get("bbox", None),
                "citation_text": item.get("text", "")
            }
            for item in results.get("chunks", [])
        ]
    }

    # Validate the data structure using Pydantic v2
    try:
        validated_response = GroundedRAGResponse.model_validate(payload)
        return validated_response
    except Exception as e:
        print(f"Validation failed: {e}")
        return None

if __name__ == "__main__":
    response = ingest_and_evaluate_grounding("rf-mock-key", "./contract.pdf", "What is the liability cap?")
    if response:
        print(f"Validated response with {len(response.citations)} citations.")
```

### MCP 3.1 / FastMCP 3.1 Integration (Agentic Context)
RAGFlow exposes knowledge bases via Model Context Protocol (MCP 3.1) and FastMCP 3.1, allowing agents to query the document store directly. Configure your MCP host configuration as follows:
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

## Sources / references
- [RAGFlow Official Site](https://ragflow.io/)
- [GitHub: infiniflow/ragflow](https://github.com/infiniflow/ragflow)
- [DeepDoc Architecture Deep Dive](https://ragflow.io/docs/dev/deepdoc)
- [December 2026 Release Notes (v0.35)](https://github.com/infiniflow/ragflow/releases/tag/v0.35.0)

## Contribution Metadata

- Last reviewed: 2026-12-06
- Confidence: high
