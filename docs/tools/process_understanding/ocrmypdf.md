# OCRmyPDF

## What it is
OCRmyPDF adds an OCR text layer to scanned PDF files, allowing them to be searched. It uses the Tesseract OCR engine and is highly configurable for various languages and document types.

## What problem it solves
Makes scanned PDF documents searchable and indexable by adding a hidden text layer, which is essential for document management systems like Paperless-ngx.

## Where it fits in the stack
**Infrastructure**. Serves as the OCR processing layer for the document management pipeline, typically used alongside Paperless-ngx.

## Typical use cases
- Adding searchable text layers to scanned PDFs for Paperless-ngx ingestion
- Batch processing scanned documents for archival and indexing
- Preparing documents for full-text search in document management systems

## Strengths
- Produces high-quality OCR output using the Tesseract engine
- Supports multiple languages and configurable processing options
- Preserves the original PDF structure while adding the text layer

## Limitations
- OCR quality depends on scan quality and document complexity
- Processing large batches can be CPU-intensive
- Tesseract may struggle with handwritten text or unusual fonts

## When to use it
- When you need to make scanned PDFs searchable in a document management system
- When batch-processing scanned documents for archival

## When not to use it
- When documents are already digital-native PDFs with embedded text
- When you need OCR for non-PDF formats (use Tesseract directly or other tools)

## Getting started

### Installation
```bash
# Using pip
pip install ocrmypdf

# Using Docker (recommended to avoid dependency issues)
docker pull jbarlow83/ocrmypdf
```

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
from ocrmypdf import OcrOptions

if __name__ == '__main__':
    options = OcrOptions(
        input_file='input.pdf',
        output_file='output.pdf',
        deskew=True,
        languages=['eng'],
    )
    ocrmypdf.ocr(options)
```

## Related tools / concepts
- [Paperless AI](../../services/paperless-ai.md)
- [Tesseract CLI](tesseract.md)
- [Docling](docling.md)
- [Firecrawl](firecrawl.md)
- [RAGFlow](ragflow.md)

## Sources / references
- [GitHub Repository](https://github.com/ocrmypdf/OCRmyPDF)
- [OCRmyPDF Documentation](https://ocrmypdf.readthedocs.io/)

## Contribution Metadata
- Last reviewed: 2026-05-27
- Confidence: high
