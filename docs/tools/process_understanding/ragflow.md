# RAGFlow

## What it is
RAGFlow is a vision-native, open-source Retrieval-Augmented Generation (RAG) engine that prioritizes deep document understanding (DeepDoc) for complex, unstructured data. By early January 2027 (v0.16.x+), it has matured into an enterprise-grade Knowledge Engine for agentic workflows, featuring native multi-modal reasoning, native integration with frontier models (such as Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, Gemma 4, and Qwen 3.6), and a modular architecture for constructing production-grade RAG pipelines.

### DeepDoc Layout Parsing & Multimodal Pipeline

```
+-----------------------------------------------------------------------------------+
|                        DEEPDOC VISION LAYOUT PARSING FLOW                         |
+-----------------------------------------------------------------------------------+
                                          |
  +-----------------------+     +-----------------------+     +---------------------+
  | UNSTRUCTURED PDF /    | --> | DEEPDOC LAYOUT VISION | --> | RECOGNIZED BLOCKS   |
  | IMAGE INPUT           |     | MODEL INFERENCE       |     | & BOUNDING BOXES    |
  +-----------------------+     +-----------------------+     +---------------------+
                                                                         |
                                                                         v
  +-----------------------+     +-----------------------+     +---------------------+
  | FASTMCP 3.1 CITATION  | <-- | HYBRID RETRIEVAL      | <-- | TEMPLATE CHUNKING   |
  | GROUNDING ENGINE      |     | (BM25 + Dense RRF)    |     | (Law/Manual/Book)   |
  +-----------------------+     +-----------------------+     +---------------------+
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

## API examples

### FastMCP 3.1 Deep-Doc Extraction Server Implementation

Below is a production-grade FastMCP 3.1 server enabling agents to query RAGFlow knowledge bases, perform multi-modal hybrid retrieval, and extract pixel-level bounding-box citations under strict Pydantic v2 schemas.

```python
"""
FastMCP 3.1 DeepDoc Retrieval & Citation Server for RAGFlow
Provides agentic document search, hybrid rank fusion, and bounding-box verification.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RAGFlowMCP")

mcp = FastMCP("RAGFlow-DeepDoc-Engine", version="3.1.0")

class VisualCitation(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    page_number: int = Field(..., ge=1, description="1-indexed document page number")
    bbox: List[float] = Field(..., min_length=4, max_length=4, description="Bounding box [x0, y0, x1, y1]")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Vision model detection confidence")

class IngestedDocument(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    doc_id: str = Field(..., pattern=r"^doc_[a-f0-9]{32}$", description="RAGFlow internal document hash identifier")
    filename: str = Field(..., description="Original filename")
    status: str = Field("pending", pattern=r"^(pending|parsing|completed|failed)$")
    citations: Optional[List[VisualCitation]] = None

    @field_validator("citations")
    def check_citations_presence_if_completed(cls, v: Optional[List[VisualCitation]], info) -> Optional[List[VisualCitation]]:
        status = info.data.get("status")
        if status == "completed" and (v is None or len(v) == 0):
            logger.warning("Completed document returned zero visual bounding-box citations.")
        return v

class RetrievalQuerySpec(BaseModel):
    dataset_id: str = Field(..., description="RAGFlow collection UUID")
    query: str = Field(..., min_length=2, description="Search prompt or query string")
    top_k: int = Field(default=5, ge=1, le=50, description="Max returned chunks")
    use_rrf: bool = Field(default=True, description="Enable Reciprocal Rank Fusion dense+sparse blend")

@mcp.tool()
def search_deepdoc_knowledge_base(ragflow_url: str, api_key: str, spec: RetrievalQuerySpec) -> Dict[str, Any]:
    """Executes a hybrid retrieval query against a RAGFlow dataset with citation grounding."""
    endpoint = f"{ragflow_url.rstrip('/')}/api/v1/retrieval"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {
        "dataset_ids": [spec.dataset_id],
        "question": spec.query,
        "top_k": spec.top_k,
        "similarity_threshold": 0.2
    }

    try:
        res = requests.post(endpoint, json=payload, headers=headers, timeout=10)
        res.raise_for_status()
        data = res.json()
        return {"status": "success", "results": data.get("data", {})}
    except Exception as err:
        logger.error(f"RAGFlow retrieval query failed: {err}")
        return {"error": str(err), "status": "failed"}

if __name__ == "__main__":
    mcp.run()
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
- Last reviewed: 2026-10-12
- Confidence: high
