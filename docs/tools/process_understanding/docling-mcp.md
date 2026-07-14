# Docling MCP

## What it is
Docling MCP is a document processing service that implements the Model Context Protocol (MCP 3.0) to provide advanced document conversion, processing, and generation tools to AI agents. In June 2026, it is the primary bridge for feeding high-fidelity document data to `claude-4-8-opus-20260528` and GPT-5.5.

## What problem it solves
It simplifies the integration of sophisticated document understanding capabilities into AI workflows. By providing a standardized MCP interface, it allows agents to convert complex PDFs into structured formats, handle large documents via memory management, and integrate directly with RAG pipelines without custom integration code for every application.

## Where it fits in the stack
**Tool / Agentic Service**. It sits in the "Process & Understanding" layer, serving as a sophisticated ingestion and transformation bridge between raw documents and LLM-ready structured data.

## Typical use cases
- **Structured Document Conversion**: Converting PDF documents into structured JSON format (DoclingDocument) for precise LLM analysis.
- **RAG Pipeline Ingestion**: Automatically processing documents and uploading them to Milvus for retrieval-augmented generation.
- **Multi-source Processing**: Handling documents from both local file systems and remote URLs seamlessly.

## Strengths
- **Protocol Standardized**: Native MCP 3.0 support ensures compatibility with any MCP-compliant host (Claude Desktop, IDEs, etc.), allowing for "zero-code" document processing integration.
- **High Fidelity**: Leverages the Docling library's layout-aware parsing for accurate conversion of complex document layouts, including tables and hierarchical headers.
- **Performance Optimized**: Includes local document caching and efficient memory management for handling large-scale processing of enterprise-sized documents.
- **RAG Integration**: Specifically designed to streamline RAG pipelines by providing clean, structured markdown or JSON that is easy to chunk and embed.

## Limitations
- **Format Focus**: Primarily optimized for PDF-to-structured-data workflows.
- **Host Dependency**: Requires an MCP-compatible environment to utilize its tool-calling capabilities.

## When to use it
- When your AI agent needs to extract structured information from complex PDF layouts (tables, headers, etc.).
- When building a RAG application that needs a reliable, high-performance document processing frontend.

## When not to use it
- For basic text extraction from simple, non-layout-heavy files where lighter tools might suffice.
- If your environment does not support the Model Context Protocol.

## Getting started

Docling MCP can be run as a standalone server or integrated into an MCP-compliant host.

### 1. Installation
Install the Docling MCP server via `pip`:

```bash
pip install docling-mcp
```

### 2. Run the Server
Start the server to make the tools available to your agents:

```bash
docling-mcp start
```

### 3. MCP Configuration
Add the server to your `mcp_servers.json` configuration for Claude Desktop or your IDE.

## CLI examples

### 1. Convert a Local File
```bash
docling-mcp convert --path "./reports/financial_q2.pdf" --format markdown
```

### 2. Process a Remote URL
```bash
docling-mcp convert --url "https://example.com/spec.pdf" --output-dir "./output"
```

### 3. Check Server Status
```bash
docling-mcp status
```

## API examples

### MCP Tool Call: Document Conversion
AI agents interact with Docling MCP using standardized tool calls.

```json
{
  "name": "convert_document",
  "arguments": {
    "source": "https://example.com/complex-report.pdf",
    "export_format": "markdown"
  }
}
```

### Python: Programmatic Docling Usage
For deeper integration, the underlying Docling library can be used directly.

```python
from docling.document_converter import DocumentConverter

def convert_to_md(source_url):
    converter = DocumentConverter()
    result = converter.convert(source_url)
    return result.document.export_to_markdown()

# Example usage
# markdown_content = convert_to_md("https://example.com/report.pdf")
```

## Related tools / concepts
- [Model Context Protocol](../automation_orchestration/mcp.md)
- [Docling](docling.md)
- [OCRmyPDF](ocrmypdf.md)
- [Milvus](../infrastructure/milvus.md)
- [RAGFlow](ragflow.md)
- [LangGraph](../frameworks/langgraph.md)
- [Smolagents](../frameworks/smolagents.md)
- [Firecrawl](firecrawl.md)
- [Crawl4AI](crawl4ai.md)

## Sources / references
- [GitHub Repository](https://github.com/docling-project/docling-mcp)
- [Docling Project Documentation](https://docling.ai/)
- [MCP Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-06-28
- Confidence: high
