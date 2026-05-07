# Docling

## What it is
Docling is an open-source Python library designed to simplify document processing by parsing diverse formats into structured, machine-readable data. It excels at layout analysis and table recognition.

## What problem it solves
Document extraction is often fragile and loses structural information like headers and table relationships. Docling uses specialized AI models to preserve document structure, making it ideal for high-fidelity RAG and document analysis.

## Where it fits in the stack
**Document Processing Layer**. It acts as the core engine for [Docling MCP](docling-mcp.md) and other ingestion pipelines.

## Typical use cases
- Converting complex PDFs, DOCX, and PPTX files into structured Markdown or JSON.
- Extracting tables from documents as Pandas DataFrames.
- Powering the ingestion phase of a Retrieval-Augmented Generation (RAG) system.
- Building searchable archives from local document stores.

## Strengths
- **Advanced Layout Analysis**: Accurately detects headers, paragraphs, and lists.
- **Superior Table Recognition**: Handles complex, nested, or borderless tables.
- **Local Execution**: Runs entirely on commodity hardware with no external API calls required.
- **Modular Design**: Easy to extend with new models or formats.

## Limitations
- **Resource Intensive**: Requires significant CPU/GPU resources for processing large batches of complex PDFs.
- **Python-Centric**: Primarily available as a Python library (though it can be served as an API).

## When to use it
- When you need to extract structured information from documents while preserving their visual and logical layout.
- When data privacy is a priority and you want to avoid cloud-based OCR services.

## When not to use it
- For extremely simple text files where basic `pypdf` or `pdfminer` would be faster.
- For high-volume real-time processing on low-powered edge devices.

## Getting started

### Installation
```bash
# Install the core library
pip install docling
```

### Basic usage
```python
from docling.document_converter import DocumentConverter

source = "https://arxiv.org/pdf/2408.09869"  # URL or local path
converter = DocumentConverter()
result = converter.convert(source)
print(result.document.export_to_markdown())
```

## CLI examples
```bash
# Convert a local PDF to Markdown (default output)
docling report.pdf

# Convert to JSON and skip OCR for speed
docling report.pdf --to json --no-ocr

# Batch convert all PDFs in a directory to a specific output folder
docling ./input_docs --from pdf --output ./converted_docs
```

## API examples
```python
from docling.document_converter import DocumentConverter

# Advanced conversion with customized pipeline
converter = DocumentConverter()
result = converter.convert("technical_manual.pdf")

# Extract structured components
markdown_content = result.document.export_to_markdown()
# Access tables as DataFrames (if any detected)
# tables = result.document.tables
```

## Related tools / concepts
- [Docling MCP](docling-mcp.md)
- [OCRmyPDF](ocrmypdf.md)
- [Unstructured](../intake_storage/unstructured.md)
- [LlamaParse](../intake_storage/llamaparse.md)
- [Tesseract CLI](tesseract.md)
- [Crawl4AI](crawl4ai.md)
- [Firecrawl](firecrawl.md)

## Sources / references
- [Official Website](https://github.com/docling-project/docling)
- [Docling Documentation](https://docling-project.github.io/docling/)

## Contribution Metadata
- Last reviewed: 2026-04-06
- Confidence: high
