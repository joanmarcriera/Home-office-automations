# Docling MCP

## What it is
Docling MCP is a high-performance document processing service that implements the FastMCP 3.1 / Model Context Protocol (MCP) specification to expose advanced layout-aware parsing, document conversion, and structured data extraction tools to autonomous AI agents. Built on IBM's Docling core conversion library, Docling MCP functions as a standardized document conversion gateway for AI models like **Claude 5.1**, **GPT-5.5 / GPT-5.6**, and **Gemini 4.0 Pro**.

In early 2027, Docling MCP solves one of the most persistent bottlenecks in enterprise KnowledgeOps: ingesting multi-format enterprise files (PDF, DOCX, PPTX, HTML, XLSX) into RAG pipelines and context windows without corrupting multi-column reading order, losing table headers, or dropping embedded diagrams and formulas.

## What problem it solves
Standard text extraction libraries (such as simple PDF text strippers or naive OCR scripts) frequently scramble multi-column layouts, merge floating sidebars into body paragraphs, misalign complex financial tables, and fail on inline mathematical equations.

Docling MCP addresses these problems through:
- **Vision-Aware Layout Parsing**: Employs deep learning computer vision models to detect visual reading order, section headers, sidebars, header/footer elements, and embedded figures.
- **High-Fidelity Markdown & JSON Structuring**: Converts unstructured binary formats directly into semantically pristine Markdown strings or structured JSON abstract syntax trees (ASTs).
- **FastMCP 3.1 Protocol Standardization**: Exposes document parsing capabilities via standardized MCP tools (`convert_document`, `batch_convert`, `extract_tables`), enabling instant zero-config integration with Claude Desktop, Claude Code, Zed, and custom agentic orchestrators.
- **Relational Table Reconstruction**: Identifies cell spans, column spans, and borderless tabular boundaries to reconstruct clean Markdown tables or pandas-compatible JSON structures.

## System Architecture

```
                                    Docling FastMCP Processing Pipeline

  +-----------------------+        +------------------------+        +--------------------------+
  |  Raw Enterprise Docs  | ---->  |  FastMCP 3.1 Gateway   | ---->  |  Layout Detection Engine |
  | (PDF, DOCX, PPTX, HTML|        |  Tool Execution Server |        |  (Vision Model & OCR)    |
  +-----------------------+        +------------------------+        +--------------------------+
                                                                                  |
                                                                                  v
  +-----------------------+        +------------------------+        +--------------------------+
  | Vector DB / Agent     | <----  | Pydantic v2 Output     | <----  | Semantic AST Generator   |
  | Context Window        |        | Validation & Formatters|        | (Markdown / JSON Tables) |
  +-----------------------+        +------------------------+        +--------------------------+
```

## Where it fits in the stack
**Category**: [Process Understanding](index.md) / Document Parsing & Knowledge Ingestion.

Docling MCP sits at the knowledge ingestion boundary of enterprise KnowledgeOps and agentic AI architectures. It transforms raw, heterogeneous enterprise documents into clean, chunkable Markdown streams for indexing in vector databases like [Milvus](../infrastructure/milvus.md) or direct ingestion into LLM context windows.

## Typical use cases
- **Multi-Column Financial PDF Processing**: Parsing complex annual reports, balance sheets, and SEC filings while preserving financial table alignments.
- **RAG Document Ingestion Pipelines**: Automated batch conversion of legacy PDF archives into chunk-friendly Markdown documents for vector indexing.
- **Patent & Scientific Standard Processing**: Extracting mathematical formulas, figures, and technical diagrams from multi-page academic papers and patents.
- **Agentic File Discovery**: Allowing autonomous AI agents (such as Claude Code or custom LangGraph nodes) to read local enterprise files on demand via FastMCP tool calls.

## Strengths
- **Protocol Standardization**: Built directly on **FastMCP 3.1**, allowing instant tool registration across modern MCP clients without custom integration adapters.
- **Superior Structural Fidelity**: Layout-aware parsing preserves reading order, section hierarchies, and table relationships across multi-column documents.
- **Multi-Format Versatility**: Uniform API for processing PDFs, Word documents, PowerPoint presentations, HTML web pages, and image scans.
- **Local Privacy & Security**: Processes documents locally on enterprise hardware without streaming sensitive internal files to third-party conversion APIs.

## Limitations
- **Hardware Resource Demand**: Computer vision layout detection and local OCR models require significant CPU/GPU compute for high-concurrency ingestion.
- **First-Run Model Download**: Requires fetching pre-trained layout vision weights during initial startup before offline processing is enabled.
- **Server Process Overhead**: Requires running a persistent local or containerized FastMCP server process to answer agent tool requests.

## When to use it
- When building RAG pipelines or agentic workflows that require precise table structure, section hierarchy, and multi-column PDF layout preservation.
- When your agents operate within FastMCP 3.1 compliant environments and need native file conversion capabilities.
- When enterprise data privacy mandates on-premise document processing without external cloud conversion dependencies.

## When not to use it
- For simple, single-column plain text files where standard file reads (`Path.read_text()`) require zero memory overhead.
- In low-memory edge devices or IoT environments where vision model weights cannot be loaded.
- When simple web scraping is sufficient (use [Firecrawl](firecrawl.md) or [Crawl4AI](crawl4ai.md)).

## Getting started

### 1. Install Docling MCP and FastMCP Dependencies
Install the official server package along with PyTorch/vision runtime:

```bash
pip install docling-mcp fastmcp pydantic
```

### 2. Launch Local FastMCP Server Process
Start the Docling MCP server in stdio or SSE mode:

```bash
docling-mcp start --transport stdio
```

### 3. Register with Claude Desktop / MCP Clients
Add Docling MCP to your client configuration file (`mcp_servers.json`):

```json
{
  "mcpServers": {
    "docling-mcp": {
      "command": "docling-mcp",
      "args": ["start", "--transport", "stdio"]
    }
  }
}
```

## CLI examples

### 1. Convert Local Multi-Column PDF to Markdown
Parse a local financial statement and output structured Markdown:

```bash
docling-mcp convert --path "./reports/q4_financials.pdf" --format markdown --output "./clean/q4_financials.md"
```

### 2. Process Remote URL Document
Fetch and parse a web-hosted technical specification PDF directly:

```bash
docling-mcp convert --url "https://example.com/specifications.pdf" --extract-tables
```

### 3. Query Server Status & Vision Model Health
Check current GPU acceleration, loaded vision model weights, and server health:

```bash
docling-mcp status
```

## API examples

### 1. FastMCP 3.1 Tool Server Implementation
The following Python script demonstrates building a custom FastMCP 3.1 tool server wrapping Docling conversion logic:

```python
import os
import tempfile
from typing import List, Optional
from fastmcp import FastMCP
from pydantic import BaseModel, Field
from docling.document_converter import DocumentConverter

mcp = FastMCP(
    name="Docling Parsing Gateway",
    version="3.1.0",
    description="FastMCP server for layout-aware document conversion and table extraction"
)

class ConversionRequest(BaseModel):
    file_path_or_url: str = Field(..., description="Local file path or remote URL to parse")
    export_format: str = Field(default="markdown", description="Format: markdown, json, or doctags")
    extract_tables: bool = Field(default=True, description="Extract tabular data into clean Markdown format")

class ConversionResponse(BaseModel):
    success: bool
    title: str
    content: str
    table_count: int
    error_message: Optional[str] = None

@mcp.tool(description="Converts enterprise PDFs, DOCX, or PPTX files into layout-faithful Markdown or JSON.")
def convert_document(request: ConversionRequest) -> ConversionResponse:
    """Parses document using Docling layout vision engine."""
    try:
        converter = DocumentConverter()
        result = converter.convert(request.file_path_or_url)

        md_output = result.document.export_to_markdown()
        num_tables = len(result.document.tables) if hasattr(result.document, "tables") else 0

        return ConversionResponse(
            success=True,
            title=result.document.name or "Parsed Document",
            content=md_output,
            table_count=num_tables,
            error_message=None
        )
    except Exception as e:
        return ConversionResponse(
            success=False,
            title="Error",
            content="",
            table_count=0,
            error_message=str(e)
        )

if __name__ == "__main__":
    mcp.run()
```

### 2. Pydantic v2 Parsing Result Validation Model
Validate and transform Docling conversion outputs inside custom Python RAG ingestion pipelines:

```python
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

class ExtractedTable(BaseModel):
    table_index: int = Field(..., ge=0)
    rows_count: int = Field(..., ge=1)
    columns_count: int = Field(..., ge=1)
    markdown_representation: str

class ParsedDoclingAST(BaseModel):
    document_name: str
    num_pages: int = Field(..., ge=1)
    markdown_full_text: str
    tables: List[ExtractedTable] = Field(default_factory=list)

    @field_validator("markdown_full_text")
    def check_non_empty(cls, v):
        if not v.strip():
            raise ValueError("Parsed Markdown text cannot be empty")
        return v

# Early 2027 Pipeline Ingestion Example
if __name__ == "__main__":
    sample_payload = {
        "document_name": "annual_report_2026.pdf",
        "num_pages": 42,
        "markdown_full_text": "# Executive Summary\n\nFiscal year 2026 demonstrated strong revenue growth...",
        "tables": [
            {
                "table_index": 0,
                "rows_count": 5,
                "columns_count": 3,
                "markdown_representation": "| Metric | Q3 | Q4 |\n|---|---|---|\n| Revenue | $10M | $12M |"
            }
        ]
    }

    try:
        ast = ParsedDoclingAST.model_validate(sample_payload)
        print(f"Parsed '{ast.document_name}' ({ast.num_pages} pages) successfully.")
        print(f"Extracted {len(ast.tables)} tabular elements.")
    except ValidationError as e:
        print(f"Validation failed: {e}")
```

### 3. Agent Tool Invocation Payload (JSON-RPC / MCP)
Standard JSON-RPC 2.0 tool invocation format sent by MCP agents to Docling MCP:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "convert_document",
    "arguments": {
      "file_path_or_url": "https://example.com/sec-10k.pdf",
      "export_format": "markdown",
      "extract_tables": true
    }
  },
  "id": 42
}
```

## Related tools / concepts
- [Docling](docling.md) — Underlying document parsing engine developed by IBM Research.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Standard open protocol for LLM tool integration.
- [OCRmyPDF](ocrmypdf.md) — Local optical character recognition utility for image PDFs.
- [Milvus](../infrastructure/milvus.md) — Enterprise distributed vector database.
- [RAGFlow](ragflow.md) — Open-source document-focused RAG engine.
- [Firecrawl](firecrawl.md) — Web-to-Markdown scraping and parsing platform.
- [Crawl4AI](crawl4ai.md) — Async open-source web crawler for LLMs.

## Sources / references
- [Docling MCP GitHub Repository](https://github.com/docling-project/docling-mcp)
- [Docling Official Documentation](https://docling.ai/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
