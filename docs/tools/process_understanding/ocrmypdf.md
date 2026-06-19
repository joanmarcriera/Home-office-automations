# OCRmyPDF

## What it is
OCRmyPDF adds an OCR text layer to scanned PDF files, allowing them to be searched. It uses the Tesseract OCR engine and is highly configurable for various languages and document types. In the 2026 agentic ecosystem, it serves as a critical pre-processor for multimodal LLMs like Claude 4.8 and GPT-5.5.

## What problem it solves
Makes scanned PDF documents searchable and indexable by adding a hidden text layer. This is essential for document management systems like Paperless-ngx and for feeding high-fidelity context into RAG (Retrieval-Augmented Generation) pipelines.

## Where it fits in the stack
**Infrastructure / Ingestion**. Serves as the OCR processing layer for the document management pipeline, typically used alongside Paperless-ngx and agentic scraping tools.

## Typical use cases
- Adding searchable text layers to scanned PDFs for Paperless-ngx ingestion.
- Batch processing scanned documents for archival and indexing in a private knowledge base.
- Pre-processing documents for LLM analysis in agentic workflows (e.g., invoice extraction).
- Converting image-only PDFs into accessible formats for screen readers.

## Strengths
- **High Quality**: Produces high-quality OCR output using the Tesseract engine.
- **Standards Compliant**: Generates valid PDF/A files for long-term archival.
- **Efficiency**: Preserves the original PDF structure while adding the text layer (no loss of original images).
- **Scalability**: Can be containerized and run in parallel for large document volumes.

## Limitations
- **Image Quality**: OCR quality depends heavily on scan quality and document complexity.
- **Resource Intensive**: Processing large batches can be CPU-intensive and requires significant VRAM if using advanced neural models.
- **Handwriting**: Tesseract may struggle with handwritten text or highly unusual fonts.

## When to use it
- When you need to make scanned PDFs searchable in a document management system.
- When preparing high-volume document archives for agentic ingestion.
- When you need a reliable, open-source bridge between physical scans and digital search.

## When not to use it
- When documents are already digital-native PDFs with embedded text layers.
- When you need OCR for non-PDF formats (use Tesseract directly or [Unstructured.io](https://unstructured.io/)).
- For complex visual-to-layout tasks where specialized models like Docling or LayoutLM are required.

## Getting started

### Installation
```bash
# Using pip (requires system dependencies like tesseract, ghostscript, unpaper)
pip install ocrmypdf

# Using Docker (recommended to avoid dependency issues)
docker pull jbarlow83/ocrmypdf
```

### Basic Setup
Ensure you have the required language packs installed for Tesseract if running locally.

## CLI examples

### Basic OCR with Docker
```bash
docker run --rm \
    -v "$(pwd):/home/docker" \
    jbarlow83/ocrmypdf \
    --language eng \
    input_scanned.pdf \
    output_searchable.pdf
```

### Batch Processing Script
```bash
for f in *.pdf; do
    docker run --rm -v "$(pwd):/home/docker" jbarlow83/ocrmypdf "$f" "ocr_$f"
done
```

### OCR with Deskew and Clean
```bash
ocrmypdf --deskew --clean --language eng input.pdf output.pdf
```

## API examples

### Modern Python API
```python
import ocrmypdf

if __name__ == '__main__':
    # Simple OCR call using the ocrmypdf module
    ocrmypdf.ocr(
        'input.pdf',
        'output.pdf',
        deskew=True,
        optimize=1,
        sidecar='output.txt'
    )
```

## Related tools / concepts
- [Paperless-ngx](../../services/paperless-ngx.md) (The primary destination for OCR'd docs)
- [Tesseract CLI](tesseract.md) (The underlying OCR engine)
- [Docling](docling.md) (Advanced document layout analysis)
- [Firecrawl](firecrawl.md) (Web scraping to PDF)
- [RAGFlow](ragflow.md) (Document-focused RAG platform)
- [Paperless AI](../../services/paperless-ai.md) (Agentic integration for Paperless)
- [Apache Tika](../../services/tika.md) (Content analysis and extraction)
- [Jules Agent](../ai_knowledge/jules.md) (Automation orchestration)

## Sources / references
- [GitHub Repository](https://github.com/ocrmypdf/OCRmyPDF)
- [OCRmyPDF Documentation](https://ocrmypdf.readthedocs.io/)
- [Tesseract OCR Home](https://tesseract-ocr.github.io/)

## Contribution Metadata
- Last reviewed: 2026-06-19
- Confidence: high
