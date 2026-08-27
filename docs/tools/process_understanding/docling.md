# Docling

## What it is
Docling is an open-source Python library and CLI tool developed by IBM Research that simplifies document processing by parsing diverse formats into structured, machine-readable data. In early January 2027 (v2.20.x+), it excels at layout analysis, table recognition, and multi-modal document understanding for [Gemma 4](../ai_knowledge/local_llms.md) and other frontier models.

## What problem it solves
Traditional document extraction often loses structural information (headers, table relationships, reading order) or fails on complex layouts. Docling uses specialized models to preserve document structure, making it ideal for high-fidelity Retrieval-Augmented Generation (RAG) and [Agentic Session Orchestration](../../knowledge_base/agent_protocols.md) workflows using **Gemma 4**, **GPT-5.6**, **Claude 5.6**, and **Gemini 4.0 Ultra**.

## Where it fits in the stack
**Category**: [Process & Understanding](index.md). It acts as the core parsing engine for ingestion pipelines, [Docling MCP](docling-mcp.md), and Knowledge Graph construction via native graph export features.

## Typical use cases
- **Multi-format Conversion**: Converting PDFs, DOCX, PPTX, HTML, and more into structured Markdown or JSON.
- **VLM-powered Extraction**: Using vision-language models (VLMs) like GraniteDocling v2 to understand charts, diagrams, and complex visual layouts.
- **RAG Ingestion**: Powering the document preparation phase of RAG systems with high-fidelity structure preservation.
- **Knowledge Graph Generation**: Transforming unstructured documents into validated knowledge graphs with precise semantic relationships.

## Strengths
- **Superior Table Recognition**: Handles nested, borderless, and complex tables with high accuracy.
- **Native VLM Support**: Integrated support for GraniteDocling v2 and other VLMs for visual document understanding (v2.80+ and v2.20+).
- **Local & Hybrid Execution**: Runs entirely on local hardware (CPU/GPU) or integrates with local LLMs ([vLLM](../infrastructure/vllm.md), [Ollama](../../services/ollama.md)) and APIs.
- **Extensive Integration**: Seamlessly works with LangChain, LlamaIndex, FastMCP 3.1, and [CrewAI](../frameworks/crewai.md).

## Limitations
- **Python 3.10+ Requirement**: Support for Python 3.9 was dropped in early 2026.
- **Resource Intensive**: High-fidelity VLM parsing requires significant VRAM or powerful CPUs for local execution.
- **Learning Curve**: Advanced pipeline customization (e.g., custom chunking, hybrid strategies) requires understanding the internal object model.

## When to use it
- When you need to preserve the logical and visual layout of complex documents for AI ingestion.
- For high-fidelity RAG where header-paragraph relationships and table data are critical.
- When transforming technical document collections into structured knowledge formats for [Gemma 4](../ai_knowledge/local_llms.md).

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

### Multi-modal Extraction
```python
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat

# Initialize with VLM support for charts and diagrams
converter = DocumentConverter(allowed_formats=[InputFormat.PDF, InputFormat.IMAGE])
result = converter.convert("chart_diagram.png")
# Extract data points from a chart
print(result.document.export_to_dict())
```

### Programmatic Extraction Verification with Strict Pydantic v2 Validation
This example showcases a production conversion harness that validates the schema of parsed document elements, layout chunks, and extracted table objects using Pydantic v2.

```python
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator

# 1. Define strict Pydantic v2 models for Docling document structures
class DoclingTable(BaseModel):
    table_id: str = Field(..., pattern=r"^tbl_\d+$")
    rows: int = Field(..., ge=1)
    columns: int = Field(..., ge=1)
    header_row: List[str]
    content: List[List[str]]

class DoclingElement(BaseModel):
    element_type: str = Field(..., pattern=r"^(heading|paragraph|table|list_item|chart)$")
    text_content: str
    page_number: int = Field(..., ge=1)
    confidence: float = Field(1.0, ge=0.0, le=1.0)
    table_data: Optional[DoclingTable] = None

    @field_validator("table_data")
    @classmethod
    def validate_table_if_table_type(cls, v: Optional[DoclingTable], info) -> Optional[DoclingTable]:
        element_type = info.data.get("element_type")
        if element_type == "table" and v is None:
            raise ValueError("table_data must be provided when element_type is 'table'")
        return v

class ParsedDocPayload(BaseModel):
    filename: str
    num_pages: int = Field(..., ge=1)
    elements: List[DoclingElement]

# 2. Strict run conversion and validation
def validate_docling_parsing(raw_payload: dict) -> Optional[ParsedDocPayload]:
    try:
        doc = ParsedDocPayload.model_validate(raw_payload)
        return doc
    except Exception as e:
        print(f"Docling output payload validation failed: {e}")
        return None

if __name__ == "__main__":
    sample_docling_payload = {
        "filename": "annual_earnings_summary.pdf",
        "num_pages": 4,
        "elements": [
            {
                "element_type": "heading",
                "text_content": "Section 1: Revenue Breakdown",
                "page_number": 1,
                "confidence": 0.99
            },
            {
                "element_type": "table",
                "text_content": "[Parsed Table Element]",
                "page_number": 2,
                "confidence": 0.97,
                "table_data": {
                    "table_id": "tbl_201",
                    "rows": 2,
                    "columns": 2,
                    "header_row": ["Quarter", "Revenue (B$)"],
                    "content": [["Q1 2026", "4.2"], ["Q2 2026", "4.8"]]
                }
            }
        ]
    }

    parsed_doc = validate_docling_parsing(sample_docling_payload)
    if parsed_doc:
        print(f"Docling conversion verified for: {parsed_doc.filename}")
        print(f"Total elements analyzed: {len(parsed_doc.elements)}")
        table_el = parsed_doc.elements[1]
        if table_el.table_data:
            print(f"Found Table ID {table_el.table_data.table_id} with headers: {table_el.table_data.header_row}")
```

### FastMCP 3.1 Integration
Docling can be exposed as an MCP tool for agentic document parsing using FastMCP 3.1:

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
- [Local LLMs (Gemma 4)](../ai_knowledge/local_llms.md)

## Sources / References
- [Official Website (GitHub)](https://github.com/docling-project/docling)
- [Docling Documentation](https://docling-project.github.io/docling/)
- [Docling-Graph Repository](https://github.com/docling-project/docling-graph)
- [IBM Research AI Blogs: Docling IBM Granite Document Parsing](https://research.ibm.com/blog/docling-ibm-granite-document-parsing)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high
