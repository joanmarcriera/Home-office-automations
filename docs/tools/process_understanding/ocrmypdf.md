# OCRmyPDF

## What it is
OCRmyPDF adds an OCR text layer to scanned PDF files, allowing them to be searched. It uses the Tesseract OCR engine (or alternative plugins like EasyOCR) and is highly configurable for various languages and document types. In the July 2026 agentic stack, it serves as a critical pre-processor for turning physical paper into structured, LLM-ready knowledge.

## What problem it solves
It makes scanned PDF documents searchable and indexable by adding a hidden text layer. This eliminates "dark data" in the homelab—documents that exist but cannot be searched or reasoned over by AI agents without expensive vision-based parsing on every access.

## Where it fits in the stack
**Ingestion & Processing**. Serves as the primary OCR processing layer for the document management pipeline, typically used as a sidecar or pre-processor for [Paperless-ngx](../../services/paperless-ngx.md).

## Typical use cases
- **Agentic Ingestion**: Automatically adding searchable text to scanned invoices for a [Gemma 3](../ai_knowledge/local_llms.md) agent to categorize.
- **Archival**: Batch processing legacy scanned documents to meet PDF/A long-term storage standards.
- **Pre-processing for RAG**: Ensuring high-quality text extraction before documents are chunked and vectorized in [RAGFlow](ragflow.md).
- **MCP 3.0 Integration**: Serving as a tool for agents using the MCP 3.0 Task Protocol to process documents on-demand.

## Strengths
- **PDF/A Support**: Produces standardized archival-grade files by default.
- **Hybrid Rendering**: Can preserve original images while placing OCR text accurately beneath them.
- **Parallel Processing**: Efficiently utilizes multi-core CPUs for high-volume document batches.
- **Plugin Architecture**: Support for advanced engines like [EasyOCR](https://github.com/ocrmypdf/OCRmyPDF-EasyOCR) for improved accuracy on complex layouts.

## Limitations
- **Visual Accuracy**: Still dependent on the underlying OCR engine's ability to handle low-contrast or degraded scans.
- **Computational Cost**: High-volume processing (especially with GPU-based plugins) requires significant system resources.
- **Handwriting**: While improving in v17.x+, it remains secondary to specialized models for dense cursive or script.

## When to use it
- When you have scanned PDFs that need to be searchable in [Paperless-ngx](../../services/paperless-ngx.md).
- When you need to standardize a collection of PDFs into a uniform, searchable format.
- When preparing documents for automated extraction by agents using [Instructor](../frameworks/instructor.md).

## When not to use it
- For "born-digital" PDFs that already contain a valid text layer.
- When you only need raw text extraction and don't need to preserve the PDF format (use [Tesseract](tesseract.md) or [Docling](docling.md) instead).

## Getting started

### Installation (Local)
OCRmyPDF requires several system dependencies (Tesseract, Ghostscript, Unpaper). On Linux/macOS:
```bash
# macOS
brew install ocrmypdf

# Ubuntu/Debian
sudo apt install ocrmypdf
```

### Installation (Docker)
Docker is the recommended way to avoid dependency conflicts:
```bash
docker pull jbarlow83/ocrmypdf:latest
```

## CLI examples

### Basic Searchable PDF Creation
```bash
# Creates a searchable PDF/A
ocrmypdf --language eng input_scanned.pdf output_searchable.pdf
```

### Advanced Cleaning and Deskewing
```bash
# Useful for low-quality home scans
ocrmypdf --deskew --clean --rotate-pages input.pdf output.pdf
```

### Docker Usage
```bash
docker run --rm -v "$(pwd):/home/docker" jbarlow83/ocrmypdf --language eng input.pdf output.pdf
```

## API examples

### Python Integration
OCRmyPDF can be used directly as a Python library for custom automation scripts.
```python
import ocrmypdf

def process_document(input_path, output_path):
    ocrmypdf.ocr(input_path, output_path, deskew=True, language=['eng'])

if __name__ == "__main__":
    process_document('scan.pdf', 'searchable.pdf')
```

## Related tools / concepts
- [Paperless-ngx](../../services/paperless-ngx.md) — Primary document management integration.
- [Tesseract CLI](tesseract.md) — The default underlying OCR engine.
- [Docling](docling.md) — High-performance document parsing for RAG.
- [Firecrawl](firecrawl.md) — Web-to-markdown extraction.
- [RAGFlow](ragflow.md) — Evaluation and vectorization platform.
- [Unstructured](../intake_storage/unstructured.md) — Broad-spectrum document partitioning.
- [LlamaParse](../intake_storage/llamaparse.md) — Advanced cloud-based PDF parsing.
- [Instructor](../frameworks/instructor.md) — Structured extraction from processed text.
- [Gemma 3](../ai_knowledge/local_llms.md) — Local LLM for reasoning over processed documents.

## Sources / references
- [Official Documentation](https://ocrmypdf.readthedocs.io/)
- [GitHub Repository](https://github.com/ocrmypdf/ocrmypdf)
- [v17.4 Release Notes](https://github.com/ocrmypdf/OCRmyPDF/releases)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high
