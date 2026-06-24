# OpenDataLoader PDF

## What it is
OpenDataLoader PDF is a specialized, open-source ingestion engine designed for high-fidelity conversion of complex PDF documents into AI-ready data formats (Markdown and JSON). It focuses on preserving semantic structure, including tables, multi-column layouts, and mathematical formulas.

## What problem it solves
It solves the "garbage-in, garbage-out" problem in RAG pipelines. Standard PDF parsers often fail on complex layouts, resulting in jumbled text that causes hallucinations in LLMs like Claude 4.8 or GPT-5.5. OpenDataLoader uses vision-aware layout detection to ensure that text is extracted in the correct reading order.

## Where it fits in the stack
**Ingest / Process & Understanding**. It acts as the bridge between legacy PDF archives and modern agentic knowledge bases.

## Typical use cases
- **Archive Migration**: Converting thousands of historical PDF reports into a clean, searchable Markdown repository.
- **Technical Document RAG**: Extracting structured data from dense manuals and whitepapers for high-precision retrieval.
- **Financial Statement Parsing**: Preserving table structures from annual reports to enable accurate multi-agent reasoning.

## Strengths
- **Layout Awareness**: Correctly identifies and parses multi-column text and floating images/tables.
- **Table Preservation**: Converts complex PDF tables into clean Markdown tables with high accuracy.
- **OCR Integration**: Seamlessly handles scanned PDFs via Tesseract or cloud-native OCR engines.
- **Scalable Batch Processing**: Optimized for multi-core performance when processing large document libraries.

## Limitations
- **Processing Time**: High-fidelity layout detection is slower than simple text extraction.
- **OCR Dependencies**: Performance on low-quality scans is heavily dependent on the chosen OCR engine.
- **Formatting Variability**: Extreme stylistic variations in PDFs can still lead to occasional parsing artifacts.

## When to use it
- When your RAG pipeline requires high precision for complex documents (legal, medical, or technical).
- When you need to process large batches of PDFs locally for privacy or cost reasons.
- When you need output that is specifically formatted for LLM consumption.

## When not to use it
- For simple, text-only PDFs where basic libraries like `PyPDF2` or `pdfplumber` are sufficient.
- When an official, structured source (like a LaTeX source or HTML version) is available.

## Getting started

### Installation
```bash
pip install opendataloader-pdf
```

### Basic Batch Conversion
```bash
# Convert all PDFs in a folder to markdown
opendataloader-pdf --input ./source_pdfs/ --output ./output_md/ --format md
```

## CLI examples
```bash
# Force layout-aware parsing for a complex 2-column paper
opendataloader-pdf --input paper.pdf --layout-aware --ocr-engine tesseract

# Extract only tables from a document as JSON
opendataloader-pdf --input report.pdf --extract tables --format json

# Process a directory with 4 parallel workers
opendataloader-pdf --input ./archive/ --output ./clean/ --parallel 4
```

## API examples

### Integration with LlamaIndex
Using OpenDataLoader's output to feed a vector index for Claude 4.8.

```python
from opendataloader_pdf import PDFConverter
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

# 1. Convert complex PDFs to AI-ready Markdown
converter = PDFConverter(layout_aware=True)
converter.convert_dir("./raw_docs", "./processed_md")

# 2. Ingest into LlamaIndex
reader = SimpleDirectoryReader("./processed_md")
documents = reader.load_data()
index = VectorStoreIndex.from_documents(documents)

# 3. Query with high confidence
query_engine = index.as_query_engine()
print(query_engine.query("What are the quarterly growth metrics in the table?"))
```

## Related tools / concepts
- [Docling](docling.md)
- [Docling MCP](docling-mcp.md)
- [Crawl4AI](crawl4ai.md)
- [LlamaParse](../intake_storage/llamaparse.md)
- [Unstructured.io](../intake_storage/unstructured.md)
- [RAG Patterns](../../knowledge_base/patterns/rag.md)
- [LlamaIndex](../ai_knowledge/llamaindex.md)

## Sources / references
- [OpenDataLoader GitHub Repository](https://github.com/opendataloader-project/opendataloader-pdf)
- [PDF to AI-Ready Data Best Practices](https://github.com/opendataloader-project/opendataloader-pdf/docs/best-practices.md)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high
