# Docling MCP

## What it is
Docling MCP is a document processing service that implements the Model Context Protocol (MCP) to provide advanced document conversion, processing, and generation tools to AI agents. It is the standardized interface for the [Docling](docling.md) library, optimized for June 2026 agentic workflows.

## What problem it solves
It simplifies the integration of sophisticated document understanding capabilities into AI workflows. By providing a standardized MCP interface, it allows agents (like `claude-4-8-opus-20260528` and GPT-5.5) to convert complex PDFs into structured formats, handle large documents via memory management, and integrate directly with RAG pipelines without custom integration code for every application.

## Where it fits in the stack
**Tool / Agentic Service**. It sits in the "Process & Understanding" layer, serving as a sophisticated ingestion and transformation bridge between raw documents and LLM-ready structured data.

## Typical use cases
- **Structured Document Conversion**: Converting PDF documents into structured JSON format (DoclingDocument) for precise LLM analysis.
- **RAG Pipeline Ingestion**: Automatically processing documents and uploading them to [Milvus](../infrastructure/milvus.md) for retrieval-augmented generation.
- **Multi-source Processing**: Handling documents from both local file systems and remote URLs seamlessly.
- **Table Extraction**: Reconstructing complex multi-page tables from financial reports with high fidelity.

## Strengths
- **Protocol Standardized**: Native MCP support ensures compatibility with any MCP-compliant host (Claude Desktop, IDEs, etc.).
- **High Fidelity**: Leverages layout-aware parsing for accurate conversion of complex document layouts, including hierarchical headers.
- **Performance Optimized**: Includes local document caching and efficient memory management forHandling enterprise-sized documents.
- **RAG Integration**: Specifically designed to provide clean, structured markdown or JSON that is easy to chunk and embed.
- **Multi-Model Optimized**: Outputs are formatted to maximize the reasoning capabilities of advanced frontier models.

## Limitations
- **Format Focus**: Primarily optimized for PDF and MS Office to structured-data workflows.
- **Host Dependency**: Requires an MCP-compatible environment (e.g., Claude Desktop, Zed, or a custom MCP host) to utilize its tool-calling capabilities.
- **Resource Intensive**: Processing very large, complex PDFs can be CPU and memory intensive on local machines.

## When to use it
- When your AI agent needs to extract structured information from complex PDF layouts (tables, headers, etc.).
- When building a RAG application that needs a reliable, high-performance document processing frontend.
- When requiring a standardized, protocol-driven way to add document intelligence to your agentic stack.

## When not to use it
- For basic text extraction from simple, non-layout-heavy files where lighter tools might suffice.
- If your environment does not support the Model Context Protocol.
- For processing handwritten notes or highly stylized artistic documents where specialized OCR models are better suited.

## Getting started
Docling MCP can be run via `npx` or as a persistent server.

```bash
# Run the Docling MCP server using npx
npx @docling/mcp-server

# Alternatively, add it to your Claude Desktop config
# "docling": {
#   "command": "npx",
#   "args": ["-y", "@docling/mcp-server"]
# }
```

## CLI examples
### 1. Basic Conversion
Convert a local PDF to Markdown via the CLI tool.
```bash
docling-mcp convert --input report.pdf --format markdown
```

### 2. Remote URL Processing
Process a document directly from a URL.
```bash
docling-mcp convert --input https://example.com/spec.pdf --output structured.json
```

### 3. Server Health Check
Verify the status of a running Docling MCP instance.
```bash
docling-mcp status --port 8080
```

## API examples
Integration within an MCP client environment.

```typescript
// Example of an agent calling the Docling MCP tool
const result = await mcpClient.callTool("docling-mcp", "convert_document", {
  source: "https://example.com/complex-report.pdf",
  export_format: "markdown",
  extract_tables: true
});

console.log(result.content[0].text);
```

## Related tools / concepts
- [Model Context Protocol](../automation_orchestration/mcp.md) — The underlying communication standard.
- [Docling](docling.md) — The core library powering this service.
- [Milvus](../infrastructure/milvus.md) — Targeted vector database for Docling outputs.
- [Everything Claude Code](../ai_knowledge/everything-claude-code.md) — Integration point for agentic workflows.
- [OpenDataLoader PDF](opendataloader-pdf.md) — Alternative high-performance PDF parser.
- [RAGFlow](ragflow.md) — Comprehensive RAG framework using Docling.
- [LangGraph](../frameworks/langgraph.md) — Framework for stateful multi-agent document processing.

## Sources / references
- [Docling MCP GitHub Repository](https://github.com/docling-project/docling-mcp)
- [Official Docling Documentation](https://ds4sd.github.io/docling/)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
