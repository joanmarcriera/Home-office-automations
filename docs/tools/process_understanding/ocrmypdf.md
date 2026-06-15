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
You can install OCRmyPDF via `pip` (requires system dependencies like Tesseract and Ghostscript) or use the official Docker image.

```bash
# Using pip
pip install ocrmypdf

# Using Docker (recommended for consistency)
docker pull jbarlow83/ocrmypdf
```

### Hello-world example
To perform basic OCR on a PDF and save the result:

```bash
ocrmypdf input.pdf output.pdf
```

## CLI examples

### Basic OCR with Docker
Run OCR on a local file using the Docker container:
```bash
docker run --rm -v "$(pwd):/home/docker" jbarlow83/ocrmypdf --language eng input.pdf output.pdf
```

### OCR with Image Pre-processing
Improve OCR quality by deskewing and cleaning the input image:
```bash
ocrmypdf --deskew --clean input.pdf output.pdf
```

### Force OCR on All Pages
Useful for PDFs that already have some text but require a full re-scan:
```bash
ocrmypdf --force-ocr input.pdf output.pdf
```

## API examples

### Python API Usage
OCRmyPDF provides a high-level `ocr` function that can be called directly from Python.

```python
import ocrmypdf

def run_ocr(input_path, output_path):
    ocrmypdf.ocr(
        input_path,
        output_path,
        deskew=True,
        optimize=1,
        sidecar='output.txt'
    )

if __name__ == "__main__":
    run_ocr('scanned_doc.pdf', 'searchable_doc.pdf')
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
