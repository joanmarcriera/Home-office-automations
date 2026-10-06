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

## Typical use cases
- **Enterprise RAG Document Preparation**: Ingesting financial filings, technical manuals, and medical documentation into vector databases with preserved header-chunk relationships.
- **VLM-Assisted Diagram & Chart Interpretation**: Utilizing GraniteDocling v2 visual-language models to extract quantitative data points directly from embedded charts and figures.
- **Automated Knowledge Graph Generation**: Transforming unstructured PDF libraries directly into property graphs (e.g., Neo4j Cypher triples via `docling-graph`).
- **FastMCP 3.1 Agent Tool Ingestion**: Providing autonomous agents with real-time tool interfaces to read, parse, and summarize uploaded user documents.
- **Contract and Form Extraction**: Converting complex non-standard forms and nested tables into validated, typed **Pydantic v2** models for automated compliance review.

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

Docling can be wrapped as a FastMCP 3.1 server, offering autonomous agents structured tools to parse and analyze documents on demand.

```python
import os
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator
from mcp.server.fastmcp import FastMCP
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions

# Initialize FastMCP 3.1 Server
mcp = FastMCP("Docling-Parsing-Provider", version="3.1.0")

# ------------------------------------------------------------------
# 1. Pydantic v2 Data Validation Schemas
# ------------------------------------------------------------------
class TableDataCell(BaseModel):
    row_index: int = Field(..., ge=0)
    col_index: int = Field(..., ge=0)
    text: str = Field(...)

class ExtractedTable(BaseModel):
    table_id: str = Field(..., pattern=r"^tbl_\d+$")
    num_rows: int = Field(..., ge=1)
    num_cols: int = Field(..., ge=1)
    headers: List[str]
    grid: List[List[str]]

class ParsedDocumentMetadata(BaseModel):
    file_path: str
    page_count: int = Field(..., ge=1)
    elements_extracted: int = Field(..., ge=0)
    tables: List[ExtractedTable]
    markdown_content: str

    @field_validator("file_path")
    @classmethod
    def validate_file_exists(cls, v: str) -> str:
        if not os.path.exists(v) and not v.startswith("http://") and not v.startswith("https://"):
            raise ValueError(f"Target document path or URL '{v}' is unreachable.")
        return v

# ------------------------------------------------------------------
# 2. FastMCP 3.1 Tool Registration
# ------------------------------------------------------------------
@mcp.tool()
async def parse_document_to_markdown(
    file_uri: str,
    enable_ocr: bool = True,
    extract_tables: bool = True
) -> str:
    """Parses a local PDF/office document or URL using Docling and returns structured metadata & markdown."""
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = enable_ocr
    pipeline_options.do_table_structure = extract_tables

    doc_converter = DocumentConverter(
        format_options={
            "pdf": PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    conv_result = doc_converter.convert(file_uri)
    doc = conv_result.document

    # Build Pydantic v2 output models
    extracted_tables: List[ExtractedTable] = []
    for idx, table in enumerate(doc.tables):
        # Convert table to grid representation
        header_list = [col.text for col in table.header.cells] if table.header else []
        grid_data = [[cell.text for cell in row.cells] for row in table.body.rows]

        extracted_tables.append(
            ExtractedTable(
                table_id=f"tbl_{idx + 1}",
                num_rows=len(grid_data),
                num_cols=len(header_list) if header_list else (len(grid_data[0]) if grid_data else 0),
                headers=header_list,
                grid=grid_data
            )
        )

    parsed_meta = ParsedDocumentMetadata(
        file_path=file_uri,
        page_count=len(doc.pages),
        elements_extracted=len(doc.texts) + len(doc.tables),
        tables=extracted_tables,
        markdown_content=doc.export_to_markdown()
    )

    return parsed_meta.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

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
- [Pydantic v2](../../reference-implementations/metadata-schemas/pydantic-v2.md) — Standard schema framework for validating Docling outputs.

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
