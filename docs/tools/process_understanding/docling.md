# Docling

## What it is
Docling is an open-source Python library and CLI tool developed by IBM Research that simplifies document processing by parsing diverse formats into structured, machine-readable data. It excels at layout analysis, table recognition, and multi-modal document understanding.

## What problem it solves
Traditional document extraction often loses structural information (headers, table relationships, reading order) or fails on complex layouts. Docling uses specialized models to preserve document structure, making it ideal for high-fidelity Retrieval-Augmented Generation (RAG) and agentic workflows using Claude 4.8 and GPT-5.5.

## Where it fits in the stack
**Category**: [Process & Understanding](index.md). It acts as the core parsing engine for ingestion pipelines, [Docling MCP](docling-mcp.md), and Knowledge Graph construction via native graph export features.

## Typical use cases
- **Multi-format Conversion**: Converting PDFs, DOCX, PPTX, HTML, and more into structured Markdown or JSON.
- **VLM-powered Extraction**: Using vision-language models (VLMs) to understand charts, diagrams, and complex visual layouts.
- **RAG Ingestion**: Powering the document preparation phase of RAG systems with high-fidelity structure preservation.
- **Knowledge Graph Generation**: Transforming unstructured documents into validated knowledge graphs with precise semantic relationships.

## Strengths
- **Superior Table Recognition**: Handles nested, borderless, and complex tables with high accuracy.
- **Native VLM Support**: Integrated support for GraniteDocling and other VLMs for visual document understanding (v2.70+).
- **Local & Hybrid Execution**: Runs entirely on local hardware (CPU/GPU) or integrates with local LLMs ([vLLM](../infrastructure/vllm.md), [Ollama](../../services/ollama.md)) and APIs.
- **Extensive Integration**: Seamlessly works with LangChain, LlamaIndex, and [CrewAI](../frameworks/crewai.md).

## Limitations
- **Python 3.10+ Requirement**: Support for Python 3.9 was dropped in early 2026.
- **Resource Intensive**: High-fidelity VLM parsing requires significant VRAM or powerful CPUs for local execution.
- **Learning Curve**: Advanced pipeline customization (e.g., custom chunking, hybrid strategies) requires understanding the internal object model.

## When to use it
- When you need to preserve the logical and visual layout of complex documents for AI ingestion.
- For high-fidelity RAG where header-paragraph relationships and table data are critical.
- When transforming technical document collections into structured knowledge formats.

## When not to use it
- For simple plain-text extraction where speed and resource efficiency are prioritized over structure.
- If you are restricted to Python 3.9 or older environments.

## Getting started

### Installation
Docling requires Python >= 3.10.

```bash
# Install the core library
pip install docling

# Install with graph support for Knowledge Graph workflows
pip install docling-graph
```

### Quickstart (Python)
```python
from docling.document_converter import DocumentConverter

source = "https://arxiv.org/pdf/2408.09869"  # URL or local path
converter = DocumentConverter()
result = converter.convert(source)
print(result.document.export_to_markdown())
```

## CLI examples

### Basic Conversion
```bash
# Convert a local PDF to Markdown
docling report.pdf

# Convert a URL and output to JSON
docling https://arxiv.org/pdf/2206.01062 --to json
```

### Advanced Parsing
```bash
# Use a specific VLM for enhanced layout understanding
docling report.pdf --model-id GraniteDocling

# Export as a structured Knowledge Graph (requires docling-graph)
docling-graph convert technical_spec.pdf --output-format cypher
```

## API examples

### Multi-modal Extraction
```python
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat

converter = DocumentConverter(allowed_formats=[InputFormat.PDF, InputFormat.IMAGE])
result = converter.convert("chart_diagram.png")
# Extract data points from a chart
print(result.document.export_to_dict())
```

### MCP 3.0 Integration
Docling can be exposed as an MCP 3.0 tool for agentic document parsing:

```json
{
  "mcpServers": {
    "docling": {
      "command": "npx",
      "args": ["-y", "@docling/mcp-server"]
    }
  }
}
```

## Related tools / concepts
- [Docling MCP](docling-mcp.md)
- [Unstructured](../intake_storage/unstructured.md)
- [LlamaParse](../intake_storage/llamaparse.md)
- [Crawl4AI](crawl4ai.md)
- [Firecrawl](firecrawl.md)
- [vLLM](../infrastructure/vllm.md)
- [Ollama](../../services/ollama.md)
- [MCP (Model Context Protocol)](../../knowledge_base/patterns/tool-calling-and-mcp.md)

## Sources / references
- [Official Website (GitHub)](https://github.com/docling-project/docling)
- [Docling Documentation](https://docling-project.github.io/docling/)
- [Docling-Graph Repository](https://github.com/docling-project/docling-graph)
- [IBM Research AI Blogs](https://research.ibm.com/blog/docling-ibm-granite-document-parsing)

## Contribution Metadata
- Last reviewed: 2026-06-20
- Confidence: high
