# Docling MCP

## What it is
Docling MCP is a high-performance document processing service that implements the Model Context Protocol (MCP 3.1) to expose advanced document conversion, parsing, and structured data generation tools to AI agents. In late 2026, it serves as a critical bridge for feeding structured, high-fidelity PDF, DOCX, and PPTX information into reasoning models like **Claude 5.1**, **GPT-5.5**, and **Gemini 4.0**.

## What problem it solves
It eliminates the heavy layout and reading-order extraction challenges in RAG (Retrieval-Augmented Generation) pipelines. Standard parser packages struggle with complex multi-column layouts, tables, embedded charts, and mathematical notations, frequently merging adjacent paragraphs incorrectly. Docling MCP uses vision-aware layout detection to parse raw documents into highly accurate, semantically organized Markdown or structured JSON.

## Where it fits in the stack
**Tool / Agentic Service**. It sits in the "Process & Understanding" layer of the KnowledgeOps stack, serving as a standardized MCP 3.1 document ingestion and transformation pipeline that agents call dynamically to digest raw company assets.

## Typical use cases
- **Complex PDF Parsing for Agents**: Giving Claude 5.1 the ability to seamlessly convert financial reports, technical standards, or research studies into Markdown.
- **RAG Pipeline Ingestion**: Converting directory batches of legacy PDF archives into chunk-optimized Markdown strings for vector indexing in engines like [Milvus](../infrastructure/milvus.md).
- **Relational Table Extraction**: Extracting multi-row, multi-column tables directly into standard Markdown format for structured database analytics.
- **Dynamic Context Building**: Loading both local files and remote URLs directly into an agent's context window with zero-config setup.

## Strengths
- **Protocol Standardization**: Built on native **MCP 3.1** standards, enabling seamless tool registration across modern MCP clients (e.g., Claude Desktop, Zed, or custom orchestrators).
- **Layout-Aware Integrity**: Features advanced layout parsing to handle complex visual structures, including header nesting, floating sidebars, and nested tables.
- **Format Agnostic**: Seamlessly converts PDFs, DOCX, PPTX, and HTML into unified LLM-ready formats.
- **Local Cache Performance**: Includes smart file caching and multi-core batch processing pipelines to speed up processing of large document folders.

## Limitations
- **High Resource Footprint**: Visual layout parsing is CPU and memory intensive, requiring substantial local resources for production concurrency.
- **Dependency on Local Models**: Relies on lightweight layout models which must be downloaded during first-time execution.
- **Host Constraints**: Requires a running MCP client environment to act as an agent-accessible tool.

## When to use it
- When building a local or cloud RAG application where high-precision document layout preservation is essential.
- When your autonomous agents are integrated with MCP-compliant environments and need to read complex multi-format corporate files.
- When you require clean, structured JSON or Markdown representing structural document hierarchies.

## When not to use it
- For trivial, plain-text documents where lightweight text utilities (like native python file reads) offer near-zero latency.
- In resource-constrained edge environments where downloading layout models is not possible.

## Getting started

Docling MCP can be run as an independent server or registered inside your MCP host.

### 1. Installation
Install the server using pip:

```bash
pip install docling-mcp
```

### 2. Start the Server
Initiate the server process to make tools available locally:

```bash
docling-mcp start
```

### 3. Register with Claude Desktop
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
Parse a multi-column corporate PDF into semantically ordered Markdown:
```bash
docling-mcp convert --path "./documents/annual_report.pdf" --format markdown
```

### Download and Parse a Remote PDF
Directly stream and convert a web-based PDF:
```bash
docling-mcp convert --url "https://example.com/spec.pdf" --output-dir "./clean_docs"
```

### Query Server Health
Check current server operational parameters:
```bash
docling-mcp status
```

## API examples

### MCP Tool Call: convert_document
Agents invoke Docling MCP using standardized tool payloads corresponding to the MCP 3.1 schema:

```json
{
  "name": "convert_document",
  "arguments": {
    "source": "https://example.com/complex-financial-report.pdf",
    "export_format": "markdown"
  }
}
```

### Programmatic Python Invocation
Interact with the underlying conversion framework directly inside custom Python pipelines:

```python
from docling.document_converter import DocumentConverter
from pydantic import BaseModel

class ConversionResult(BaseModel):
    success: bool
    markdown_content: str

def parse_pdf_to_markdown(source_url: str) -> ConversionResult:
    try:
        converter = DocumentConverter()
        conversion_result = converter.convert(source_url)
        md_text = conversion_result.document.export_to_markdown()
        return ConversionResult(success=True, markdown_content=md_text)
    except Exception as e:
        return ConversionResult(success=False, markdown_content=str(e))

# Example usage
# parsed_doc = parse_pdf_to_markdown("https://example.com/technical-paper.pdf")
# print(parsed_doc.markdown_content)
```

## Related tools / concepts
- [Model Context Protocol](../automation_orchestration/mcp.md) - Protocol for connecting client models to external tools.
- [Docling](docling.md) - Core layout parsing library developed by IBM.
- [OCRmyPDF](ocrmypdf.md) - Local OCR processing tool for scanned PDFs.
- [Milvus](../infrastructure/milvus.md) - High-scalability vector database.
- [RAGFlow](ragflow.md) - Advanced document-centric RAG engine.
- [LangGraph](../frameworks/langgraph.md) - State-based multi-agent application framework.
- [Smolagents](../frameworks/smolagents.md) - Lightweight agent-building framework.
- [Firecrawl](firecrawl.md) - High-efficiency web-to-markdown scraping platform.
- [Crawl4AI](crawl4ai.md) - Asynchronous, local-first web crawling library.

## Sources / references
- [Docling MCP GitHub Repository](https://github.com/docling-project/docling-mcp)
- [Docling Main Project Hub](https://docling.ai/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-11-01
- Confidence: high
