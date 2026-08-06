# Docling

## What it is
Docling is an open-source Python library and CLI tool developed by IBM Research that simplifies document processing by parsing diverse formats into structured, machine-readable data. In late December 2026, it excels at layout analysis, table recognition, and multi-modal document understanding for [Gemma 3](../ai_knowledge/local_llms.md), Claude 5.1, GPT-5.5, and other frontier models.

## What problem it solves
Traditional document extraction often loses structural information (headers, table relationships, reading order) or fails on complex layouts. Docling uses specialized models to preserve document structure, making it ideal for high-fidelity Retrieval-Augmented Generation (RAG) and [Agentic Session Orchestration](../../knowledge_base/agent_protocols.md) workflows using [Gemma 3](../ai_knowledge/local_llms.md), Claude 5.1, and GPT-5.5.

## Where it fits in the stack
**Category**: [Process & Understanding](index.md). It acts as the core parsing engine for ingestion pipelines, [Docling MCP](docling-mcp.md), and Knowledge Graph construction via native graph export features.

## Typical use cases
- **Multi-format Conversion**: Converting PDFs, DOCX, PPTX, HTML, and more into structured Markdown or JSON.
- **VLM-powered Extraction**: Using vision-language models (VLMs) like GraniteDocling to understand charts, diagrams, and complex visual layouts.
- **RAG Ingestion**: Powering the document preparation phase of RAG systems with high-fidelity structure preservation.
- **Knowledge Graph Generation**: Transforming unstructured documents into validated knowledge graphs with precise semantic relationships.

## Strengths
- **Superior Table Recognition**: Handles nested, borderless, and complex tables with high accuracy.
- **Native VLM Support**: Integrated support for GraniteDocling and other VLMs for visual document understanding (v2.85+ as of late December 2026).
- **Local & Hybrid Execution**: Runs entirely on local hardware (CPU/GPU) or integrates with local LLMs ([vLLM](../infrastructure/vllm.md), [Ollama](../../services/ollama.md)) and APIs.
- **Extensive Integration**: Seamlessly works with LangChain, LlamaIndex, and [CrewAI](../frameworks/crewai.md).

## Limitations
- **Python 3.10+ Requirement**: Support for Python 3.9 was dropped in early 2026.
- **Resource Intensive**: High-fidelity VLM parsing requires significant VRAM or powerful CPUs for local execution.
- **Learning Curve**: Advanced pipeline customization (e.g., custom chunking, hybrid strategies) requires understanding the internal object model.

## When to use it
- When you need to preserve the logical and visual layout of complex documents for AI ingestion.
- For high-fidelity RAG where header-paragraph relationships and table data are critical.
- When transforming technical document collections into structured knowledge formats for [Gemma 3](../ai_knowledge/local_llms.md).

## When not to use it
- For simple plain-text extraction where speed and resource efficiency are prioritized over structure.
- If you are restricted to Python 3.9 or older environments.

## Getting started

### Installation
Docling requires Python >= 3.10.

```bash
# Install the core library
pip install docling pydantic>=2.0

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

### Python: Document Conversion & Pydantic v2 Structuring
This script converts a document using Docling and extracts tables and structural headings, validating the structured outputs against strict Pydantic v2 schemas.

```python
from typing import List, Literal, Optional
from pydantic import BaseModel, Field
from docling.document_converter import DocumentConverter

# 1. Define strict Pydantic v2 schemas for document layout structure
class ExtractedTable(BaseModel):
    table_index: int = Field(..., ge=0)
    caption: Optional[str] = None
    rows_count: int = Field(..., gt=0)
    columns_count: int = Field(..., gt=0)
    markdown_representation: str = Field(..., min_length=5)

class DocumentStructure(BaseModel):
    title: str = Field(..., min_length=2)
    headings: List[str] = Field(default_factory=list)
    tables: List[ExtractedTable] = Field(default_factory=list)
    word_count: int = Field(..., gt=0)
    is_fully_parsed: bool

# 2. Convert and validate structures
def parse_and_validate_document(source_path: str) -> Optional[DocumentStructure]:
    try:
        # Initialize standard Docling document converter
        converter = DocumentConverter()
        result = converter.convert(source_path)
        doc = result.document

        headings = []
        tables = []

        # Iterate over structural items in doc and build schema parameters
        for idx, element in enumerate(doc.elements):
            if element.type == "heading":
                headings.append(element.text)
            elif element.type == "table":
                tables.append(ExtractedTable(
                    table_index=idx,
                    caption=element.caption if hasattr(element, "caption") else None,
                    rows_count=len(element.rows) if hasattr(element, "rows") else 1,
                    columns_count=len(element.cols) if hasattr(element, "cols") else 1,
                    markdown_representation=element.export_to_markdown() if hasattr(element, "export_to_markdown") else ""
                ))

        payload = {
            "title": doc.title if hasattr(doc, "title") and doc.title else "Untitled Parse Document",
            "headings": headings,
            "tables": tables,
            "word_count": len(doc.text.split()) if hasattr(doc, "text") else 1,
            "is_fully_parsed": True
        }

        # Validate using Pydantic v2
        validated_doc = DocumentStructure.model_validate(payload)
        return validated_doc
    except Exception as e:
        print(f"Failed parsing/validation: {e}")
        return None

if __name__ == "__main__":
    doc_struct = parse_and_validate_document("https://arxiv.org/pdf/2408.09869")
    if doc_struct:
        print(f"Validated document '{doc_struct.title}' with {len(doc_struct.tables)} tables.")
```

### MCP 3.1 / FastMCP 3.1 Integration
Docling can be exposed as an MCP 3.1 tool for agentic document parsing:

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
- [Agentic Session Orchestration](../../knowledge_base/agent_protocols.md)
- [Local LLMs (Gemma 3)](../ai_knowledge/local_llms.md)

## Sources / References
- [Official Website (GitHub)](https://github.com/docling-project/docling)
- [Docling Documentation](https://docling-project.github.io/docling/)
- [Docling-Graph Repository](https://github.com/docling-project/docling-graph)
- [IBM Research AI Blogs](https://research.ibm.com/blog/docling-ibm-granite-document-parsing)

## Contribution Metadata
- Last reviewed: 2026-12-06
- Confidence: high
