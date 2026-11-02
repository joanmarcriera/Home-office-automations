# Docling

**Docling** is an open-source document parsing, layout analysis, and structure extraction engine developed by IBM Research. Designed to convert multi-format enterprise documents—including PDFs, DOCX, PPTX, HTML, and raster image files—into high-fidelity structured formats (Markdown, JSON, and Knowledge Graph triples), Docling preserves complex document visual structure, reading order, nested tables, and multi-column layouts.

As of early January 2027 (v2.20.x+), Docling serves as a foundational intake layer for **Retrieval-Augmented Generation (RAG)** pipelines, vector database indexing, and autonomous agent systems powered by **FastMCP 3.1** and frontier models such as **Gemma 4**, **Claude 5.6**, **GPT-5.6**, and **Gemini 4.0 Ultra**.

---

## What it is
Docling is a specialized multi-modal parsing framework that replaces traditional plain-text OCR or naive PDF text extraction with specialized computer vision and layout understanding models (such as **GraniteDocling v2** and LayoutAnalysis models). It parses visual document hierarchies into an intermediate unified document object model (`DoclingDocument`), enabling loss-free conversion into Markdown, JSON, HTML, or graph databases.

```
+-----------------------------------------------------------------------------------+
|                                 INPUT DOCUMENTS                                   |
|               (PDF / DOCX / PPTX / HTML / Scanned Images / Charts)                |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                              DOCLING PARSING ENGINE                               |
|                                                                                   |
|  +--------------------------+  +--------------------------+  +-----------------+  |
|  | Visual Layout Analysis   |  | Table Structure Model    |  | Reading Order   |  |
|  | (GraniteDocling VLM)     |  | (TableFormer / Docling)  |  | Optimization    |  |
|  +--------------------------+  +--------------------------+  +-----------------+  |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                           UNIFIED `DoclingDocument` DOM                           |
+-----------------------------------------------------------------------------------+
                                          |
                +-------------------------+-------------------------+
                |                                                   |
                v                                                   v
+-------------------------------+                   +-------------------------------+
|     STRUCTURED EXPORTS        |                   |    AGENT & RAG INTEGRATION    |
| (Markdown / JSON / Cypher Graph)|                 | (FastMCP 3.1 / Vector DBs)     |
+-------------------------------+                   +-------------------------------+
```

---

## What problem it solves
Legacy text extraction tools (such as naive PDF reader libraries) suffer from severe limitations when processing complex real-world documents:
1. **Loss of Layout and Hierarchy**: Headers, sub-headers, sidebars, and multi-column text blocks are flattened into a single stream of text, destroying reading order.
2. **Table Structural Breakdown**: Multi-line cells, borderless tables, merged headers, and numerical alignment are lost, causing downstream RAG systems to retrieve garbage tabular data.
3. **Visual Context Blindness**: Embedded charts, figures, and diagrams are ignored or converted to raw unlabelled image references.
4. **Format Fragmentation**: Ingestion pipelines historically required separate parsers for Word documents, PowerPoint presentations, web HTML, and PDF files.

Docling provides a unified parsing API that preserves structural semantic context across all supported input formats.

---

## Where it fits in the stack
Docling resides in the **Intake & Process Understanding layer** of the enterprise AI infrastructure.

```
+-----------------------------------------------------------------------+
|                       UNSTRUCTURED INPUT DATA                         |
|             (PDFs, Financial Reports, Slides, Web Pages)              |
+-----------------------------------------------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                    PROCESS & UNDERSTANDING LAYER                      |
|                             (Docling)                                 |
|                                                                       |
|  +-----------------------+  +--------------------+  +--------------+  |
|  | Layout & Table Parser |  | GraniteDocling VLM |  | Object DOM   |  |
|  +-----------------------+  +--------------------+  +--------------+  |
+-----------------------------------------------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                   KNOWLEDGE INGESTION & STORAGE                       |
|           (Vector DBs / Knowledge Graphs / FastMCP 3.1 Tools)         |
+-----------------------------------------------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                      AGENTIC CONSUMPTION LAYER                        |
|            (Claude 5.6 / Gemma 4 / GPT-5.6 / Gemini 4.0)             |
+-----------------------------------------------------------------------+
```

---

## Architectural Mechanics: Granular VLM & Layout Parsing

Docling decouples the extraction pipeline into distinct, modular stage processors that operate over an intermediate document abstraction:

1. **Format Decoupling and PDF Pre-processing**:
   Incoming documents are transformed into raw raster or page-coordinate canvases. For digital PDFs, Docling extracts raw programmatic text runs with precise bounding boxes while isolating raster artifacts for neural OCR. Scanned inputs route directly through an accelerated OCR engine (such as Tesseract or EasyOCR) that generates unified character and word bounding geometry.
2. **Visual Layout Segmentation (GraniteDocling)**:
   A lightweight vision-language backbone segments the canvas into hierarchical regions: Section Headers, Paragraphs, Footnotes, Captions, Floating Figures, and Tabular Grids. Bounding boxes are clustered into reading orders via a topological sorting algorithm that resolves multi-column newspaper layouts and asymmetric callout boxes.
3. **TableFormer Deep Structural Reconstruction**:
   Recognized tabular regions are dispatched to TableFormer, a deep structural attention network. TableFormer predicts logical table topology: row spans, column spans, multi-tier headers, and sparse cells without relying on physical borders. The resulting table model represents both the visual presentation and semantic relational data.
4. **Hierarchical DOM Synthesizer (`DoclingDocument`)**:
   All extracted primitives merge into an in-memory document tree. Nodes maintain bidirectional pointers to their parent sections, child elements, and original physical page bounding coordinates `(x0, y0, x1, y1)`.
5. **Contextual Token Chunking (`HybridChunker`)**:
   Downstream RAG workflows utilize the tree hierarchy to chunk text semantically. Rather than splitting on fixed character windows, `HybridChunker` packs complete semantic nodes while preserving header trails (e.g., `# Q3 Financials > ## Operating Expenses > ### R&D Overhead`) in vector chunk metadata.

---

## Typical use cases
- **Enterprise RAG Document Preparation**: Ingesting financial filings, technical manuals, and medical documentation into vector databases with preserved header-chunk relationships.
- **VLM-Assisted Diagram & Chart Interpretation**: Utilizing GraniteDocling v2 visual-language models to extract quantitative data points directly from embedded charts and figures.
- **Automated Knowledge Graph Generation**: Transforming unstructured PDF libraries directly into property graphs (e.g., Neo4j Cypher triples via `docling-graph`).
- **FastMCP 3.1 Agent Tool Ingestion**: Providing autonomous agents with real-time tool interfaces to read, parse, and summarize uploaded user documents.
- **Contract and Form Extraction**: Converting complex non-standard forms and nested tables into validated, typed **Pydantic v2** models for automated compliance review.

---

## Comparative Assessment: Document Ingestion Frameworks

| Capability / Metric | IBM Docling (v2.20+) | Unstructured.io (v0.16+) | LlamaParse (Cloud) | PyPDF / PDFPlumber |
| :--- | :--- | :--- | :--- | :--- |
| **Execution Topology** | 100% Local / Self-Hosted Docker | Local or Hosted API | Cloud Managed API Only | 100% Local Python Library |
| **Table Structure Reconstruction** | Deep TableFormer (borderless & multi-span) | Heuristic / OCR Bounding Grid | Vision Model (Cloud Prompts) | Coordinate-based Heuristics |
| **VLM Native Acceleration** | GraniteDocling v2 & VLLM integration | LayoutLMv3 / Tesseract OCR | Proprietary LlamaCloud | None (Plain Text Extraction) |
| **Unified Document DOM** | `DoclingDocument` with Bounding Coordinates | List of `Element` dataclasses | Markdown & JSON Tree | Raw strings and dict boxes |
| **Agent Protocol Integration** | Native FastMCP 3.1 Server Tools | REST / Python SDK | Python SDK / LangChain | Custom Scripting Required |
| **Knowledge Graph Export** | Built-in Cypher / Graph Triples | Requires Graphiti Extension | Third-party glue | None |
| **License** | Open Source (MIT) | Source Available / Commercial | Proprietary SaaS | Open Source (MIT / GPL) |

---

## Strengths
- **Superior Table Extraction**: Advanced deep learning model (TableFormer architecture) accurate even on borderless, multi-header, and merged cell tables.
- **Native Vision-Language Model (VLM) Integration**: Native support for IBM GraniteDocling v2 and open VLMs for multimodal visual layout reasoning.
- **Flexible Execution Modes**: Runs 100% locally on CPU/GPU hardware or connects to local inference backends ([vLLM](../infrastructure/vllm.md), [Ollama](../../services/ollama.md)).
- **Unified Object Model**: Exposes a rich Python document object model (`DoclingDocument`) with precise bounding box coordinates, section tags, and element metadata.
- **Extensive Framework Ecosystem**: Native connectors for LangChain, LlamaIndex, FastMCP 3.1, CrewAI, and Haystack.

---

## Limitations
- **Python 3.10+ Environment Constraint**: Python 3.9 and older runtimes are unsupported in post-v2 release streams.
- **Resource Intensity for VLM Processing**: High-fidelity VLM page analysis requires dedicated GPU VRAM (e.g., 8GB+ VRAM for local execution) or multi-core CPU allocations.
- **Complex API for Custom Pipelines**: Deep customization of pipeline stages (e.g., overriding specific OCR engines or layout matchers) requires familiarity with Docling's internal object model.

---

## When to use it
- When document structure, section headers, and tabular integrity are critical to RAG accuracy.
- When building FastMCP 3.1 document parsing tools for AI agents.
- When generating Knowledge Graphs directly from multi-page PDF documents.
- When operating in privacy-sensitive or offline environments requiring local GPU/CPU execution.

---

## When not to use it
- For plain, unstructured text files (e.g., `.txt`, simple logs) where basic string reads suffice.
- In legacy environments constrained to Python 3.9 or lower.
- When ultra-low sub-millisecond document parsing speed is required at the expense of structural accuracy.

---

## FastMCP 3.1 Integration & Pydantic v2 Schema Patterns

Docling can be wrapped as a production FastMCP 3.1 server, offering autonomous agents structured tools to parse and analyze documents on demand with strict Pydantic v2 schemas (`extra="forbid"`, `frozen=True`).

```python
import os
import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
from mcp.server.fastmcp import FastMCP
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.chunking import HybridChunker

logger = logging.getLogger("DoclingFastMCP")
logging.basicConfig(level=logging.INFO)

# Initialize FastMCP 3.1 Server
mcp = FastMCP("Docling-Parsing-Provider", version="3.1.0")

# ------------------------------------------------------------------
# 1. Pydantic v2 Data Validation Schemas (Strict & Frozen)
# ------------------------------------------------------------------
class ParseDocumentInput(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    file_uri: str = Field(..., description="Local absolute path or HTTPS URL of the target document.")
    enable_ocr: bool = Field(default=True, description="Whether to trigger OCR for scanned images.")
    extract_tables: bool = Field(default=True, description="Execute deep TableFormer structural parsing.")
    max_chunk_tokens: int = Field(default=512, ge=64, le=4096, description="Max token limit per semantic chunk.")

    @field_validator("file_uri")
    @classmethod
    def validate_file_uri(cls, v: str) -> str:
        if v.startswith("http://") or v.startswith("https://"):
            return v
        if not os.path.isabs(v) or not os.path.exists(v):
            raise ValueError(f"Target local document path must be an existing absolute path: {v}")
        return v

class TableDataCell(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    row_index: int = Field(..., ge=0)
    col_index: int = Field(..., ge=0)
    text: str = Field(...)

class ExtractedTable(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    table_id: str = Field(..., pattern=r"^tbl_\d+$")
    num_rows: int = Field(..., ge=1)
    num_cols: int = Field(..., ge=0)
    headers: List[str] = Field(default_factory=list)
    grid: List[List[str]] = Field(default_factory=list)

class DocumentChunk(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    chunk_id: int = Field(..., ge=0)
    text: str = Field(...)
    token_count: int = Field(..., ge=1)
    heading_hierarchy: List[str] = Field(default_factory=list)

class ParsedDocumentPayload(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    file_path: str
    page_count: int = Field(..., ge=1)
    elements_extracted: int = Field(..., ge=0)
    tables: List[ExtractedTable]
    chunks: List[DocumentChunk]
    markdown_content: str

# ------------------------------------------------------------------
# 2. FastMCP 3.1 Tool Registration
# ------------------------------------------------------------------
@mcp.tool()
async def parse_document_to_structured_dom(params: ParseDocumentInput) -> str:
    """Parses a local PDF/Office document or URL using Docling and returns typed chunks and tables."""
    try:
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = params.enable_ocr
        pipeline_options.do_table_structure = params.extract_tables

        doc_converter = DocumentConverter(
            format_options={
                "pdf": PdfFormatOption(pipeline_options=pipeline_options)
            }
        )

        conv_result = doc_converter.convert(params.file_uri)
        doc = conv_result.document

        # Extract structured tabular representations
        extracted_tables: List[ExtractedTable] = []
        for idx, table in enumerate(doc.tables):
            header_list = [col.text for col in table.header.cells] if table.header else []
            grid_data = [[cell.text for cell in row.cells] for row in table.body.rows]

            extracted_tables.append(
                ExtractedTable(
                    table_id=f"tbl_{idx + 1}",
                    num_rows=max(len(grid_data), 1),
                    num_cols=len(header_list) if header_list else (len(grid_data[0]) if grid_data else 0),
                    headers=header_list,
                    grid=grid_data
                )
            )

        # Generate semantic chunks preserving heading hierarchy
        chunker = HybridChunker(max_tokens=params.max_chunk_tokens)
        generated_chunks: List[DocumentChunk] = []
        for c_idx, raw_chunk in enumerate(chunker.chunk(doc)):
            headers = []
            if hasattr(raw_chunk, "meta") and raw_chunk.meta and hasattr(raw_chunk.meta, "headings"):
                headers = list(raw_chunk.meta.headings)
            generated_chunks.append(
                DocumentChunk(
                    chunk_id=c_idx,
                    text=raw_chunk.text,
                    token_count=max(len(raw_chunk.text.split()), 1),
                    heading_hierarchy=headers
                )
            )

        payload = ParsedDocumentPayload(
            file_path=params.file_uri,
            page_count=len(doc.pages),
            elements_extracted=len(doc.texts) + len(doc.tables),
            tables=extracted_tables,
            chunks=generated_chunks,
            markdown_content=doc.export_to_markdown()
        )

        return payload.model_dump_json(indent=2)
    except Exception as exc:
        logger.error(f"Failed to parse document: {exc}", exc_info=True)
        return f'{{"error": "{str(exc)}"}}'

if __name__ == "__main__":
    mcp.run()
```

---

## Production Deployment & Operational Topologies

### Docker Compose Sidecar Deployment
For production agent rigs, Docling runs as a dedicated document processing microservice paired with a FastMCP daemon.

```yaml
version: "3.8"

services:
  docling-service:
    image: quay.io/ds4sd/docling:v2.20.0
    container_name: docling-core-engine
    restart: unless-stopped
    environment:
      - OMP_NUM_THREADS=4
      - DOCLING_DEVICE=cuda
      - PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    volumes:
      - /opt/data/documents:/data/documents:ro
      - /opt/cache/huggingface:/root/.cache/huggingface
    ports:
      - "127.0.0.1:8080:8080"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 15s
      timeout: 5s
      retries: 3

  fastmcp-docling-agent:
    build:
      context: .
      dockerfile: Dockerfile.mcp
    container_name: fastmcp-docling-worker
    restart: unless-stopped
    environment:
      - DOCLING_API_ENDPOINT=http://docling-service:8080
      - MCP_PORT=8765
    depends_on:
      docling-service:
        condition: service_healthy
    volumes:
      - /opt/data/documents:/data/documents:ro
    ports:
      - "127.0.0.1:8765:8765"
```

### Systemd Service Configuration
For bare-metal Linux workstations and on-premise compute nodes, run the Docling FastMCP worker under systemd management.

```ini
[Unit]
Description=Docling FastMCP 3.1 Document Ingestion Worker
After=network.target remote-fs.target

[Service]
Type=simple
User=docling-worker
Group=ai-services
WorkingDirectory=/opt/docling-service
Environment="PATH=/opt/docling-service/.venv/bin:/usr/local/cuda/bin:/usr/bin"
Environment="CUDA_VISIBLE_DEVICES=0"
Environment="PYTHONUNBUFFERED=1"
ExecStart=/opt/docling-service/.venv/bin/python -m mcp_docling_server
Restart=always
RestartSec=5s
LimitNOFILE=65536
MemoryMax=16G
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

---

## Diagnostic Troubleshooting Matrix

| Symptom / Error | Root Cause | Immediate Diagnostic Command | Remediation Step |
| :--- | :--- | :--- | :--- |
| `CUDA out of memory` during table parsing | High-resolution PDF rasterization exceeding GPU VRAM during TableFormer attention. | `nvidia-smi --query-gpu=memory.used,memory.free --format=csv` | Set `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` or fallback pipeline option to CPU execution (`pipeline_options.device = "cpu"`). |
| `RuntimeError: Model weights not found in cache` | Sandbox environment blocked from downloading GraniteDocling/TableFormer weights from Hugging Face Hub. | `curl -Is https://huggingface.co \| head -n 5` | Pre-seed `/root/.cache/huggingface/hub` or configure `HF_ENDPOINT` mirror / internal nexus artifactory. |
| Inverted reading order in multi-column research papers | Heading-level bounding boxes overlapping with marginal notes or floating graphics. | Check `doc.texts[n].prov[0].bbox` coordinates in JSON export. | Enable visual layout correction flags: `pipeline_options.do_ocr = True` and adjust reading order sort heuristic to horizontal band priority. |
| Borderless table parsed as plain unformatted text paragraphs | High confidence threshold in TableFormer causing table region rejection. | Inspect `doc.tables` count vs visual page inspection. | Lower table detection threshold or ensure `pipeline_options.do_table_structure = True` is explicitly passed in `PdfFormatOption`. |
| Pydantic validation failure on `file_uri` | Agent passes a relative local file path that fails `validate_file_uri` assertion. | Review FastMCP stderr logs for `ValueError: Target local document path must be an existing absolute path`. | Update agent orchestration prompt to resolve all input document paths via `os.path.abspath()` before invoking tool. |

---

## Getting started

### Installation
Docling requires Python >= 3.10.

```bash
# Install core package
pip install docling pydantic>=2.0 fastmcp>=3.1.0

# Install with Knowledge Graph conversion support
pip install docling-graph
```

### Basic Python Usage
```python
from docling.document_converter import DocumentConverter

source_pdf = "https://arxiv.org/pdf/2408.09869"
converter = DocumentConverter()
result = converter.convert(source_pdf)

# Export parsed document structure directly to Markdown
markdown_text = result.document.export_to_markdown()
print(markdown_text[:500])
```

---

## CLI examples

### Standard Batch Conversions
```bash
# Convert a local PDF file to Markdown
docling report.pdf

# Convert a web document and export as structured JSON
docling https://arxiv.org/pdf/2206.01062 --to json --output ./parsed_output

# Batch process a directory of DOCX and PDF documents
docling ./input_docs/ --to md --output ./markdown_output
```

### Advanced VLM and Graph Processing
```bash
# Force GraniteDocling VLM usage for enhanced visual chart extraction
docling financial_report.pdf --model-id GraniteDocling

# Export document as Cypher graph triples for Neo4j loading (requires docling-graph)
docling-graph convert technical_spec.pdf --output-format cypher --output ./graph_output
```

---

## API examples

### Direct Chunking and RAG Integration
Docling includes built-in hierarchical chunking tools that maintain header-section relationships:

```python
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker

converter = DocumentConverter()
result = converter.convert("complex_document.pdf")

# Apply hybrid chunking that respects document header boundaries
chunker = HybridChunker(max_tokens=512)
chunks = list(chunker.chunk(result.document))

print(f"Generated {len(chunks)} structural chunks.")
print(f"Chunk 1 text: {chunks[0].text}")
print(f"Chunk 1 metadata: {chunks[0].meta}")
```

---

## Related tools / concepts
- [Docling MCP](docling-mcp.md) — Dedicated MCP server implementation for Docling.
- [Unstructured](../intake_storage/unstructured.md) — Alternative document partitioning library.
- [LlamaParse](../intake_storage/llamaparse.md) — Cloud-based document parsing service.
- [Crawl4AI](crawl4ai.md) — Open-source web crawling and scraping library.
- [Firecrawl](firecrawl.md) — Web scraping API optimized for LLMs.
- [vLLM](../infrastructure/vllm.md) — High-performance local inference engine for VLM backends.
- [Pydantic v2](../frameworks/pydantic.md) — Standard schema framework for validating Docling outputs.

---

## Sources / references
- [Docling GitHub Repository](https://github.com/docling-project/docling)
- [Docling Official Documentation](https://docling-project.github.io/docling/)
- [Docling Graph Extension](https://github.com/docling-project/docling-graph)
- [IBM Research: Granite Document Processing](https://research.ibm.com/blog/docling-ibm-granite-document-parsing)

---

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
