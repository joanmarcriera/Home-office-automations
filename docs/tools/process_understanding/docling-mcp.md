# Docling MCP

## What it is
Docling MCP is a high-performance document processing service that implements the FastMCP 3.1 / Model Context Protocol specification to expose advanced document conversion, layout parsing, and structured data extraction tools to AI agents. In early 2027, it serves as a critical bridge for feeding structured, layout-faithful PDF, DOCX, PPTX, and HTML content into reasoning models like **Claude 5.1**, **GPT-5.5 / GPT-5.6**, and **Gemini 4.0**.

## What problem it solves
It eliminates the layout and reading-order corruption common in traditional document ingestion pipelines for Retrieval-Augmented Generation (RAG). Standard text extraction packages struggle with multi-column layouts, floating sidebars, embedded charts, complex tables, and mathematical formulas, frequently merging adjacent paragraphs incorrectly. Docling MCP uses vision-aware layout detection models to parse raw documents into highly accurate, semantically structured Markdown or JSON.

## Where it fits in the stack
**Tool / Agentic Service**. It sits in the "Process & Understanding" layer of the KnowledgeOps stack, serving as a standardized **FastMCP 3.1** document ingestion and transformation pipeline that agents call dynamically to digest raw enterprise documents.

## Typical use cases
- **Complex PDF Parsing for Agents**: Giving Claude 5.1 or GPT-5.5 agents the capability to convert multi-column financial reports, patents, or technical standards into Markdown.
- **RAG Pipeline Ingestion**: Converting directory batches of legacy PDF archives into chunk-optimized Markdown strings for vector indexing in engines like [Milvus](../infrastructure/milvus.md).
- **Relational Table Extraction**: Extracting multi-row, borderless tables directly into clean Markdown or JSON arrays for database analysis.
- **Dynamic Context Building**: Loading both local files and remote URLs directly into an agent's context window with zero-config MCP setup.

## Strengths
- **Protocol Standardization**: Native compliance with **FastMCP 3.1** standards, enabling zero-config tool registration across modern MCP clients (Claude Desktop, Claude Code, Zed, or custom orchestrators).
- **Layout-Aware Integrity**: Uses advanced vision-based layout parsing to preserve structural reading order, header hierarchies, sidebars, and nested tables.
- **Format Agnostic**: Seamlessly converts PDFs, DOCX, PPTX, and HTML files into unified, LLM-ready formats.
- **Local Cache Performance**: Features smart file caching and multi-core batch processing pipelines to accelerate parsing of large document folders.

## Limitations
- **High Resource Footprint**: Visual layout detection is CPU and GPU intensive, requiring substantial local resources for high-concurrency workloads.
- **Local Model Downloads**: Requires downloading lightweight layout models during first-time execution.
- **Host Constraints**: Requires a running MCP client environment or host server to expose tools to agents.

## When to use it
- When building a local or cloud RAG application where layout preservation and reading-order accuracy are critical.
- When your autonomous agents operate in FastMCP-compliant environments and need to process multi-format enterprise files.
- When you require clean, structured JSON or Markdown representing structural document hierarchies.

## When not to use it
- For trivial, single-column plain-text documents where lightweight text utilities (like native python file reads) offer near-zero latency.
- In resource-constrained edge environments where downloading layout models is not possible.

## Getting started

Docling MCP can be run as an independent server process or registered directly within your MCP client environment.

### 1. Installation
Install the server package via pip:

```bash
pip install docling-mcp pydantic
```

### 2. Start the Server
Initiate the FastMCP 3.1 server process locally:

```bash
docling-mcp start
```

### 3. Register with Claude Desktop / Claude Code
Add Docling MCP to your local `mcp_servers.json` configuration file:

```json
{
  "mcpServers": {
    "docling-mcp": {
      "command": "docling-mcp",
      "args": ["start"]
    }
  }
}
```

## CLI examples

### Convert a Complex PDF File
Parse a multi-column PDF into semantically ordered Markdown:
```bash
docling-mcp convert --path "./documents/annual_report.pdf" --format markdown
```

### Download and Parse a Remote PDF
Directly stream and convert a web-hosted PDF file:
```bash
docling-mcp convert --url "https://example.com/spec.pdf" --output-dir "./clean_docs"
```

### Query Server Health
Check current operational status and loaded model configurations:
```bash
docling-mcp status
```

## API examples

### FastMCP Tool Call: convert_document
Agents invoke Docling MCP using standardized tool payloads corresponding to the FastMCP 3.1 schema:

```json
{
  "name": "convert_document",
  "arguments": {
    "source": "https://example.com/complex-financial-report.pdf",
    "export_format": "markdown"
  }
}
```

### Programmatic Python Invocation with Pydantic v2
Interact with the underlying conversion framework inside custom Python pipelines:

```python
from docling.document_converter import DocumentConverter
from pydantic import BaseModel, Field

class ConversionResult(BaseModel):
    success: bool
    markdown_content: str = Field(description="Structured Markdown output")
    document_title: str = Field(default="Untitled", description="Extracted document title")

def parse_pdf_to_markdown(source_url: str) -> ConversionResult:
    try:
        converter = DocumentConverter()
        conversion_result = converter.convert(source_url)
        md_text = conversion_result.document.export_to_markdown()
        return ConversionResult(
            success=True,
            markdown_content=md_text,
            document_title=conversion_result.document.name or "Document"
        )
    except Exception as e:
        return ConversionResult(success=False, markdown_content=str(e), document_title="Error")

# Example execution
# parsed_doc = parse_pdf_to_markdown("https://example.com/technical-paper.pdf")
# print(parsed_doc.markdown_content)
```

## Related tools / concepts
- [Model Context Protocol](../automation_orchestration/mcp.md) - Standard protocol for agent-to-tool integrations.
- [Docling](docling.md) - Core layout parsing library developed by IBM.
- [OCRmyPDF](ocrmypdf.md) - Local OCR engine for scanned PDFs.
- [Milvus](../infrastructure/milvus.md) - High-scalability vector database.
- [RAGFlow](ragflow.md) - Document-centric RAG platform.
- [LangGraph](../frameworks/langgraph.md) - Multi-agent application framework.
- [Firecrawl](firecrawl.md) - Web-to-markdown scraping platform.
- [Crawl4AI](crawl4ai.md) - Asynchronous web crawling library.

## Sources / references
- [Docling MCP GitHub Repository](https://github.com/docling-project/docling-mcp)
- [Docling Main Project Hub](https://docling.ai/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
