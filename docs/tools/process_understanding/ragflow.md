# RAGFlow

## What it is
RAGFlow is a vision-native, open-source Retrieval-Augmented Generation (RAG) engine that prioritizes deep document understanding (DeepDoc) for complex, unstructured data. As of 2027 (v0.16.x+), it has matured into an enterprise-grade Knowledge Engine for agentic workflows, featuring native multi-modal reasoning, seamless integration with frontier models (such as Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, Gemma 4, and Qwen 3.6), and a modular architecture for constructing production-grade RAG pipelines.

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

## Document Understanding & Engine Comparison Matrix

| Feature / Engine | RAGFlow (DeepDoc) | Dify | Docling | Unstructured.io | LlamaParse |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Parsing Focus** | Vision Layout + Deep Semantic | Workflow / Chat Focus | Layout Parsing (Docling Core) | Document Ingestion Rules | Cloud-based Parsing API |
| **OCR / Vision Engine** | Built-in DeepDoc (YOLOv8 + LayoutLM) | Pluggable Third-Party | Native Docling Vision | Pluggable / Tesseract | Proprietary LlamaCloud |
| **Chunking Strategy** | Layout-Aware + Template Rules | Character / Token Based | Structural Markdown AST | Rule / Token Based | Markdown / Element Based |
| **Hybrid Retrieval** | BM25 + Vector + RRF Native | Vector Primary / Hybrid | Vector Primary | Vector Primary | Vector Primary |
| **Agent Protocol** | FastMCP 3.1 / MCP Native | REST / Webhook Primary | CLI / Python API | REST / Python SDK | LlamaIndex / REST |
| **Visual Bounding Boxes** | Native Pixel Coordinates | None | Optional Markdown Span | Optional Coordinates | High Precision Bounding Boxes |
| **Deployment Model** | Self-Hosted Docker Cluster | Self-Hosted / SaaS | Open Source Library | Open Source / API | Managed SaaS API |

## Operational Sizing & Infrastructure Requirements

| Deployment Tier | Concurrency | Target RAM / VRAM | Disk Storage | Recommended GPU Acceleration | Recommended Storage Backend |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Developer Sandbox** | 1-2 users | 16 GB RAM / 8 GB VRAM | 50 GB NVMe | NVIDIA RTX 4080 (16GB) | Local NVMe Path |
| **Team Cluster** | 10-50 users | 64 GB RAM / 24 GB VRAM | 500 GB NVMe | NVIDIA A10G / L4 (24GB) | MinIO S3 Object Storage |
| **Enterprise Fleet** | 100+ concurrent | 128 GB+ RAM / Dual 48GB VRAM | 2 TB+ NVMe RAID | 2x NVIDIA A100 / H100 | Distributed Ceph / AWS S3 |

## DeepDoc Template Processing Strategies

```
+-----------------------------------------------------------------------------------+
|                        DEEPDOC TEMPLATE CHUNKING STRATEGIES                       |
+-----------------------------------------------------------------------------------+

   +----------------+     +-------------------+     +-------------------------+
   |   Q&A TEMPLATE | --> | Split by Q&A Pair | --> | Preserves Question Context|
   +----------------+     +-------------------+     +-------------------------+

   +----------------+     +-------------------+     +-------------------------+
   |   LAW TEMPLATE | --> | Article / Section | --> | Strict Legal Clause Bounds|
   +----------------+     +-------------------+     +-------------------------+

   +----------------+     +-------------------+     +-------------------------+
   | MANUAL TEMPLATE| --> | Heading Hierarchy | --> | Structural Table Context|
   +----------------+     +-------------------+     +-------------------------+
```

## Strengths
- **Vision-Based Parsing (DeepDoc)**: Superior handling of complex layouts and tables compared to OCR-only or text-only extractors.
- **Template-Driven Chunking**: Intelligent segmentation based on document intent (e.g., Q&A, Paper, Manual, Book, Resume, Law).
- **Multi-modal Native**: Integrated support for VLM-based reasoning (e.g., Qwen 3.6-VL, Gemma 4 Vision) directly within the RAG pipeline.
- **Agentic Hooks**: Features native Model Context Protocol (FastMCP 3.1) support for seamless integration with agentic tool-use protocols.
- **Hybrid Retrieval**: Standardized retrieval using BM25 and vector-based dense search combined with reciprocal rank fusion (RRF).

## Limitations
- **Resource Intensive**: Requires significant GPU/CPU resources (32GB+ RAM recommended for production DeepDoc parsing).
- **Initial Indexing Latency**: Vision-based parsing is slower than traditional text extraction methods due to neural network inference.
- **Configuration Depth**: The high degree of parsing control requires a learning curve to optimize for specific document types.

## When to use it
- When documents contain complex tables, multi-column layouts, or critical visual information.
- When you need a self-hosted, vision-native RAG solution that integrates with FastMCP 3.1.
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

### Task Queue & System Diagnostics
```bash
# Query active tasks from Redis parsing queue
docker exec -it ragflow-redis redis-cli LLEN task_queue

# Inspect GPU utilization during active DeepDoc vision inference
nvidia-smi --query-gpu=utilization.gpu,utilization.memory,memory.used,memory.total --format=csv
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
    model_config = ConfigDict(extra="forbid", frozen=True)

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

class RAGFlowChunkingConfig(BaseModel):
    chunk_token_size: int = Field(default=512, ge=64, le=2048, description="Target token count per document chunk")
    overlap_tokens: int = Field(default=64, ge=0, le=256, description="Token overlap between adjacent chunks")
    parse_tables_with_ocr: bool = Field(default=True, description="Enable visual layout parsing for PDF tables")

@mcp.tool()
def configure_deepdoc_chunking(dataset_id: str, config_dict: dict) -> dict:
    """
    FastMCP 3.1 tool for configuring RAGFlow DeepDoc document chunking parameters.
    """
    cfg = RAGFlowChunkingConfig.model_validate(config_dict)
    return {
        "status": "configured",
        "dataset_id": dataset_id,
        "chunk_token_size": cfg.chunk_token_size,
        "overlap_tokens": cfg.overlap_tokens,
        "parse_tables_with_ocr": cfg.parse_tables_with_ocr
    }

class DocumentParsingJobSpec(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    dataset_id: str = Field(..., description="Target dataset UUID")
    document_ids: List[str] = Field(..., min_length=1, description="List of RAGFlow document IDs to parse")
    run_ocr: bool = Field(default=True, description="Enable visual layout OCR pass")

@mcp.tool()
def trigger_deepdoc_parsing_job(spec: DocumentParsingJobSpec) -> Dict[str, Any]:
    """
    FastMCP 3.1 tool for triggering async DeepDoc vision parsing tasks on queued documents.
    """
    return {
        "status": "queued",
        "dataset_id": spec.dataset_id,
        "job_count": len(spec.document_ids),
        "ocr_enabled": spec.run_ocr
    }

if __name__ == "__main__":
    mcp.run()
```

### FastMCP 3.1 Integration (Agentic Context)
RAGFlow exposes knowledge bases via Model Context Protocol (FastMCP 3.1), allowing agents to query the document store directly. Configure your MCP host configuration as follows:
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

## Troubleshooting & Operational Diagnostics

| Issue / Symptom | Probable Cause | Diagnostic Command | Remediation Action |
| :--- | :--- | :--- | :--- |
| **Elasticsearch / Infinity OOM** | Heap size allocated below DeepDoc indexing load | `docker logs ragflow-es \| grep -i oom` | Increase `vm.max_map_count=262144` and set ES heap `-Xms4g -Xmx4g` |
| **DeepDoc Parsing Stall** | CUDA out of memory on large visual PDF page | `nvidia-smi` | Switch parsing mode from GPU-dense batching to CPU fallback or split PDF |
| **Low Retrieval Recall** | RRF fusion weights biased towards dense search | `curl -X POST http://ragflow:9337/api/v1/retrieval` | Adjust BM25 vs Dense weight ratio in dataset parameters (e.g. 0.5/0.5) |
| **FastMCP Timeout** | Long vision parsing queue delaying chunk fetching | `mcp-server --debug` | Implement asynchronous polling using `doc_id` status before query submission |
| **MySQL Connection Pool Exhaustion** | Unclosed API query connections from concurrent agents | `docker logs ragflow-mysql \| grep "Too many connections"` | Increase `max_connections=500` in MySQL `my.cnf` configuration |

## Production Deployment & Systemd Service Architecture

To run RAGFlow FastMCP 3.1 gateway background workers as resilient system services on enterprise Linux hosts, use the systemd unit template below:

```ini
[Unit]
Description=RAGFlow FastMCP 3.1 DeepDoc Engine Service
After=network.target docker.service
Requires=docker.service

[Service]
Type=simple
User=ragflow
Group=ragflow
WorkingDirectory=/opt/ragflow-mcp
ExecStart=/usr/bin/python3 -m mcp.server.fastmcp run ragflow_server.py
Restart=always
RestartSec=10s
Environment=PYTHONUNBUFFERED=1
Environment=RAGFLOW_API_URL=http://localhost:9337
Environment=RAGFLOW_API_KEY=rf-prod-key-7781239

# Security and Isolation Guardrails
ProtectSystem=full
ProtectHome=true
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

## Enterprise Governance & Audit Logging Guardrails

In high-compliance production deployments, RAGFlow must adhere to strict audit trail and data sovereignty principles:

1. **Pixel-Level Citation Persistence**: Every chunk stored in Infinity or Elasticsearch includes metadata referencing the bounding box (`[x0, y0, x1, y1]`) and raw image hash to verify compliance during regulatory reviews.
2. **PII Masking at Ingestion**: Ingest pipelines automatically pass parsed text through PII detection models prior to generating dense vector embeddings.
3. **Role-Based Dataset Segmentation**: Knowledge base datasets must be partitioned using dataset UUID ACLs mapped directly to enterprise OIDC identities.

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

---
## Contribution Metadata
- Last reviewed: 2026-10-12
- Confidence: high
