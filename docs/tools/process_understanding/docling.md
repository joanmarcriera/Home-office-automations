# Docling

## What it is
Docling is an open-source Python library and CLI tool developed by IBM Research that simplifies document processing by parsing diverse formats into structured, machine-readable data. It excels at layout analysis, table recognition, and multi-modal document understanding.

## What problem it solves
Traditional document extraction often loses structural information (headers, table relationships, reading order) or fails on complex layouts. Docling uses specialized models (e.g., GraniteDocling) to preserve document structure, making it ideal for high-fidelity Retrieval-Augmented Generation (RAG) and agentic workflows.

## Where it fits in the stack
**Category**: [Process Understanding](index.md). It acts as the core parsing engine for ingestion pipelines, [Docling MCP](docling-mcp.md), and Knowledge Graph construction via [Docling-Graph](#advanced-knowledge-graph-construction-docling-graph).

## Typical use cases
- **Multi-format Conversion**: Converting PDFs, DOCX, PPTX, HTML, and more into structured Markdown or JSON.
- **VLM-powered Extraction**: Using vision-language models (VLMs) to understand charts, diagrams, and complex visual layouts.
- **RAG Ingestion**: Powering the document preparation phase of RAG systems with high-fidelity structure preservation.
- **Knowledge Graph Generation**: Transforming unstructured documents into validated knowledge graphs with precise semantic relationships.

## Strengths
- **Superior Table Recognition**: Handles nested, borderless, and complex tables with high accuracy.
- **Native VLM Support**: (v2.70+) Integrated support for GraniteDocling and other VLMs for visual document understanding.
- **Local & Hybrid Execution**: Runs entirely on local hardware (CPU/GPU) or integrates with local LLMs ([vLLM](../infrastructure/vllm.md), [Ollama](../../services/ollama.md)) and APIs.
- **Extensive Integration**: Seamlessly works with LangChain, LlamaIndex, and [CrewAI](../frameworks/crewai.md).

## Limitations
- **Python 3.10+ Requirement**: Support for Python 3.9 was dropped in version 2.70.0 (May 2026).
- **Resource Intensive**: High-fidelity VLM parsing requires significant VRAM or powerful CPUs.
- **Learning Curve**: Advanced pipeline customization (e.g., custom chunking, hybrid strategies) requires understanding the internal object model.

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

## CLI Reference
Docling provides a versatile CLI for batch processing:

```bash
# Convert a local PDF to Markdown
docling report.pdf

# Convert a URL and output to JSON
docling https://arxiv.org/pdf/2206.01062 --to json

# Use a specific VLM for enhanced layout understanding
docling report.pdf --model-id GraniteDocling
```

## Advanced: Knowledge Graph Construction (Docling-Graph)
Released in 2026, **Docling-Graph** converts unstructured documents into validated NetworkX Directed Graphs with rich edge metadata.

```python
from docling_graph import DoclingGraphConverter

# Convert a document into a semantic knowledge graph
converter = DoclingGraphConverter(llm_provider="ollama")
graph = converter.convert("technical_spec.pdf")

# Export to Cypher for Neo4j import
graph.export_to_cypher("output.cypher")
```

## Features (2026 Update)
- **Chart Understanding**: Native extraction of data points and insights from charts and diagrams using VLMs.
- **Docling-Graph**: Transformation of text into precise semantic relationships for explainable reasoning.
- **Hybrid Chunking**: Leverages Docling's segmentation with semantic LLM chunking for context-aware RAG.
- **Trace System**: Unified logging and visualization of the extraction pipeline.

## When to use it
- When you need to preserve the logical and visual layout of complex documents.
- For high-fidelity RAG where header-paragraph relationships and table data are critical.
- When transforming technical document collections into knowledge graphs.

## When not to use it
- For simple plain-text extraction where speed is prioritized over structure.
- If you are restricted to Python 3.9 or older environments.

## Related tools / concepts
- [Docling MCP](docling-mcp.md)
- [Unstructured](../intake_storage/unstructured.md)
- [LlamaParse](../intake_storage/llamaparse.md)
- [Crawl4AI](crawl4ai.md)
- [Firecrawl](firecrawl.md)
- [vLLM](../infrastructure/vllm.md)
- [Ollama](../../services/ollama.md)
- [NetworkX](https://networkx.org/)

## Sources / References
- [Official Website (GitHub)](https://github.com/docling-project/docling)
- [Docling Documentation](https://docling-project.github.io/docling/)
- [Docling-Graph Repository](https://github.com/docling-project/docling-graph)
- [IBM Think 2026 Announcements](https://www.ibm.com/new/announcements/ibm-think-2026)

## Contribution Metadata
- Last reviewed: 2026-05-28
- Confidence: high
